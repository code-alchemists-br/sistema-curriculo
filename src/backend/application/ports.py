"""Define portas internas necessárias às operações de estudantes.

As portas descrevem somente as capacidades de que o caso de uso precisa, sem
escolher banco, ORM ou estratégia de geração de UUID. Elas existem para que a
orquestração permaneça testável com doubles e para que adapters futuros possam
depender do núcleo da aplicação.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol

from backend.domain.curriculo import Curriculo

# Proveniência: decision-analysis prompts/backend/20260920-210822-refatoracao-entidades-dominio-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260923-153647-cadastro-formacao-academica-v001.md#v001
from backend.domain.itens_perfil import (
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    CategoriaCompetencia,
    Competencia,
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    Curso,
    Documento,
    ExperienciaProfissional,
    FormacaoAcademica,
    Idioma,
    # Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
    LinkProfissional,
    ProjetoAcademico,
)
from backend.domain.usuario import Usuario

# Proveniência: decision-analysis prompts/backend/20260921-162749-cadastro-experiencias-profissionais-v001.md#v001
# Proveniência: decision-analysis prompts/backend/20260921-235140-cadastro-projetos-academicos-v001.md#v001
from backend.domain.value_objects import (
    # Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
    CompetenciaId,
    CurriculoId,
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    CursoId,
    Email,
    ExperienciaProfissionalId,
    FormacaoAcademicaId,
    # Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
    IdiomaId,
    # Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
    LinkProfissionalId,
    ProjetoAcademicoId,
    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    ReferenciaCurriculo,
    UsuarioId,
)


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
# Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
class RepositorioFormacaoAcademica(Protocol):
    """Define consulta e persistência assíncrona de formações acadêmicas.

    A porta recebe identidades tipadas para consultar por formação e
    proprietário, e entidades válidas para salvar ou atualizar, sem escolher
    ORM, tabela ou transação. Ela existe para que os casos de uso cadastrem e
    editem formações sem acoplar a Application à infraestrutura.
    """

    async def salvar(self, formacao: FormacaoAcademica) -> None:
        """Solicita a persistência assíncrona de uma formação acadêmica válida.

        Implementações aguardam o armazenamento e preservam a entidade recebida
        sem criar regras de negócio adicionais. O método existe para separar a
        intenção de cadastrar formação do mecanismo concreto de persistência.
        """

    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    async def obter_por_id_e_usuario(
        self, formacao_id: FormacaoAcademicaId, usuario_id: UsuarioId
    ) -> FormacaoAcademica | None:
        """Obtém a formação somente quando pertence ao usuário informado.

        A implementação consulta conjuntamente identidade e proprietário e
        retorna ausência tanto para ID inexistente quanto alheio. Ela existe
        para que a edição não revele a existência de formações de outros usuários.
        """

    # Proveniência: decision-analysis prompts/backend/20261014-210357-expor-edicao-formacao-academica-v001.md#v001
    async def atualizar(self, formacao: FormacaoAcademica) -> None:
        """Solicita a atualização de uma formação existente e válida.

        A implementação persiste o estado completo recebido sem alterar
        invariantes ou controlar a tecnologia/transação. Ela existe para salvar
        a edição decidida pelo caso de uso através de uma porta interna.
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
        """


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


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class RepositorioCompetencia(Protocol):
    """Define a consulta e a persistência de competências válidas.

    A porta recebe conceitos de domínio e expõe a chave de duplicidade sem
    escolher banco, índice ou ORM. Ela existe para que o caso de uso impeça
    competências equivalentes e permaneça testável com doubles.
    """

    async def existe_por_chave_de_duplicidade(
        self,
        usuario_id: UsuarioId,
        categoria: CategoriaCompetencia,
        descricao_normalizada: str,
    ) -> bool:
        """Informa se já existe competência com a chave lógica fornecida.

        Implementações consultam o armazenamento usando proprietário, categoria
        e descrição canônica, sem definir a política de normalização. O método
        existe para que a Application interrompa o cadastro duplicado antes de
        solicitar persistência.
        """

    async def salvar(self, competencia: Competencia) -> None:
        """Solicita a persistência assíncrona de uma competência válida.

        Implementações armazenam a entidade recebida sem acrescentar regra de
        negócio. O método existe para separar a intenção de cadastro do adapter
        que futuramente reforçará a mesma chave por índice único.
        """


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class GeradorCompetenciaId(Protocol):
    """Fornece identidades tipadas para novas competências.

    A porta encapsula a origem da identidade e devolve ``CompetenciaId`` pronto
    para o domínio. Ela existe para manter o caso de uso determinístico em
    testes e independente de uma estratégia concreta de UUID.
    """

    def gerar(self) -> CompetenciaId:
        """Gera a identidade da próxima competência cadastrada.

        Implementações escolhem a fonte do UUID e devolvem o value object
        correspondente. O método existe para que a entidade seja construída
        com identidade explícita sem acoplar a Application à infraestrutura.
        """


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
class RepositorioIdioma(Protocol):
    """Define a consulta e a persistência de idiomas válidos.

    A porta recebe conceitos de domínio e expõe a chave de duplicidade sem
    escolher banco, índice ou ORM. Ela existe para que o caso de uso impeça
    idiomas equivalentes e permaneça testável com doubles.
    """

    async def existe_por_chave_de_duplicidade(
        self,
        usuario_id: UsuarioId,
        idioma_normalizado: str,
    ) -> bool:
        """Informa se já existe idioma com a chave lógica fornecida.

        Implementações consultam o armazenamento usando proprietário e a
        denominação canônica, sem definir a política de normalização. O método
        existe para que a Application interrompa o cadastro duplicado antes de
        solicitar persistência.
        """

    async def salvar(self, idioma: Idioma) -> None:
        """Solicita a persistência assíncrona de um idioma válido.

        Implementações armazenam a entidade recebida sem acrescentar regra de
        negócio. O método existe para separar a intenção de cadastro do adapter
        que futuramente reforçará a mesma chave por índice único.
        """


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
class GeradorIdiomaId(Protocol):
    """Fornece identidades tipadas para novos idiomas.

    A porta encapsula a origem da identidade e devolve ``IdiomaId`` pronto
    para o domínio. Ela existe para manter o caso de uso determinístico em
    testes e independente de uma estratégia concreta de UUID.
    """

    def gerar(self) -> IdiomaId:
        """Gera a identidade do próximo idioma cadastrado.

        Implementações escolhem a fonte do UUID e devolvem o value object
        correspondente. O método existe para que a entidade seja construída
        com identidade explícita sem acoplar a Application à infraestrutura.
        """


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class RepositorioCurso(Protocol):
    """Define a consulta e a persistência de cursos válidos.

    A porta recebe conceitos de domínio e expõe a verificação de duplicidade
    sem escolher banco, índice ou ORM. Ela existe para que o caso de uso impeça
    cursos equivalentes e permaneça testável com doubles.
    """

    async def existe_por_chave_de_duplicidade(
        self,
        usuario_id: UsuarioId,
        nome_normalizado: str,
        instituicao_normalizada: str,
    ) -> bool:
        """Informa se já existe curso com a chave lógica de nome e instituição fornecida.

        Implementações consultam o armazenamento usando proprietário, nome e
        instituição canônicos, sem definir a política de normalização. O método
        existe para que a Application interrompa o cadastro duplicado antes de
        solicitar persistência.
        """

    async def salvar(self, curso: Curso) -> None:
        """Solicita a persistência assíncrona de um curso válido.

        Implementações armazenam a entidade recebida sem acrescentar regra de
        negócio. O método existe para separar a intenção de cadastro do adapter
        que futuramente reforçará a mesma chave por índice único.
        """


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class GeradorCursoId(Protocol):
    """Fornece identidades tipadas para novos cursos.

    A porta encapsula a origem da identidade e devolve ``CursoId`` pronto
    para o domínio. Ela existe para manter o caso de uso determinístico em
    testes e independente de uma estratégia concreta de UUID.
    """

    def gerar(self) -> CursoId:
        """Gera a identidade do próximo curso cadastrado.

        Implementações escolhem a fonte do UUID e devolvem o value object
        correspondente. O método existe para que a entidade seja construída
        com identidade explícita sem acoplar a Application à infraestrutura.
        """


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class RepositorioLinkProfissional(Protocol):
    """Define a consulta e a persistência de links profissionais válidos.

    A porta recebe conceitos de domínio e expõe a verificação de duplicidade
    sem escolher banco, índice ou ORM. Ela existe para que o caso de uso impeça
    links duplicados para o mesmo estudante e permaneça testável com doubles.
    """

    async def existe_por_chave_de_duplicidade(
        self,
        usuario_id: UsuarioId,
        url_normalizada: str,
    ) -> bool:
        """Informa se já existe link profissional com a URL normalizada para o usuário.

        Implementações consultam o armazenamento usando a identidade do proprietário
        e a chave canônica da URL, sem definir a política de normalização. O método
        existe para que a Application interrompa o cadastro duplicado antes de
        solicitar persistência.
        """

    async def salvar(self, link: LinkProfissional) -> None:
        """Solicita a persistência assíncrona de um link profissional válido.

        Implementações armazenam a entidade recebida sem acrescentar regra de
        negócio. O método existe para separar a intenção de cadastro do adapter
        que futuramente reforçará a mesma chave por índice único.
        """


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class GeradorLinkProfissionalId(Protocol):
    """Fornece identidades tipadas para novos links profissionais.

    A porta encapsula a origem da identidade e devolve ``LinkProfissionalId`` pronto
    para o domínio. Ela existe para manter o caso de uso determinístico em
    testes e independente de uma estratégia concreta de UUID.
    """

    def gerar(self) -> LinkProfissionalId:
        """Gera a identidade do próximo link profissional cadastrado.

        Implementações escolhem a fonte do UUID e devolvem o value object
        correspondente. O método existe para que a entidade seja construída
        com identidade explícita sem acoplar a Application à infraestrutura.
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


