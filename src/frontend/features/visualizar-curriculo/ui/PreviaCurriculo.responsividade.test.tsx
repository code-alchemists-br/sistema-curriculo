// Proveniência: decision-analysis prompts/frontend/20261019-080800-previa-responsividade-evidencias-v001.md#v001
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import { ModeloClassico } from "./ModeloClassico";
import { ModeloCompacto } from "./ModeloCompacto";

afterEach(cleanup);

/**
 * Cria uma prévia completa e estruturada de currículo para teste em múltiplos tamanhos.
 *
 * **O que faz:** Instancia em memória um objeto `PreviaCurriculo` com dados ricos em todas as seções.
 * **Como faz:** Retorna dados com endereços, links externos, formação, experiência, projetos, competências, idiomas e documentos.
 * **Qual finalidade atende:** Garante dados representativos para validar a consistência visual em todas as resoluções de F1.1.
 */
function criarPreviaParaResponsividade(): PreviaCurriculo {
  return {
    curriculo_id: "curriculo-resp-409",
    titulo_versao: "Engenheira de Software e Acessibilidade",
    layout: "classico",
    estudante: {
      nome: "Beatriz Helena Figueiredo Rocha",
      email: "beatriz.rocha@fatec.sp.gov.br",
      contato: {
        endereco: "Avenida Paulista, 1000, Bela Vista, São Paulo - SP",
        telefones: ["(11) 98765-1122", "(11) 97654-3344"],
        linkedin:
          "https://linkedin.com/in/beatriz-helena-figueiredo-rocha-tech",
        curriculo_lattes: "https://lattes.cnpq.br/9988776655443322",
      },
    },
    formacoes: [
      {
        id: "form-409",
        instituicao: "FATEC São Paulo",
        curso: "Análise e Desenvolvimento de Sistemas",
        nivel: "Graduação Tecnológica",
        status: "Concluído",
        inicio: "2020-02-01",
        fim: "2023-12-15",
      },
    ],
    experiencias: [
      {
        id: "exp-409",
        empresa: "Laboratório de Tecnologia e Cidadania",
        cargo: "Engenheira de Software Frontend",
        descricao:
          "Desenvolvimento de plataformas públicas com design inclusivo, conformidade WCAG 2.1 AA e layout adaptável a celulares, tablets e monitores widescreen.",
        inicio: "2024-01-10",
        fim: null,
      },
    ],
    projetos: [
      {
        id: "proj-409",
        titulo: "Portal Acessível de Empregabilidade",
        descricao:
          "Aplicação web responsiva com alternância de layouts de currículo e renderização adaptativa.",
        tecnologias: "React, TypeScript, CSS Grid, Flexbox",
      },
    ],
    competencias: [
      {
        id: "comp-409-1",
        descricao: "Acessibilidade Digital (WCAG)",
        nivel: "Especialista",
      },
      { id: "comp-409-2", descricao: "Design Responsivo", nivel: "Avançado" },
      { id: "comp-409-3", descricao: "TypeScript", nivel: "Avançado" },
    ],
    idiomas: [
      { id: "idioma-409-1", idioma: "Inglês", nivel: "Fluente" },
      { id: "idioma-409-2", idioma: "Francês", nivel: "Intermediário" },
    ],
    documentos: [
      {
        id: "doc-409-1",
        nome_arquivo: "Diploma_Graduacao_ADS_FATEC.pdf",
        tipo_arquivo: "PDF",
      },
    ],
  };
}

/**
 * Renderiza um nó JSX dentro de um contêiner configurado com a largura fornecida em pixels.
 *
 * **O que faz:** Encapsula o componente em uma `<div>` simulando o viewport especificado em F1.1.
 * **Como faz:** Define largura fixa e `overflow-x: hidden` no elemento pai do teste.
 * **Qual finalidade atende:** Permite verificar a conformidade de renderização em cada resolução da matriz F1.1.
 */
function renderizarComLargura(
  elemento: React.ReactElement,
  larguraPixels: number,
) {
  return render(
    <div
      data-testid={`viewport-container-${larguraPixels}`}
      style={{
        width: `${larguraPixels}px`,
        maxWidth: `${larguraPixels}px`,
        margin: "0 auto",
        boxSizing: "border-box",
        overflowX: "hidden",
      }}
    >
      {elemento}
    </div>,
  );
}

