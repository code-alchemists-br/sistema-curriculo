# Contratos HTTP das informações complementares

**Escopo:** rotas de criação existentes na branch `dev`, commit `ab2b8bc` (19/10/2026). Os caminhos abaixo são rotas FastAPI sem prefixo adicional no código-fonte; um gateway de implantação pode acrescentar um prefixo.

Todas as rotas de criação abaixo obtêm o proprietário a partir da sessão autenticada. O cliente não deve enviar `usuario_id` no corpo para escolher o dono. O sucesso é `201 Created`; ausência de sessão resulta em `401`, executor não configurado em `503` e corpo/regra inválidos em `422`. Competência, idioma, curso, certificação e link profissional também convertem duplicidade em `409 Conflict`.

| Recurso | Rota e método | Campos de entrada | Campos principais da resposta |
| --- | --- | --- | --- |
| Competência | `POST /competencias` | `categoria` (`tecnica` ou `comportamental`), `descricao`, `nivel` | `id`, `usuario_id`, `categoria`, `descricao`, `nivel` |
| Idioma | `POST /idiomas` | `idioma`, `nivel` | `id`, `usuario_id`, `idioma`, `nivel` |
| Curso | `POST /cursos` | `nome`, `instituicao`, `carga_horaria` opcional (`integer` estrito ou `null`) | `id`, `usuario_id`, `nome`, `instituicao`, `carga_horaria` |
| Certificação | `POST /certificacoes` | `nome`, `organizacao_emissora` | `id`, `usuario_id`, `nome`, `organizacao_emissora` |
| Projeto acadêmico | `POST /projetos-academicos` | `titulo`, `descricao`, `tecnologias` | `id`, `usuario_id`, `titulo`, `descricao`, `tecnologias` |
| Link profissional | `POST /links-profissionais` | `rotulo`, `url` | `id`, `usuario_id`, `rotulo`, `url` |

O backend valida os textos e aplica as regras do domínio. Certificação valida texto e limites de tamanho; link profissional aceita URL HTTP/HTTPS válida e não expõe sua chave de comparação normalizada; curso não converte silenciosamente carga horária fracionária; categoria de competência é restrita ao enum publicado.

## Limite de escopo da API atual

Este inventário documenta as rotas existentes, não presume CRUD completo. Para estes seis recursos, o código consultado publica rotas `POST` de cadastro, mas não publica rotas genéricas `GET`, `PUT` ou `DELETE` equivalentes. Não invente tais endpoints em clientes ou manuais. A prévia de currículo tem DTOs próprios e não expõe chaves internas de armazenamento.

O endpoint `POST /projetos-academicos/sugestao-descricao` é separado do cadastro: recebe título e tecnologias, devolve somente uma sugestão textual (`200`) e não salva o projeto. A descrição deve ser revisada pelo estudante antes do cadastro.

## Referências de verificação

- Backend: `api/competencia.py`, `api/idioma.py`, `api/curso.py`, `api/certificacao.py`, `api/projeto_academico.py`, `api/link_profissional.py` e os testes `test_api_competencia.py`, `test_api_idioma.py`, `test_api_curso.py`, `test_api_certificacao.py`, `test_api_projeto_academico.py`, `test_api_link_profissional.py`.
- Composição: `api/factory.py` registra as seis rotas.

**Card:** #425.