class RepositorioCurriculo(Protocol):
    """Define a capacidade assíncrona de consultar e persistir versões de currículo.

    A porta recebe e devolve o agregado de domínio e torna aguardáveis somente a
    consulta, a inserção e a atualização, que serão I/O em adapters. Ela existe
    para que os casos de uso de criação e manutenção de versões não conheçam
    banco, ORM ou implementação concreta.
    """

    async def obter_por_id(self, curriculo_id: CurriculoId) -> Curriculo | None:
        """Obtém assincronamente a versão de currículo identificada, quando existir.

        Implementações consultam o armazenamento e devolvem somente o agregado ou
        ausência, sem expor detalhes de persistência. O método existe para que o
        caso de uso localize a versão correta por identidade tipada.
        """

    async def atualizar(self, curriculo: Curriculo) -> None:
        """Solicita assincronamente a persistência do novo estado da versão.

        Implementações atualizam a representação armazenada sem introduzir regras
        de currículo na infraestrutura. O método existe para persistir a edição
        decidida pelo núcleo.
        """

    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    async def salvar(self, curriculo: Curriculo) -> None:
        """Solicita assincronamente a persistência de uma nova versão válida.

        Implementações inserem a representação do agregado já construído e
        validado pelo núcleo, sem introduzir regras de currículo na
        infraestrutura. O método existe para registrar a versão criada sem
        acoplar a Application ao armazenamento.
        """

    # Proveniência: decision-analysis prompts/backend/20261009-192604-listagem-versoes-curriculo-v001.md#v001
    async def listar_por_usuario(self, usuario_id: UsuarioId) -> tuple[Curriculo, ...]:
        """Lista assincronamente as versões de currículo pertencentes ao usuário.

        Implementações consultam o armazenamento pelo proprietário e devolvem os
        agregados completos, com suas referências, no mesmo contrato de
        ``obter_por_id``, ou uma tupla vazia, sem aplicar ordem nem regras de
        currículo. O método existe para que o caso de uso de listagem obtenha
        todas as versões do estudante sem conhecer banco, ORM ou tabelas.
        """

    # Proveniência: decision-analysis prompts/backend/20261013-183632-exclusao-versao-curriculo-v001.md#v001
    async def excluir(self, curriculo: Curriculo) -> None:
        """Solicita assincronamente a remoção definitiva da versão e de sua seleção.

        Implementações removem do armazenamento a versão e tudo o que depende
        dela, como as referências aos itens, sem introduzir regras de currículo
        na infraestrutura. O método existe para persistir a exclusão decidida
        pelo núcleo sem acoplar a Application a banco, ORM ou tabelas.
        """


# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
class GeradorCurriculoId(Protocol):
    """Fornece identificadores tipados para novas versões de currículo.

    A porta separa a geração de identidade da orquestração e devolve um value
    object válido. Ela existe para tornar os testes determinísticos e manter o
    núcleo livre da estratégia concreta de geração de UUID.
    """

    # Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001
    def gerar(self) -> CurriculoId:
        """Gera o identificador da próxima versão de currículo.

        A implementação escolhe a estratégia concreta e retorna o tipo de
        domínio esperado. O método existe para que a criação sempre receba uma
        identidade explícita e válida.
        """


# Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
class ConsultaProprietarioItem(Protocol):
    """Define a consulta do proprietário de um item do perfil referenciável.

    A porta recebe a referência tipada e devolve somente a identidade do dono,
    sem expor o item, o armazenamento ou o tipo concreto de repositório. Ela
    existe para que o caso de uso verifique que o item pertence ao mesmo
    usuário da versão, regra que atravessa agregados e não cabe ao domínio.
    """

    # Proveniência: decision-analysis prompts/backend/20261007-190814-selecao-itens-versao-curriculo-v001.md#v001
    async def obter_proprietario(
        self, referencia: ReferenciaCurriculo
    ) -> UsuarioId | None:
        """Obtém assincronamente o dono do item referenciado, quando ele existir.

        Implementações consultam o armazenamento do tipo de item indicado e
        devolvem a identidade do proprietário ou ausência, sem revelar detalhes
        de persistência. O método existe para que a seleção recuse itens
        inexistentes ou de outro usuário antes de alterar a versão.
        """


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
ItemPerfil = (
    FormacaoAcademica
    | ExperienciaProfissional
    | ProjetoAcademico
    | Competencia
    | Idioma
    | Documento
)


# Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
class ConsultaItemPerfil(Protocol):
    """Define a capacidade assíncrona de ler um item de perfil por sua referência.

    A porta recebe a referência tipada de uma versão de currículo e devolve a
    entidade do item correspondente, sem expor armazenamento. Ela existe para
    que a prévia leia os seis tipos de item por um único contrato, deixando a
    implementação por tipo a cargo de adapters.
    """

    # Proveniência: decision-analysis prompts/backend/20261008-183601-previa-versao-curriculo-v001.md#v001
    async def obter_item(self, referencia: ReferenciaCurriculo) -> ItemPerfil | None:
        """Obtém assincronamente o item referenciado, quando ele existir.

        Implementações consultam o armazenamento do tipo indicado pela
        referência e devolvem a entidade ou ausência, sem aplicar regras de
        propriedade. O método existe para que o caso de uso leia o conteúdo dos
        itens selecionados e decida sozinho o que pode ser exibido.
        """


# Proveniência: decision-analysis prompts/backend/20261009-110249-contrato-adaptador-busca-vagas-v002.md#v002
@dataclass(frozen=True, slots=True)
class VagaExternaDto:
    """Representa de forma imutável uma vaga retornada pela busca.

    A estrutura reúne os oito campos aprovados no modelo de referência e não
    inclui detalhes de transporte ou do provedor. Ela existe para tipar os
    resultados de busca consumidos pela Application.
    """

    id: str
    titulo: str
    empresa: str
    descricao: str
    requisitos: tuple[str, ...]
    localizacao: str
    modalidade: str
    url_candidatura: str


# Proveniência: decision-analysis prompts/backend/20261009-110249-contrato-adaptador-busca-vagas-v002.md#v002
class BuscadorVagas(Protocol):
    """Define a capacidade assíncrona interna de consultar vagas.

    A porta especifica os parâmetros e o DTO retornado sem nomear provedor ou
    transporte. Ela existe para que os casos de uso dependam de uma abstração
    que possa ser atendida por adapters externos ou doubles.
    """

    async def buscar_vagas(
        self,
        termo: str = "",
        filtros: dict[str, Any] | None = None,
    ) -> list[VagaExternaDto]:
        """Solicita a busca de vagas e retorna seus resultados tipados.

        A operação recebe o termo e o mapa opcional de filtros da assinatura e
        aguarda a implementação que realiza a consulta. Ela existe para
        manter a Application independente da origem da busca.
        """
