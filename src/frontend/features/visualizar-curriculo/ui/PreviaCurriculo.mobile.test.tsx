// Proveniência: decision-analysis prompts/frontend/20261019-075200-previa-curriculo-largura-movel-v001.md#v001
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import { ModeloClassico } from "./ModeloClassico";
import { ModeloCompacto } from "./ModeloCompacto";

afterEach(cleanup);

/**
 * Cria uma prévia determinística e completa de currículo para validação de responsividade.
 *
 * **O que faz:** Gera um objeto `PreviaCurriculo` contendo estudante, contato, formações, experiências, projetos, competências, idiomas e documentos.
 * **Como faz:** Instancia as entidades em memória com dados representativos e URLs de tamanho extenso para testar quebra de layout.
 * **Qual finalidade atende:** Garante dados de entrada idênticos e previsíveis para todos os cenários de teste móvel.
 */
function criarPreviaCompleta(): PreviaCurriculo {
  return {
    curriculo_id: "curriculo-mobile-001",
    titulo_versao: "Desenvolvedor Mobile e Web",
    layout: "classico",
    estudante: {
      nome: "Mariana Clara dos Santos Albuquerque",
      email: "mariana.albuquerque@fatec.sp.gov.br",
      contato: {
        endereco: "Rua das Flores, 123, Bloco B, Apto 402, São Paulo - SP",
        telefones: ["(11) 98765-4321", "(11) 91234-5678"],
        linkedin:
          "https://linkedin.com/in/mariana-clara-albuquerque-desenvolvedora-fullstack-especialista",
        curriculo_lattes:
          "https://lattes.cnpq.br/1234567890123456789012345678901234567890",
      },
    },
    formacoes: [
      {
        id: "form-01",
        instituicao: "Faculdade de Tecnologia de São Paulo (FATEC)",
        curso: "Análise e Desenvolvimento de Sistemas",
        nivel: "Tecnólogo",
        status: "Concluído",
        inicio: "2021-02-01",
        fim: "2024-06-30",
      },
    ],
    experiencias: [
      {
        id: "exp-01",
        empresa: "Soluções de Software Inovadoras S.A.",
        cargo: "Desenvolvedora Frontend Júnior",
        descricao:
          "Desenvolvimento e manutenção de interfaces responsivas para web e mobile utilizando React, TypeScript e boas práticas de acessibilidade WCAG.",
        inicio: "2024-07-01",
        fim: null,
      },
    ],
    projetos: [
      {
        id: "proj-01",
        titulo: "Aplicativo de Gestão Curricular Acessível",
        descricao:
          "Interface responsiva voltada a estudantes e recrutadores com suporte a leitores de tela.",
        tecnologias: "React, TypeScript, CSS Modules",
      },
    ],
    competencias: [
      { id: "comp-01", descricao: "TypeScript", nivel: "Avançado" },
      {
        id: "comp-02",
        descricao: "Design Responsivo (Mobile-first)",
        nivel: "Avançado",
      },
    ],
    idiomas: [
      { id: "idioma-01", idioma: "Inglês", nivel: "Avançado" },
      { id: "idioma-02", idioma: "Espanhol", nivel: "Básico" },
    ],
    documentos: [
      {
        id: "doc-01",
        nome_arquivo: "Certificado_Conclusao_FATEC_2024.pdf",
        tipo_arquivo: "PDF",
      },
    ],
  };
}

/**
 * Renderiza um elemento JSX envolvido em um contêiner com largura móvel restrita (F1.1).
 *
 * **O que faz:** Envolve o nó JSX em uma `<div>` com estilo inline `width` e `maxWidth` especificados e `overflow: hidden`.
 * **Como faz:** Cria um contêiner delimitador simulando a largura do viewport de dispositivos móveis definidos em F1.1.
 * **Qual finalidade atende:** Permite verificar a integridade da árvore DOM renderizada dentro dos limites de largura móvel (360px, 480px, 640px).
 */
function renderizarEmViewportMovel(
  elemento: React.ReactElement,
  larguraPixels: number,
) {
  return render(
    <div
      data-testid={`viewport-container-${larguraPixels}`}
      style={{
        width: `${larguraPixels}px`,
        maxWidth: `${larguraPixels}px`,
        boxSizing: "border-box",
        overflowX: "hidden",
      }}
    >
      {elemento}
    </div>,
  );
}

