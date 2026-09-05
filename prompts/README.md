# Prompts do processo de desenvolvimento

Esta pasta mantém os prompts estruturados e versionados utilizados pela equipe
durante o processo de desenvolvimento. Seu conteúdo auxilia análise, geração,
revisão e documentação, mas não faz parte dos recursos carregados pela aplicação
em tempo de execução.

## Organização

- `backend/` — prompts relacionados ao desenvolvimento e à revisão do backend.
- `frontend/` — prompts relacionados ao desenvolvimento e à revisão do frontend.
- `requisitos/` — prompts para levantamento, análise e refinamento de requisitos.
- `revisao/` — prompts para revisão de código, arquitetura e documentação.
- `templates/` — modelos reutilizáveis para a criação de novos prompts.

## Estrutura de um prompt

Cada prompt DEVE ser armazenado em Markdown e explicar, quando aplicável:

- objetivo e contexto de uso;
- entradas e variáveis esperadas, usando a forma `{{nome_da_variavel}}`;
- instruções e restrições;
- formato esperado da resposta;
- exemplos de entrada e saída;
- modelo, ferramenta ou capacidade necessária;
- dados que NÃO DEVEM ser enviados;
- versão ou histórico de mudanças relevantes.

Os nomes dos arquivos DEVEM descrever sua finalidade e utilizar letras
minúsculas separadas por hífen, por exemplo `revisar-caso-de-uso.md`.

## Limite de escopo

Prompts usados apenas no processo de desenvolvimento DEVEM permanecer nesta
pasta. Prompts que venham a ser carregados pela aplicação em produção DEVEM
ficar próximos ao módulo consumidor em `src/` e seguir as regras arquiteturais
daquela área.
