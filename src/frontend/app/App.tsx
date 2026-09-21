// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001

import { PaginaAcessoEstudante } from "../pages/acesso-estudante";

/**
 * Inicializa a superfície de acesso do estudante.
 *
 * O componente delega a composição da tela à camada pages, sem conhecer seus
 * formulários ou o transporte HTTP. Ele existe para manter a inicialização da
 * aplicação separada do caso de uso de cadastro e confirmação de credenciais.
 */
export function App() {
  return <PaginaAcessoEstudante />;
}
