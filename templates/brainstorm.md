# Brainstorm para ajudar a criar a skill

## Como usar

Forneça ao agente os três arquivos desta pasta: problema.md, brainstorm.md e SKILL.md. O problema descreve o objetivo inicial; este roteiro conduz a conversa; SKILL.md é o modelo que será adaptado. Informe a pasta do projeto e a fonte dos dados, quando disponíveis.

Pedido sugerido:

> Leia problema.md, brainstorm.md e o template SKILL.md. Ajude-me a criar uma skill para o problema apresentado. Faça perguntas sobre o caso de uso, os dados, as regras, as ferramentas e o resultado esperado. Depois de esclarecer as decisões essenciais, crie a skill adaptada e os recursos necessários no projeto. Comece pela conversa, sem inventar decisões para preencher o modelo.

## Objetivo do agente

Ajude o usuário a transformar o problema descrito em problema.md em uma skill reutilizável. O caso inicial desta pasta é um copiloto para análise de dados. A skill deve explicar quando atuar, quais informações utilizar, como executar o trabalho e como reconhecer uma entrega correta.

O modelo é genérico para permitir a adaptação. A skill final deve ser específica e útil para a tarefa escolhida. Não produza apenas um arquivo com frases como “siga boas práticas” ou “faça corretamente”.

## 1. Preparação

1. Leia problema.md para compreender o objetivo e SKILL.md para conhecer o modelo. Consulte o contexto já fornecido pelo usuário. Use o problema como ponto de partida, sem confundi-lo com uma skill pronta ou com todas as decisões já resolvidas.
2. Consulte as instruções aplicáveis ao projeto e os materiais relevantes, quando disponíveis.
3. Identifique o que já está confirmado, o que pode ser proposto e o que exige uma resposta do usuário.
4. Confira quais ferramentas e recursos existem no ambiente. A skill orienta sua utilização, mas não concede acesso ou instala dependências por si só.
5. Se algum material essencial não estiver acessível, explique o impedimento. Continue as partes da discussão que não dependem dele.

## 2. Como conduzir a conversa

- Use português simples e explique termos técnicos quando necessário.
- Faça de duas a quatro perguntas relacionadas por rodada. Faça apenas uma quando a resposta exigir mais reflexão.
- Use as respostas para escolher o próximo tema. Não envie todo este roteiro como um questionário de uma vez.
- Evite perguntar informações que já estejam claras no pedido ou nos materiais disponíveis.
- Explore alternativas quando houver uma decisão real, explique suas consequências e identifique sua recomendação como proposta.
- Priorize dúvidas que mudam a execução ou a forma de aceitar o resultado.
- Mantenha uma primeira versão pequena que resolva a tarefa. Deixe melhorias futuras fora do escopo atual.
- Apresente sínteses curtas nas transições importantes e dê espaço para correções, sem pedir confirmação para cada detalhe.

## 3. Perguntas iniciais

Comece pelo que ainda não foi informado:

1. Qual tarefa você quer repetir com ajuda da skill e quem vai utilizá-la?
2. Em quais situações ela deve atuar? Dê um exemplo de pedido real.
3. O que você espera receber como resultado e como saberá que está correto?

Se essas respostas já estiverem disponíveis, resuma seu entendimento e pergunte sobre a principal dúvida restante.

## 4. Aprofundamento conforme o caso de uso

### Tarefa e escopo

- Como esse trabalho acontece hoje? Que conhecimento ou procedimento costuma precisar ser explicado novamente?
- O que entra na primeira versão e o que deve ficar para depois?
- Há uma tarefa parecida em que esta skill não deve ser usada?

### Entradas

- Que informações, arquivos ou parâmetros o usuário precisa fornecer?
- Quais entradas são obrigatórias? Há valores padrão já acordados?
- Como reconhecer uma entrada ausente, inválida ou incompatível?
- Onde os materiais ficam e como informar seu caminho ou endereço?

### Regras e conhecimento do domínio

- Quais decisões ou convenções alteram o modo de executar a tarefa?
- Existe um dicionário, manual, padrão ou outra referência relevante?
- Que exceções realmente importam para a primeira entrega?
- Que termos podem ser ambíguos e precisam de uma definição?

Confira as regras nos materiais disponíveis. Não invente requisitos, campos, fórmulas ou decisões para completar o modelo.

### Saída e aceitação

- Qual conteúdo o usuário precisa receber e em qual formato?
- Se houver arquivos, onde salvar e como lidar com uma saída existente?
- Que exemplo pequeno permite comparar o resultado esperado com o obtido?
- Que evidência ajuda a conferir a entrega sem depender apenas da afirmação do agente?

### Execução e ferramentas

