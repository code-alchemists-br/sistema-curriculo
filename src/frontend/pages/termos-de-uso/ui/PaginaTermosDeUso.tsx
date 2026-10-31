import { PaginaDocumentoPublico } from "../../../shared/ui/PaginaDocumentoPublico";
import { CabecalhoPublico } from "../../../widgets/cabecalho-publico";

/** Define as ações de navegação usadas pela página pública de termos. */
export interface PaginaTermosDeUsoProps {
  onNavegarInicio?: () => void;
  onNavegarLogin?: () => void;
  onNavegarCadastro?: () => void;
  onNavegarPoliticaDePrivacidade?: () => void;
}

/**
 * Apresenta orientações de uso do Sistema Currículo ao estudante.
 *
 * Como faz: organiza somente informações confirmadas na documentação do
 * projeto em seções semânticas e delega as transições de tela ao App.
 *
 * Qual finalidade atende: torna as orientações de uso acessíveis pela
 * navegação pública sem criar regras de conta, persistência ou backend.
 */
export function PaginaTermosDeUso({
  onNavegarInicio,
  onNavegarLogin,
  onNavegarCadastro,
  onNavegarPoliticaDePrivacidade,
}: PaginaTermosDeUsoProps) {
  return (
    <PaginaDocumentoPublico
      cabecalho={
        <CabecalhoPublico
          onNavegarCadastro={onNavegarCadastro}
          onNavegarInicio={onNavegarInicio}
          onNavegarLogin={onNavegarLogin}
        />
      }
      descricao="Orientações para utilizar a LIMINAL na organização e apresentação das informações do seu currículo."
      rodape={
        <div className="pagina-documento-publico__rodape-conteudo">
          <span>LIMINAL — Sistema Currículo</span>
          <nav
            aria-label="Navegação entre documentos legais"
            className="pagina-documento-publico__navegacao"
          >
            <button
              className="pagina-documento-publico__link"
              onClick={onNavegarPoliticaDePrivacidade}
              type="button"
            >
              Ler Política de Privacidade
            </button>
            <button
              className="pagina-documento-publico__link"
              onClick={onNavegarInicio}
              type="button"
            >
              Voltar ao início
            </button>
          </nav>
        </div>
      }
      sobrancelha="Transparência e uso responsável"
      titulo="Termos de Uso"
      aviso={
        <p>
          <strong>Versão em desenvolvimento.</strong> Este texto apresenta as
          orientações já documentadas no projeto. A definição jurídica final,
          incluindo vigência e canais formais de atendimento, ainda depende de
          publicação pela equipe responsável.
        </p>
      }
    >
      <section aria-labelledby="termos-finalidade">
        <h2 id="termos-finalidade">1. Finalidade da plataforma</h2>
        <p>
          A LIMINAL apoia estudantes na organização de informações pessoais e
          profissionais e na elaboração de currículos. O sistema reúne dados de
          perfil, formação, experiências, competências e informações
          complementares para que possam ser usados em versões de currículo.
        </p>
      </section>

      <section aria-labelledby="termos-conta">
        <h2 id="termos-conta">2. Uso da conta</h2>
        <p>
          O acesso previsto utiliza e-mail e senha. Mantenha suas credenciais
          sob seu controle e não as compartilhe com outras pessoas. A conta deve
          ser usada para acessar e administrar os dados e currículos da própria
          pessoa estudante.
        </p>
      </section>

      <section aria-labelledby="termos-conteudo">
        <h2 id="termos-conteudo">3. Informações do currículo</h2>
        <p>
          Informe dados pertinentes, verdadeiros e relacionados ao seu próprio
          percurso acadêmico ou profissional. Para testes, apresentações e
          demonstrações, use apenas dados fictícios da massa de teste e nunca
          copie credenciais, documentos ou currículos reais para registros
          públicos.
        </p>
      </section>

      <section aria-labelledby="termos-seguranca">
        <h2 id="termos-seguranca">4. Segurança e acesso</h2>
        <p>
          A plataforma prevê que dados pessoais e currículos sejam associados à
          conta autenticada. A interface não substitui os controles de
          segurança: a autorização para operações protegidas deve ser validada
          pelo servidor.
        </p>
      </section>

      <section aria-labelledby="termos-recursos">
        <h2 id="termos-recursos">5. Recursos em evolução</h2>
        <p>
          Algumas funcionalidades do projeto permanecem em desenvolvimento ou
          dependem de integrações ainda não publicadas. A existência de uma tela
          não representa, por si só, confirmação de que uma ação como exportação
          ou envio de e-mail já esteja disponível em produção.
        </p>
      </section>

      <section aria-labelledby="termos-atualizacoes">
        <h2 id="termos-atualizacoes">6. Atualizações deste documento</h2>
        <p>
          Este conteúdo deve acompanhar as decisões técnicas e de produto
          aprovadas. Quando a versão jurídica definitiva for publicada, ela
          deverá informar sua data de vigência e substituir claramente esta
          versão informativa.
        </p>
      </section>
    </PaginaDocumentoPublico>
  );
}
