import {
  FalhaFormacaoAcademica,
  type CadastroFormacaoAcademicaEntrada,
  type ClienteFormacaoAcademica,
} from "./cliente-formacao-academica";

/** Normaliza string de data para o formato YYYY-MM-DD esperado pelo backend. */
function normalizarDataParaBackend(data: string | undefined): string | null {
  if (!data || !data.trim()) return null;
  const limpo = data.trim();
  if (/^\d{4}-\d{2}$/.test(limpo)) {
    return `${limpo}-01`;
  }
  return limpo;
}

/**
 * Cria o cliente HTTP para persistência de formação acadêmica no backend.
 *
 * Envia as informações para POST /formacoes-academicas com credentials: "include",
 * traduzindo os campos para snake_case e tratando falhas de rede e indisponibilidade.
 */
export function criarClienteFormacaoAcademicaHttp(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteFormacaoAcademica {
  return {
    async cadastrar(entrada: CadastroFormacaoAcademicaEntrada): Promise<void> {
      if (!urlDaApi || urlDaApi.trim() === "") {
        throw new FalhaFormacaoAcademica("indisponivel");
      }

      const payload = {
        instituicao: entrada.instituicao.trim(),
        curso: entrada.curso.trim(),
        nivel: entrada.nivel,
        data_inicio: normalizarDataParaBackend(entrada.dataInicio),
        data_fim: normalizarDataParaBackend(entrada.dataFim),
        status: entrada.status,
      };

      const baseUrl = urlDaApi.replace(/\/+$/, "");

      try {
        const resposta = await fetch(`${baseUrl}/formacoes-academicas`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify(payload),
        });

        if (resposta.status === 201 || resposta.ok) {
          return;
        }

        if (resposta.status >= 500) {
          throw new FalhaFormacaoAcademica("indisponivel");
        }

        throw new FalhaFormacaoAcademica("resposta-invalida");
      } catch (erro: unknown) {
        if (erro instanceof FalhaFormacaoAcademica) {
          throw erro;
        }
        throw new FalhaFormacaoAcademica("rede");
      }
    },
  };
}