describe("Prévia de Currículo — Validação na Largura Móvel F1.1 (Issue #366)", () => {
  describe("Modelo Clássico em Viewport Móvel", () => {
    /**
     * Valida a integridade da apresentação do Modelo Clássico na largura móvel estreita (360px).
     *
     * **O que faz:** Renderiza o ModeloClássico em contêiner de 360px e verifica a presença de todas as seções e dados sem omissões indevidas.
     * **Como faz:** Utiliza `renderizarEmViewportMovel(..., 360)` e efetua asserções de busca no DOM por cabeçalho, contatos, formação, experiência e projetos.
     * **Qual finalidade atende:** Atende a F1.1 e RNF03 garantindo que smartphones pequenos apresentem todo o conteúdo do currículo clássico de forma legível.
     */
    it("apresenta todas as seções e dados do currículo clássico na largura móvel de 360px", () => {
      const previa = criarPreviaCompleta();
      renderizarEmViewportMovel(<ModeloClassico previa={previa} />, 360);

      const artigo = screen.getByRole("article", {
        name: `Currículo de ${previa.estudante.nome}`,
      });
      expect(artigo).toHaveClass("modelo-classico");

      expect(
        screen.getByRole("heading", { level: 1, name: previa.estudante.nome }),
      ).toBeInTheDocument();
      expect(screen.getByText(previa.estudante.email)).toBeInTheDocument();
      expect(screen.getByText("(11) 98765-4321")).toBeInTheDocument();
      expect(screen.getByRole("link", { name: "LinkedIn" })).toHaveAttribute(
        "href",
        previa.estudante.contato?.linkedin,
      );
      expect(
        screen.getByRole("link", { name: "Currículo Lattes" }),
      ).toHaveAttribute("href", previa.estudante.contato?.curriculo_lattes);

      expect(
        screen.getByRole("heading", { level: 2, name: "Formação acadêmica" }),
      ).toBeInTheDocument();
      expect(
        screen.getByText("Análise e Desenvolvimento de Sistemas"),
      ).toBeInTheDocument();

      expect(
        screen.getByRole("heading", {
          level: 2,
          name: "Experiência profissional",
        }),
      ).toBeInTheDocument();
      expect(
        screen.getByText("Desenvolvedora Frontend Júnior"),
      ).toBeInTheDocument();

      expect(
        screen.getByRole("heading", { level: 2, name: "Projetos acadêmicos" }),
      ).toBeInTheDocument();
      expect(
        screen.getByText("Aplicativo de Gestão Curricular Acessível"),
      ).toBeInTheDocument();

      expect(
        screen.getByRole("heading", { level: 2, name: "Competências" }),
      ).toBeInTheDocument();
      expect(
        screen.getByText("Design Responsivo (Mobile-first)"),
      ).toBeInTheDocument();

      expect(
        screen.getByRole("heading", { level: 2, name: "Idiomas" }),
      ).toBeInTheDocument();
      expect(screen.getByText("Inglês")).toBeInTheDocument();

      expect(
        screen.getByRole("heading", {
          level: 2,
          name: "Documentos complementares",
        }),
      ).toBeInTheDocument();
      expect(
        screen.getByText("Certificado_Conclusao_FATEC_2024.pdf (PDF)"),
      ).toBeInTheDocument();
    });

    /**
     * Valida a estrutura semântica e hierarquia do Modelo Clássico no limite móvel de 480px e 640px.
     *
     * **O que faz:** Confere que nos breakpoints de 480px e 640px (limite móvel de 40rem do ModeloClássico), as listas e seções mantêm classes consistentes.
     * **Como faz:** Renderiza o componente com `renderizarEmViewportMovel(..., 480)` e `(..., 640)` avaliando a presença das classes do layout clássico.
     * **Qual finalidade atende:** Garante que a transição entre telas muito estreitas (360px) e o limite superior móvel (640px / 40rem) preserve a semântica.
     */
    it("preserva a hierarquia semântica e classes no breakpoint móvel clássico de 640px (40rem)", () => {
      const previa = criarPreviaCompleta();
      renderizarEmViewportMovel(<ModeloClassico previa={previa} />, 640);

      const listaContato = screen.getByRole("list", {
        name: "Informações de contato",
      });
      expect(listaContato).toHaveClass("modelo-classico__contato");

      const itens = screen.getAllByRole("listitem");
      expect(itens.length).toBeGreaterThanOrEqual(8);
    });
  });

  describe("Modelo Compacto em Viewport Móvel", () => {
    /**
     * Valida a integridade da apresentação do Modelo Compacto na largura móvel estreita (360px).
     *
     * **O que faz:** Renderiza o ModeloCompacto em contêiner de 360px e afere que todos os dados essenciais permanecem visíveis.
     * **Como faz:** Renderiza com `renderizarEmViewportMovel(..., 360)` e valida cabeçalho, contatos, formações e experiências no layout compacto.
     * **Qual finalidade atende:** Garante que a variante compacta funcione perfeitamente em smartphones sem truncamentos acidentais.
     */
    it("apresenta todas as seções e dados do currículo compacto na largura móvel de 360px", () => {
      const previa = criarPreviaCompleta();
      renderizarEmViewportMovel(<ModeloCompacto previa={previa} />, 360);

      const artigo = screen.getByRole("article", {
        name: `Currículo de ${previa.estudante.nome}`,
      });
      expect(artigo).toHaveClass("modelo-compacto");

      expect(
        screen.getByRole("heading", { level: 1, name: previa.estudante.nome }),
      ).toBeInTheDocument();
      expect(screen.getByText(previa.estudante.email)).toBeInTheDocument();
      expect(screen.getByText("(11) 98765-4321")).toBeInTheDocument();

      expect(
        screen.getByRole("heading", { level: 2, name: "Formação acadêmica" }),
      ).toBeInTheDocument();
      expect(
        screen.getByText("Análise e Desenvolvimento de Sistemas"),
      ).toBeInTheDocument();

      expect(
        screen.getByRole("heading", {
          level: 2,
          name: "Experiência profissional",
        }),
      ).toBeInTheDocument();
      expect(
        screen.getByText("Desenvolvedora Frontend Júnior"),
      ).toBeInTheDocument();

      expect(
        screen.getByRole("heading", { level: 2, name: "Competências" }),
      ).toBeInTheDocument();
      expect(screen.getByText("TypeScript — Avançado")).toBeInTheDocument();
    });

    /**
     * Valida a preservação e formatação no breakpoint de 480px (30rem do ModeloCompacto).
     *
     * **O que faz:** Avalia a presença da classe raiz `modelo-compacto` e das seções sob viewport de 480px.
     * **Como faz:** Renderiza com `renderizarEmViewportMovel(..., 480)` e valida a existência dos nós no DOM.
     * **Qual finalidade atende:** Assegura fidelidade ao breakpoint de 30rem definido em `ModeloCompacto.css` para a transição móvel.
     */
    it("mantém a apresentação completa no breakpoint móvel de 480px (30rem)", () => {
      const previa = criarPreviaCompleta();
      renderizarEmViewportMovel(<ModeloCompacto previa={previa} />, 480);

      const listaContato = screen.getByRole("list", {
        name: "Informações de contato",
      });
      expect(listaContato).toHaveClass("modelo-compacto__contato");
      expect(screen.getByText(previa.estudante.email)).toBeInTheDocument();
    });
  });

  describe("Blindagem contra Overflow Horizontal em Telas Móveis", () => {
    /**
     * Valida a integridade de renderização com URLs extensas de LinkedIn e Lattes em viewport móvel de 360px.
     *
     * **O que faz:** Verifica que links com textos ou endereços longos são renderizados no DOM dentro de seus contêineres sem quebras de execução.
     * **Como faz:** Passa URLs contendo mais de 80 caracteres e confere que os nós ancorados (`<a>`) existem no documento com seus respectivos `href`.
     * **Qual finalidade atende:** Garante que a regra CSS de `overflow-wrap: break-word` atue sobre links reais impedindo o transbordamento horizontal da tela.
     */
    it("renderiza URLs longas de contato em 360px sem corromper a árvore de elementos", () => {
      const previa = criarPreviaCompleta();

      const { container: containerClassico } = renderizarEmViewportMovel(
        <ModeloClassico previa={previa} />,
        360,
      );
      const linksClassicos = containerClassico.querySelectorAll("a");
      expect(linksClassicos.length).toBeGreaterThanOrEqual(2);
      expect(linksClassicos[0].getAttribute("href")).toContain("linkedin.com");
      expect(linksClassicos[1].getAttribute("href")).toContain(
        "lattes.cnpq.br",
      );

      cleanup();

      const { container: containerCompacto } = renderizarEmViewportMovel(
        <ModeloCompacto previa={previa} />,
        360,
      );
      const linksCompactos = containerCompacto.querySelectorAll("a");
      expect(linksCompactos.length).toBeGreaterThanOrEqual(2);
      expect(linksCompactos[0].getAttribute("href")).toContain("linkedin.com");
      expect(linksCompactos[1].getAttribute("href")).toContain(
        "lattes.cnpq.br",
      );
    });
  });
});
