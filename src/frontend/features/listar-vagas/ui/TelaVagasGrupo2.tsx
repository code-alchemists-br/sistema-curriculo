import { useCallback, useEffect, useState, type FormEvent } from "react";

import type { SugestaoVaga } from "../../../entities/vaga";
import {
  criarClienteDecisoesRecomendacaoIndisponivel,
  type ClienteDecisoesRecomendacao,
  type DecisaoRecomendacao,
} from "../api/cliente-decisoes-recomendacao";
import type {
  ClienteVagasGrupo2,
  CriteriosPesquisaVagas,
} from "../api/cliente-vagas-grupo2";
import { obterMensagemErroVagas } from "../model/mensagem-erro-vagas";
import "./TelaVagasGrupo2.css";

/** Define as dependências remotas recebidas pela tela de vagas. */
export interface TelaVagasGrupo2Props {
  cliente: ClienteVagasGrupo2;
  clienteDecisoes?: ClienteDecisoesRecomendacao;
}

type EstadoVagasGrupo2 =
  | { tipo: "carregando" }
  | { tipo: "resultado"; sugestoes: SugestaoVaga[] }
  | { tipo: "vazio"; criterios: CriteriosPesquisaVagas }
  | { tipo: "erro"; mensagem: string; criterios: CriteriosPesquisaVagas };

type EstadoDecisao =
  | { tipo: "ocioso" }
  | { tipo: "salvando"; decisao: DecisaoRecomendacao }
  | { tipo: "salva"; decisao: DecisaoRecomendacao }
  | { tipo: "erro"; decisao: DecisaoRecomendacao };

const clienteDecisoesPadrao = criarClienteDecisoesRecomendacaoIndisponivel();

/**
 * Lista sugestões de vagas e registra decisões explícitas do estudante.
 *
 * A tela conserva o termo digitado no estado local, repassa-o ao cliente a
 * cada busca e renderiza um estado vazio sem apagar o formulário. As decisões
 * são anunciadas apenas após a Promise do cliente resolver, para não comunicar
 * um salvamento que não ocorreu.
 */
export function TelaVagasGrupo2({
  cliente,
  clienteDecisoes = clienteDecisoesPadrao,
}: TelaVagasGrupo2Props) {
  const [termo, setTermo] = useState("");
  const [estado, setEstado] = useState<EstadoVagasGrupo2>({
    tipo: "carregando",
  });
  const [decisoes, setDecisoes] = useState<Record<string, EstadoDecisao>>({});

  const pesquisar = useCallback(
    async (criterios: CriteriosPesquisaVagas): Promise<EstadoVagasGrupo2> => {
      try {
        const sugestoes = await cliente.listarSugestoes(criterios);

        return sugestoes.length === 0
          ? { tipo: "vazio", criterios }
          : { tipo: "resultado", sugestoes };
      } catch (erro: unknown) {
        return {
          tipo: "erro",
          mensagem: obterMensagemErroVagas(erro),
          criterios,
        };
      }
    },
    [cliente],
  );

  const executarPesquisa = useCallback(
    (criterios: CriteriosPesquisaVagas): void => {
      setEstado({ tipo: "carregando" });
      void pesquisar(criterios).then(setEstado);
    },
    [pesquisar],
  );

  useEffect(() => {
    let componenteAtivo = true;

    void pesquisar({ termo: "" }).then((novoEstado) => {
      if (componenteAtivo) {
        setEstado(novoEstado);
      }
    });

    return () => {
      componenteAtivo = false;
    };
  }, [pesquisar]);

  function enviarPesquisa(evento: FormEvent<HTMLFormElement>): void {
    evento.preventDefault();
    executarPesquisa({ termo: termo.trim() });
  }

  function tentarNovamente(): void {
    const criterios =
      estado.tipo === "vazio" || estado.tipo === "erro"
        ? estado.criterios
        : { termo: termo.trim() };
    executarPesquisa(criterios);
  }

  async function salvarDecisao(
    sugestao: SugestaoVaga,
    decisao: DecisaoRecomendacao,
  ): Promise<void> {
    const chave = chaveDaSugestao(sugestao);

    setDecisoes((atuais) => ({
      ...atuais,
      [chave]: { tipo: "salvando", decisao },
    }));

    try {
      await clienteDecisoes.salvarDecisao({
        curriculoId: sugestao.curriculoId,
        vagaId: sugestao.vaga.id,
        decisao,
      });

      setDecisoes((atuais) => ({
        ...atuais,
        [chave]: { tipo: "salva", decisao },
      }));
    } catch {
      setDecisoes((atuais) => ({
        ...atuais,
        [chave]: { tipo: "erro", decisao },
      }));
    }
  }

  return (
    <section aria-labelledby="titulo-vagas-grupo2" className="vagas-grupo2">
      <div>
        <p className="eyebrow">Vagas sugeridas</p>
        <h1 id="titulo-vagas-grupo2">Oportunidades para o seu currículo</h1>
        <p>Estas vagas foram sugeridas pela integração com o Grupo 2.</p>
      </div>

      <form className="vagas-grupo2__pesquisa" onSubmit={enviarPesquisa}>
        <label htmlFor="termo-pesquisa-vagas">Palavra-chave</label>

        <input
          id="termo-pesquisa-vagas"
          onChange={(evento) => setTermo(evento.target.value)}
          type="search"
          value={termo}
        />

        <button type="submit">Pesquisar vagas</button>
      </form>

      {renderizarEstado(estado, tentarNovamente, decisoes, salvarDecisao)}
    </section>
  );
}

