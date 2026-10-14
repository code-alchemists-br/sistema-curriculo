import type { ReactNode } from "react";

/**
 * Propriedades para configuração do componente de campo de formulário acessível.
 */
export interface CampoFormularioProps {
  /** Identificador único do elemento de entrada no DOM. */
  id: string;
  /** Rótulo textual apresentado ao usuário. */
  rotulo?: string;
  /** Rótulo alternativo para compatibilidade. */
  label?: string;
  /** Valor atual controlado do campo. */
  valor?: string;
  /** Callback acionado ao alterar o valor digitado. */
  onChange?: (valor: string) => void;
  /** Tipo HTML do input (ex.: 'text', 'email', 'tel', 'password'). Padrão: 'text'. */
  tipo?: string;
  /** Mensagem de erro de validação associada ao campo. */
  erro?: string;
  /** Mensagem ou instrução de apoio opcional. */
  ajuda?: string;
  /** Indica se o preenchimento do campo é obrigatório. */
  obrigatorio?: boolean;
  /** Indica se o campo está desabilitado para interação. */
  desabilitado?: boolean;
  /** Texto provisório de orientação no interior do campo. */
  placeholder?: string;
  /** Sugestão de preenchimento automático do navegador. */
  autoComplete?: string;
  /** Classe CSS customizada opcional para o contêiner. */
  className?: string;
  /** Elemento customizado alternativo para renderização interna (ex.: select ou textarea). */
  children?: ReactNode;
}

/**
 * Renderiza um campo de formulário acessível com rótulo, mensagem de erro e vínculos ARIA.
 *
 * **O que faz:** Estrutura visualmente e semanticamente um campo de formulário, seu rótulo e eventuais erros.
 * **Como faz:** Associa o rótulo ao campo via `htmlFor={id}`, vincula o parágrafo de erro dinamicamente
 * via `aria-describedby` e `aria-invalid="true"`, e exibe o texto de validação em um container com classe `field__error`.
 * **Qual finalidade atende:** Elimina a duplicação de lógica de acessibilidade (WCAG) nos formulários da aplicação,
 * centralizando a conformidade com as diretrizes do projeto na camada shared.
 */
export function CampoFormulario({
  id,
  rotulo,
  label,
  valor = "",
  onChange,
  tipo = "text",
  erro,
  ajuda,
  obrigatorio = false,
  desabilitado = false,
  placeholder,
  autoComplete,
  className = "field",
  children,
}: CampoFormularioProps) {
  const textoRotulo = rotulo ?? label ?? "";
  const idErro = `${id}-erro`;
  const idAjuda = `${id}-ajuda`;

  const idsDescricao: string[] = [];
  if (erro !== undefined && erro.trim() !== "") {
    idsDescricao.push(idErro);
  }
  if (ajuda !== undefined && ajuda.trim() !== "") {
    idsDescricao.push(idAjuda);
  }

  const ariaDescribedBy =
    idsDescricao.length > 0 ? idsDescricao.join(" ") : undefined;
  const possuiErro = erro !== undefined && erro.trim() !== "";

  return (
    <div className={className}>
      {textoRotulo && (
        <label htmlFor={id}>
          {textoRotulo}
          {ajuda !== undefined && ajuda.trim() !== "" && (
            <span
              aria-describedby={idAjuda}
              aria-label={`Ajuda: ${ajuda}`}
              title={ajuda}
            >
              {" "}
              ?
            </span>
          )}
        </label>
      )}

      {ajuda !== undefined && ajuda.trim() !== "" && (
        <span hidden id={idAjuda}>
          {ajuda}
        </span>
      )}

      {children ?? (
        <input
          aria-describedby={ariaDescribedBy}
          aria-invalid={possuiErro ? true : undefined}
          autoComplete={autoComplete}
          disabled={desabilitado}
          id={id}
          onChange={(evento) => onChange?.(evento.target.value)}
          placeholder={placeholder}
          required={obrigatorio}
          type={tipo}
          value={valor}
        />
      )}

      {possuiErro && (
        <p className="field__error" id={idErro}>
          {erro}
        </p>
      )}
    </div>
  );
}
