"""Testa unitariamente as rotas HTTP de seleção e desseleção de itens da versão."""

import unittest
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from backend.api.itens_versao_curriculo import (
    SelecaoVersaoResposta,
    SelecionarItemRequisicao,
    criar_router,
)
from backend.application import (
    CurriculoNaoEncontrado,
    DesselecionarItemVersaoCurriculoEntrada,
    ItemNaoEncontrado,
    SelecionarItemVersaoCurriculoEntrada,
)
from backend.domain import (
    CompetenciaId,
    Curriculo,
    CurriculoId,
    DocumentoId,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    IdiomaId,
    ProjetoAcademicoId,
    ReferenciaCurriculo,
    RegraDeDominioViolada,
    UsuarioId,
)

# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001

CAMINHO_SELECAO = "/estudantes/{usuario_id}/curriculos/{curriculo_id}/itens"
CAMINHO_DESSELECAO = "/estudantes/{usuario_id}/curriculos/{curriculo_id}/itens/{tipo}/{item_id}"


class SelecionarItemExecutorDouble:
    """Substitui o caso de uso de seleção e registra as entradas recebidas.

    O double devolve um resultado ou levanta um erro pré-configurado, sem tocar
    portas, banco ou domínio de verdade. Ele existe para testar a tradução HTTP
    da rota isoladamente da orquestração da Application.
    """

    def __init__(self, resultado: Curriculo | None = None, erro: Exception | None = None) -> None:
        """Guarda o comportamento configurado e inicia o histórico de chamadas.

        O construtor não acessa recursos externos. Ele existe para permitir que
        cada teste configure sucesso ou falha de forma explícita.
        """
        self._resultado = resultado
        self._erro = erro
        self.entradas: list[SelecionarItemVersaoCurriculoEntrada] = []

    async def executar(self, entrada: SelecionarItemVersaoCurriculoEntrada) -> Curriculo:
        """Registra a entrada recebida e devolve o resultado ou levanta o erro.

        O método aguarda de forma trivial, sem I/O real. Ele existe para tornar
        observável o que o handler HTTP enviou ao caso de uso.
        """
        self.entradas.append(entrada)
        if self._erro is not None:
            raise self._erro
        if self._resultado is None:
            raise AssertionError("O double não recebeu resultado nem erro configurado.")
        return self._resultado


class DesselecionarItemExecutorDouble:
    """Substitui o caso de uso de desseleção e registra as entradas recebidas.

    O double devolve um resultado ou levanta um erro pré-configurado, sem tocar
    portas, banco ou domínio de verdade. Ele existe para testar a tradução HTTP
    da rota isoladamente da orquestração da Application.
    """

    def __init__(self, resultado: Curriculo | None = None, erro: Exception | None = None) -> None:
        """Guarda o comportamento configurado e inicia o histórico de chamadas.

        O construtor não acessa recursos externos. Ele existe para permitir que
        cada teste configure sucesso ou falha de forma explícita.
        """
        self._resultado = resultado
        self._erro = erro
        self.entradas: list[DesselecionarItemVersaoCurriculoEntrada] = []

    async def executar(self, entrada: DesselecionarItemVersaoCurriculoEntrada) -> Curriculo:
        """Registra a entrada recebida e devolve o resultado ou levanta o erro.

        O método aguarda de forma trivial, sem I/O real. Ele existe para tornar
        observável o que o handler HTTP enviou ao caso de uso.
        """
        self.entradas.append(entrada)
        if self._erro is not None:
            raise self._erro
        if self._resultado is None:
            raise AssertionError("O double não recebeu resultado nem erro configurado.")
        return self._resultado


def _rota(router: APIRouter, caminho: str, metodo: str):
    """Localiza a rota registrada para inspeção e chamada direta em teste.

    A função varre as rotas do router por caminho e método HTTP e devolve o
    objeto da rota, que expõe o endpoint e a configuração declarada. Ela existe
    para exercitar o handler sem iniciar servidor ASGI ou cliente HTTP real.
    """
    for rota in router.routes:
        if rota.path == caminho and metodo in rota.methods:
            return rota
    raise AssertionError(f"Rota {metodo} {caminho} não encontrada.")


