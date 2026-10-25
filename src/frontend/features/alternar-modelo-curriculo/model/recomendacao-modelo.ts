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
 * O que faz: Relaciona a categoria selecionada a um layout já suportado pelo
 * front-end e pelo backend.
 * Como faz: Usa uma decisão local, determinística e apenas informativa.
 * Por que existe: Orienta iniciantes sem restringir sua autonomia na seleção.
 */
export function obterRecomendacaoModelo(objetivo: ObjetivoCurriculo): string {
  switch (objetivo) {
    case "primeiro-emprego":
    case "tecnologia":
    case "criativo-design":
      return "Recomendamos o modelo Compacto por oferecer uma leitura direta das informações.";
    case "administrativo-corporativo":
    case "academico-pesquisador":
      return "Recomendamos o modelo Clássico por sua hierarquia visual sóbria.";
    case "outro":
      return "Você pode escolher o modelo que melhor representa seu objetivo.";
  }
}
