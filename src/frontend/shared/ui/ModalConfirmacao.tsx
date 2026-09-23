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
}

/**
 * Renderiza um diálogo modal de confirmação acessível e reutilizável.
 *
 * O componente usa renderização condicional para exibir ou ocultar o overlay,
 * captura Escape e foca automaticamente no botão de cancelamento ao abrir.
 * Ele existe para oferecer uma superfície genérica de confirmação sem conhecer
 * o domínio que a utiliza.
 */
export function ModalConfirmacao({
  aberto,
  titulo,
  descricao,
  textoBotaoConfirmar = "Confirmar",
  textoBotaoCancelar = "Cancelar",
  onConfirmar,
  onCancelar
}: ModalConfirmacaoProps) {
  const refBotaoCancelar = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (aberto) {
      refBotaoCancelar.current?.focus();
    }
  }, [aberto]);

  useEffect(() => {
    if (!aberto) return;

    function lidarComTecla(evento: KeyboardEvent): void {
      if (evento.key === "Escape") {
        evento.preventDefault();
        onCancelar();
      }
    }

    document.addEventListener("keydown", lidarComTecla);
    return () => document.removeEventListener("keydown", lidarComTecla);
  }, [aberto, onCancelar]);

  if (!aberto) return null;

  return (
    <div
      aria-modal="true"
      role="dialog"
      aria-labelledby="modal-titulo"
      aria-describedby="modal-descricao"
    >
      <h2 id="modal-titulo">{titulo}</h2>
      <p id="modal-descricao">{descricao}</p>
      <div>
        <button
          onClick={onCancelar}
          ref={refBotaoCancelar}
          type="button"
        >
          {textoBotaoCancelar}
        </button>
        <button
          onClick={onConfirmar}
          type="button"
        >
          {textoBotaoConfirmar}
        </button>
      </div>
    </div>
  );
}
