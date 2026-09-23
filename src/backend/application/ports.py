"""Define portas internas necessárias às operações de estudantes.

As portas descrevem somente as capacidades de que o caso de uso precisa, sem
escolher banco, ORM ou estratégia de geração de UUID. Elas existem para que a
orquestração permaneça testável com doubles e para que adapters futuros possam
depender do núcleo da aplicação.
"""

from datetime import datetime
from typing import Protocol

# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
from backend.domain.itens_perfil import ExperienciaProfissional
# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
from backend.domain.itens_perfil import ProjetoAcademico
from backend.domain.usuario import Usuario
# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
from backend.domain.itens_perfil import FormacaoAcademica
from backend.domain.value_objects import Email, UsuarioId
from backend.domain.value_objects import FormacaoAcademicaId
# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
from backend.domain.value_objects import ExperienciaProfissionalId
# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
from backend.domain.value_objects import ProjetoAcademicoId


# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260916-cadastro-acesso-estudante-v002.md#v002
class RepositorioUsuario(Protocol):
    """Define a capacidade assíncrona de consultar e persistir usuários.

    A porta recebe e devolve conceitos de domínio e torna aguardáveis somente a
    consulta e o salvamento, que serão I/O em adapters futuros. Ela existe para
    que o caso de uso libere o fluxo durante a persistência sem conhecer banco,
    ORM ou implementação concreta.
    """

    async def existe_por_email(self, email: Email) -> bool:
        """Informa assincronamente se existe usuário com o e-mail fornecido.

        Implementações aguardam o mecanismo de armazenamento e preservam o
        contrato booleano do núcleo. O método existe para que o caso de uso
        interrompa cadastros duplicados antes de solicitar persistência.
        """

    async def salvar(self, usuario: Usuario) -> None:
        """Solicita assincronamente a persistência de usuário válido.

        Implementações aguardam o armazenamento sem alterar regra de negócio.
        O método existe para separar a decisão de cadastro da infraestrutura
        Code First que será implementada por adapter externo.
        """

    async def obter_por_email(self, email: Email) -> Usuario | None:
        """Obtém assincronamente a conta associada ao e-mail, quando ela existir.

        Implementações aguardam a leitura no armazenamento e devolvem somente o
        agregado do domínio ou ausência, sem revelar detalhes de persistência.
        O método existe para que o caso de uso de acesso confira credenciais sem
        acoplar a Application ao banco, ORM ou API.
        """

    # Proveniência: decision-analysis prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md#v001
    async def obter_por_id(self, usuario_id: UsuarioId) -> Usuario | None:
        """Obtém assincronamente o perfil identificado, quando ele existir.

        Implementações consultam o armazenamento e devolvem somente o agregado
        ou ausência, sem expor detalhes externos. O método existe para que os
        casos de uso editem e excluam o perfil correto por identidade tipada.
        """

    async def atualizar(self, usuario: Usuario) -> None:
        """Solicita assincronamente a persistência do novo estado do usuário.

        Implementações atualizam a representação armazenada sem introduzir
        regras de perfil na infraestrutura. O método existe para persistir as
        transições de edição e exclusão decididas pelo núcleo.
        """


# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
class RepositorioFormacaoAcademica(Protocol):
    """Define a persistência assíncrona de formações acadêmicas válidas.

    A porta recebe uma entidade de domínio pronta e delega o I/O ao adapter que
    a implementar, sem escolher ORM, tabela ou transação. Ela existe para que o
    caso de uso registre formações sem acoplar a Application à infraestrutura.
    """

    async def salvar(self, formacao: FormacaoAcademica) -> None:
        """Solicita a persistência assíncrona de uma formação acadêmica válida.

        Implementações aguardam o armazenamento e preservam a entidade recebida
        sem criar regras de negócio adicionais. O método existe para separar a
        intenção de cadastrar formação do mecanismo concreto de persistência.
        """


# Proveniência: decision-analysis prompts/backend/20260920-202606-edicao-exclusao-perfil-estudante-v001.md#v001
class Relogio(Protocol):
    """Define a obtenção substituível do instante corrente para casos de uso.

    A porta entrega um ``datetime`` sem escolher relógio do sistema ou fuso na
    Application e pode ser substituída por stub. Ela existe para tornar a data
    de exclusão determinística em testes e externa ao domínio.
    """

    def agora(self) -> datetime:
        """Obtém o instante controlado que será aplicado à exclusão lógica.

        Implementações consultam sua fonte de tempo e retornam o valor sem
        alterar agregados. O método existe para separar a passagem do tempo da
        transição pura executada por ``Usuario``.
        """


