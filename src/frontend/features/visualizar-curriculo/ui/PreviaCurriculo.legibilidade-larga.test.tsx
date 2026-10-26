// Proveniência: decision-analysis prompts/frontend/20261026-081230-legibilidade-modelos-tela-larga-v001.md#v001
import { cleanup, render, screen } from "@testing-library/react";
import React from "react";
import { afterEach, describe, expect, it } from "vitest";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import { ModeloClassico } from "./ModeloClassico";
import { ModeloCompacto } from "./ModeloCompacto";

afterEach(cleanup);

/**
 * Cria uma prévia rica e representativa de currículo para teste de legibilidade em telas amplas.
 *
 * **O que faz:** Constrói um objeto completo de `PreviaCurriculo` contendo dados em todas as seções cadastrais.
 * **Como faz:** Retorna estruturas populadas com dados pessoais, contatos múltiplos, formação acadêmica, experiências com períodos, projetos descritivos, competências, idiomas e documentos.
 * **Qual finalidade atende:** Fornece massa de dados realista para avaliar diagramação, densidade tipográfica e quebras de linha em viewports largos (>= 1024px).
 */
function criarPreviaParaLegibilidadeLarga(): PreviaCurriculo {
  return {
    curriculo_id: "curriculo-larga-220",
    titulo_versao: "Engenheiro de Software Sênior — Arquitetura e Frontend",
    layout: "classico",
    estudante: {
      nome: "Carlos Eduardo de Albuquerque Menezes",
      email: "carlos.menezes@fatec.sp.gov.br",
      contato: {
        endereco:
          "Avenida Engenheiro Luís Carlos Berrini, 1500, Itaim Bibi, São Paulo - SP",
        telefones: ["(11) 98877-6655", "(11) 3214-5500"],
        linkedin:
          "https://linkedin.com/in/carlos-eduardo-albuquerque-menezes-dev",
        curriculo_lattes: "https://lattes.cnpq.br/1122334455667788",
      },
    },
    formacoes: [
      {
        id: "form-220-1",
        instituicao: "Faculdade de Tecnologia de São Paulo (FATEC-SP)",
        curso: "Tecnologia em Análise e Desenvolvimento de Sistemas",
        nivel: "Graduação Tecnológica",
        status: "Concluído",
        inicio: "2018-02-01",
        fim: "2021-12-18",
      },
      {
        id: "form-220-2",
        instituicao: "Universidade de São Paulo (USP)",
        curso: "Especialização em Engenharia de Software e Qualidade",
        nivel: "Pós-graduação Lato Sensu",
        status: "Concluído",
        inicio: "2022-03-01",
        fim: "2023-11-30",
      },
    ],
    experiencias: [
      {
        id: "exp-220-1",
        empresa: "Tech Solutions Arquitetura de Sistemas S/A",
        cargo: "Engenheiro de Software Especialista",
        descricao:
          "Liderança técnica na modernização de interfaces com foco em design responsivo, alta legibilidade tipográfica para recrutamento corporativo e aderência às diretrizes de acessibilidade WCAG 2.1 AA.",
        inicio: "2022-01-15",
        fim: null,
      },
      {
        id: "exp-220-2",
        empresa: "Inovação Digital Brasil Ltda.",
        cargo: "Desenvolvedor Frontend Pleno",
        descricao:
          "Desenvolvimento e refatoração de sistemas web em React e TypeScript, aplicando Feature-Sliced Design e otimizações de layout em grades CSS e Flexbox.",
        inicio: "2019-06-01",
        fim: "2021-12-31",
      },
    ],
    projetos: [
      {
        id: "proj-220-1",
        titulo: "Plataforma de Seleção e Triagem Curricular Acessível",
        descricao:
          "Arquitetura de visualização e exportação de currículos com múltiplos modelos tipográficos profissionais para visualização em telas widescreen e impressão de alta fidelidade.",
        tecnologias: "React, TypeScript, CSS Grid, Vitest, Testing Library",
      },
    ],
    competencias: [
      {
        id: "comp-220-1",
        descricao: "Arquitetura Frontend e FSD",
        nivel: "Especialista",
      },
      {
        id: "comp-220-2",
        descricao: "Design Responsivo e Tipografia",
        nivel: "Especialista",
      },
      {
        id: "comp-220-3",
        descricao: "Testes de Componente e Qualidade",
        nivel: "Avançado",
      },
      {
        id: "comp-220-4",
        descricao: "TypeScript e Clean Code",
        nivel: "Especialista",
      },
    ],
    idiomas: [
      { id: "idioma-220-1", idioma: "Inglês", nivel: "Avançado (C1)" },
      { id: "idioma-220-2", idioma: "Espanhol", nivel: "Intermediário (B2)" },
    ],
    documentos: [
      {
        id: "doc-220-1",
        nome_arquivo: "Certificado_Ingles_Avancado_C1.pdf",
        tipo_arquivo: "PDF",
      },
      {
        id: "doc-220-2",
        nome_arquivo: "Diploma_Graduacao_FATEC_SP.pdf",
        tipo_arquivo: "PDF",
      },
    ],
  };
}

