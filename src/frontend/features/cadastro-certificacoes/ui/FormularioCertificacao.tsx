import { useState, type FormEvent } from "react";

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
  /** Valores iniciais opcionais para os campos do formulário. */
  valoresIniciais?: ValoresCertificacao;
  /** Callback acionado ao submeter dados válidos. Suporta retorno síncrono ou Promise. */
  onSalvar?: (valores: ValoresCertificacao) => void | Promise<void>;
  /** Título apresentado no cabeçalho do formulário. Padrão: 'Certificações'. */
  titulo?: string;
  /** Prefixo para os identificadores dos campos no DOM. Padrão: 'certificacao'. */
  prefixoId?: string;
}

interface MensagemFeedback {
  tipo: "sucesso" | "erro";
  texto: string;
}

/**
 * Renderiza e gerencia o formulário acessível para cadastro de certificações.
 *
 * **O que faz:** Controla a entrada de dados, validação síncrona, vínculo de erros ARIA e submissão de certificações.
 * **Como faz:** Utiliza estado React local, associa rótulos e mensagens de erro via `CampoFormulario`, previne o comportamento nativo de submit e controla o ciclo de envio com feedback acessível (`role="status"` ou `role="alert"`).
 * **Qual finalidade atende:** Atende aos requisitos da issue #207 (F4.17), assegurando uma experiência acessível e aderente a WCAG 2.1 AA sem acoplamento a bibliotecas externas.
 */
export function FormularioCertificacao({
  valoresIniciais = criarCertificacaoVazia(),
  onSalvar,
  titulo = "Certificações",
  prefixoId = "certificacao",
}: FormularioCertificacaoProps) {
  const [valores, setValores] = useState<ValoresCertificacao>(valoresIniciais);
  const [erros, setErros] = useState<ErrosCertificacao>({});
  const [mensagem, setMensagem] = useState<MensagemFeedback | null>(null);
  const [enviando, setEnviando] = useState(false);

  /**
   * Atualiza o valor de um campo e limpa o erro e feedback ativo correspondente.
   *
   * **O que faz:** Sincroniza o estado do campo com a digitação do usuário.
   * **Como faz:** Atualiza a chave correspondente em `valores` e remove a mensagem de erro do campo em `erros`.
   * **Qual finalidade atende:** Proporciona resposta interativa imediata ao usuário sem manter erros obsoletos na tela.
   */
  function atualizarCampo(
    campo: keyof ValoresCertificacao,
    novoValor: string,
  ): void {
    setValores((atuais) => ({ ...atuais, [campo]: novoValor }));
    setErros((atuais) => {
      if (atuais[campo] === undefined) return atuais;
      const novosErros = { ...atuais };
      delete novosErros[campo];
      return novosErros;
    });
    setMensagem(null);
  }

  /**
   * Processa o envio controlado do formulário de certificação.
   *
   * **O que faz:** Intercepta a submissão, executa validação e despacha os dados higienizados para persistência.
   * **Como faz:** Cancela o submit padrão do navegador, valida os campos com `validarCertificacao`, gerencia a flag `enviando` e notifica o resultado com papéis semânticos ARIA.
   * **Qual finalidade atende:** Evita recargas de página, bloqueia envios com dados inválidos ou múltiplos cliques concorrentes.
   */
  async function enviarFormulario(
    evento: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    evento.preventDefault();
    if (enviando) return;

    const novosErros = validarCertificacao(valores);
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
      const valoresNormalizados = normalizarCertificacao(valores);
      await onSalvar?.(valoresNormalizados);
      setValores(criarCertificacaoVazia());
      setMensagem({
        tipo: "sucesso",
        texto: "Certificação salva com sucesso.",
      });
    } catch {
      setMensagem({
        tipo: "erro",
        texto: "Não foi possível salvar a certificação. Tente novamente.",
      });
    } finally {
      setEnviando(false);
    }
  }

  const idNome = `${prefixoId}-nome`;
  const idEmissor = `${prefixoId}-emissor`;

  return (
    <form
      aria-labelledby={`${prefixoId}-titulo`}
      className="formulario-certificacao"
      noValidate
      onSubmit={enviarFormulario}
    >
      <h2 id={`${prefixoId}-titulo`}>{titulo}</h2>

      <div className="formulario-certificacao__grupo">
        <CampoFormulario
          desabilitado={enviando}
          erro={erros.nome}
          id={idNome}
          obrigatorio
          onChange={(valor) => atualizarCampo("nome", valor)}
          rotulo="Nome da certificação"
          valor={valores.nome}
        />

        <CampoFormulario
          desabilitado={enviando}
          erro={erros.organizacaoEmissora}
          id={idEmissor}
          obrigatorio
          onChange={(valor) => atualizarCampo("organizacaoEmissora", valor)}
          rotulo="Organização emissora"
          valor={valores.organizacaoEmissora}
        />
      </div>

      {mensagem !== null && (
        <p
          className={`form-message form-message--${mensagem.tipo}`}
          role={mensagem.tipo === "sucesso" ? "status" : "alert"}
        >
          {mensagem.texto}
        </p>
      )}

      <div className="formulario-certificacao__acoes">
        <button disabled={enviando} type="submit">
          {enviando ? "Salvando certificação..." : "Salvar certificação"}
        </button>
      </div>
    </form>
  );
}
