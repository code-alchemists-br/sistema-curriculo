import { useState, type FormEvent } from "react";

import {
  FalhaPerfilEstudante,
  type ClientePerfilEstudante,
} from "../api/cliente-perfil-estudante";
import {
  criarStudentDeValoresPerfil,
  criarValoresDeStudent,
  traduzirFalhaPerfil,
  validarPerfilEstudante,
  type ErrosPerfilEstudante,
  type ValoresPerfilEstudante,
} from "../model/formulario-perfil";
import type { Student } from "../../../entities/student";
import "./FormularioEdicaoPerfil.css";

/** Aplica máscara em formato brasileiro (11) 91234-5678 ou (11) 3333-4444. */
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

/** Define o cliente e os dados iniciais usados pela tela de configurações. */
export interface FormularioEdicaoPerfilProps {
  cliente: ClientePerfilEstudante;
  valoresIniciais: Student;
  onPerfilAtualizado?: (perfil: Student) => void;
}

/**
 * Renderiza e controla o formulário de edição do perfil do estudante.
 *
 * O componente mantém os valores no estado local e valida antes de salvar. Ele existe para
 * oferecer manutenção do perfil sem acoplar a interface a HTTP ou ao backend.
 */
export function FormularioEdicaoPerfil({
  cliente,
  valoresIniciais,
  onPerfilAtualizado,
}: FormularioEdicaoPerfilProps) {
  const [valores, setValores] = useState<ValoresPerfilEstudante>(() => {
    const dadosIniciais = criarValoresDeStudent(valoresIniciais);
    return {
      ...dadosIniciais,
      telefones: dadosIniciais.telefones.map((tel) => formatarTelefone(tel)),
    };
  });
  const [erros, setErros] = useState<ErrosPerfilEstudante>({});
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  /** Atualiza um campo simples e remove o feedback anterior daquele campo. */
  function atualizarCampo(
    campo: Exclude<keyof ValoresPerfilEstudante, "telefones">,
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

  /** Inclui um novo campo vazio para que o estudante informe outro telefone. */
  function adicionarTelefone(): void {
    setValores((atuais) => ({
      ...atuais,
      telefones: [...atuais.telefones, ""],
    }));
  }

  /** Remove um telefone adicional e reindexa os erros remanescentes. */
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
      Object.keys(atuais.telefones).forEach((chave) => {
        const indiceAtual = Number(chave);
        if (indiceAtual !== indiceRemover) {
          const erro = atuais.telefones?.[indiceAtual];
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

  /**
   * Valida e salva as alterações do perfil usando o cliente injetado.
   *
   * O envio impede o comportamento nativo, converte valores em Student e
   * chama somente o contrato injetado. Ele existe para manter a regra de
   * experiência testável enquanto a persistência real não está disponível.
   */
  async function enviarFormulario(
    evento: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    evento.preventDefault();
    const novosErros = validarPerfilEstudante(valores);

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      return;
    }

    setEnviando(true);
    setMensagem(null);

    try {
      const perfilAtualizado = criarStudentDeValoresPerfil(valores);
      await cliente.atualizar(perfilAtualizado);
      onPerfilAtualizado?.(perfilAtualizado);
      setMensagem("Perfil atualizado com sucesso.");
    } catch (erro: unknown) {
      const codigo =
        erro instanceof FalhaPerfilEstudante
          ? erro.codigo
          : "resposta-invalida";
      setMensagem(traduzirFalhaPerfil(codigo));
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form
      className="formulario-edicao-perfil"
      noValidate
      onSubmit={enviarFormulario}
    >
      <div className="formulario-edicao-perfil__linha-dupla">
        <CampoTexto
          erro={erros.nomeCompleto}
          id="perfil-nome-completo"
          label="Nome completo"
          onChange={(valor) => atualizarCampo("nomeCompleto", valor)}
          placeholder="Ex.: Ana Carolina Souza"
          required
          value={valores.nomeCompleto}
        />
        <CampoTexto
          erro={erros.email}
          id="perfil-email"
          label="E-mail"
          onChange={(valor) => atualizarCampo("email", valor)}
          placeholder="seu.email@exemplo.com"
          required
          type="email"
          value={valores.email}
        />
      </div>

      <CampoTexto
        erro={erros.enderecoCompleto}
        id="perfil-endereco-completo"
        label="Endereço completo"
        onChange={(valor) => atualizarCampo("enderecoCompleto", valor)}
        placeholder="Ex.: Rua das Flores, 123 — São Paulo, SP"
        required
        value={valores.enderecoCompleto}
      />

      <div className="formulario-edicao-perfil__telefones field">
        <div className="formulario-edicao-perfil__cabecalho-telefones">
          <span className="formulario-edicao-perfil__titulo-campo">
            Telefones de contato
          </span>
          <button
            className="formulario-edicao-perfil__adicionar-telefone"
            onClick={adicionarTelefone}
            type="button"
          >
            + Adicionar telefone
          </button>
        </div>

        <div className="formulario-edicao-perfil__lista-telefones">
          {valores.telefones.map((telefone, indice) => {
            const id = `perfil-telefone-${indice}`;
            const erro = erros.telefones?.[indice];
            const idErro = `${id}-erro`;

            return (
              <div className="formulario-edicao-perfil__item-telefone" key={id}>
                <div className="formulario-edicao-perfil__item-telefone-topo">
                  <label htmlFor={id}>Telefone {indice + 1}</label>
                  {valores.telefones.length > 1 && (
                    <button
                      aria-label={`Remover Telefone ${indice + 1}`}
                      className="formulario-edicao-perfil__remover-telefone"
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
      </div>

      <div className="formulario-edicao-perfil__secao-links">
        <span className="formulario-edicao-perfil__subtitulo-secao">
          Links profissionais e acadêmicos
        </span>
        <div className="formulario-edicao-perfil__linha-dupla">
          <CampoTexto
            erro={erros.linkedIn}
            id="perfil-linkedin"
            label="LinkedIn"
            onChange={(valor) => atualizarCampo("linkedIn", valor)}
            placeholder="https://linkedin.com/in/seuperfil"
            type="url"
            value={valores.linkedIn}
          />
          <CampoTexto
            erro={erros.curriculoLattes}
            id="perfil-curriculo-lattes"
            label="Currículo Lattes"
            onChange={(valor) => atualizarCampo("curriculoLattes", valor)}
            placeholder="http://lattes.cnpq.br/0000000000000000"
            type="url"
            value={valores.curriculoLattes}
          />
        </div>
      </div>

      {mensagem !== null && (
        <p
          className="form-message"
          role={mensagem.includes("sucesso") ? "status" : "alert"}
        >
          {mensagem}
        </p>
      )}

      <button
        className="formulario-edicao-perfil__salvar"
        disabled={enviando}
        type="submit"
      >
        {enviando ? "Salvando alterações..." : "Salvar alterações"}
      </button>
    </form>
  );
}

/** Define os valores de um campo textual do formulário. */
interface CampoTextoProps {
  erro?: string;
  id: string;
  label: string;
  onChange: (valor: string) => void;
  placeholder?: string;
  required?: boolean;
  type?: "email" | "text" | "url";
  value: string;
}

/**
 * Renderiza um campo textual com rótulo e erro associado.
 *
 * O componente usa controles HTML nativos e descrição acessível para leitores de tela.
 */
function CampoTexto({
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

  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <input
        aria-describedby={erro === undefined ? undefined : idErro}
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
