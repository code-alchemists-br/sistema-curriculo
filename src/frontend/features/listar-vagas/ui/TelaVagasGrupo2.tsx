import { useCallback, useEffect, useState } from "react";

import type { SugestaoVaga } from "../../../entities/vaga";
import type { ClienteDecisoesRecomendacao } from "../api/cliente-decisoes-recomendacao";
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

const VARIANTES_AVATAR = ["azul", "vermelho", "verde", "laranja"] as const;

function obterVarianteAvatar(empresa: string): string {
  let soma = 0;
  for (let i = 0; i < empresa.length; i += 1) {
    soma += empresa.charCodeAt(i);
  }
  return VARIANTES_AVATAR[soma % VARIANTES_AVATAR.length];
}

function obterInicialEmpresa(empresa: string): string {
  const limpa = empresa.trim();
  if (
    !limpa ||
    limpa.toLowerCase() === "empresa confidencial" ||
    limpa.toLowerCase() === "empresa não informada"
  ) {
    return "✦";
  }
  return limpa.charAt(0).toUpperCase();
}

/**
 * Apresenta as vagas recomendadas pela integração do Grupo 2 para o currículo
 * do estudante, priorizando leitura rápida, hierarquia clara e acesso direto
 * à publicação original.
 */
export function TelaVagasGrupo2({ cliente }: TelaVagasGrupo2Props) {
  const [estado, setEstado] = useState<EstadoVagasGrupo2>({
    tipo: "carregando",
  });

  const consultarRecomendacoes = useCallback(
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

  const tentarNovamente = useCallback((): void => {
    setEstado({ tipo: "carregando" });
    void consultarRecomendacoes({ termo: "" }).then(setEstado);
  }, [consultarRecomendacoes]);

  useEffect(() => {
    let componenteAtivo = true;

    void consultarRecomendacoes({ termo: "" }).then((novoEstado) => {
      if (componenteAtivo) {
        setEstado(novoEstado);
      }
    });

    return () => {
      componenteAtivo = false;
    };
  }, [consultarRecomendacoes]);

  return (
    <section aria-labelledby="titulo-vagas-grupo2" className="vagas-grupo2">
      <header className="vagas-grupo2__hero">
        <h1 id="titulo-vagas-grupo2">
          Oportunidades compatíveis com o seu perfil
        </h1>
        <p className="vagas-grupo2__subtitulo">
          Vagas selecionadas automaticamente com base nas competências e
          experiências do seu currículo.
        </p>
      </header>

      <div className="vagas-grupo2__corpo-resultados">
        {renderizarEstado(estado, tentarNovamente)}
      </div>
    </section>
  );
}

/** Renderiza o estado atual da consulta de recomendações. */
function renderizarEstado(
  estado: EstadoVagasGrupo2,
  aoTentarNovamente: () => void,
) {
  if (estado.tipo === "carregando") {
    return (
      <p className="vagas-grupo2__carregando" role="status">
        Carregando vagas sugeridas...
      </p>
    );
  }

  if (estado.tipo === "vazio") {
    return (
      // Proveniência: decision-analysis prompts/frontend/20261019-073800-vagas-leitor-tela-teclado-v001.md#v001
      <section
        aria-labelledby="titulo-vagas-vazias"
        className="vagas-grupo2__estado"
        role="status"
      >
        <h2 id="titulo-vagas-vazias">Nenhuma vaga compatível no momento</h2>
        <p>Ainda não encontramos oportunidades alinhadas ao seu currículo.</p>
        <p>
          Adicione mais competências ou experiências para ampliar suas
          correspondências.
        </p>
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

  const total = estado.sugestoes.length;
  const rotuloContagem =
    total === 1
      ? "1 oportunidade alinhada às suas competências"
      : `${total} oportunidades alinhadas às suas competências`;

  return (
    <div className="vagas-grupo2__secao-lista">
      <div aria-hidden="true" className="vagas-grupo2__cabecalho-secao">
        <span className="vagas-grupo2__titulo-recomendadas">
          Vagas recomendadas
        </span>
        <span className="vagas-grupo2__info-ordem">{rotuloContagem}</span>
      </div>

      <ul aria-label="Vagas sugeridas" className="vagas-grupo2__lista">
        {estado.sugestoes.map((sugestao) => (
          <li key={chaveDaSugestao(sugestao)}>
            <CartaoVaga sugestao={sugestao} />
          </li>
        ))}
      </ul>
    </div>
  );
}

/** Apresenta uma vaga recomendada com hierarquia limpa e ação direta. */
function CartaoVaga({ sugestao }: { sugestao: SugestaoVaga }) {
  const { vaga } = sugestao;
  const nomeEmpresa = vaga.empresa || "Empresa confidencial";
  const varianteAvatar = obterVarianteAvatar(nomeEmpresa);
  const inicialEmpresa = obterInicialEmpresa(nomeEmpresa);

  const possuiClassificacao =
    Boolean(vaga.nivelSenioridade) ||
    vaga.modalidade !== null ||
    Boolean(
      vaga.requisitos.length === 0 &&
        vaga.palavrasChave &&
        vaga.palavrasChave.length > 0,
    );

  return (
    <article className="vagas-grupo2__card">
      <div className="vagas-grupo2__corpo-card">
        {(sugestao.ranque !== undefined ||
          sugestao.pontuacaoCompatibilidade !== undefined) && (
          <div
            aria-label="Compatibilidade da recomendação"
            className="vagas-grupo2__faixa-afinidade"
          >
            {sugestao.ranque !== undefined && (
              <span className="vagas-grupo2__ranque">
                #{sugestao.ranque} em relevância
              </span>
            )}
            {sugestao.pontuacaoCompatibilidade !== undefined && (
              <span className="vagas-grupo2__score">
                {Math.round(sugestao.pontuacaoCompatibilidade)}% compatível
              </span>
            )}
          </div>
        )}

        <div className="vagas-grupo2__cabecalho-card">
          <div
            aria-hidden="true"
            className={`vagas-grupo2__avatar vagas-grupo2__avatar--${varianteAvatar}`}
          >
            {inicialEmpresa}
          </div>

          <div className="vagas-grupo2__identificacao">
            <h2>{vaga.titulo}</h2>
            <p className="vagas-grupo2__subtitulo-empresa">
              <strong>{nomeEmpresa}</strong>
              {vaga.localizacao !== null && (
                <>
                  <span aria-hidden="true" className="vagas-grupo2__ponto">
                    •
                  </span>
                  <span className="vagas-grupo2__localizacao">
                    {vaga.localizacao}
                  </span>
                </>
              )}
            </p>
          </div>
        </div>

        {possuiClassificacao && (
          <div
            aria-label="Classificação da vaga"
            className="vagas-grupo2__metadados"
          >
            {vaga.nivelSenioridade && (
              <span className="vagas-grupo2__pill vagas-grupo2__pill--roxo">
                {vaga.nivelSenioridade}
              </span>
            )}
            {vaga.modalidade !== null && (
              <span className="vagas-grupo2__pill vagas-grupo2__pill--verde">
                {vaga.modalidade}
              </span>
            )}
            {vaga.requisitos.length === 0 &&
              vaga.palavrasChave &&
              vaga.palavrasChave.map((palavra) => (
                <span
                  className="vagas-grupo2__pill vagas-grupo2__pill--laranja"
                  key={palavra}
                >
                  {palavra}
                </span>
              ))}
          </div>
        )}

        <p className="vagas-grupo2__descricao">{vaga.descricao}</p>

        {vaga.requisitos.length > 0 && (
          <ul
            aria-label="Competências e requisitos"
            className="vagas-grupo2__requisitos-tags"
          >
            {vaga.requisitos.map((requisito) => (
              <li key={requisito}>{requisito}</li>
            ))}
          </ul>
        )}
      </div>

      <div className="vagas-grupo2__rodape-card">
        <div className="vagas-grupo2__meta-rodape">
          <div className="vagas-grupo2__bloco-salario">
            {vaga.salario ? (
              <span className="vagas-grupo2__salario">{vaga.salario}</span>
            ) : (
              <span
                aria-hidden="true"
                className="vagas-grupo2__salario vagas-grupo2__salario--combinar"
              >
                Remuneração a combinar
              </span>
            )}
          </div>

          {vaga.dataPublicacao && (
            <div className="vagas-grupo2__bloco-publicacao">
              <svg
                aria-hidden="true"
                fill="none"
                height="14"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                width="14"
              >
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
              </svg>
              <span className="vagas-grupo2__publicacao">
                Publicada em {vaga.dataPublicacao}
              </span>
            </div>
          )}
        </div>

        {vaga.urlCandidatura !== null && (
          <a
            className="vagas-grupo2__acao"
            href={vaga.urlCandidatura}
            rel="noreferrer"
            target="_blank"
          >
            Acessar vaga original
          </a>
        )}
      </div>
    </article>
  );
}

/** Gera uma chave estável para cada sugestão listada. */
function chaveDaSugestao(sugestao: SugestaoVaga): string {
  return `${sugestao.curriculoId}-${sugestao.vaga.id}`;
}