/** Renderiza o estado de consulta sem remover o formulário de pesquisa. */
function renderizarEstado(
  estado: EstadoVagasGrupo2,
  aoTentarNovamente: () => void,
  decisoes: Record<string, EstadoDecisao>,
  aoSalvarDecisao: (
    sugestao: SugestaoVaga,
    decisao: DecisaoRecomendacao,
  ) => Promise<void>,
) {
  if (estado.tipo === "carregando") {
    return <p role="status">Carregando vagas sugeridas...</p>;
  }

  if (estado.tipo === "vazio") {
    const complemento = estado.criterios.termo
      ? ` para “${estado.criterios.termo}”`
      : "";

    return (
      // Proveniência: decision-analysis prompts/frontend/20261019-073800-vagas-leitor-tela-teclado-v001.md#v001
      <section
        aria-labelledby="titulo-vagas-vazias"
        className="vagas-grupo2__estado"
        role="status"
      >
        <h2 id="titulo-vagas-vazias">Nenhuma vaga encontrada</h2>
        <p>Não encontramos vagas sugeridas{complemento}.</p>
        <p>Você pode ajustar a palavra-chave e pesquisar novamente.</p>
      </section>
    );
  }

  if (estado.tipo === "erro") {
    return (
      <section
        aria-labelledby="titulo-erro-vagas"
        className="vagas-grupo2__estado vagas-grupo2__estado--erro"
        role="alert"
      >
        <h2 id="titulo-erro-vagas">Não foi possível carregar as vagas</h2>
        <p>{estado.mensagem}</p>

        <button
          className="vagas-grupo2__botao-recuperar"
          onClick={aoTentarNovamente}
          type="button"
        >
          Tentar novamente
        </button>
      </section>
    );
  }

  return (
    <ul aria-label="Vagas sugeridas" className="vagas-grupo2__lista">
      {estado.sugestoes.map((sugestao) => (
        <li key={chaveDaSugestao(sugestao)}>
          <CartaoVaga
            estadoDecisao={
              decisoes[chaveDaSugestao(sugestao)] ?? {
                tipo: "ocioso",
              }
            }
            onSalvarDecisao={aoSalvarDecisao}
            sugestao={sugestao}
          />
        </li>
      ))}
    </ul>
  );
}

/** Apresenta uma vaga e os controles acessíveis de decisão da sugestão. */
function CartaoVaga({
  sugestao,
  estadoDecisao,
  onSalvarDecisao,
}: {
  sugestao: SugestaoVaga;
  estadoDecisao: EstadoDecisao;
  onSalvarDecisao: (
    sugestao: SugestaoVaga,
    decisao: DecisaoRecomendacao,
  ) => Promise<void>;
}) {
  const { vaga } = sugestao;
  const salvando = estadoDecisao.tipo === "salvando";

  return (
    <article className="vagas-grupo2__card">
      <h2>{vaga.titulo}</h2>

      <p>
        <strong>{vaga.empresa}</strong>
      </p>

      <p>{vaga.descricao}</p>

      {(vaga.localizacao !== null || vaga.modalidade !== null) && (
        <div
          aria-label="Localização e modalidade"
          className="vagas-grupo2__metadados"
        >
          {vaga.localizacao !== null && <span>{vaga.localizacao}</span>}
          {vaga.modalidade !== null && <span>{vaga.modalidade}</span>}
        </div>
      )}

      <h3>Requisitos</h3>

      {vaga.requisitos.length === 0 ? (
        <p>Requisitos não informados.</p>
      ) : (
        <ul className="vagas-grupo2__requisitos">
          {vaga.requisitos.map((requisito) => (
            <li key={requisito}>{requisito}</li>
          ))}
        </ul>
      )}

      <div
        aria-label={`Decisão sobre ${vaga.titulo}`}
        className="vagas-grupo2__decisoes"
      >
        <button
          disabled={salvando}
          onClick={() => void onSalvarDecisao(sugestao, "aceitar")}
          type="button"
        >
          Aceitar recomendação
        </button>

        <button
          disabled={salvando}
          onClick={() => void onSalvarDecisao(sugestao, "rejeitar")}
          type="button"
        >
          Rejeitar recomendação
        </button>
      </div>

      {estadoDecisao.tipo === "salvando" && (
        <p role="status">Salvando decisão...</p>
      )}

      {estadoDecisao.tipo === "salva" && (
        <p role="status">
          Recomendação {textoDaDecisao(estadoDecisao.decisao)} e salva.
        </p>
      )}

      {estadoDecisao.tipo === "erro" && (
        <p role="alert">
          Não foi possível salvar a recomendação{" "}
          {textoDaDecisao(estadoDecisao.decisao)}. Tente novamente.
        </p>
      )}

      {vaga.urlCandidatura !== null && (
        <a
          className="vagas-grupo2__acao"
          href={vaga.urlCandidatura}
          rel="noreferrer"
          target="_blank"
        >
          Ver detalhes da vaga
        </a>
      )}
    </article>
  );
}

/** Gera uma chave estável para guardar o estado visual de cada sugestão. */
function chaveDaSugestao(sugestao: SugestaoVaga): string {
  return `${sugestao.curriculoId}-${sugestao.vaga.id}`;
}

/** Traduz o valor técnico da decisão para a frase apresentada à pessoa usuária. */
function textoDaDecisao(decisao: DecisaoRecomendacao): string {
  return decisao === "aceitar" ? "aceita" : "rejeitada";
}
