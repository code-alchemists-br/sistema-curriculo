import { useEffect, useMemo, useRef, useState } from "react";

import type { ModeloApresentacaoCurriculo } from "../features/alternar-modelo-curriculo";
import type { ValoresFormacaoAcademica } from "../features/cadastrar-formacao-academica";
import type { ValoresCertificacao } from "../features/cadastro-certificacoes";
import type { ValoresProjetoAcademico } from "../features/cadastro-projeto-academico";
import type { Curso } from "../features/edit-courses";
import type { Idioma } from "../features/edit-languages";
import type { ValoresDadosPessoais } from "../features/edit-personal-data";
import type { Experiencia } from "../features/edit-professional-experience";
import type { Habilidades } from "../features/edit-skills";
import {
  validarCurriculo,
  type CurriculoParaValidacao,
} from "../features/validate-curriculum";
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
  exportarPreviaParaDocx,
  exportarElementoParaPdf,
} from "../pages/visualizar-curriculo";
import { PaginaVagasGrupo2 } from "../pages/vagas";
import type { UsuarioAutenticado } from "../widgets/cabecalho-publico";
import {
  criarClienteVagasDemonstracao,
  criarClienteVagasHttp,
  criarClienteDecisoesDemonstracao,
} from "../features/listar-vagas";
import {
  criarClienteAcessoDemonstracao,
  criarClienteAcessoEstudante,
} from "../features/acesso-estudante";
import { criarClienteDadosPessoaisHttp } from "../features/edit-personal-data";
import { criarClienteFormacaoAcademicaHttp } from "../features/cadastrar-formacao-academica";
import { criarClienteExperienciasHttp } from "../features/edit-professional-experience";
import { criarClienteCursosHttp } from "../features/edit-courses";
import { criarClienteCertificacoesHttp } from "../features/cadastro-certificacoes";
import { criarClienteIdiomasHttp } from "../features/edit-languages";
import { criarClienteCompetenciasHttp } from "../features/edit-skills";
import { criarClienteProjetosAcademicosHttp } from "../features/cadastro-projeto-academico";
import {
  criarClienteAcessoResiliente,
  criarClienteDadosPessoaisResiliente,
  criarClienteFormacaoAcademicaResiliente,
  criarClienteVagasResiliente,
} from "./servicos-resilientes";
import "../shared/styles/animations.css";

const apiBaseUrl = import.meta.env.VITE_API_URL;
const clienteVagasDemo = criarClienteVagasDemonstracao();
const clienteVagasBase = apiBaseUrl
  ? criarClienteVagasHttp(apiBaseUrl)
  : clienteVagasDemo;
const clienteVagasHttp = apiBaseUrl
  ? criarClienteVagasResiliente(clienteVagasBase, clienteVagasDemo)
  : clienteVagasDemo;

const clienteDecisoesDemo = criarClienteDecisoesDemonstracao();
const clienteAcessoDemo = criarClienteAcessoDemonstracao();
const clienteAcessoBase = apiBaseUrl
  ? criarClienteAcessoEstudante(apiBaseUrl)
  : clienteAcessoDemo;
const clienteAcessoHttp = apiBaseUrl
  ? criarClienteAcessoResiliente(clienteAcessoBase, clienteAcessoDemo)
  : clienteAcessoDemo;

const clienteDadosPessoaisBase = apiBaseUrl
  ? criarClienteDadosPessoaisHttp(apiBaseUrl)
  : undefined;
const clienteDadosPessoaisHttp = clienteDadosPessoaisBase
  ? criarClienteDadosPessoaisResiliente(clienteDadosPessoaisBase)
  : undefined;

const clienteFormacaoAcademicaBase = apiBaseUrl
  ? criarClienteFormacaoAcademicaHttp(apiBaseUrl)
  : undefined;
const clienteFormacaoAcademicaHttp = clienteFormacaoAcademicaBase
  ? criarClienteFormacaoAcademicaResiliente(clienteFormacaoAcademicaBase)
  : undefined;

const clienteExperienciasHttp = apiBaseUrl
  ? criarClienteExperienciasHttp(apiBaseUrl)
  : undefined;

const clienteCompetenciasHttp = apiBaseUrl
  ? criarClienteCompetenciasHttp(apiBaseUrl)
  : undefined;
