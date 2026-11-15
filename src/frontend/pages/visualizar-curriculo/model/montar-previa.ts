import type { PreviaCurriculo } from "../../../entities/curriculo";
import type { ModeloApresentacaoCurriculo } from "../../../features/alternar-modelo-curriculo";
import type { ValoresFormacaoAcademica } from "../../../features/cadastrar-formacao-academica";
import type { ValoresCertificacao } from "../../../features/cadastro-certificacoes";
import type { ValoresProjetoAcademico } from "../../../features/cadastro-projeto-academico";
import type { Curso } from "../../../features/edit-courses";
import {
  NIVEIS_IDIOMA,
  type Idioma,
  type NivelIdioma,
} from "../../../features/edit-languages";
import type { ValoresDadosPessoais } from "../../../features/edit-personal-data";
import type { Experiencia } from "../../../features/edit-professional-experience";
import type { Habilidades } from "../../../features/edit-skills";

/** Dados consolidados coletados nas etapas do Wizard para compor a prévia do currículo. */
export interface DadosParaMontagemPrevia {
  dadosPessoais?: ValoresDadosPessoais;
  formacoes?: ValoresFormacaoAcademica[];
  experiencias?: Experiencia[];
  cursos?: Curso[];
  certificacoes?: ValoresCertificacao[];
  idiomas?: Idioma[];
  competencias?: Habilidades;
  projetos?: ValoresProjetoAcademico[];
  modelo?: ModeloApresentacaoCurriculo;
}

/** Garante que datas inseridas pelo usuário tenham formato ISO seguro para Intl.DateTimeFormat. */
function normalizarData(data?: string | null): string {
  if (!data || typeof data !== "string") return "2024-01-01";
  const trimmed = data.trim();
  if (/^\d{4}-\d{2}-\d{2}$/.test(trimmed)) return trimmed;
  if (/^\d{4}-\d{2}$/.test(trimmed)) return `${trimmed}-01`;
  if (/^\d{4}$/.test(trimmed)) return `${trimmed}-01-01`;
  return "2024-01-01";
}

/**
 * Converte os dados das seções preenchidas pelo estudante na entidade canônica PreviaCurriculo.
 *
 * Mapeia contatos, formações, experiências, competências, idiomas e certificados
 * sem perder informações nem introduzir dependências de backend em runtime.
 */
export function montarPreviaCurriculo(
  dados: DadosParaMontagemPrevia,
): PreviaCurriculo {
  const {
    dadosPessoais,
    formacoes = [],
    experiencias = [],
    cursos = [],
    certificacoes = [],
    idiomas = [],
    competencias,
    projetos = [],
    modelo = "classico",
  } = dados;

  const nomeEstudante = dadosPessoais?.nomeCompleto?.trim() || "Estudante";
  const emailEstudante = dadosPessoais?.email?.trim() || "";
  const telefonesEstudante =
    dadosPessoais?.telefones?.filter((t) => t.trim().length > 0) || [];

  const lattesFormacao = formacoes.find(
    (f) => f.curriculoLattes && f.curriculoLattes.trim().length > 0,
  )?.curriculoLattes;
  const lattesFinal =
    dadosPessoais?.curriculoLattes?.trim() || lattesFormacao?.trim() || null;

  return {
    curriculo_id: "curriculo-principal",
    titulo_versao: `Currículo de ${nomeEstudante}`,
    layout: modelo,
    estudante: {
      nome: nomeEstudante,
      email: emailEstudante,
      contato: {
        endereco: dadosPessoais?.enderecoCompleto?.trim() || "",
        telefones: telefonesEstudante,
        linkedin: dadosPessoais?.linkedIn?.trim() || null,
        curriculo_lattes: lattesFinal,
      },
    },
    formacoes: formacoes.map((formacao, index) => ({
      id: `formacao-${index + 1}`,
      instituicao: formacao.instituicao || "Instituição de ensino",
      curso: formacao.curso || "Curso superior",
      nivel: formacao.nivel || "Graduação",
      status: formacao.status === "concluido" ? "Concluído" : "Em andamento",
      inicio: normalizarData(formacao.dataInicio),
      fim:
        formacao.status === "concluido" && formacao.dataFim
          ? normalizarData(formacao.dataFim)
          : null,
    })),
    experiencias: experiencias.map((exp, index) => ({
      id: `experiencia-${index + 1}`,
      empresa: exp.empresa || "Empresa",
      cargo: exp.cargo || "Profissional",
      descricao: exp.descricao || "",
      inicio: normalizarData(exp.inicio),
      fim: exp.empregoAtual || !exp.fim ? null : normalizarData(exp.fim),
    })),
    projetos: projetos.map((proj, index) => ({
      id: `projeto-${index + 1}`,
      titulo: proj.titulo || "Projeto acadêmico",
      descricao: proj.descricao || "",
      tecnologias: proj.tecnologias || "",
    })),
    competencias: [
      ...(competencias?.hardSkills?.map((hard, index) => ({
        id: `competencia-hard-${index + 1}`,
        descricao: hard,
        nivel: "Técnica",
      })) || []),
      ...(competencias?.softSkills?.map((soft, index) => ({
        id: `competencia-soft-${index + 1}`,
        descricao: soft,
        nivel: "Comportamental",
      })) || []),
    ],
    idiomas: idiomas.map((idioma, index) => ({
      id: `idioma-${index + 1}`,
      idioma: idioma.nome || "Idioma",
      nivel:
        idioma.nivel && NIVEIS_IDIOMA[idioma.nivel as NivelIdioma]
          ? NIVEIS_IDIOMA[idioma.nivel as NivelIdioma]
          : "Básico",
    })),
    documentos: [
      ...certificacoes.map((cert, index) => ({
        id: `certificacao-${index + 1}`,
        nome_arquivo: cert.nome || "Certificação profissional",
        tipo_arquivo: cert.organizacaoEmissora
          ? `Emissão: ${cert.organizacaoEmissora}`
          : "Certificado",
      })),
      ...cursos.map((curso, index) => ({
        id: `curso-${index + 1}`,
        nome_arquivo: curso.nome || "Curso de aperfeiçoamento",
        tipo_arquivo: curso.instituicao
          ? `Carga horária: ${curso.cargaHoraria}h — ${curso.instituicao}`
          : `${curso.cargaHoraria}h`,
      })),
    ],
  };
}
