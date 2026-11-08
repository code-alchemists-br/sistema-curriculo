import type { Experiencia } from "../model/experiencias";

export type CodigoFalhaExperiencia =
  "indisponivel" | "rede" | "resposta-invalida";

export class FalhaExperiencia extends Error {
  constructor(public readonly codigo: CodigoFalhaExperiencia) {
    super(codigo);
    this.name = "FalhaExperiencia";
  }
}

/** Normaliza string de data (ex: YYYY-MM ou YYYY-MM-DD) para YYYY-MM-DD. */
function normalizarDataParaBackend(data: string | undefined): string | null {
  if (!data || !data.trim()) return null;
  const limpo = data.trim();
  if (/^\d{4}-\d{2}$/.test(limpo)) {
    return `${limpo}-01`;
  }
  return limpo;
}

export interface ClienteExperienciaProfissional {
  salvar(experiencias: Experiencia[]): Promise<void>;
}

/**
 * Cria o cliente HTTP para persistência de experiências profissionais no backend.
 *
 * Envia cada experiência preenchida para POST /experiencias-profissionais com
 * credentials: "include", normalizando datas e tratando flags de emprego atual.
 */
export function criarClienteExperienciasHttp(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteExperienciaProfissional {
  return {
    async salvar(experiencias: Experiencia[]): Promise<void> {
      if (!urlDaApi || urlDaApi.trim() === "") {
        throw new FalhaExperiencia("indisponivel");
      }

      const baseUrl = urlDaApi.replace(/\/+$/, "");

      if (experiencias.length === 0) {
        return;
      }

      for (const exp of experiencias) {
        if (!exp.empresa.trim() && !exp.cargo.trim()) continue;

        const payload = {
          empresa: exp.empresa.trim(),
          cargo: exp.cargo.trim(),
          descricao: exp.descricao.trim(),
          data_inicio: normalizarDataParaBackend(exp.inicio),
          data_fim: exp.empregoAtual
            ? null
            : normalizarDataParaBackend(exp.fim),
        };

        try {
          const resposta = await fetch(
            `${baseUrl}/experiencias-profissionais`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              credentials: "include",
              body: JSON.stringify(payload),
            },
          );

          if (resposta.status === 201 || resposta.ok) {
            continue;
          }

          if (resposta.status >= 500) {
            throw new FalhaExperiencia("indisponivel");
          }

          throw new FalhaExperiencia("resposta-invalida");
        } catch (erro: unknown) {
          if (erro instanceof FalhaExperiencia) {
            throw erro;
          }
          throw new FalhaExperiencia("rede");
        }
      }
    },
  };
}