const clienteProjetosAcademicosHttp = apiBaseUrl
  ? criarClienteProjetosAcademicosHttp(apiBaseUrl)
  : undefined;

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
    const rawLocal = localStorage.getItem(CHAVE_RASCUNHO_CURRICULO);
    if (rawLocal) {
      return JSON.parse(rawLocal) as RascunhoCurriculo;
    }
  } catch {
    // Continua para fallback em sessionStorage caso localStorage esteja inacessível
  }
  try {
    const rawSession = sessionStorage.getItem(CHAVE_RASCUNHO_CURRICULO);
    if (rawSession) {
      return JSON.parse(rawSession) as RascunhoCurriculo;
    }
  } catch {
    // Ignora erro
  }
  return null;
}

function salvarRascunho(rascunho: RascunhoCurriculo): void {
  if (typeof window === "undefined") return;
  const serializado = JSON.stringify(rascunho);
  try {
    localStorage.setItem(CHAVE_RASCUNHO_CURRICULO, serializado);
  } catch {
    // Ignora restrições de localStorage
  }
  try {
    sessionStorage.setItem(CHAVE_RASCUNHO_CURRICULO, serializado);
  } catch {
    // Ignora restrições de sessionStorage
  }
}

function limparRascunho(): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.removeItem(CHAVE_RASCUNHO_CURRICULO);
  } catch {
    // Ignora restrições
  }
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

  // Cada conta mantém somente suas confirmações durante esta instância do App.
  // Recriar os clientes na troca de identidade evita suprimir POSTs de outra pessoa.
  const identidadeCadastro = usuarioLogado?.email;
  const envioCadastro = useRef<AbortController | null>(null);
  useEffect(() => {
    return () => {
      envioCadastro.current?.abort();
    };
  }, [identidadeCadastro]);

  /** Invalida I/O da etapa anterior para não restaurar dados após saída, troca de conta ou logout. */
  function cancelarCadastro(): void {
    envioCadastro.current?.abort();
    envioCadastro.current = null;
  }

  /** Cria uma tentativa cancelável e substitui a anterior para impedir continuidade de lotes obsoletos. */
  function iniciarCadastro(): AbortController {
    cancelarCadastro();
    const controle = new AbortController();
    envioCadastro.current = controle;
    return controle;
  }
  const clientesCadastro = useMemo(() => {
    return {
      identidade: identidadeCadastro,
      cursos: apiBaseUrl ? criarClienteCursosHttp(apiBaseUrl) : undefined,
      certificacoes: apiBaseUrl
        ? criarClienteCertificacoesHttp(apiBaseUrl)
        : undefined,
      idiomas: apiBaseUrl ? criarClienteIdiomasHttp(apiBaseUrl) : undefined,
    };
  }, [identidadeCadastro]);

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
    cancelarCadastro();
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
    cancelarCadastro();
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
    setModelo(undefined);
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
  const [modelo, setModelo] = useState<ModeloApresentacaoCurriculo | undefined>(
    () => carregarRascunho()?.modelo,
  );
  const modeloAtivo: ModeloApresentacaoCurriculo = modelo ?? "classico";
  const [origemSelecaoModelo, setOrigemSelecaoModelo] = useState<
    "wizard" | "visualizacao"
  >("wizard");
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
    cancelarCadastro();
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
      envioCadastro.current?.abort();
      envioCadastro.current = null;
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
        cliente={clienteDadosPessoaisHttp}
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
        cliente={clienteFormacaoAcademicaHttp}
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
        onSalvar={async (listaExperiencias) => {
          setExperiencias(listaExperiencias);
          if (clienteExperienciasHttp) {
            try {
              await clienteExperienciasHttp.salvar(listaExperiencias);
            } catch {
              // Em caso de indisponibilidade, mantém os dados no estado e no rascunho
            }
          }
          navegar("cursos-certificacoes");
        }}
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
        onAvancar={async (cursosValidados, certificacoesValidadas) => {
          const controle = iniciarCadastro();
          try {
            await clientesCadastro.cursos?.salvar(
              cursosValidados,
              controle.signal,
            );
            if (controle.signal.aborted) return;
            await clientesCadastro.certificacoes?.salvar(
              certificacoesValidadas,
              controle.signal,
            );
            if (controle.signal.aborted) return;
            setCursos(cursosValidados);
            setCertificacoes(certificacoesValidadas);
            navegar("idiomas");
          } finally {
            if (envioCadastro.current === controle)
              envioCadastro.current = null;
          }
        }}
        onContinuarLocal={(cursosValidados, certificacoesValidadas) => {
          setCursos(cursosValidados);
          setCertificacoes(certificacoesValidadas);
          navegar("idiomas");
        }}
        onVoltar={() => navegar("experiencias-profissionais")}
        onVoltarInicio={voltarAoInicio}
      />
    );
  }

  if (rotaAtiva === "idiomas") {
    return (
      <PaginaIdiomas
        idiomasIniciais={idiomas}
        onAvancar={async (idiomasValidados) => {
          const controle = iniciarCadastro();
          try {
            await clientesCadastro.idiomas?.salvar(
              idiomasValidados,
              controle.signal,
            );
            if (controle.signal.aborted) return;
            setIdiomas(idiomasValidados);
            navegar("competencias");
          } finally {
            if (envioCadastro.current === controle)
              envioCadastro.current = null;
          }
        }}
        onContinuarLocal={(idiomasValidados) => {
          setIdiomas(idiomasValidados);
          navegar("competencias");
        }}
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
        onAvancar={async () => {
          if (clienteCompetenciasHttp && competencias) {
            try {
              await clienteCompetenciasHttp.salvar(competencias);
            } catch {
              // Preservado no rascunho
            }
          }
          navegar("projetos-academicos");
        }}
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
        onAvancar={async () => {
          if (clienteProjetosAcademicosHttp && projetos) {
            for (const p of projetos) {
              if (p.titulo.trim() || p.descricao.trim()) {
                try {
                  await clienteProjetosAcademicosHttp.cadastrar(p);
                } catch {
                  // Preservado no rascunho
                }
              }
            }
          }
          setOrigemSelecaoModelo("wizard");
          navegar("selecionar-modelo");
        }}
        onVoltar={() => navegar("competencias")}
        onVoltarInicio={voltarAoInicio}
        projetosIniciais={projetos}
      />
    );
  }

  if (rotaAtiva === "selecionar-modelo") {
    const veioDeVisualizacao = origemSelecaoModelo === "visualizacao";

    return (
      <PaginaSelecaoModeloCurriculo
        aoAlterarModeloInstantaneo={(novoModelo) => {
          setModelo(novoModelo);
        }}
        aoConfirmar={(novoModelo) => {
          setModelo(novoModelo);
          if (veioDeVisualizacao) {
            setOrigemSelecaoModelo("wizard");
            navegar("visualizar-curriculo");
          } else {
            navegar("validacao-curriculo");
          }
        }}
        modeloInicial={modelo}
        onVoltar={() => {
          if (veioDeVisualizacao) {
            setOrigemSelecaoModelo("wizard");
            navegar("visualizar-curriculo");
          } else {
            navegar("projetos-academicos");
          }
        }}
        onVoltarInicio={() => {
          setOrigemSelecaoModelo("wizard");
          voltarAoInicio();
        }}
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
          const previaCalculada = montarPreviaCurriculo({
            dadosPessoais,
            formacoes,
            experiencias,
            cursos,
            certificacoes,
            idiomas,
            competencias,
            projetos,
            modelo: modeloAtivo,
          });
          const nomeEstudante =
            dadosPessoais?.nomeCompleto?.trim() || "Estudante";
          void exportarElementoParaPdf({
            previa: previaCalculada,
            nomeArquivo: `Curriculo - ${nomeEstudante}`,
          });
        }}
        onExportarDocx={() => {
          const previaCalculada = montarPreviaCurriculo({
            dadosPessoais,
            formacoes,
            experiencias,
            cursos,
            certificacoes,
            idiomas,
            competencias,
            projetos,
            modelo: modeloAtivo,
          });
          const nomeEstudante =
            dadosPessoais?.nomeCompleto?.trim() || "Estudante";
          exportarPreviaParaDocx({
            previa: previaCalculada,
            nomeArquivo: `Curriculo - ${nomeEstudante}`,
          });
        }}
        onVisualizarPreview={() => navegar("visualizar-curriculo")}
        onVoltar={() => {
          setOrigemSelecaoModelo("wizard");
          navegar("selecionar-modelo");
        }}
        onVoltarInicio={voltarAoInicio}
      />
    );
  }

  if (rotaAtiva === "visualizar-curriculo") {
    const resultadoValidacao = validarCurriculo(dadosValidacao);
    const previaCalculada = montarPreviaCurriculo({
      dadosPessoais,
      formacoes,
      experiencias,
      cursos,
      certificacoes,
      idiomas,
      competencias,
      projetos,
      modelo: modeloAtivo,
    });

    return (
      <PaginaVisualizacaoCurriculo
        aoAlterarModelo={() => {
          setOrigemSelecaoModelo("visualizacao");
          navegar("selecionar-modelo");
        }}
        aoTrocarModelo={(novoModelo) => {
          setModelo(novoModelo);
        }}
        autoBaixar={autoBaixarPdf}
        modelo={modeloAtivo}
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
        podeExportar={resultadoValidacao.podeExportarPdf}
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
        cliente={clienteAcessoHttp}
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
        cliente={clienteVagasHttp}
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
