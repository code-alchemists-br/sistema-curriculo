import { useEffect, useState, type FormEvent, type ReactNode } from "react";

import {
  FalhaVersaoCurriculo,
  type ClienteVersoesCurriculo,
} from "../api/cliente-versoes-curriculo";
import {
  obterRotuloModeloVersao,
  OPCOES_MODELO_VERSAO,
  type EdicaoVersaoCurriculo,
  type ModeloVersaoCurriculo,
  type ResumoVersaoCurriculo,
} from "../model/versao-curriculo-perfil";
import "./PainelCurriculosPerfil.css";

/** Define as dependências e ações disponíveis no painel de versões. */
export interface PainelCurriculosPerfilProps {
  cliente: ClienteVersoesCurriculo;
  onCriarNovaVersao?: () => void;
  renderizarMiniatura: (modelo: ModeloVersaoCurriculo) => ReactNode;
}

/** Representa os estados de carregamento que o painel pode comunicar. */
type EstadoListaVersoes = "carregando" | "erro" | "sucesso";

/**
 * Exibe e permite alterar os metadados das versões já existentes do currículo.
 *
 * O painel lista título e modelo, mantendo a alteração restrita aos campos que
 * fazem sentido para esta tela. Ele existe para centralizar a manutenção de
 * versões no perfil, sem duplicar o fluxo que altera as informações que compõem
 * cada currículo.
 */
