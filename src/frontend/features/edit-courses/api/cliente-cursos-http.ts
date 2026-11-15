import type { Curso } from "../model/cursos";

export type CodigoFalhaCurso = "indisponivel" | "rede" | "resposta-invalida";

export class FalhaCurso extends Error {
  constructor(public readonly codigo: CodigoFalhaCurso) {
    super(codigo);
    this.name = "FalhaCurso";
  }
}

export interface ClienteCursos {
  salvar(cursos: Curso[]): Promise<void>;
}

/**
 * Cria o cliente HTTP para persistência de cursos no backend.
 *
 * Envia cada curso preenchido para POST /cursos com credentials: "include".
 */
export function criarClienteCursosHttp(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteCursos {
  return {
    async salvar(cursos: Curso[]): Promise<void> {
      if (!urlDaApi || urlDaApi.trim() === "") {
        throw new FalhaCurso("indisponivel");
      }

      const baseUrl = urlDaApi.replace(/\/+$/, "");

      if (cursos.length === 0) {
        return;
      }

      for (const item of cursos) {
        if (!item.nome.trim() || !item.instituicao.trim()) continue;

        const carga = Number(item.cargaHoraria);
        const payload = {
          nome: item.nome.trim(),
          instituicao: item.instituicao.trim(),
          carga_horaria:
            !Number.isNaN(carga) && carga > 0 ? Math.round(carga) : null,
        };

        try {
          const resposta = await fetch(`${baseUrl}/cursos`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(payload),
          });

          if (resposta.status === 201 || resposta.ok) {
            continue;
          }

          if (resposta.status >= 500) {
            throw new FalhaCurso("indisponivel");
          }

          throw new FalhaCurso("resposta-invalida");
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
