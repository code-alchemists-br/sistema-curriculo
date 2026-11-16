import type { ModeloApresentacaoCurriculo } from "../features/alternar-modelo-curriculo";
import type { ValoresFormacaoAcademica } from "../features/cadastrar-formacao-academica";
import type { ValoresCertificacao } from "../features/cadastro-certificacoes";
import type { ValoresProjetoAcademico } from "../features/cadastro-projeto-academico";
import type { Curso } from "../features/edit-courses";
import type { Idioma, NivelIdioma } from "../features/edit-languages";
import type { ValoresDadosPessoais } from "../features/edit-personal-data";
import type { Experiencia } from "../features/edit-professional-experience";
import type { Habilidades } from "../features/edit-skills";

/** Currículo no formato que as telas do cadastro usam. */
export interface CurriculoDasTelas {
  dadosPessoais: ValoresDadosPessoais;
  formacoes: ValoresFormacaoAcademica[];
  experiencias: Experiencia[];
  cursos: Curso[];
  certificacoes: ValoresCertificacao[];
  idiomas: Idioma[];
  competencias: Habilidades;
  projetos: ValoresProjetoAcademico[];
  modelo: ModeloApresentacaoCurriculo | null;
}

/**
 * Falha ao salvar ou ler o currículo, com mensagem pronta para a tela.
 *
 * Existe para que nenhuma etapa avance fingindo que salvou: quem chama mostra
 * `message` ao estudante e mantém os dados digitados para tentar de novo.
 */
export class FalhaCurriculoNoBanco extends Error {
  constructor(
    message: string,
    public readonly status: number | null,
  ) {
    super(message);
    this.name = "FalhaCurriculoNoBanco";
  }
}

type Secao =
  | "formacoes"
  | "experiencias"
  | "projetos"
  | "competencias"
  | "idiomas"
  | "cursos"
  | "certificacoes";

/**
 * Cliente que lê e grava o currículo inteiro do estudante logado.
 *
 * - O que faz: lê tudo o que foi salvo (GET /estudantes/me/curriculo) e troca
 *   uma seção inteira pela lista atual da tela (PUT .../{secao}).
 * - Como faz: converte entre o formato das telas e o da API e transforma
 *   qualquer resposta de erro em `FalhaCurriculoNoBanco` com texto amigável.
 * - Qual finalidade atende: o banco passa a ser a fonte do currículo; salvar
 *   de novo uma etapa substitui os itens em vez de duplicar.
 */
export function criarClienteCurriculoNoBanco(urlDaApi: string) {
  const base = urlDaApi.replace(/\/+$/, "");

  async function requisitar(metodo: string, caminho: string, corpo?: unknown) {
    let resposta: Response;
    try {
      resposta = await fetch(`${base}/estudantes/me/curriculo${caminho}`, {
        method: metodo,
        headers: corpo === undefined ? undefined : { "Content-Type": "application/json" },
        body: corpo === undefined ? undefined : JSON.stringify(corpo),
        credentials: "include",
      });
    } catch {
      throw new FalhaCurriculoNoBanco(
        "Sem conexão com o servidor. Seus dados continuam aqui; tente novamente.",
        null,
      );
    }
    if (resposta.ok) return resposta;
    throw new FalhaCurriculoNoBanco(await mensagemDeErro(resposta), resposta.status);
  }

  return {
    async carregar(): Promise<CurriculoDasTelas> {
      const resposta = await requisitar("GET", "");
      return paraTelas(await resposta.json());
    },

    async salvarFormacoes(formacoes: ValoresFormacaoAcademica[]): Promise<void> {
      const lattes = formacoes.some((f) => f.naoPossuiLattes)
        ? undefined
        : formacoes.find((f) => f.curriculoLattes?.trim())?.curriculoLattes?.trim();
      await requisitar("PUT", "/formacoes", {
        curriculo_lattes: lattes || null,
        itens: formacoes
          .filter((f) => f.instituicao.trim() || f.curso.trim())
          .map((f) => ({
            instituicao: f.instituicao.trim(),
            curso: f.curso.trim(),
            nivel: f.nivel,
            status: f.status,
            data_inicio: dataCompleta(f.dataInicio),
            data_fim: f.status === "concluido" || f.dataFim ? dataCompleta(f.dataFim) : null,
          })),
      });
    },

    async salvarExperiencias(experiencias: Experiencia[]): Promise<void> {
      await salvarSecao("experiencias", experiencias
        .filter((e) => e.empresa.trim() || e.cargo.trim())
        .map((e) => ({
          empresa: e.empresa.trim(),
          cargo: e.cargo.trim(),
          descricao: e.descricao.trim(),
          data_inicio: dataCompleta(e.inicio),
          data_fim: e.empregoAtual ? null : dataCompleta(e.fim),
        })));
    },

    async salvarCursos(cursos: Curso[]): Promise<void> {
      await salvarSecao("cursos", cursos
        .filter((c) => c.nome.trim())
        .map((c) => ({
          nome: c.nome.trim(),
          instituicao: c.instituicao.trim(),
          carga_horaria: c.cargaHoraria.trim() ? Number(c.cargaHoraria) : null,
        })));
    },

    async salvarCertificacoes(certificacoes: ValoresCertificacao[]): Promise<void> {
      await salvarSecao("certificacoes", certificacoes
        .filter((c) => c.nome.trim())
        .map((c) => ({ nome: c.nome.trim(), organizacao_emissora: c.organizacaoEmissora.trim() })));
    },

    async salvarIdiomas(idiomas: Idioma[]): Promise<void> {
      await salvarSecao("idiomas", idiomas
        .filter((i) => i.nome.trim() && i.nivel)
        .map((i) => ({ idioma: i.nome.trim(), nivel: i.nivel })));
    },

    async salvarCompetencias(competencias: Habilidades): Promise<void> {
      await salvarSecao("competencias", [
        ...competencias.hardSkills.map((d) => ({ categoria: "tecnica", descricao: d.trim() })),
        ...competencias.softSkills.map((d) => ({ categoria: "comportamental", descricao: d.trim() })),
      ].filter((c) => c.descricao));
    },

    async salvarProjetos(projetos: ValoresProjetoAcademico[]): Promise<void> {
      await salvarSecao("projetos", projetos
        .filter((p) => p.titulo.trim() || p.descricao.trim())
        .map((p) => ({
          titulo: p.titulo.trim(),
          descricao: p.descricao.trim(),
          tecnologias: p.tecnologias.trim(),
        })));
    },

    async salvarModelo(modelo: ModeloApresentacaoCurriculo): Promise<void> {
      await requisitar("PUT", "/modelo", { modelo });
    },
  };

  async function salvarSecao(secao: Secao, itens: unknown[]): Promise<void> {
    await requisitar("PUT", `/${secao}`, { itens });
  }
}

