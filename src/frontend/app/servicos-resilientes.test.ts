import { describe, expect, it, vi } from "vitest";

import type { Student } from "../entities/student";
import {
  FalhaDadosPessoais,
  type ClienteDadosPessoais,
} from "../features/edit-personal-data";
import {
  FalhaFormacaoAcademica,
  type CadastroFormacaoAcademicaEntrada,
  type ClienteFormacaoAcademica,
} from "../features/cadastrar-formacao-academica";
import {
  FalhaAcessoEstudante,
  type ClienteAcessoEstudante,
} from "../features/acesso-estudante";
import {
  FalhaVagasGrupo2,
  type ClienteVagasGrupo2,
} from "../features/listar-vagas";
import {
  criarClienteAcessoResiliente,
  criarClienteDadosPessoaisResiliente,
  criarClienteFormacaoAcademicaResiliente,
  criarClienteVagasResiliente,
} from "./servicos-resilientes";

const estudanteExemplo: Student = {
  nomeCompleto: "Ana Silva",
  enderecoCompleto: "Av Paulista, 1000, São Paulo",
  cidade: "São Paulo",
  telefones: ["(11) 98765-4321"],
  email: "ana@exemplo.com",
};

const formacaoExemplo: CadastroFormacaoAcademicaEntrada = {
  instituicao: "FATEC",
  curso: "Análise e Desenvolvimento de Sistemas",
  nivel: "tecnologo",
  dataInicio: "2022-02-01",
  dataFim: "2024-12-01",
  status: "concluido",
};

