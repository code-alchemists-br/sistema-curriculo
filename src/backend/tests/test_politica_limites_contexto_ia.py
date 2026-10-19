"""Verifica a política de limites de contexto de inteligência artificial."""

import json
import tempfile
import unittest
from pathlib import Path

from backend.infrastructure.configuracao.politica_limites_contexto_ia import (
    FonteArquivoPoliticaLimitesContextoIa,
    PoliticaLimitesContextoIaInvalida,
    caminho_politica_limites_contexto_ia_padrao,
)


def _politica_base() -> dict[str, object]:
    """Cria um documento de política válido e pequeno para cada cenário.

    A função retorna uma nova árvore para que cada teste possa alterá-la sem
    contaminar os demais. Ela existe para tornar explícitos os limites que o
    adapter precisa validar ao carregar um arquivo.
    """
    return {
        "versao": "1",
        "padrao": {
            "limites_campos": {"empresa": 120, "descricao_vaga": 6000},
            "orcamento_total_caracteres": 10000,
        },
        "teto_seguranca": {
            "limites_campos": {"empresa": 120, "descricao_vaga": 6000},
            "orcamento_total_caracteres": 10000,
        },
        "substituicoes": {
            "por_acao": {},
            "por_modelo": {},
            "por_acao_modelo": {},
        },
    }


class FonteArquivoPoliticaLimitesContextoIaTestCase(unittest.TestCase):
    """Exercita leitura, precedência e recarga segura do adapter de arquivo."""

    def setUp(self) -> None:
        """Cria um arquivo de configuração isolado e uma fonte para o cenário.

        O método usa diretório temporário para que mudanças de arquivo sejam
        reais, sem modificar a política mantida no repositório. Ele existe para
        verificar a recarga sem efeitos sobre a execução local do backend.
        """
        self.diretorio = tempfile.TemporaryDirectory()
        self.caminho = Path(self.diretorio.name) / "limites_contexto_ia.json"
        self.fonte = FonteArquivoPoliticaLimitesContextoIa(self.caminho)

    def tearDown(self) -> None:
        """Remove os arquivos temporários criados para o cenário de teste.

        O método encerra o diretório temporário depois de cada execução. Ele
        existe para manter os testes independentes e não deixar configuração de
        exemplo no sistema de arquivos do desenvolvedor.
        """
        self.diretorio.cleanup()

    def _escrever(self, politica: object) -> None:
        """Grava uma versão JSON da política no caminho observado pela fonte.

        O método serializa todo o documento de uma vez e acrescenta quebra de
        linha. Ele existe para simular a publicação de uma nova configuração
        pelo responsável técnico, fora de qualquer endpoint HTTP.
        """
        self.caminho.write_text(
            json.dumps(politica, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def test_carrega_limites_padrao_do_arquivo(self) -> None:
        """Carrega a primeira versão válida como política efetiva do servidor.

        O cenário grava o documento mínimo e consulta a fonte. Ele existe para
        garantir que os valores armazenados no arquivo, e não constantes do
        código, definam o contexto inicial.
        """
        self._escrever(_politica_base())

        politica = self.fonte.obter()

        limites = politica.resolver(None, None)
        self.assertEqual(politica.versao, "1")
        self.assertEqual(limites.limites_campos["empresa"], 120)
        self.assertEqual(limites.orcamento_total_caracteres, 10000)

    def test_arquivo_padrao_distribuido_no_backend_e_valido(self) -> None:
        """Carrega o arquivo de política entregue com o código do servidor.

        O cenário resolve o caminho padrão e o submete ao mesmo adapter usado
        em produção. Ele existe para impedir que uma edição do arquivo interno
        invalide a configuração que futuros casos de uso deverão receber.
        """
        politica = FonteArquivoPoliticaLimitesContextoIa(
            caminho_politica_limites_contexto_ia_padrao()
        ).obter()

        self.assertEqual(politica.versao, "1")
        self.assertEqual(
            politica.resolver(None, None).orcamento_total_caracteres,
            10000,
        )

    def test_recarrega_arquivo_e_aplica_precedencia_por_acao_e_modelo(self) -> None:
        """Atualiza o cache quando o arquivo muda e respeita a precedência definida.

        O cenário publica substituições por modelo, ação e combinação depois da
        primeira leitura. Ele existe para comprovar que o processo adota a nova
        política sem reinicialização e resolve o limite mais específico.
        """
        self._escrever(_politica_base())
        politica_inicial = self.fonte.obter()

        politica_atualizada = _politica_base()
        politica_atualizada["versao"] = "2"
        substituicoes = politica_atualizada["substituicoes"]
        assert isinstance(substituicoes, dict)
        substituicoes["por_modelo"] = {
            "gpt-5.6-luna": {"orcamento_total_caracteres": 8000}
        }
        substituicoes["por_acao"] = {
            "adequar_curriculo_vaga": {"orcamento_total_caracteres": 7000}
        }
        substituicoes["por_acao_modelo"] = {
            "adequar_curriculo_vaga": {
                "gpt-5.6-luna": {"orcamento_total_caracteres": 6000}
            }
        }
        self._escrever(politica_atualizada)

        politica_recarregada = self.fonte.obter()

        self.assertIsNot(politica_recarregada, politica_inicial)
        self.assertEqual(politica_recarregada.versao, "2")
        self.assertEqual(
            politica_recarregada.resolver(
                "adequar_curriculo_vaga", "gpt-5.6-luna"
            ).orcamento_total_caracteres,
            6000,
        )

    def test_mantem_ultima_politica_valida_quando_atualizacao_e_invalida(self) -> None:
        """Conserva o cache válido se o arquivo for publicado de forma incompleta.

        O cenário carrega uma política, substitui o arquivo por JSON inválido e
        consulta novamente a fonte. Ele existe para evitar interrupção de
        requisições em uma edição manual ainda não concluída.
        """
        self._escrever(_politica_base())
        politica_valida = self.fonte.obter()
        self.caminho.write_text("{", encoding="utf-8")

        politica_depois_da_falha = self.fonte.obter()

        self.assertIs(politica_depois_da_falha, politica_valida)

    def test_recusa_primeira_carga_invalida(self) -> None:
        """Sinaliza erro explícito quando não existe política válida para preservar.

        O cenário deixa o primeiro documento incompleto e tenta carregá-lo. Ele
        existe para impedir que o backend opere com limites não validados após
        uma instalação ou publicação incorreta.
        """
        self.caminho.write_text("{}", encoding="utf-8")

        with self.assertRaises(PoliticaLimitesContextoIaInvalida):
            self.fonte.obter()

    def test_recusa_sobrescrita_que_ultrapassa_teto_de_seguranca(self) -> None:
        """Recusa arquivo cuja substituição amplia o orçamento além do teto aprovado.

        O cenário declara uma ação com orçamento maior que o teto configurado.
        Ele existe para assegurar que ajustes operacionais não ampliem a
        exposição de dados por engano.
        """
        politica = _politica_base()
        substituicoes = politica["substituicoes"]
        assert isinstance(substituicoes, dict)
        substituicoes["por_acao"] = {
            "adequar_curriculo_vaga": {"orcamento_total_caracteres": 10001}
        }
        self._escrever(politica)

        with self.assertRaises(PoliticaLimitesContextoIaInvalida):
            self.fonte.obter()