export type ClienteCurriculoNoBanco = ReturnType<typeof criarClienteCurriculoNoBanco>;

/** Converte "2025-03" ou "2025-03-01" na data completa que a API espera. */
function dataCompleta(data: string | undefined): string | null {
  const limpa = data?.trim();
  if (!limpa) return null;
  return /^\d{4}-\d{2}$/.test(limpa) ? `${limpa}-01` : limpa;
}

/** Traduz a resposta de erro em uma frase que o estudante entenda. */
async function mensagemDeErro(resposta: Response): Promise<string> {
  if (resposta.status === 401) return "Sua sessão expirou. Entre novamente para salvar.";
  if (resposta.status === 409) return "Há itens repetidos. Remova as repetições e tente de novo.";
  if (resposta.status >= 500) {
    return "O servidor não conseguiu salvar agora. Seus dados continuam aqui; tente novamente.";
  }
  try {
    const corpo = await resposta.json();
    if (typeof corpo?.detail === "string") return `Não foi possível salvar: ${corpo.detail}`;
  } catch {
    // Sem corpo legível: usa a mensagem genérica abaixo.
  }
  return "Algum dado não foi aceito pelo servidor. Confira os campos e tente de novo.";
}

/** Converte a resposta da API para o formato das telas. */
function paraTelas(api: any): CurriculoDasTelas {
  const dados = api.dados_pessoais ?? {};
  const endereco = [dados.endereco, dados.cidade].filter(Boolean).join(", ");
  const lattes = dados.curriculo_lattes ?? "";
  return {
    dadosPessoais: {
      nomeCompleto: dados.nome ?? "",
      email: dados.email ?? "",
      enderecoCompleto: endereco,
      telefones: dados.telefones?.length ? dados.telefones : [""],
      linkedIn: dados.linkedin ?? "",
      curriculoLattes: lattes,
    },
    formacoes: (api.formacoes ?? []).map((f: any) => ({
      instituicao: f.instituicao,
      curso: f.curso,
      nivel: f.nivel,
      status: f.status,
      dataInicio: f.data_inicio ?? "",
      dataFim: f.data_fim ?? "",
      curriculoLattes: lattes,
      naoPossuiLattes: !lattes,
    })),
    experiencias: (api.experiencias ?? []).map((e: any) => ({
      empresa: e.empresa,
      cargo: e.cargo,
      descricao: e.descricao,
      inicio: e.data_inicio ?? "",
      fim: e.data_fim ?? "",
      empregoAtual: !e.data_fim,
    })),
    cursos: (api.cursos ?? []).map((c: any) => ({
      nome: c.nome,
      instituicao: c.instituicao,
      cargaHoraria: c.carga_horaria == null ? "" : String(c.carga_horaria),
    })),
    certificacoes: (api.certificacoes ?? []).map((c: any) => ({
      nome: c.nome,
      organizacaoEmissora: c.organizacao_emissora,
    })),
    idiomas: (api.idiomas ?? []).map((i: any) => ({
      nome: i.idioma,
      nivel: i.nivel as NivelIdioma,
    })),
    competencias: {
      hardSkills: (api.competencias ?? [])
        .filter((c: any) => c.categoria === "tecnica")
        .map((c: any) => c.descricao),
      softSkills: (api.competencias ?? [])
        .filter((c: any) => c.categoria === "comportamental")
        .map((c: any) => c.descricao),
    },
    projetos: (api.projetos ?? []).map((p: any) => ({
      titulo: p.titulo,
      descricao: p.descricao,
      tecnologias: p.tecnologias,
    })),
    modelo: api.modelo ?? null,
  };
}
