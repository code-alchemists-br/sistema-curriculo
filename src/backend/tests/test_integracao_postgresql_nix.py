"""Valida a disponibilidade do PostgreSQL efêmero no ambiente de integração."""

import os
import unittest

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from backend.tests.fixtures.credenciais_sessao import solicitar_asgi


@unittest.skipUnless(
    os.environ.get("DATABASE_URL"),
    "Requer DATABASE_URL fornecida pelo executor de integração PostgreSQL.",
)
class PostgreSqlNixIntegracaoTestCase(unittest.IsolatedAsyncioTestCase):
    """Confirma o contrato de conexão do PostgreSQL oferecido pelo shell Nix.

    O caso usa a URL temporária preparada pelo executor, conecta pelo driver
    assíncrono e consulta o banco criado para a execução. Ele existe para
    impedir que a CI sinalize integração verde sem disponibilizar um servidor
    PostgreSQL funcional para os testes que dependem dele.
    """

    async def test_main_crud_experiencias_com_sessao_e_postgresql_reais(self) -> None:
        """Exercita todas as operações de experiência com conta e cookie reais.

        Valida documentação, autenticação, propriedade, cadastro, edição e
        exclusão lógica com consultas independentes para impedir regressão dos
        executores ausentes ou sucesso sem persistência confirmada.
        """
        from uuid import UUID

        from sqlalchemy import select

        from backend.infrastructure.persistence.sqlalchemy.experiencia_profissional import (
            ExperienciaProfissionalRegistro,
        )
        from backend.main import _engine_persistencia, app

        documento = app.openapi()
        rota = documento["paths"]["/experiencias-profissionais"]
        self.assertIn("post", rota)
        self.assertEqual(rota["post"]["tags"], rota["get"]["tags"])
        rota_item = documento["paths"]["/experiencias-profissionais/{experiencia_id}"]
        self.assertTrue({"put", "delete"} <= set(rota_item))
        dados_conta = {
            "nome": "Ana Experiência", "email": "ana.experiencia@example.test",
            "senha": "Senha-Integracao-123",
        }
        conta = await solicitar_asgi(app, "POST", "/estudantes", dados=dados_conta)
        self.assertEqual(conta.status, 201)
        acesso = await solicitar_asgi(
            app, "POST", "/acessos",
            dados={"email": dados_conta["email"], "senha": dados_conta["senha"]},
        )
        self.assertEqual(acesso.status, 204)
        token = acesso.cookie_sessao().value
        dados = {
            "empresa": "Empresa Exemplo", "cargo": "Desenvolvedora",
            "descricao": "Desenvolvimento de aplicações.",
            "data_inicio": "2024-02-01", "data_fim": None,
        }
        anonima = await solicitar_asgi(app, "POST", "/experiencias-profissionais", dados=dados)
        self.assertEqual(anonima.status, 401)
        criada = await solicitar_asgi(app, "POST", "/experiencias-profissionais", dados=dados, token=token)
        self.assertEqual(criada.status, 201)
        identidade = UUID(criada.json()["id"])
        self.assertEqual(identidade.version, 4)
        listada = await solicitar_asgi(app, "GET", "/experiencias-profissionais", token=token)
        self.assertEqual(listada.status, 200)
        self.assertEqual(listada.json(), {"experiencias": [criada.json()]})
        invalida = await solicitar_asgi(
            app, "POST", "/experiencias-profissionais",
            dados={**dados, "data_fim": "2023-01-01"}, token=token,
        )
        self.assertEqual(invalida.status, 422)
        tabela = ExperienciaProfissionalRegistro.__table__
        async with _engine_persistencia.connect() as conexao:
            registros = (await conexao.execute(
                select(tabela).where(tabela.c.usuario_id == UUID(criada.json()["usuario_id"]))
            )).mappings().all()
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0]["id"], identidade)
        self.assertEqual(registros[0]["empresa"], dados["empresa"])

        caminho = f"/experiencias-profissionais/{identidade}"
        for metodo in ("PUT", "DELETE"):
            sem_sessao = await solicitar_asgi(
                app, metodo, caminho, dados=dados if metodo == "PUT" else None
            )
            self.assertEqual(sem_sessao.status, 401)

        outra_conta = {**dados_conta, "email": "outra.experiencia@example.test"}
        segunda = await solicitar_asgi(app, "POST", "/estudantes", dados=outra_conta)
        self.assertEqual(segunda.status, 201)
        outro_acesso = await solicitar_asgi(
            app, "POST", "/acessos",
            dados={"email": outra_conta["email"], "senha": outra_conta["senha"]},
        )
        self.assertEqual(outro_acesso.status, 204)
        outro_token = outro_acesso.cookie_sessao().value
        for metodo in ("PUT", "DELETE"):
            alheia = await solicitar_asgi(
                app, metodo, caminho, token=outro_token,
                dados=dados if metodo == "PUT" else None,
            )
            self.assertEqual(alheia.status, 404)
        preservada = await solicitar_asgi(app, "GET", "/experiencias-profissionais", token=token)
        self.assertEqual(preservada.json(), {"experiencias": [criada.json()]})

        novos_dados = {**dados, "cargo": "Desenvolvedora Sênior", "data_fim": "2026-01-01"}
        editada = await solicitar_asgi(app, "PUT", caminho, dados=novos_dados, token=token)
        self.assertEqual(editada.status, 200)
        self.assertEqual(editada.json()["id"], str(identidade))
        self.assertEqual(editada.json()["cargo"], novos_dados["cargo"])
        listada = await solicitar_asgi(app, "GET", "/experiencias-profissionais", token=token)
        self.assertEqual(listada.json(), {"experiencias": [editada.json()]})
        async with _engine_persistencia.connect() as conexao:
            registro = (await conexao.execute(select(tabela).where(tabela.c.id == identidade))).mappings().one()
            self.assertEqual(registro["cargo"], novos_dados["cargo"])

        instante = None
        for _ in range(2):
            excluida = await solicitar_asgi(app, "DELETE", caminho, token=token)
            self.assertEqual(excluida.status, 204)
            self.assertEqual(excluida.corpo, b"")
            async with _engine_persistencia.connect() as conexao:
                registro = (await conexao.execute(select(tabela).where(tabela.c.id == identidade))).mappings().one()
            self.assertIsNotNone(registro["deleted_at"])
            if instante is None:
                instante = registro["deleted_at"]
            self.assertEqual(registro["deleted_at"], instante)
        listada = await solicitar_asgi(app, "GET", "/experiencias-profissionais", token=token)
        self.assertEqual(listada.json(), {"experiencias": []})
        editada_excluida = await solicitar_asgi(app, "PUT", caminho, dados=novos_dados, token=token)
        self.assertEqual(editada_excluida.status, 404)

    async def test_main_cadastra_edita_e_exclui_formacao_com_sessao_real(self) -> None:
        """Valida o fluxo HTTP composto pelo Uvicorn no PostgreSQL migrado.

        Cadastra conta, autentica por cookie e confere cada escrita em consulta
        independente para impedir sucesso HTTP sem commit e preservar exclusão.
        """
        from uuid import UUID

        from sqlalchemy import select

        from backend.infrastructure.persistence.sqlalchemy.formacao_academica import (
            FormacaoAcademicaRegistro,
        )
        from backend.main import _engine_persistencia, app

        dados = {
            "nome": "Ana Formação",
            "email": "ana.formacao@example.test",
            "senha": "Senha-Integracao-123",
        }
        conta = await solicitar_asgi(app, "POST", "/estudantes", dados=dados)
        self.assertEqual(conta.status, 201)
        acesso = await solicitar_asgi(
            app, "POST", "/acessos",
            dados={"email": dados["email"], "senha": dados["senha"]},
        )
        self.assertEqual(acesso.status, 204)
        token = acesso.cookie_sessao().value
        formacao = {
            "instituicao": "Universidade Local",
            "curso": "Computação",
            "nivel": "graduacao",
            "data_inicio": "2024-02-01",
            "data_fim": None,
            "status": "em_andamento",
        }
        criada = await solicitar_asgi(
            app, "POST", "/formacoes-academicas", dados=formacao, token=token
        )
        self.assertEqual(criada.status, 201)
        identidade = UUID(criada.json()["id"])
        caminho = f"/formacoes-academicas/{identidade}"
        tabela = FormacaoAcademicaRegistro.__table__
        consulta = select(tabela).where(tabela.c.id == identidade)
        async with _engine_persistencia.connect() as conexao:
            registro = (await conexao.execute(consulta)).mappings().one()
            self.assertEqual(registro["curso"], formacao["curso"])

        formacao["curso"] = "Engenharia de Computação"
        editada = await solicitar_asgi(app, "PUT", caminho, dados=formacao, token=token)
        self.assertEqual(editada.status, 200)
        async with _engine_persistencia.connect() as conexao:
            registro = (await conexao.execute(consulta)).mappings().one()
            self.assertEqual(registro["curso"], formacao["curso"])

        for _ in range(2):
            excluida = await solicitar_asgi(app, "DELETE", caminho, token=token)
            self.assertEqual(excluida.status, 204)
        async with _engine_persistencia.connect() as conexao:
            registro = (await conexao.execute(consulta)).mappings().one()
            self.assertIsNotNone(registro["deleted_at"])
        editada = await solicitar_asgi(app, "PUT", caminho, dados=formacao, token=token)
        self.assertEqual(editada.status, 404)

    async def test_conecta_ao_banco_temporario_exposto_pelo_executor(self) -> None:
        """Consulta o banco efêmero usando a URL fornecida pelo executor.

        O cenário cria uma engine assíncrona, verifica o nome do banco atual e
        sempre libera a conexão ao finalizar. Ele existe para validar servidor,
        socket e driver PostgreSQL juntos, antes dos cenários de persistência.
        """
        database_url = os.environ.get("DATABASE_URL")
        self.assertIsNotNone(database_url)
        assert database_url is not None
        engine = create_async_engine(database_url)
        self.addAsyncCleanup(engine.dispose)

        async with engine.connect() as connection:
            database_name = await connection.scalar(text("SELECT current_database()"))

        self.assertEqual(database_name, "sistema_curriculo_test")

    async def test_aplicacao_composta_cadastra_conta_e_recusa_email_duplicado(
        self,
    ) -> None:
        """Exercita o cadastro da aplicação real contra PostgreSQL migrado.

        O cenário importa a aplicação somente após o executor definir a URL,
        envia duas requisições HTTP ASGI pela rota pública e repete o e-mail.
        Ele existe para impedir que o cadastro volte a receber dependências
        ausentes ou responda sucesso sem persistir a conta.
        """
        from backend.main import app

        dados = {
            "nome": "Ana Integração",
            "email": "ana.integracao@example.test",
            "senha": "Senha-Integracao-123",
        }
        primeira = await solicitar_asgi(app, "POST", "/estudantes", dados=dados)
        repetida = await solicitar_asgi(app, "POST", "/estudantes", dados=dados)
        acesso = await solicitar_asgi(
            app,
            "POST",
            "/acessos",
            dados={"email": dados["email"], "senha": dados["senha"]},
        )

        self.assertEqual(primeira.status, 201)
        self.assertEqual(repetida.status, 409)
        self.assertEqual(acesso.status, 204)
        self.assertTrue(acesso.cabecalhos("set-cookie"))

    async def test_main_versao_curriculo_modelo_selecao_previa_e_decisao_com_postgresql_real(
        self,
    ) -> None:
        """Exercita escolha de modelo, seleção, prévia, revisão e decisão ponta a ponta.

        Cria conta e sessão reais, uma formação e uma versão do currículo, troca o
        modelo, seleciona e desseleciona o item, lê prévia e revisão, registra a
        decisão e confere o banco por consulta independente, além de recusar outra
        conta. Ele existe para impedir que as rotas de versão voltem a ficar sem
        executor (503) ou a responder sucesso sem gravar, já que os demais testes
        de currículo usam SQLite e dublês.
        """
        from uuid import UUID

        from sqlalchemy import text

        from backend.main import _engine_persistencia, app

        dados_conta = {
            "nome": "Bia Modelo",
            "email": "bia.modelo@example.test",
            "senha": "Senha-Integracao-123",
        }
        conta = await solicitar_asgi(app, "POST", "/estudantes", dados=dados_conta)
        self.assertEqual(conta.status, 201)
        usuario_id = conta.json()["id"]
        acesso = await solicitar_asgi(
            app, "POST", "/acessos",
            dados={"email": dados_conta["email"], "senha": dados_conta["senha"]},
        )
        self.assertEqual(acesso.status, 204)
        token = acesso.cookie_sessao().value

        formacao = await solicitar_asgi(
            app, "POST", "/formacoes-academicas", token=token,
            dados={
                "instituicao": "UFRJ", "curso": "Sistemas de Informação",
                "nivel": "graduacao", "data_inicio": "2022-02-01",
                "data_fim": None, "status": "em_andamento",
            },
        )
        self.assertEqual(formacao.status, 201)
        formacao_id = formacao.json()["id"]

        base = f"/estudantes/{usuario_id}/curriculos"
        criada = await solicitar_asgi(
            app, "POST", base, token=token,
            dados={"titulo_versao": "Versão TI", "layout": "moderno", "is_public": False},
        )
        self.assertEqual(criada.status, 201)
        curriculo_id = criada.json()["id"]
        self.assertEqual(criada.json()["layout"], "moderno")
        caminho = f"{base}/{curriculo_id}"

        editada = await solicitar_asgi(
            app, "PUT", caminho, token=token,
            dados={"titulo_versao": "Versão TI", "layout": "academico", "is_public": False},
        )
        self.assertEqual(editada.status, 200)
        listada = await solicitar_asgi(app, "GET", base, token=token)
        self.assertEqual(listada.status, 200)
        self.assertEqual(
            [(v["id"], v["layout"]) for v in listada.json()["versoes"]],
            [(curriculo_id, "academico")],
        )

        item = {"tipo": "formacao_academica", "item_id": formacao_id}
        selecionada = await solicitar_asgi(
            app, "POST", f"{caminho}/itens", token=token, dados=item
        )
        self.assertEqual(selecionada.status, 201)
        duplicada = await solicitar_asgi(
            app, "POST", f"{caminho}/itens", token=token, dados=item
        )
        self.assertEqual(duplicada.status, 422)
        inexistente = await solicitar_asgi(
            app, "POST", f"{caminho}/itens", token=token,
            dados={**item, "item_id": "00000000-0000-4000-8000-000000000999"},
        )
        self.assertEqual(inexistente.status, 404)
        async with _engine_persistencia.connect() as conexao:
            gravados = await conexao.scalar(
                text("SELECT count(*) FROM curriculo_itens WHERE curriculo_id = :c"),
                {"c": UUID(curriculo_id)},
            )
        self.assertEqual(gravados, 1)

        ordem = [
            "dados-pessoais", "formacao-academica", "experiencias-profissionais",
            "projetos-academicos", "competencias", "idiomas",
            "documentos-complementares",
        ]
        reordenada = await solicitar_asgi(
            app, "PUT", f"{caminho}/ordem-secoes", token=token,
            dados={"ordem_secoes": ordem},
        )
        self.assertEqual(reordenada.status, 204)

        previa = await solicitar_asgi(app, "GET", f"{caminho}/previa", token=token)
        self.assertEqual(previa.status, 200)
        self.assertEqual(previa.json()["layout"], "academico")
        self.assertEqual(
            [f["id"] for f in previa.json()["formacoes"]], [formacao_id]
        )

        revisao = await solicitar_asgi(app, "GET", f"{caminho}/revisao", token=token)
        self.assertEqual(revisao.status, 200)
        self.assertFalse(revisao.json()["aprovado"])
        codigos = {p["codigo"] for p in revisao.json()["pendencias"]}
        self.assertIn("EXPERIENCIA_AUSENTE", codigos)

        decidida = await solicitar_asgi(
            app, "PUT", f"{caminho}/recomendacoes/PROJETO_AUSENTE", token=token,
            dados={"decisao": "aceita"},
        )
        self.assertEqual(decidida.status, 200)
        decisoes = await solicitar_asgi(
            app, "GET", f"{caminho}/recomendacoes", token=token
        )
        self.assertEqual(decisoes.status, 200)
        self.assertEqual(
            [(d["codigo"], d["decisao"]) for d in decisoes.json()["decisoes"]],
            [("PROJETO_AUSENTE", "aceita")],
        )

        outra_conta = {**dados_conta, "email": "outra.modelo@example.test"}
        self.assertEqual(
            (await solicitar_asgi(app, "POST", "/estudantes", dados=outra_conta)).status,
            201,
        )
        outro_acesso = await solicitar_asgi(
            app, "POST", "/acessos",
            dados={"email": outra_conta["email"], "senha": outra_conta["senha"]},
        )
        outro_token = outro_acesso.cookie_sessao().value
        alheia = await solicitar_asgi(app, "GET", base, token=outro_token)
        self.assertEqual(alheia.status, 403)

        desselecionada = await solicitar_asgi(
            app, "DELETE", f"{caminho}/itens/formacao_academica/{formacao_id}",
            token=token,
        )
        self.assertEqual(desselecionada.status, 204)
        async with _engine_persistencia.connect() as conexao:
            restantes = await conexao.scalar(
                text("SELECT count(*) FROM curriculo_itens WHERE curriculo_id = :c"),
                {"c": UUID(curriculo_id)},
            )
        self.assertEqual(restantes, 0)

        excluida = await solicitar_asgi(app, "DELETE", caminho, token=token)
        self.assertEqual(excluida.status, 204)
        vazia = await solicitar_asgi(app, "GET", base, token=token)
        self.assertEqual(vazia.json(), {"versoes": []})
