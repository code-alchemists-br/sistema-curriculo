import { useState } from "react";

import { PaginaAcessoEstudante } from "../pages/acesso-estudante";
import { PaginaCompetencias } from "../pages/competencias";
import { PaginaCursosIdiomas } from "../pages/cursos-idiomas";
import { PaginaExperienciasProfissionais } from "../pages/experiencias-profissionais";
import { PaginaFormacaoAcademica } from "../pages/formacao-academica";
import { PaginaInicio } from "../pages/inicio";
import { PaginaDadosPessoais } from "../pages/personal-data";
import { PaginaPoliticaDePrivacidade } from "../pages/politica-de-privacidade";
import { PaginaCadastroProjetosAcademicos } from "../pages/projetos-academicos";
import { PaginaSelecaoModeloCurriculo } from "../pages/selecionar-modelo-curriculo";
import { PaginaTermosDeUso } from "../pages/termos-de-uso";
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
  | "termos-de-uso"
  | "politica-de-privacidade"
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
      if (etapa === "termos-de-uso") return "termos-de-uso";
      if (etapa === "politica-de-privacidade") return "politica-de-privacidade";
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

  /**
   * Abre uma página pública de documento e registra a etapa na URL.
   *
   * Como faz: atualiza somente o parâmetro `etapa` do histórico local e o
   * estado da rota, preservando o mecanismo de navegação leve já usado no App.
   *
   * Qual finalidade atende: permite que os documentos legais sejam acessíveis
   * por links internos e por URL sem introduzir uma biblioteca de rotas.
   */
  function abrirDocumentoPublico(
    rota: "termos-de-uso" | "politica-de-privacidade",
  ): void {
    if (typeof window !== "undefined") {
      const url = new URL(window.location.href);
      url.searchParams.set("etapa", rota);
      url.searchParams.delete("aba");
      window.history.pushState({}, "", url.toString());
    }
    setRotaAtiva(rota);
  }

  /**
   * Retorna à página inicial e remove parâmetros de navegação temporários.
   *
   * Como faz: limpa os parâmetros usados pelo App no endereço atual antes de
   * atualizar o estado local que determina a composição exibida.
   *
   * Qual finalidade atende: garante que os documentos públicos tenham um
   * caminho de retorno previsível, inclusive para navegação por teclado.
   */
  function voltarAoInicio(): void {
    if (typeof window !== "undefined") {
      const url = new URL(window.location.href);
      url.searchParams.delete("etapa");
      url.searchParams.delete("aba");
      window.history.pushState({}, "", url.toString());
    }
    setRotaAtiva("inicio");
  }

  /**
   * Abre o acesso da conta já selecionando a aba solicitada.
   *
   * Como faz: sincroniza o estado local da aba com os parâmetros da URL antes
   * de trocar a composição ativa para a página de acesso.
   *
   * Qual finalidade atende: reutiliza a mesma entrada de autenticação nos
   * cabeçalhos das páginas públicas sem duplicar a regra de navegação.
   */
  function abrirAcesso(aba: "acesso" | "cadastro"): void {
    setAbaAcesso(aba);
    if (typeof window !== "undefined") {
      const url = new URL(window.location.href);
      url.searchParams.set("etapa", "acesso");
      if (aba === "cadastro") {
        url.searchParams.set("aba", "cadastro");
      } else {
        url.searchParams.delete("aba");
      }
      window.history.pushState({}, "", url.toString());
    }
    setRotaAtiva("acesso");
  }

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

  if (rotaAtiva === "termos-de-uso") {
    return (
      <PaginaTermosDeUso
        onNavegarCadastro={() => abrirAcesso("cadastro")}
        onNavegarInicio={voltarAoInicio}
        onNavegarLogin={() => abrirAcesso("acesso")}
        onNavegarPoliticaDePrivacidade={() =>
          abrirDocumentoPublico("politica-de-privacidade")
        }
      />
    );
  }

  if (rotaAtiva === "politica-de-privacidade") {
    return (
      <PaginaPoliticaDePrivacidade
        onNavegarCadastro={() => abrirAcesso("cadastro")}
        onNavegarInicio={voltarAoInicio}
        onNavegarLogin={() => abrirAcesso("acesso")}
        onNavegarTermosDeUso={() => abrirDocumentoPublico("termos-de-uso")}
      />
    );
  }

  if (rotaAtiva === "acesso") {
    return (
      <PaginaAcessoEstudante
        abaInicial={abaAcesso}
        onVoltarInicio={voltarAoInicio}
      />
    );
  }

  return (
    <PaginaInicio
      onCriarCurriculo={() => setRotaAtiva("dados-pessoais")}
      onNavegarCadastro={() => abrirAcesso("cadastro")}
      onNavegarLogin={() => abrirAcesso("acesso")}
      onNavegarInicio={voltarAoInicio}
      onNavegarPoliticaDePrivacidade={() =>
        abrirDocumentoPublico("politica-de-privacidade")
      }
      onNavegarTermosDeUso={() => abrirDocumentoPublico("termos-de-uso")}
    />
  );
}
