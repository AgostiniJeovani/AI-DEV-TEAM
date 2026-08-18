# Protocolo de handoff

O handoff é o contrato entre agentes. Ele reduz repetição, torna decisões auditáveis e deixa claro o que ainda precisa de julgamento humano.

## Formato

```text
HANDOFF
De: <agente>
Para: <agente ou usuário>
Objetivo: <resultado esperado>
Contexto: <repositório, requisitos e evidências analisados>
Decisões: <decisões tomadas e justificativas>
Artefatos: <arquivos, diagramas, testes ou links>
Pendências: <questões abertas e informação faltante>
Riscos: <risco, impacto e mitigação>
Próximo passo: <ação concreta, responsável e condição de término>
```

## Regras

- Fatos observados e inferências devem ser separados.
- O próximo agente deve conseguir começar sem repetir toda a investigação.
- Decisões irreversíveis, riscos altos e ações externas devem ser destacados.
- Um handoff não é aprovação automática: o destinatário ainda valida o próprio escopo.