describe("servicos-resilientes", () => {
  describe("criarClienteDadosPessoaisResiliente", () => {
    it("deve delegar a chamada ao cliente http quando a requisição for bem-sucedida", async () => {
      const salvarMock = vi.fn().mockResolvedValue(undefined);
      const clienteHttp: ClienteDadosPessoais = { salvar: salvarMock };
      const cliente = criarClienteDadosPessoaisResiliente(clienteHttp);

      await expect(cliente.salvar(estudanteExemplo)).resolves.toBeUndefined();
      expect(salvarMock).toHaveBeenCalledWith(estudanteExemplo);
    });

    it("deve absorver silenciosamente indisponibilidade de backend sem quebrar o fluxo", async () => {
      const salvarMock = vi
        .fn()
        .mockRejectedValue(new FalhaDadosPessoais("indisponivel"));
      const clienteHttp: ClienteDadosPessoais = { salvar: salvarMock };
      const cliente = criarClienteDadosPessoaisResiliente(clienteHttp);

      await expect(cliente.salvar(estudanteExemplo)).resolves.toBeUndefined();
      expect(salvarMock).toHaveBeenCalled();
    });

    it("deve absorver falha física de conexão de rede (TypeError)", async () => {
      const salvarMock = vi
        .fn()
        .mockRejectedValue(new TypeError("Failed to fetch"));
      const clienteHttp: ClienteDadosPessoais = { salvar: salvarMock };
      const cliente = criarClienteDadosPessoaisResiliente(clienteHttp);

      await expect(cliente.salvar(estudanteExemplo)).resolves.toBeUndefined();
    });

    it("deve repassar falhas de regra de negócio (ex: resposta-invalida) para tratamento da UI", async () => {
      const salvarMock = vi
        .fn()
        .mockRejectedValue(new FalhaDadosPessoais("resposta-invalida"));
      const clienteHttp: ClienteDadosPessoais = { salvar: salvarMock };
      const cliente = criarClienteDadosPessoaisResiliente(clienteHttp);

      await expect(cliente.salvar(estudanteExemplo)).rejects.toThrow(
        "resposta-invalida",
      );
    });

    it("deve lidar com cliente http indefinido sem disparar erros", async () => {
      const cliente = criarClienteDadosPessoaisResiliente(undefined);
      await expect(cliente.salvar(estudanteExemplo)).resolves.toBeUndefined();
    });
  });

  describe("criarClienteFormacaoAcademicaResiliente", () => {
    it("deve delegar o cadastro ao cliente http quando houver sucesso", async () => {
      const cadastrarMock = vi.fn().mockResolvedValue(undefined);
      const clienteHttp: ClienteFormacaoAcademica = {
        cadastrar: cadastrarMock,
      };
      const cliente = criarClienteFormacaoAcademicaResiliente(clienteHttp);

      await expect(cliente.cadastrar(formacaoExemplo)).resolves.toBeUndefined();
      expect(cadastrarMock).toHaveBeenCalledWith(formacaoExemplo);
    });

    it("deve absorver falha de rede do backend e avançar normalmente", async () => {
      const cadastrarMock = vi
        .fn()
        .mockRejectedValue(new FalhaFormacaoAcademica("rede"));
      const clienteHttp: ClienteFormacaoAcademica = {
        cadastrar: cadastrarMock,
      };
      const cliente = criarClienteFormacaoAcademicaResiliente(clienteHttp);

      await expect(cliente.cadastrar(formacaoExemplo)).resolves.toBeUndefined();
    });

    it("deve absorver falha de indisponibilidade (HTTP 500+)", async () => {
      const cadastrarMock = vi
        .fn()
        .mockRejectedValue(new FalhaFormacaoAcademica("indisponivel"));
      const clienteHttp: ClienteFormacaoAcademica = {
        cadastrar: cadastrarMock,
      };
      const cliente = criarClienteFormacaoAcademicaResiliente(clienteHttp);

      await expect(cliente.cadastrar(formacaoExemplo)).resolves.toBeUndefined();
    });

    it("deve repassar falhas de validação de dados para o formulário exibir erros", async () => {
      const cadastrarMock = vi
        .fn()
        .mockRejectedValue(new FalhaFormacaoAcademica("resposta-invalida"));
      const clienteHttp: ClienteFormacaoAcademica = {
        cadastrar: cadastrarMock,
      };
      const cliente = criarClienteFormacaoAcademicaResiliente(clienteHttp);

      await expect(cliente.cadastrar(formacaoExemplo)).rejects.toThrow(
        "resposta-invalida",
      );
    });

    it("deve lidar com cliente http indefinido sem disparar erros", async () => {
      const cliente = criarClienteFormacaoAcademicaResiliente(undefined);
      await expect(cliente.cadastrar(formacaoExemplo)).resolves.toBeUndefined();
    });
  });

  describe("criarClienteAcessoResiliente", () => {
    it("deve cadastrar via cliente http se disponível", async () => {
      const cadastrarHttp = vi.fn().mockResolvedValue({
        id: "1",
        nome: "Ana",
        email: "ana@exemplo.com",
      });
      const clienteHttp = {
        cadastrar: cadastrarHttp,
        acessar: vi.fn(),
      } as unknown as ClienteAcessoEstudante;

      const clienteFallback = {
        cadastrar: vi.fn(),
        acessar: vi.fn(),
      } as unknown as ClienteAcessoEstudante;

      const cliente = criarClienteAcessoResiliente(
        clienteHttp,
        clienteFallback,
      );
      const res = await cliente.cadastrar({
        nome: "Ana",
        email: "ana@exemplo.com",
        senha: "123",
      });

      expect(res.id).toBe("1");
      expect(cadastrarHttp).toHaveBeenCalled();
      expect(clienteFallback.cadastrar).not.toHaveBeenCalled();
    });

    it("deve alternar para fallback em memória se o cadastro http falhar por rede", async () => {
      const clienteHttp = {
        cadastrar: vi.fn().mockRejectedValue(new FalhaAcessoEstudante("rede")),
        acessar: vi.fn(),
      } as unknown as ClienteAcessoEstudante;

      const fallbackMock = vi.fn().mockResolvedValue({
        id: "demo-1",
        nome: "Ana",
        email: "ana@exemplo.com",
      });
      const clienteFallback = {
        cadastrar: fallbackMock,
        acessar: vi.fn(),
      } as unknown as ClienteAcessoEstudante;

      const cliente = criarClienteAcessoResiliente(
        clienteHttp,
        clienteFallback,
      );
      const res = await cliente.cadastrar({
        nome: "Ana",
        email: "ana@exemplo.com",
        senha: "123",
      });

      expect(res.id).toBe("demo-1");
      expect(fallbackMock).toHaveBeenCalled();
    });

    it("deve alternar para fallback em memória se o login http falhar por rede", async () => {
      const clienteHttp = {
        cadastrar: vi.fn(),
        acessar: vi.fn().mockRejectedValue(new FalhaAcessoEstudante("rede")),
      } as unknown as ClienteAcessoEstudante;

      const acessarFallback = vi.fn().mockResolvedValue(undefined);
      const clienteFallback = {
        cadastrar: vi.fn(),
        acessar: acessarFallback,
      } as unknown as ClienteAcessoEstudante;

      const cliente = criarClienteAcessoResiliente(
        clienteHttp,
        clienteFallback,
      );
      await expect(
        cliente.acessar({ email: "ana@exemplo.com", senha: "123" }),
      ).resolves.toBeUndefined();
      expect(acessarFallback).toHaveBeenCalled();
    });

    it("deve repassar falha de credenciais inválidas sem mascarar", async () => {
      const clienteHttp = {
        cadastrar: vi.fn(),
        acessar: vi
          .fn()
          .mockRejectedValue(new FalhaAcessoEstudante("credenciais-invalidas")),
      } as unknown as ClienteAcessoEstudante;

      const clienteFallback = {
        cadastrar: vi.fn(),
        acessar: vi.fn(),
      } as unknown as ClienteAcessoEstudante;

      const cliente = criarClienteAcessoResiliente(
        clienteHttp,
        clienteFallback,
      );
      await expect(
        cliente.acessar({ email: "ana@exemplo.com", senha: "errada" }),
      ).rejects.toThrow("credenciais-invalidas");
    });
  });

  describe("criarClienteVagasResiliente", () => {
    it("deve delegar a busca ao cliente http quando online", async () => {
      const listarHttp = vi.fn().mockResolvedValue([
        {
          curriculoId: "c1",
          ranque: 1,
          vaga: { id: "v1", titulo: "Dev", empresa: "Tech", descricao: "Desc" },
        },
      ]);
      const clienteHttp = {
        listarSugestoes: listarHttp,
      } as unknown as ClienteVagasGrupo2;
      const clienteFallback = {
        listarSugestoes: vi.fn(),
      } as unknown as ClienteVagasGrupo2;

      const cliente = criarClienteVagasResiliente(clienteHttp, clienteFallback);
      const resultado = await cliente.listarSugestoes({ termo: "Dev" });

      expect(resultado).toHaveLength(1);
      expect(listarHttp).toHaveBeenCalled();
      expect(clienteFallback.listarSugestoes).not.toHaveBeenCalled();
    });

    it("deve usar o cliente de demonstração quando o serviço de vagas falhar com indisponivel", async () => {
      const clienteHttp = {
        listarSugestoes: vi
          .fn()
          .mockRejectedValue(new FalhaVagasGrupo2("indisponivel")),
      } as unknown as ClienteVagasGrupo2;

      const fallbackMock = vi.fn().mockResolvedValue([
        {
          curriculoId: "c1",
          ranque: 1,
          vaga: {
            id: "v-demo",
            titulo: "Vaga Demo",
            empresa: "Empresa",
            descricao: "...",
          },
        },
      ]);
      const clienteFallback = {
        listarSugestoes: fallbackMock,
      } as unknown as ClienteVagasGrupo2;

      const cliente = criarClienteVagasResiliente(clienteHttp, clienteFallback);
      const resultado = await cliente.listarSugestoes({ termo: "" });

      expect(resultado).toHaveLength(1);
      expect(resultado[0].vaga.id).toBe("v-demo");
      expect(fallbackMock).toHaveBeenCalled();
    });
  });
});
