import { z } from "zod";

/** Representa o estado de uma etapa obrigatória do Wizard. */
export const estadoSecaoObrigatoriaSchema = z.object({
  status: z.enum(["preenchida", "pulada"]),
  mensagemErro: z.string().trim().min(1).optional()
});

/** Representa os dados pessoais mínimos já definidos pelo formulário existente. */
const dadosPessoaisSchema = z.object({
  nomeCompleto: z.string().trim().min(1, "Informe o nome completo."),
  enderecoCompleto: z.string().trim().min(1, "Informe o endereço completo."),
  telefones: z.array(z.string().trim().min(1, "Informe um telefone.")).min(1, "Informe pelo menos um telefone."),
  email: z.string().trim().email("Informe um e-mail válido.")
});

/** Representa as competências mantidas pela feature de competências. */
const competenciasSchema = z
  .object({
    hardSkills: z.array(z.string().trim().min(1)).default([]),
    softSkills: z.array(z.string().trim().min(1)).default([])
  })
  .refine(
    ({ hardSkills, softSkills }) => hardSkills.length > 0 || softSkills.length > 0,
    { path: ["competencias"], message: "Informe pelo menos uma competência técnica ou comportamental." }
  );

/** Representa o mínimo do projeto acadêmico que a feature atual consegue validar. */
const projetoAcademicoSchema = z.object({
  titulo: z.string().trim().min(1, "Informe o título do projeto."),
  descricao: z.string().trim().min(1, "Informe a descrição do projeto."),
  tecnologias: z.string().trim()
});

/** Representa todo o estado necessário para a validação final do currículo. */
export const curriculoParaValidacaoSchema = z.object({
  dadosPessoais: dadosPessoaisSchema,
  formacaoAcademica: estadoSecaoObrigatoriaSchema,
  experienciasProfissionais: estadoSecaoObrigatoriaSchema,
  competencias: competenciasSchema,
  projetosAcademicos: z.array(projetoAcademicoSchema)
});

export interface EstadoSecaoObrigatoria {
  status: "preenchida" | "pulada";
  mensagemErro?: string;
}

export interface DadosPessoaisParaValidacao {
  nomeCompleto: string;
  enderecoCompleto: string;
  telefones: string[];
  email: string;
}

export interface CompetenciasParaValidacao {
  hardSkills: string[];
  softSkills: string[];
}

export interface ProjetoAcademicoParaValidacao {
  titulo: string;
  descricao: string;
  tecnologias: string;
}

export interface CurriculoParaValidacao {
  dadosPessoais: DadosPessoaisParaValidacao;
  formacaoAcademica: EstadoSecaoObrigatoria;
  experienciasProfissionais: EstadoSecaoObrigatoria;
  competencias: CompetenciasParaValidacao;
  projetosAcademicos: ProjetoAcademicoParaValidacao[];
}

/** Identifica as seções relevantes para liberar a prévia e a exportação. */
export type IdSecaoCurriculo =
  | "dados-pessoais"
  | "formacao-academica"
  | "experiencias-profissionais"
  | "competencias";

/** Classifica uma seção conforme o resultado da validação final. */
export type StatusValidacaoSecao = "valida" | "pendente" | "erro";

/** Expõe um resultado estável e apresentável da validação do currículo. */
export interface ResultadoValidacaoSecao {
  id: IdSecaoCurriculo;
  titulo: string;
  status: StatusValidacaoSecao;
  mensagens: string[];
}

/** Agrega o resultado final usado para bloquear ou liberar ações críticas. */
export interface ResultadoValidacaoCurriculo {
  valido: boolean;
  secoes: ResultadoValidacaoSecao[];
  podeVisualizarPreview: boolean;
  podeExportarPdf: boolean;
}

const METADADOS_SECOES: Array<Pick<ResultadoValidacaoSecao, "id" | "titulo">> = [
  { id: "dados-pessoais", titulo: "Dados pessoais" },
  { id: "formacao-academica", titulo: "Formação acadêmica" },
  { id: "experiencias-profissionais", titulo: "Experiências profissionais" },
  { id: "competencias", titulo: "Competências" }
];

/**
 * Valida o currículo inteiro e transforma falhas técnicas em pendências por seção.
 * Usa Zod para validar os dados e interpreta etapas explicitamente puladas como
 * pendências, bloqueando prévia e PDF. Essa função existe para concentrar a regra
 * transversal do Wizard em um contrato único e reutilizável pela interface.
 */
export function validarCurriculo(valores: unknown): ResultadoValidacaoCurriculo {
  const resultado = curriculoParaValidacaoSchema.safeParse(valores);
  const secoes: ResultadoValidacaoSecao[] = METADADOS_SECOES.map(({ id, titulo }) => ({
    id,
    titulo,
    status: "valida",
    mensagens: []
  }));

  if (!resultado.success) {
    for (const issue of resultado.error.issues) {
      const id = idDaSecao(issue.path[0]);
      if (id === undefined) continue;

      const secao = secoes.find((item) => item.id === id);
      if (secao === undefined) continue;

      secao.status = issue.path[1] === "status" && issue.message === "Required"
        ? "pendente"
        : "erro";
      secao.mensagens.push(issue.message);
    }
  }

  if (resultado.success) {
    aplicarPendenciasDeEtapas(resultado.data, secoes);
  }

  const valido = secoes.every((secao) => secao.status === "valida");

  return {
    valido,
    secoes,
    podeVisualizarPreview: valido,
    podeExportarPdf: valido
  };
}

/** Converte o caminho produzido pelo Zod no identificador da seção da tela. */
function idDaSecao(caminho: PropertyKey | undefined): IdSecaoCurriculo | undefined {
  switch (caminho) {
    case "dadosPessoais":
      return "dados-pessoais";
    case "formacaoAcademica":
      return "formacao-academica";
    case "experienciasProfissionais":
      return "experiencias-profissionais";
    case "competencias":
      return "competencias";
    default:
      return undefined;
  }
}

/** Marca etapas puladas e mensagens explícitas como pendências do Wizard. */
function aplicarPendenciasDeEtapas(
  valores: CurriculoParaValidacao,
  secoes: ResultadoValidacaoSecao[]
): void {
  const etapas: Array<[IdSecaoCurriculo, EstadoSecaoObrigatoria]> = [
    ["formacao-academica", valores.formacaoAcademica],
    ["experiencias-profissionais", valores.experienciasProfissionais]
  ];

  for (const [id, etapa] of etapas) {
    const secao = secoes.find((item) => item.id === id);
    if (secao === undefined) continue;

    if (etapa.status === "pulada") {
      secao.status = "pendente";
      secao.mensagens.push(etapa.mensagemErro ?? "Etapa não concluída.");
      continue;
    }

    if (etapa.mensagemErro !== undefined) {
      secao.status = "erro";
      secao.mensagens.push(etapa.mensagemErro);
    }
  }
}
