import { act, cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { Destaques } from "./Destaques";

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("Destaques", () => {
  it("renderiza o título da seção de métricas com destaque e fechamento", () => {
    render(<Destaques />);

    expect(
      screen.getByRole("heading", {
        name: /CONSTRUÍMOS A PONTE ENTRE O SEU TALENTO/i,
        level: 2,
      }),
    ).toBeInTheDocument();
  });

  it("renderiza os 3 blocos de métricas com seus valores e descrições", () => {
    render(<Destaques />);

    expect(screen.getByText("< 10 min")).toBeInTheDocument();
    expect(screen.getByText(/Do cadastro ao currículo/i)).toBeInTheDocument();

    expect(screen.getByText("100%")).toBeInTheDocument();
    expect(screen.getByText(/Gratuito e sem/i)).toBeInTheDocument();

    expect(screen.getByText("2 formatos")).toBeInTheDocument();
    expect(screen.getByText(/Prontos para envio:/i)).toBeInTheDocument();
  });

  it("ativa a classe de visibilidade imediatamente quando IntersectionObserver não está disponível", () => {
    const { container } = render(<Destaques />);
    const section = container.querySelector(".destaques-section");
    expect(section).toHaveClass("destaques-section--visivel");
  });

  it("dispara a classe de visibilidade quando a seção intercepta a viewport via IntersectionObserver", () => {
    let callbackCapturado: (entries: Partial<IntersectionObserverEntry>[]) => void = () => {};
    const observeMock = vi.fn();
    const disconnectMock = vi.fn();

    class MockIntersectionObserver {
      constructor(cb: (entries: Partial<IntersectionObserverEntry>[]) => void) {
        callbackCapturado = cb;
      }
      observe = observeMock;
      disconnect = disconnectMock;
      unobserve = vi.fn();
    }

    vi.stubGlobal("IntersectionObserver", MockIntersectionObserver);

    const { container } = render(<Destaques />);
    const section = container.querySelector(".destaques-section");

    // Inicialmente não visível até interceptar
    expect(section).not.toHaveClass("destaques-section--visivel");
    expect(observeMock).toHaveBeenCalled();

    // Simula a seção cruzando a viewport
    act(() => {
      callbackCapturado([{ isIntersecting: true }]);
    });

    expect(section).toHaveClass("destaques-section--visivel");
    expect(disconnectMock).toHaveBeenCalled();
  });
});