- A tarefa pode ser realizada com instruções e ferramentas já disponíveis?
- Alguma operação precisa de código, acesso a arquivos, navegador, API ou outro recurso?
- Se houver código, quais dependências e comandos são necessários? O que já foi executado e conferido?
- Uma etapa repetida se beneficiaria de um script reutilizável?
- Quais limites concretos precisam ser respeitados durante a execução?

Não suponha que toda skill precisa de scripts, Python, MCP, acesso à internet ou serviços externos. Escolha os recursos pela tarefa e pelo ambiente do usuário. Se houver implementação de código, esclareça o processo de trabalho apenas na medida necessária ao projeto e às instruções existentes.

### Verificação do comportamento

- Qual pedido normal deve ativar a skill e produzir um resultado conhecido?
- Qual entrada ausente ou inválida permite conferir o tratamento de um problema?
- Qual pedido fora do escopo permite conferir se a skill está sendo selecionada em excesso?
- Que aspectos do resultado precisam de uma comparação independente ou de revisão humana?

## 5. Síntese antes de adaptar o modelo

Apresente:

- Tarefa, público, condições de uso e limites.
- Entradas, regras e referências confirmadas.
- Saída, destino e critérios de aceitação.
- Procedimento proposto e ferramentas realmente necessárias.
- Casos de teste e resultados esperados.
- Decisões pendentes que afetem a execução.

Pergunte antes de fechar uma parte que dependa de uma informação crítica. As demais podem ser redigidas como rascunho. Identifique hipóteses e propostas sem apresentá-las como decisões confirmadas.

## 6. Criação da skill com apoio do template

Depois de esclarecer as decisões essenciais, produza os arquivos da skill no projeto escolhido. Não se limite a devolver perguntas ou a copiar o modelo com campos em aberto. Se uma parte depender de uma informação crítica ainda ausente, identifique a pendência e avance somente no que não depender dela.

1. Escolha um nome curto em letras minúsculas, números e hífens. Use o mesmo nome no campo name e na pasta da skill.
2. Escreva uma description específica, indicando a tarefa e quando aplicá-la. Esse campo ajuda na seleção da skill.
3. Preencha o corpo com as entradas, regras, passos e critérios discutidos. Inclua apenas detalhes que ajudem o agente a executar a tarefa.
4. Substitua todos os campos entre colchetes e remova os comentários de preenchimento. Não deixe instruções genéricas do template na skill final.
5. Remova seções e linhas que não se aplicam. Um template completo não exige uma skill longa.
6. Coloque documentação extensa em references/, código reutilizável em scripts/ e modelos de saída em assets/, somente quando esses recursos forem necessários.
7. Use referências relativas válidas e explique quando consultar cada recurso. Não crie pastas vazias ou links para arquivos inexistentes.
8. Aproveite recursos e convenções existentes do projeto. Mantenha orientações gerais no AGENTS.md, quando houver, evitando cópias que possam divergir.

## 7. Testes e revisão

Confira separadamente a estrutura do arquivo e o comportamento da skill. Um nome válido e um YAML correto não provam que o procedimento funciona.

No ambiente autorizado, execute os casos pertinentes e compare os resultados com os critérios acordados. Teste seleção explícita e, quando a ferramenta permitir, seleção automática. Inclua um pedido fora do escopo.

Se houver código novo, verifique sua execução e os comportamentos importantes. Se a tarefa não utilizar código, confira os resultados por critérios adequados ao tipo de entrega.

Corrija a causa das falhas e repita as verificações afetadas. Identifique passou, falhou e não verificado. Não relate uma verificação planejada como executada.

## 8. Salvamento e entrega

- Preserve problema.md, brainstorm.md e SKILL.md desta pasta como materiais de autoria. Salve a skill adaptada na pasta do projeto, mantendo o nome obrigatório SKILL.md no pacote final.
- Confira o diretório de descoberta da ferramenta escolhida. Nos exemplos de projeto local da aula, use .agents/skills/nome-da-skill/ no Codex ou .claude/skills/nome-da-skill/ no Claude Code.
- Se o projeto ou o destino não puderem ser inferidos, pergunte antes de salvar.
- Entregue SKILL.md e somente os recursos que sustentam seu funcionamento, com instruções de uso e verificação.
- Informe os arquivos, as decisões, as evidências e as pendências relevantes. Use o fluxo de revisão do repositório quando fizer parte da atividade.

O resultado é uma skill criada para o caso concreto, com os recursos necessários e verificações identificadas, que outra pessoa consegue usar e conferir. Esses arquivos de autoria não precisam ser copiados para a skill instalada, a menos que algum deles tenha uma função concreta no procedimento final.
