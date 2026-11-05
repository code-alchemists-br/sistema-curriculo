# Manual do Estudante — Sistema Currículo

**Projeto:** Sistema Currículo — FATEC-SP  
**Atualização:** 01/11/2026  
**Issue:** #433 — F12.13  
**Status:** Manual atualizado com orientações de exportação PDF/DOCX e tratamento de falhas comuns.

## 1. Apresentação

O Sistema Currículo foi desenvolvido para ajudar estudantes a organizar suas informações pessoais, acadêmicas e profissionais e utilizá-las na elaboração de currículos.

O sistema permite cadastrar informações, preparar diferentes versões de currículo, selecionar conteúdos e visualizar a apresentação das versões.

Também possui funcionalidades de geração de arquivos PDF e DOCX, destinadas ao compartilhamento de currículos e à edição dos documentos em aplicativos compatíveis.

Este manual apresenta a jornada prevista para o estudante, os formatos disponíveis para exportação e orientações para resolver problemas comuns.

**Importante:** algumas funcionalidades possuem implementação no backend, mas a integração completa de todos os controles à interface web ainda precisa ser confirmada em demonstração. Por isso, os procedimentos apresentados descrevem a utilização esperada, sem afirmar que todas as opções já estejam disponíveis na navegação atual.

## 2. Acesso ao sistema

O estudante deve utilizar sua própria conta para acessar as funcionalidades protegidas do Sistema Currículo.

Na interface de acesso, o usuário poderá utilizar as opções disponibilizadas para autenticação e cadastro.

Para proteger seus dados:

- não compartilhe sua senha;
- evite acessar sua conta em computadores públicos;
- encerre a sessão quando terminar de utilizar o sistema;
- não divulgue códigos de acesso ou informações de sessão.

O sistema utiliza a identidade autenticada para controlar o acesso aos currículos e aos dados cadastrados.

## 3. Cadastro das informações do perfil

O estudante pode organizar suas informações por categorias, incluindo:

- dados pessoais e de contato;
- formação acadêmica;
- experiências profissionais;
- cursos e certificações;
- competências;
- idiomas;
- projetos acadêmicos;
- links profissionais.

As informações devem ser preenchidas de forma clara e atualizada.

Os dados cadastrados poderão ser utilizados na composição das diferentes versões de currículo, conforme as funcionalidades disponíveis.

## 4. Criação de uma versão de currículo

O sistema permite trabalhar com diferentes versões de currículo.

Essa funcionalidade é útil para organizar informações conforme o tipo de vaga ou área profissional desejada.

O procedimento previsto envolve:

1. Acessar a área de currículos.
2. Criar uma versão.
3. Informar um título para identificá-la.
4. Escolher o modelo de apresentação.
5. Selecionar as informações que deverão compor a versão.
6. Conferir o conteúdo na prévia.

As versões permitem reutilizar dados do perfil sem precisar realizar um novo cadastro completo para cada currículo.

## 5. Seleção e organização das informações

O estudante pode utilizar itens previamente cadastrados em seu perfil para montar uma versão de currículo.

Entre os tipos de informações selecionáveis estão:

- formações acadêmicas;
- experiências profissionais;
- projetos acadêmicos;
- competências;
- idiomas;
- documentos complementares.

Também existe uma organização das seções do currículo.

A escolha dos itens de uma versão não deve apagar as informações originais do perfil nem impedir sua utilização em outras versões.

## 6. Escolha do modelo

O sistema possui dois modelos de apresentação identificados como:

| Modelo | Identificador |
|---|---|
| Clássico | `classico` |
| Compacto | `compacto` |

O modelo determina a apresentação das informações selecionadas.

A escolha do modelo não altera automaticamente os dados acadêmicos ou profissionais do estudante.

Antes de exportar, recomenda-se verificar se o conteúdo está legível e organizado no modelo selecionado.

## 7. Revisão e prévia do currículo

A prévia permite conferir o conteúdo e a organização de uma versão antes do compartilhamento.

O estudante deve verificar:

1. Nome e informações de contato.
2. Formação acadêmica.
3. Experiências profissionais.
4. Competências e idiomas.
5. Projetos e outras informações selecionadas.
6. Ordem das seções.
7. Apresentação geral do documento.

O backend também possui uma funcionalidade de revisão que identifica informações obrigatórias ausentes e recomendações de melhoria.

A revisão distingue erros e avisos. Erros impedem que a revisão seja considerada aprovada, enquanto avisos representam sugestões.

Caso alguma informação esteja incorreta, o estudante deve realizar a alteração na funcionalidade correspondente e conferir novamente o currículo.

