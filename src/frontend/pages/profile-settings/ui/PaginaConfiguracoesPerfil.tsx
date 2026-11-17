import {
  criarClientePerfilIndisponivel,
  FormularioEdicaoPerfil,
  type ClientePerfilEstudante,
} from "../../../features/edit-profile";
import { MiniaturaModeloCurriculo } from "../../../features/alternar-modelo-curriculo";
import {
  criarClienteVersoesCurriculoDemonstracao,
  PainelCurriculosPerfil,
  type ClienteVersoesCurriculo,
} from "../../../features/gerenciar-curriculos-perfil";
import type { Student } from "../../../entities/student";
import "./PaginaConfiguracoesPerfil.css";

/** Define o cliente e os dados iniciais recebidos pela página de configurações. */
export interface PaginaConfiguracoesPerfilProps {
  cliente?: ClientePerfilEstudante;
  clienteCurriculos?: ClienteVersoesCurriculo;
  valoresIniciais?: Student;
  onCriarNovaVersao?: () => void;
  onPerfilAtualizado?: (perfil: Student) => void;
  onVoltar?: () => void;
  onVoltarInicio?: () => void;
  aoBaixarCurriculo?: (formato: "pdf" | "docx") => Promise<void> | void;
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
  clienteCurriculos = criarClienteVersoesCurriculoDemonstracao(),
  valoresIniciais = DADOS_FICTICIOS,
  onCriarNovaVersao,
  onPerfilAtualizado,
  onVoltar,
  onVoltarInicio,
  aoBaixarCurriculo,
}: PaginaConfiguracoesPerfilProps) {
  return (
    <main className="pagina-configuracoes-perfil">
      <section
        aria-labelledby="titulo-configuracoes-perfil"
        className="pagina-configuracoes-perfil__conteudo"
      >
        {(onVoltar || onVoltarInicio) && (
          <nav
            aria-label="Navegação de retorno"
            className="pagina-configuracoes-perfil__topo"
          >
            {onVoltar && (
              <button
                aria-label="Voltar para o perfil"
                className="pagina-configuracoes-perfil__voltar"
                onClick={onVoltar}
                type="button"
              >
                ← Voltar ao perfil
              </button>
            )}
            {onVoltarInicio && (
              <button
                aria-label="Voltar para a página inicial"
                className="pagina-configuracoes-perfil__btn-inicio"
                onClick={onVoltarInicio}
                type="button"
              >
                Início
              </button>
            )}
          </nav>
        )}

        <header className="pagina-configuracoes-perfil__cabecalho">
          <p className="pagina-configuracoes-perfil__sobretitulo">
            Configurações da conta
          </p>
          <h1 id="titulo-configuracoes-perfil">Perfil e modelo do currículo</h1>
          <span>
            Atualize seus dados cadastrais e gerencie o modelo de apresentação
            do seu currículo.
          </span>
        </header>

        <div className="pagina-configuracoes-perfil__grade">
          <section
            aria-labelledby="titulo-dados-perfil"
            className="pagina-configuracoes-perfil__painel"
          >
            <header className="pagina-configuracoes-perfil__cabecalho-painel">
              <h2 id="titulo-dados-perfil">Informações pessoais</h2>
              <span>
                Estes dados identificam seu perfil na plataforma e no cabeçalho
                do currículo.
              </span>
            </header>
            <FormularioEdicaoPerfil
              cliente={cliente}
              onPerfilAtualizado={onPerfilAtualizado}
              valoresIniciais={valoresIniciais}
            />
          </section>

          <div className="pagina-configuracoes-perfil__painel pagina-configuracoes-perfil__painel--versoes">
            <PainelCurriculosPerfil
              aoBaixarCurriculo={aoBaixarCurriculo}
              cliente={clienteCurriculos}
              onCriarNovaVersao={onCriarNovaVersao}
              renderizarMiniatura={(modelo) => (
                <MiniaturaModeloCurriculo modelo={modelo} />
              )}
            />
          </div>
        </div>
      </section>
    </main>
  );
}