export function PainelCurriculosPerfil({
  cliente,
  onCriarNovaVersao,
  renderizarMiniatura,
}: PainelCurriculosPerfilProps) {
  const [estadoLista, setEstadoLista] =
    useState<EstadoListaVersoes>("carregando");
  const [versoes, setVersoes] = useState<ResumoVersaoCurriculo[]>([]);
  const [idEmEdicao, setIdEmEdicao] = useState<string | null>(null);
  const [edicao, setEdicao] = useState<EdicaoVersaoCurriculo | null>(null);
  const [salvando, setSalvando] = useState(false);
  const [mensagem, setMensagem] = useState<string | null>(null);

  useEffect(() => {
    let componenteAtivo = true;

    void cliente
      .listar()
      .then((versoesCarregadas) => {
        if (!componenteAtivo) return;
        setVersoes(versoesCarregadas);
        setEstadoLista("sucesso");
      })
      .catch(() => {
        if (!componenteAtivo) return;
        setEstadoLista("erro");
      });

    return () => {
      componenteAtivo = false;
    };
  }, [cliente]);

  /** Prepara uma versão para edição sem alterar a lista original antecipadamente. */
  function iniciarEdicao(versao: ResumoVersaoCurriculo): void {
    setIdEmEdicao(versao.id);
    setEdicao({
      tituloVersao: versao.tituloVersao,
      modelo: versao.modelo,
    });
    setMensagem(null);
  }

  /** Cancela a edição local sem descartar nenhuma versão já salva. */
  function cancelarEdicao(): void {
    setIdEmEdicao(null);
    setEdicao(null);
  }

  /** Atualiza um único valor do formulário controlado de edição. */
  function atualizarEdicao<Campo extends keyof EdicaoVersaoCurriculo>(
    campo: Campo,
    valor: EdicaoVersaoCurriculo[Campo],
  ): void {
    setEdicao((valoresAtuais) =>
      valoresAtuais === null
        ? valoresAtuais
        : { ...valoresAtuais, [campo]: valor },
    );
  }

  /**
   * Salva título e modelo da versão que está aberta para edição.
   *
   * A lista só é substituída depois da resposta do cliente. Assim, uma falha não
   * faz a pessoa perder a referência da versão que já estava exibida.
   */
  async function salvarEdicao(evento: FormEvent<HTMLFormElement>): Promise<void> {
    evento.preventDefault();

    if (idEmEdicao === null || edicao === null) return;

    const versaoOriginal = versoes.find((versao) => versao.id === idEmEdicao);

    if (versaoOriginal === undefined) {
      setMensagem("Esta versão não está mais disponível. Atualize a página e tente novamente.");
      return;
    }

    if (edicao.tituloVersao.trim() === "") {
      setMensagem("Informe um título para identificar esta versão.");
      return;
    }

    setSalvando(true);
    setMensagem(null);

    try {
      const versaoAtualizada = await cliente.atualizar(idEmEdicao, {
        ...edicao,
        tituloVersao: edicao.tituloVersao.trim(),
        visibilidade: versaoOriginal.visibilidade,
      });
      setVersoes((versoesAtuais) =>
        versoesAtuais.map((versao) =>
          versao.id === versaoAtualizada.id ? versaoAtualizada : versao,
        ),
      );
      setIdEmEdicao(null);
      setEdicao(null);
      setMensagem("Versão atualizada com sucesso.");
    } catch (erro: unknown) {
      setMensagem(obterMensagemFalha(erro));
    } finally {
      setSalvando(false);
    }
  }

  return (
    <section
      aria-labelledby="titulo-versoes-curriculo"
      className="painel-curriculos-perfil"
    >
      <header className="painel-curriculos-perfil__cabecalho">
        <div>
          <p className="painel-curriculos-perfil__sobretitulo">
            Currículos salvos
          </p>
          <h2 id="titulo-versoes-curriculo">Gerencie suas versões</h2>
          <p>
            Consulte as versões que você criou, identifique o modelo usado e
            altere o título ou o modelo quando precisar.
          </p>
        </div>
        {onCriarNovaVersao && (
          <button
            className="painel-curriculos-perfil__criar"
            onClick={onCriarNovaVersao}
            type="button"
          >
            Criar nova versão
          </button>
        )}
      </header>

      {mensagem !== null && (
        <p
          className="painel-curriculos-perfil__mensagem"
          role={mensagem.includes("sucesso") ? "status" : "alert"}
        >
          {mensagem}
        </p>
      )}

      {estadoLista === "carregando" && (
        <p className="painel-curriculos-perfil__estado" role="status">
          Carregando suas versões de currículo...
        </p>
      )}

      {estadoLista === "erro" && (
        <p className="painel-curriculos-perfil__estado" role="alert">
          Não foi possível carregar seus currículos agora. Tente novamente mais
          tarde.
        </p>
      )}

      {estadoLista === "sucesso" && versoes.length === 0 && (
        <div className="painel-curriculos-perfil__vazio">
          <h3>Nenhuma versão criada ainda</h3>
          <p>Quando você finalizar um currículo, ele aparecerá neste espaço.</p>
        </div>
      )}

      {estadoLista === "sucesso" && versoes.length > 0 && (
        <ul className="painel-curriculos-perfil__lista">
          {versoes.map((versao) => (
            <li className="painel-curriculos-perfil__item" key={versao.id}>
              {idEmEdicao === versao.id && edicao !== null ? (
                <form
                  aria-label={`Editar ${versao.tituloVersao}`}
                  className="painel-curriculos-perfil__formulario"
                  onSubmit={salvarEdicao}
                >
                  <CampoEdicao
                    id={`titulo-${versao.id}`}
                    label="Título da versão"
                    onChange={(valor) => atualizarEdicao("tituloVersao", valor)}
                    value={edicao.tituloVersao}
                  />
                  <div className="painel-curriculos-perfil__campo">
                    <label htmlFor={`modelo-${versao.id}`}>Modelo</label>
                    <select
                      id={`modelo-${versao.id}`}
                      onChange={(evento) =>
                        atualizarEdicao(
                          "modelo",
                          evento.target.value as ModeloVersaoCurriculo,
                        )
                      }
                      value={edicao.modelo}
                    >
                      {OPCOES_MODELO_VERSAO.map((opcao) => (
                        <option key={opcao.valor} value={opcao.valor}>
                          {opcao.rotulo}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="painel-curriculos-perfil__acoes-edicao">
                    <button disabled={salvando} type="submit">
                      {salvando ? "Salvando..." : "Salvar versão"}
                    </button>
                    <button
                      disabled={salvando}
                      onClick={cancelarEdicao}
                      type="button"
                    >
                      Cancelar
                    </button>
                  </div>
                </form>
              ) : (
                <CartaoVersao
                  onEditar={() => iniciarEdicao(versao)}
                  renderizarMiniatura={renderizarMiniatura}
                  versao={versao}
                />
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

/** Exibe os metadados de uma versão e uma miniatura estrutural do seu modelo. */
function CartaoVersao({
  onEditar,
  renderizarMiniatura,
  versao,
}: {
  onEditar: () => void;
  renderizarMiniatura: (modelo: ModeloVersaoCurriculo) => ReactNode;
  versao: ResumoVersaoCurriculo;
}) {
  const rotuloModelo = obterRotuloModeloVersao(versao.modelo);

  return (
    <article className="painel-curriculos-perfil__cartao">
      <div
        aria-label={`Prévia estrutural do modelo ${rotuloModelo}`}
        className="painel-curriculos-perfil__frame-modelo"
        role="img"
      >
        {renderizarMiniatura(versao.modelo)}
      </div>
      <div className="painel-curriculos-perfil__dados-versao">
        <p className="painel-curriculos-perfil__modelo">Modelo: {rotuloModelo}</p>
        <h3>{versao.tituloVersao}</h3>
        <button
          aria-label={`Editar versão ${versao.tituloVersao}`}
          className="painel-curriculos-perfil__editar"
          onClick={onEditar}
          type="button"
        >
          Editar versão
        </button>
      </div>
    </article>
  );
}

/** Renderiza um campo simples do formulário de edição de versão. */
function CampoEdicao({
  id,
  label,
  onChange,
  value,
}: {
  id: string;
  label: string;
  onChange: (valor: string) => void;
  value: string;
}) {
  return (
    <div className="painel-curriculos-perfil__campo">
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        onChange={(evento) => onChange(evento.target.value)}
        required
        type="text"
        value={value}
      />
    </div>
  );
}

/** Traduz as falhas do cliente sem expor detalhes de implementação. */
function obterMensagemFalha(erro: unknown): string {
  if (erro instanceof FalhaVersaoCurriculo && erro.codigo === "nao-encontrado") {
    return "Esta versão não está mais disponível. Atualize a página e tente novamente.";
  }

  return "Não foi possível salvar esta versão no momento. Tente novamente mais tarde.";
}
