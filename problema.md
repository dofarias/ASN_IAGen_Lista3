# Problema Criação de uma skill para análise de dados

## Contexto

Uma pessoa precisa explorar dados e responder perguntas para apoiar decisões, mas não quer escrever manualmente uma nova análise a cada solicitação. Os dados podem estar em arquivos ou em outra fonte autorizada, e a interpretação correta depende do significado dos campos, das regras do domínio e das relações entre as informações.

Queremos criar uma skill que ajude um agente de IA a atuar como copiloto de analytics. A pessoa fará perguntas em linguagem natural, e o agente utilizará um procedimento consistente para compreender o pedido, consultar os dados, executar o código necessário e apresentar uma resposta verificável.

## Objetivo

Criar uma skill reutilizável para analisar os dados fornecidos pelo usuário, adaptada ao seu contexto e às ferramentas disponíveis. O agente deve conseguir transformar uma pergunta em uma análise executada, explicar o resultado e continuar a investigação a partir de novos pedidos.

O caso de uso específico será definido no brainstorm. Não há uma base, um conjunto de indicadores ou uma linguagem de programação fixados neste arquivo.

## Como esperamos utilizar

1. O usuário informa a fonte dos dados e descreve o que deseja investigar.
2. O agente identifica a estrutura disponível e consulta as regras relevantes.
3. Quando uma dúvida mudar o significado do cálculo, o agente pergunta antes de prosseguir ou aplica um padrão previamente acordado, informando qual foi utilizado.
4. O agente prepara ou reutiliza código adequado, executa a análise no ambiente autorizado e confere o resultado.
5. O usuário recebe a resposta com os filtros, as definições, as evidências e as limitações necessárias para compreendê-la.
6. O usuário pode pedir uma continuação, como alterar o período, comparar grupos ou detalhar uma categoria. O agente ajusta a análise e executa novamente o que for necessário.

## Comportamentos esperados

- Localizar a fonte informada e verificar quais arquivos, tabelas ou campos realmente existem.
- Compreender o que cada registro representa e quais relacionamentos podem ser utilizados.
- Traduzir a pergunta em métricas, filtros e agregações explícitas.
- Consultar os dados por meio de código, usando as ferramentas disponíveis e adequadas à tarefa.
- Evitar contagens ou valores duplicados ao relacionar informações.
- Identificar entradas ausentes, resultados vazios e limitações que afetem a interpretação.
- Produzir tabelas ou gráficos quando ajudarem a responder à pergunta.
- Informar o código executado ou seu caminho, a forma de execução e a saída relevante.
- Apresentar números como calculados somente quando houver execução que os sustente.
- Explicar quando uma pergunta não puder ser respondida com os dados disponíveis.
- Preservar os dados originais e separar os arquivos produzidos pela análise.

## O que precisa ser definido na conversa

- Quem utilizará o copiloto e quais decisões pretende apoiar.
- Quais dados estão disponíveis, onde ficam e como o agente pode acessá-los.
- Quais perguntas a primeira versão precisa atender.
- Como definir as métricas, as regras de negócio e os relacionamentos relevantes.
- Quais ferramentas, linguagem e dependências serão utilizadas.
- Como informar caminhos e filtros sem depender da máquina do autor.
- Qual será o formato da resposta e onde salvar eventuais saídas.
- Quais limites de atuação são necessários para esse caso de uso.
- Quais exemplos pequenos permitem conferir os cálculos e o comportamento da skill.

Não transforme essas decisões pendentes em fatos presumidos. Use o dicionário, os dados e as respostas do usuário para resolvê-las.

## Resultado da criação

Uma pasta de skill com `SKILL.md` preenchido para o caso de uso e os recursos que seu funcionamento exigir. Regras e documentação podem ficar em `references/`; código reutilizável pode ficar em `scripts/`.

A skill deve registrar como receber um pedido, executar a análise, verificar o resultado e responder. As ferramentas e permissões do ambiente é que permitem ler os dados e executar o código.

## Como reconhecer uma entrega útil

Outra pessoa consegue configurar o acesso aos dados, ativar a skill, fazer uma pergunta e conferir a resposta produzida. As verificações devem incluir uma análise com resultado conhecido, uma mudança no pedido, uma situação sem dados e uma pergunta que não possa ser respondida pela fonte disponível.

Use `brainstorm.md` para conduzir a conversa e `SKILL.md` como modelo de autoria. Preserve esses modelos e crie a versão adaptada na pasta do projeto escolhido.
