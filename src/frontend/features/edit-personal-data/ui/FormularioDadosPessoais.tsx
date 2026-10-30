import { useEffect, useRef, useState, type FormEvent } from "react";

import {
  FalhaDadosPessoais,
  type ClienteDadosPessoais,
} from "../api/cliente-dados-pessoais";
import "./FormularioDadosPessoais.css";
import {
  criarStudent,
  criarValoresIniciais,
  traduzirFalhaDadosPessoais,
  validarDadosPessoais,
  type ErrosDadosPessoais,
  type ValoresDadosPessoais,
} from "../model/formulario-dados-pessoais";

/** Aplica máscara em formato brasileiro (11) 91234-5678 ou (11) 3333-4444 */
function formatarTelefone(valor: string): string {
  const digitos = valor.replace(/\D/g, "").slice(0, 11);

  if (digitos.length <= 2) {
    return digitos.length > 0 ? `(${digitos}` : "";
  }
  if (digitos.length <= 6) {
    return `(${digitos.slice(0, 2)}) ${digitos.slice(2)}`;
  }
  if (digitos.length <= 10) {
    return `(${digitos.slice(0, 2)}) ${digitos.slice(2, 6)}-${digitos.slice(6)}`;
  }
  return `(${digitos.slice(0, 2)}) ${digitos.slice(2, 7)}-${digitos.slice(7, 11)}`;
}

/** Define o cliente usado para manter os dados pessoais do estudante. */
export interface FormularioDadosPessoaisProps {
  cliente: ClienteDadosPessoais;
  /** Notifica a porcentagem de campos preenchidos nesta etapa (0 a 100). */
  aoAlterarProgresso?: (progresso: number) => void;
  /** Callback para avançar para a próxima etapa ao salvar com sucesso. */
  aoAvancar?: () => void;
  /** Callback para retornar para a etapa anterior. */
  onVoltar?: () => void;
  /** Valores iniciais opcionais para restauração de estado. */
  valoresIniciais?: ValoresDadosPessoais;
  /** Notifica alterações nos valores para preservação de estado. */
  aoAlterarValores?: (valores: ValoresDadosPessoais) => void;
}

