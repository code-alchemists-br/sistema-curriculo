/** Define o dado mínimo necessário para solicitar a recuperação de senha. */
export interface SolicitarRecuperacaoSenhaEntrada {
  email: string;
}

/**
 * Representa os dados temporários aceitos pelo endpoint de confirmação.
 *
 * O cliente serializa os dois campos em JSON e o backend valida o token e
 * deriva a senha antes de persistir. O contrato existe para concluir a troca
 * sem expor detalhes HTTP aos componentes.
 */
export interface RedefinirSenhaEntrada {
  token: string;
  senha: string;
}

/** Enumera falhas que podem ser apresentadas sem expor detalhes internos. */
export type CodigoFalhaRecuperacaoSenha =
  | "indisponivel"
  | "rede"
  | "resposta-invalida"
  | "dados-invalidos"
  | "token-invalido";

/** Representa uma falha conhecida no pedido de recuperação de senha. */
export class FalhaRecuperacaoSenha extends Error {
  constructor(public readonly codigo: CodigoFalhaRecuperacaoSenha) {
    super(codigo);
    this.name = "FalhaRecuperacaoSenha";
  }
}

/** Define a operação remota usada pela tela sem acoplar a UI a HTTP. */
export interface ClienteRecuperacaoSenha {
  solicitar(entrada: SolicitarRecuperacaoSenhaEntrada): Promise<void>;
  redefinir(entrada: RedefinirSenhaEntrada): Promise<void>;
}

/**
 * Cria o cliente HTTP dos endpoints públicos de recuperação de senha.
 *
 * Envia os DTOs esperados e valida os status 202/204, traduzindo erros de rede,
 * validação e token expirado para códigos estáveis. Existe para ligar a feature
 * ao backend sem expor detalhes HTTP aos componentes.
 */
export function criarClienteRecuperacaoSenha(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteRecuperacaoSenha {
  return {
    async solicitar(entrada) {
      const resposta = await enviar(urlDaApi, "/recuperacoes-senha", entrada);
      if (resposta.status !== 202) {
        throw new FalhaRecuperacaoSenha(classificarFalha(resposta.status));
      }
      try {
        const corpo: unknown = await resposta.json();
        if (
          typeof corpo === "object" &&
          corpo !== null &&
          "mensagem" in corpo &&
          typeof corpo.mensagem === "string"
        )
          return;
      } catch {
        // A resposta inválida é traduzida pelo erro estável abaixo.
      }
      throw new FalhaRecuperacaoSenha("resposta-invalida");
    },
    async redefinir(entrada) {
      const resposta = await enviar(
        urlDaApi,
        "/recuperacoes-senha/confirmacao",
        entrada,
      );
      if (resposta.status === 204) return;
      throw new FalhaRecuperacaoSenha(classificarFalha(resposta.status));
    },
  };
}

/**
 * Envia JSON ao endpoint configurado e converte falhas de transporte.
 *
 * A função normaliza a barra final da URL e captura rejeições do fetch. Ela
 * existe para que ambas as operações compartilhem o mesmo transporte seguro.
 */
async function enviar(
  urlDaApi: string | undefined,
  caminho: string,
  entrada: SolicitarRecuperacaoSenhaEntrada | RedefinirSenhaEntrada,
): Promise<Response> {
  if (urlDaApi === undefined || urlDaApi.trim() === "") {
    throw new FalhaRecuperacaoSenha("indisponivel");
  }
  try {
    return await fetch(`${urlDaApi.replace(/\/+$/, "")}${caminho}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(entrada),
    });
  } catch {
    throw new FalhaRecuperacaoSenha("rede");
  }
}

/**
 * Converte status HTTP em códigos estáveis da feature.
 *
 * A função reconhece validação, indisponibilidade e token expirado; status
 * desconhecidos viram resposta inválida para evitar dependência da UI em HTTP.
 */
function classificarFalha(status: number): CodigoFalhaRecuperacaoSenha {
  if (status === 400) return "token-invalido";
  if (status === 422) return "dados-invalidos";
  if (status === 503) return "indisponivel";
  return "resposta-invalida";
}

/**
 * Cria um cliente provisório que declara a integração como indisponível.
 *
 * A implementação nunca armazena e-mails nem simula envio de mensagem. Ela
 * existe para compor a tela sem declarar um backend inexistente como pronto.
 */
export function criarClienteRecuperacaoSenhaIndisponivel(): ClienteRecuperacaoSenha {
  return {
    async solicitar() {
      throw new FalhaRecuperacaoSenha("indisponivel");
    },
    async redefinir() {
      throw new FalhaRecuperacaoSenha("indisponivel");
    },
  };
}
