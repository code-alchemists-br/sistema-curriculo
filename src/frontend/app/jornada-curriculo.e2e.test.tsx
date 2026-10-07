// Proveniência: decision-analysis prompts/frontend/20261007-081300-cenario-e2e-preenchimento-curriculo-v001.md#v001
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useMemo, useState } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { Student } from "../entities/student";
import {
  FalhaDadosPessoais,
  type ClienteDadosPessoais
} from "../features/edit-personal-data";
import type {
  CurriculoParaValidacao,
  EstadoSecaoObrigatoria
} from "../features/validate-curriculum";
import { PaginaDadosPessoais } from "../pages/personal-data";
import { PaginaValidacaoCurriculo } from "../pages/validacao-curriculo";

afterEach(cleanup);

/**
 * Propriedades de configuração do orquestrador de testes da jornada do estudante.
 *
 * **O que faz:** Estrutura os parâmetros de entrada e dependências necessárias para a simulação da jornada.
 * **Como faz:** Agrupa o double de persistência de dados pessoais, estados das etapas curriculares e callbacks de ações finais.
 * **Qual finalidade atende:** Permite que a suíte de testes E2E configure diferentes cenários da jornada (caminho feliz, bloqueios e falhas).
 */
export interface JornadaCurriculoHarnessProps {
  clienteDadosPessoais: ClienteDadosPessoais;
  formacaoAcademica?: EstadoSecaoObrigatoria;
  experienciasProfissionais?: EstadoSecaoObrigatoria;
  competencias?: CurriculoParaValidacao["competencias"];
  projetosAcademicos?: CurriculoParaValidacao["projetosAcademicos"];
  onVisualizarPreview?: () => void;
  onExportarPdf?: () => void;
  onConfirmarCurriculo?: () => void;
}

/**
 * Componente harness orquestrador da jornada interativa de preenchimento e revisão.
 *
 * **O que faz:** Integra a etapa inicial de dados pessoais e contato com a tela de revisão e validação final do currículo.
 * **Como faz:** Controla a etapa ativa do Wizard, intercepta a persistência assíncrona dos dados pessoais pelo double e compõe o modelo de validação completo para exibição na etapa de revisão.
 * **Qual finalidade atende:** Viabiliza o teste automatizado E2E de ponta a ponta reproduzindo fielmente o comportamento observado pelo estudante no navegador.
 */
