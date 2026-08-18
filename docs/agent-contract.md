# Contrato dos agentes

## Schema TOML do Codex

Cada agente standalone deve ter os três campos obrigatórios:

```toml
name = "nome-do-agente"
description = "Quando e por que usar este agente."
sandbox_mode = "read-only"

developer_instructions = """
Instruções completas do agente.
"""
```

O `sandbox_mode` é opcional no schema, mas este repositório o define para tornar
a autonomia explícita. Os valores usados aqui são `read-only` para análise,
arquitetura, segurança, QA e revisão; e `workspace-write` para implementação
autorizada de código, operação ou documentação.

Não usamos `model` nem `model_reasoning_effort` nesta primeira versão. Assim, a
configuração do ambiente pode resolver o modelo disponível sem quebrar o
catálogo por indisponibilidade.

## Onde ficam os conceitos do time

O schema do Codex não possui campos nativos para `role`, `responsibilities`,
`handoff_targets` ou `non_responsibilities`. Esses conceitos ficam descritos
dentro de `developer_instructions`, em linguagem que o agente consegue seguir.

O campo `description` deve permanecer curto e servir como orientação de seleção.
As instruções devem explicar propósito, responsabilidades, limites, autonomia,
saídas esperadas e handoffs.

## Checklist de revisão

Ao criar ou revisar um agente, pergunte:

1. Qual decisão ou trabalho ele torna melhor?
2. Qual é o limite que evita sobreposição?
3. O que ele precisa ler antes de agir?
4. Ele pode escrever? Se sim, o pedido precisa autorizar a mudança?
5. Como o usuário verifica o resultado?
6. Que agente recebe a saída?
7. O arquivo passa em `scripts/validate-agents.py`?
