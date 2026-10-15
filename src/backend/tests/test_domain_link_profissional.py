"""Testa invariantes, value objects e normalização da entidade de link profissional."""

import unittest
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
from backend.domain import (
    TAMANHO_MAXIMO_ROTULO_LINK,
    LinkProfissional,
    LinkProfissionalId,
    RegraDeDominioViolada,
    UsuarioId,
    normalizar_chave_rotulo_link,
    normalizar_chave_url,
    normalizar_rotulo_link,
    validar_e_normalizar_url_link,
)

ID_VALIDO = UUID("00000000-0000-0000-0000-000000000001")
USUARIO_ID_VALIDO = UUID("00000000-0000-0000-0000-000000000002")


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class LinkProfissionalIdTestCase(unittest.TestCase):
    """Verifica a integridade e construção do Value Object LinkProfissionalId.

    A suíte valida que instâncias válidas de UUID sejam aceitas e que tipos
    incompatíveis sejam prontamente rejeitados na instanciação. Ela existe para
    proteger a integridade da identidade de links profissionais.
    """

    def test_cria_link_profissional_id_com_uuid_valido(self) -> None:
        """Aceita UUID válido na criação de LinkProfissionalId.

        O cenário instancia LinkProfissionalId com um UUID padrão e confere o valor encapsulado.
        Ele existe para assegurar a construção correta do identificador de domínio.
        """
        link_id = LinkProfissionalId(ID_VALIDO)
        self.assertEqual(link_id.valor, ID_VALIDO)

    def test_rejeita_link_profissional_id_com_tipo_invalido(self) -> None:
        """Rejeita valor não UUID na criação de LinkProfissionalId.

        O cenário passa tipos inadequados (string, inteiro) e confirma o disparo
        de RegraDeDominioViolada. Ele existe para evitar contaminação do domínio.
        """
        with self.assertRaises(RegraDeDominioViolada):
            LinkProfissionalId("invalido")  # type: ignore[arg-type]


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class NormalizacaoLinkTestCase(unittest.TestCase):
    """Testa funções puras de validação e normalização de rótulo e URL de link profissional.

    A suíte cobre limites de caracteres, detecção de caracteres de controle,
    validação estrita de esquemas HTTP/HTTPS, validação de host e canonicidade de chave.
    Ela existe para certificar que a higienização de links seja determinística.
    """

    def test_normalizar_rotulo_link_apara_e_valida(self) -> None:
        """Apara espaços periféricos e aceita rótulo válido.

        O cenário passa texto com espaços no início e fim e valida que são removidos.
        Ele existe para manter descrições limpas no perfil.
        """
        resultado = normalizar_rotulo_link("  Portfólio no GitHub  ")
        self.assertEqual(resultado, "Portfólio no GitHub")

    def test_normalizar_rotulo_link_rejeita_nao_string(self) -> None:
        """Rejeita valores não textuais com RegraDeDominioViolada.

        O cenário passa um número no lugar de texto e confere a exceção.
        Ele existe para barrar tipos espúrios em tempo de execução.
        """
        with self.assertRaises(RegraDeDominioViolada):
            normalizar_rotulo_link(12345)  # type: ignore[arg-type]

    def test_normalizar_rotulo_link_rejeita_vazio(self) -> None:
        """Rejeita strings vazias ou formadas apenas por espaços.

        O cenário passa espaços e tabulações vazias e exige a exceção.
        Ele existe para garantir preenchimento de campos obrigatórios.
        """
        with self.assertRaises(RegraDeDominioViolada):
            normalizar_rotulo_link("   \t  ")

    def test_normalizar_rotulo_link_rejeita_caracteres_de_controle(self) -> None:
        """Rejeita caracteres de controle e quebras de linha no rótulo.

        O cenário insere caractere nulo ou quebra de linha e valida a rejeição.
        Ele existe para prevenir quebras de layout e injeções invisíveis.
        """
        with self.assertRaises(RegraDeDominioViolada):
            normalizar_rotulo_link("Link\x00Inválido")

        with self.assertRaises(RegraDeDominioViolada):
            normalizar_rotulo_link("Link\nCom Linha")

    def test_normalizar_rotulo_link_rejeita_tamanho_excessivo(self) -> None:
        """Rejeita rótulos cujo comprimento aparado ultrapasse 100 caracteres.

        O cenário gera string de 101 caracteres e valida o disparo da regra.
        Ele existe para impor o limite máximo definido para o rótulo.
        """
        with self.assertRaises(RegraDeDominioViolada):
            normalizar_rotulo_link("A" * (TAMANHO_MAXIMO_ROTULO_LINK + 1))

    def test_validar_url_link_aceita_http_e_https(self) -> None:
        """Aceita URLs válidas com esquemas HTTP e HTTPS.

        O cenário passa URLs completas com caminhos e parâmetros e confere o retorno.
        Ele existe para assegurar suporte pleno aos protocolos padrão da web.
        """
        url1 = validar_e_normalizar_url_link(
            "https://github.com/usuario/projeto?tab=readme"
        )
        self.assertEqual(url1, "https://github.com/usuario/projeto?tab=readme")

        url2 = validar_e_normalizar_url_link("HTTP://MEUSITE.COM/portfolio")
        self.assertEqual(url2, "http://MEUSITE.COM/portfolio")

    def test_validar_url_link_rejeita_nao_string(self) -> None:
        """Rejeita tipos não textuais passados para URL.

        O cenário passa tipos incorretos e confere o lançamento de RegraDeDominioViolada.
        Ele existe para impedir contaminação tipológica no domínio.
        """
        with self.assertRaises(RegraDeDominioViolada):
            validar_e_normalizar_url_link(None)  # type: ignore[arg-type]

    def test_validar_url_link_rejeita_vazio(self) -> None:
        """Rejeita URLs vazias ou compostas apenas de espaços.

        O cenário testa strings brancas e valida o disparo da exceção de domínio.
        Ele existe para garantir que todo link contenha destino obrigatório.
        """
        with self.assertRaises(RegraDeDominioViolada):
            validar_e_normalizar_url_link("   ")

    def test_validar_url_link_rejeita_caracteres_de_controle(self) -> None:
        """Rejeita URLs com quebras de linha ou caracteres de controle ASCII.

        O cenário injeta novas linhas e bytes nulos e exige RegraDeDominioViolada.
        Ele existe para mitigar injeções maliciosas de cabeçalhos e scripts.
        """
        with self.assertRaises(RegraDeDominioViolada):
            validar_e_normalizar_url_link("https://github.com/usuario\n")

        with self.assertRaises(RegraDeDominioViolada):
            validar_e_normalizar_url_link("https://github.com\x00/usuario")

    def test_validar_url_link_rejeita_tamanho_excessivo(self) -> None:
        """Rejeita URLs que ultrapassem o limite de 2048 caracteres.

        O cenário gera uma URL excessivamente longa e confere o erro de validação.
        Ele existe para respeitar o limite padrão de interoperabilidade web.
        """
        url_longa = "https://exemplo.com/" + "a" * 2040
        with self.assertRaises(RegraDeDominioViolada):
            validar_e_normalizar_url_link(url_longa)

    def test_validar_url_link_rejeita_esquemas_proibidos(self) -> None:
        """Rejeita esquemas perigosos ou não permitidos como javascript, data e file.

        O cenário testa injeções clássicas e protocolos inseguros e confirma bloqueio.
        Ele existe como barreira de segurança preventiva essencial.
        """
        esquemas_inseguros = [
            "javascript:alert(1)",
            "data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==",
            "file:///etc/passwd",
            "ftp://arquivos.exemplo.com",
            "mailto:aluno@exemplo.com",
        ]
        for url in esquemas_inseguros:
            with self.subTest(url=url):
                with self.assertRaises(RegraDeDominioViolada):
                    validar_e_normalizar_url_link(url)

    def test_validar_url_link_rejeita_sem_host(self) -> None:
        """Rejeita URLs sem netloc ou com host vazio.

        O cenário passa URLs apenas com esquema ou sem domínio válido.
        Ele existe para exigir links direcionados a domínios web legítimos.
        """
        urls_sem_host = [
            "https://",
            "http://",
            "https:///caminho",
            "http:///",
        ]
        for url in urls_sem_host:
            with self.subTest(url=url):
                with self.assertRaises(RegraDeDominioViolada):
                    validar_e_normalizar_url_link(url)

    def test_normalizar_chave_url_canonica(self) -> None:
        """Gera chave canônica uniforme para verificação de duplicidade.

        O cenário compara URLs com caixas misturadas e barras terminais e confere
        a equivalência canônica. Ele existe para garantir deduplicação robusta.
        """
        chave1 = normalizar_chave_url("HTTPS://GITHUB.COM/usuario/")
        chave2 = normalizar_chave_url("https://github.com/usuario")
        self.assertEqual(chave1, "https://github.com/usuario")
        self.assertEqual(chave1, chave2)

        chave_raiz = normalizar_chave_url("https://meusite.com/")
        self.assertEqual(chave_raiz, "https://meusite.com")

    def test_normalizar_chave_rotulo_link_colapsa_espacos(self) -> None:
        """Colapsa espaços múltiplos e aplica casefold ao rótulo.

        O cenário envia espaços múltiplos e caracteres misturados e valida a chave.
        Ele existe para dar suporte a comparações determinísticas de rótulo.
        """
        resultado = normalizar_chave_rotulo_link("  Portfólio   PESSOAL  ")
        self.assertEqual(resultado, "portfólio pessoal")


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class LinkProfissionalEntidadeTestCase(unittest.TestCase):
    """Testa a construção e as propriedades da entidade LinkProfissional.

    A suíte valida a integridade da entidade ao ser construída com dados válidos,
    o acionamento de invariantes e o cálculo de propriedades canônicas.
    Ela existe para garantir solidez da raiz de dados de link profissional.
    """

    def test_cria_link_profissional_valido(self) -> None:
        """Constrói entidade com campos válidos e confere atributos e chaves canônicas.

        O cenário instancia LinkProfissional com dados adequados e valida suas propriedades.
        Ele existe para demonstrar o ciclo de vida válido da entidade.
        """
        link = LinkProfissional(
            id=LinkProfissionalId(ID_VALIDO),
            usuario_id=UsuarioId(USUARIO_ID_VALIDO),
            rotulo="  GitHub Principal  ",
            url="  https://github.com/usuario/repo/  ",
        )
        self.assertEqual(link.id.valor, ID_VALIDO)
        self.assertEqual(link.usuario_id.valor, USUARIO_ID_VALIDO)
        self.assertEqual(link.rotulo, "GitHub Principal")
        self.assertEqual(link.url, "https://github.com/usuario/repo/")
        self.assertEqual(link.rotulo_normalizado, "github principal")
        self.assertEqual(link.url_normalizada, "https://github.com/usuario/repo")

    def test_rejeita_link_profissional_com_rotulo_invalido(self) -> None:
        """Rejeita criação de entidade quando o rótulo viola invariantes.

        O cenário passa rótulo vazio e valida o disparo de RegraDeDominioViolada.
        Ele existe para manter a entidade sempre íntegra.
        """
        with self.assertRaises(RegraDeDominioViolada):
            LinkProfissional(
                id=LinkProfissionalId(ID_VALIDO),
                usuario_id=UsuarioId(USUARIO_ID_VALIDO),
                rotulo="   ",
                url="https://github.com/usuario",
            )

    def test_rejeita_link_profissional_com_url_invalida(self) -> None:
        """Rejeita criação de entidade quando a URL viola invariantes ou esquemas permitidos.

        O cenário passa esquema malicioso e valida o bloqueio da entidade.
        Ele existe para blindar o domínio contra dados não autorizados.
        """
        with self.assertRaises(RegraDeDominioViolada):
            LinkProfissional(
                id=LinkProfissionalId(ID_VALIDO),
                usuario_id=UsuarioId(USUARIO_ID_VALIDO),
                rotulo="Link Inseguro",
                url="javascript:alert(1)",
            )


if __name__ == "__main__":
    unittest.main()
