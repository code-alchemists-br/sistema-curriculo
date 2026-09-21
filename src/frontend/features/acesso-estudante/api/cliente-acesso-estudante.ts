// Proveniência: decision-analysis prompts/frontend/20260920-232013-tela-cadastro-acesso-estudante-v001.md#v001

/** Representa os dados externos exigidos para criar uma conta de estudante. */
export interface CadastroEstudanteEntrada {
  nome: string;
  email: string;
  senha: string;
}

/** Representa os dados externos exigidos para confirmar credenciais. */
export interface AcessoEstudanteEntrada {
  email: string;
  senha: string;
}

/** Representa a resposta pública normalizada após o cadastro bem-sucedido. */
export interface EstudanteCadastrado {
  id: string;
  nome: string;
  email: string;
}

/** Enumera falhas de transporte traduzíveis para a experiência da tela. */
export type CodigoFalhaAcessoEstudante =
  | "credenciais-invalidas"
  | "email-ja-cadastrado"
  | "dados-invalidos"
  | "indisponivel"
  | "rede"
  | "resposta-invalida";

/**
 * Carrega uma falha conhecida da fronteira HTTP.
 *
 * A classe conserva um código estável separado de mensagens do servidor e do
 * componente visual. Ela existe para permitir que a feature apresente feedback
 * claro sem acoplar a interface a detalhes de status HTTP.
 */
export class FalhaAcessoEstudante extends Error {
  constructor(public readonly codigo: CodigoFalhaAcessoEstudante) {
    super(codigo);
    this.name = "FalhaAcessoEstudante";
  }
}

/**
 * Define as operações remotas consumidas pelos formulários da feature.
 *
 * O contrato oculta fetch e os DTOs HTTP atrás de intenções de cadastro e
 * acesso. Ele existe para desacoplar a UI, possibilitando doubles unitários e
 * futura substituição quando a composição do backend estiver disponível.
 */
export interface ClienteAcessoEstudante {
  cadastrar(entrada: CadastroEstudanteEntrada): Promise<EstudanteCadastrado>;
  acessar(entrada: AcessoEstudanteEntrada): Promise<void>;
}

/**
 * Cria o cliente HTTP dos contratos atuais de cadastro e confirmação de acesso.
 *
 * A fábrica monta URLs a partir de VITE_API_URL, envia somente os DTOs aceitos
 * pelo backend e converte status e JSON em tipos locais. Ela existe para isolar
 * o transporte dos componentes visuais e tornar a ausência atual do backend
 * substituível por doubles nos testes unitários.
 */
export function criarClienteAcessoEstudante(
  urlDaApi = import.meta.env.VITE_API_URL
): ClienteAcessoEstudante {
  return {
    async cadastrar(entrada) {
      const baseUrl = normalizarUrlDaApi(urlDaApi);
      const resposta = await enviarRequisicao(`${baseUrl}/estudantes`, entrada);

      if (resposta.status === 201) return lerEstudanteCadastrado(resposta);

      throw new FalhaAcessoEstudante(classificarFalhaCadastro(resposta.status));
    },
    async acessar(entrada) {
      const baseUrl = normalizarUrlDaApi(urlDaApi);
      const resposta = await enviarRequisicao(`${baseUrl}/acessos`, entrada);

      if (resposta.status === 204) return;

      throw new FalhaAcessoEstudante(classificarFalhaAcesso(resposta.status));
    }
  };
}

/**
 * Normaliza a origem configurada e torna sua ausência uma indisponibilidade.
 *
 * A função remove apenas a barra final para compor endpoints previsíveis e não
 * tenta escolher uma origem de produção. Ela existe para preservar a decisão
 * de CORS e URL por ambiente fora da tela.
 */
function normalizarUrlDaApi(urlDaApi: string | undefined): string {
  if (urlDaApi === undefined || urlDaApi.trim() === "") {
    throw new FalhaAcessoEstudante("indisponivel");
  }

  return urlDaApi.replace(/\/$/, "");
}

/**
 * Envia um DTO JSON e converte indisponibilidade de rede em uma falha estável.
 *
 * A função centraliza método, cabeçalhos e serialização sem interpretar regras
 * do formulário. Ela existe para evitar chamadas HTTP em componentes visuais.
 */
async function enviarRequisicao(
  url: string,
  corpo: CadastroEstudanteEntrada | AcessoEstudanteEntrada
): Promise<Response> {
  try {
    return await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(corpo)
    });
  } catch {
    throw new FalhaAcessoEstudante("rede");
  }
}

/**
 * Lê e valida a resposta de cadastro antes de expor um modelo à interface.
 *
 * A função confere os três campos públicos esperados, recusando JSON ausente ou
 * incompatível. Ela existe para impedir que um DTO externo vire modelo de UI
 * sem validação na fronteira.
 */
async function lerEstudanteCadastrado(resposta: Response): Promise<EstudanteCadastrado> {
  try {
    const dados: unknown = await resposta.json();

    if (
      typeof dados === "object" &&
      dados !== null &&
      "id" in dados &&
      "nome" in dados &&
      "email" in dados &&
      typeof dados.id === "string" &&
      typeof dados.nome === "string" &&
      typeof dados.email === "string"
    ) {
      return { id: dados.id, nome: dados.nome, email: dados.email };
    }
  } catch {
    // A tradução abaixo mantém a falha de JSON no contrato local da feature.
  }

  throw new FalhaAcessoEstudante("resposta-invalida");
}

/**
 * Traduz status de cadastro para categorias compreensíveis pela feature.
 *
 * A função preserva os códigos explicitamente contratados e agrupa outros
 * status como indisponibilidade. Ela existe para impedir condicionais HTTP na
 * camada visual.
 */
function classificarFalhaCadastro(status: number): CodigoFalhaAcessoEstudante {
  if (status === 409) return "email-ja-cadastrado";
  if (status === 422) return "dados-invalidos";
  return "indisponivel";
}

/**
 * Traduz status de confirmação de credenciais para categorias da feature.
 *
 * A função reconhece credenciais não confirmadas sem expor qual campo falhou e
 * agrupa indisponibilidade do serviço. Ela existe para manter a comunicação de
 * acesso fiel ao contrato atual sem declarar uma sessão inexistente.
 */
function classificarFalhaAcesso(status: number): CodigoFalhaAcessoEstudante {
  if (status === 401) return "credenciais-invalidas";
  return "indisponivel";
}
