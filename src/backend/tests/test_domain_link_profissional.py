"""Testa invariantes, value objects e normalização da entidade de link profissional."""

import unittest
from uuid import UUID

# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
from backend.domain import (
    TAMANHO_MAXIMO_ROTULO_LINK,
    TAMANHO_MAXIMO_URL_LINK,
    CertificacaoId,
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

    def test_rejeita_identidade_de_outro_tipo(self) -> None:
        """Impede usar como identidade um ID de outro item ou um UUID cru.

        O cenário fornece ``CertificacaoId`` e ``UUID`` no lugar do
        ``LinkProfissionalId``. Ele existe para que o link nunca receba a
        identidade de outro tipo de item do perfil.
        """
        for identidade in (CertificacaoId(ID_VALIDO), ID_VALIDO):
            with self.subTest(identidade=type(identidade).__name__):
                with self.assertRaises(RegraDeDominioViolada):
                    LinkProfissional(
                        id=identidade,  # type: ignore[arg-type]
                        usuario_id=UsuarioId(USUARIO_ID_VALIDO),
                        rotulo="GitHub",
                        url="https://github.com/usuario",
                    )

    def test_rejeita_proprietario_ausente_ou_de_outro_tipo(self) -> None:
        """Impede link sem dono ou com dono não tipado.

        O cenário fornece ``None`` e um ``UUID`` cru no lugar do ``UsuarioId``.
        Ele existe para que todo link pertença a um estudante válido.
        """
        for proprietario in (None, USUARIO_ID_VALIDO):
            with self.subTest(proprietario=proprietario):
                with self.assertRaises(RegraDeDominioViolada):
                    LinkProfissional(
                        id=LinkProfissionalId(ID_VALIDO),
                        usuario_id=proprietario,  # type: ignore[arg-type]
                        rotulo="GitHub",
                        url="https://github.com/usuario",
                    )


class ValidacaoEndurecidaUrlLinkTestCase(unittest.TestCase):
    """Verifica as regras de host, credenciais, espaços e porta da URL do link.

    Os cenários cobrem URLs que eram aceitas indevidamente e URLs legítimas que
    precisam continuar válidas. A classe existe para garantir que o link
    aponte para um destino real e não exponha credenciais.
    """

    def test_rejeita_url_sem_host_real(self) -> None:
        """Recusa URLs cujo host é ausente ou formado só por pontuação.

        O cenário usa netlocs não vazios mas sem host de verdade. Ele existe
        para impedir links sem destino que passavam pela checagem de netloc.
        """
        for url in ("http://:80", "https://@", "https://.", "https://-", "https://exem_plo.com"):
            with self.subTest(url=url):
                with self.assertRaises(RegraDeDominioViolada):
                    validar_e_normalizar_url_link(url)

    def test_rejeita_usuario_e_senha_embutidos(self) -> None:
        """Recusa URLs com credenciais ou com ``@`` disfarçando o domínio real.

        O cenário inclui usuário, usuário e senha e o truque de domínio falso
        antes do ``@``. Ele existe para não vazar credenciais no currículo nem
        permitir links enganosos.
        """
        for url in (
            "https://user:senha@site.com",
            "https://user@site.com",
            "https://banco.com@site-falso.com",
        ):
            with self.subTest(url=url):
                with self.assertRaises(RegraDeDominioViolada):
                    validar_e_normalizar_url_link(url)

    def test_rejeita_espacos_internos(self) -> None:
        """Recusa espaços no host ou no caminho da URL.

        O cenário coloca espaço em diferentes partes da URL já aparada. Ele
        existe para exigir que espaços sejam codificados como ``%20``.
        """
        for url in (
            "https://exa mple.com",
            "https://exemplo.com/caminho com espaco",
            "https://exemplo.com/?q=a b",
        ):
            with self.subTest(url=url):
                with self.assertRaises(RegraDeDominioViolada):
                    validar_e_normalizar_url_link(url)

    def test_rejeita_porta_invalida(self) -> None:
        """Recusa porta não numérica, zero ou acima de 65535.

        O cenário usa portas fora do intervalo válido. Ele existe para que o
        link sempre aponte para um endereço utilizável.
        """
        for url in ("http://host.com:abc", "http://host.com:0", "http://host.com:70000"):
            with self.subTest(url=url):
                with self.assertRaises(RegraDeDominioViolada):
                    validar_e_normalizar_url_link(url)

    def test_aceita_urls_legitimas(self) -> None:
        """Mantém válidas URLs comuns após o endurecimento da validação.

        O cenário cobre porta válida, subdomínio, espaço codificado, query e
        fragmento, host em maiúsculas, IPv4 e IPv6. Ele existe para que as novas
        regras não rejeitem links profissionais legítimos.
        """
        casos = {
            "https://exemplo.com:8443/x": "https://exemplo.com:8443/x",
            "https://pt.linkedin.com/in/usuario": "https://pt.linkedin.com/in/usuario",
            "https://exemplo.com/caminho%20codificado": "https://exemplo.com/caminho%20codificado",
            "https://exemplo.com/p?tab=readme#secao": "https://exemplo.com/p?tab=readme#secao",
            "HTTPS://Exemplo.COM/Perfil": "https://Exemplo.COM/Perfil",
            "http://192.168.0.1/portfolio": "http://192.168.0.1/portfolio",
            "http://[::1]:8080/": "http://[::1]:8080/",
            "https://meu-site.com.br": "https://meu-site.com.br",
        }
        for entrada, esperado in casos.items():
            with self.subTest(url=entrada):
                self.assertEqual(validar_e_normalizar_url_link(entrada), esperado)

    def test_aceita_url_no_limite_de_2048_caracteres(self) -> None:
        """Aceita URL com exatamente 2048 caracteres.

        O cenário monta uma URL no tamanho máximo permitido. Ele existe para
        cobrir a fronteira do limite, já que só o excesso era testado.
        """
        prefixo = "https://exemplo.com/"
        url = prefixo + "a" * (TAMANHO_MAXIMO_URL_LINK - len(prefixo))

        self.assertEqual(len(url), TAMANHO_MAXIMO_URL_LINK)
        self.assertEqual(validar_e_normalizar_url_link(url), url)


if __name__ == "__main__":
    unittest.main()
