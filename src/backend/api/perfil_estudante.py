"""Expõe DTOs e handlers HTTP para edição e exclusão do perfil do estudante.

O módulo converte JSON e identidade de rota em tipos da Application e traduz
falhas conhecidas em respostas HTTP sem expor entidades, hash de senha ou
detalhes de persistência. Ele existe para manter transporte e segurança fora
das regras de domínio e dos casos de uso de perfil.
"""

from typing import Protocol
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field, field_validator

from backend.application import (
    AtualizarPerfilCompletoEntrada,
    ConsultarPerfilEstudanteEntrada,
    EditarPerfilEntrada,
    EmailJaCadastrado,
    ExcluirPerfilEntrada,
    PerfilExcluido,
    PerfilNaoEncontrado,
)
from backend.domain import (
    DadosContato,
    Email,
    Endereco,
    Nome,
    RegraDeDominioViolada,
    Telefone,
    Usuario,
    UsuarioId,
)


class AtualizacaoPerfilCompletoExecutor(Protocol):
    """Define a capacidade de atualização integral consumida pela rota nova.

    O contrato recebe valores tipados e devolve o agregado atualizado, sem
    acoplar transporte a persistência concreta. Ele existe para injetar o caso
    de uso completo e permitir testes isolados da interface HTTP.
    """

    async def executar(self, entrada: AtualizarPerfilCompletoEntrada) -> Usuario:
        """Atualiza todos os campos editáveis e devolve o agregado resultante.

        A implementação aplica regras de perfil e persiste pela porta interna.
        O método existe para manter o handler responsável apenas pela fronteira.
        """


class EdicaoPerfilExecutor(Protocol):
    """Define a capacidade de editar perfil que o router precisa invocar.

    O contrato recebe a entrada da Application e devolve o agregado com o novo
    estado, sem acoplar o handler a banco ou implementação concreta. Ele existe
    para tornar a interface HTTP testável com doubles que exercitam a mesma
    intenção do caso de uso real.
    """

    async def executar(self, entrada: EditarPerfilEntrada) -> Usuario:
        """Executa a edição interna e devolve o agregado atualizado.

        Implementações aplicam regras de perfil sem definir respostas HTTP. O
        método existe para que o router se concentre em traduzir fronteiras.
        """


class ExclusaoPerfilExecutor(Protocol):
    """Define a capacidade de excluir perfil que o router precisa invocar.

    O contrato recebe a entrada da Application e devolve o agregado já marcado
    como excluído, sem acoplar o handler a relógio ou repositório concreto. Ele
    existe para tornar a interface HTTP testável com doubles.
    """

    async def executar(self, entrada: ExcluirPerfilEntrada) -> Usuario:
        """Executa a exclusão lógica interna e devolve o estado resultante.

        Implementações aplicam a transição idempotente sem definir resposta
        HTTP. O método existe para que o router traduza apenas a fronteira.
        """


class ConsultaPerfilExecutor(Protocol):
    """Define a capacidade de consulta de perfil consumida pelo router.

    O contrato aceita identidade tipada e devolve o agregado encontrado. Ele
    existe para manter a consulta HTTP desacoplada de persistência concreta.
    """

    async def executar(self, entrada: ConsultarPerfilEstudanteEntrada) -> Usuario:
        """Busca o perfil ativo associado à identidade autenticada.

        A implementação delega ao caso de uso injetado sem I/O no handler. O
        método existe para tornar a consulta substituível por doubles em testes.
        """


async def obter_principal(request: Request) -> UUID:
    """Devolve a identidade de usuário instalada pelo middleware de sessão.

    A função valida o tipo do UUID na fronteira e responde 401 quando não há
    principal autenticado. Ela existe para impedir confiança em IDs do cliente.
    """
    usuario_id = getattr(request.state, "usuario_id", None)
    if not isinstance(usuario_id, UUID):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão ausente ou inválida.")
    return usuario_id


class EditarPerfilRequisicao(BaseModel):
    """Representa o JSON aceito para editar nome e e-mail de um perfil.

    O DTO limita presença e tamanho na fronteira antes da conversão a VOs e não
    aceita senha, hash ou identidade — que permanecem fora deste contrato. Ele
    existe para separar transporte do núcleo de edição de perfil.
    """

    nome: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=3, max_length=320)


