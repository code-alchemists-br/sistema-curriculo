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
}: PaginaConfiguracoesPerfilProps) {
  return (
    <main className="pagina-configuracoes-perfil">
      <section
        aria-labelledby="titulo-configuracoes-perfil"
        className="pagina-configuracoes-perfil__conteudo"
      >
        {onVoltar && (
          <button
            aria-label="Voltar para a página inicial"
            className="pagina-configuracoes-perfil__voltar"
            onClick={onVoltar}
            type="button"
          >
            ← Voltar para o início
          </button>
        )}
        <header className="pagina-configuracoes-perfil__cabecalho">
          <p>Configurações</p>
          <h1 id="titulo-configuracoes-perfil">Seu perfil e seus currículos</h1>
          <span>
            Mantenha seus dados de contato atualizados e organize as versões de
            currículo que você já criou.
          </span>
        </header>
        <div className="pagina-configuracoes-perfil__grade">
          <section
            aria-labelledby="titulo-dados-perfil"
            className="pagina-configuracoes-perfil__painel"
          >
            <header className="pagina-configuracoes-perfil__cabecalho-painel">
              <p>Dados do perfil</p>
              <h2 id="titulo-dados-perfil">Informações pessoais</h2>
              <span>
                Atualize endereço, telefone, e-mail e links profissionais.
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
