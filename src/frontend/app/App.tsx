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
import { PaginaConfiguracoesPerfil } from "../pages/profile-settings";
import { PaginaDadosPessoais } from "../pages/personal-data";
import { PaginaPoliticaDePrivacidade } from "../pages/politica-de-privacidade";
import { PaginaCadastroProjetosAcademicos } from "../pages/projetos-academicos";
import { PaginaRecuperacaoSenha } from "../pages/recuperar-senha";
import { PaginaSelecaoModeloCurriculo } from "../pages/selecionar-modelo-curriculo";
import { PaginaTermosDeUso } from "../pages/termos-de-uso";
import { PaginaValidacaoCurriculo } from "../pages/validacao-curriculo";
import {
  PaginaVisualizacaoCurriculo,
  montarPreviaCurriculo,
} from "../pages/visualizar-curriculo";
import { PaginaVagasGrupo2 } from "../pages/vagas";
import type { UsuarioAutenticado } from "../widgets/cabecalho-publico";
import {
  criarClienteVagasDemonstracao,
  criarClienteDecisoesDemonstracao,
} from "../features/listar-vagas";
import { criarClienteAcessoDemonstracao } from "../features/acesso-estudante";
import "../shared/styles/animations.css";

const clienteVagasDemo = criarClienteVagasDemonstracao();
const clienteDecisoesDemo = criarClienteDecisoesDemonstracao();
const clienteAcessoDemo = criarClienteAcessoDemonstracao();

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
  | "termos-de-uso"
  | "politica-de-privacidade"
  | "validacao-curriculo"
  | "visualizar-curriculo"
  | "vagas"
  | "configuracoes-perfil"
  | "recuperar-senha";

/**
 * Redefine a posição de rolagem da janela e de contêineres internos para o topo.
 *
 * Como faz: desativa a restauração automática nativa do histórico (history.scrollRestoration = 'manual')
 * e redefine o scroll da janela (window), dos elementos raiz (documentElement, body) e de contêineres
 * internos com rolagem independente (como o painel de etapas do currículo e documentos legais).
 *
 * Qual finalidade atende: garante que aterrissar em qualquer tela ou alternar entre etapas
 * sempre inicie a visualização no topo, mesmo após rolagem prévia até o rodapé.
 */
function resetarScroll(): void {
  if (typeof window !== "undefined") {
    try {
      if ("scrollRestoration" in window.history) {
        window.history.scrollRestoration = "manual";
      }
    } catch {
      // Ignora erro em ambientes restritos
    }

    if (typeof window.scrollTo === "function") {
      window.scrollTo(0, 0);
    }
    if (document.documentElement) {
      document.documentElement.scrollTop = 0;
    }
    if (document.body) {
      document.body.scrollTop = 0;
    }

    const conteineres = document.querySelectorAll<HTMLElement>(
      ".layout-cadastro__conteudo, .pagina-documento-publico, .pagina-vagas, .pagina-visualizacao-curriculo, main, [data-scroll-container]",
    );
    conteineres.forEach((el) => {
      el.scrollTop = 0;
    });
  }
}

interface RascunhoCurriculo {
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

const CHAVE_RASCUNHO_CURRICULO = "liminal_curriculo_rascunho";

function carregarRascunho(): RascunhoCurriculo | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = sessionStorage.getItem(CHAVE_RASCUNHO_CURRICULO);
    return raw ? (JSON.parse(raw) as RascunhoCurriculo) : null;
  } catch {
    return null;
  }
}

function salvarRascunho(rascunho: RascunhoCurriculo): void {
  if (typeof window === "undefined") return;
  try {
    sessionStorage.setItem(CHAVE_RASCUNHO_CURRICULO, JSON.stringify(rascunho));
  } catch {
    // Ignora restrições de sessionStorage
  }
}