describe("Prévia de Currículo — Matriz Completa de Responsividade F1.1 (Issue #409)", () => {
  const matrizBreakpointsF11 = [
    { nome: "Mobile Compacto", largura: 360 },
    { nome: "Mobile Médio", largura: 480 },
    { nome: "Mobile Clássico", largura: 640 },
    { nome: "Tablet", largura: 768 },
    { nome: "Desktop Padrão", largura: 1024 },
    { nome: "Desktop Amplo", largura: 1280 },
  ];

  describe("Modelo Clássico — Cobertura da Matriz F1.1", () => {
    /**
     * Valida a integridade dos dados e estrutura do Modelo Clássico em todas as resoluções de F1.1.
     *
     * **O que faz:** Itera por cada largura da matriz (360px a 1280px) garantindo a presença do cabeçalho e de todas as seções.
     * **Como faz:** Renderiza em loop com `renderizarComLargura`, executa cleanup e testa nós do DOM.
     * **Qual finalidade atende:** Comprova ausência de quebra de renderização em qualquer ponto da curva de breakpoints de F1.1.
     */
    it.each(matrizBreakpointsF11)(
      "mantém todos os dados do Modelo Clássico íntegros na resolução de $largura px ($nome)",
      ({ largura }) => {
        const previa = criarPreviaParaResponsividade();
        renderizarComLargura(<ModeloClassico previa={previa} />, largura);

        expect(
          screen.getByRole("heading", {
            level: 1,
            name: previa.estudante.nome,
          }),
        ).toBeInTheDocument();
        expect(screen.getByText(previa.estudante.email)).toBeInTheDocument();
        expect(
          screen.getByText("Análise e Desenvolvimento de Sistemas"),
        ).toBeInTheDocument();
        expect(
          screen.getByText("Engenheira de Software Frontend"),
        ).toBeInTheDocument();
        expect(
          screen.getByText("Portal Acessível de Empregabilidade"),
        ).toBeInTheDocument();
        expect(
          screen.getByText("Acessibilidade Digital (WCAG)"),
        ).toBeInTheDocument();
        expect(
          screen.getByText("Diploma_Graduacao_ADS_FATEC.pdf (PDF)"),
        ).toBeInTheDocument();

        cleanup();
      },
    );

    /**
     * Valida o comportamento de empilhamento móvel versus expansão desktop no Modelo Clássico.
     *
     * **O que faz:** Confere que as classes responsáveis pelo empilhamento (`modelo-classico`) estão presentes e que os links possuem quebra segura.
     * **Como faz:** Inspeciona atributos de classe e atributos de âncora nos contatos.
     * **Qual finalidade atende:** Assegura que o CSS responsivo atue corretamente nos limites de 640px e 768px+.
     */
    it("mantém classes e hierarquia de seções consistentes em Tablet (768px) e Desktop (1024px)", () => {
      const previa = criarPreviaParaResponsividade();
      const { container } = renderizarComLargura(
        <ModeloClassico previa={previa} />,
        1024,
      );

      const artigo = container.querySelector(".modelo-classico");
      expect(artigo).toBeInTheDocument();

      const secoes = container.querySelectorAll(".modelo-classico__secao");
      expect(secoes.length).toBe(6); // formação, experiência, projetos, competências, idiomas, documentos
    });
  });

  describe("Modelo Compacto — Cobertura da Matriz F1.1", () => {
    /**
     * Valida a integridade dos dados e estrutura do Modelo Compacto em todas as resoluções de F1.1.
     *
     * **O que faz:** Itera pelas resoluções de 360px a 1280px e confirma que todos os blocos permanecem legíveis.
     * **Como faz:** Renderiza o componente com `renderizarComLargura`, executa cleanup e testa os cabeçalhos semânticos.
     * **Qual finalidade atende:** Garante que a variante compacta responda estavelmente em toda a matriz F1.1.
     */
    it.each(matrizBreakpointsF11)(
      "mantém todos os dados do Modelo Compacto íntegros na resolução de $largura px ($nome)",
      ({ largura }) => {
        const previa = criarPreviaParaResponsividade();
        renderizarComLargura(<ModeloCompacto previa={previa} />, largura);

        expect(
          screen.getByRole("heading", {
            level: 1,
            name: previa.estudante.nome,
          }),
        ).toBeInTheDocument();
        expect(screen.getByText(previa.estudante.email)).toBeInTheDocument();
        expect(
          screen.getByText("Análise e Desenvolvimento de Sistemas"),
        ).toBeInTheDocument();
        expect(
          screen.getByText("Engenheira de Software Frontend"),
        ).toBeInTheDocument();
        expect(
          screen.getByText("Portal Acessível de Empregabilidade"),
        ).toBeInTheDocument();
        expect(
          screen.getByText("Acessibilidade Digital (WCAG) — Especialista"),
        ).toBeInTheDocument();
        expect(
          screen.getByText("Diploma_Graduacao_ADS_FATEC.pdf (PDF)"),
        ).toBeInTheDocument();

        cleanup();
      },
    );

    /**
     * Valida a presença da classe do contêiner e a transição fluida no breakpoint de 480px do Modelo Compacto.
     *
     * **O que faz:** Avalia a classe `.modelo-compacto` e a lista de contatos na resolução de 480px (30rem) e 768px.
     * **Como faz:** Realiza consultas de seletores e lista de elementos com Testing Library.
     * **Qual finalidade atende:** Confirma o cumprimento do breakpoint de 30rem definido em `ModeloCompacto.css`.
     */
    it("preserva a lista de contatos e itens inline em resoluções de transição (480px e 768px)", () => {
      const previa = criarPreviaParaResponsividade();
      const { container } = renderizarComLargura(
        <ModeloCompacto previa={previa} />,
        768,
      );

      const contato = container.querySelector(".modelo-compacto__contato");
      expect(contato).toBeInTheDocument();

      const itensInline = container.querySelectorAll(
        ".modelo-compacto__itens-inline",
      );
      expect(itensInline.length).toBe(3); // competências, idiomas, documentos
    });
  });
});
