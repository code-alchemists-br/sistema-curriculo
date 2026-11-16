import {
  idiomaEstaVazio,
  normalizarIdioma,
  validarIdioma,
  type Idioma,
} from "../model/idiomas";

export type CodigoFalhaIdioma = "indisponivel" | "rede" | "resposta-invalida";

/**
 * Encapsula um código estável em Error para classificar configuração, rede e
 * rejeição do lote sem expor detalhes internos do servidor à interface.
 */
export class FalhaIdioma extends Error {
  /** Registra o código e identifica a classe para permitir tratamento tipado da falha. */
  constructor(
    public readonly codigo: CodigoFalhaIdioma,
    public readonly statusHttp?: number,
  ) {
    super(codigo);
    this.name = "FalhaIdioma";
  }
}

/** Define a porta de persistência de listas para manter a UI independente de HTTP. */
export interface ClienteIdiomas {
  /** Persiste o lote por promessa para permitir avanço somente após confirmação. */
  salvar(idiomas: Idioma[], signal?: AbortSignal): Promise<void>;
}

/**
 * Cria o cliente HTTP para persistência de idiomas no backend.
 *
 * Valida todo o lote e envia os payloads normalizados por POST /idiomas com cookies.
 * Um Set por instância evita reenviar payloads confirmados ao retornar ou repetir
 * após sucesso parcial. O chamador deve manter uma instância por identidade;
 * não há sincronização remota nem atualização dos registros já cadastrados.
 */
export function criarClienteIdiomasHttp(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteIdiomas {
  const confirmados = new Set<string>();

  return {
    /**
     * Valida o lote inteiro antes de qualquer POST e registra somente confirmações.
     * Assim, rascunhos parciais não são perdidos e o retry preserva sucessos anteriores.
     */
    async salvar(idiomas: Idioma[], signal?: AbortSignal): Promise<void> {
      const preenchidos = idiomas.filter((item) => !idiomaEstaVazio(item));
      if (
        preenchidos.some((item) => Object.keys(validarIdioma(item)).length > 0)
      ) {
        throw new FalhaIdioma("resposta-invalida");
      }
      const normalizados = preenchidos.map(normalizarIdioma);
      if (normalizados.length === 0) return;

      if (!urlDaApi || urlDaApi.trim() === "") {
        throw new FalhaIdioma("indisponivel");
      }

      const baseUrl = urlDaApi.replace(/\/+$/, "");

      for (const item of normalizados) {
        signal?.throwIfAborted();
        const payload = {
          idioma: item.nome,
          nivel: item.nivel,
        };
        const body = JSON.stringify(payload);
        if (confirmados.has(body)) continue;

        try {
          const resposta = await fetch(`${baseUrl}/idiomas`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
            ...(signal ? { signal } : {}),
            body,
          });

          signal?.throwIfAborted();
          if (resposta.ok) {
            confirmados.add(body);
            continue;
          }

          if (resposta.status >= 500) {
            throw new FalhaIdioma("indisponivel");
          }

          throw new FalhaIdioma("resposta-invalida", resposta.status);
        } catch (erro: unknown) {
          if (erro instanceof FalhaIdioma) {
            throw erro;
          }
          throw new FalhaIdioma("rede");
        }
      }
    },
  };
}
