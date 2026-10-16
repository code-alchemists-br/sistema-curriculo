import { FalhaVagasGrupo2 } from "../api/cliente-vagas-grupo2";

/**
 * Converte uma falha de integração em uma mensagem compreensível e segura ao estudante.
 *
 * **O que faz:** Mapeia exceções técnicas para mensagens orientativas em português.
 * **Como faz:** Avalia a tipagem do erro (ex.: `FalhaVagasGrupo2`) e retorna textos amigáveis sem expor URLs, status HTTP, termos de integração ou stack traces.
 * **Qual finalidade atende:** Cumpre os requisitos de usabilidade e segurança da informação ao omitir detalhes técnicos da integração.
 */
export function obterMensagemErroVagas(erro: unknown): string {
  if (erro instanceof FalhaVagasGrupo2) {
    if (erro.codigo === "resposta-invalida") {
      return "Recebemos uma resposta inesperada ao consultar as vagas. Tente novamente mais tarde.";
    }

    if (erro.codigo === "tempo-limite") {
      return "O serviço de vagas demorou para responder. Verifique sua conexão e tente novamente.";
    }

    return "O serviço de vagas está temporariamente indisponível. Tente novamente mais tarde.";
  }

  return "Não foi possível carregar as vagas no momento. Tente novamente mais tarde.";
}
