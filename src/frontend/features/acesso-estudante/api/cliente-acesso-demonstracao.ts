import {
  type AcessoEstudanteEntrada,
  type CadastroEstudanteEntrada,
  type ClienteAcessoEstudante,
  type EstudanteCadastrado,
  FalhaAcessoEstudante,
} from "./cliente-acesso-estudante";

export interface UsuarioDemonstracao {
  id: string;
  nome: string;
  email: string;
  senha: string;
}

const USUARIOS_DEMONSTRACAO_PADRAO: UsuarioDemonstracao[] = [
  {
    id: "00000000-0000-4000-8000-000000000001",
    nome: "Estudante Exemplo",
    email: "estudante@exemplo.com",
    senha: "SenhaValida123!",
  },
];

/**
 * Cria um cliente em memória que reproduz as regras de negócio de cadastro e login.
 *
 * Permite testar a experiência de ponta a ponta na interface visual sem
 * exigir PostgreSQL ou backend rodando na máquina local.
 */
export function criarClienteAcessoDemonstracao(
  usuariosIniciais: UsuarioDemonstracao[] = USUARIOS_DEMONSTRACAO_PADRAO,
): ClienteAcessoEstudante {
  const usuarios = [...usuariosIniciais];

  return {
    async cadastrar(
      entrada: CadastroEstudanteEntrada,
    ): Promise<EstudanteCadastrado> {
      await new Promise((resolver) => setTimeout(resolver, 300));
      const emailNormalizado = entrada.email.trim().toLowerCase();

      if (usuarios.some((u) => u.email.toLowerCase() === emailNormalizado)) {
        throw new FalhaAcessoEstudante("email-ja-cadastrado");
      }

      const novoUsuario: UsuarioDemonstracao = {
        id:
          typeof crypto !== "undefined" && crypto.randomUUID
            ? crypto.randomUUID()
            : `usr-${Date.now()}`,
        nome: entrada.nome.trim(),
        email: entrada.email.trim(),
        senha: entrada.senha,
      };

      usuarios.push(novoUsuario);

      return {
        id: novoUsuario.id,
        nome: novoUsuario.nome,
        email: novoUsuario.email,
      };
    },

    async acessar(entrada: AcessoEstudanteEntrada): Promise<void> {
      await new Promise((resolver) => setTimeout(resolver, 250));
      const emailNormalizado = entrada.email.trim().toLowerCase();

      const usuario = usuarios.find(
        (u) =>
          u.email.toLowerCase() === emailNormalizado &&
          u.senha === entrada.senha,
      );

      if (!usuario) {
        throw new FalhaAcessoEstudante("credenciais-invalidas");
      }
    },
  };
}
