import {
  criarClienteRecuperacaoSenhaIndisponivel,
  FormularioRecuperacaoSenha,
  type ClienteRecuperacaoSenha,
} from "../../../features/recuperar-senha";

/** Define a dependência opcional usada pela página de recuperação de senha. */
export interface PaginaRecuperacaoSenhaProps {
  cliente?: ClienteRecuperacaoSenha;
}

/**
 * Compõe a tela independente de recuperação de senha.
 *
 * A página usa a API pública da feature e fornece um cliente indisponível como
 * fallback enquanto não há backend integrado. Ela existe para preservar a
 * composição FSD sem inventar rota, sessão ou envio de e-mail em produção.
 */
export function PaginaRecuperacaoSenha({
  cliente,
}: PaginaRecuperacaoSenhaProps) {
  return (
    <main className="app-shell">
      <section
        aria-labelledby="titulo-recuperacao"
        className="app-shell__content"
      >
        <p className="eyebrow">Sistema Currículo</p>
        <h1 id="titulo-recuperacao">Recupere sua senha</h1>
        <FormularioRecuperacaoSenha
          cliente={cliente ?? criarClienteRecuperacaoSenhaIndisponivel()}
        />
      </section>
    </main>
  );
}