/** Renderiza e controla o formulário de dados pessoais e contato. */
export function FormularioDadosPessoais({
  cliente,
  aoAlterarProgresso,
  aoAvancar,
  onVoltar,
  valoresIniciais,
  aoAlterarValores,
}: FormularioDadosPessoaisProps) {
  const [valores, setValores] = useState<ValoresDadosPessoais>(
    valoresIniciais ?? criarValoresIniciais(),
  );
  const [erros, setErros] = useState<ErrosDadosPessoais>({});
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const focoNoNovoTelefone = useRef(false);

  useEffect(() => {
    aoAlterarValores?.(valores);
  }, [valores, aoAlterarValores]);

  useEffect(() => {
    if (aoAlterarProgresso) {
      let preenchidos = 0;
      const totalObrigatorios = 3;
      if (valores.nomeCompleto.trim().length > 0) preenchidos++;
      if (valores.email.trim().length > 0) preenchidos++;
      if (valores.telefones.some((t) => t.trim().length > 0)) preenchidos++;

      const porcentagem = Math.round((preenchidos / totalObrigatorios) * 100);
      aoAlterarProgresso(porcentagem);
    }
  }, [valores, aoAlterarProgresso]);

  /** Move o foco para o telefone recém-adicionado, depois que ele for renderizado. */
  function definirUltimoTelefone(elemento: HTMLInputElement | null): void {
    if (elemento !== null && focoNoNovoTelefone.current) {
      elemento.focus();
      focoNoNovoTelefone.current = false;
    }
  }

  /** Atualiza um campo simples e remove o feedback anterior daquele campo. */
  function atualizarCampo(
    campo: Exclude<keyof ValoresDadosPessoais, "telefones">,
    valor: string,
  ): void {
    setValores((atuais) => ({ ...atuais, [campo]: valor }));
    setErros((atuais) => ({ ...atuais, [campo]: undefined }));
    setMensagem(null);
  }

  /** Atualiza um telefone específico e remove somente seu erro associado. */
  function atualizarTelefone(indice: number, telefone: string): void {
    setValores((atuais) => ({
      ...atuais,
      telefones: atuais.telefones.map((valor, indiceAtual) =>
        indiceAtual === indice ? telefone : valor,
      ),
    }));
    setErros((atuais) => {
      const errosDeTelefone = { ...atuais.telefones };
      delete errosDeTelefone[indice];

      return {
        ...atuais,
        telefones:
          Object.keys(errosDeTelefone).length === 0
            ? undefined
            : errosDeTelefone,
      };
    });
    setMensagem(null);
  }

  /** Inclui um novo telefone e sinaliza que ele deve receber foco. */
  function adicionarTelefone(): void {
    focoNoNovoTelefone.current = true;
    setValores((atuais) => ({
      ...atuais,
      telefones: [...atuais.telefones, ""],
    }));
  }

  /** Remove um telefone adicional e reordena os erros restantes. */
  function removerTelefone(indiceRemover: number): void {
    if (valores.telefones.length <= 1) return;

    setValores((atuais) => ({
      ...atuais,
      telefones: atuais.telefones.filter(
        (_, indice) => indice !== indiceRemover,
      ),
    }));

    setErros((atuais) => {
      if (!atuais.telefones) return atuais;

      const novosErrosDeTelefone: Record<number, string> = {};
      let novoIndice = 0;
      Object.keys(atuais.telefones).forEach((key) => {
        const indiceNum = Number(key);
        if (indiceNum !== indiceRemover) {
          const erro = atuais.telefones?.[indiceNum];
          if (erro) {
            novosErrosDeTelefone[novoIndice] = erro;
          }
          novoIndice++;
        }
      });

      return {
        ...atuais,
        telefones:
          Object.keys(novosErrosDeTelefone).length === 0
            ? undefined
            : novosErrosDeTelefone,
      };
    });

    setMensagem(null);
  }

  /** Valida e salva os dados, preservando os valores para uma tentativa posterior em caso de falha. */
  async function enviarFormulario(
    evento: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    evento.preventDefault();
    const novosErros = validarDadosPessoais(valores);

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      return;
    }

    setEnviando(true);
    setMensagem(null);

    try {
      await cliente.salvar(criarStudent(valores));
      setMensagem("Dados pessoais salvos com sucesso.");
      aoAvancar?.();
    } catch (erro: unknown) {
      const codigo =
        erro instanceof FalhaDadosPessoais ? erro.codigo : "resposta-invalida";
      setMensagem(traduzirFalhaDadosPessoais(codigo));
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form
      aria-busy={enviando}
      className="formulario-dados-pessoais"
      noValidate
      onSubmit={enviarFormulario}
    >
      {/* 1. Nome Completo */}
      <CampoTexto
        erro={erros.nomeCompleto}
        id="nome-completo"
        label="Nome Completo"
        onChange={(valor) => atualizarCampo("nomeCompleto", valor)}
        placeholder="Ex.: Carlos Eduardo da Silva"
        required
        value={valores.nomeCompleto}
      />

      {/* 2. E-mail */}
      <CampoTexto
        erro={erros.email}
        id="email"
        label="E-mail"
        onChange={(valor) => atualizarCampo("email", valor)}
        placeholder="seu.email@exemplo.com"
        required
        type="email"
        value={valores.email}
      />

      {/* 3. Telefone */}
      <div className="field">
        <span className="titulo-campo titulo-campo--obrigatorio">Telefone</span>

        <div
          className={`lista-telefones ${valores.telefones.length > 1 ? "lista-telefones--multipla" : ""}`}
        >
          {valores.telefones.map((telefone, indice) => {
            const id = `telefone-${indice}`;
            const erro = erros.telefones?.[indice];
            const idErro = `${id}-erro`;
            const eUltimoTelefone = indice === valores.telefones.length - 1;

            return (
              <div key={id} className="item-telefone">
                <div className="item-telefone__topo">
                  <label htmlFor={id} className="label-subtitulo">
                    Telefone {indice + 1}
                  </label>
                  {valores.telefones.length > 1 && (
                    <button
                      aria-label={`Remover Telefone ${indice + 1}`}
                      className="btn-remover-telefone"
                      onClick={() => removerTelefone(indice)}
                      type="button"
                    >
                      Remover
                    </button>
                  )}
                </div>

                <input
                  aria-describedby={erro === undefined ? undefined : idErro}
                  aria-invalid={erro === undefined ? undefined : true}
                  autoComplete="tel"
                  id={id}
                  onChange={(evento) =>
                    atualizarTelefone(
                      indice,
                      formatarTelefone(evento.target.value),
                    )
                  }
                  placeholder="(11) 91234-5678"
                  ref={eUltimoTelefone ? definirUltimoTelefone : undefined}
                  required
                  type="tel"
                  value={telefone}
                />
                {erro !== undefined && (
                  <p className="field__error" id={idErro}>
                    {erro}
                  </p>
                )}
              </div>
            );
          })}
        </div>

        <button
          className="btn-adicionar-telefone"
          onClick={adicionarTelefone}
          type="button"
        >
          + Adicionar telefone
        </button>
      </div>

      {/* 4. Endereço */}
      <CampoTexto
        erro={erros.enderecoCompleto}
        id="endereco-completo"
        label="Endereço"
        onChange={(valor) => atualizarCampo("enderecoCompleto", valor)}
        placeholder="Cidade, Estado (ou endereço completo)..."
        value={valores.enderecoCompleto}
      />

      {/* 5. Linkedin */}
      <CampoTexto
        id="linkedin"
        label="Linkedin"
        onChange={(valor) => atualizarCampo("linkedIn", valor)}
        placeholder="https://linkedin.com/in/seuperfil"
        type="url"
        value={valores.linkedIn}
      />

      {enviando && <p role="status">Salvando dados pessoais...</p>}
      {mensagem !== null && (
        <p
          className="form-message"
          role={mensagem.includes("sucesso") ? "status" : "alert"}
        >
          {mensagem}
        </p>
      )}

      <div className="botoes-navegacao">
        {onVoltar && (
          <button
            type="button"
            className="btn-voltar"
            onClick={onVoltar}
            aria-label="Voltar para a etapa anterior"
          >
            Voltar
          </button>
        )}
        <button
          aria-label={enviando ? "Salvando dados..." : "Salvar dados pessoais"}
          className="btn-proximo"
          disabled={enviando}
          type="submit"
        >
          {enviando ? "Salvando..." : "Próximo"}
        </button>
      </div>
    </form>
  );
}