class VerificadorSenha(Protocol):
    """Define a comparação segura entre uma senha informada e um hash armazenado.

    A porta deixa o algoritmo criptográfico na infraestrutura e entrega apenas
    uma decisão booleana ao caso de uso. Ela existe para que autenticação não
    armazene senha em texto claro nem dependa de uma biblioteca de segurança.
    """

    def confere(self, senha: str, hash_senha: str) -> bool:
        """Informa se a senha em texto claro corresponde ao hash persistido.

        Implementações usam uma comparação apropriada ao formato de hash e não
        expõem dados da credencial. O método existe para separar a decisão de
        acesso da derivação criptográfica concreta.
        """


# Proveniência: decision-analysis prompts/backend/20260914-cadastro-acesso-estudante-v001.md#v001
class GeradorUsuarioId(Protocol):
    """Define a geração substituível da identidade de um usuário.

    A porta encapsula a origem do UUID e entrega um ``UsuarioId`` já tipado ao
    caso de uso. Ela existe para que testes controlem a identidade gerada sem
    depender de aleatoriedade ou de uma implementação externa.
    """

    def gerar(self) -> UsuarioId:
        """Gera uma identidade tipada para um novo usuário.

        Implementações podem obter um UUID de qualquer fonte compatível, mas
        retornam o value object do domínio. O método existe para manter o fluxo
        de cadastro determinístico em testes e independente da infraestrutura.
        """


# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
class GeradorFormacaoAcademicaId(Protocol):
    """Define a geração substituível de identidade para uma formação acadêmica.

    A porta encapsula a origem do UUID e devolve o value object tipado, sem
    impor uma estratégia de aleatoriedade à Application. Ela existe para que o
    cadastro crie identidades determinísticas em testes e independentes de I/O.
    """

    def gerar(self) -> FormacaoAcademicaId:
        """Gera uma identidade tipada para a nova formação acadêmica.

        Implementações podem consultar qualquer fonte compatível e retornam o
        tipo de domínio já validado. O método existe para manter a criação da
        entidade explícita e substituível no caso de uso.
# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
class RepositorioExperienciaProfissional(Protocol):
    """Define a persistência necessária ao cadastro de uma experiência.

    A porta recebe a entidade já validada e delega seu armazenamento a uma
    implementação externa assíncrona, sem conhecer banco ou ORM. Ela existe
    para manter o caso de uso independente da tecnologia de persistência.
    """

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    async def salvar(self, experiencia: ExperienciaProfissional) -> None:
        """Armazena uma experiência profissional validada.

        A implementação concreta executa a persistência depois da criação da
        entidade pelo caso de uso, preservando o contrato assíncrono. O método
        existe para registrar a nova experiência sem acoplar a aplicação a um
        mecanismo de armazenamento específico.
        """


# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
class GeradorExperienciaProfissionalId(Protocol):
    """Fornece identificadores tipados para novas experiências profissionais.

    A porta separa a política de geração de identificadores da orquestração do
    cadastro e devolve um value object válido. Ela existe para permitir que o
    núcleo seja testado de modo determinístico e permaneça livre de infraestrutura.
    """

    # Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
    def gerar(self) -> ExperienciaProfissionalId:
        """Gera o identificador da próxima experiência profissional.

        A implementação define a estratégia concreta de geração e retorna o
        tipo de domínio esperado pelo caso de uso. O método existe para que a
        criação da entidade sempre receba uma identidade explícita e válida.
        """


# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
class RepositorioProjetoAcademico(Protocol):
    """Define a persistência necessária ao cadastro de um projeto acadêmico.

    A porta recebe a entidade já validada e delega o armazenamento a uma
    implementação externa assíncrona, sem conhecer banco ou ORM. Ela existe
    para manter o caso de uso independente da tecnologia de persistência.
    """

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    async def salvar(self, projeto: ProjetoAcademico) -> None:
        """Armazena um projeto acadêmico validado.

        A implementação concreta persiste a entidade depois da criação pelo
        caso de uso, preservando o contrato assíncrono. O método existe para
        registrar o projeto sem acoplar a Application ao armazenamento.
        """


# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
class GeradorProjetoAcademicoId(Protocol):
    """Fornece identificadores tipados para novos projetos acadêmicos.

    A porta separa a geração de identidade da orquestração e devolve um value
    object válido. Ela existe para tornar os testes determinísticos e manter o
    núcleo livre da estratégia concreta de geração de UUID.
    """

    # Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
    def gerar(self) -> ProjetoAcademicoId:
        """Gera o identificador do próximo projeto acadêmico.

        A implementação escolhe a estratégia concreta e retorna o tipo de
        domínio esperado. O método existe para que a criação sempre receba uma
        identidade explícita e válida.
        """
