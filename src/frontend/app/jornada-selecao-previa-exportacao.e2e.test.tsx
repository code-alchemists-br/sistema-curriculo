// Proveniência: Issue #373 (F9.4) — cenário E2E de criação, seleção, prévia e exportação.
import { cleanup, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useMemo, useState } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { Student } from "../entities/student";
import type { ClienteDadosPessoais } from "../features/edit-personal-data";
import type { CurriculoParaValidacao } from "../features/validate-curriculum";
import { PaginaDadosPessoais } from "../pages/personal-data";
import { PaginaValidacaoCurriculo } from "../pages/validacao-curriculo";

afterEach(cleanup);

/**
 * Item do perfil do estudante que pode integrar uma versão de currículo.
 *
 * **O que faz:** descreve um item selecionável com identificador e rótulo.
 * **Como faz:** estrutura mínima de dados usada pelo catálogo do cenário.
 * **Qual finalidade atende:** simular o catálogo de itens do perfil, cuja UI e
 * API de seleção ainda não estão em `dev`.
 */
interface ItemPerfil {
  id: string;
  rotulo: string;
}

/**
 * Porta de exportação simulada que devolve o binário a ser baixado.
 *
 * **O que faz:** define o contrato assíncrono de geração de PDF.
 * **Como faz:** recebe o currículo validado e resolve com um `Blob`.
 * **Qual finalidade atende:** permitir mock de resposta de download enquanto o
 * gerador real de binários não existe em `dev`.
 */
interface ExportadorPdf {
  exportar(curriculo: CurriculoParaValidacao): Promise<Blob>;
}

const FORMACOES: ItemPerfil[] = [
  { id: "f1", rotulo: "Bacharelado em Ciência da Computação" }
];
const EXPERIENCIAS: ItemPerfil[] = [
  { id: "e1", rotulo: "Estágio em Desenvolvimento Web" },
  { id: "e2", rotulo: "Monitoria de Algoritmos" }
];
const COMPETENCIAS: ItemPerfil[] = [
  { id: "c1", rotulo: "TypeScript" },
  { id: "c2", rotulo: "Comunicação" }
];

/**
 * Orquestra a jornada criação → seleção → revisão → prévia → exportação.
 *
 * **O que faz:** encadeia as telas reais de dados pessoais e validação com uma
 * etapa de seleção de itens e uma prévia, ambas simuladas localmente.
 * **Como faz:** guarda os dados salvos e os itens marcados, deriva o modelo de
 * validação a partir deles (seção sem item marcado vira "pulada"), exibe a
 * prévia a partir da seleção e delega o download ao exportador injetado.
 * **Qual finalidade atende:** permitir o teste E2E do fluxo completo sem
 * depender de rotas de seleção/prévia ainda não integradas nem de geradores
 * de binário.
 */
