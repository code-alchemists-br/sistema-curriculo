import { useEffect, useState } from "react";

import type { ModeloApresentacaoCurriculo } from "../features/alternar-modelo-curriculo";
import type { ValoresFormacaoAcademica } from "../features/cadastrar-formacao-academica";
import type { ValoresCertificacao } from "../features/cadastro-certificacoes";
import type { ValoresProjetoAcademico } from "../features/cadastro-projeto-academico";
import type { Curso } from "../features/edit-courses";
import type { Idioma } from "../features/edit-languages";
import type { ValoresDadosPessoais } from "../features/edit-personal-data";
import type { Experiencia } from "../features/edit-professional-experience";
import type { Habilidades } from "../features/edit-skills";
import type { CurriculoParaValidacao } from "../features/validate-curriculum";
import { PaginaAcessoEstudante } from "../pages/acesso-estudante";
import { PaginaCompetencias } from "../pages/competencias";
import { PaginaCursosCertificacoes } from "../pages/cursos-certificacoes";
import { PaginaExperienciasProfissionais } from "../pages/experiencias-profissionais";
import { PaginaFormacaoAcademica } from "../pages/formacao-academica";
import { PaginaIdiomas } from "../pages/idiomas";
import { PaginaInicio } from "../pages/inicio";
import { PaginaDadosPessoais } from "../pages/personal-data";
import { PaginaCadastroProjetosAcademicos } from "../pages/projetos-academicos";
import { PaginaSelecaoModeloCurriculo } from "../pages/selecionar-modelo-curriculo";
import { PaginaValidacaoCurriculo } from "../pages/validacao-curriculo";

type RotaAtiva =
  | "inicio"
  | "acesso"
  | "dados-pessoais"
  | "formacao-academica"
  | "experiencias-profissionais"
  | "cursos-certificacoes"
  | "cursos-idiomas"
  | "idiomas"
  | "competencias"
  | "projetos-academicos"
  | "selecionar-modelo"
  | "validacao-curriculo";

/**
 * Ponto de entrada da aplicação.
 *
 * Gerencia o estado central de dados de todas as seções do currículo para
 * garantir navegação bidirecional com preservação completa das informações
 * inseridas pelo estudante em qualquer uma das 9 etapas.
 */
