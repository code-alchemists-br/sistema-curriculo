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
  type AcessoEstudanteEntrada,
  type CadastroEstudanteEntrada,
  type ClienteAcessoEstudante,
  type EstudanteCadastrado,
} from "../features/acesso-estudante";
import {
  FalhaVagasGrupo2,
  type ClienteVagasGrupo2,
  type CriteriosPesquisaVagas,
} from "../features/listar-vagas";
import type { SugestaoVaga } from "../entities/vaga";

/**
 * Verifica se um erro representa uma falha de conexão física ou indisponibilidade de rede.
 */
function ehErroDeConexao(erro: unknown): boolean {
  if (erro instanceof TypeError) {
    return true;
  }
  if (
    erro instanceof Error &&
    /failed to fetch|network|conex[aã]o|refused|offline/i.test(erro.message)
  ) {
    return true;
  }
  return false;
}

/**
 * Adapta o cliente de dados pessoais para não bloquear a navegação em caso de
 * indisponibilidade de rede ou backend fora do ar, preservando os dados localmente.
 *
 * @param clienteHttp Cliente HTTP conectado ao backend.
 * @returns Cliente de dados pessoais com fallback silencioso para falhas de rede.
 */
export function criarClienteDadosPessoaisResiliente(
  clienteHttp?: ClienteDadosPessoais,
): ClienteDadosPessoais {
  return {
    async salvar(dados: Student): Promise<void> {
      if (!clienteHttp) {
        return;
      }
      try {
        await clienteHttp.salvar(dados);
      } catch (erro: unknown) {
        if (
          (erro instanceof FalhaDadosPessoais &&
            (erro.codigo === "indisponivel" ||
              (erro.codigo as string) === "rede")) ||
          ehErroDeConexao(erro)
        ) {
          console.warn(
            "[Resiliência Offline] Backend indisponível ao salvar dados pessoais. Prosseguindo com dados no rascunho local.",
          );
          return;
        }
        throw erro;
      }
    },
  };
}

/**
 * Adapta o cliente de formação acadêmica para não bloquear o fluxo de cadastro
 * quando a API remota estiver desligada, mantendo as informações preenchidas no rascunho.
 *
 * @param clienteHttp Cliente HTTP conectado ao backend.
 * @returns Cliente de formação acadêmica com fallback silencioso para falhas de rede.
 */
export function criarClienteFormacaoAcademicaResiliente(
  clienteHttp?: ClienteFormacaoAcademica,
): ClienteFormacaoAcademica {
  return {
    async cadastrar(entrada: CadastroFormacaoAcademicaEntrada): Promise<void> {
      if (!clienteHttp) {
        return;
      }
      try {
        await clienteHttp.cadastrar(entrada);
      } catch (erro: unknown) {
        if (
          (erro instanceof FalhaFormacaoAcademica &&
            (erro.codigo === "rede" || erro.codigo === "indisponivel")) ||
          ehErroDeConexao(erro)
        ) {
          console.warn(
            "[Resiliência Offline] Backend indisponível ao salvar formação acadêmica. Prosseguindo com dados no rascunho local.",
          );
          return;
        }
        throw erro;
      }
    },
  };
}

/**
 * Adapta o cliente de autenticação para chavear de forma transparente para demonstração
 * em memória quando o servidor não responder por falha de conexão ou indisponibilidade.
 *
 * @param clienteHttp Cliente HTTP de autenticação.
 * @param clienteFallback Cliente em memória / demonstração para contingência.
 * @returns Cliente de autenticação resiliente a quedas de rede.
 */
export function criarClienteAcessoResiliente(
  clienteHttp: ClienteAcessoEstudante,
  clienteFallback: ClienteAcessoEstudante,
): ClienteAcessoEstudante {
  return {
    async cadastrar(
      entrada: CadastroEstudanteEntrada,
    ): Promise<EstudanteCadastrado> {
      try {
        return await clienteHttp.cadastrar(entrada);
      } catch (erro: unknown) {
        if (
          (erro instanceof FalhaAcessoEstudante &&
            (erro.codigo === "rede" || erro.codigo === "indisponivel")) ||
          ehErroDeConexao(erro)
        ) {
          console.warn(
            "[Resiliência Offline] Backend indisponível para cadastro de estudante. Utilizando modo demonstração.",
          );
          return await clienteFallback.cadastrar(entrada);
        }
        throw erro;
      }
    },
    async acessar(entrada: AcessoEstudanteEntrada): Promise<void> {
      try {
        return await clienteHttp.acessar(entrada);
      } catch (erro: unknown) {
        if (
          (erro instanceof FalhaAcessoEstudante &&
            (erro.codigo === "rede" || erro.codigo === "indisponivel")) ||
          ehErroDeConexao(erro)
        ) {
          console.warn(
            "[Resiliência Offline] Backend indisponível para login de estudante. Utilizando modo demonstração.",
          );
          return await clienteFallback.acessar(entrada);
        }
        throw erro;
      }
    },
  };
}

/**
 * Adapta o cliente de vagas para retornar dados de demonstração caso o endpoint
 * esteja inacessível ou atinja timeout no backend.
 *
 * @param clienteHttp Cliente HTTP de busca de vagas.
 * @param clienteFallback Cliente de demonstração para contingência.
 * @returns Cliente de vagas resiliente a falhas no servidor.
 */
export function criarClienteVagasResiliente(
  clienteHttp: ClienteVagasGrupo2,
  clienteFallback: ClienteVagasGrupo2,
): ClienteVagasGrupo2 {
  return {
    async listarSugestoes(
      criterios: CriteriosPesquisaVagas,
    ): Promise<SugestaoVaga[]> {
      try {
        return await clienteHttp.listarSugestoes(criterios);
      } catch (erro: unknown) {
        if (
          (erro instanceof FalhaVagasGrupo2 &&
            (erro.codigo === "indisponivel" ||
              erro.codigo === "tempo-limite")) ||
          ehErroDeConexao(erro)
        ) {
          console.warn(
            "[Resiliência Offline] Backend de vagas indisponível. Utilizando vagas de demonstração.",
          );
          return await clienteFallback.listarSugestoes(criterios);
        }
        throw erro;
      }
    },
  };
}