function JornadaCompletaHarness({
  cliente,
  exportador
}: {
  cliente: ClienteDadosPessoais;
  exportador: ExportadorPdf;
}) {
  const [etapa, setEtapa] = useState<"dados" | "selecao" | "revisao">("dados");
  const [dados, setDados] = useState<Student | null>(null);
  const [marcados, setMarcados] = useState<Set<string>>(new Set());
  const [previaAberta, setPreviaAberta] = useState(false);
  const [download, setDownload] = useState<string | null>(null);

  const clienteInterceptador = useMemo<ClienteDadosPessoais>(
    () => ({
      salvar: async (student) => {
        await cliente.salvar(student);
        setDados(student);
      }
    }),
    [cliente]
  );

  function alternar(id: string): void {
    setMarcados((atuais) => {
      const novos = new Set(atuais);
      if (novos.has(id)) novos.delete(id);
      else novos.add(id);
      return novos;
    });
    setPreviaAberta(false);
  }

  const selecionados = (itens: ItemPerfil[]) => itens.filter((item) => marcados.has(item.id));

  const curriculo: CurriculoParaValidacao = {
    dadosPessoais: {
      nomeCompleto: dados?.nomeCompleto ?? "",
      enderecoCompleto: dados?.enderecoCompleto ?? "",
      telefones: dados?.telefones ?? [],
      email: dados?.email ?? ""
    },
    formacaoAcademica:
      selecionados(FORMACOES).length > 0
        ? { status: "preenchida" }
        : { status: "pulada", mensagemErro: "Selecione ao menos uma formação." },
    experienciasProfissionais:
      selecionados(EXPERIENCIAS).length > 0
        ? { status: "preenchida" }
        : { status: "pulada", mensagemErro: "Selecione ao menos uma experiência." },
    competencias: {
      hardSkills: selecionados(COMPETENCIAS.slice(0, 1)).map((item) => item.rotulo),
      softSkills: selecionados(COMPETENCIAS.slice(1)).map((item) => item.rotulo)
    },
    projetosAcademicos: []
  };

  async function exportar(): Promise<void> {
    const arquivo = await exportador.exportar(curriculo);
    setDownload(`curriculo.pdf (${arquivo.size} bytes)`);
  }

  const grupos: Array<[string, ItemPerfil[]]> = [
    ["Formações", FORMACOES],
    ["Experiências", EXPERIENCIAS],
    ["Competências", COMPETENCIAS]
  ];

  return (
    <div>
      <section aria-label="Etapa de dados" hidden={etapa !== "dados"}>
        <PaginaDadosPessoais cliente={clienteInterceptador} />
        <button type="button" disabled={dados === null} onClick={() => setEtapa("selecao")}>
          Ir para seleção
        </button>
      </section>

      <section aria-label="Etapa de seleção" hidden={etapa !== "selecao"}>
        <h2>Selecione os itens da versão</h2>
        {grupos.map(([titulo, itens]) => (
          <fieldset key={titulo}>
            <legend>{titulo}</legend>
            {itens.map((item) => (
              <label key={item.id}>
                <input
                  type="checkbox"
                  checked={marcados.has(item.id)}
                  onChange={() => alternar(item.id)}
                />
                {item.rotulo}
              </label>
            ))}
          </fieldset>
        ))}
        <button type="button" onClick={() => setEtapa("dados")}>
          Editar dados pessoais
        </button>
        <button type="button" onClick={() => setEtapa("revisao")}>
          Ir para revisão
        </button>
      </section>

      <section aria-label="Etapa de revisão" hidden={etapa !== "revisao"}>
        <button type="button" onClick={() => setEtapa("selecao")}>
          Voltar para seleção
        </button>
        <PaginaValidacaoCurriculo
          dados={curriculo}
          onVisualizarPreview={() => setPreviaAberta(true)}
          onExportarPdf={() => void exportar()}
          onConfirmarCurriculo={() => undefined}
        />
        {previaAberta && (
          <article aria-label="Prévia do currículo">
            <h2>{curriculo.dadosPessoais.nomeCompleto}</h2>
            <ul>
              {[...FORMACOES, ...EXPERIENCIAS, ...COMPETENCIAS]
                .filter((item) => marcados.has(item.id))
                .map((item) => (
                  <li key={item.id}>{item.rotulo}</li>
                ))}
            </ul>
          </article>
        )}
        {download !== null && <p>Download iniciado: {download}</p>}
      </section>
    </div>
  );
}

/**
 * Preenche e salva os dados pessoais pela interface, como o estudante faria.
 *
 * **O que faz:** digita os campos obrigatórios e envia o formulário.
 * **Como faz:** usa `userEvent` sobre os campos acessíveis por rótulo.
 * **Qual finalidade atende:** reutilizar o passo inicial da jornada nos cenários.
 */
async function criarDadosPessoais(
  usuario: ReturnType<typeof userEvent.setup>,
  nome: string
): Promise<void> {
  await usuario.type(screen.getByLabelText("Nome completo"), nome);
  await usuario.type(screen.getByLabelText("Endereço completo"), "Rua das Flores, 10");
  await usuario.type(screen.getByLabelText("Telefone 1"), "(11) 99999-0000");
  await usuario.type(screen.getByLabelText("E-mail"), "ana@exemplo.com");
  await usuario.click(screen.getByRole("button", { name: "Salvar dados pessoais" }));
  await screen.findByText("Dados pessoais salvos com sucesso.");
}

/**
 * Marca itens pelo rótulo na etapa de seleção.
 *
 * **O que faz:** clica nas caixas de seleção dos itens informados.
 * **Como faz:** localiza cada checkbox por papel e nome acessível.
 * **Qual finalidade atende:** expressar a escolha dos itens da versão nos testes.
 */
async function marcar(
  usuario: ReturnType<typeof userEvent.setup>,
  rotulos: string[]
): Promise<void> {
  for (const rotulo of rotulos) {
    await usuario.click(screen.getByRole("checkbox", { name: rotulo }));
  }
}

