import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type CSSProperties,
  type ReactElement,
} from "react";

import type { ModeloApresentacaoCurriculo } from "../features/alternar-modelo-curriculo";
import {
  FalhaFormacaoAcademica,
  type ClienteFormacaoAcademica,
  type ValoresFormacaoAcademica,
} from "../features/cadastrar-formacao-academica";
import type { ValoresCertificacao } from "../features/cadastro-certificacoes";
import type { ValoresProjetoAcademico } from "../features/cadastro-projeto-academico";
import type { Curso } from "../features/edit-courses";
import type { Idioma } from "../features/edit-languages";
import type { ValoresDadosPessoais } from "../features/edit-personal-data";
import type { Experiencia } from "../features/edit-professional-experience";
import type { Habilidades } from "../features/edit-skills";
import type { Student } from "../entities/student";
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
import { PaginaMeuPerfil } from "../pages/meu-perfil";
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
  exportarElementoParaPdf,
  exportarPreviaParaDocx,
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
import {
  FalhaPerfilEstudante,
  type ClientePerfilEstudante,
} from "../features/edit-profile";
import { criarClienteVersoesCurriculoDemonstracao } from "../features/gerenciar-curriculos-perfil";
import { criarClienteVagasResiliente } from "./servicos-resilientes";
import {
  criarClienteCurriculoNoBanco,
  FalhaCurriculoNoBanco,
  type CurriculoDasTelas,
} from "./curriculo-no-banco";
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
// Sem "modo demonstração" quando a API cai: o estudante precisa saber que não
// entrou de verdade, senão nada do que preencher será salvo.
const clienteAcessoHttp = clienteAcessoBase;

// Dados pessoais vão direto para PUT /estudantes/me/perfil (substitui, não duplica).
const clienteDadosPessoaisHttp = apiBaseUrl
  ? criarClienteDadosPessoaisHttp(apiBaseUrl)
  : undefined;

// As demais seções são lidas e substituídas inteiras por /estudantes/me/curriculo.
const clienteCurriculo = apiBaseUrl
  ? criarClienteCurriculoNoBanco(apiBaseUrl)
  : undefined;

/** Estilo do aviso de falha ao salvar, fixo no rodapé da tela. */
const ESTILO_AVISO_FALHA: CSSProperties = {
  position: "fixed",
  left: "50%",
  bottom: "1.5rem",
  transform: "translateX(-50%)",
  zIndex: 1000,
  display: "flex",
  alignItems: "center",
  gap: "1rem",
  width: "min(calc(100% - 2rem), 40rem)",
  padding: "0.9rem 1.1rem",
  border: "1px solid rgba(239, 68, 68, 0.45)",
  borderRadius: "0.75rem",
  background: "#2a0f0f",
  color: "#fecaca",
  fontFamily: "Poppins, sans-serif",
  boxShadow: "0 1rem 2.5rem rgb(0 0 0 / 45%)",
};

const clienteVersoesCurriculoDemo = criarClienteVersoesCurriculoDemonstracao();

/**
 * Mantém o salvamento do perfil na sessão enquanto não há identidade autenticada
 * suficiente para acionar o endpoint real de perfil.
 *
 * A atualização é confirmada pela própria composição do App após o formulário
 * validar os dados. A exclusão continua indisponível para não simular uma ação
 * irreversível que não pode ser persistida nesta camada.
 */
