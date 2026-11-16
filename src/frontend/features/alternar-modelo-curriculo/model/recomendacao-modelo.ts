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
    inicio?: string;
    fim?: string;
    empregoAtual?: boolean;
  }>;
  formacoes?: ReadonlyArray<{
    nivel?: string;
    curriculoLattes?: string;
    curso?: string;
    instituicao?: string;
    status?: string;
  }>;
  projetos?: ReadonlyArray<{
    titulo?: string;
    tecnologias?: string;
    descricao?: string;
  }>;
  competencias?: {
    hardSkills?: ReadonlyArray<string>;
    softSkills?: ReadonlyArray<string>;
  };
  idiomas?: ReadonlyArray<{ nome?: string; nivel?: string }>;
  cursos?: ReadonlyArray<{ nome?: string; instituicao?: string }>;
  certificacoes?: ReadonlyArray<{
    nome?: string;
    organizacaoEmissora?: string;
  }>;
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

/** Um dado do perfil descrito como pergunta e resposta, para enviar à IA. */
export interface LinhaPerfilIa {
  pergunta: string;
  resposta: string;
}

/**
 * Resume o perfil preenchido nas etapas em até 10 linhas para a IA recomendar
 * o modelo.
 *
 * Como faz: agrupa cada seção numa linha (experiências com período, formação com
 * nível e situação, projetos, competências, idiomas, cursos e certificações) e
 * inclui o objetivo escolhido e a quantidade de itens, que pesa na escolha de
 * um modelo compacto. Não inclui nome nem contatos.
 */
export function resumirPerfilParaIa(
  perfil: PerfilParaRecomendacao | undefined,
  objetivo: string,
): LinhaPerfilIa[] {
  const linhas: LinhaPerfilIa[] = [
    { pergunta: "Objetivo do currículo", resposta: objetivo },
  ];
  if (!perfil) return linhas;
  const limpar = (itens: ReadonlyArray<string | undefined>, separador = ", ") =>
    itens
      .map((i) => i?.trim())
      .filter(Boolean)
      .join(separador);
  const adicionar = (pergunta: string, resposta: string) => {
    if (resposta) linhas.push({ pergunta, resposta: resposta.slice(0, 2000) });
  };

  const experiencias = perfil.experiencias ?? [];
  adicionar(
    `Experiências (${experiencias.length})`,
    limpar(
      experiencias.map((e) => {
        const periodo = e.inicio
          ? `${e.inicio} a ${e.empregoAtual ? "atual" : e.fim || "?"}`
          : "";
        return limpar([e.cargo, e.empresa, periodo, e.descricao], " - ");
      }),
      " | ",
    ),
  );
  if (experiencias.length === 0)
    adicionar("Experiência profissional", "Nenhuma informada");

  const formacoes = perfil.formacoes ?? [];
  adicionar(
    "Formação",
    limpar(
      formacoes.map((f) =>
        limpar([f.nivel, f.curso, f.instituicao, f.status], " - "),
      ),
      " | ",
    ),
  );
  if (formacoes.some((f) => f.curriculoLattes?.trim()))
    adicionar("Currículo Lattes", "Informado");

  const projetos = perfil.projetos ?? [];
  adicionar(
    `Projetos (${projetos.length})`,
    limpar(
      projetos.map((p) =>
        limpar([p.titulo, p.tecnologias, p.descricao], " - "),
      ),
      " | ",
    ),
  );
  adicionar(
    "Competências técnicas",
    limpar(perfil.competencias?.hardSkills ?? []),
  );
  adicionar(
    "Competências comportamentais",
    limpar(perfil.competencias?.softSkills ?? []),
  );
  adicionar(
    "Idiomas",
    limpar((perfil.idiomas ?? []).map((i) => limpar([i.nome, i.nivel], " "))),
  );
  adicionar(
    "Cursos",
    limpar(
      (perfil.cursos ?? []).map((c) => limpar([c.nome, c.instituicao], " - ")),
    ),
  );
  adicionar(
    "Certificações",
    limpar(
      (perfil.certificacoes ?? []).map((c) =>
        limpar([c.nome, c.organizacaoEmissora], " - "),
      ),
    ),
  );
  return linhas.slice(0, 10);
}