function limparRascunho(): void {
  if (typeof window === "undefined") return;
  try {
    sessionStorage.removeItem(CHAVE_RASCUNHO_CURRICULO);
  } catch {
    // Ignora restrições
  }
}

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
      if (etapa === "termos-de-uso") return "termos-de-uso";
      if (etapa === "politica-de-privacidade") return "politica-de-privacidade";
      if (etapa === "validacao-curriculo") return "validacao-curriculo";
      if (etapa === "visualizar-curriculo" || etapa === "previa")
        return "visualizar-curriculo";
      if (etapa === "vagas") return "vagas";
      if (etapa === "configuracoes-perfil" || etapa === "perfil")
        return "configuracoes-perfil";
      if (etapa === "recuperar-senha" || etapa === "recuperacao-senha")
        return "recuperar-senha";
      if (etapa === "acesso") return "acesso";
    }
    return "inicio";
  });

  const [usuarioLogado, setUsuarioLogado] = useState<UsuarioAutenticado | null>(
    () => {
      if (typeof window !== "undefined") {
        try {
          const salvo = sessionStorage.getItem("liminal_usuario_sessao");
          if (salvo) return JSON.parse(salvo);
        } catch {
          return null;
        }
      }
      return null;
    },
  );

  const [intencaoAcesso, setIntencaoAcesso] = useState<
    "criar-curriculo" | "criar-conta" | "login" | null
  >(() => {
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      const intencao = params.get("intencao");
      if (
        intencao === "criar-curriculo" ||
        intencao === "criar-conta" ||
        intencao === "login"
      ) {
        return intencao;
      }
    }
    return null;
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
      url.searchParams.delete("intencao");
      window.history.pushState({}, "", url.toString());
    }
    resetarScroll();
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
      url.searchParams.delete("intencao");
      window.history.pushState({}, "", url.toString());
    }
    resetarScroll();
    setIntencaoAcesso(null);
    setRotaAtiva("inicio");
  }

  /**
   * Abre o acesso da conta já selecionando a aba e preservando a intenção do fluxo.
   */
  function abrirAcesso(
    aba: "acesso" | "cadastro",
    intencao?: "criar-curriculo" | "criar-conta" | "login",
  ): void {
    setAbaAcesso(aba);
    if (intencao) {
      setIntencaoAcesso(intencao);
    }
    if (typeof window !== "undefined") {
      const url = new URL(window.location.href);
      url.searchParams.set("etapa", "acesso");
      if (aba === "cadastro") {
        url.searchParams.set("aba", "cadastro");
      } else {
        url.searchParams.delete("aba");
      }
      if (intencao) {
        url.searchParams.set("intencao", intencao);
      } else {
        url.searchParams.delete("intencao");
      }
      window.history.pushState({}, "", url.toString());
    }
    resetarScroll();
    setRotaAtiva("acesso");
  }

  function aoFazerLogout(): void {
    setUsuarioLogado(null);
    limparRascunho();
    setDadosPessoais(undefined);
    setFormacoes(undefined);
    setExperiencias(undefined);
    setCursos(undefined);
    setCertificacoes(undefined);
    setIdiomas(undefined);
    setCompetencias(undefined);
    setProjetos(undefined);
    setModelo("classico");
    if (typeof window !== "undefined") {
      try {
        sessionStorage.removeItem("liminal_usuario_sessao");
      } catch {
        // Ignora erro em ambientes sem suporte
      }
    }
    voltarAoInicio();
  }

  function aoClicarCriarCurriculo(): void {
    if (usuarioLogado) {
      navegar("dados-pessoais");
    } else {
      abrirAcesso("cadastro", "criar-curriculo");
    }
  }

  // Estados persistidos de cada etapa do cadastro com suporte a rascunho em sessionStorage
  const [dadosPessoais, setDadosPessoais] = useState<
    ValoresDadosPessoais | undefined
  >(() => carregarRascunho()?.dadosPessoais);
  const [formacoes, setFormacoes] = useState<
    ValoresFormacaoAcademica[] | undefined
  >(() => carregarRascunho()?.formacoes);
  const [experiencias, setExperiencias] = useState<Experiencia[] | undefined>(
    () => carregarRascunho()?.experiencias,
  );
  const [cursos, setCursos] = useState<Curso[] | undefined>(
    () => carregarRascunho()?.cursos,
  );
  const [certificacoes, setCertificacoes] = useState<
    ValoresCertificacao[] | undefined
  >(() => carregarRascunho()?.certificacoes);
  const [idiomas, setIdiomas] = useState<Idioma[] | undefined>(
    () => carregarRascunho()?.idiomas,
  );
  const [competencias, setCompetencias] = useState<Habilidades | undefined>(
    () => carregarRascunho()?.competencias,
  );
  const [projetos, setProjetos] = useState<
    ValoresProjetoAcademico[] | undefined
  >(() => carregarRascunho()?.projetos);
  const [modelo, setModelo] = useState<ModeloApresentacaoCurriculo>(
    () => carregarRascunho()?.modelo ?? "classico",
  );
  const [autoBaixarPdf, setAutoBaixarPdf] = useState(false);

  useEffect(() => {
    salvarRascunho({
      dadosPessoais,
      formacoes,
      experiencias,
      cursos,
      certificacoes,
      idiomas,
      competencias,
      projetos,
      modelo,
    });
  }, [
    dadosPessoais,
    formacoes,
    experiencias,
    cursos,
    certificacoes,
    idiomas,
    competencias,
    projetos,
    modelo,
  ]);

  /**
   * Navega para uma etapa interna e mantém a URL correspondente sincronizada.
   *
   * Como faz: atualiza o parâmetro `etapa` no histórico local e, em seguida,
   * altera o estado que determina a página exibida pela aplicação.
   *
   * Qual finalidade atende: preserva a navegação entre as etapas do currículo
   * sem depender de uma biblioteca externa de roteamento.
   */
  function navegar(etapa: RotaAtiva): void {
    if (typeof window !== "undefined") {
      const url = new URL(window.location.href);
      if (etapa === "inicio" || etapa === "acesso") {
        url.searchParams.delete("etapa");
      } else {
        url.searchParams.set("etapa", etapa);
      }
      window.history.pushState({}, "", url.toString());
    }
    resetarScroll();
    setRotaAtiva(etapa);
  }

  useEffect(() => {
    resetarScroll();
    if (typeof requestAnimationFrame === "function") {
      const frameId = requestAnimationFrame(() => {
        resetarScroll();
      });
      return () => cancelAnimationFrame(frameId);
    }
  }, [rotaAtiva]);

  useEffect(() => {
    /**
     * Recompõe a rota ativa após navegação pelo histórico do navegador.
     *
     * Como faz: lê o parâmetro `etapa` da URL exposta pelo evento `popstate`
     * e aplica a rota encontrada ou a página inicial como valor padrão.
     *
     * Qual finalidade atende: mantém a tela apresentada coerente quando a
     * pessoa utiliza os botões de avançar e voltar do navegador.
     */
    function aoMudarHistorico(): void {
      const params = new URLSearchParams(window.location.search);
      const etapa = params.get("etapa") as RotaAtiva | null;
      const intencao = params.get("intencao") as
        "criar-curriculo" | "criar-conta" | "login" | null;
      setIntencaoAcesso(intencao);
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
    },
    formacaoAcademica: {
      status: formacoes && formacoes.length > 0 ? "preenchida" : "pulada",
    },
    experienciasProfissionais: {
      status: experiencias && experiencias.length > 0 ? "preenchida" : "pulada",
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
        onVoltarInicio={voltarAoInicio}
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
        onVoltarInicio={voltarAoInicio}
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
        onVoltarInicio={voltarAoInicio}
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
        onVoltarInicio={voltarAoInicio}
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
        onVoltarInicio={voltarAoInicio}
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
        onVoltarInicio={voltarAoInicio}
      />
    );
  }

  if (rotaAtiva === "projetos-academicos") {
    return (
      <PaginaCadastroProjetosAcademicos
        aoAlterarProjetos={setProjetos}
        onAvancar={() => navegar("selecionar-modelo")}
        onVoltar={() => navegar("competencias")}
        onVoltarInicio={voltarAoInicio}
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
        onVoltarInicio={voltarAoInicio}
        perfilEstudante={{
          experiencias,
          formacoes,
          projetos,
          competencias,
        }}
      />
    );
  }

  if (rotaAtiva === "validacao-curriculo") {
    return (
      <PaginaValidacaoCurriculo
        dados={dadosValidacao}
        onCorrigirSecao={(secaoId) => navegar(secaoId)}
        onExportarPdf={() => {
          setAutoBaixarPdf(true);
          navegar("visualizar-curriculo");
        }}
        onVisualizarPreview={() => navegar("visualizar-curriculo")}
        onVoltar={() => navegar("selecionar-modelo")}
        onVoltarInicio={voltarAoInicio}
      />
    );
  }

  if (rotaAtiva === "visualizar-curriculo") {
    const previaCalculada = montarPreviaCurriculo({
      dadosPessoais,
      formacoes,
      experiencias,
      cursos,
      certificacoes,
      idiomas,
      competencias,
      projetos,
      modelo,
    });

    return (
      <PaginaVisualizacaoCurriculo
        aoAlterarModelo={() => navegar("selecionar-modelo")}
        autoBaixar={autoBaixarPdf}
        modelo={modelo}
        onExportarPdf={() => {
          setAutoBaixarPdf(false);
        }}
        onVoltar={() => {
          setAutoBaixarPdf(false);
          navegar("validacao-curriculo");
        }}
        onVoltarInicio={() => {
          setAutoBaixarPdf(false);
          voltarAoInicio();
        }}
        previa={previaCalculada}
      />
    );
  }

  if (rotaAtiva === "termos-de-uso") {
    return (
      <PaginaTermosDeUso
        onNavegarCadastro={() => abrirAcesso("cadastro", "criar-conta")}
        onNavegarInicio={voltarAoInicio}
        onNavegarLogin={() => abrirAcesso("acesso", "login")}
        onNavegarPoliticaDePrivacidade={() =>
          abrirDocumentoPublico("politica-de-privacidade")
        }
      />
    );
  }

  if (rotaAtiva === "politica-de-privacidade") {
    return (
      <PaginaPoliticaDePrivacidade
        onNavegarCadastro={() => abrirAcesso("cadastro", "criar-conta")}
        onNavegarInicio={voltarAoInicio}
        onNavegarLogin={() => abrirAcesso("acesso", "login")}
        onNavegarTermosDeUso={() => abrirDocumentoPublico("termos-de-uso")}
      />
    );
  }

  if (rotaAtiva === "acesso") {
    return (
      <PaginaAcessoEstudante
        abaInicial={abaAcesso}
        cliente={clienteAcessoDemo}
        onSucessoAcesso={(dados) => {
          const nomeResolvido = dados?.nome?.trim() || "";
          const emailResolvido = dados?.email?.trim() || "";
          const usuario: UsuarioAutenticado = {
            nome:
              nomeResolvido ||
              (emailResolvido ? emailResolvido.split("@")[0] : "Estudante"),
            email: emailResolvido,
          };

          setUsuarioLogado(usuario);
          if (typeof window !== "undefined") {
            try {
              sessionStorage.setItem(
                "liminal_usuario_sessao",
                JSON.stringify(usuario),
              );
            } catch {
              // Ignora erro em ambientes sem suporte a sessionStorage
            }
          }

          if (nomeResolvido || emailResolvido) {
            setDadosPessoais((atuais) => ({
              enderecoCompleto: atuais?.enderecoCompleto || "",
              telefones: atuais?.telefones || [""],
              linkedIn: atuais?.linkedIn || "",
              curriculoLattes: atuais?.curriculoLattes || "",
              nomeCompleto: nomeResolvido || atuais?.nomeCompleto || "",
              email: emailResolvido || atuais?.email || "",
            }));
          }

          const intencao = intencaoAcesso;
          setIntencaoAcesso(null);

          if (intencao === "criar-curriculo") {
            navegar("dados-pessoais");
          } else {
            voltarAoInicio();
          }
        }}
        onNavegarRecuperarSenha={() => navegar("recuperar-senha")}
        onVoltarInicio={voltarAoInicio}
      />
    );
  }

  if (rotaAtiva === "recuperar-senha") {
    return (
      <PaginaRecuperacaoSenha
        onVoltarInicio={voltarAoInicio}
        onVoltarLogin={() => abrirAcesso("acesso", "login")}
      />
    );
  }

  if (rotaAtiva === "vagas") {
    return (
      <PaginaVagasGrupo2
        cliente={clienteVagasDemo}
        clienteDecisoes={clienteDecisoesDemo}
        onVoltar={() => navegar("inicio")}
      />
    );
  }

  if (rotaAtiva === "configuracoes-perfil") {
    return <PaginaConfiguracoesPerfil onVoltar={() => navegar("inicio")} />;
  }

  return (
    <PaginaInicio
      onCriarCurriculo={aoClicarCriarCurriculo}
      onNavegarCadastro={() => abrirAcesso("cadastro", "criar-conta")}
      onNavegarLogin={() => abrirAcesso("acesso", "login")}
      onNavegarInicio={voltarAoInicio}
      onNavegarVagas={() => navegar("vagas")}
      onNavegarPerfil={() => navegar("configuracoes-perfil")}
      onNavegarPoliticaDePrivacidade={() =>
        abrirDocumentoPublico("politica-de-privacidade")
      }
      onNavegarTermosDeUso={() => abrirDocumentoPublico("termos-de-uso")}
      usuarioLogado={usuarioLogado}
      temProgressoCurriculo={Boolean(
        dadosPessoais?.nomeCompleto ||
        (formacoes && formacoes.length > 0) ||
        (experiencias && experiencias.length > 0) ||
        (cursos && cursos.length > 0),
      )}
      onLogout={aoFazerLogout}
    />
  );
}
