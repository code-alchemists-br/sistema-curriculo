import { useEffect, useId, useRef, type ReactNode } from "react";
import "./Dialogo.css";

/**
 * Propriedades para configuração do componente genérico de diálogo acessível.
 */
export interface DialogoProps {
  /** Determina a visibilidade do diálogo modal na tela. */
  aberto: boolean;
  /** Título principal acessível apresentado no cabeçalho do diálogo. */
  titulo: string;
  /** Descrição textual complementar associada ao diálogo. */
  descricao?: string;
  /** Callback acionado ao solicitar o fechamento (via Escape ou clique no botão de fechar). */
  onFechar: () => void;
  /** Elemento opcional que disparou a abertura para restauração de foco; se omitido, captura o activeElement. */
  elementoDisparador?: HTMLElement | null;
  /** Conteúdo interno customizável apresentado no corpo do diálogo. */
  children?: ReactNode;
}

/**
 * Obtém os elementos interativos e focalizáveis contidos dentro do container.
 *
 * **O que faz:** Filtra e retorna todos os elementos capazes de receber foco pelo teclado.
 * **Como faz:** Executa querySelectorAll procurando links, botões, inputs, selects e elementos com tabindex válido.
 * **Qual finalidade atende:** Viabiliza o mecanismo de contenção de foco (focus trap) para navegação acessível.
 */
function obterElementosFocalizaveis(
  container: HTMLElement | null,
): HTMLElement[] {
  if (!container) return [];
  const seletor =
    'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])';
  return Array.from(container.querySelectorAll<HTMLElement>(seletor)).filter(
    (el) =>
      !el.hasAttribute("disabled") && el.getAttribute("aria-hidden") !== "true",
  );
}

/**
 * Renderiza um diálogo modal com foco contido e retorno automático de foco ao disparador.
 *
 * **O que faz:** Exibe um diálogo modal com semântica ARIA completa, isolamento de navegação e restauração de foco.
 * **Como faz:** Captura o elemento disparador no momento da abertura e restaura seu foco no fechamento;
 * intercepta eventos de teclado Tab/Shift+Tab para manter o foco contido dentro do modal (focus trap);
 * e fecha ao pressionar Escape ou clicar no botão fechar.
 * **Qual finalidade atende:** Garante total conformidade com as diretrizes WCAG 2.1 (Critérios 2.1.2 e 2.4.3),
 * permitindo navegação fluida e acessível por teclado e tecnologias assistivas.
 */
export function Dialogo({
  aberto,
  titulo,
  descricao,
  onFechar,
  elementoDisparador,
  children,
}: DialogoProps) {
  const idTitulo = useId();
  const idDescricao = useId();
  const containerRef = useRef<HTMLDivElement>(null);
  const disparadorRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (aberto) {
      disparadorRef.current =
        elementoDisparador ?? (document.activeElement as HTMLElement | null);

      const focalizaveis = obterElementosFocalizaveis(containerRef.current);
      if (focalizaveis.length > 0) {
        focalizaveis[0]?.focus();
      } else {
        containerRef.current?.focus();
      }
    } else if (disparadorRef.current) {
      disparadorRef.current.focus();
      disparadorRef.current = null;
    }
  }, [aberto, elementoDisparador]);

  useEffect(() => {
    return () => {
      disparadorRef.current?.focus();
    };
  }, []);

  useEffect(() => {
    if (!aberto) return;

    function lidarComKeyDown(evento: KeyboardEvent): void {
      if (evento.key === "Escape") {
        evento.preventDefault();
        onFechar();
        return;
      }

      if (evento.key === "Tab") {
        if (!containerRef.current) return;
        const focalizaveis = obterElementosFocalizaveis(containerRef.current);
        if (focalizaveis.length === 0) {
          evento.preventDefault();
          return;
        }

        const primeiro = focalizaveis[0];
        const ultimo = focalizaveis[focalizaveis.length - 1];

        if (evento.shiftKey) {
          if (
            document.activeElement === primeiro ||
            !containerRef.current.contains(document.activeElement)
          ) {
            evento.preventDefault();
            ultimo.focus();
          }
        } else {
          if (
            document.activeElement === ultimo ||
            !containerRef.current.contains(document.activeElement)
          ) {
            evento.preventDefault();
            primeiro.focus();
          }
        }
      }
    }

    document.addEventListener("keydown", lidarComKeyDown);
    return () => document.removeEventListener("keydown", lidarComKeyDown);
  }, [aberto, onFechar]);

  if (!aberto) return null;

  return (
    <div
      className="dialogo-overlay"
      onClick={(evento) => {
        if (evento.target === evento.currentTarget) {
          onFechar();
        }
      }}
      role="presentation"
    >
      <div
        aria-describedby={descricao ? idDescricao : undefined}
        aria-labelledby={idTitulo}
        aria-modal="true"
        className="dialogo"
        ref={containerRef}
        role="dialog"
        tabIndex={-1}
      >
        <div className="dialogo__cabecalho">
          <h2 className="dialogo__titulo" id={idTitulo}>
            {titulo}
          </h2>
          <button
            aria-label="Fechar diálogo"
            className="dialogo__botao-fechar"
            onClick={onFechar}
            type="button"
          >
            ×
          </button>
        </div>

        {descricao && (
          <p className="dialogo__descricao" id={idDescricao}>
            {descricao}
          </p>
        )}

        <div className="dialogo__conteudo">{children}</div>
      </div>
    </div>
  );
}
