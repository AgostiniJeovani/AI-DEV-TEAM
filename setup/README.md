# Configuração do AI-DEV-TEAM

Este guia é para quem está configurando o projeto pela primeira vez.

## O que vamos fazer

Os agentes ficam versionados em `agents/` dentro deste repositório. O Codex
procura agentes globais em uma pasta própria do usuário. A automação cria uma
**junction**, que é como uma ponte de pasta:

```text
%USERPROFILE%\.codex\agents
        → pasta agents/ deste repositório
```

O Codex acessa a ponte, mas os arquivos continuam em um único lugar: o
repositório. Assim não precisamos manter duas cópias sincronizadas.

## Antes de começar

Você precisa de:

- Windows;
- Codex instalado e funcionando;
- este repositório salvo localmente;
- Python 3.11 ou mais recente para o validador.

Não coloque senhas, tokens ou arquivos `.env` neste repositório.

## Configuração em três passos

### Passo 1 — abra o terminal na raiz

Abra o PowerShell na pasta onde está este README. Se preferir, use:

```powershell
cd <raiz-do-repositório>
```

### Passo 2 — execute a automação

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-windows.ps1
```

O script verifica a pasta dos agentes, cria a ponte se ela ainda não existir e
confirma que ela aponta para este repositório. Ele não substitui uma pasta real
nem uma ponte que aponte para outro lugar.

Se tudo estiver certo, você verá uma mensagem semelhante a:

```text
Junction já configurada: ...\.codex\agents -> ...\agents
validation=passed
```

Rodar o comando novamente é seguro; ele não recria uma ponte válida.

### Passo 3 — valide os arquivos

```powershell
python .\scripts\validate-agents.py
```

Procure no final:

```text
agent_count=13
missing_required=0
unsupported_fields=0
architect_read_only=True
documentation_complete=True
validation=passed
```

Se aparecer `validation=failed`, leia as linhas `ERROR` e corrija o arquivo
indicado antes de abrir o Codex.

## Como confirmar visualmente

No Explorer, abra `%USERPROFILE%\.codex\agents`. A pasta deve aparecer como
uma junction/atalho de sistema e conter os mesmos `.toml` que estão em
`agents/` neste repositório.

Para uma confirmação técnica sem alterar nada:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-windows.ps1 -CheckOnly
```

## Como desfazer

Se quiser parar de disponibilizar o catálogo globalmente, remova apenas a
junction:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\remove-junction-windows.ps1
```

Os arquivos dentro do repositório não são apagados. O script recusa remover
uma pasta real ou uma junction apontando para outro lugar.

## Problemas comuns

### “Python não foi encontrado”

Instale Python 3.11+ ou execute apenas a verificação da junction com
`-SkipValidation`. O validador continuará pendente até Python estar disponível.

### “O destino já existe e não é uma junction”

O script parou para não apagar uma pasta real. Verifique o conteúdo e faça
backup antes de decidir manualmente o que fazer. Não apague nada só para forçar
o script.

### “A junction aponta para outro lugar”

Existe uma configuração anterior. Não use `Remove-Item` diretamente. Confirme
o destino e use o script de remoção somente se aquela junction for realmente
do AI-DEV-TEAM.

### O Codex não mostra os agentes

1. execute o validador;
2. execute `setup-windows.ps1 -CheckOnly`;
3. confirme que abriu o repositório correto no Codex;
4. reinicie a sessão do Codex se ela já estava aberta antes da configuração;
5. verifique se os arquivos estão em `agents/` e terminam em `.toml`.

Depois da configuração, volte ao README da raiz e siga a seção **Primeiro
uso**.

