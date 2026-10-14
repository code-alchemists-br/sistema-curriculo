"""Expoe DTOs e handlers HTTP para cadastro e verificacao de acesso de estudante.

O modulo converte JSON em tipos da Application, deriva senha na borda e traduz
falhas conhecidas em respostas HTTP sem expor entidades ou hashes. Ele existe
para manter transporte e segurança fora das regras de domínio e casos de uso.
"""

from datetime import datetime
from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel, Field

from backend.application import (
    AcessarEstudanteEntrada,
    CadastrarEstudanteEntrada,
    CredenciaisInvalidas,
    EmailJaCadastrado,
)
from backend.domain import Email, HashSenha, Nome, RegraDeDominioViolada, Usuario


class DerivadorSenha(Protocol):
    """Define a derivação de senha que a interface precisa antes do cadastro.

    O contrato recebe a credencial temporariamente e devolve seu value object
    derivado, sem revelar algoritmo ou adapter à rota. Ele existe para que a
    composição injete segurança concreta e a API permaneça testável.
    """

    def derivar(self, senha: str) -> HashSenha:
        """Deriva uma senha em texto claro para o value object persistível.

        Implementações aplicam salt e algoritmo de segurança fora do handler e
        retornam somente o valor derivado. O método existe para impedir que a
        rota conheça ou implemente detalhes criptográficos.
        """


class CadastroEstudanteExecutor(Protocol):
    """Define a capacidade de cadastrar estudante que o router precisa invocar.

    O contrato recebe a entrada da Application e devolve seu agregado, sem
    acoplar o handler a banco ou implementação concreta. Ele existe para tornar
    a interface HTTP testável com doubles que exercitam a mesma intenção.
    """

    async def executar(self, entrada: CadastrarEstudanteEntrada) -> Usuario:
        """Executa o cadastro interno e devolve o agregado persistido.

        Implementações aplicam regras de negócio sem definir respostas HTTP. O
        método existe para que o router se concentre em traduzir fronteiras.
        """


class AcessoEstudanteExecutor(Protocol):
    """Define a capacidade de confirmar acesso que o router precisa invocar.

    O contrato mantém consulta e comparação de senha fora do controller e
    devolve o agregado autenticado após sucesso. Ele existe para que a borda
    emita sessão sem acessar repositório nem repetir validação de senha.
    """

    async def executar(self, entrada: AcessarEstudanteEntrada) -> Usuario:
        """Confirma a entrada de acesso ou sinaliza credenciais não confirmadas.

        Implementações não expõem qual credencial falhou. O método existe para
        que a interface devolva uma resposta uniforme e segura ao cliente.
        """


class GerenciadorSessoes(Protocol):
    """Define o ciclo de sessão que a interface precisa delegar.

    O contrato mantém tokens e persistência atrás de uma abstração injetada e
    existe para autenticar requisições sem aceitar identidade do cliente.
    """

    async def criar(self, usuario_id: UUID) -> tuple[str, datetime]:
        """Emite token opaco e informa sua expiração absoluta."""

    async def usuario_da_sessao(self, token: str | None) -> UUID | None:
        """Resolve o principal para token ativo ou retorna ausência."""

    async def revogar(self, token: str | None) -> None:
        """Revoga a sessão correspondente ao token, quando existente."""


async def obter_principal(request: Request) -> UUID:
    """Exige cookie válido e devolve a identidade obtida no armazenamento.

    A função consulta o gerenciador instalado na composição da aplicação e
    nunca aceita identidade de path ou JSON. Ela existe para ser injetada como
    dependência em rotas que exigem autenticação server-side.
    """
    sessoes: GerenciadorSessoes | None = getattr(request.app.state, "sessoes", None)
    if sessoes is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Autenticação necessária.")
    usuario_id = await sessoes.usuario_da_sessao(request.cookies.get("sistema_curriculo_sessao"))
    if usuario_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Autenticação necessária.")
    return usuario_id


class CadastroEstudanteRequisicao(BaseModel):
    """Representa o JSON aceito para criar uma conta de estudante.

    O DTO limita presença e tamanho na fronteira antes da conversão a VOs e não
    é usado como modelo do domínio. Ele existe para separar transporte do núcleo.
    """

    nome: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=3, max_length=320)
    senha: str = Field(min_length=8, max_length=1024)


