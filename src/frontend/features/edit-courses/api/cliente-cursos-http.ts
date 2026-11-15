import {
  cursoEstaVazio,
  normalizarCurso,
  validarCurso,
  type Curso,
} from "../model/cursos";

export type CodigoFalhaCurso = "indisponivel" | "rede" | "resposta-invalida";

/**
 * Encapsula um código estável em Error para classificar configuração, rede e
 * rejeição do lote sem expor detalhes internos do servidor à interface.
 */
export class FalhaCurso extends Error {
  /** Registra o código e identifica a classe para permitir tratamento tipado da falha. */
  constructor(
    public readonly codigo: CodigoFalhaCurso,
    public readonly statusHttp?: number,
  ) {
    super(codigo);
    this.name = "FalhaCurso";
  }
}

/** Define a porta de persistência de listas para manter a UI independente de HTTP. */
export interface ClienteCursos {
  /** Persiste o lote por promessa para permitir avanço somente após confirmação. */
  salvar(cursos: Curso[], signal?: AbortSignal): Promise<void>;
}

/**
 * Cria o cliente HTTP para persistência de cursos no backend.
 *
 * Valida todo o lote e envia os payloads normalizados por POST /cursos com cookies.
 * Um Set por instância evita reenviar payloads confirmados ao retornar ou repetir
 * após sucesso parcial. O chamador deve manter uma instância por identidade;
 * não há sincronização remota nem atualização dos registros já cadastrados.
 */
export function criarClienteCursosHttp(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteCursos {
  const confirmados = new Set<string>();

  return {
    /**
     * Valida o lote inteiro antes de qualquer POST e registra somente confirmações.
     * Assim, rascunhos parciais não são perdidos e o retry preserva sucessos anteriores.
     */
    async salvar(cursos: Curso[], signal?: AbortSignal): Promise<void> {
      const preenchidos = cursos.filter((item) => !cursoEstaVazio(item));
      if (
        preenchidos.some((item) => Object.keys(validarCurso(item)).length > 0)
      ) {
        throw new FalhaCurso("resposta-invalida");
      }
      const normalizados = preenchidos.map(normalizarCurso);
      if (normalizados.length === 0) return;

      if (!urlDaApi || urlDaApi.trim() === "") {
        throw new FalhaCurso("indisponivel");
      }

      const baseUrl = urlDaApi.replace(/\/+$/, "");

      for (const item of normalizados) {
        signal?.throwIfAborted();
        const payload = {
          nome: item.nome,
          instituicao: item.instituicao,
          carga_horaria:
            item.cargaHoraria === "" ? null : Number(item.cargaHoraria),
        };
        const body = JSON.stringify(payload);
        if (confirmados.has(body)) continue;

        try {
          const resposta = await fetch(`${baseUrl}/cursos`, {
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
            throw new FalhaCurso("indisponivel");
          }

          throw new FalhaCurso("resposta-invalida", resposta.status);
        } catch (erro: unknown) {
          if (erro instanceof FalhaCurso) {
            throw erro;
          }
          throw new FalhaCurso("rede");
        }
      }
    },
  };
}