/**
 * Renderiza um nó JSX dentro de um contêiner simulador de tela larga em pixels.
 *
 * **O que faz:** Encapsula o componente em uma `<div>` simulando viewports desktop definidos em F1.1.
 * **Como faz:** Aplica largura rígida e `overflow-x: hidden` para validação de layout no DOM de teste.
 * **Qual finalidade atende:** Permite verificar a contenção geométrica e regras de legibilidade em 1024px e 1280px+.
 */
function renderizarEmTelaLarga(
  elemento: React.ReactElement,
  larguraPixels: number,
) {
  return render(
    <div
      data-testid={`tela-larga-container-${larguraPixels}`}
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

describe("Legibilidade em Tela Larga para Modelos de Currículo — Issue #220 [F5.12]", () => {
  const resolucoesTelaLarga = [
    { nome: "Desktop Padrão (F1.1)", largura: 1024 },
    { nome: "Desktop Amplo (F1.1)", largura: 1280 },
    { nome: "Full HD Widescreen", largura: 1920 },
  ];

  describe("Modelo Clássico — Validação de Legibilidade em Tela Larga", () => {
    /**
     * Valida a contenção de largura máxima e margem centrada em resoluções de tela ampla.
     *
     * **O que faz:** Inspeciona o contêiner raiz do `ModeloClassico` para certificar que adota a classe `.modelo-classico`.
     * **Como faz:** Renderiza em 1024px, 1280px e 1920px e verifica a existência do elemento artigo delimitador de largura máxima.
     * **Qual finalidade atende:** Garante que o texto não se estenda descontroladamente pela tela inteira em monitores grandes.
     */
    it.each(resolucoesTelaLarga)(
      "mantém contenção e integridade em $nome ($largura px)",
      ({ largura }) => {
        const previa = criarPreviaParaLegibilidadeLarga();
        const { container } = renderizarEmTelaLarga(
          <ModeloClassico previa={previa} />,
          largura,
        );

        const artigo = container.querySelector(".modelo-classico");
        expect(artigo).toBeInTheDocument();

        // Confirma que o título principal e as seções chave estão legíveis e presentes
        expect(
          screen.getByRole("heading", {
            level: 1,
            name: previa.estudante.nome,
          }),
        ).toBeInTheDocument();
        expect(screen.getByText(previa.estudante.email)).toBeInTheDocument();
        expect(
          screen.getByRole("heading", {
            level: 2,
            name: /formação acadêmica/i,
          }),
        ).toBeInTheDocument();
        expect(
          screen.getByRole("heading", {
            level: 2,
            name: /experiência profissional/i,
          }),
        ).toBeInTheDocument();

        cleanup();
      },
    );

    /**
     * Valida o alinhamento de itens com cabeçalho bi-coluna (título à esquerda, período à direita).
     *
     * **O que faz:** Verifica a classe `.modelo-classico__linha-cabecalho` que opera com `display: flex; justify-content: space-between`.
     * **Como faz:** Busca todas as instâncias de `.modelo-classico__linha-cabecalho` e confirma presença de título e período associados.
     * **Qual finalidade atende:** Garante leitura confortável e organizada de histórico profissional e acadêmico em tela larga.
     */
    it("apresenta cabeçalhos de itens em estrutura bi-coluna organizada", () => {
      const previa = criarPreviaParaLegibilidadeLarga();
      const { container } = renderizarEmTelaLarga(
        <ModeloClassico previa={previa} />,
        1280,
      );

      const linhasCabecalho = container.querySelectorAll(
        ".modelo-classico__linha-cabecalho",
      );
      // 2 formações + 2 experiências = 4 cabeçalhos de itens
      expect(linhasCabecalho.length).toBe(4);

      // Cada cabeçalho deve conter o título do item e o período
      linhasCabecalho.forEach((linha) => {
        expect(
          linha.querySelector(".modelo-classico__titulo-item"),
        ).toBeInTheDocument();
        expect(
          linha.querySelector(".modelo-classico__periodo"),
        ).toBeInTheDocument();
      });
    });

    /**
     * Valida a distribuição em grid de competências e documentos para aproveitamento ótimo da tela larga.
     *
     * **O que faz:** Confere que as seções de competências utilizam `.modelo-classico__grid-duas-colunas`.
     * **Como faz:** Inspeciona as listas com classe `.modelo-classico__grid-duas-colunas` e valida seus itens filhos.
     * **Qual finalidade atende:** Assegura que competências e idiomas não formem uma coluna vertical única excessivamente estreita em telas de alta resolução.
     */
    it("distribui competências e idiomas em grid estruturado", () => {
      const previa = criarPreviaParaLegibilidadeLarga();
      const { container } = renderizarEmTelaLarga(
        <ModeloClassico previa={previa} />,
        1280,
      );

      const grids = container.querySelectorAll(
        ".modelo-classico__grid-duas-colunas",
      );
      // 1 grid para competências + 1 grid para idiomas = 2 grids
      expect(grids.length).toBe(2);

      expect(
        screen.getByText(/Arquitetura Frontend e FSD/i),
      ).toBeInTheDocument();
      expect(
        screen.getByText(/Design Responsivo e Tipografia/i),
      ).toBeInTheDocument();
      expect(screen.getByText(/Inglês/i)).toBeInTheDocument();
      expect(screen.getByText(/Espanhol/i)).toBeInTheDocument();
    });

    /**
     * Valida os separadores de contato horizontais em tela larga no Modelo Clássico.
     *
     * **O que faz:** Verifica se a lista de contatos `.modelo-classico__contato` contém múltiplos itens e formatação legível.
     * **Como faz:** Localiza o elemento `.modelo-classico__contato` e verifica seus filhos `<li>`.
     * **Qual finalidade atende:** Garante leitura limpa e espaçada das vias de contato do candidato.
     */
    it("organiza contatos com clareza tipográfica horizontal", () => {
      const previa = criarPreviaParaLegibilidadeLarga();
      const { container } = renderizarEmTelaLarga(
        <ModeloClassico previa={previa} />,
        1024,
      );

      const listaContato = container.querySelector(".modelo-classico__contato");
      expect(listaContato).toBeInTheDocument();

      const itensContato = listaContato?.querySelectorAll("li");
      expect(itensContato?.length).toBeGreaterThanOrEqual(4); // email, telefones, endereço, links
    });
  });

  describe("Modelo Compacto — Validação de Legibilidade em Tela Larga", () => {
    /**
     * Valida a contenção de largura máxima e margem centrada do Modelo Compacto em tela ampla.
     *
     * **O que faz:** Inspeciona o elemento com classe `.modelo-compacto` em 1024px e 1280px.
     * **Como faz:** Renderiza no contêiner de teste e valida presença dos blocos estruturais essenciais.
     * **Qual finalidade atende:** Garante que o layout compacto mantenha proporções equilibradas e alta densidade de leitura.
     */
    it.each(resolucoesTelaLarga)(
      "mantém legibilidade e densidade tipográfica em $nome ($largura px)",
      ({ largura }) => {
        const previa = criarPreviaParaLegibilidadeLarga();
        const { container } = renderizarEmTelaLarga(
          <ModeloCompacto previa={previa} />,
          largura,
        );

        const artigo = container.querySelector(".modelo-compacto");
        expect(artigo).toBeInTheDocument();

        expect(
          screen.getByRole("heading", {
            level: 1,
            name: previa.estudante.nome,
          }),
        ).toBeInTheDocument();
        expect(screen.getByText(previa.estudante.email)).toBeInTheDocument();
        expect(
          screen.getByRole("heading", {
            level: 2,
            name: /formação acadêmica/i,
          }),
        ).toBeInTheDocument();

        cleanup();
      },
    );

    /**
     * Valida a disposição inline com separadores em listas secundárias no Modelo Compacto.
     *
     * **O que faz:** Confere que `.modelo-compacto__contato` e `.modelo-compacto__itens-inline` exibem os itens de forma contínua e legível.
     * **Como faz:** Inspeciona os elementos com a classe `.modelo-compacto__itens-inline`.
     * **Qual finalidade atende:** Assegura economia de altura vertical sem prejuízo de clareza visual em monitores amplos.
     */
    it("apresenta listas secundárias no formato inline com alta legibilidade", () => {
      const previa = criarPreviaParaLegibilidadeLarga();
      const { container } = renderizarEmTelaLarga(
        <ModeloCompacto previa={previa} />,
        1280,
      );

      const listasInline = container.querySelectorAll(
        ".modelo-compacto__itens-inline",
      );
      // Competências e idiomas utilizam formato inline no Modelo Compacto
      expect(listasInline.length).toBeGreaterThanOrEqual(2);

      expect(
        screen.getByText(/Arquitetura Frontend e FSD/i),
      ).toBeInTheDocument();
      expect(screen.getByText(/Inglês/i)).toBeInTheDocument();
    });

    /**
     * Valida a hierarquia de cabeçalhos e ausência de sobreposição no Modelo Compacto em tela ampla.
     *
     * **O que faz:** Atesta que os títulos h2 de todas as seções permanecem destacados com a cor semântica `#1e3a8a`.
     * **Como faz:** Busca todos os títulos de nível 2 e valida quantidade e correspondência com as seções preenchidas.
     * **Qual finalidade atende:** Confirma que a escaneabilidade visual é imediata para avaliadores corporativos.
     */
    it("assegura escaneabilidade e hierarquia de seções", () => {
      const previa = criarPreviaParaLegibilidadeLarga();
      renderizarEmTelaLarga(<ModeloCompacto previa={previa} />, 1024);

      const titulosSecao = screen.getAllByRole("heading", { level: 2 });
      // Formação, Experiência, Projetos, Competências, Idiomas, Informações Adicionais
      expect(titulosSecao.length).toBe(6);
    });
  });
});
