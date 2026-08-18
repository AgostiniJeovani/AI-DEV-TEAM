# Agentes

Os arquivos desta pasta são agentes customizados compatíveis com o formato standalone do Codex. Cada arquivo contém apenas campos suportados pelo schema: `name`, `description`, `developer_instructions` e, quando necessário, `sandbox_mode`.

Para usar este catálogo no Codex, a configuração recomendada para este
repositório é uma junction global:

```text
%USERPROFILE%\.codex\agents
    └── junction → <raiz-do-repositório>\agents
```

Assim, o repositório é a única fonte de verdade e o Codex enxerga os agentes
globais sem duplicar os arquivos. O script `scripts/setup-windows.ps1` cria ou
verifica essa junction.

Como alternativa, para um projeto isolado, copie os arquivos para:

- `.codex/agents/` para agentes específicos daquele projeto; ou
- `~/.codex/agents/` para agentes pessoais globais.

O nome do arquivo deve acompanhar o campo `name`. Não fixe `model` ou `model_reasoning_effort` nesta primeira versão; o Codex pode resolver essas configurações conforme disponibilidade e configuração do ambiente.