export function JornadaCurriculoHarness({
  clienteDadosPessoais,
  formacaoAcademica = { status: "preenchida" },
  experienciasProfissionais = { status: "preenchida" },
  competencias = {
    hardSkills: ["TypeScript", "React"],
    softSkills: ["Comunicação", "Trabalho em equipe"]
  },
  projetosAcademicos = [
    {
      titulo: "Sistema de Currículo",
      descricao: "Plataforma web para elaboração de currículos universitários",
      tecnologias: "React, TypeScript"
    }
  ],
  onVisualizarPreview,
  onExportarPdf,
  onConfirmarCurriculo
}: JornadaCurriculoHarnessProps) {
  const [etapa, setEtapa] = useState<"dados-pessoais" | "revisao">("dados-pessoais");
  const [dadosSalvos, setDadosSalvos] = useState<Student | null>(null);

  const clienteInterceptador: ClienteDadosPessoais = useMemo(
    () => ({
      salvar: async (student: Student) => {
        await clienteDadosPessoais.salvar(student);
        setDadosSalvos(student);
      }
    }),
    [clienteDadosPessoais]
  );

  const dadosConsolidados: CurriculoParaValidacao = useMemo(
    () => ({
      dadosPessoais: dadosSalvos
        ? {
            nomeCompleto: dadosSalvos.nomeCompleto,
            enderecoCompleto: dadosSalvos.enderecoCompleto,
            telefones: dadosSalvos.telefones,
            email: dadosSalvos.email
          }
        : {
            nomeCompleto: "",
            enderecoCompleto: "",
            telefones: [],
            email: ""
          },
      formacaoAcademica,
      experienciasProfissionais,
      competencias,
      projetosAcademicos
    }),
    [dadosSalvos, formacaoAcademica, experienciasProfissionais, competencias, projetosAcademicos]
  );

  return (
    <div>
      <nav aria-label="Navegação do Wizard">
        <ol>
          <li aria-current={etapa === "dados-pessoais" ? "step" : undefined}>
            Etapa 1: Dados pessoais
          </li>
          <li aria-current={etapa === "revisao" ? "step" : undefined}>
            Etapa 2: Revisão e validação
          </li>
        </ol>
      </nav>

      <section
        aria-label="Etapa de dados pessoais"
        hidden={etapa !== "dados-pessoais"}
      >
        <PaginaDadosPessoais cliente={clienteInterceptador} />
        <div style={{ marginTop: "1rem" }}>
          <button
            type="button"
            disabled={dadosSalvos === null}
            onClick={() => setEtapa("revisao")}
          >
            Avançar para revisão
          </button>
        </div>
      </section>

      <section
        aria-label="Etapa de revisão e validação"
        hidden={etapa !== "revisao"}
      >
        <div style={{ marginBottom: "1rem" }}>
          <button
            type="button"
            onClick={() => setEtapa("dados-pessoais")}
          >
            Voltar para dados pessoais
          </button>
        </div>
        <PaginaValidacaoCurriculo
          dados={dadosConsolidados}
          onConfirmarCurriculo={onConfirmarCurriculo}
          onExportarPdf={onExportarPdf}
          onVisualizarPreview={onVisualizarPreview}
        />
      </section>
    </div>
  );
}

/**
 * Preenche os campos interativos de dados pessoais durante o fluxo do teste E2E.
 *
 * **O que faz:** Digita as informações de identificação e contato nos campos acessíveis da interface.
 * **Como faz:** Utiliza os métodos do `userEvent` para digitar nome, endereço, telefone e e-mail via `getByLabelText`.
 * **Qual finalidade atende:** Automatiza a entrada de dados do estudante reproduzindo a digitação humana no formulário.
 */
async function preencherCamposDadosPessoais(
  usuario: ReturnType<typeof userEvent.setup>,
  dados: {
    nomeCompleto: string;
    enderecoCompleto: string;
    telefone: string;
    email: string;
  }
): Promise<void> {
  await usuario.type(screen.getByLabelText("Nome completo"), dados.nomeCompleto);
  await usuario.type(screen.getByLabelText("Endereço completo"), dados.enderecoCompleto);
  await usuario.type(screen.getByLabelText("Telefone 1"), dados.telefone);
  await usuario.type(screen.getByLabelText("E-mail"), dados.email);
}

