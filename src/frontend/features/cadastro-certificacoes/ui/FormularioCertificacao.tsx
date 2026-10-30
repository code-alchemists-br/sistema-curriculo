import { useEffect, useState, type FormEvent } from "react";

import { CampoFormulario } from "../../../shared";
import {
  criarCertificacaoVazia,
  normalizarCertificacao,
  validarCertificacao,
  type ErrosCertificacao,
  type ValoresCertificacao,
} from "../model/certificacao";
import "./FormularioCertificacao.css";

/**
 * Propriedades para configuração do formulário acessível de certificação.
 */
export interface FormularioCertificacaoProps {
  /** Valores iniciais opcionais para uma certificação única. */
  valoresIniciais?: ValoresCertificacao;
  /** Lista inicial de certificações para edição múltipla. */
  certificacoesIniciais?: ValoresCertificacao[];
  /** Callback acionado ao submeter dados válidos. Suporta retorno síncrono ou Promise. */
  onSalvar?: (
    valores: ValoresCertificacao | ValoresCertificacao[],
  ) => void | Promise<void>;
  /** Título apresentado no cabeçalho do formulário. Padrão: 'Certificações'. */
  titulo?: string;
  /** Prefixo para os identificadores dos campos no DOM. Padrão: 'certificacao'. */
  prefixoId?: string;
  /** Notifica a porcentagem de campos preenchidos nesta seção (0 a 100). */
  aoAlterarProgresso?: (progresso: number) => void;
  /** Notifica alterações nas certificações para preservação de estado. */
  aoAlterarCertificacoes?: (certificacoes: ValoresCertificacao[]) => void;
  /** Controla a visibilidade do botão interno de salvar (padrão: true para retrocompatibilidade). */
  exibirBotaoSalvar?: boolean;
}

interface MensagemFeedback {
  tipo: "sucesso" | "erro";
  texto: string;
}

/**
 * Renderiza e gerencia o formulário acessível para cadastro de certificações.
 *
 * Controla entrada dinâmica de múltiplas certificações, validação síncrona,
 * placeholders contextualizados e vínculos ARIA de acessibilidade.
 */
