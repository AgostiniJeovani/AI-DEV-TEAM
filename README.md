# AI-DEV-TEAM

Time de agentes especializados para apoiar projetos de software com descoberta,
requisitos, arquitetura, design, implementação, dados/IA, qualidade, segurança,
operação e documentação.

Este README é o ponto de entrada. Ele não tenta ensinar todos os detalhes de
uma vez: mostra o caminho correto e envia você para o documento certo quando o
assunto ficar específico.

## Comece aqui

### Se você está conhecendo o projeto

Leia somente estas seções deste README:

1. [O que é](#o-que-é);
2. [Como o repositório está organizado](#como-o-repositório-está-organizado);
3. [Como os agentes trabalham](#como-os-agentes-trabalham);
4. [Primeiro uso](#primeiro-uso).

Depois pare de ler este arquivo e siga o documento indicado em **Próximo
passo**. Não é necessário ler o README inteiro em ordem.

### Se você quer configurar o time

Vá diretamente para [`setup/README.md`](setup/README.md). Ele explica a
junction em linguagem simples, executa a automação e mostra como desfazer.

### Se você quer entender os agentes

Leia [`agents/README.md`](agents/README.md) e depois os `.toml` na ordem do
fluxo. Os TOML são a fonte de verdade das instruções de cada agente.

### Se você quer testar

Primeiro execute a validação automatizada descrita em
[`docs/testing.md`](docs/testing.md). Depois faça os smoke tests comportamentais
com os prompts prontos naquele documento.

### Se você quer acompanhar a evolução do sistema

Leia [`docs/NEXT_STEPS.md`](docs/NEXT_STEPS.md). Ele contém o backlog da semana,
a trilha de pesquisa e os critérios para evoluir do catálogo atual para um
primeiro loop de agentes controlado.

## O que é

O AI-DEV-TEAM é um catálogo versionado de agentes especialistas para Codex.
Cada agente possui uma responsabilidade principal, limites explícitos, modo de
autonomia e instruções de handoff.

A proposta é dividir o trabalho sem criar sobreposição desnecessária:

- agentes de descoberta e análise entendem o problema;
- agentes de arquitetura definem decisões e planos;
- agentes de engenharia implementam quando autorizados;
- agentes de QA, revisão e segurança verificam o resultado;
- DevOps e documentação preparam a operação e a continuidade.

Princípios que não devem ser perdidos:

- leitura do contexto antes de agir;
- responsabilidades claras;
- handoffs explícitos;
- anti-overengineering;
- security by design;
- evidência sobre preferência;
- autonomia proporcional ao papel;
- mudanças reversíveis e autorizadas;
- nenhum modelo ou provedor fixado sem necessidade.

## Como o repositório está organizado

```text
AI-DEV-TEAM/
├── README.md                         ← este ponto de entrada
├── AGENTS.md                         ← regras globais do time
├── .gitignore
├── agents/                           ← agentes Codex versionados
├── docs/                             ← fluxo, contratos e testes
├── setup/                            ← tutorial de configuração
├── scripts/                          ← validação e automação Windows
├── skills/                           ← catálogo de skills planejadas
├── tools/                            ← espaço para utilitários/contratos
└── adapters/                         ← integrações futuras com runtimes
```

O que está funcional nesta versão: `agents/`, `docs/`, `setup/` e `scripts/`.

`skills/`, `tools/` e `adapters/` estão preparados e documentados, mas ainda
não possuem implementações concretas. Não confunda uma pasta planejada com uma
capacidade já carregada pelo Codex.

## Como os agentes trabalham

Fluxo recomendado para um projeto novo:

```text
project-configurator
        ↓
requirements-analyst
        ↓
system-analyst
        ↓
system-architect ───────→ security-engineer quando necessário
        ↓
uiux-designer / frontend-engineer / backend-engineer / data-ai-engineer
        ↓
qa-engineer → code-reviewer → devops-engineer → technical-writer
```

Esse fluxo é adaptável. Tarefas pequenas podem pular etapas; mudanças com
autenticação, dados pessoais, pagamentos, IA, migrações, infraestrutura crítica
ou exposição pública devem envolver as revisões adequadas.

### Catálogo rápido

| Agente | Papel | Modo |
|---|---|---|
| `project-configurator` | Mapeia projeto, stack, comandos e regras locais | read-only |
| `requirements-analyst` | Define requisitos e critérios de aceite | read-only |
| `system-analyst` | Modela domínio, fluxos, estados e contratos | read-only |
| `system-architect` | Define arquitetura, decisões e plano incremental | read-only |
| `uiux-designer` | Define jornadas, interface e acessibilidade | read-only |
| `frontend-engineer` | Implementa interfaces React/Next/TypeScript/Tailwind | escrita autorizada |
| `backend-engineer` | Implementa APIs, domínio, persistência e integrações | escrita autorizada |
| `data-ai-engineer` | Implementa dados, RAG, LLMs e avaliação de IA | escrita autorizada |
| `qa-engineer` | Define e executa estratégia de qualidade | read-only |
| `code-reviewer` | Revisa bugs, riscos e manutenção | read-only |
| `security-engineer` | Analisa ameaças, controles, privacidade e abuso | read-only |
| `devops-engineer` | Cuida de entrega, operação, observabilidade e rollback | escrita autorizada |
| `technical-writer` | Mantém setup, decisões e documentação úteis | escrita autorizada |

Os detalhes, limites e instruções de cada agente estão nos arquivos `.toml` da
pasta `agents/`. `system-architect` não implementa: ele entrega
decisões, especificações e handoffs.

## Primeiro uso

### 1. Configurar

Na raiz do repositório, execute:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-windows.ps1
```

O script conecta:

```text
%USERPROFILE%\.codex\agents
        → <raiz-do-repositório>\agents
```

Isso é uma junction: o Codex acessa o caminho global, mas os arquivos continuam
vivendo e sendo versionados neste repositório. A explicação para iniciantes,
saída esperada, remoção e problemas comuns estão em
[`setup/README.md`](setup/README.md).

### 2. Validar

```powershell
python .\scripts\validate-agents.py
```

Resultado esperado:

```text
agent_count=13
missing_required=0
unsupported_fields=0
architect_read_only=True
documentation_complete=True
validation=passed
```

Se a validação falhar, corrija o problema antes de testar o comportamento dos
agentes. O script não publica, não instala dependências e não acessa segredos.

### 3. Fazer o primeiro smoke test

Abra a pasta do AI-DEV-TEAM no Codex e peça:

```text
Use o agente project-configurator para mapear este repositório.
Não altere nenhum arquivo. Retorne estrutura, stack, comandos de validação,
riscos e um handoff para requirements-analyst.
```

O resultado esperado é uma análise com evidências, sem alterações, seguida de
um handoff claro.

Depois teste o arquiteto:

```text
Use system-architect para analisar uma pequena funcionalidade hipotética.
Produza requisitos assumidos, alternativas, arquitetura, riscos, segurança,
plano incremental e handoff. Não crie nem altere arquivos.
```

O resultado esperado é planejamento, não implementação.

Para o roteiro completo, incluindo teste de implementadores, QA, revisão e
limites de segurança, siga [`docs/testing.md`](docs/testing.md).

## Handoffs

Handoff é a passagem formal de um resultado para o próximo responsável. Ele não
é uma responsabilidade adicional do agente.

O formato mínimo é:

```text
HANDOFF
De: <agente>
Para: <agente ou usuário>
Objetivo: <resultado esperado>
Contexto: <o que foi analisado>
Decisões: <decisões e justificativas>
Artefatos: <arquivos, links ou evidências>
Pendências: <questões em aberto>
Riscos: <riscos e mitigação>
Próximo passo: <ação concreta e responsável>
```

O fluxo detalhado e os casos condicionais estão em
[`docs/workflow.md`](docs/workflow.md) e
[`docs/handoff-protocol.md`](docs/handoff-protocol.md).

## Skills, tools e adapters

### Skills

Skills são capacidades reutilizáveis, diferentes da identidade dos agentes.
Esta primeira versão ainda não possui skills concretas com `SKILL.md`; o
catálogo planejado está em [`skills/README.md`](skills/README.md).

Quando uma skill for criada, ela deve explicar quando usar, pré-requisitos,
procedimento, validação e limites.

### Tools

`tools/` será usado para contratos e utilitários compartilhados. Toda ferramenta
deve documentar permissões, entradas, saídas e riscos.

### Adapters

`adapters/` será usado para integrações futuras com Claude Code, Hermes ou outros
runtimes. Um adapter não pode mudar responsabilidades ou limites do agente.

## Manutenção

Ao alterar um agente:

1. edite o TOML em `agents/`;
2. preserve `name` e o papel principal;
3. execute `scripts/validate-agents.py`;
4. atualize o documento afetado, se o fluxo mudou;
5. repita os smoke tests relevantes;
6. revise o diff antes de versionar.

Não edite a cópia vista por meio da junction. Edite sempre a fonte em
`agents/`.

Para entender o formato dos TOML, consulte
[`docs/agent-contract.md`](docs/agent-contract.md). Para criar skills, siga o
README em `skills/` e adicione um `SKILL.md` completo.

## Documentos de referência

Leia somente quando o assunto aparecer:

- [`AGENTS.md`](AGENTS.md) — regras globais que o Codex deve seguir;
- [`setup/README.md`](setup/README.md) — configuração para iniciantes;
- [`agents/README.md`](agents/README.md) — catálogo e ativação dos agentes;
- [`docs/agent-contract.md`](docs/agent-contract.md) — schema e revisão de TOML;
- [`docs/workflow.md`](docs/workflow.md) — ciclo de trabalho e responsabilidades;
- [`docs/handoff-protocol.md`](docs/handoff-protocol.md) — formato de handoff;
- [`docs/testing.md`](docs/testing.md) — validação e testes comportamentais;
- [`scripts/README.md`](scripts/README.md) — automações disponíveis.

O formato de agentes standalone e os diretórios suportados podem evoluir; para
referência atual, consulte a [documentação oficial de
Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
