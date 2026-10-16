"""Implementa a geração de identidades de domínio com UUID versão 4.

O adapter encapsula a fonte de aleatoriedade e devolve value objects já tipados,
sem expor o gerador de UUID às camadas internas. Ele existe para atender a porta
de identidade com uma estratégia concreta e substituível.
"""

from uuid import uuid4

from backend.application.ports import (
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    GeradorCertificacaoId,
    GeradorCompetenciaId,
    GeradorCurriculoId,
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    GeradorCursoId,
    # Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
    GeradorIdiomaId,
    # Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
    GeradorLinkProfissionalId,
    # Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
    GeradorProjetoAcademicoId,
)
from backend.domain.value_objects import (
    # Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
    CertificacaoId,
    CompetenciaId,
    CurriculoId,
    # Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
    CursoId,
    # Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
    IdiomaId,
    # Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
    LinkProfissionalId,
    # Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
    ProjetoAcademicoId,
)

# Proveniência: decision-analysis prompts/backend/20261006-183934-criacao-versao-curriculo-v001.md#v001


class GeradorCurriculoIdUuid4(GeradorCurriculoId):
    """Gera identidades de versão de currículo a partir de UUID versão 4.

    A implementação cria um UUID aleatório a cada chamada e o embrulha em um
    ``CurriculoId``. Ela existe para que a criação de versões receba identidades
    únicas sem que a Application conheça a biblioteca ou a estratégia de geração.
    """

    def gerar(self) -> CurriculoId:
        """Gera um ``CurriculoId`` novo e aleatório.

        O método chama o gerador de UUID versão 4 e devolve o value object do
        domínio, sem manter estado entre chamadas. Ele existe para implementar o
        contrato da porta de identidade de currículo.
        """
        return CurriculoId(uuid4())


# Proveniência: decision-analysis prompts/backend/20261013-142942-cadastro-competencias-api-v002.md#v002
class GeradorCompetenciaIdUuid4(GeradorCompetenciaId):
    """Gera identidades de competência com UUID versão 4.

    A implementação cria um UUID aleatório e o encapsula no value object de
    competência. Ela existe para satisfazer a porta da Application sem expor a
    biblioteca de geração de identidade às camadas internas.
    """

    def gerar(self) -> CompetenciaId:
        """Devolve uma identidade nova e tipada para competência.

        O método delega a aleatoriedade ao UUID4 e converte seu resultado para
        ``CompetenciaId``. Ele existe para oferecer ao caso de uso uma origem
        concreta, substituível e sem estado de identificadores.
        """
        return CompetenciaId(uuid4())


# Proveniência: decision-analysis prompts/backend/20261015-094754-cadastro-idiomas-api-v001.md#v001
class GeradorIdiomaIdUuid4(GeradorIdiomaId):
    """Gera identidades de idioma com UUID versão 4.

    A implementação cria um UUID aleatório e o encapsula no value object de
    idioma. Ela existe para satisfazer a porta da Application sem expor a
    biblioteca de geração de identidade às camadas internas.
    """

    def gerar(self) -> IdiomaId:
        """Devolve uma identidade nova e tipada para idioma.

        O método delega a aleatoriedade ao UUID4 e converte seu resultado para
        ``IdiomaId``. Ele existe para oferecer ao caso de uso uma origem
        concreta, substituível e sem estado de identificadores.
        """
        return IdiomaId(uuid4())


# Proveniência: decision-analysis prompts/backend/20261015-130837-cadastro-curso-api-v001.md#v001
class GeradorCursoIdUuid4(GeradorCursoId):
    """Gera identidades de curso com UUID versão 4.

    A implementação cria um UUID aleatório e o encapsula no value object de
    curso. Ela existe para satisfazer a porta da Application sem expor a
    biblioteca de geração de identidade às camadas internas.
    """

    def gerar(self) -> CursoId:
        """Devolve uma identidade nova e tipada para curso.

        O método delega a aleatoriedade ao UUID4 e converte seu resultado para
        ``CursoId``. Ele existe para oferecer ao caso de uso uma origem
        concreta, substituível e sem estado de identificadores.
        """
        return CursoId(uuid4())
# Proveniência: decision-analysis prompts/backend/20261015-115730-cadastro-certificacao-api-v001.md#v001
class GeradorCertificacaoIdUuid4(GeradorCertificacaoId):
    """Gera identidades de certificação a partir de UUID versão 4.

    A implementação obtém um identificador pseudoaleatório e o devolve como
    ``CertificacaoId`` tipado, sem manter estado. Ela existe para fornecer a
    estratégia padrão de identidade exigida pela porta do caso de uso.
    """

    def gerar(self) -> CertificacaoId:
        """Gera um ``CertificacaoId`` novo com UUID4 nativo.

        O método delega a aleatoriedade ao UUID4 e converte seu resultado para
        ``CertificacaoId``. Ele existe para oferecer ao caso de uso uma origem
        concreta, substituível e sem estado de identificadores.
        """
        return CertificacaoId(uuid4())


# Proveniência: decision-analysis prompts/backend/20261015-212205-expor-cadastro-projeto-academico-v001.md#v001
class GeradorProjetoAcademicoIdUuid4(GeradorProjetoAcademicoId):
    """Gera identidades de projeto acadêmico com UUID versão 4.

    A implementação cria um UUID aleatório e o encapsula no value object do
    projeto. Ela existe para fornecer a estratégia concreta exigida pela porta
    sem expor geração de identidade à Application.
    """

    def gerar(self) -> ProjetoAcademicoId:
        """Devolve uma identidade nova e tipada de projeto acadêmico.

        O método delega a aleatoriedade ao UUID4 e converte o resultado para o
        value object esperado. Ele existe para atender o contrato de geração do
        caso de uso de cadastro.
        """
        return ProjetoAcademicoId(uuid4())


# Proveniência: decision-analysis prompts/backend/20261015-152803-cadastro-link-profissional-api-v001.md#v001
class GeradorLinkProfissionalIdUuid4(GeradorLinkProfissionalId):
    """Gera identidades de link profissional com UUID versão 4.

    A implementação cria um UUID aleatório e o encapsula no value object de
    link profissional. Ela existe para satisfazer a porta da Application sem
    expor a biblioteca de geração de identidade às camadas internas.
    """

    def gerar(self) -> LinkProfissionalId:
        """Devolve uma identidade nova e tipada para link profissional.

        O método delega a aleatoriedade ao UUID4 e converte seu resultado para
        ``LinkProfissionalId``. Ele existe para oferecer ao caso de uso uma origem
        concreta, substituível e sem estado de identificadores.
        """
        return LinkProfissionalId(uuid4())