const clientePerfilDaSessao: ClientePerfilEstudante = {
  async atualizar() {
    return undefined;
  },
  async excluir() {
    throw new FalhaPerfilEstudante("indisponivel");
  },
};

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
  | "meu-perfil"
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
      if (etapa === "configuracoes-perfil") return "configuracoes-perfil";
      if (etapa === "meu-perfil" || etapa === "perfil") return "meu-perfil";
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

  // Envio em andamento de uma etapa; é cancelado ao navegar, sair ou trocar de conta.
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

  /**
   * Abre uma nova tentativa de envio cancelável, cancelando a anterior.
   *
   * O sinal devolvido acompanha a requisição; navegar, sair ou trocar de conta
   * o cancela, e quem chamou não deve avançar depois disso. Existe para que
   * uma resposta atrasada não mude de tela nem restaure dados de outra sessão.
   */
  function iniciarCadastro(): AbortController {
    cancelarCadastro();
    const controle = new AbortController();
    envioCadastro.current = controle;
    return controle;
  }

  /**
   * Salva uma etapa no banco e só avança se o envio não foi cancelado.
   *
   * Cria a tentativa cancelável, espera a gravação e verifica o sinal antes de
   * navegar; falhas sobem para quem chamou (a página mostra o erro). Existe
   * para as etapas cujas páginas exibem o próprio erro de gravação.
   */
  async function salvarComCancelamento(
    salvar: (signal: AbortSignal) => Promise<void> | undefined,
    destino: RotaAtiva,
  ): Promise<void> {
    const controle = iniciarCadastro();
    try {
      await salvar(controle.signal);
      if (!controle.signal.aborted) navegar(destino);
    } finally {
      if (envioCadastro.current === controle) envioCadastro.current = null;
    }
  }

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
    setCurriculoCarregadoDe(null);
    setCurriculoPronto(false);
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
  // E-mail cujo currículo já veio do banco; enquanto for outro, está carregando.
  const [curriculoCarregadoDe, setCurriculoCarregadoDe] = useState<
    string | null
  >(null);
  const carregandoCurriculo = Boolean(
    usuarioLogado &&
    clienteCurriculo &&
    curriculoCarregadoDe !== usuarioLogado.email,
  );
  const [erroSalvamento, setErroSalvamento] = useState<string | null>(null);
  // Currículo pronto = o estudante chegou a escolher e salvar o modelo.
  const [curriculoPronto, setCurriculoPronto] = useState(false);
  const [salvando, setSalvando] = useState(false);
  // Valores mais recentes de cada seção. Algumas etapas chamam "salvar" e
  // "avançar" no mesmo clique, antes de o estado do React atualizar; por isso
  // o salvamento lê daqui, e não do estado capturado no render anterior.
  const ultimos = useRef({
    formacoes,
    experiencias,
    cursos,
    certificacoes,
    idiomas,
    competencias,
    projetos,
  });
  useEffect(() => {
    ultimos.current = {
      formacoes,
      experiencias,
      cursos,
      certificacoes,
      idiomas,
      competencias,
      projetos,
    };
  });

  // Callbacks estáveis: os formulários os usam em efeitos, e uma função nova a
  // cada render faria o efeito rodar sem parar. Também atualizam `ultimos`
  // na hora, para o salvamento disparado no mesmo clique ler a lista nova.
  const alterarFormacoes = useCallback((lista: ValoresFormacaoAcademica[]) => {
    ultimos.current.formacoes = lista;
    setFormacoes(lista);
  }, []);
  const alterarCompetencias = useCallback((habilidades: Habilidades) => {
    ultimos.current.competencias = habilidades;
    setCompetencias(habilidades);
  }, []);
  const alterarProjetos = useCallback((lista: ValoresProjetoAcademico[]) => {
    ultimos.current.projetos = lista;
    setProjetos(lista);
  }, []);

  /**
   * Troca o estado das telas pelo currículo lido do banco.
   *
   * Seções vazias viram `undefined` para os formulários abrirem com seus
   * valores iniciais; também marca se o currículo está pronto e usa o nome
   * salvo no cabeçalho. Existe para o banco ser a fonte do que a tela mostra.
   */
  function aplicarCurriculo(c: CurriculoDasTelas): void {
    const ouNada = <T,>(lista: T[]) => (lista.length > 0 ? lista : undefined);
    setDadosPessoais(c.dadosPessoais);
    setFormacoes(ouNada(c.formacoes));
    setExperiencias(ouNada(c.experiencias));
    setCursos(ouNada(c.cursos));
    setCertificacoes(ouNada(c.certificacoes));
    setIdiomas(ouNada(c.idiomas));
    setProjetos(ouNada(c.projetos));
    setCompetencias(
      c.competencias.hardSkills.length || c.competencias.softSkills.length
        ? c.competencias
        : undefined,
    );
    if (c.modelo) setModelo(c.modelo);
    setCurriculoPronto(c.modelo !== null);
    // O login só devolve o e-mail; o nome de verdade vem do banco.
    const nome = c.dadosPessoais.nomeCompleto.trim();
    if (nome) {
      setUsuarioLogado((atual) => {
        if (!atual || atual.nome === nome) return atual;
        const atualizado = { ...atual, nome };
        try {
          sessionStorage.setItem(
            "liminal_usuario_sessao",
            JSON.stringify(atualizado),
          );
        } catch {
          // Ignora erro em ambientes sem suporte a sessionStorage
        }
        return atualizado;
      });
    }
  }

  /**
   * Esquece o estudante deste navegador quando a sessão acaba.
   *
   * Limpa o usuário do estado e do `sessionStorage`. Existe para que uma
   * sessão expirada (401) leve o estudante a entrar de novo.
   */
  function esquecerUsuario(): void {
    setUsuarioLogado(null);
    try {
      sessionStorage.removeItem("liminal_usuario_sessao");
    } catch {
      // Ignora erro em ambientes sem suporte a sessionStorage
    }
  }

  // Ao abrir a aplicação logado, ou logo após o login, o currículo vem do banco:
  // ele é a fonte de verdade, e o rascunho do navegador só guarda o que está
  // sendo digitado. Sessão expirada (401) faz o estudante entrar de novo.
  useEffect(() => {
    if (!usuarioLogado || !clienteCurriculo) return;
    let ativo = true;
    const email = usuarioLogado.email;
    clienteCurriculo
      .carregar()
      .then((curriculo) => {
        if (ativo) aplicarCurriculo(curriculo);
      })
      .catch((erro: unknown) => {
        if (!ativo) return;
        if (erro instanceof FalhaCurriculoNoBanco && erro.status === 401) {
          esquecerUsuario();
        } else {
          setErroSalvamento(
            "Não foi possível carregar seu currículo do servidor. Os dados mostrados podem estar desatualizados.",
          );
        }
      })
      .finally(() => {
        if (ativo) setCurriculoCarregadoDe(email);
      });
    return () => {
      ativo = false;
    };
    // Recarrega só quando muda quem está logado.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [usuarioLogado?.email]);

  /**
   * Salva uma etapa no banco e só então avança.
   *
   * Se a gravação falhar, o estudante continua na etapa, com os dados
   * digitados, e vê o motivo no aviso do rodapé. Sem API configurada, só avança.
   */
  async function salvarEAvancar(
    salvar: (signal: AbortSignal) => Promise<void>,
    destino: RotaAtiva,
  ): Promise<void> {
    if (!clienteCurriculo) {
      navegar(destino);
      return;
    }
    const controle = iniciarCadastro();
    setSalvando(true);
    setErroSalvamento(null);
    try {
      await salvar(controle.signal);
      if (!controle.signal.aborted) navegar(destino);
    } catch (erro: unknown) {
      if (controle.signal.aborted) return;
      if (erro instanceof FalhaCurriculoNoBanco && erro.status === 401) {
        esquecerUsuario();
      }
      setErroSalvamento(
        erro instanceof Error ? erro.message : "Não foi possível salvar agora.",
      );
    } finally {
      if (envioCadastro.current === controle) envioCadastro.current = null;
      setSalvando(false);
    }
  }

  // A etapa de formação chama `cadastrar` uma vez por formação; cada chamada
  // substitui a lista inteira, então repetir não duplica nada.
  const clienteFormacaoAcademicaHttp: ClienteFormacaoAcademica | undefined =
    clienteCurriculo
      ? {
          async cadastrar() {
            try {
              await clienteCurriculo.salvarFormacoes(
                ultimos.current.formacoes ?? [],
              );
            } catch (erro: unknown) {
              const status =
                erro instanceof FalhaCurriculoNoBanco ? erro.status : null;
              throw new FalhaFormacaoAcademica(
                status === null
                  ? "rede"
                  : status === 401 || status >= 500
                    ? "indisponivel"
                    : "resposta-invalida",
              );
            }
          },
        }
      : undefined;

  /**
   * Mostra a página com o aviso de gravação no rodapé, quando houver.
   *
   * Exibe "Salvando no servidor..." durante a gravação e, em falha, o motivo
   * com um botão para fechar. Existe para as etapas cujas páginas não mostram
   * o erro de gravação sozinhas.
   */
  function comAviso(pagina: ReactElement): ReactElement {
    return (
      <>
        {pagina}
        {salvando && (
          <div
            role="status"
            style={{
              ...ESTILO_AVISO_FALHA,
              background: "#1a1a1a",
              color: "#f3f3f3",
              border: "1px solid rgb(255 255 255 / 15%)",
            }}
          >
            Salvando no servidor...
          </div>
        )}
        {erroSalvamento && !salvando && (
          <div role="alert" style={ESTILO_AVISO_FALHA}>
            <span style={{ flex: 1 }}>{erroSalvamento}</span>
            <button
              onClick={() => setErroSalvamento(null)}
              style={{
                background: "none",
                border: "1px solid currentColor",
                borderRadius: "0.5rem",
                color: "inherit",
                cursor: "pointer",
                padding: "0.35rem 0.75rem",
                font: "inherit",
              }}
              type="button"
            >
              Fechar
            </button>
          </div>
        )}
      </>
    );
  }

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
   * Atualiza os dados de perfil preservados na sessão de criação do currículo.
   *
   * A função recebe uma entidade já validada pelo formulário, converte os links
   * opcionais para os campos controlados da etapa inicial e mantém o cabeçalho
   * autenticado coerente com nome e e-mail que acabaram de ser salvos.
   */
  function sincronizarPerfilAtualizado(perfil: Student): void {
    setDadosPessoais({
      nomeCompleto: perfil.nomeCompleto,
      enderecoCompleto: perfil.enderecoCompleto,
      telefones: [...perfil.telefones],
      email: perfil.email,
      linkedIn: perfil.linkedIn ?? "",
      curriculoLattes: perfil.curriculoLattes ?? "",
    });

    if (usuarioLogado !== null) {
      const usuarioAtualizado: UsuarioAutenticado = {
        nome: perfil.nomeCompleto,
        email: perfil.email,
      };
      setUsuarioLogado(usuarioAtualizado);

      if (typeof window !== "undefined") {
        try {
          sessionStorage.setItem(
            "liminal_usuario_sessao",
            JSON.stringify(usuarioAtualizado),
          );
        } catch {
          // Ignora erro em ambientes sem suporte a sessionStorage.
        }
      }
    }
  }

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
    setErroSalvamento(null);
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

  // Enquanto o currículo chega do banco, as etapas esperam: os formulários
  // leem os valores iniciais só ao abrir e mostrariam dados antigos.
  const rotasComCurriculo: RotaAtiva[] = [
    "dados-pessoais",
    "formacao-academica",
    "experiencias-profissionais",
    "cursos-certificacoes",
    "cursos-idiomas",
    "idiomas",
    "competencias",
    "projetos-academicos",
    "selecionar-modelo",
    "validacao-curriculo",
    "visualizar-curriculo",
    "meu-perfil",
  ];
  if (carregandoCurriculo && rotasComCurriculo.includes(rotaAtiva)) {
    return (
      <main
        aria-busy="true"
        style={{
          minHeight: "100vh",
          display: "grid",
          placeItems: "center",
          background: "#050505",
          color: "#a3a3a3",
          fontFamily: "Poppins, sans-serif",
        }}
      >
        Carregando seu currículo...
      </main>
    );
  }

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
        aoAlterarFormacoes={alterarFormacoes}
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
          // Falha aqui sobe para o formulário, que mostra o motivo e não avança.
          await salvarComCancelamento(
            (signal) =>
              clienteCurriculo?.salvarExperiencias(listaExperiencias, signal),
            "cursos-certificacoes",
          );
        }}
        onVoltar={() => navegar("formacao-academica")}
        onVoltarInicio={voltarAoInicio}
      />
    );
  }

  if (rotaAtiva === "cursos-certificacoes" || rotaAtiva === "cursos-idiomas") {
    return comAviso(
      <PaginaCursosCertificacoes
        aoAlterarCertificacoes={setCertificacoes}
        aoAlterarCursos={setCursos}
        certificacoesIniciais={certificacoes}
        cursosIniciais={cursos}
        onAvancar={async (cursosValidados, certificacoesValidadas) => {
          // Substitui as seções inteiras no banco (sem duplicar). Se falhar,
          // a página mostra o erro e não avança.
          setCursos(cursosValidados);
          setCertificacoes(certificacoesValidadas);
          await salvarComCancelamento(async (signal) => {
            await clienteCurriculo?.salvarCursos(cursosValidados, signal);
            if (signal.aborted) return;
            await clienteCurriculo?.salvarCertificacoes(
              certificacoesValidadas,
              signal,
            );
          }, "idiomas");
        }}
        onVoltar={() => navegar("experiencias-profissionais")}
        onVoltarInicio={voltarAoInicio}
      />,
    );
  }

  if (rotaAtiva === "idiomas") {
    return comAviso(
      <PaginaIdiomas
        idiomasIniciais={idiomas}
        onAvancar={async (idiomasValidados) => {
          // Substitui a seção inteira no banco; falhas aparecem na página.
          setIdiomas(idiomasValidados);
          await salvarComCancelamento(
            (signal) =>
              clienteCurriculo?.salvarIdiomas(idiomasValidados, signal),
            "competencias",
          );
        }}
        onSalvar={setIdiomas}
        onVoltar={() => navegar("cursos-certificacoes")}
        onVoltarInicio={voltarAoInicio}
      />,
    );
  }

  if (rotaAtiva === "competencias") {
    return comAviso(
      <PaginaCompetencias
        competenciasIniciais={competencias}
        onAvancar={() =>
          void salvarEAvancar(
            (signal) =>
              clienteCurriculo!.salvarCompetencias(
                ultimos.current.competencias ?? {
                  hardSkills: [],
                  softSkills: [],
                },
                signal,
              ),
            "projetos-academicos",
          )
        }
        onSalvar={alterarCompetencias}
        onVoltar={() => navegar("idiomas")}
        onVoltarInicio={voltarAoInicio}
      />,
    );
  }

  if (rotaAtiva === "projetos-academicos") {
    return comAviso(
      <PaginaCadastroProjetosAcademicos
        aoAlterarProjetos={alterarProjetos}
        onAvancar={() => {
          setOrigemSelecaoModelo("wizard");
          void salvarEAvancar(
            (signal) =>
              clienteCurriculo!.salvarProjetos(
                ultimos.current.projetos ?? [],
                signal,
              ),
            "selecionar-modelo",
          );
        }}
        onVoltar={() => navegar("competencias")}
        onVoltarInicio={voltarAoInicio}
        projetosIniciais={projetos}
      />,
    );
  }

  if (rotaAtiva === "selecionar-modelo") {
    const veioDeVisualizacao = origemSelecaoModelo === "visualizacao";

    return comAviso(
      <PaginaSelecaoModeloCurriculo
        aoAlterarModeloInstantaneo={(novoModelo) => {
          setModelo(novoModelo);
        }}
        aoConfirmar={(novoModelo) => {
          setModelo(novoModelo);
          if (veioDeVisualizacao) setOrigemSelecaoModelo("wizard");
          void salvarEAvancar(
            async (signal) => {
              await clienteCurriculo!.salvarModelo(novoModelo, signal);
              if (!signal.aborted) setCurriculoPronto(true);
            },
            veioDeVisualizacao ? "visualizar-curriculo" : "validacao-curriculo",
          );
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
          idiomas,
          cursos,
          certificacoes,
        }}
      />,
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

    return comAviso(
      <PaginaVisualizacaoCurriculo
        aoAlterarModelo={() => {
          setOrigemSelecaoModelo("visualizacao");
          navegar("selecionar-modelo");
        }}
        aoTrocarModelo={(novoModelo) => {
          setModelo(novoModelo);
          // Grava a troca no banco; se falhar, o aviso do rodapé mostra o motivo.
          void salvarEAvancar(
            (signal) => clienteCurriculo!.salvarModelo(novoModelo, signal),
            "visualizar-curriculo",
          );
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
      />,
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
    return (
      <PaginaConfiguracoesPerfil
        cliente={clientePerfilDaSessao}
        clienteCurriculos={clienteVersoesCurriculoDemo}
        onCriarNovaVersao={() => navegar("dados-pessoais")}
        onPerfilAtualizado={sincronizarPerfilAtualizado}
        onVoltar={() => navegar("meu-perfil")}
        valoresIniciais={{
          nomeCompleto:
            dadosPessoais?.nomeCompleto || usuarioLogado?.nome || "Estudante",
          enderecoCompleto: dadosPessoais?.enderecoCompleto || "",
          telefones: dadosPessoais?.telefones || [""],
          email: dadosPessoais?.email || usuarioLogado?.email || "",
          linkedIn: dadosPessoais?.linkedIn || "",
          curriculoLattes: dadosPessoais?.curriculoLattes || "",
        }}
      />
    );
  }

  if (rotaAtiva === "meu-perfil") {
    const possuiCurriculo = Boolean(
      (formacoes && formacoes.length > 0) ||
      (experiencias && experiencias.length > 0) ||
      (projetos && projetos.length > 0) ||
      (cursos && cursos.length > 0) ||
      (idiomas && idiomas.length > 0) ||
      competencias?.hardSkills?.length ||
      competencias?.softSkills?.length,
    );
    const dadosDoPerfil = {
      ...dadosPessoais,
      nomeCompleto:
        dadosPessoais?.nomeCompleto || usuarioLogado?.nome || "Estudante",
      email: dadosPessoais?.email || usuarioLogado?.email || "",
    } as ValoresDadosPessoais;
    const previaDoPerfil = montarPreviaCurriculo({
      dadosPessoais: dadosDoPerfil,
      formacoes,
      experiencias,
      cursos,
      certificacoes,
      idiomas,
      competencias,
      projetos,
      modelo: modeloAtivo,
    });
    const nomeArquivo = `Curriculo - ${dadosDoPerfil.nomeCompleto}`;

    return (
      <PaginaMeuPerfil
        modelo={modeloAtivo}
        onEditarCurriculo={() =>
          navegar(possuiCurriculo ? "validacao-curriculo" : "dados-pessoais")
        }
        onEditarPerfil={() => navegar("configuracoes-perfil")}
        aoBaixarCurriculo={(formato) =>
          formato === "pdf"
            ? exportarElementoParaPdf({ previa: previaDoPerfil, nomeArquivo })
            : exportarPreviaParaDocx({ previa: previaDoPerfil, nomeArquivo })
        }
        onVoltarInicio={voltarAoInicio}
        possuiCurriculo={possuiCurriculo}
        previa={previaDoPerfil}
      />
    );
  }

  return (
    <PaginaInicio
      onCriarCurriculo={aoClicarCriarCurriculo}
      onNavegarCadastro={() => abrirAcesso("cadastro", "criar-conta")}
      onNavegarLogin={() => abrirAcesso("acesso", "login")}
      onNavegarInicio={voltarAoInicio}
      onNavegarVagas={() => navegar("vagas")}
      onNavegarPerfil={() =>
        usuarioLogado ? navegar("meu-perfil") : abrirAcesso("acesso", "login")
      }
      onNavegarPoliticaDePrivacidade={() =>
        abrirDocumentoPublico("politica-de-privacidade")
      }
      onNavegarTermosDeUso={() => abrirDocumentoPublico("termos-de-uso")}
      usuarioLogado={usuarioLogado}
      temCurriculoPronto={curriculoPronto}
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