## 8. Exportação do currículo

A exportação permite obter um arquivo correspondente à versão de currículo selecionada.

Os formatos disponíveis no backend são:

| Formato | Extensão | Finalidade |
|---|---|---|
| PDF | `.pdf` | Compartilhar uma versão final do currículo |
| DOCX | `.docx` | Abrir e editar o documento em aplicativos compatíveis |

O PDF é recomendado para envio a empresas e processos seletivos quando se deseja preservar a apresentação.

O DOCX é recomendado quando o estudante precisa realizar ajustes adicionais em um editor de texto.

## 9. Como exportar o currículo

O fluxo previsto para o estudante é:

1. Acessar o sistema com sua conta.
2. Localizar as versões de currículo disponíveis.
3. Selecionar a versão desejada.
4. Conferir as informações e o modelo na prévia.
5. Escolher o formato PDF ou DOCX.
6. Solicitar a geração do arquivo.
7. Salvar o documento disponibilizado pelo navegador.
8. Abrir o arquivo para conferir seu conteúdo.

A disponibilidade dos controles e seus nomes definitivos depende da integração da funcionalidade às telas da aplicação.

As rotas de download já estão implementadas no backend, mas sua existência não comprova, isoladamente, que todos os passos estejam disponíveis em uma interface web integrada.

Para orientações específicas sobre cada formato, consulte o [Guia de exportação PDF e DOCX](guia-exportacao-pdf-docx.md).

## 10. Exportação em PDF

O PDF é indicado principalmente para envio de currículos.

Ao gerar esse formato, o estudante deve conferir se:

- o documento abre corretamente;
- os textos estão legíveis;
- as seções estão organizadas;
- não existem informações cortadas;
- todas as páginas estão completas;
- os dados pessoais e profissionais estão corretos.

Depois dessa conferência, o arquivo poderá ser utilizado em processos seletivos.

## 11. Exportação em DOCX

O DOCX pode ser aberto em aplicativos de edição de documentos compatíveis com esse formato.

Ele é útil quando o estudante deseja realizar alterações diretamente no arquivo baixado.

Entretanto, essas alterações não modificam automaticamente as informações cadastradas no Sistema Currículo.

Caso queira que a alteração apareça em futuras exportações, o estudante deve atualizar os dados na própria aplicação.

A apresentação do DOCX também pode variar conforme o aplicativo utilizado para abrir o arquivo.

## 12. Problemas comuns e soluções

Durante o uso do sistema podem ocorrer situações que impeçam a consulta, revisão ou exportação do currículo.

A tabela apresenta orientações para os problemas mais comuns.

| Problema | Possível causa | O que fazer |
|---|---|---|
| Não consegue acessar a conta | Sessão inválida ou expirada | Realizar novamente o login |
| Currículo não aparece | Versão não encontrada ou indisponível | Conferir a versão selecionada |
| Informações estão incorretas | Dados do perfil desatualizados | Corrigir os dados no sistema e conferir novamente |
| Exportação não funciona | Serviço indisponível ou falha na geração | Tentar novamente e comunicar a equipe se persistir |
| PDF não abre corretamente | Download incompleto ou arquivo inválido | Realizar novo download e utilizar leitor compatível |
| DOCX apresenta diferenças visuais | Variações entre editores de documentos | Abrir em aplicativo compatível e conferir a formatação |
| Arquivo baixado não contém a informação desejada | Versão ou itens selecionados incorretos | Revisar a seleção e gerar novamente |
| Busca de vagas não retorna resultados | Nenhuma oportunidade encontrada ou serviço externo indisponível | Conferir os critérios e tentar novamente quando necessário |

## 13. Falhas relacionadas à exportação

### 13.1. Autenticação necessária

A exportação exige que o estudante esteja autenticado.

Se a sessão estiver inválida ou ausente, a solicitação poderá ser recusada.

**Orientação:** entrar novamente na conta e repetir a operação.

### 13.2. Currículo não encontrado

A exportação só pode ser realizada para versões às quais o estudante tem acesso.

Se a versão não existir ou pertencer a outro usuário, a solicitação não será concluída.

**Orientação:** selecionar uma versão pertencente à própria conta.

### 13.3. Falha na geração do arquivo

Caso ocorra um problema interno durante a geração, o sistema poderá apresentar:

> Não foi possível gerar o arquivo. Tente novamente.

**Orientação:** repetir a solicitação. Se a falha continuar, comunicar a equipe responsável.

### 13.4. Exportação indisponível

