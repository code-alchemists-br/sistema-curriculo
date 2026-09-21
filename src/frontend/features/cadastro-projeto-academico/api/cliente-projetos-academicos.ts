// Proveniência: decision-analysis prompts/frontend/20260921-120136-tela-cadastro-projetos-academicos-v001.md#v001

/** Representa os dados de projeto aceitos pela fronteira futura do cliente. */
export interface ProjetoAcademicoEntrada {
  titulo: string;
  descricao: string;
  tecnologias: string;
}

/** Enumera falhas que a interface pode comunicar sem expor detalhes técnicos. */
export type CodigoFalhaCadastroProjeto = "indisponivel" | "resposta-invalida";

/**
 * Representa uma falha conhecida durante o cadastro de projeto acadêmico.
 *
 * A classe carrega apenas um código estável de interface, separado de HTTP ou
 * persistência. Ela existe para manter o formulário testável enquanto o
 * backend ainda não fornece o contrato que realizará o cadastro.
 */
export class FalhaCadastroProjeto extends Error {
  constructor(public readonly codigo: CodigoFalhaCadastroProjeto) {
    super(codigo);
    this.name = "FalhaCadastroProjeto";
  }
}

/**
 * Define a intenção de cadastrar projeto consumida pela interface.
 *
 * O contrato recebe um DTO explícito e omite identidade, transporte e banco.
 * Ele existe para que UI e testes dependam da mesma fronteira, substituível por
 * uma implementação HTTP depois que o backend definir o contrato real.
 */
export interface ClienteProjetosAcademicos {
  cadastrar(entrada: ProjetoAcademicoEntrada): Promise<void>;
}

/**
 * Cria o cliente provisório que revela a indisponibilidade do backend atual.
 *
 * A implementação rejeita toda solicitação com uma falha controlada e não
 * armazena dados localmente. Ela existe para impedir que a tela prometa
 * persistência antes de caso de uso, identidade e API serem disponibilizados.
 */
export function criarClienteProjetosAcademicosIndisponivel(): ClienteProjetosAcademicos {
  return {
    async cadastrar() {
      throw new FalhaCadastroProjeto("indisponivel");
    }
  };
}
