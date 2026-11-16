import { act, cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

afterEach(cleanup);

import { PaginaCursosCertificacoes } from "./PaginaCursosCertificacoes";

const curso = { nome: " React ", instituicao: " Fatec ", cargaHoraria: " 40 " };
const certificacao = { nome: " AWS  Cloud ", organizacaoEmissora: " Amazon " };

describe("cadastro de cursos e certificações pelo Próximo real", () => {
  it("permite pular as duas seções totalmente vazias sem inventar cadastros", async () => {
    const onAvancar = vi.fn();
    render(<PaginaCursosCertificacoes onAvancar={onAvancar} />);
    await userEvent.click(
      screen.getByRole("button", { name: "Avançar para próxima etapa" }),
    );
    expect(onAvancar).toHaveBeenCalledExactlyOnceWith([], []);
  });

  it("bloqueia curso parcial, associa o erro ao campo e foca o primeiro inválido", async () => {
    const onAvancar = vi.fn();
    render(
      <PaginaCursosCertificacoes
        cursosIniciais={[{ ...curso, instituicao: "" }]}
        onAvancar={onAvancar}
      />,
    );
    await userEvent.click(
      screen.getByRole("button", { name: "Avançar para próxima etapa" }),
    );
    expect(onAvancar).not.toHaveBeenCalled();
    expect(screen.getByLabelText("Instituição")).toHaveAttribute(
      "aria-invalid",
      "true",
    );
    expect(screen.getByLabelText("Instituição")).toHaveAccessibleDescription(
      "Informe a instituição.",
    );
    expect(screen.getByLabelText("Instituição")).toHaveFocus();
  });

  it("bloqueia certificação parcial mesmo com curso válido", async () => {
    const onAvancar = vi.fn();
    render(
      <PaginaCursosCertificacoes
        cursosIniciais={[curso]}
        certificacoesIniciais={[{ ...certificacao, organizacaoEmissora: "" }]}
        onAvancar={onAvancar}
      />,
    );
    await userEvent.click(
      screen.getByRole("button", { name: "Avançar para próxima etapa" }),
    );
    expect(onAvancar).not.toHaveBeenCalled();
    expect(screen.getByLabelText("Organização emissora")).toHaveAttribute(
      "aria-invalid",
      "true",
    );
    expect(screen.getByLabelText("Organização emissora")).toHaveFocus();
  });

  it("não arredonda nem aceita carga horária fracionada", async () => {
    const onAvancar = vi.fn();
    render(
      <PaginaCursosCertificacoes
        cursosIniciais={[{ ...curso, cargaHoraria: "1.5" }]}
        onAvancar={onAvancar}
      />,
    );
    await userEvent.click(
      screen.getByRole("button", { name: "Avançar para próxima etapa" }),
    );
    expect(onAvancar).not.toHaveBeenCalled();
    expect(screen.getByLabelText("Carga horária (horas)")).toHaveAttribute(
      "aria-invalid",
      "true",
    );
  });

  it("avança por teclado com listas normalizadas e ignora somente entradas inteiramente vazias", async () => {
    const onAvancar = vi.fn();
    render(
      <PaginaCursosCertificacoes
        cursosIniciais={[
          curso,
          { nome: "", instituicao: "", cargaHoraria: "" },
        ]}
        certificacoesIniciais={[certificacao]}
        onAvancar={onAvancar}
      />,
    );
    screen.getByRole("button", { name: "Avançar para próxima etapa" }).focus();
    await userEvent.keyboard("{Enter}");
    expect(onAvancar).toHaveBeenCalledExactlyOnceWith(
      [{ nome: "React", instituicao: "Fatec", cargaHoraria: "40" }],
      [{ nome: "AWS Cloud", organizacaoEmissora: "Amazon" }],
    );
  });

  it("permite remover e desfazer o último curso e a última certificação", async () => {
    const usuario = userEvent.setup();
    render(
      <PaginaCursosCertificacoes
        cursosIniciais={[curso]}
        certificacoesIniciais={[certificacao]}
      />,
    );
    await usuario.click(
      screen.getByRole("button", { name: "Remover curso 1" }),
    );
    expect(screen.queryByLabelText("Nome do curso")).not.toBeInTheDocument();
    await usuario.click(
      screen.getByRole("button", { name: "Desfazer remoção do curso" }),
    );
    expect(screen.getByLabelText("Nome do curso")).toHaveValue(" React ");
    await usuario.click(
      screen.getByRole("button", { name: "Remover certificação 1" }),
    );
    expect(
      screen.queryByLabelText("Nome da certificação"),
    ).not.toBeInTheDocument();
    await usuario.click(
      screen.getByRole("button", { name: "Desfazer remoção da certificação" }),
    );
    expect(screen.getByLabelText("Nome da certificação")).toHaveValue(
      " AWS  Cloud ",
    );
  });

  it("aguarda o envio sem aceitar cliques concorrentes ou alteração dos dados", async () => {
    let concluir!: () => void;
    const pendente = new Promise<void>((resolve) => {
      concluir = resolve;
    });
    const onAvancar = vi.fn(() => pendente);
    render(
      <PaginaCursosCertificacoes
        cursosIniciais={[curso]}
        onAvancar={onAvancar}
      />,
    );
    const proximo = screen.getByRole("button", {
      name: "Avançar para próxima etapa",
    });
    await userEvent.dblClick(proximo);
    expect(onAvancar).toHaveBeenCalledTimes(1);
    expect(proximo).toBeDisabled();
    expect(screen.getByLabelText("Nome do curso")).toBeDisabled();
    expect(
      screen.getByRole("button", { name: "Voltar para a etapa anterior" }),
    ).toBeDisabled();
    await act(async () => concluir());
    await waitFor(() => expect(proximo).toBeEnabled());
  });

  it("comunica falha, preserva os dados e permite tentar novamente", async () => {
    const onAvancar = vi
      .fn()
      .mockRejectedValueOnce(new Error("offline"))
      .mockResolvedValueOnce(undefined);
    render(
      <PaginaCursosCertificacoes
        cursosIniciais={[curso]}
        onAvancar={onAvancar}
      />,
    );
    const proximo = screen.getByRole("button", {
      name: "Avançar para próxima etapa",
    });
    await userEvent.click(proximo);
    expect(await screen.findByRole("alert")).toHaveTextContent(
      /não foi possível salvar/i,
    );
    expect(screen.getByLabelText("Nome do curso")).toHaveValue(" React ");
    await userEvent.click(proximo);
    expect(onAvancar).toHaveBeenCalledTimes(2);
    await waitFor(() =>
      expect(screen.queryByRole("alert")).not.toBeInTheDocument(),
    );
  });
});
