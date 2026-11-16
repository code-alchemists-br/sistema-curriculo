import type { PreviaCurriculo } from "../../../entities/curriculo";
import {
  CurriculoNoModelo,
  ROTULOS_MODELO_CURRICULO,
} from "../../../features/visualizar-curriculo";
import "./PaginaMeuPerfil.css";

/** Dados e ações recebidos pela página de perfil. */
export interface PaginaMeuPerfilProps {
  /** Currículo atual do estudante, montado com os dados das etapas. */
  previa: PreviaCurriculo;
  /** Chave do modelo visual escolhido para o currículo. */
  modelo: string;
  /** Indica se o estudante já preencheu alguma parte do currículo. */
  possuiCurriculo: boolean;
  onEditarPerfil: () => void;
  onEditarCurriculo: () => void;
  onVoltarInicio: () => void;
}

/** Iniciais do nome para o avatar (ex.: "Ana Teste Fluxo" → "AF"). */
function iniciais(nome: string): string {
  const partes = nome.trim().split(/\s+/).filter(Boolean);
  if (partes.length === 0) return "?";
  const primeira = partes[0][0];
  const ultima = partes.length > 1 ? partes[partes.length - 1][0] : "";
  return (primeira + ultima).toUpperCase();
}

/** Um item da lista de dados do perfil; não aparece quando está vazio. */
function Dado({ rotulo, valor }: { rotulo: string; valor?: string | null }) {
  if (!valor || !valor.trim()) return null;
  return (
    <div className="pagina-meu-perfil__dado">
      <dt>{rotulo}</dt>
      <dd>{valor}</dd>
    </div>
  );
}

/**
 * Mostra o perfil do estudante só para leitura, ao lado do currículo atual.
 *
 * - O que faz: à esquerda, os dados pessoais e um resumo do que já foi
 *   preenchido; à direita, o currículo no modelo escolhido; no topo, os botões
 *   para editar o perfil ou o currículo.
 * - Como faz: lê tudo da mesma prévia usada na visualização do currículo, sem
 *   chamadas HTTP e sem campos editáveis; as edições são delegadas por callback.
 * - Qual finalidade atende: dá ao estudante um lugar para conferir os próprios
 *   dados e o currículo de uma vez, antes de decidir o que alterar.
 */
export function PaginaMeuPerfil({
  previa,
  modelo,
  possuiCurriculo,
  onEditarPerfil,
  onEditarCurriculo,
  onVoltarInicio,
}: PaginaMeuPerfilProps) {
  const { estudante } = previa;
  const contato = estudante.contato;
  const formacaoPrincipal = previa.formacoes[0];
  const resumo = [
    { rotulo: "Experiências", total: previa.experiencias.length },
    { rotulo: "Projetos", total: previa.projetos.length },
    { rotulo: "Competências", total: previa.competencias.length },
    { rotulo: "Idiomas", total: previa.idiomas.length },
    { rotulo: "Cursos e certificações", total: previa.documentos.length },
  ];

  return (
    <main className="pagina-meu-perfil">
      <div className="pagina-meu-perfil__conteudo">
        <header className="pagina-meu-perfil__cabecalho">
          <div>
            <button
              className="pagina-meu-perfil__voltar"
              onClick={onVoltarInicio}
              type="button"
            >
              ← Voltar ao início
            </button>
            <p className="pagina-meu-perfil__sobretitulo">Perfil</p>
            <h1 id="titulo-meu-perfil">Meu perfil</h1>
          </div>
          <div className="pagina-meu-perfil__acoes">
            <button
              className="pagina-meu-perfil__btn-secundario"
              onClick={onEditarPerfil}
              type="button"
            >
              Editar perfil
            </button>
            <button
              className="pagina-meu-perfil__btn-primario"
              onClick={onEditarCurriculo}
              type="button"
            >
              {possuiCurriculo ? "Editar currículo" : "Criar currículo"}
            </button>
          </div>
        </header>

        <div className="pagina-meu-perfil__grade">
          <aside
            aria-labelledby="titulo-dados-perfil"
            className="pagina-meu-perfil__cartao"
          >
            <div className="pagina-meu-perfil__identidade">
              <span aria-hidden="true" className="pagina-meu-perfil__avatar">
                {iniciais(estudante.nome)}
              </span>
              <div>
                <h2 id="titulo-dados-perfil">{estudante.nome}</h2>
                {formacaoPrincipal && (
                  <p>
                    {formacaoPrincipal.curso} · {formacaoPrincipal.instituicao}
                  </p>
                )}
              </div>
            </div>

            <dl className="pagina-meu-perfil__dados">
              <Dado rotulo="E-mail" valor={estudante.email} />
              <Dado rotulo="Telefone" valor={contato?.telefones.join(" · ")} />
              <Dado rotulo="Endereço" valor={contato?.endereco} />
              <Dado rotulo="LinkedIn" valor={contato?.linkedin} />
              <Dado rotulo="Currículo Lattes" valor={contato?.curriculo_lattes} />
            </dl>

            <h3 className="pagina-meu-perfil__subtitulo">Seu currículo</h3>
            <p className="pagina-meu-perfil__modelo">
              Modelo:{" "}
              <strong>{ROTULOS_MODELO_CURRICULO[modelo] ?? modelo}</strong>
            </p>
            <ul className="pagina-meu-perfil__resumo">
              {resumo.map((item) => (
                <li key={item.rotulo}>
                  <strong>{item.total}</strong>
                  <span>{item.rotulo}</span>
                </li>
              ))}
            </ul>
          </aside>

          <section
            aria-label="Currículo atual"
            className="pagina-meu-perfil__moldura"
          >
            {possuiCurriculo ? (
              <CurriculoNoModelo modelo={modelo} previa={previa} />
            ) : (
              <div className="pagina-meu-perfil__vazio">
                <p>Você ainda não montou seu currículo.</p>
                <button
                  className="pagina-meu-perfil__btn-primario"
                  onClick={onEditarCurriculo}
                  type="button"
                >
                  Criar currículo
                </button>
              </div>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}
