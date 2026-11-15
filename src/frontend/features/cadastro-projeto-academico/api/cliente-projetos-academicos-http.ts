import {
  FalhaCadastroProjeto,
  type ClienteProjetosAcademicos,
  type ProjetoAcademicoEntrada,
} from "./cliente-projetos-academicos";

/**
 * Cria o cliente HTTP para persistência de projetos acadêmicos no backend.
 *
 * Envia as informações para POST /projetos-academicos com credentials: "include",
 * tratando respostas de sucesso e falhas de rede de forma segura.
 */
export function criarClienteProjetosAcademicosHttp(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteProjetosAcademicos {
  return {
    async cadastrar(entrada: ProjetoAcademicoEntrada): Promise<void> {
      if (!urlDaApi || urlDaApi.trim() === "") {
        throw new FalhaCadastroProjeto("indisponivel");
      }

      const payload = {
        titulo: entrada.titulo.trim(),
        descricao: entrada.descricao.trim(),
        tecnologias: entrada.tecnologias.trim(),
      };

      const baseUrl = urlDaApi.replace(/\/+$/, "");

      try {
        const resposta = await fetch(`${baseUrl}/projetos-academicos`, {
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
          throw new FalhaCadastroProjeto("indisponivel");
        }

        throw new FalhaCadastroProjeto("resposta-invalida");
      } catch (erro: unknown) {
        if (erro instanceof FalhaCadastroProjeto) {
          throw erro;
        }
        throw new FalhaCadastroProjeto("indisponivel");
      }
    },
  };
}
