import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import { FormularioCertificacao } from "./FormularioCertificacao";

afterEach(cleanup);

describe("FormularioCertificacao", () => {
  it("renderiza os campos com rótulos semânticos e identificadores associados", () => {
    render(<FormularioCertificacao />);

    const campoNome = screen.getByLabelText("Nome da certificação");
    const campoEmissor = screen.getByLabelText("Organização emissora");
    const botaoSalvar = screen.getByRole("button", {
      name: "Salvar certificação",
    });

    expect(campoNome).toBeInTheDocument();
    expect(campoNome).toHaveAttribute("id", "certificacao-nome");
    expect(campoEmissor).toBeInTheDocument();
    expect(campoEmissor).toHaveAttribute("id", "certificacao-emissor");
    expect(botaoSalvar).toBeEnabled();
  });

  it("associa mensagens de erro via aria-describedby e aria-invalid ao submeter campos vazios", async () => {
    const usuario = userEvent.setup();
    const onSalvar = vi.fn();

    render(<FormularioCertificacao onSalvar={onSalvar} />);

    const botaoSalvar = screen.getByRole("button", {
      name: "Salvar certificação",
    });
    await usuario.click(botaoSalvar);

    expect(onSalvar).not.toHaveBeenCalled();

    const alerta = screen.getByRole("alert");
    expect(alerta).toHaveTextContent(
      "Corrija os campos destacados antes de salvar a certificação.",
    );

    const campoNome = screen.getByLabelText("Nome da certificação");
    expect(campoNome).toHaveAttribute("aria-invalid", "true");
    expect(campoNome).toHaveAttribute(
      "aria-describedby",
      "certificacao-nome-erro",
    );
    expect(screen.getByText("Informe o nome da certificação.")).toHaveAttribute(
      "id",
      "certificacao-nome-erro",
    );

    const campoEmissor = screen.getByLabelText("Organização emissora");
    expect(campoEmissor).toHaveAttribute("aria-invalid", "true");
    expect(campoEmissor).toHaveAttribute(
      "aria-describedby",
      "certificacao-emissor-erro",
    );
    expect(
      screen.getByText("Informe a instituição ou organização emissora."),
    ).toHaveAttribute("id", "certificacao-emissor-erro");
  });

  it("limpa o erro e o feedback ativo ao digitar em um campo inválido", async () => {
    const usuario = userEvent.setup();

    render(<FormularioCertificacao />);

    await usuario.click(
      screen.getByRole("button", { name: "Salvar certificação" }),
    );

    const campoNome = screen.getByLabelText("Nome da certificação");
    expect(campoNome).toHaveAttribute("aria-invalid", "true");

    await usuario.type(campoNome, "AWS Cloud Practitioner");

    expect(campoNome).not.toHaveAttribute("aria-invalid");
    expect(
      screen.queryByText("Informe o nome da certificação."),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByText(
        "Corrija os campos destacados antes de salvar a certificação.",
      ),
    ).not.toBeInTheDocument();

    const campoEmissor = screen.getByLabelText("Organização emissora");
    expect(campoEmissor).toHaveAttribute("aria-invalid", "true");
  });

  it("executa submissão controlada com dados normalizados e anuncia sucesso via role status", async () => {
    const usuario = userEvent.setup();
    const onSalvar = vi.fn().mockResolvedValue(undefined);

    render(<FormularioCertificacao onSalvar={onSalvar} />);

    const campoNome = screen.getByLabelText("Nome da certificação");
    const campoEmissor = screen.getByLabelText("Organização emissora");

    await usuario.type(campoNome, "   Scrum    Master   Professional  ");
    await usuario.type(campoEmissor, "   Scrum.org   ");

    await usuario.click(
      screen.getByRole("button", { name: "Salvar certificação" }),
    );

    expect(onSalvar).toHaveBeenCalledTimes(1);
    expect(onSalvar).toHaveBeenCalledWith({
      nome: "Scrum Master Professional",
      organizacaoEmissora: "Scrum.org",
    });

    const status = await screen.findByRole("status");
    expect(status).toHaveTextContent("Certificação salva com sucesso.");

    expect(campoNome).toHaveValue("");
    expect(campoEmissor).toHaveValue("");
  });

  it("desabilita os controles e previne envios concorrentes durante o processamento assíncrono", async () => {
    const usuario = userEvent.setup();
    let resolverEnvio: (() => void) | undefined;
    const onSalvar = vi.fn(
      () =>
        new Promise<void>((resolve) => {
          resolverEnvio = resolve;
        }),
    );

    render(<FormularioCertificacao onSalvar={onSalvar} />);

    await usuario.type(
      screen.getByLabelText("Nome da certificação"),
      "Oracle Java Certified",
    );
    await usuario.type(screen.getByLabelText("Organização emissora"), "Oracle");

    const botaoSalvar = screen.getByRole("button", {
      name: "Salvar certificação",
    });
    await usuario.click(botaoSalvar);

    expect(
      screen.getByRole("button", { name: "Salvando certificação..." }),
    ).toBeDisabled();
    expect(screen.getByLabelText("Nome da certificação")).toBeDisabled();
    expect(screen.getByLabelText("Organização emissora")).toBeDisabled();

    // Tentativa de segundo clique enquanto está desabilitado
    await usuario.click(
      screen.getByRole("button", { name: "Salvando certificação..." }),
    );
    expect(onSalvar).toHaveBeenCalledTimes(1);

    resolverEnvio?.();

    expect(
      await screen.findByRole("button", { name: "Salvar certificação" }),
    ).toBeEnabled();
    expect(await screen.findByRole("status")).toHaveTextContent(
      "Certificação salva com sucesso.",
    );
  });

  it("comunica erro com role alert caso o salvamento falhe e preserva os dados para correção", async () => {
    const usuario = userEvent.setup();
    const onSalvar = vi
      .fn()
      .mockRejectedValue(new Error("Falha temporária de rede"));

    render(<FormularioCertificacao onSalvar={onSalvar} />);

    const campoNome = screen.getByLabelText("Nome da certificação");
    const campoEmissor = screen.getByLabelText("Organização emissora");

    await usuario.type(campoNome, "Kubernetes CKA");
    await usuario.type(campoEmissor, "Cloud Native Computing Foundation");

    await usuario.click(
      screen.getByRole("button", { name: "Salvar certificação" }),
    );

    const alerta = await screen.findByRole("alert");
    expect(alerta).toHaveTextContent(
      "Não foi possível salvar a certificação. Tente novamente.",
    );

    expect(campoNome).toHaveValue("Kubernetes CKA");
    expect(campoEmissor).toHaveValue("Cloud Native Computing Foundation");
    expect(
      screen.getByRole("button", { name: "Salvar certificação" }),
    ).toBeEnabled();
  });

  it("adiciona e remove entradas de certificação dinamicamente", async () => {
    const usuario = userEvent.setup();
    render(<FormularioCertificacao />);

    expect(screen.getAllByLabelText("Nome da certificação")).toHaveLength(1);

    await usuario.click(
      screen.getByRole("button", { name: "+ Adicionar certificação" }),
    );

    expect(screen.getAllByLabelText("Nome da certificação")).toHaveLength(2);
    expect(
      screen.getByRole("button", { name: "Remover certificação 2" }),
    ).toBeInTheDocument();

    await usuario.click(
      screen.getByRole("button", { name: "Remover certificação 2" }),
    );

    expect(screen.getAllByLabelText("Nome da certificação")).toHaveLength(1);
  });
});
