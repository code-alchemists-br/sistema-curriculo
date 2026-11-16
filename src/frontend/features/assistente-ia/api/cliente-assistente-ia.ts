import type {
  CampoRevisavel,
  InformacaoPerfil,
  RecomendacaoModelo,
  RevisaoTexto,
} from "../model/tipos";

/** Falha do assistente de IA, com mensagem já legível para o estudante. */
export class FalhaAssistenteIa extends Error {
  constructor(mensagem: string) {
    super(mensagem);
    this.name = "FalhaAssistenteIa";
  }
}

/** Operações do assistente de IA, escondendo fetch e DTOs da interface. */
export interface ClienteAssistenteIa {
  revisar(entrada: {
    campo: CampoRevisavel;
    texto: string;
    pergunta?: string;
    contexto?: Record<string, string>;
  }): Promise<RevisaoTexto>;
  recomendarModelo(perfil: InformacaoPerfil[]): Promise<RecomendacaoModelo>;
}

/** Cria o cliente HTTP usando VITE_API_URL e o cookie de sessão do navegador. */
export function criarClienteAssistenteIa(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteAssistenteIa {
  const base = (urlDaApi ?? "").replace(/\/$/, "");

  /**
   * Envia um POST JSON ao assistente e devolve o corpo da resposta.
   *
   * Exige `VITE_API_URL`, inclui o cookie de sessão e traduz falha de rede,
   * sessão ausente (401) e erros da API em `FalhaAssistenteIa`. Existe para
   * que revisão e recomendação compartilhem o mesmo tratamento de erros.
   */
  async function postar(caminho: string, corpo: unknown): Promise<any> {
    if (!base)
      throw new FalhaAssistenteIa("Defina VITE_API_URL para usar a IA.");
    let resposta: Response;
    try {
      resposta = await fetch(`${base}${caminho}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(corpo),
        credentials: "include",
      });
    } catch {
      throw new FalhaAssistenteIa("Não foi possível falar com o servidor.");
    }
    if (resposta.status === 401)
      throw new FalhaAssistenteIa("Entre na sua conta para usar a IA.");
    let dados: any = null;
    try {
      dados = await resposta.json();
    } catch {
      // Sem corpo JSON: a mensagem abaixo usa só o status.
    }
    if (!resposta.ok) {
      throw new FalhaAssistenteIa(
        typeof dados?.detail === "string"
          ? dados.detail
          : `A IA respondeu com erro ${resposta.status}.`,
      );
    }
    return dados;
  }

  return {
    async revisar({ campo, texto, pergunta, contexto }) {
      const dados = await postar("/assistente/revisoes", {
        campo,
        texto,
        pergunta,
        contexto: contexto ?? {},
      });
      if (
        !Array.isArray(dados?.sugestoes) ||
        typeof dados?.situacao !== "string"
      ) {
        throw new FalhaAssistenteIa("A revisão voltou num formato inesperado.");
      }
      return {
        situacao: dados.situacao,
        motivo: String(dados.motivo ?? ""),
        sugestoes: dados.sugestoes.map(String).slice(0, 3),
        podeManterTexto: Boolean(dados.pode_manter_texto),
      };
    },

    async recomendarModelo(perfil) {
      const dados = await postar("/assistente/recomendacao-modelo", {
        extras: perfil.slice(0, 10),
      });
      if (typeof dados?.modelo !== "string") {
        throw new FalhaAssistenteIa(
          "A recomendação voltou num formato inesperado.",
        );
      }
      return {
        modelo: dados.modelo,
        motivo: String(dados.motivo ?? ""),
        alternativa:
          typeof dados.alternativa === "string" ? dados.alternativa : null,
      };
    },
  };
}
