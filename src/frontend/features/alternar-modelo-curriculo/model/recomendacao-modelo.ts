/** Representa uma categoria usada somente para orientar a escolha do modelo. */
export type ObjetivoCurriculo =
  | "primeiro-emprego"
  | "tecnologia"
  | "administrativo-corporativo"
  | "criativo-design"
  | "academico-pesquisador"
  | "outro";

/** Define uma opção exibida no campo Objetivo do currículo. */
export interface OpcaoObjetivoCurriculo {
  valor: ObjetivoCurriculo;
  rotulo: string;
}

/** Opções iniciais previstas para orientar a escolha de modelo. */
export const OPCOES_OBJETIVO_CURRICULO: ReadonlyArray<OpcaoObjetivoCurriculo> =
  [
    { valor: "primeiro-emprego", rotulo: "Primeiro emprego / estágio" },
    { valor: "tecnologia", rotulo: "Tecnologia" },
    {
      valor: "administrativo-corporativo",
      rotulo: "Administrativo / corporativo",
    },
    { valor: "criativo-design", rotulo: "Criativo / design" },
    { valor: "academico-pesquisador", rotulo: "Acadêmico / pesquisador" },
    { valor: "outro", rotulo: "Outro" },
  ];

/**
 * Produz uma recomendação textual sem alterar a escolha feita pelo estudante.
 *
 * - O que faz: Relaciona a categoria informada a um modelo oficial do catálogo.
 * - Como faz: Usa uma decisão local, determinística e apenas informativa.
 * - Qual finalidade atende: Orienta iniciantes sem restringir a autonomia na seleção de layout.
 */
export function obterRecomendacaoModelo(objetivo: ObjetivoCurriculo): string {
  switch (objetivo) {
    case "primeiro-emprego":
      return "Recomendamos o modelo Primeiro emprego para valorizar formação, projetos e competências.";
    case "tecnologia":
    case "outro":
      return "Recomendamos o modelo Moderno por equilibrar competências, projetos e experiência.";
    case "administrativo-corporativo":
      return "Recomendamos o modelo Profissional clássico por sua hierarquia visual sóbria.";
    case "criativo-design":
      return "Recomendamos o modelo Criativo para dar maior destaque à identidade e aos projetos.";
    case "academico-pesquisador":
      return "Recomendamos o modelo Acadêmico para priorizar formação e projetos acadêmicos.";
  }
}
