// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

/**
 * Configura a compilação React e o DOM isolado dos testes unitários.
 *
 * A configuração usa o plugin oficial do Vite e registra o setup do Vitest sem
 * iniciar servidores, navegar ou acessar o backend. Ela existe para tornar a
 * fundação TypeScript reproduzível antes da implementação da tela de acesso.
 */
export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: "./app/test/setup.ts"
  }
});
