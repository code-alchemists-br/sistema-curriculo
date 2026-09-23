import { useState, type FormEvent } from "react";

import { ModalConfirmacao } from "../../../shared";
import {
  FalhaPerfilEstudante,
  type ClientePerfilEstudante
} from "../api/cliente-perfil-estudante";
import {
  criarStudentDeValoresPerfil,
  criarValoresDeStudent,
  traduzirFalhaPerfil,
  validarPerfilEstudante,
  type ErrosPerfilEstudante,
  type ValoresPerfilEstudante
} from "../model/formulario-perfil";
import type { Student } from "../../../entities/student";

/** Define o cliente e os dados iniciais usados pela tela de configurações. */
export interface FormularioEdicaoPerfilProps {
  cliente: ClientePerfilEstudante;
  valoresIniciais: Student;
}

/**
 * Renderiza e controla o formulário de edição e exclusão do perfil.
 *
 * O componente mantém os valores no estado local, valida antes de salvar, e
 * exige confirmação explícita via modal para excluir a conta. Ele existe para
 * oferecer manutenção do perfil sem acoplar a interface a HTTP ou ao backend.
 */
export function FormularioEdicaoPerfil({ cliente, valoresIniciais }: FormularioEdicaoPerfilProps) {
  const [valores, setValores] = useState<ValoresPerfilEstudante>(() =>
    criarValoresDeStudent(valoresIniciais)
  );
  const [erros, setErros] = useState<ErrosPerfilEstudante>({});
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [excluindo, setExcluindo] = useState(false);
  const [modalAberto, setModalAberto] = useState(false);

  /** Atualiza um campo simples e remove o feedback anterior daquele campo. */
  function atualizarCampo(campo: Exclude<keyof ValoresPerfilEstudante, "telefones">, valor: string): void {
    setValores((atuais) => ({ ...atuais, [campo]: valor }));
    setErros((atuais) => ({ ...atuais, [campo]: undefined }));
    setMensagem(null);
  }

  /** Atualiza um telefone específico e remove somente seu erro associado. */
  function atualizarTelefone(indice: number, telefone: string): void {
    setValores((atuais) => ({
      ...atuais,
      telefones: atuais.telefones.map((valor, indiceAtual) => (indiceAtual === indice ? telefone : valor))
    }));
    setErros((atuais) => {
      const errosDeTelefone = { ...atuais.telefones };
      delete errosDeTelefone[indice];

      return {
        ...atuais,
        telefones: Object.keys(errosDeTelefone).length === 0 ? undefined : errosDeTelefone
      };
    });
    setMensagem(null);
  }

  /** Inclui um novo campo vazio para que o estudante informe outro telefone. */
  function adicionarTelefone(): void {
    setValores((atuais) => ({ ...atuais, telefones: [...atuais.telefones, ""] }));
  }

  /**
   * Valida e salva as alterações do perfil usando o cliente injetado.
   *
   * O envio impede o comportamento nativo, converte valores em Student e
   * chama somente o contrato injetado. Ele existe para manter a regra de
   * experiência testável enquanto a persistência real não está disponível.
   */
  async function enviarFormulario(evento: FormEvent<HTMLFormElement>): Promise<void> {
    evento.preventDefault();
    const novosErros = validarPerfilEstudante(valores);

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      return;
    }

    setEnviando(true);
    setMensagem(null);

    try {
      await cliente.atualizar(criarStudentDeValoresPerfil(valores));
      setMensagem("Perfil atualizado com sucesso.");
    } catch (erro: unknown) {
      const codigo = erro instanceof FalhaPerfilEstudante ? erro.codigo : "resposta-invalida";
      setMensagem(traduzirFalhaPerfil(codigo));
    } finally {
      setEnviando(false);
    }
  }

  /**
   * Confirma a exclusão da conta após o modal ter sido aceito pelo estudante.
   *
   * A função fecha o modal, entra em estado de carregamento e chama o cliente.
   * Ela existe para garantir que a exclusão só aconteça após confirmação
   * explícita e para comunicar o resultado de forma clara.
   */
  async function confirmarExclusao(): Promise<void> {
    setModalAberto(false);
    setExcluindo(true);
    setMensagem(null);

    try {
      await cliente.excluir();
      setMensagem("Sua conta foi excluída com sucesso.");
    } catch (erro: unknown) {
      const codigo = erro instanceof FalhaPerfilEstudante ? erro.codigo : "resposta-invalida";
      setMensagem(traduzirFalhaPerfil(codigo));
    } finally {
      setExcluindo(false);
    }
  }

  return (
    <>
      <form noValidate onSubmit={enviarFormulario}>
        <CampoTexto
          erro={erros.nomeCompleto}
          id="perfil-nome-completo"
          label="Nome completo"
          onChange={(valor) => atualizarCampo("nomeCompleto", valor)}
          required
          value={valores.nomeCompleto}
        />
        <CampoTexto
          erro={erros.enderecoCompleto}
          id="perfil-endereco-completo"
          label="Endereço completo"
          onChange={(valor) => atualizarCampo("enderecoCompleto", valor)}
          required
          value={valores.enderecoCompleto}
        />
        <div className="field">
          <span>Telefones</span>
          {valores.telefones.map((telefone, indice) => {
            const id = `perfil-telefone-${indice}`;
            const erro = erros.telefones?.[indice];
            const idErro = `${id}-erro`;

            return (
              <div key={id}>
                <label htmlFor={id}>Telefone {indice + 1}</label>
                <input
                  aria-describedby={erro === undefined ? undefined : idErro}
                  aria-invalid={erro === undefined ? undefined : true}
                  autoComplete="tel"
                  id={id}
                  onChange={(evento) => atualizarTelefone(indice, evento.target.value)}
                  required
                  type="tel"
                  value={telefone}
                />
                {erro !== undefined && <p className="field__error" id={idErro}>{erro}</p>}
              </div>
            );
          })}
          <button onClick={adicionarTelefone} type="button">+ Adicionar telefone</button>
        </div>
        <CampoTexto
          erro={erros.email}
          id="perfil-email"
          label="E-mail"
          onChange={(valor) => atualizarCampo("email", valor)}
          required
          type="email"
          value={valores.email}
        />
        <CampoTexto
          ajuda="Informe o endereço público do seu perfil profissional, se possuir um."
          id="perfil-linkedin"
          label="LinkedIn (opcional)"
          onChange={(valor) => atualizarCampo("linkedIn", valor)}
          type="url"
          value={valores.linkedIn}
        />
        <CampoTexto
          ajuda="Informe o endereço público do seu currículo na Plataforma Lattes, se possuir um."
          id="perfil-curriculo-lattes"
          label="Currículo Lattes (opcional)"
          onChange={(valor) => atualizarCampo("curriculoLattes", valor)}
          type="url"
          value={valores.curriculoLattes}
        />
        {mensagem !== null && (
          <p className="form-message" role={mensagem.includes("sucesso") ? "status" : "alert"}>
            {mensagem}
          </p>
        )}
        <button disabled={enviando || excluindo} type="submit">
          {enviando ? "Salvando alterações..." : "Salvar alterações"}
        </button>
      </form>
      <button
        disabled={enviando || excluindo}
        onClick={() => setModalAberto(true)}
        type="button"
      >
        {excluindo ? "Excluindo conta..." : "Excluir minha conta"}
      </button>
      <ModalConfirmacao
        aberto={modalAberto}
        descricao="Todos os seus dados e currículos serão perdidos permanentemente. Esta ação não pode ser desfeita."
        onCancelar={() => setModalAberto(false)}
        onConfirmar={confirmarExclusao}
        textoBotaoCancelar="Cancelar"
        textoBotaoConfirmar="Excluir minha conta"
        titulo="Tem certeza que deseja excluir sua conta?"
      />
    </>
  );
}

