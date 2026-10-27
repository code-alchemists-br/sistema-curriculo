// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001
import { useState } from "react";

import {
  criarClienteAcessoEstudante,
  FormularioAcesso,
  FormularioCadastro,
  type ClienteAcessoEstudante,
} from "../../../features/acesso-estudante";
import gradienteLogin from "../../../shared/assets/images/gradiente_login.webp";
import "./PaginaAcessoEstudante.css";

/** Define o colaborador da página para permitir composição e testes isolados. */
export interface PaginaAcessoEstudanteProps {
  cliente?: ClienteAcessoEstudante;
  onVoltarInicio?: () => void;
  abaInicial?: "acesso" | "cadastro";
}

/**
 * Compõe a porta de entrada que alterna entre cadastro e acesso do estudante.
 *
 * A página mantém somente a aba ativa e o e-mail que o cadastro devolve, usando
 * formulários de feature através de sua API pública. Ela existe para unir os
 * dois fluxos de conta sem criar navegação autenticada ainda não definida.
 */
export function PaginaAcessoEstudante({
  cliente,
  onVoltarInicio,
  abaInicial = "acesso",
}: PaginaAcessoEstudanteProps) {
  const [abaAtiva, setAbaAtiva] = useState<"acesso" | "cadastro">(abaInicial);
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
    <main className="pagina-acesso-estudante app-shell">
      <img
        alt=""
        aria-hidden="true"
        className="pagina-acesso-estudante__glow"
        src={gradienteLogin}
      />
      <div className="pagina-acesso-estudante__container">
        {onVoltarInicio && (
          <button
            className="pagina-acesso-estudante__voltar"
            onClick={onVoltarInicio}
            type="button"
          >
            ← Voltar para o início
          </button>
        )}
        <section
          aria-labelledby="titulo-acesso"
          className="pagina-acesso-estudante__card app-shell__content"
        >
          <span className="pagina-acesso-estudante__eyebrow eyebrow">
            LIMINAL
          </span>
          <h1 className="pagina-acesso-estudante__titulo" id="titulo-acesso">
            {abaAtiva === "acesso"
              ? "Conecte-se na LIMINAL"
              : "Crie uma nova conta"}
          </h1>
          <section
            aria-label={
              abaAtiva === "acesso"
                ? "Formulário de acesso"
                : "Formulário de cadastro"
            }
            className="pagina-acesso-estudante__formulario-wrapper account-form"
          >
            {abaAtiva === "acesso" ? (
              <FormularioAcesso
                cliente={clienteDaPagina}
                emailInicial={emailCadastrado}
              />
            ) : (
              <FormularioCadastro
                aoCadastrar={concluirCadastro}
                cliente={clienteDaPagina}
              />
            )}
          </section>
        </section>

        <footer className="pagina-acesso-estudante__alternador">
          {abaAtiva === "acesso" ? (
            <p className="pagina-acesso-estudante__alternador-texto">
              Não tem uma conta?{" "}
              <button
                className="pagina-acesso-estudante__alternador-botao"
                onClick={() => selecionarAba("cadastro")}
                type="button"
              >
                Criar conta
              </button>
            </p>
          ) : (
            <p className="pagina-acesso-estudante__alternador-texto">
              Já tem uma conta?{" "}
              <button
                className="pagina-acesso-estudante__alternador-botao"
                onClick={() => selecionarAba("acesso")}
                type="button"
              >
                Entrar
              </button>
            </p>
          )}
        </footer>
      </div>
    </main>
  );
}
