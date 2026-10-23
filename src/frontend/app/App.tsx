import { useState } from "react";

import { PaginaAcessoEstudante } from "../pages/acesso-estudante";
import { PaginaInicio } from "../pages/inicio";

type RotaAtiva = "inicio" | "acesso";

/**
 * Ponto de entrada da aplicação.
 *
 * Apresenta a página inicial pública da LIMINAL com a seção Hero e o cabeçalho.
 * As ações de cadastro, login e criação de currículo conduzem o usuário à tela
 * de acesso e gerenciamento de conta do estudante.
 */
export function App() {
  const [rotaAtiva, setRotaAtiva] = useState<RotaAtiva>("inicio");

  if (rotaAtiva === "acesso") {
    return <PaginaAcessoEstudante />;
  }

  return (
    <PaginaInicio
      onNavegarCadastro={() => setRotaAtiva("acesso")}
      onNavegarLogin={() => setRotaAtiva("acesso")}
      onNavegarInicio={() => setRotaAtiva("inicio")}
    />
  );
}
