import type { ReactNode } from "react";
import "./EstadoVazioSecao.css";

/**
 * Propriedades para configuração da visualização de estado vazio de uma seção.
 */
export interface EstadoVazioSecaoProps {
  /** Nome ou título da seção (ex: "Formação acadêmica", "Experiência profissional"). */
  titulo: string;
  /** Mensagem complementar explicativa sobre a ausência de itens. */
  mensagem?: string;
  /** Rótulo textual do botão de ação opcional (ex: "Adicionar formação"). */
  textoAcao?: string;
  /** Callback executado ao acionar o botão de ação. */
  onAcao?: () => void;
  /** Elementos visuais ou nós adicionais customizados. */
  children?: ReactNode;
}

/**
 * Apresenta a visualização acessível de estado vazio para uma seção sem itens.
 *
 * - O que faz: Exibe uma mensagem informativa, ícone sutil e ação opcional quando uma seção selecionada não contém itens.
 * - Como faz: Renderiza um container semântico com papel ARIA `role="status"` e `aria-label`, estilizado com CSS puro sem bibliotecas de terceiros.
 * - Qual finalidade atende: Comunica de forma clara, amigável e acessível aos estudantes e recrutadores que a seção está ativa no modelo, mas ainda não possui itens preenchidos ou selecionados.
 *
 * @param props Propriedades de configuração do estado vazio da seção.
 * @returns Elemento JSX representando o estado vazio.
 */
export function EstadoVazioSecao({
  titulo,
  mensagem,
  textoAcao,
  onAcao,
  children,
}: EstadoVazioSecaoProps) {
  const mensagemPadrao = `Nenhum item selecionado ou cadastrado para ${titulo.toLowerCase()}.`;
  const rotuloAcaoPadrao = `Adicionar ${titulo.toLowerCase()}`;

  return (
    <div
      aria-label={`Seção ${titulo} sem itens`}
      className="estado-vazio-secao"
      role="status"
    >
      <div aria-hidden="true" className="estado-vazio-secao__indicador">
        <svg
          className="estado-vazio-secao__icone"
          fill="none"
          height="20"
          stroke="currentColor"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          viewBox="0 0 24 24"
          width="20"
        >
          <circle cx="12" cy="12" r="10" />
          <line x1="12" x2="12" y1="8" y2="12" />
          <line x1="12" x2="12.01" y1="16" y2="16" />
        </svg>
      </div>

      <div className="estado-vazio-secao__conteudo">
        <p className="estado-vazio-secao__mensagem">
          {mensagem ?? mensagemPadrao}
        </p>
        {children}
      </div>

      {onAcao && (
        <button
          className="estado-vazio-secao__botao"
          onClick={onAcao}
          type="button"
        >
          {textoAcao ?? rotuloAcaoPadrao}
        </button>
      )}
    </div>
  );
}