class AtualizarPerfilCompletoRequisicao(BaseModel):
    """Representa os campos editáveis enviados na atualização integral.

    O DTO exige nome, e-mail, endereço e telefones e aceita links opcionais;
    ausência de LinkedIn ou Lattes os limpa no PUT. Ele existe para definir
    substituição completa sem aceitar identidade, senha ou estado interno.
    """

    nome: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=3, max_length=320)
    endereco: str = Field(min_length=1, max_length=500)
    cidade: str = Field(min_length=1, max_length=120)
    telefones: list[str] = Field(min_length=1, max_length=5)
    linkedin: str | None = Field(default=None, max_length=300)
    curriculo_lattes: str | None = Field(default=None, max_length=300)

    @field_validator("cidade")
    @classmethod
    def validar_cidade(cls, valor: str) -> str:
        """Normaliza a cidade e rejeita texto composto somente por espaços.

        A validação remove espaços periféricos antes da conversão ao domínio.
        Ela existe para que o campo obrigatório não seja persistido como vazio.
        """
        cidade = valor.strip()
        if not cidade:
            raise ValueError("Cidade não pode ser vazia.")
        return cidade


class PerfilResposta(BaseModel):
    """Representa somente os dados públicos devolvidos após editar um perfil.

    O DTO extrai identidade, nome e e-mail sem serializar hash de senha, data
    de exclusão ou a entidade de domínio. Ele existe para proteger credenciais
    e detalhes internos na saída HTTP.
    """

    id: UUID
    nome: str
    email: str


class PerfilCompletoResposta(BaseModel):
    """Representa os campos editáveis devolvidos após salvar o perfil completo.

    O DTO inclui identidade, nome, e-mail e contato, mas exclui hash de senha e
    estado interno. Ele existe para confirmar valores salvos sem serializar o
    agregado de domínio diretamente.
    """

    id: UUID
    nome: str
    email: str
    endereco: str
    cidade: str | None
    telefones: list[str]
    linkedin: str | None
    curriculo_lattes: str | None


class DadosPessoaisResposta(BaseModel):
    """Projeta somente os dados pessoais permitidos na resposta de consulta.

    O DTO omite ID, hash e estado de persistência, extraindo os contatos do
    agregado. Ele existe para controlar explicitamente o payload público.
    """

    nome: str
    email: str
    telefones: list[str]
    cidade: str | None
    linkedin: str | None
    curriculo_lattes: str | None

    @classmethod
    def de_usuario(cls, usuario: Usuario) -> "DadosPessoaisResposta":
        """Converte o agregado para os campos aprovados de consulta pessoal.

        Contato ausente vira lista vazia e opcionais nulos, sem serializar a
        entidade completa. O método existe para evitar vazamento de credenciais.
        """
        contato = usuario.dados_contato
        return cls(
            nome=usuario.nome.valor,
            email=usuario.email.valor,
            telefones=[telefone.valor for telefone in contato.telefones] if contato else [],
            cidade=contato.cidade.valor if contato and contato.cidade else None,
            linkedin=contato.linkedin if contato else None,
            curriculo_lattes=contato.curriculo_lattes if contato else None,
        )


