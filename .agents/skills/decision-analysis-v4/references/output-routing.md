# Protocolo de roteamento de saída

O destino é uma decisão auditável da análise.

## Descoberta

1. Resolva `prompts` a partir da raiz do projeto e confirme que permanece no workspace.
2. Liste suas subpastas imediatas existentes; não use lista codificada como inventário real.
3. Para candidatas plausíveis, examine nome, instruções aplicáveis e uma amostra mínima das convenções locais quando necessário.

## Critérios, em ordem

1. destino determinado por instrução aplicável;
2. continuidade da linhagem;
3. propósito principal da análise;
4. classificação do problema;
5. função dos artefatos principais analisados;
6. convenções locais;
7. maior especificidade semântica.

Nomes como `requisitos`, `backend`, `frontend`, `revisao` e `templates` são pistas, não inventário fixo. Arquivos `stylesheet` ou `markup` favorecem `frontend`; código servidor, domínio, dados ou integrações favorecem `backend`; documentação de necessidades favorece `requisitos`. Contudo, o propósito da análise prevalece sobre a extensão.

Não escolha `templates` apenas por analisar um prompt nem `revisao` apenas por `lineage.mode: revision`.

## Revisões e ausência de destino

- Revisão comum permanece na pasta anterior.
- Mude somente por alteração material de propósito ou escopo e registre no delta.
- Em empate, escolha a melhor candidata, use `confidence: low` e registre alternativas.
- Se nenhuma pasta for defensável, não crie pasta nem grave na raiz: solicite destino.

## Registro e mensagem

```yaml
routing:
  root: prompts
  selected_directory: prompts/<pasta>
  considered_directories: [prompts/<a>, prompts/<b>]
  confidence: high | medium | low
  rationale: "justificativa curta"
```

Termine a resposta exatamente com:

`Arquivo criado em <caminho>. Avalie se o local escolhido é de fato o mais adequado.`
