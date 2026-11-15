import type { ModeloApresentacaoCurriculo } from "../ui/AlternadorModeloCurriculo";

/** Representa uma categoria usada somente para orientar a escolha do modelo. */
export type ObjetivoCurriculo =
  | "ats-simples"
  | "administrativo-corporativo"
  | "compacto"
  | "tecnologia"
  | "criativo-design"
  | "academico-pesquisador"
  | "primeiro-emprego"
  | "outro";

/** Define uma opção exibida no campo Objetivo do currículo. */
export interface OpcaoObjetivoCurriculo {
  valor: ObjetivoCurriculo;
  rotulo: string;
}

/** Opções alinhadas diretamente aos modelos disponíveis no catálogo. */
export const OPCOES_OBJETIVO_CURRICULO: ReadonlyArray<OpcaoObjetivoCurriculo> =
  [
    {
      valor: "ats-simples",
      rotulo: "Triagem automatizada / ATS (Sistemas de vagas)",
    },
    {
      valor: "administrativo-corporativo",
      rotulo:
        "Administrativo / Corporativo tradicional (Profissional clássico)",
    },
    {
      valor: "compacto",
      rotulo: "Currículo condensado / Uma página (Compacto)",
    },
    {
      valor: "tecnologia",
      rotulo: "Tecnologia / Startups / Inovação (Moderno)",
    },
    {
      valor: "criativo-design",
      rotulo: "Criativo / Design / Portfólio (Criativo)",
    },
    {
      valor: "academico-pesquisador",
      rotulo: "Acadêmico / Científico / Pesquisa (Acadêmico)",
    },
    {
      valor: "primeiro-emprego",
      rotulo: "Primeiro emprego / Estágio (Primeiro emprego)",
    },
    {
      valor: "outro",
      rotulo: "Outro objetivo (Recomendação geral)",
    },
  ];

/**
 * Retorna o modelo correspondente ao objetivo selecionado no filtro.
 */
export function obterModeloRecomendadoPorObjetivo(
  objetivo: ObjetivoCurriculo,
): ModeloApresentacaoCurriculo {
  switch (objetivo) {
    case "ats-simples":
      return "ats-simples";
    case "administrativo-corporativo":
      return "classico";
    case "compacto":
      return "compacto";
    case "tecnologia":
      return "moderno";
    case "criativo-design":
      return "criativo";
    case "academico-pesquisador":
      return "academico";
    case "primeiro-emprego":
      return "primeiro-emprego";
    case "outro":
      return "moderno";
  }
}

/**
 * Produz uma recomendação textual alinhada ao objetivo e modelo escolhidos.
 *
 * - O que faz: Relaciona a categoria informada a um modelo oficial do catálogo.
 * - Como faz: Usa uma decisão local, determinística e informativa.
 * - Qual finalidade atende: Orienta a escolha de layout sem restringir a autonomia do estudante.
 */
export function obterRecomendacaoModelo(objetivo: ObjetivoCurriculo): string {
  switch (objetivo) {
    case "ats-simples":
      return "Recomendamos o modelo ATS simples por sua leitura otimizada para sistemas de triagem de vagas online.";
    case "administrativo-corporativo":
      return "Recomendamos o modelo Profissional clássico por sua hierarquia visual sóbria e tradicional.";
    case "compacto":
      return "Recomendamos o modelo Compacto para uma leitura rápida, direta e condensada em uma única página.";
    case "tecnologia":
      return "Recomendamos o modelo Moderno por equilibrar competências, projetos e experiência.";
    case "criativo-design":
      return "Recomendamos o modelo Criativo para dar maior destaque à identidade visual e aos projetos.";
    case "academico-pesquisador":
      return "Recomendamos o modelo Acadêmico para priorizar formação e projetos acadêmicos. Para perfis acadêmicos e pós-graduação, o Currículo Lattes é obrigatório.";
    case "primeiro-emprego":
      return "Recomendamos o modelo Primeiro emprego para valorizar formação, projetos e competências antes da experiência.";
    case "outro":
      return "Recomendamos o modelo Moderno por equilibrar competências, projetos e experiência de forma harmônica.";
  }
}

/** Define a estrutura mínima de perfil para inferir o objetivo profissional no cliente. */
export interface PerfilParaRecomendacao {
  experiencias?: ReadonlyArray<{
    empresa?: string;
    cargo?: string;
    descricao?: string;
  }>;
  formacoes?: ReadonlyArray<{
    nivel?: string;
    curriculoLattes?: string;
  }>;
  projetos?: ReadonlyArray<{
    titulo?: string;
    tecnologias?: string;
  }>;
  competencias?: {
    hardSkills?: ReadonlyArray<string>;
    softSkills?: ReadonlyArray<string>;
  };
}

/**
 * Infere o objetivo profissional mais adequado a partir do preenchimento das etapas anteriores.
 * Permite que o sistema pré-selecione o modelo ideal automaticamente no frontend.
 */
export function inferirObjetivoDoPerfil(
  perfil: PerfilParaRecomendacao,
): ObjetivoCurriculo {
  const temMestradoOuDoutorado = perfil.formacoes?.some(
    (f) => f.nivel === "mestrado" || f.nivel === "doutorado",
  );
  const temLattes = perfil.formacoes?.some((f) =>
    Boolean(f.curriculoLattes && f.curriculoLattes.trim().length > 0),
  );
  if (temMestradoOuDoutorado || temLattes) {
    return "academico-pesquisador";
  }

  const experienciasValidas =
    perfil.experiencias?.filter(
      (e) =>
        Boolean(e.empresa?.trim()) ||
        Boolean(e.cargo?.trim()) ||
        Boolean(e.descricao?.trim()),
    ) ?? [];

  if (experienciasValidas.length === 0) {
    return "primeiro-emprego";
  }

  const temProjetosValidos = perfil.projetos?.some(
    (p) => Boolean(p.titulo?.trim()) || Boolean(p.tecnologias?.trim()),
  );
  const temMuitasSkills = (perfil.competencias?.hardSkills?.length ?? 0) >= 3;

  if (temProjetosValidos || temMuitasSkills) {
    return "tecnologia";
  }

  return "administrativo-corporativo";
}
