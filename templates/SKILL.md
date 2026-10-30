---
name: nome-da-skill
description: "[Descreva a tarefa específica que esta skill realiza e as situações em que deve ser usada.]"
---

# [Nome da skill]

<!-- MODELO PARA ADAPTAR: substitua os campos entre colchetes e remova comentários e seções opcionais sem utilidade. O nome no YAML deve corresponder ao nome da pasta da skill. Este arquivo é um modelo de autoria; copiá-lo para templates/ não instala uma skill. -->

## 1. Tarefa e resultado esperado

Realize [tarefa delimitada] para [usuário ou contexto], produzindo [resultado observável].

- **Objetivo:** [Que necessidade a tarefa atende.]
- **Incluído:** [Quais operações fazem parte da primeira versão.]
- **Fora do escopo:** [Limites que ajudam a evitar interpretações erradas, se necessários.]

## 2. Quando usar

Use esta skill quando [condição específica de uso relacionada à tarefa].

[Se houver tarefas muito parecidas, explique a distinção necessária para escolher esta skill corretamente. Evite descrever a skill como solução para qualquer pedido.]

## 3. Entradas

| Entrada | Formato ou origem | Obrigatória | Como usar ou validar |
| --- | --- | --- | --- |
| [Entrada principal] | [Texto, arquivo, parâmetro, serviço ou outro formato] | [Sim ou não] | [Regra de validação] |
| [Entrada adicional, se necessária] | [Formato ou origem] | [Sim ou não] | [Regra ou valor padrão explicitamente acordado] |

Quando faltar uma entrada que altere o resultado, [pergunta ou ação necessária]. Para uma entrada inválida, [como explicar o problema ou prosseguir sem comprometer o resultado].

## 4. Saída

- **Entrega:** [Conteúdo que deve ser apresentado ou produzido.]
- **Formato:** [Texto, arquivo, tabela, imagem, alteração de código ou outro.]
- **Destino:** [Local ou forma de definir o destino com o usuário, se houver arquivo.]
- **Evidências:** [O que permite conferir a tarefa: cálculo, trecho, referência, execução ou inspeção adequada.]

[Defina unidades, nomes, estrutura ou convenções de saída apenas quando importarem para quem recebe a entrega.]

## 5. Regras específicas da tarefa

1. [Regra do domínio que muda como o agente deve executar a tarefa.]
2. [Restrição ou convenção necessária para interpretar entradas ou produzir a saída.]
3. [Tratamento de uma exceção relevante, se houver.]

[Para regras extensas, mantenha aqui somente a orientação de consulta e use uma referência relativa real. Não duplique a mesma regra em vários arquivos.]

## 6. Procedimento

### Compreender o pedido

1. Identifique [objetivo, parâmetros e informações relevantes do pedido].
2. Confira as entradas e consulte [documentos ou referências necessários].
3. Resolva ambiguidades que mudem o resultado. Use [padrão acordado], quando aplicável, e informe sua utilização.

### Executar a tarefa

4. [Ação concreta necessária para produzir o resultado.]
5. [Próxima ação ou decisão relevante.]
6. [Como utilizar uma ferramenta, um script ou um recurso, se a tarefa precisar deles. Caso contrário, remova esta etapa.]

### Conferir o resultado

7. Compare [parte verificável da saída] com [critério, exemplo conhecido ou fonte de referência].
8. Confira [outro aspecto relevante para a qualidade desta tarefa].
9. Se houver divergência, identifique a causa e [ação de correção]. Repita a verificação afetada. Quando não for possível resolver, relate o impedimento e o que ficou sem verificar.

### Entregar

10. Apresente [resultado e explicação necessária ao usuário] no formato definido.
11. Informe [decisões, limitações ou pendências que afetem o uso da entrega].

## 7. Recursos de apoio

<!-- Se a skill não precisar de recursos adicionais, remova esta seção. Crie apenas os arquivos necessários e substitua os caminhos abaixo pelos reais. -->

- **Referências:** [Link relativo para regras ou documentação] — consultar quando [condição].
- **Scripts:** [Caminho relativo de código reutilizável] — executar quando [necessidade concreta].
- **Assets:** [Caminho de modelo ou arquivo usado na entrega] — utilizar em [parte da tarefa].

Resolva caminhos dos recursos a partir da pasta da skill. [Se entradas ou saídas estiverem fora dessa pasta, explique como informar seus caminhos sem depender da máquina do autor.]

## 8. Ambiente e ferramentas

<!-- Remova o que não se aplicar. Uma skill pode funcionar somente com instruções e ferramentas já disponíveis. Não é obrigatório ter código, Python, MCP ou uma API. -->

- **Ferramentas necessárias:** [Capacidades realmente exigidas pela tarefa.]
- **Dependências:** [Programas, bibliotecas ou serviços, quando necessários.]
- **Execução:** [Comando ou forma de uso, com entradas e parâmetros explicados.]
- **Se o recurso não estiver disponível:** [Como informar o impedimento ou usar uma alternativa adequada e autorizada.]

Não descreva uma operação como executada quando ela tiver sido apenas proposta. [Se houver cálculo ou execução, especifique as evidências que o usuário deve receber.]

## 9. Limites de atuação

- **Preservar:** [Arquivos, conteúdo ou decisões que esta tarefa precisa manter.]
- **Alterações previstas:** [O que a execução desta tarefa pode modificar dentro do pedido recebido.]
- **Decisões a esclarecer:** [Dúvidas que precisam de resposta antes de uma ação relevante.]

[Inclua apenas limites concretos da tarefa. O texto da skill não substitui permissões do ambiente nem amplia o pedido do usuário. Se o projeto tiver AGENTS.md, consulte as regras gerais aplicáveis, evitando cópias desnecessárias.]

## 10. Critérios de conclusão

Considere a tarefa concluída quando:

- [Critério observável sobre o conteúdo ou comportamento da entrega.]
- [Verificação relevante realizada e seu resultado conferido.]
- [Arquivo ou resposta produzido no formato e destino esperados.]

Se um critério não puder ser verificado, informe essa limitação sem apresentá-lo como atendido.

## 11. Exemplos de uso

### Pedido pertinente

> [Pedido realista em que a skill deve ser utilizada, com entradas suficientes.]

**Resultado esperado:** [Características observáveis da resposta ou do arquivo produzido.]

### Entrada ausente ou inválida

> [Pedido que permita conferir o tratamento de uma falha relevante.]

**Comportamento esperado:** [Pergunta, mensagem ou decisão adequada à situação.]

### Pedido fora do escopo

> [Pedido próximo, mas que não precisa desta skill.]

**Comportamento esperado:** [Como reconhecer que o procedimento desta skill não se aplica.]

<!-- Revise o tamanho final: exemplos extensos e conjuntos de testes podem ficar em arquivos de apoio, se necessário. A versão final deve conter o que ajuda outro agente a executar a tarefa específica, sem carregar todo este roteiro de preenchimento. -->
