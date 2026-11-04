import {
  criarClientePerfilIndisponivel,
  FormularioEdicaoPerfil,
  type ClientePerfilEstudante,
} from "../../../features/edit-profile";
import type { Student } from "../../../entities/student";

/** Define o cliente e os dados iniciais recebidos pela página de configurações. */
export interface PaginaConfiguracoesPerfilProps {
  cliente?: ClientePerfilEstudante;
  valoresIniciais?: Student;
  onVoltar?: () => void;
}

const DADOS_FICTICIOS: Student = {
  nomeCompleto: "Estudante Exemplo",
  enderecoCompleto: "Rua Exemplo, 123",
  telefones: ["(11) 90000-0000"],
  email: "estudante@exemplo.com",
};

/**
 * Compõe a página de configurações do perfil do estudante.
 *
 * A página fornece contexto e entrega a interação para a feature por sua API
 * pública. Ela existe para manter a composição de página separada das regras
 * de formulário, sem decidir roteamento ou persistência ainda indisponíveis.
 */
export function PaginaConfiguracoesPerfil({
  cliente = criarClientePerfilIndisponivel(),
  valoresIniciais = DADOS_FICTICIOS,
  onVoltar,
}: PaginaConfiguracoesPerfilProps) {
  return (
    <main className="app-shell">
      <section
        aria-labelledby="titulo-configuracoes-perfil"
        className="app-shell__content"
      >
        {onVoltar && (
          <div style={{ marginBottom: "1rem" }}>
            <button
              type="button"
              className="btn-voltar"
              onClick={onVoltar}
              aria-label="Voltar para a página inicial"
            >
              ← Voltar para o início
            </button>
          </div>
        )}
        <p className="eyebrow">Configurações</p>
        <h1 id="titulo-configuracoes-perfil">Editar perfil</h1>
        <p>Atualize seus dados pessoais ou exclua sua conta permanentemente.</p>
        <FormularioEdicaoPerfil
          cliente={cliente}
          valoresIniciais={valoresIniciais}
        />
      </section>
    </main>
  );
}