export function FormularioCertificacao({
  valoresIniciais,
  certificacoesIniciais,
  onSalvar,
  titulo = "Certificações",
  prefixoId = "certificacao",
  aoAlterarProgresso,
  aoAlterarCertificacoes,
  exibirBotaoSalvar = true,
}: FormularioCertificacaoProps) {
  const [certificacoes, setCertificacoes] = useState<ValoresCertificacao[]>(
    () => {
      if (certificacoesIniciais && certificacoesIniciais.length > 0) {
        return certificacoesIniciais;
      }
      if (valoresIniciais) {
        return [valoresIniciais];
      }
      return [criarCertificacaoVazia()];
    },
  );

  const [erros, setErros] = useState<Record<number, ErrosCertificacao>>({});
  const [mensagem, setMensagem] = useState<MensagemFeedback | null>(null);
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    aoAlterarCertificacoes?.(certificacoes);
  }, [certificacoes, aoAlterarCertificacoes]);

  useEffect(() => {
    if (!aoAlterarProgresso) return;
    if (certificacoes.length === 0) {
      aoAlterarProgresso(0);
      return;
    }
    let preenchidos = 0;
    const total = certificacoes.length * 2;

    certificacoes.forEach((cert) => {
      if (cert.nome.trim().length > 0) preenchidos++;
      if (cert.organizacaoEmissora.trim().length > 0) preenchidos++;
    });

    aoAlterarProgresso(total > 0 ? Math.round((preenchidos / total) * 100) : 0);
  }, [certificacoes, aoAlterarProgresso]);

  function atualizarCampo(
    indice: number,
    campo: keyof ValoresCertificacao,
    novoValor: string,
  ): void {
    setCertificacoes((atuais) =>
      atuais.map((cert, i) =>
        i === indice ? { ...cert, [campo]: novoValor } : cert,
      ),
    );

    setErros((atuais) => {
      if (!atuais[indice] || atuais[indice][campo] === undefined) return atuais;
      const errosCert = { ...atuais[indice] };
      delete errosCert[campo];
      const novosErros = { ...atuais };
      if (Object.keys(errosCert).length === 0) {
        delete novosErros[indice];
      } else {
        novosErros[indice] = errosCert;
      }
      return novosErros;
    });
    setMensagem(null);
  }

  function adicionarCertificacao(): void {
    setCertificacoes((atuais) => [...atuais, criarCertificacaoVazia()]);
  }

  function removerCertificacao(indice: number): void {
    setCertificacoes((atuais) => atuais.filter((_, i) => i !== indice));
    setErros((atuais) => {
      const novosErros: Record<number, ErrosCertificacao> = {};
      Object.entries(atuais).forEach(([chave, valor]) => {
        const idxOriginal = Number(chave);
        if (idxOriginal < indice) {
          novosErros[idxOriginal] = valor;
        } else if (idxOriginal > indice) {
          novosErros[idxOriginal - 1] = valor;
        }
      });
      return novosErros;
    });
    setMensagem(null);
  }

  async function enviarFormulario(
    evento: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    evento.preventDefault();
    if (enviando) return;

    const novosErros: Record<number, ErrosCertificacao> = {};
    certificacoes.forEach((cert, idx) => {
      const errosCert = validarCertificacao(cert);
      if (Object.keys(errosCert).length > 0) {
        novosErros[idx] = errosCert;
      }
    });

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      setMensagem({
        tipo: "erro",
        texto: "Corrija os campos destacados antes de salvar a certificação.",
      });
      return;
    }

    setEnviando(true);
    setErros({});
    setMensagem(null);

    try {
      const valoresNormalizados = certificacoes.map(normalizarCertificacao);
      if (onSalvar) {
        if (certificacoes.length === 1) {
          await onSalvar(valoresNormalizados[0]);
        } else {
          await onSalvar(valoresNormalizados);
        }
      }
      setMensagem({
        tipo: "sucesso",
        texto: "Certificação salva com sucesso.",
      });
      if (certificacoes.length === 1 && exibirBotaoSalvar) {
        setCertificacoes([criarCertificacaoVazia()]);
      }
    } catch {
      setMensagem({
        tipo: "erro",
        texto: "Não foi possível salvar a certificação. Tente novamente.",
      });
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form
      aria-labelledby={`${prefixoId}-titulo`}
      className="formulario-certificacao"
      noValidate
      onSubmit={enviarFormulario}
    >
      <h2 id={`${prefixoId}-titulo`}>{titulo}</h2>

      {certificacoes.map((cert, indice) => {
        const idNome =
          indice === 0 ? `${prefixoId}-nome` : `${prefixoId}-${indice}-nome`;
        const idEmissor =
          indice === 0
            ? `${prefixoId}-emissor`
            : `${prefixoId}-${indice}-emissor`;
        const errosCert = erros[indice];

        return (
          <fieldset
            aria-label={`Certificação ${indice + 1}`}
            key={`cert-${indice}`}
          >
            <legend className="sr-only">Certificação {indice + 1}</legend>

            {certificacoes.length > 1 && (
              <div className="item-sublista__topo">
                <span className="label-subtitulo">
                  Certificação {indice + 1}
                </span>
                <button
                  aria-label={`Remover certificação ${indice + 1}`}
                  className="btn-remover-item"
                  onClick={() => removerCertificacao(indice)}
                  type="button"
                >
                  Remover
                </button>
              </div>
            )}

            <div className="formulario-certificacao__grupo">
              <CampoFormulario
                desabilitado={enviando}
                erro={errosCert?.nome}
                id={idNome}
                onChange={(valor) => atualizarCampo(indice, "nome", valor)}
                placeholder="Ex.: AWS Certified Solutions Architect, Scrum Master..."
                rotulo="Nome da certificação"
                valor={cert.nome}
              />

              <CampoFormulario
                desabilitado={enviando}
                erro={errosCert?.organizacaoEmissora}
                id={idEmissor}
                onChange={(valor) =>
                  atualizarCampo(indice, "organizacaoEmissora", valor)
                }
                placeholder="Ex.: Amazon Web Services, Scrum.org..."
                rotulo="Organização emissora"
                valor={cert.organizacaoEmissora}
              />
            </div>
          </fieldset>
        );
      })}

      <button
        className="btn-adicionar-item"
        onClick={adicionarCertificacao}
        type="button"
      >
        + Adicionar certificação
      </button>

      {mensagem !== null && (
        <p
          className={`form-message form-message--${mensagem.tipo}`}
          role={mensagem.tipo === "sucesso" ? "status" : "alert"}
        >
          {mensagem.texto}
        </p>
      )}

      {exibirBotaoSalvar && (
        <div className="formulario-certificacao__acoes">
          <button disabled={enviando} type="submit">
            {enviando ? "Salvando certificação..." : "Salvar certificação"}
          </button>
        </div>
      )}
    </form>
  );
}
