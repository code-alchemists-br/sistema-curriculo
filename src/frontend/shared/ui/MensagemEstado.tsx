import { useId, type ReactNode } from "react";
import "./MensagemEstado.css";

/**
 * Enumera os tipos de estado suportados pelo componente.
 */
export type TipoMensagemEstado = "carregando" | "vazio" | "erro";

/**
 * Propriedades para configuração do componente de mensagem de estado.
 */
export interface MensagemEstadoProps {
  /** Tipo de estado a ser apresentado: carregamento, vazio ou erro. */
  tipo: TipoMensagemEstado;
  /** Título principal informativo ou descritivo do estado. */
  titulo?: string;
  /** Mensagem complementar com orientações ou detalhes do estado. */
  mensagem?: string;
  /** Rótulo textual do botão de ação. Padrão: 'Tentar novamente' em erros, 'Recarregar' em vazio. */
  textoAcao?: string;
  /** Callback acionado ao clicar no botão de ação. */
  onAcao?: () => void;
  /** Conteúdo visual ou nós adicionais customizados. */
  children?: ReactNode;
}

/**
 * Renderiza mensagens de estado padronizadas para carregamento, vazio e erro.
 *
 * **O que faz:** Apresenta visualmente e semanticamente o status de requisições ou listas vazias.
 * **Como faz:** Seleciona elementos semânticos e papéis ARIA conformes (`role="status"` em carregamento,
 * `role="alert"` em erro e `<section>` em estado vazio), renderizando títulos, descrições e ações opcionais.
 * **Qual finalidade atende:** Centraliza e padroniza os estados assíncronos da interface na camada shared,
 * sem acoplamento a regras ou entidades do domínio do sistema.
 */
export function MensagemEstado({
  tipo,
  titulo,
  mensagem,
  textoAcao,
  onAcao,
  children,
}: MensagemEstadoProps) {
  const idTitulo = useId();

  if (tipo === "carregando") {
    return (
      <div
        aria-live="polite"
        className="mensagem-estado mensagem-estado--carregando"
        role="status"
      >
        {titulo && (
          <h3 className="mensagem-estado__titulo" id={idTitulo}>
            {titulo}
          </h3>
        )}
        <p className="mensagem-estado__descricao">
          {mensagem ?? "Carregando..."}
        </p>
        {children}
      </div>
    );
  }

  if (tipo === "vazio") {
    const textoBotao = textoAcao ?? "Recarregar";
    return (
      <section
        aria-labelledby={titulo ? idTitulo : undefined}
        className="mensagem-estado mensagem-estado--vazio"
      >
        {titulo && (
          <h3 className="mensagem-estado__titulo" id={idTitulo}>
            {titulo}
          </h3>
        )}
        {mensagem && (
          <p className="mensagem-estado__descricao">{mensagem}</p>
        )}
        {children}
        {onAcao && (
          <button
            className="mensagem-estado__botao"
            onClick={onAcao}
            type="button"
          >
            {textoBotao}
          </button>
        )}
      </section>
    );
  }

  const textoBotaoErro = textoAcao ?? "Tentar novamente";
  return (
    <section
      aria-labelledby={titulo ? idTitulo : undefined}
      className="mensagem-estado mensagem-estado--erro"
      role="alert"
    >
      {titulo && (
        <h3 className="mensagem-estado__titulo" id={idTitulo}>
          {titulo}
        </h3>
      )}
      {mensagem && (
        <p className="mensagem-estado__descricao">{mensagem}</p>
      )}
      {children}
      {onAcao && (
        <button
          className="mensagem-estado__botao"
          onClick={onAcao}
          type="button"
        >
          {textoBotaoErro}
        </button>
      )}
    </section>
  );
}
