import { useState } from "react";

import { PaginaAcessoEstudante } from "../pages/acesso-estudante";
import { PaginaCompetencias } from "../pages/competencias";
import { PaginaCursosIdiomas } from "../pages/cursos-idiomas";
import { PaginaExperienciasProfissionais } from "../pages/experiencias-profissionais";
import { PaginaFormacaoAcademica } from "../pages/formacao-academica";
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
  | "cursos-idiomas"
  | "competencias"
  | "projetos-academicos"
  | "selecionar-modelo"
  | "validacao-curriculo";

/**
 * Ponto de entrada da aplicação.
 *
 * Apresenta a página inicial pública da LIMINAL com a seção Hero e o cabeçalho.
 * O CTA de criar currículo conduz diretamente ao Wizard de cadastro de dados pessoais.
 * A ação de login conduz à tela de acesso e gerenciamento de conta do estudante.
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
      if (etapa === "cursos-idiomas") return "cursos-idiomas";
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

  if (rotaAtiva === "dados-pessoais") {
    return <PaginaDadosPessoais />;
  }

  if (rotaAtiva === "formacao-academica") {
    return <PaginaFormacaoAcademica />;
  }

  if (rotaAtiva === "experiencias-profissionais") {
    return <PaginaExperienciasProfissionais />;
  }

  if (rotaAtiva === "cursos-idiomas") {
    return (
      <PaginaCursosIdiomas
        onAvancar={() => {
          if (typeof window !== "undefined") {
            const url = new URL(window.location.href);
            url.searchParams.set("etapa", "competencias");
            window.history.pushState({}, "", url.toString());
          }
          setRotaAtiva("competencias");
        }}
      />
    );
  }

  if (rotaAtiva === "competencias") {
    return <PaginaCompetencias />;
  }

  if (rotaAtiva === "projetos-academicos") {
    return (
      <PaginaCadastroProjetosAcademicos
        onAvancar={() => {
          if (typeof window !== "undefined") {
            const url = new URL(window.location.href);
            url.searchParams.set("etapa", "selecionar-modelo");
            window.history.pushState({}, "", url.toString());
          }
          setRotaAtiva("selecionar-modelo");
        }}
      />
    );
  }

  if (rotaAtiva === "selecionar-modelo") {
    return (
      <PaginaSelecaoModeloCurriculo
        aoConfirmar={() => {
          if (typeof window !== "undefined") {
            const url = new URL(window.location.href);
            url.searchParams.set("etapa", "validacao-curriculo");
            window.history.pushState({}, "", url.toString());
          }
          setRotaAtiva("validacao-curriculo");
        }}
      />
    );
  }

  if (rotaAtiva === "validacao-curriculo") {
    return <PaginaValidacaoCurriculo />;
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
      onCriarCurriculo={() => setRotaAtiva("dados-pessoais")}
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
      onNavegarInicio={() => setRotaAtiva("inicio")}
    />
  );
}
