// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001
import { useState } from "react";

import {
  criarClienteAcessoEstudante,
  FormularioAcesso,
  FormularioCadastro,
  type ClienteAcessoEstudante
} from "../../../features/acesso-estudante";

/** Define o colaborador da página para permitir composição e testes isolados. */
export interface PaginaAcessoEstudanteProps {
  cliente?: ClienteAcessoEstudante;
}

/**
 * Compõe a porta de entrada que alterna entre cadastro e acesso do estudante.
 *
 * A página mantém somente a aba ativa e o e-mail que o cadastro devolve, usando
 * formulários de feature através de sua API pública. Ela existe para unir os
 * dois fluxos de conta sem criar navegação autenticada ainda não definida.
 */
export function PaginaAcessoEstudante({ cliente }: PaginaAcessoEstudanteProps) {
  const [abaAtiva, setAbaAtiva] = useState<"acesso" | "cadastro">("acesso");
  const [emailCadastrado, setEmailCadastrado] = useState("");
  const clienteDaPagina = cliente ?? criarClienteAcessoEstudante();

  /** Troca a aba visível preservando dados controlados por cada formulário. */
  function selecionarAba(aba: "acesso" | "cadastro"): void {
    setAbaAtiva(aba);
  }

  /** Preenche o próximo acesso com o e-mail cadastrado e nunca retém a senha. */
  function concluirCadastro(email: string): void {
    setEmailCadastrado(email);
    setAbaAtiva("acesso");
  }

  return (
    <main className="app-shell">
      <section aria-labelledby="titulo-acesso" className="app-shell__content">
        <p className="eyebrow">Sistema Currículo</p>
        <h1 id="titulo-acesso">Acesse sua conta</h1>
        <p>Crie sua conta ou confirme suas credenciais para iniciar sua jornada.</p>
        <div aria-label="Escolha o fluxo de conta" className="tabs" role="tablist">
          <button
            aria-selected={abaAtiva === "acesso"}
            className="tabs__button"
            onClick={() => selecionarAba("acesso")}
            role="tab"
            type="button"
          >
            Entrar
          </button>
          <button
            aria-selected={abaAtiva === "cadastro"}
            className="tabs__button"
            onClick={() => selecionarAba("cadastro")}
            role="tab"
            type="button"
          >
            Criar conta
          </button>
        </div>
        <section aria-label={abaAtiva === "acesso" ? "Formulário de acesso" : "Formulário de cadastro"} className="account-form">
          {abaAtiva === "acesso" ? (
            <FormularioAcesso cliente={clienteDaPagina} emailInicial={emailCadastrado} />
          ) : (
            <FormularioCadastro aoCadastrar={concluirCadastro} cliente={clienteDaPagina} />
          )}
        </section>
      </section>
    </main>
  );
}