/** Define os valores de um campo textual do formulário. */
interface CampoTextoProps {
  ajuda?: string;
  erro?: string;
  id: string;
  label: string;
  onChange: (valor: string) => void;
  placeholder?: string;
  required?: boolean;
  type?: "email" | "text" | "url";
  value: string;
}

/** Renderiza um campo textual, incluindo ajuda e feedback de erro acessíveis. */
function CampoTexto({
  ajuda,
  erro,
  id,
  label,
  onChange,
  placeholder,
  required = false,
  type = "text",
  value,
}: CampoTextoProps) {
  const idErro = `${id}-erro`;
  const idAjuda = `${id}-ajuda`;

  const idsDescricao: string[] = [];
  if (erro !== undefined) {
    idsDescricao.push(idErro);
  }
  if (ajuda !== undefined) {
    idsDescricao.push(idAjuda);
  }
  const ariaDescribedBy =
    idsDescricao.length > 0 ? idsDescricao.join(" ") : undefined;

  return (
    <div className="field">
      <label
        htmlFor={id}
        className={`titulo-campo ${required ? "titulo-campo--obrigatorio" : ""}`}
      >
        {label}
      </label>
      {ajuda !== undefined && (
        <span className="field__help" id={idAjuda}>
          {ajuda}
        </span>
      )}
      <input
        aria-describedby={ariaDescribedBy}
        aria-invalid={erro === undefined ? undefined : true}
        id={id}
        onChange={(evento) => onChange(evento.target.value)}
        placeholder={placeholder}
        required={required}
        type={type}
        value={value}
      />
      {erro !== undefined && (
        <p className="field__error" id={idErro}>
          {erro}
        </p>
      )}
    </div>
  );
}
