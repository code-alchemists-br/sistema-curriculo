import { PaginaDocumentoPublico } from "../../../shared/ui/PaginaDocumentoPublico";
import { CabecalhoPublico } from "../../../widgets/cabecalho-publico";

/** Define as ações de navegação usadas pela página pública de privacidade. */
export interface PaginaPoliticaDePrivacidadeProps {
  onNavegarInicio?: () => void;
  onNavegarLogin?: () => void;
  onNavegarCadastro?: () => void;
  onNavegarTermosDeUso?: () => void;
}

/**
 * Apresenta as práticas de privacidade confirmadas na documentação do projeto.
 *
 * Como faz: agrupa em seções os dados tratados, suas finalidades e os
 * controles técnicos já definidos, sem afirmar prazos ou práticas pendentes.
 *
 * Qual finalidade atende: oferece transparência à pessoa estudante sem criar
 * compromissos jurídicos que ainda não foram aprovados pelo projeto.
 */
export function PaginaPoliticaDePrivacidade({
  onNavegarInicio,
  onNavegarLogin,
  onNavegarCadastro,
  onNavegarTermosDeUso,
}: PaginaPoliticaDePrivacidadeProps) {
  return (
    <PaginaDocumentoPublico
      cabecalho={
        <CabecalhoPublico
          onNavegarCadastro={onNavegarCadastro}
          onNavegarInicio={onNavegarInicio}
          onNavegarLogin={onNavegarLogin}
        />
      }
      descricao="Informações sobre o tratamento de dados necessárias para a conta e para a construção do currículo."
      rodape={
        <div className="pagina-documento-publico__rodape-conteudo">
          <span>LIMINAL — Sistema Currículo</span>
          <nav
            aria-label="Navegação entre documentos legais"
            className="pagina-documento-publico__navegacao"
          >
            <button
              className="pagina-documento-publico__link"
              onClick={onNavegarTermosDeUso}
              type="button"
            >
              Ler Termos de Uso
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
      sobrancelha="Transparência e proteção de dados"
      titulo="Política de Privacidade"
      aviso={
        <p>
          <strong>Versão em desenvolvimento.</strong> Esta tela consolida
          práticas confirmadas nos documentos técnicos do projeto. Informações
          ainda não definidas, como prazo geral de retenção, canal do
          controlador e versão jurídica vigente, não são apresentadas como se já
          existissem.
        </p>
      }
    >
      <section aria-labelledby="privacidade-dados">
        <h2 id="privacidade-dados">1. Dados tratados</h2>
        <p>
          Para manter uma conta e organizar currículos, o sistema pode tratar
          dados de identificação e contato, além de informações acadêmicas e
          profissionais fornecidas pela própria pessoa estudante.
        </p>
        <ul>
          <li>nome, e-mail, endereço e telefone;</li>
          <li>formação, experiências, competências, cursos e idiomas;</li>
          <li>projetos, certificações, links e documentos complementares;</li>
          <li>versões de currículo e os itens escolhidos para cada versão.</li>
        </ul>
      </section>

      <section aria-labelledby="privacidade-finalidades">
        <h2 id="privacidade-finalidades">2. Finalidades</h2>
        <p>
          As informações são usadas para viabilizar o cadastro e a manutenção da
          conta, a organização do perfil, a criação e a visualização de
          currículos e os recursos do produto que forem efetivamente
          disponibilizados.
        </p>
      </section>

      <section aria-labelledby="privacidade-acesso">
        <h2 id="privacidade-acesso">3. Acesso e proteção</h2>
        <p>
          Dados pessoais e currículos devem ser associados à conta autenticada.
          As operações protegidas precisam verificar autorização e propriedade
          no servidor; alterar identificadores enviados pela interface não deve
          permitir acesso aos recursos de outra pessoa.
        </p>
      </section>

      <section aria-labelledby="privacidade-ia">
        <h2 id="privacidade-ia">4. Assistência por inteligência artificial</h2>
        <p>
          Caso uma assistência de IA seja disponibilizada, o envio de dados a um
          provedor externo dependerá de consentimento explícito. O contexto deve
          conter somente as informações necessárias à ação solicitada e não deve
          incluir telefones, endereço ou documentos sem justificativa direta.
        </p>
      </section>

      <section aria-labelledby="privacidade-exclusao">
        <h2 id="privacidade-exclusao">5. Exclusão e retenção</h2>
        <p>
          A documentação atual prevê exclusão lógica para perfil e documentos
          complementares em situações aplicáveis. Ela não define prazo geral de
          retenção, purga física, comportamento de backups ou anonimização
          definitiva; esses pontos exigem uma política específica aprovada.
        </p>
      </section>

      <section aria-labelledby="privacidade-atualizacoes">
        <h2 id="privacidade-atualizacoes">6. Próximas definições</h2>
        <p>
          Uma política publicada para uso em produção deverá identificar o
          responsável pelo tratamento, o canal de contato e a data de vigência,
          além de refletir as decisões jurídicas e operacionais aprovadas pela
          equipe responsável.
        </p>
      </section>
    </PaginaDocumentoPublico>
  );
}
