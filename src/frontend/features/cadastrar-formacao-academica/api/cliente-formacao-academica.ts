/** Representa os níveis acadêmicos aceitos no cadastro de formação. */
export type NivelFormacaoAcademica =
  | "ensino_fundamental"
  | "ensino_medio"
  | "tecnico"
  | "tecnologo"
  | "graduacao"
  | "especializacao"
  | "mestrado"
  | "doutorado";

/** Representa a situação atual ou final de uma formação acadêmica. */
export type StatusFormacaoAcademica =
  "em_andamento" | "concluido" | "interrompido";

/** Define os dados normalizados enviados pela tela para cadastrar uma formação. */
export interface CadastroFormacaoAcademicaEntrada {
  instituicao: string;
  curso: string;
  nivel: NivelFormacaoAcademica;
  dataInicio: string;
  dataFim?: string;
  status: StatusFormacaoAcademica;
}

/** Enumera as falhas que a interface consegue comunicar sem expor transporte. */
export type CodigoFalhaFormacaoAcademica =
  "indisponivel" | "rede" | "resposta-invalida";

/** Representa uma falha conhecida ao solicitar o cadastro de uma formação. */
export class FalhaFormacaoAcademica extends Error {
  constructor(public readonly codigo: CodigoFalhaFormacaoAcademica) {
    super(codigo);
    this.name = "FalhaFormacaoAcademica";
  }
}

/** Define a intenção de cadastro consumida pelo formulário, sem expor HTTP à UI. */
export interface ClienteFormacaoAcademica {
  cadastrar(entrada: CadastroFormacaoAcademicaEntrada): Promise<void>;
}

/**
 * Cria um cliente temporário que comunica a indisponibilidade da integração.
 *
 * A implementação rejeita toda solicitação com uma falha estável e não grava
 * dados localmente. Ela existe para permitir que a página seja composta antes
 * da definição da integração real, sem simular persistência em produção.
 */
export function criarClienteFormacaoAcademicaIndisponivel(): ClienteFormacaoAcademica {
  return {
    async cadastrar() {
      throw new FalhaFormacaoAcademica("indisponivel");
    },
  };
}