describe("Jornada E2E de Preenchimento e Revisão de Currículo", () => {
  /**
   * Valida o fluxo feliz completo da jornada do estudante.
   *
   * **O que faz:** Testa o preenchimento de dados pessoais com inclusão de múltiplos telefones, salvamento com double, navegação para revisão e acionamento das ações de prévia, confirmação e exportação de PDF.
   * **Como faz:** Simula a interação completa via `userEvent`, aguarda os feedbacks com `role="status"` e valida as chamadas dos doubles.
   * **Qual finalidade atende:** Garante que o estudante consegue concluir com sucesso a jornada inteira sem bloqueios indevidos quando todos os dados são válidos.
   */
  it("conclui a jornada com sucesso desde o preenchimento de dados pessoais até a liberação e disparo das ações de exportação", async () => {
    const usuario = userEvent.setup();
    const clienteDadosPessoais: ClienteDadosPessoais = {
      salvar: vi.fn().mockResolvedValue(undefined)
    };
    const onVisualizarPreview = vi.fn();
    const onConfirmarCurriculo = vi.fn();
    const onExportarPdf = vi.fn();

    render(
      <JornadaCurriculoHarness
        clienteDadosPessoais={clienteDadosPessoais}
        onConfirmarCurriculo={onConfirmarCurriculo}
        onExportarPdf={onExportarPdf}
        onVisualizarPreview={onVisualizarPreview}
      />
    );

    // 1. Início da jornada: dados pessoais
    expect(screen.getByRole("heading", { name: "Conte um pouco sobre você" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Avançar para revisão" })).toBeDisabled();

    // 2. Preenchimento de dados pessoais com telefone adicional
    await preencherCamposDadosPessoais(usuario, {
      nomeCompleto: "Mariana Souza",
      enderecoCompleto: "Avenida Paulista, 1000 - Bela Vista, São Paulo - SP",
      telefone: "(11) 98765-4321",
      email: "mariana.souza@universidade.edu.br"
    });

    await usuario.click(screen.getByRole("button", { name: "+ Adicionar telefone" }));
    await usuario.type(screen.getByLabelText("Telefone 2"), "(11) 91234-5678");

    // 3. Submissão do formulário de dados pessoais
    await usuario.click(screen.getByRole("button", { name: "Salvar dados pessoais" }));

    // 4. Verificação do feedback de sucesso e liberação de navegação
    expect(await screen.findByRole("status")).toHaveTextContent("Dados pessoais salvos com sucesso.");
    expect(clienteDadosPessoais.salvar).toHaveBeenCalledWith({
      nomeCompleto: "Mariana Souza",
      enderecoCompleto: "Avenida Paulista, 1000 - Bela Vista, São Paulo - SP",
      telefones: ["(11) 98765-4321", "(11) 91234-5678"],
      email: "mariana.souza@universidade.edu.br"
    });

    const botaoAvancar = screen.getByRole("button", { name: "Avançar para revisão" });
    expect(botaoAvancar).toBeEnabled();

    // 5. Transição para a etapa final de revisão
    await usuario.click(botaoAvancar);

    // 6. Verificação do estado consolidado na tela de validação
    expect(screen.getByRole("heading", { name: "Valide os dados do currículo" })).toBeInTheDocument();
    expect(screen.getByRole("status")).toHaveTextContent("Todas as seções obrigatórias estão válidas.");

    // Verifica que todas as seções obrigatórias aparecem como válidas
    expect(screen.getByText("Dados pessoais")).toBeInTheDocument();
    expect(screen.getByText("Formação acadêmica")).toBeInTheDocument();
    expect(screen.getByText("Experiências profissionais")).toBeInTheDocument();
    expect(screen.getByText("Competências")).toBeInTheDocument();

    const statusesValidos = screen.getAllByText(/Válida/);
    expect(statusesValidos.length).toBeGreaterThanOrEqual(4);

    // 7. Verificação e acionamento das ações liberadas
    const botaoPreview = screen.getByRole("button", { name: "Visualizar prévia" });
    const botaoConfirmar = screen.getByRole("button", { name: "Confirmar currículo" });
    const botaoExportarPdf = screen.getByRole("button", { name: "Exportar PDF" });

    expect(botaoPreview).toBeEnabled();
    expect(botaoConfirmar).toBeEnabled();
    expect(botaoExportarPdf).toBeEnabled();

    await usuario.click(botaoPreview);
    await usuario.click(botaoConfirmar);
    await usuario.click(botaoExportarPdf);

    expect(onVisualizarPreview).toHaveBeenCalledTimes(1);
    expect(onConfirmarCurriculo).toHaveBeenCalledTimes(1);
    expect(onExportarPdf).toHaveBeenCalledTimes(1);
  });

  /**
   * Valida o bloqueio de ações na revisão quando existe etapa curricular pendente.
   *
   * **O que faz:** Simula um fluxo onde a formação acadêmica foi pulada, verifica a exibição do alerta de pendência e a desabilitação dos botões de ação final.
   * **Como faz:** Injeta uma seção obrigatória com `status: "pulada"` no harness, avança até a revisão e assegura que os botões permanecem desabilitados.
   * **Qual finalidade atende:** Garante que currículos incompletos não permitam confirmação ou exportação indevida de PDF.
   */
  it("bloqueia as ações de confirmação e exportação de PDF quando uma seção obrigatória está pendente", async () => {
    const usuario = userEvent.setup();
    const clienteDadosPessoais: ClienteDadosPessoais = {
      salvar: vi.fn().mockResolvedValue(undefined)
    };
    const onVisualizarPreview = vi.fn();
    const onConfirmarCurriculo = vi.fn();
    const onExportarPdf = vi.fn();

    render(
      <JornadaCurriculoHarness
        clienteDadosPessoais={clienteDadosPessoais}
        formacaoAcademica={{
          status: "pulada",
          mensagemErro: "A formação acadêmica é obrigatória antes de continuar."
        }}
        onConfirmarCurriculo={onConfirmarCurriculo}
        onExportarPdf={onExportarPdf}
        onVisualizarPreview={onVisualizarPreview}
      />
    );

    await preencherCamposDadosPessoais(usuario, {
      nomeCompleto: "Carlos Alberto",
      enderecoCompleto: "Rua das Amoreiras, 50 - Campinas - SP",
      telefone: "(19) 99888-7766",
      email: "carlos.alberto@email.com"
    });

    await usuario.click(screen.getByRole("button", { name: "Salvar dados pessoais" }));
    expect(await screen.findByRole("status")).toHaveTextContent("salvos com sucesso");

    await usuario.click(screen.getByRole("button", { name: "Avançar para revisão" }));

    // Verificação de bloqueio na revisão
    expect(screen.getByRole("alert")).toHaveTextContent(
      "Há pendências que precisam ser corrigidas antes de continuar."
    );
    expect(screen.getByText("Formação acadêmica")).toBeInTheDocument();
    expect(screen.getByText(/Pendente/)).toBeInTheDocument();
    expect(screen.getByText("A formação acadêmica é obrigatória antes de continuar.")).toBeInTheDocument();

    const botaoPreview = screen.getByRole("button", { name: "Visualizar prévia" });
    const botaoConfirmar = screen.getByRole("button", { name: "Confirmar currículo" });
    const botaoExportarPdf = screen.getByRole("button", { name: "Exportar PDF" });

    expect(botaoPreview).toBeDisabled();
    expect(botaoConfirmar).toBeDisabled();
    expect(botaoExportarPdf).toBeDisabled();

    // Validação de que cliques não disparam callbacks
    await usuario.click(botaoPreview);
    await usuario.click(botaoConfirmar);
    await usuario.click(botaoExportarPdf);

    expect(onVisualizarPreview).not.toHaveBeenCalled();
    expect(onConfirmarCurriculo).not.toHaveBeenCalled();
    expect(onExportarPdf).not.toHaveBeenCalled();
  });

  /**
   * Valida a resiliência da interface diante de falha temporária no serviço de persistência.
   *
   * **O que faz:** Testa o tratamento de erro assíncrono durante o salvamento de dados pessoais, assegurando a preservação das entradas digitadas e o bloqueio do avanço.
   * **Como faz:** Configura o double para rejeitar a operação com `FalhaDadosPessoais("indisponivel")` e verifica a mensagem com `role="alert"`.
   * **Qual finalidade atende:** Garante que o estudante não perca os dados digitados e não avance na jornada em caso de falha de persistência.
   */
  it("preserva os dados preenchidos e impede o avanço quando o double indica indisponibilidade", async () => {
    const usuario = userEvent.setup();
    const clienteDadosPessoais: ClienteDadosPessoais = {
      salvar: vi.fn().mockRejectedValue(new FalhaDadosPessoais("indisponivel"))
    };

    render(
      <JornadaCurriculoHarness
        clienteDadosPessoais={clienteDadosPessoais}
      />
    );

    await preencherCamposDadosPessoais(usuario, {
      nomeCompleto: "Juliana Mendes",
      enderecoCompleto: "Rua do Comércio, 120 - Santos - SP",
      telefone: "(13) 97777-6655",
      email: "juliana.mendes@email.com"
    });

    await usuario.click(screen.getByRole("button", { name: "Salvar dados pessoais" }));

    // Verificação de erro amigável sem perda de dados
    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Não foi possível salvar os dados pessoais no momento. Tente novamente mais tarde."
    );

    expect(screen.getByLabelText("Nome completo")).toHaveValue("Juliana Mendes");
    expect(screen.getByLabelText("Endereço completo")).toHaveValue("Rua do Comércio, 120 - Santos - SP");
    expect(screen.getByLabelText("Telefone 1")).toHaveValue("(13) 97777-6655");
    expect(screen.getByLabelText("E-mail")).toHaveValue("juliana.mendes@email.com");

    // Não deve permitir avançar para revisão
    expect(screen.getByRole("button", { name: "Avançar para revisão" })).toBeDisabled();
  });

  /**
   * Valida o fluxo de retorno e edição de dados durante a jornada.
   *
   * **O que faz:** Permite que o estudante retorne da revisão para a etapa anterior, altere uma informação e veja o resultado atualizado na revisão.
   * **Como faz:** Conclui o fluxo inicial, aciona o botão de retorno, atualiza o nome via `userEvent`, salva novamente e confirma a transição para revisão.
   * **Qual finalidade atende:** Garante a navegabilidade bidirecional da jornada conforme especificado na regra de negócio de revisão e edição.
   */
  it("permite retornar da revisão para editar os dados pessoais e avançar novamente", async () => {
    const usuario = userEvent.setup();
    const clienteDadosPessoais: ClienteDadosPessoais = {
      salvar: vi.fn().mockResolvedValue(undefined)
    };

    render(
      <JornadaCurriculoHarness
        clienteDadosPessoais={clienteDadosPessoais}
      />
    );

    // Preenche dados iniciais
    await preencherCamposDadosPessoais(usuario, {
      nomeCompleto: "Beatriz Lima",
      enderecoCompleto: "Rua Alvorada, 300 - Curitiba - PR",
      telefone: "(41) 98888-1111",
      email: "beatriz.lima@email.com"
    });

    await usuario.click(screen.getByRole("button", { name: "Salvar dados pessoais" }));
    expect(await screen.findByRole("status")).toHaveTextContent("salvos com sucesso");

    // Avança para a revisão
    await usuario.click(screen.getByRole("button", { name: "Avançar para revisão" }));
    expect(screen.getByRole("heading", { name: "Valide os dados do currículo" })).toBeInTheDocument();

    // Retorna para a etapa de dados pessoais
    await usuario.click(screen.getByRole("button", { name: "Voltar para dados pessoais" }));
    expect(screen.getByRole("heading", { name: "Conte um pouco sobre você" })).toBeInTheDocument();

    // Campo de nome deve conter o valor anterior
    const campoNome = screen.getByLabelText("Nome completo");
    expect(campoNome).toHaveValue("Beatriz Lima");

    // Atualiza o nome e salva novamente
    await usuario.clear(campoNome);
    await usuario.type(campoNome, "Beatriz Alencar Lima");
    await usuario.click(screen.getByRole("button", { name: "Salvar dados pessoais" }));
    expect(await screen.findByRole("status")).toHaveTextContent("salvos com sucesso");

    expect(clienteDadosPessoais.salvar).toHaveBeenLastCalledWith(
      expect.objectContaining({
        nomeCompleto: "Beatriz Alencar Lima"
      })
    );

    // Avança novamente para a revisão
    await usuario.click(screen.getByRole("button", { name: "Avançar para revisão" }));
    expect(screen.getByRole("heading", { name: "Valide os dados do currículo" })).toBeInTheDocument();
    expect(screen.getByRole("status")).toHaveTextContent("Todas as seções obrigatórias estão válidas.");
  });
});