def criar_router(
    editar_perfil: EdicaoPerfilExecutor | None,
    excluir_perfil: ExclusaoPerfilExecutor | None,
    atualizar_perfil_completo: AtualizacaoPerfilCompletoExecutor | None = None,
    consultar_perfil: ConsultaPerfilExecutor | None = None,
) -> APIRouter:
    """Cria rotas HTTP de perfil usando casos de uso injetados pela composição.

    A função converte identidade de rota e JSON em entradas da Application e
    traduz exceções conhecidas em status seguros. Ela existe para registrar a
    API e permitir testes unitários com doubles, sem sessão de banco real.

    A rota conserva ``usuario_id`` no caminho por compatibilidade, mas exige
    que ele corresponda à identidade autenticada instalada pelo middleware.
    Essa checagem local também impede escrita anônima se a aplicação for
    composta sem middleware.
    """
    router = APIRouter()

    @router.get("/estudantes/{usuario_id}", response_model=DadosPessoaisResposta)
    async def consultar(
        usuario_id: UUID,
        principal_id: UUID = Depends(obter_principal),
    ) -> DadosPessoaisResposta:
        """Devolve dados pessoais somente ao proprietário autenticado.

        O handler mascara IDs alheios como 404, consulta o caso de uso e projeta
        o DTO permitido. Ele existe para proteger leitura contra enumeração.
        """
        if principal_id != usuario_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil não encontrado.")
        if consultar_perfil is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Consulta indisponível.")
        try:
            usuario = await consultar_perfil.executar(
                ConsultarPerfilEstudanteEntrada(usuario_id=UsuarioId(principal_id))
            )
        except PerfilNaoEncontrado as erro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil não encontrado.") from erro
        return DadosPessoaisResposta.de_usuario(usuario)

    @router.put("/estudantes/me/perfil", response_model=PerfilCompletoResposta)
    async def atualizar_completo(
        requisicao: AtualizarPerfilCompletoRequisicao,
        request: Request,
    ) -> PerfilCompletoResposta:
        """Atualiza todos os campos editáveis do estudante autenticado.

        O handler deriva o proprietário de ``request.state``, converte JSON em
        value objects e traduz falhas de domínio em respostas HTTP. Ele existe
        para oferecer uma operação integral sem aceitar ID de proprietário do
        cliente nem alterar os endpoints existentes.
        """
        usuario_autenticado = getattr(request.state, "usuario_id", None)
        if not isinstance(usuario_autenticado, UUID):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Autenticação necessária.")
        if atualizar_perfil_completo is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Atualização indisponível.")
        try:
            dados_contato = DadosContato(
                endereco=Endereco(requisicao.endereco),
                telefones=tuple(Telefone(telefone) for telefone in requisicao.telefones),
                linkedin=requisicao.linkedin,
                curriculo_lattes=requisicao.curriculo_lattes,
                cidade=requisicao.cidade,
            )
            usuario = await atualizar_perfil_completo.executar(
                AtualizarPerfilCompletoEntrada(
                    usuario_id=UsuarioId(usuario_autenticado),
                    nome=Nome(requisicao.nome),
                    email=Email(requisicao.email),
                    dados_contato=dados_contato,
                )
            )
        except RegraDeDominioViolada as erro:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(erro)) from erro
        except PerfilNaoEncontrado as erro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
        except PerfilExcluido as erro:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(erro)) from erro
        except EmailJaCadastrado as erro:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(erro)) from erro

        assert usuario.dados_contato is not None
        return PerfilCompletoResposta(
            id=usuario.id.valor,
            nome=usuario.nome.valor,
            email=usuario.email.valor,
            endereco=usuario.dados_contato.endereco.valor,
            cidade=(
                usuario.dados_contato.cidade.valor
                if usuario.dados_contato.cidade is not None
                else None
            ),
            telefones=[telefone.valor for telefone in usuario.dados_contato.telefones],
            linkedin=usuario.dados_contato.linkedin,
            curriculo_lattes=usuario.dados_contato.curriculo_lattes,
        )

    @router.put("/estudantes/{usuario_id}", response_model=PerfilResposta)
    async def editar(
        usuario_id: UUID,
        requisicao: EditarPerfilRequisicao,
        request: Request,
    ) -> PerfilResposta:
        """Executa edição HTTP e devolve os dados públicos do perfil atualizado.

        O handler cria VOs e identidade tipada, aguarda o caso de uso e traduz
        ausência, exclusão e duplicidade sem expor detalhes internos. Ele
        existe para expor a edição sem levar HTTP à Application.
        """
        if editar_perfil is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Edição indisponível.")
        usuario_autenticado = getattr(request.state, "usuario_id", None)
        if not isinstance(usuario_autenticado, UUID):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Autenticação necessária.")
        if usuario_autenticado != usuario_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="A sessão não pode alterar este perfil.")
        try:
            entrada = EditarPerfilEntrada(
                usuario_id=UsuarioId(usuario_id),
                nome=Nome(requisicao.nome),
                email=Email(requisicao.email),
            )
            usuario = await editar_perfil.executar(entrada)
        except RegraDeDominioViolada as erro:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(erro)) from erro
        except PerfilNaoEncontrado as erro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
        except PerfilExcluido as erro:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(erro)) from erro
        except EmailJaCadastrado as erro:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(erro)) from erro
        return PerfilResposta(id=usuario.id.valor, nome=usuario.nome.valor, email=usuario.email.valor)

    @router.delete("/estudantes/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def excluir(usuario_id: UUID) -> None:
        """Executa exclusão lógica HTTP sem expor o estado resultante ao cliente.

        O handler converte a identidade de rota, aguarda o caso de uso e traduz
        ausência sem revelar se o perfil já estava excluído. Ele existe para
        tornar a exclusão idempotente também do ponto de vista HTTP.
        """
        if excluir_perfil is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Exclusão indisponível.")
        entrada = ExcluirPerfilEntrada(usuario_id=UsuarioId(usuario_id))
        try:
            await excluir_perfil.executar(entrada)
        except PerfilNaoEncontrado as erro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro

    return router