export function App() {
  const [rotaAtiva, setRotaAtiva] = useState<RotaAtiva>(() => {
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      const etapa = params.get("etapa");
      if (etapa === "dados-pessoais") return "dados-pessoais";
      if (etapa === "formacao-academica") return "formacao-academica";
      if (etapa === "experiencias-profissionais")
        return "experiencias-profissionais";
      if (etapa === "cursos-certificacoes" || etapa === "cursos-idiomas")
        return "cursos-certificacoes";
      if (etapa === "idiomas") return "idiomas";
      if (etapa === "competencias") return "competencias";
      if (etapa === "projetos-academicos") return "projetos-academicos";
      if (etapa === "selecionar-modelo") return "selecionar-modelo";
      if (etapa === "validacao-curriculo") return "validacao-curriculo";
      if (etapa === "acesso") return "acesso";
    }
    return "inicio";
  });

  const [abaAcesso, setAbaAcesso] = useState<"acesso" | "cadastro">(() => {
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      if (params.get("aba") === "cadastro") return "cadastro";
    }
    return "acesso";
  });

  // Estados persistidos em memória de cada etapa do cadastro
  const [dadosPessoais, setDadosPessoais] = useState<ValoresDadosPessoais>();
  const [formacoes, setFormacoes] = useState<ValoresFormacaoAcademica[]>();
  const [experiencias, setExperiencias] = useState<Experiencia[]>();
  const [cursos, setCursos] = useState<Curso[]>();
  const [certificacoes, setCertificacoes] = useState<ValoresCertificacao[]>();
  const [idiomas, setIdiomas] = useState<Idioma[]>();
  const [competencias, setCompetencias] = useState<Habilidades>();
  const [projetos, setProjetos] = useState<ValoresProjetoAcademico[]>();
  const [modelo, setModelo] = useState<ModeloApresentacaoCurriculo>("classico");

  function navegar(etapa: RotaAtiva) {
    if (typeof window !== "undefined") {
      const url = new URL(window.location.href);
      if (etapa === "inicio" || etapa === "acesso") {
        url.searchParams.delete("etapa");
      } else {
        url.searchParams.set("etapa", etapa);
      }
      window.history.pushState({}, "", url.toString());
    }
    setRotaAtiva(etapa);
  }

  useEffect(() => {
    function aoMudarHistorico() {
      const params = new URLSearchParams(window.location.search);
      const etapa = params.get("etapa") as RotaAtiva | null;
      if (etapa) {
        setRotaAtiva(etapa);
      } else {
        setRotaAtiva("inicio");
      }
    }
    window.addEventListener("popstate", aoMudarHistorico);
    return () => window.removeEventListener("popstate", aoMudarHistorico);
  }, []);

  const dadosValidacao: CurriculoParaValidacao = {
    dadosPessoais: {
      nomeCompleto: dadosPessoais?.nomeCompleto || "Nome não informado",
      enderecoCompleto: dadosPessoais?.enderecoCompleto || "",
      telefones:
        dadosPessoais?.telefones?.filter((t) => t.trim().length > 0) || [],
      email: dadosPessoais?.email || "",
      linkedIn: dadosPessoais?.linkedIn || undefined,
    },
    formacaoAcademica: {
      status: formacoes && formacoes.length > 0 ? "preenchida" : "vazia",
    },
    experienciasProfissionais: {
      status: experiencias && experiencias.length > 0 ? "preenchida" : "vazia",
    },
    competencias: competencias ?? {
      hardSkills: [],
      softSkills: [],
    },
    projetosAcademicos:
      projetos?.map((p) => ({
        titulo: p.titulo,
        descricao: p.descricao,
        tecnologias: p.tecnologias,
      })) ?? [],
  };

  if (rotaAtiva === "dados-pessoais") {
    return (
      <PaginaDadosPessoais
        aoAvancar={() => navegar("formacao-academica")}
        aoAlterarValores={setDadosPessoais}
        onVoltar={() => navegar("inicio")}
        valoresIniciais={dadosPessoais}
      />
    );
  }

  if (rotaAtiva === "formacao-academica") {
    return (
      <PaginaFormacaoAcademica
        aoAlterarFormacoes={setFormacoes}
        formacoesIniciais={formacoes}
        onAvancar={() => navegar("experiencias-profissionais")}
        onVoltar={() => navegar("dados-pessoais")}
      />
    );
  }

  if (rotaAtiva === "experiencias-profissionais") {
    return (
      <PaginaExperienciasProfissionais
        aoAlterarExperiencias={setExperiencias}
        experienciasIniciais={experiencias}
        onSalvar={() => navegar("cursos-certificacoes")}
        onVoltar={() => navegar("formacao-academica")}
      />
    );
  }

  if (rotaAtiva === "cursos-certificacoes" || rotaAtiva === "cursos-idiomas") {
    return (
      <PaginaCursosCertificacoes
        aoAlterarCertificacoes={setCertificacoes}
        aoAlterarCursos={setCursos}
        certificacoesIniciais={certificacoes}
        cursosIniciais={cursos}
        onAvancar={() => navegar("idiomas")}
        onVoltar={() => navegar("experiencias-profissionais")}
      />
    );
  }

  if (rotaAtiva === "idiomas") {
    return (
      <PaginaIdiomas
        idiomasIniciais={idiomas}
        onAvancar={() => navegar("competencias")}
        onSalvar={setIdiomas}
        onVoltar={() => navegar("cursos-certificacoes")}
      />
    );
  }

  if (rotaAtiva === "competencias") {
    return (
      <PaginaCompetencias
        competenciasIniciais={competencias}
        onAvancar={() => navegar("projetos-academicos")}
        onSalvar={setCompetencias}
        onVoltar={() => navegar("idiomas")}
      />
    );
  }

  if (rotaAtiva === "projetos-academicos") {
    return (
      <PaginaCadastroProjetosAcademicos
        aoAlterarProjetos={setProjetos}
        onAvancar={() => navegar("selecionar-modelo")}
        onVoltar={() => navegar("competencias")}
        projetosIniciais={projetos}
      />
    );
  }

  if (rotaAtiva === "selecionar-modelo") {
    return (
      <PaginaSelecaoModeloCurriculo
        aoConfirmar={(novoModelo) => {
          setModelo(novoModelo);
          navegar("validacao-curriculo");
        }}
        modeloInicial={modelo}
        onVoltar={() => navegar("projetos-academicos")}
      />
    );
  }

  if (rotaAtiva === "validacao-curriculo") {
    return (
      <PaginaValidacaoCurriculo
        dados={dadosValidacao}
        onVoltar={() => navegar("selecionar-modelo")}
      />
    );
  }

  if (rotaAtiva === "acesso") {
    return (
      <PaginaAcessoEstudante
        abaInicial={abaAcesso}
        onVoltarInicio={() => {
          if (typeof window !== "undefined") {
            const url = new URL(window.location.href);
            url.searchParams.delete("etapa");
            url.searchParams.delete("aba");
            window.history.pushState({}, "", url.toString());
          }
          setRotaAtiva("inicio");
        }}
      />
    );
  }

  return (
    <PaginaInicio
      onCriarCurriculo={() => navegar("dados-pessoais")}
      onNavegarCadastro={() => {
        setAbaAcesso("cadastro");
        if (typeof window !== "undefined") {
          const url = new URL(window.location.href);
          url.searchParams.set("etapa", "acesso");
          url.searchParams.set("aba", "cadastro");
          window.history.pushState({}, "", url.toString());
        }
        setRotaAtiva("acesso");
      }}
      onNavegarLogin={() => {
        setAbaAcesso("acesso");
        if (typeof window !== "undefined") {
          const url = new URL(window.location.href);
          url.searchParams.set("etapa", "acesso");
          url.searchParams.delete("aba");
          window.history.pushState({}, "", url.toString());
        }
        setRotaAtiva("acesso");
      }}
      onNavegarInicio={() => navegar("inicio")}
    />
  );
}