A exportação poderá estar indisponível quando o serviço responsável pela geração do formato não estiver configurado ou disponível no ambiente.

**Orientação:** tentar novamente após a normalização do serviço.

### 13.5. Download incompleto

Se o arquivo não abrir ou estiver incompleto, o estudante deve verificar se o navegador concluiu o download.

**Orientação:** realizar uma nova exportação e conferir a extensão do arquivo.

## 14. Conferência do documento após o download

Após exportar, recomenda-se realizar uma revisão final.

O estudante deve observar:

1. Se o nome e os contatos estão corretos.
2. Se o currículo corresponde à versão escolhida.
3. Se as informações selecionadas foram incluídas.
4. Se os textos estão completos.
5. Se não existem cortes ou sobreposições visíveis.
6. Se o arquivo abre normalmente.
7. Se o formato corresponde ao solicitado pela empresa.

Essa conferência é importante porque o currículo será utilizado fora do sistema e poderá ser compartilhado com recrutadores e empresas.

## 15. Segurança e privacidade

Os currículos podem conter informações pessoais, acadêmicas e profissionais.

Por isso, recomenda-se:

- compartilhar o documento somente quando necessário;
- verificar o destinatário antes do envio;
- evitar armazenar currículos em computadores compartilhados;
- remover arquivos baixados de dispositivos públicos;
- não utilizar serviços externos desconhecidos para converter documentos que contenham dados pessoais;
- não compartilhar credenciais de acesso ao sistema.

As rotas de exportação exigem autenticação e verificam a propriedade da versão solicitada.

O estudante não pode exportar um currículo de outra pessoa apenas por conhecer seu identificador.

## 16. Informações técnicas de referência

O backend disponibiliza as seguintes operações:

| Formato | Método | Endpoint |
|---|---|---|
| PDF | GET | `/estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/pdf` |
| DOCX | GET | `/estudantes/{usuario_id}/curriculos/{curriculo_id}/exportacao/docx` |

As respostas de sucesso utilizam os tipos de conteúdo correspondentes e disponibilizam o arquivo para download.

Os principais códigos HTTP são:

| Código | Significado |
|---|---|
| `200` | Arquivo gerado e devolvido |
| `401` | Autenticação ausente ou inválida |
| `403` | Acesso não autorizado à identidade solicitada |
| `404` | Versão não encontrada ou indisponível para o estudante |
| `500` | Falha na geração do arquivo |
| `503` | Serviço de exportação não configurado |

Essas informações são destinadas à manutenção da documentação e ao suporte. O estudante não precisa utilizar diretamente os endpoints para seguir o fluxo previsto na interface.

## 17. Estado atual da funcionalidade

As rotas e os casos de uso de exportação PDF e DOCX estão presentes no backend atual.

A aplicação também possui componentes relacionados a cadastro, seleção de informações, modelos e validação de currículo.

Entretanto, ainda é necessário confirmar em ambiente integrado a disponibilidade dos controles de exportação e o funcionamento completo da jornada do estudante.

Por esse motivo, este manual diferencia as capacidades técnicas existentes dos procedimentos previstos para a interface.

A documentação deve ser revisada após a demonstração integrada, utilizando os nomes definitivos das opções disponíveis e os resultados observados.

## 18. Documentação complementar

Para informações mais detalhadas, consulte:

- [Guia de exportação PDF e DOCX](guia-exportacao-pdf-docx.md)
- [Mapeamento da jornada do estudante](mapeamento_jornadas.md)
- [Modelos de currículo](modelos_curriculo.md)
- [Contratos de informações complementares](contratos-informacoes-complementares.md)
- [Prévia do currículo](previa-curriculo.md)

## 19. Rastreabilidade

- **Issue:** #433 — F12.13
- **Issue relacionada:** #386 — F10.4
- **Requisito:** RF09 — Exportação de currículos em PDF e DOCX
- **Casos de uso:** UC07 e UC08
- **WBS:** 1.1.2.4, 1.8.2.1–1.8.2.4
- **Documento atualizado:** `docs/manual-estudante.md`
- **Guia complementar:** `docs/guia-exportacao-pdf-docx.md`

## 20. Conclusão

O Sistema Currículo reúne funcionalidades para organizar as informações do estudante e preparar versões de currículo.

A exportação em PDF e DOCX permite utilizar essas versões em processos seletivos ou em aplicativos de edição de documentos compatíveis.

Este manual orienta a escolha dos formatos, a conferência do conteúdo e a resolução de problemas comuns, respeitando a diferença entre as capacidades já implementadas no backend e as etapas da interface que ainda dependem de validação integrada.
