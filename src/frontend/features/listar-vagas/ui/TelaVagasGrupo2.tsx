import { useCallback, useEffect, useState } from "react";

import type { SugestaoVaga } from "../../../entities/vaga";
import {
  FalhaVagasGrupo2,
  type ClienteVagasGrupo2,
} from "../api/cliente-vagas-grupo2";
import "./TelaVagasGrupo2.css";

/** Define o cliente de integração recebido pela tela de resultados. */
export interface TelaVagasGrupo2Props {
  cliente: ClienteVagasGrupo2;
}

/** Representa cada estado mutuamente exclusivo da consulta de sugestões. */
type EstadoVagasGrupo2 =
  | { tipo: "carregando" }
  | { tipo: "resultado"; sugestoes: SugestaoVaga[] }
  | { tipo: "vazio" }
  | { tipo: "erro"; mensagem: string };

/**
 * Apresenta sugestões de vagas da integração com o Grupo 2.
 *
 * O componente inicia a consulta quando é montado, classifica o retorno em
 * carregamento, resultado, vazio ou erro e permite tentar novamente. Ele existe
 * para exibir as vagas sugeridas sem criar associações persistidas ou conhecer
 * detalhes de HTTP e autenticação.
 */
export function TelaVagasGrupo2({ cliente }: TelaVagasGrupo2Props) {
  const [estado, setEstado] = useState<EstadoVagasGrupo2>({ tipo: "carregando" });

  /** Consulta o cliente injetado e converte o desfecho no estado da interface. */
  const carregarVagas = useCallback(async (): Promise<void> => {
    setEstado({ tipo: "carregando" });

    try {
      const sugestoes = await cliente.listarSugestoes();
      setEstado(sugestoes.length === 0 ? { tipo: "vazio" } : { tipo: "resultado", sugestoes });
    } catch (erro: unknown) {
      setEstado({ tipo: "erro", mensagem: mensagemDeErro(erro) });
    }
  }, [cliente]);

  useEffect(() => {
    void carregarVagas();
  }, [carregarVagas]);

  return (
    <section aria-labelledby="titulo-vagas-grupo2" className="vagas-grupo2">
      <div>
        <p className="eyebrow">Vagas sugeridas</p>
        <h1 id="titulo-vagas-grupo2">Oportunidades para o seu currículo</h1>
        <p>Estas vagas foram sugeridas pela integração com o Grupo 2.</p>
      </div>
      {renderizarEstado(estado, carregarVagas)}
    </section>
  );
}

/** Exibe o conteúdo adequado para o estado atual da consulta. */
function renderizarEstado(
  estado: EstadoVagasGrupo2,
  aoTentarNovamente: () => Promise<void>,
) {
  if (estado.tipo === "carregando") {
    return <p role="status">Carregando vagas sugeridas...</p>;
  }

  if (estado.tipo === "vazio") {
    return (
      <section className="vagas-grupo2__estado" aria-labelledby="titulo-vagas-vazias">
        <h2 id="titulo-vagas-vazias">Nenhuma vaga encontrada</h2>
        <p>Não encontramos vagas sugeridas para este currículo neste momento.</p>
      </section>
    );
  }

  if (estado.tipo === "erro") {
    return (
      <section className="vagas-grupo2__estado" aria-labelledby="titulo-erro-vagas" role="alert">
        <h2 id="titulo-erro-vagas">Não foi possível carregar as vagas</h2>
        <p>{estado.mensagem}</p>
        <button onClick={() => void aoTentarNovamente()} type="button">
          Tentar novamente
        </button>
      </section>
    );
  }

  return (
    <ul aria-label="Vagas sugeridas" className="vagas-grupo2__lista">
      {estado.sugestoes.map((sugestao) => (
        <li key={`${sugestao.curriculoId}-${sugestao.vaga.id}`}>
          <CartaoVaga sugestao={sugestao} />
        </li>
      ))}
    </ul>
  );
}

/** Renderiza os dados apresentáveis de uma vaga sugerida. */
function CartaoVaga({ sugestao }: { sugestao: SugestaoVaga }) {
  const { vaga } = sugestao;

  return (
    <article className="vagas-grupo2__card">
      <h2>{vaga.titulo}</h2>
      <p><strong>{vaga.empresa}</strong></p>
      <p>{vaga.descricao}</p>
      {(vaga.localizacao !== null || vaga.modalidade !== null) && (
        <div aria-label="Localização e modalidade" className="vagas-grupo2__metadados">
          {vaga.localizacao !== null && <span>{vaga.localizacao}</span>}
          {vaga.modalidade !== null && <span>{vaga.modalidade}</span>}
        </div>
      )}
      <h3>Requisitos</h3>
      {vaga.requisitos.length === 0 ? (
        <p>Requisitos não informados.</p>
      ) : (
        <ul className="vagas-grupo2__requisitos">
          {vaga.requisitos.map((requisito) => <li key={requisito}>{requisito}</li>)}
        </ul>
      )}
      {vaga.urlCandidatura !== null && (
        <a className="vagas-grupo2__acao" href={vaga.urlCandidatura} rel="noreferrer" target="_blank">
          Ver detalhes da vaga
        </a>
      )}
    </article>
  );
}

/** Traduz a falha da fronteira em texto seguro e compreensível. */
function mensagemDeErro(erro: unknown): string {
  if (erro instanceof FalhaVagasGrupo2 && erro.codigo === "resposta-invalida") {
    return "Recebemos uma resposta inesperada. Tente novamente mais tarde.";
  }

  return "A integração de vagas está indisponível no momento. Tente novamente mais tarde.";
}
