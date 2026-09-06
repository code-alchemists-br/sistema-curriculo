# Protocolo de implementação de testes

Use somente após o gate resultar em `valid`.

## Delimitar

1. Mapeie cada critério elegível a cenário, nível, dados, oráculo e arquivo de teste.
2. Liste unitários, mudanças de produto e operações externas como handoffs antes de escrever.
3. Identifique runner, convenções, helpers e isolamento já usados pelo projeto.
4. Escolha o menor conjunto de testes que cubra os riscos aprovados sem duplicação entre níveis.
5. Confirme o `AGENTS.md` mais específico antes de editar cada caminho.

## Implementar

- Teste interfaces e resultados observáveis, evitando acoplamento desnecessário a detalhes internos.
- Use dados sintéticos, nomes neutros e credenciais próprias de teste.
- Torne setup, isolamento e cleanup explícitos; não dependa da ordem dos testes.
- Reutilize fixtures e harnesses existentes antes de criar novos.
- Para dependências externas, use ambiente de teste autorizado, emulator, container descartável, stub ou contrato conforme a finalidade do teste.
- Mantenha thresholds, workloads e matrizes exatamente como aprovados.
- Não enfraqueça asserções para obter verde e não transforme falha legítima em retry do teste.
- Não edite o produto. Se faltar testabilidade, contrato ou comportamento, pare a parte afetada e registre evidência.

## Testes não funcionais

- Separe aquecimento, medição e cleanup quando isso afetar o resultado.
- Registre unidade, percentil, duração, concorrência e ambiente usados, conforme a análise.
- Controle variáveis externas e evite comparar números de ambientes incompatíveis.
- Em segurança, resiliência ou chaos, limite ações ao cenário e alvo autorizados.
- Trate flutuação técnica com método de medição aprovado, não com tolerâncias inventadas.

## Executar e verificar

Comece pela menor execução segura que valide descoberta e sintaxe; depois execute o cenário aprovado. Não rode carga, stress, fault injection ou scanner ativo sem alvo explicitamente seguro.

Quando houver falha:

- confirme que o teste falhou pelo comportamento pretendido, e não por setup defeituoso;
- corrija somente o artefato de teste quando o defeito estiver nele;
- quando a evidência apontar para o produto, não o altere; reporte o defeito e o comando para reprodução.

Inspecione o diff e confirme:

- todos os arquivos alterados pertencem à suíte ou são dependências/configurações exclusivamente de teste aprovadas;
- nenhum código produtivo, CI, deploy ou infraestrutura compartilhada foi alterado;
- nenhum teste unitário isolado entrou no escopo;
- outputs temporários e relatórios não foram versionados indevidamente;
- mudanças preexistentes foram preservadas;
- execuções e resultados relatados correspondem ao que realmente ocorreu.

## Relatar

Informe:

1. análise e versão aplicadas;
2. evidências do veredito `valid`;
3. níveis, cenários e atributos cobertos;
4. artefatos alterados, dados e harnesses usados;
5. comandos executados, ambiente, resultados e limiares;
6. defeitos do produto encontrados sem correção;
7. instruções adicionais e handoffs.

Diferencie claramente teste aprovado, teste vermelho esperado, teste não executado e teste bloqueado.
