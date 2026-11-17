import {
  FalhaRecuperacaoSenha,
  type ClienteRecuperacaoSenha,
  type SolicitarRecuperacaoSenhaEntrada,
} from "./cliente-recuperacao-senha";

/**
 * Cria o cliente HTTP para a rota POST /recuperacoes-senha do backend.
 *
 * Utiliza fetch com credentials: "include" e Content-Type: application/json.
 * Interpreta status 202 (e 200) como sucesso da solicitação.
 * Converte erros de conexão física em falha de "rede" e HTTP 5xx em "indisponivel".
 */
export function criarClienteRecuperacaoSenhaHttp(
  urlDaApi = import.meta.env.VITE_API_URL,
): ClienteRecuperacaoSenha {
  return {
    async solicitar(entrada: SolicitarRecuperacaoSenhaEntrada): Promise<void> {
      const base = (urlDaApi ?? "").replace(/\/$/, "");
      if (!base) {
        throw new FalhaRecuperacaoSenha("indisponivel");
      }

      let resposta: Response;
      try {
        resposta = await fetch(`${base}/recuperacoes-senha`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: entrada.email }),
          credentials: "include",
        });
      } catch {
        throw new FalhaRecuperacaoSenha("rede");
      }

      if (resposta.status === 202 || resposta.status === 200) {
        return;
      }

      if (resposta.status === 422) {
        throw new FalhaRecuperacaoSenha("resposta-invalida");
      }

      if (resposta.status >= 500) {
        throw new FalhaRecuperacaoSenha("indisponivel");
      }

      throw new FalhaRecuperacaoSenha("resposta-invalida");
    },
  };
}

/**
 * Cria o cliente de demonstração para recuperação de senha quando o backend não está configurado.
 *
 * Simula um envio seguro com sucesso imediato sem expor erros ao usuário final.
 */
export function criarClienteRecuperacaoSenhaDemonstracao(): ClienteRecuperacaoSenha {
  return {
    async solicitar(_entrada: SolicitarRecuperacaoSenhaEntrada): Promise<void> {
      // Pequena latência simulada para feedback de carregamento perceptível
      await new Promise((resolve) => setTimeout(resolve, 300));
    },
  };
}