describe("Jornada E2E: criação, seleção, prévia e exportação", () => {
  /**
   * Cobre o caminho feliz completo, da criação ao download simulado.
   *
   * **O que faz:** cria e edita os dados, seleciona itens, abre a prévia e exporta.
   * **Como faz:** conduz a interface com `userEvent` e verifica o que o usuário vê
   * e o que o double de exportação recebe.
   * **Qual finalidade atende:** garantir que o fluxo F9.4 funciona ponta a ponta.
   */
  it("conclui criação, edição, seleção, prévia e exportação com download simulado", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteDadosPessoais = { salvar: vi.fn().mockResolvedValue(undefined) };
    const exportador: ExportadorPdf = {
      exportar: vi.fn().mockResolvedValue(new Blob(["%PDF-1.4"], { type: "application/pdf" }))
    };
    render(<JornadaCompletaHarness cliente={cliente} exportador={exportador} />);

    // 1. Criação e edição dos dados.
    await criarDadosPessoais(usuario, "Ana Silva");
    await usuario.click(screen.getByRole("button", { name: "Ir para seleção" }));
    await usuario.click(screen.getByRole("button", { name: "Editar dados pessoais" }));
    const nome = screen.getByLabelText("Nome completo");
    await usuario.clear(nome);
    await usuario.type(nome, "Ana Souza Silva");
    await usuario.click(screen.getByRole("button", { name: "Salvar dados pessoais" }));
    await vi.waitFor(() => expect(cliente.salvar).toHaveBeenCalledTimes(2));
    expect(cliente.salvar).toHaveBeenLastCalledWith(
      expect.objectContaining({ nomeCompleto: "Ana Souza Silva" })
    );

    // 2. Seleção dos itens da versão.
    await usuario.click(screen.getByRole("button", { name: "Ir para seleção" }));
    await marcar(usuario, [
      "Bacharelado em Ciência da Computação",
      "Estágio em Desenvolvimento Web",
      "TypeScript"
    ]);
    await usuario.click(screen.getByRole("button", { name: "Ir para revisão" }));

    // 3. Revisão válida e prévia refletindo a seleção.
    expect(screen.getAllByRole("status")[0]).toHaveTextContent(
      "Todas as seções obrigatórias estão válidas."
    );
    await usuario.click(screen.getByRole("button", { name: "Visualizar prévia" }));
    const previa = screen.getByRole("article", { name: "Prévia do currículo" });
    expect(within(previa).getByRole("heading", { name: "Ana Souza Silva" })).toBeInTheDocument();
    expect(within(previa).getByText("Estágio em Desenvolvimento Web")).toBeInTheDocument();
    expect(within(previa).getByText("TypeScript")).toBeInTheDocument();
    expect(within(previa).queryByText("Monitoria de Algoritmos")).not.toBeInTheDocument();

    // 4. Exportação com resposta de download simulada.
    await usuario.click(screen.getByRole("button", { name: "Exportar PDF" }));
    expect(await screen.findByText(/Download iniciado: curriculo\.pdf \(8 bytes\)/)).toBeInTheDocument();
    expect(exportador.exportar).toHaveBeenCalledTimes(1);
    expect(exportador.exportar).toHaveBeenCalledWith(
      expect.objectContaining({
        dadosPessoais: expect.objectContaining({ nomeCompleto: "Ana Souza Silva" }),
        competencias: { hardSkills: ["TypeScript"], softSkills: [] }
      })
    );
  });

  /**
   * Cobre o bloqueio quando a seleção deixa uma seção obrigatória vazia.
   *
   * **O que faz:** seleciona itens sem nenhuma experiência e tenta chegar à prévia.
   * **Como faz:** verifica o alerta, a pendência listada e os botões desabilitados.
   * **Qual finalidade atende:** garantir que seleção incompleta não gera prévia
   * nem exportação.
   */
  it("bloqueia prévia e exportação quando nenhuma experiência foi selecionada", async () => {
    const usuario = userEvent.setup();
    const cliente: ClienteDadosPessoais = { salvar: vi.fn().mockResolvedValue(undefined) };
    const exportador: ExportadorPdf = { exportar: vi.fn() };
    render(<JornadaCompletaHarness cliente={cliente} exportador={exportador} />);

    await criarDadosPessoais(usuario, "Bruno Lima");
    await usuario.click(screen.getByRole("button", { name: "Ir para seleção" }));
    await marcar(usuario, ["Bacharelado em Ciência da Computação", "Comunicação"]);
    await usuario.click(screen.getByRole("button", { name: "Ir para revisão" }));

    expect(screen.getByRole("alert")).toHaveTextContent("Há pendências");
    expect(screen.getByText("Selecione ao menos uma experiência.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Visualizar prévia" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Exportar PDF" })).toBeDisabled();
    expect(screen.queryByRole("article", { name: "Prévia do currículo" })).not.toBeInTheDocument();
    expect(exportador.exportar).not.toHaveBeenCalled();

    // Corrige a seleção e o fluxo é liberado.
    await usuario.click(screen.getByRole("button", { name: "Voltar para seleção" }));
    await marcar(usuario, ["Monitoria de Algoritmos"]);
    await usuario.click(screen.getByRole("button", { name: "Ir para revisão" }));
    expect(screen.getByRole("button", { name: "Exportar PDF" })).toBeEnabled();
  });
});