/** Define os valores de um campo textual do formulário. */
interface CampoTextoProps {
  ajuda?: string;
  erro?: string;
  id: string;
  label: string;
  onChange: (valor: string) => void;
  required?: boolean;
  type?: "email" | "text" | "url";
  value: string;
}

/**
 * Renderiza um campo com rótulo, tooltip explicativo opcional e erro associado.
 *
 * O componente usa controles HTML nativos, um título exibido ao passar o mouse
 * e descrição acessível para leitores de tela. Ele existe para manter a
 * semântica e a apresentação dos campos consistentes dentro desta feature.
 */
function CampoTexto({ ajuda, erro, id, label, onChange, required = false, type = "text", value }: CampoTextoProps) {
  const idErro = `${id}-erro`;
  const idAjuda = `${id}-ajuda`;

  return (
    <div className="field">
      <label htmlFor={id}>
        {label}
        {ajuda !== undefined && (
          <span aria-describedby={idAjuda} aria-label={`Ajuda: ${ajuda}`} title={ajuda}> ?</span>
        )}
      </label>
      {ajuda !== undefined && <span hidden id={idAjuda}>{ajuda}</span>}
      <input
        aria-describedby={erro === undefined ? undefined : idErro}
        aria-invalid={erro === undefined ? undefined : true}
        id={id}
        onChange={(evento) => onChange(evento.target.value)}
        required={required}
        type={type}
        value={value}
      />
      {erro !== undefined && <p className="field__error" id={idErro}>{erro}</p>}
    </div>
  );
}
