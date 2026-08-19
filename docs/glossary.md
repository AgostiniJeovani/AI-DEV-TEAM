# Glossary — English Terms Explained in Portuguese

This project uses English as its canonical language. This glossary explains
the terms that appear most often so the repository is also a learning guide.

| English term | Explicação em português |
|---|---|
| Agent | Agente: especialista que recebe uma tarefa, contexto, ferramentas e limites. |
| Agent loop | Loop do agente: ciclo de entender, agir, observar, verificar e decidir se continua ou para. |
| Adapter | Adaptador: camada que traduz o contrato do projeto para Codex, Claude, Hermes ou outro runtime. |
| Acceptance criteria | Critérios de aceite: condições observáveis que precisam ser verdadeiras para considerar o trabalho aprovado. |
| Artifact | Artefato: resultado concreto produzido pelo trabalho, como código, documento, plano, teste ou relatório. |
| Backlog | Lista priorizada de melhorias ou tarefas ainda não concluídas. |
| Blocked | Bloqueado: o trabalho não pode continuar sem uma decisão, permissão, informação ou mudança externa. |
| Budget | Orçamento: limite de chamadas, tokens, tempo, tentativas, subagentes ou dinheiro/ créditos. |
| Checkpoint | Ponto de salvamento: estado persistido para permitir retomada depois de uma pausa ou falha. |
| Checker | Verificador: agente ou processo que avalia o resultado produzido por outro agente. |
| Context | Contexto: informações disponíveis para o agente em uma execução, incluindo instruções, arquivos, ferramentas e histórico relevante. |
| Context engineering | Engenharia de contexto: seleção e manutenção do conjunto correto de informações para cada etapa. |
| Contract | Contrato: formato combinado de entradas, saídas, responsabilidades, critérios e limites. |
| Developer instructions | Instruções do desenvolvedor: regras principais que definem como o agente deve trabalhar. |
| Evidence | Evidência: arquivo, comando, teste, log, referência ou observação que sustenta uma afirmação. |
| Evaluator | Avaliador: componente que compara um resultado com critérios definidos. |
| Evaluator-optimizer | Padrão em que um agente produz, outro avalia e o primeiro revisa com base no feedback. |
| Fail closed | Falhar fechado: quando algo dá errado, o sistema bloqueia a ação em vez de liberar por segurança. |
| Handoff | Passagem formal de resultado, contexto e próximo passo para outro agente ou pessoa. |
| Harness | Harness: ambiente de execução ao redor do modelo, incluindo ferramentas, permissões, estado, validações e recuperação. |
| Harness engineering | Engenharia do harness: projetar esse ambiente para tornar o comportamento legível, verificável e seguro. |
| Human-in-the-loop | Pessoa no loop: a execução pausa e exige aprovação humana antes de uma ação sensível. |
| Invariant | Invariante: regra que deve permanecer verdadeira durante toda a execução. |
| Maker | Produtor: agente que cria o artefato inicial ou propõe uma mudança. |
| Needs review | Precisa de revisão: o resultado não deve ser aceito automaticamente; requer análise de pessoa ou agente autorizado. |
| Non-functional requirement | Requisito não funcional: qualidade ou restrição como segurança, performance, acessibilidade, custo ou disponibilidade. |
| Observability | Observabilidade: capacidade de entender o que aconteceu usando logs, métricas, traces e evidências. |
| Over-engineering | Overengineering: complexidade maior do que o problema exige. |
| Prompt injection | Injeção de prompt: conteúdo malicioso ou conflitante que tenta fazer o agente ignorar suas regras. |
| Read-only | Somente leitura: pode inspecionar e produzir análise, mas não alterar arquivos. |
| Retry | Nova tentativa: repetição controlada após uma falha considerada recuperável. |
| Rollback | Reversão: retorno a uma versão ou estado anterior quando uma mudança causa problema. |
| Scope | Escopo: limites do que está incluído e excluído na tarefa. |
| Security by design | Segurança desde o desenho: segurança considerada na arquitetura e nos fluxos, não apenas no final. |
| State | Estado: situação atual da tarefa, como `in_progress`, `blocked` ou `completed`. |
| Terminal state | Estado terminal: resultado final que encerra uma tarefa, como `completed`, `failed` ou `timed_out`. |
| Trace | Trace: registro da execução, incluindo decisões, chamadas de modelo, ferramentas, handoffs e resultados. |
| Workspace-write | Escrita autorizada no workspace: o agente pode alterar arquivos dentro do escopo permitido. |

## The shortest mental model

```text
prompt       = what the agent is told
context      = what the agent can see
harness      = what controls the execution
loop         = how the work repeats or stops
handoff      = how work moves to the next owner
evaluation   = how we know it worked
budget       = how much it is allowed to consume
```