def _criar_curriculo(usuario_id: UsuarioId, referencias: tuple[ReferenciaCurriculo, ...] = ()) -> Curriculo:
    """Cria uma versão de currículo válida, com a seleção informada, para o double.

    A função monta o agregado sem acessar gerador, banco ou relógio e inclui as
    referências recebidas. Ela existe para reduzir repetição mantendo cada teste
    focado na tradução HTTP.
    """
    curriculo = Curriculo(
        id=CurriculoId(uuid4()),
        usuario_id=usuario_id,
        titulo_versao="Estágio em TI",
        layout="classico",
        is_public=False,
    )
    for referencia in referencias:
        curriculo.incluir_referencia(referencia)
    return curriculo


class SelecionarItemRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução HTTP da seleção de item pela rota POST.

    A classe substitui o caso de uso por um double e observa o que a rota envia
    e devolve. Ela existe para testar a unidade de interface isoladamente da
    Application e da infraestrutura.
    """

    async def test_seleciona_item_e_devolve_a_selecao_atual_ordenada(self) -> None:
        """Confirma a resposta com a seleção ordenada e a entrada enviada ao caso de uso.

        O teste configura um double de sucesso com duas referências fora de
        ordem, chama o handler e compara a resposta pública e a entrada
        registrada. Ele existe para proteger o contrato de seleção.
        """
        usuario_id, projeto_id, idioma_id = uuid4(), uuid4(), uuid4()
        curriculo = _criar_curriculo(
            UsuarioId(usuario_id),
            (
                ReferenciaCurriculo(ProjetoAcademicoId(projeto_id)),
                ReferenciaCurriculo(IdiomaId(idioma_id)),
            ),
        )
        executor = SelecionarItemExecutorDouble(resultado=curriculo)
        selecionar = _rota(criar_router(executor, None), CAMINHO_SELECAO, "POST").endpoint

        resposta = await selecionar(
            usuario_id=usuario_id,
            curriculo_id=curriculo.id.valor,
            requisicao=SelecionarItemRequisicao(tipo="projeto_academico", item_id=projeto_id),
        )

        self.assertEqual(resposta.curriculo_id, curriculo.id.valor)
        self.assertEqual(
            [(item.tipo, item.item_id) for item in resposta.itens],
            [("idioma", idioma_id), ("projeto_academico", projeto_id)],
        )
        self.assertEqual(
            executor.entradas,
            [
                SelecionarItemVersaoCurriculoEntrada(
                    usuario_id=UsuarioId(usuario_id),
                    curriculo_id=curriculo.id,
                    referencia=ReferenciaCurriculo(ProjetoAcademicoId(projeto_id)),
                )
            ],
        )

    async def test_converte_cada_tipo_textual_na_referencia_de_dominio(self) -> None:
        """Confirma que os seis textos de tipo viram o identificador de domínio certo.

        O teste repete a chamada para cada tipo aceito e observa a referência
        entregue ao caso de uso. Ele existe para proteger o vocabulário do
        transporte contra trocas entre tipos de item.
        """
        esperados: dict[str, type] = {
            "formacao_academica": FormacaoAcademicaId,
            "experiencia_profissional": ExperienciaProfissionalId,
            "projeto_academico": ProjetoAcademicoId,
            "competencia": CompetenciaId,
            "idioma": IdiomaId,
            "documento": DocumentoId,
        }
        for tipo, classe in esperados.items():
            with self.subTest(tipo=tipo):
                usuario_id, item_id = uuid4(), uuid4()
                executor = SelecionarItemExecutorDouble(resultado=_criar_curriculo(UsuarioId(usuario_id)))
                selecionar = _rota(criar_router(executor, None), CAMINHO_SELECAO, "POST").endpoint

                await selecionar(
                    usuario_id=usuario_id,
                    curriculo_id=uuid4(),
                    requisicao=SelecionarItemRequisicao(tipo=tipo, item_id=item_id),  # type: ignore[arg-type]
                )

                self.assertEqual(executor.entradas[0].referencia, ReferenciaCurriculo(classe(item_id)))

    async def test_declara_status_201_e_resposta_publica(self) -> None:
        """Confirma o status de sucesso e o modelo de resposta declarados na rota.

        O teste inspeciona a configuração da rota registrada, já que a chamada
        direta ao handler não passa pela camada que aplica o status. Ele existe
        para proteger o contrato HTTP de seleção.
        """
        rota = _rota(criar_router(None, None), CAMINHO_SELECAO, "POST")

        self.assertEqual(rota.status_code, 201)
        self.assertIs(rota.response_model, SelecaoVersaoResposta)

    async def test_indisponivel_quando_executor_ausente(self) -> None:
        """Confirma 503 quando nenhum caso de uso de seleção foi injetado.

        O teste chama o handler sem executor e observa a indisponibilidade
        explícita antes de qualquer outra decisão.
        """
        selecionar = _rota(criar_router(None, None), CAMINHO_SELECAO, "POST").endpoint

        with self.assertRaises(HTTPException) as contexto:
            await selecionar(
                usuario_id=uuid4(),
                curriculo_id=uuid4(),
                requisicao=SelecionarItemRequisicao(tipo="idioma", item_id=uuid4()),
            )

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_ausencia_de_versao_ou_de_item_vira_404(self) -> None:
        """Confirma 404 tanto para versão ausente quanto para item ausente ou alheio.

        O teste configura o double para cada falha de não encontrado e observa a
        tradução HTTP preservando a mensagem. Ele existe para proteger a negação
        sem revelar a diferença entre ausência e propriedade alheia.
        """
        for erro in (CurriculoNaoEncontrado("Versão de currículo não encontrada."), ItemNaoEncontrado("Item do perfil não encontrado.")):
            with self.subTest(erro=type(erro).__name__):
                executor = SelecionarItemExecutorDouble(erro=erro)
                selecionar = _rota(criar_router(executor, None), CAMINHO_SELECAO, "POST").endpoint

                with self.assertRaises(HTTPException) as contexto:
                    await selecionar(
                        usuario_id=uuid4(),
                        curriculo_id=uuid4(),
                        requisicao=SelecionarItemRequisicao(tipo="idioma", item_id=uuid4()),
                    )

                self.assertEqual(contexto.exception.status_code, 404)
                self.assertEqual(contexto.exception.detail, str(erro))

    async def test_violacao_de_dominio_vira_422(self) -> None:
        """Confirma 422 quando o caso de uso sinaliza violação de regra de domínio.

        O teste configura o double para levantar a falha de duplicidade e observa
        a tradução HTTP preservando a mensagem. Ele existe para proteger o
        mapeamento de erro da fronteira.
        """
        executor = SelecionarItemExecutorDouble(erro=RegraDeDominioViolada("Item já está incluído no currículo."))
        selecionar = _rota(criar_router(executor, None), CAMINHO_SELECAO, "POST").endpoint

        with self.assertRaises(HTTPException) as contexto:
            await selecionar(
                usuario_id=uuid4(),
                curriculo_id=uuid4(),
                requisicao=SelecionarItemRequisicao(tipo="idioma", item_id=uuid4()),
            )

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(contexto.exception.detail, "Item já está incluído no currículo.")


class SelecionarItemRequisicaoTestCase(unittest.TestCase):
    """Verifica a validação estrutural do DTO de seleção na fronteira.

    A classe constrói o DTO com dados fora do formato esperado. Ela existe para
    proteger o vocabulário de tipos e o formato do identificador antes de
    qualquer chamada ao caso de uso.
    """

    def test_rejeita_tipo_desconhecido_e_identificador_invalido(self) -> None:
        """Confirma que tipo fora do vocabulário ou id malformado não formam requisição.

        O teste tenta construir o DTO com um tipo inexistente e com um
        identificador que não é UUID, observando a falha de validação estrutural,
        que o framework traduziria em 422.
        """
        with self.assertRaises(ValidationError):
            SelecionarItemRequisicao(tipo="certificado", item_id=uuid4())  # type: ignore[arg-type]
        with self.assertRaises(ValidationError):
            SelecionarItemRequisicao(tipo="idioma", item_id="nao-e-uuid")  # type: ignore[arg-type]


class DesselecionarItemRotaTestCase(unittest.IsolatedAsyncioTestCase):
    """Verifica a tradução HTTP da desseleção de item pela rota DELETE.

    A classe substitui o caso de uso por um double e observa o que a rota envia
    e devolve. Ela existe para testar a unidade de interface isoladamente da
    Application e da infraestrutura.
    """

    async def test_desseleciona_item_e_envia_a_entrada_correta_sem_conteudo(self) -> None:
        """Confirma a entrada enviada ao caso de uso e a ausência de corpo na resposta.

        O teste chama o handler com um tipo e um id de item e compara a entrada
        registrada no double, além do retorno vazio. Ele existe para proteger o
        contrato de desseleção.
        """
        usuario_id, item_id = uuid4(), uuid4()
        curriculo = _criar_curriculo(UsuarioId(usuario_id))
        executor = DesselecionarItemExecutorDouble(resultado=curriculo)
        desselecionar = _rota(criar_router(None, executor), CAMINHO_DESSELECAO, "DELETE").endpoint

        resultado = await desselecionar(
            usuario_id=usuario_id,
            curriculo_id=curriculo.id.valor,
            tipo="idioma",
            item_id=item_id,
        )

        self.assertIsNone(resultado)
        self.assertEqual(
            executor.entradas,
            [
                DesselecionarItemVersaoCurriculoEntrada(
                    usuario_id=UsuarioId(usuario_id),
                    curriculo_id=curriculo.id,
                    referencia=ReferenciaCurriculo(IdiomaId(item_id)),
                )
            ],
        )

    async def test_declara_status_204(self) -> None:
        """Confirma o status de sucesso sem conteúdo declarado na rota.

        O teste inspeciona a configuração da rota registrada, já que a chamada
        direta ao handler não passa pela camada que aplica o status. Ele existe
        para proteger o contrato HTTP de desseleção.
        """
        rota = _rota(criar_router(None, None), CAMINHO_DESSELECAO, "DELETE")

        self.assertEqual(rota.status_code, 204)

    async def test_indisponivel_quando_executor_ausente(self) -> None:
        """Confirma 503 quando nenhum caso de uso de desseleção foi injetado.

        O teste chama o handler sem executor e observa a indisponibilidade
        explícita antes de qualquer outra decisão.
        """
        desselecionar = _rota(criar_router(None, None), CAMINHO_DESSELECAO, "DELETE").endpoint

        with self.assertRaises(HTTPException) as contexto:
            await desselecionar(usuario_id=uuid4(), curriculo_id=uuid4(), tipo="idioma", item_id=uuid4())

        self.assertEqual(contexto.exception.status_code, 503)

    async def test_ausencia_de_versao_vira_404(self) -> None:
        """Confirma 404 quando o caso de uso sinaliza versão ausente ou alheia.

        O teste configura o double para a falha de não encontrado e observa a
        tradução HTTP preservando a mensagem. Ele existe para proteger a negação
        sem revelar a diferença entre ausência e propriedade alheia.
        """
        executor = DesselecionarItemExecutorDouble(erro=CurriculoNaoEncontrado("Versão de currículo não encontrada."))
        desselecionar = _rota(criar_router(None, executor), CAMINHO_DESSELECAO, "DELETE").endpoint

        with self.assertRaises(HTTPException) as contexto:
            await desselecionar(usuario_id=uuid4(), curriculo_id=uuid4(), tipo="idioma", item_id=uuid4())

        self.assertEqual(contexto.exception.status_code, 404)

    async def test_violacao_de_dominio_vira_422(self) -> None:
        """Confirma 422 quando o caso de uso sinaliza item não selecionado.

        O teste configura o double para levantar a violação de domínio e observa
        a tradução HTTP preservando a mensagem. Ele existe para proteger o
        mapeamento de erro da fronteira.
        """
        executor = DesselecionarItemExecutorDouble(erro=RegraDeDominioViolada("Item não está incluído no currículo."))
        desselecionar = _rota(criar_router(None, executor), CAMINHO_DESSELECAO, "DELETE").endpoint

        with self.assertRaises(HTTPException) as contexto:
            await desselecionar(usuario_id=uuid4(), curriculo_id=uuid4(), tipo="idioma", item_id=uuid4())

        self.assertEqual(contexto.exception.status_code, 422)
        self.assertEqual(contexto.exception.detail, "Item não está incluído no currículo.")
