import { useEffect, useRef } from "react";

/** Define as propriedades do modal genérico de confirmação. */
export interface ModalConfirmacaoProps {
  aberto: boolean;
  titulo: string;
  descricao: string;
  textoBotaoConfirmar?: string;
  textoBotaoCancelar?: string;
  onConfirmar: () => void;
  onCancelar: () => void;
  /** Elemento opcional que disparou a abertura; se omitido, captura o activeElement. */
  elementoDisparador?: HTMLElement | null;
}

/**
 * Renderiza um diálogo modal de confirmação acessível e reutilizável.
 *
 * **O que faz:** Exibe um diálogo modal com semântica ARIA, contenção de foco e retorno automático ao elemento disparador.
 * **Como faz:** Captura o elemento ativo no momento da abertura e restaura seu foco no fechamento ou desmontagem;
 * intercepta a tecla Tab para manter o foco contido dentro do modal (focus trap); e fecha via tecla Escape.
 * **Qual finalidade atende:** Garante plena conformidade com WCAG 2.1 (Critérios 2.1.2 Sem Armadilha de Teclado
 * e 2.4.3 Ordem do Foco) e o WAI-ARIA Modal Dialog Pattern.
 */
export function ModalConfirmacao({
  aberto,
  titulo,
  descricao,
  textoBotaoConfirmar = "Confirmar",
  textoBotaoCancelar = "Cancelar",
  onConfirmar,
  onCancelar,
  elementoDisparador,
}: ModalConfirmacaoProps) {
  const refBotaoCancelar = useRef<HTMLButtonElement>(null);
  const refBotaoConfirmar = useRef<HTMLButtonElement>(null);
  const refDisparador = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (aberto) {
      refDisparador.current =
        elementoDisparador ?? (document.activeElement as HTMLElement | null);
      refBotaoCancelar.current?.focus();
    } else if (refDisparador.current) {
      refDisparador.current.focus();
      refDisparador.current = null;
    }
  }, [aberto, elementoDisparador]);

  useEffect(() => {
    return () => {
      refDisparador.current?.focus();
    };
  }, []);

  useEffect(() => {
    if (!aberto) return;

    function lidarComTecla(evento: KeyboardEvent): void {
      if (evento.key === "Escape") {
        evento.preventDefault();
        onCancelar();
        return;
      }

      if (evento.key === "Tab") {
        const botoes = [
          refBotaoCancelar.current,
          refBotaoConfirmar.current,
        ].filter((b): b is HTMLButtonElement => b !== null);

        if (botoes.length === 0) return;

        const primeiro = botoes[0];
        const ultimo = botoes[botoes.length - 1];

        if (evento.shiftKey) {
          if (document.activeElement === primeiro) {
            evento.preventDefault();
            ultimo.focus();
          }
        } else {
          if (document.activeElement === ultimo) {
            evento.preventDefault();
            primeiro.focus();
          }
        }
      }
    }

    document.addEventListener("keydown", lidarComTecla);
    return () => document.removeEventListener("keydown", lidarComTecla);
  }, [aberto, onCancelar]);

  if (!aberto) return null;

  return (
    <div
      aria-describedby="modal-descricao"
      aria-labelledby="modal-titulo"
      aria-modal="true"
      role="dialog"
    >
      <h2 id="modal-titulo">{titulo}</h2>
      <p id="modal-descricao">{descricao}</p>
      <div>
        <button onClick={onCancelar} ref={refBotaoCancelar} type="button">
          {textoBotaoCancelar}
        </button>
        <button onClick={onConfirmar} ref={refBotaoConfirmar} type="button">
          {textoBotaoConfirmar}
        </button>
      </div>
    </div>
  );
}