class AcessoEstudanteRequisicao(BaseModel):
    """Representa o JSON aceito para confirmar credenciais de acesso.

    O DTO limita dados recebidos e mantém senha fora de respostas e persistência.
    Ele existe para proteger a fronteira contra entradas incompletas ou excessivas.
    """

    email: str = Field(min_length=3, max_length=320)
    senha: str = Field(min_length=8, max_length=1024)


class EstudanteResposta(BaseModel):
    """Representa somente os dados públicos devolvidos após cadastro bem-sucedido.

    O DTO extrai identidade, nome e e-mail sem serializar hash de senha ou a
    entidade de domínio. Ele existe para proteger credenciais na saída HTTP.
    """

    id: UUID
    nome: str
    email: str


def criar_router(
    cadastrar_estudante: CadastroEstudanteExecutor | None,
    acessar_estudante: AcessoEstudanteExecutor | None,
    derivador_senha: DerivadorSenha | None = None,
    sessoes: GerenciadorSessoes | None = None,
) -> APIRouter:
    """Cria rotas HTTP usando casos de uso injetados pela composição externa.

    A função deriva senhas apenas no cadastro e converte exceções conhecidas em
    status seguros. Ela existe para registrar a API e permitir testes unitários
    com doubles sem criar sessão de banco ou servidor real.
    """
    router = APIRouter()

    @router.post("/estudantes", response_model=EstudanteResposta, status_code=status.HTTP_201_CREATED)
    async def cadastrar(requisicao: CadastroEstudanteRequisicao) -> EstudanteResposta:
        """Executa cadastro HTTP e devolve dados públicos do estudante criado.

        O handler cria VOs, deriva senha e aguarda o caso de uso, traduzindo
        duplicidade e formato inválido sem expor segredos. Ele existe para expor
        UC01 sem levar HTTP ou scrypt à Application.
        """
        if cadastrar_estudante is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Cadastro indisponível.")
        if derivador_senha is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Cadastro indisponível.")
        try:
            usuario = await cadastrar_estudante.executar(CadastrarEstudanteEntrada(nome=Nome(requisicao.nome), email=Email(requisicao.email), hash_senha=derivador_senha.derivar(requisicao.senha)))
        except RegraDeDominioViolada as erro:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(erro)) from erro
        except EmailJaCadastrado as erro:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(erro)) from erro
        return EstudanteResposta(id=usuario.id.valor, nome=usuario.nome.valor, email=usuario.email.valor)

    @router.post("/acessos", status_code=status.HTTP_204_NO_CONTENT)
    async def acessar(requisicao: AcessoEstudanteRequisicao) -> Response:
        """Confirma credenciais e emite cookie de sessão somente no sucesso.

        O handler converte somente e-mail e senha em entrada, aguarda o caso de
        uso e cria uma sessão opaca. Ele existe para fornecer identidade local
        sem expor token no JSON.
        """
        if acessar_estudante is None or sessoes is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Acesso indisponível.")
        try:
            usuario = await acessar_estudante.executar(AcessarEstudanteEntrada(email=Email(requisicao.email), senha=requisicao.senha))
        except (RegraDeDominioViolada, CredenciaisInvalidas) as erro:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-mail ou senha não conferem.") from erro
        token, expira = await sessoes.criar(usuario.id.valor)
        response = Response(status_code=status.HTTP_204_NO_CONTENT)
        response.set_cookie("sistema_curriculo_sessao", token, expires=expira, httponly=True, secure=True, samesite="lax", path="/")
        return response

    @router.post("/sessoes/logout", status_code=status.HTTP_204_NO_CONTENT)
    async def logout(request: Request, response: Response) -> None:
        """Revoga a credencial corrente e remove o cookie do cliente.

        O token é obtido do cookie e nunca é devolvido no corpo. A rota existe
        para encerrar imediatamente a sessão server-side.
        """
        if sessoes is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Sessões indisponíveis.")
        await sessoes.revogar(request.cookies.get("sistema_curriculo_sessao"))
        response.delete_cookie("sistema_curriculo_sessao", path="/", secure=True, httponly=True, samesite="lax")

    return router
