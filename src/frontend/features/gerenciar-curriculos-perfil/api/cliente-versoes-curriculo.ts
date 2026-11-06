import type {
  AtualizacaoVersaoCurriculo,
  ResumoVersaoCurriculo,
} from "../model/versao-curriculo-perfil";

/** Enumera falhas que podem ser explicadas no painel de versões. */
export type CodigoFalhaVersaoCurriculo =
  | "indisponivel"
  | "nao-encontrado"
  | "resposta-invalida";

/**
 * Representa uma falha conhecida ao consultar ou alterar uma versão de currículo.
 *
 * A classe conserva somente um código estável. Ela existe para que a interface
 * trate indisponibilidade e ausência de versão sem depender de detalhes de rede.
 */
export class FalhaVersaoCurriculo extends Error {
  constructor(public readonly codigo: CodigoFalhaVersaoCurriculo) {
    super(codigo);
    this.name = "FalhaVersaoCurriculo";
  }
}

/**
 * Define as operações usadas pelo painel de currículos já criados.
 *
 * O contrato espelha a listagem de versões existente: título, layout, visibilidade
 * e quantidade de itens. Ele não representa edição de itens do currículo, que
 * permanece no fluxo próprio de composição das seções.
 */
export interface ClienteVersoesCurriculo {
  listar(): Promise<ResumoVersaoCurriculo[]>;
  atualizar(
    id: string,
    dados: AtualizacaoVersaoCurriculo,
  ): Promise<ResumoVersaoCurriculo>;
}

/**
 * Cria um cliente em memória para a demonstração da interface atual.
 *
 * A implementação guarda somente os metadados já previstos pela API de versões.
 * Ela existe para manter a tela navegável enquanto a autenticação ainda não
 * fornece o identificador necessário para conectar o cliente HTTP real.
 */
export function criarClienteVersoesCurriculoDemonstracao(): ClienteVersoesCurriculo {
  let versoes: ResumoVersaoCurriculo[] = [
    {
      id: "versao-estagio-2026",
      tituloVersao: "Currículo para estágio",
      modelo: "primeiro-emprego",
      visibilidade: "privado",
      totalItens: 8,
    },
    {
      id: "versao-desenvolvedor-2026",
      tituloVersao: "Desenvolvedor(a) Frontend",
      modelo: "moderno",
      visibilidade: "publico",
      totalItens: 14,
    },
  ];

  return {
    async listar() {
      return versoes.map((versao) => ({ ...versao }));
    },
    async atualizar(id, dados) {
      const indice = versoes.findIndex((versao) => versao.id === id);

      if (indice === -1) {
        throw new FalhaVersaoCurriculo("nao-encontrado");
      }

      const versaoAtualizada: ResumoVersaoCurriculo = {
        ...versoes[indice],
        ...dados,
      };
      versoes = versoes.map((versao) =>
        versao.id === id ? versaoAtualizada : versao,
      );

      return { ...versaoAtualizada };
    },
  };
}
