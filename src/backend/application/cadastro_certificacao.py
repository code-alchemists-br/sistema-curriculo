from dataclasses import dataclass
from backend.application.ports import GeradorCertificacaoId, RepositorioCertificacao
from backend.domain.itens_perfil import Certificacao
from backend.domain.value_objects import UsuarioId

@dataclass(frozen=True, slots=True)
class CadastrarCertificacaoEntrada:
    usuario_id: UsuarioId
    nome: str
    organizacao_emissora: str

class CadastrarCertificacao:
    def __init__(self, repositorio: RepositorioCertificacao, gerador_id: GeradorCertificacaoId) -> None:
        self._repositorio = repositorio
        self._gerador_id = gerador_id

    async def executar(self, entrada: CadastrarCertificacaoEntrada) -> Certificacao:
        certificacao = Certificacao(
            id=self._gerador_id.gerar(),
            usuario_id=entrada.usuario_id,
            nome=entrada.nome,
            organizacao_emissora=entrada.organizacao_emissora,
        )
        await self._repositorio.salvar(certificacao)
        return certificacao