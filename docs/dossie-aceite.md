# Dossiê de evidências para aceite

**Estado:** compilação inicial de evidências de código da branch `dev`, commit `ab2b8bc28c19bd55cacef41a4401ad9e34040276` (19/10/2026). Não é uma decisão de entrega; faltam execução demonstrável e aprovação da equipe.

## Evidência técnica localizada

| Área | Evidência no repositório | O que demonstra | O que não demonstra |
| --- | --- | --- | --- |
| API de vagas | `src/backend/tests/test_api_vagas.py` | Casos unitários da fronteira HTTP, resultados, vazio, autenticação e falhas controladas. | Serviço externo do Grupo 2 ativo em ambiente integrado. |
| Cadastro complementar | `src/backend/tests/test_api_competencia.py`, `test_api_idioma.py`, `test_api_curso.py`, `test_api_certificacao.py`, `test_api_projeto_academico.py`, `test_api_link_profissional.py` | Contratos de cadastro cobertos por testes unitários. | Fluxo completo na interface. |
| Prévia | `src/backend/tests/test_api_previa_versao_curriculo.py`; testes dos modelos frontend | Contrato de leitura e renderizações isoladas. | Navegação completa conectada ou exportação PDF/DOCX. |
| Jornada simulada | `src/frontend/app/jornada-selecao-previa-exportacao.e2e.test.tsx` | Um harness local testa partes do fluxo usando seleção e exportador simulados. | Jornada integrada real ou binário PDF gerado pelo produto. |
| Registro de mudanças | PR #564: <https://github.com/code-alchemists-br/sistema-curriculo/pull/564> | Merge de política de limites recarregável na branch. | Aceite do projeto ou adequação de ponta a ponta entregue. |

## Itens obrigatórios ainda sem evidência

- [ ] Execução da demonstração, com data, commit, ambiente, roteiro seguido e capturas sanitizadas.
- [ ] Resultado observado de cada cenário e falhas reais encontradas.
- [ ] Decisão formal da equipe: aceitar ou não aceitar; responsável e justificativa.
- [ ] Lições aprendidas baseadas na execução.
- [ ] Pendências pós-entrega, donos e prazos.

Não marque os itens acima como concluídos por causa da existência de testes automatizados ou de um mock. Não inclua dados pessoais, credenciais ou tokens nas evidências.

## Relação com o registro de lições

Após a reunião, preencher [`registro-aceite-licoes.md`](registro-aceite-licoes.md), anexar/ligar as evidências e atualizar este dossiê com os resultados reais.

**Card:** #436. O índice de evidências está iniciado, mas o critério de aceite do card permanece pendente enquanto demonstração, decisão de entrega e lições não forem registradas.
