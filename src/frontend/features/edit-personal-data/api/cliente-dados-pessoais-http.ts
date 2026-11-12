import type { Student } from "../../../entities/student";
import {
  FalhaDadosPessoais,
  type ClienteDadosPessoais,
} from "./cliente-dados-pessoais";

/**
 * Cria o cliente HTTP para persistência dos dados pessoais no backend.
 *
 * Utiliza fetch com credentials: "include" para enviar cookies de sessão,
 * monta o payload esperado pela rota PUT /estudantes/me/perfil e traduz
 * eventuais erros em FalhaDadosPessoais sem expor detalhes de transporte à UI.
 */
export function criarClienteDadosPessoaisHttp(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteDadosPessoais {
  return {
    async salvar(dados: Student): Promise<void> {
      if (!urlDaApi || urlDaApi.trim() === "") {
        throw new FalhaDadosPessoais("indisponivel");
      }

      const telefonesLimpos = dados.telefones
        .map((t) => t.trim())
        .filter((t) => t.length > 0);

      const payload = {
        nome: dados.nomeCompleto.trim(),
        email: dados.email.trim(),
        endereco: dados.enderecoCompleto.trim(),
        cidade: dados.cidade.trim(),
        telefones:
          telefonesLimpos.length > 0 ? telefonesLimpos : ["Não informado"],
        linkedin: dados.linkedIn?.trim() || null,
        curriculo_lattes: dados.curriculoLattes?.trim() || null,
      };

      const baseUrl = urlDaApi.replace(/\/+$/, "");

      try {
        const resposta = await fetch(`${baseUrl}/estudantes/me/perfil`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify(payload),
        });

        if (resposta.ok) {
          return;
        }

        if (resposta.status >= 500) {
          throw new FalhaDadosPessoais("indisponivel");
        }

        throw new FalhaDadosPessoais("resposta-invalida");
      } catch (erro: unknown) {
        if (erro instanceof FalhaDadosPessoais) {
          throw erro;
        }
        throw new FalhaDadosPessoais("indisponivel");
      }
    },
  };
}
