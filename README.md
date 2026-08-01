# Git Avançado — Currículo 11

Exercícios práticos, um módulo por commit.

## Módulo 1 — Internals do Git

- Objects: blob (conteúdo), tree (estrutura de pastas), commit (snapshot + metadados)
- Refs (branches) são só arquivos texto apontando pra um hash de commit
- Hash é gerado a partir do CONTEÚDO, não do nome — dois arquivos idênticos
geram o mesmo blob (deduplicação automática)
- Histórico é uma cadeia: cada commit aponta pro seu parent

## Módulo 2 — Rebase interativo

Prática de `git rebase -i` para reescrita de histórico local.

**Comandos praticados:**
- `pick` — mantém o commit
- `reword` — edita a mensagem do commit
- `edit` — pausa o rebase pra alterar conteúdo (`commit --amend`)
- `squash` — funde com o commit anterior, combinando as mensagens
- `fixup` — funde com o commit anterior, descartando a mensagem
- `drop` — remove o commit
- reorder — muda a ordem dos commits reordenando as linhas no editor do rebase

**O que foi feito:**
Criação de commits "sujos" de propósito (wip, typos, testes) e limpeza via fixup + drop. Uso de edit para remover conteúdo indesejado que squash/fixup não apaga sozinho (eles fundem commits, não editam o arquivo). Reorder de commits e squash com edição de mensagem combinada. Resolução manual de conflitos de rebase gerados quando a reordenação ou edição de um commit no meio da cadeia quebra o contexto que os patches seguintes esperavam encontrar.

**Principais aprendizados:**
- Squash/fixup reescrevem o histórico de commits, não o conteúdo do arquivo — é preciso editar manualmente se algo precisa ser removido do código
- Rebase reaplica commits como patches; reordenar ou editar um commit no meio pode gerar conflito mesmo sem incompatibilidade real de conteúdo, porque o contexto do patch mudou
- Qualquer alteração num commit muda seu hash e, em cascata, o hash de todos os commits seguintes (efeito do parent hash)

## Módulo 3: Cherry-pick (com resolução de conflitos)

Praticado `git cherry-pick` para aplicar um commit específico de outra branch sem trazer todo o histórico dela.

**Comandos explorados:**
- `git cherry-pick <hash>` — aplica o diff de um commit específico como novo commit na branch atual
- `git cherry-pick <hash1>..<hash2>` — aplica um intervalo de commits
- `git cherry-pick -n` (`--no-commit`) — aplica as mudanças sem commitar
- `git cherry-pick -x` — registra na mensagem de qual commit a mudança veio
- `git cherry-pick --continue` / `--abort` / `--skip` — controle do processo em caso de conflito

**Resolução de conflito:**
Criadas duas branches (`feature-zero` e `feature-round`) que alteravam a mesma função (`divide`) de formas diferentes — uma tratando divisão por zero, outra arredondando o resultado. Ao dar cherry-pick de `feature-round` dentro de `feature-zero`, o Git parou no conflito por ambas mexerem na mesma linha. Resolvido manualmente combinando as duas mudanças, mantendo o tratamento de zero e o arredondamento juntos.

Fluxo de resolução: editar o arquivo removendo os marcadores (`<<<<<<<`, `=======`, `>>>>>>>`), `git add` no arquivo resolvido, e `git cherry-pick --continue` para finalizar o commit.

**Aprendizado principal:** cherry-pick traz uma mudança pontual de uma branch pra outra sem mergear tudo, mas gera conflito sempre que a mesma região de código foi alterada nos dois lados — a resolução segue o mesmo princípio de qualquer conflito de merge/rebase.

## Módulo 4 — Reflog

### O que é
O reflog (`git reflog`) registra localmente todo movimento das referências (HEAD, branches) — commits, checkouts, resets, rebases, amends. Diferente do `git log`, que mostra só o histórico alcançável por uma branch, o reflog mostra pra onde as referências já apontaram, incluindo commits que ficaram "soltos" (sem nenhuma branch apontando pra eles).

Importante: é local e temporário (não vai no push, expira por padrão em 90 dias os commits alcançáveis e 30 dias os não-alcançáveis).

### Prática 1 — reset --hard e recuperação direta
- 4 commits sequenciais na main (`primeiro` → `quarto`)
- `git reset --hard HEAD~3` simulou a perda dos últimos 3 commits
- `git reflog` mostrou o histórico completo, incluindo os commits "perdidos"
- Recuperado com `git reset --hard HEAD@{1}`, voltando ao estado exato de antes do reset

### Prática 2 — recuperação via branch nova (mais seguro)
- Repetido o `reset --hard HEAD~3`
- Em vez de sobrescrever a main, criada uma branch nova a partir do reflog: `git branch recuperada HEAD@{1}`
- `main` continuou no estado "quebrado", enquanto `recuperada` tinha o histórico completo — permite decidir depois o que fazer, sem mexer no estado atual

### Prática 3 — branch deletada
- Criada `branch-teste`, com um commit
- Deletada com `git branch -D branch-teste`
- O próprio Git mostrou o hash do commit no aviso de deleção (`Deleted branch branch-teste (was <hash>)`) — atalho mais direto que vasculhar o reflog inteiro
- Branch recriada com `git branch branch-teste <hash>`, commit recuperado intacto

### Comandos-chave

git reflog

git reflog show <branch>

git reset –hard HEAD@{n}

git branch <nome> HEAD@{n}

git branch <nome> <hash>

## Módulo 5: Bisect (debugging via histórico)

Praticado dentro da subpasta `modulo5-bisect`, com um projeto de teste (`contador.py`)
contendo funções simples (soma, subtração, multiplicação, divisão, potência, média).

Um bug foi introduzido de propósito em um commit no meio do histórico, disfarçado
de refatoração ("refatora funcao soma para maior clareza"), trocando `a + b` por
`a - b`. Mais commits inocentes foram feitos depois, simulando um bug que passou
despercebido por um tempo.

Criado um teste simples (`assert soma(2, 3) == 5`) pra detectar o problema.

**Busca manual:**
git bisect start

git bisect bad HEAD

git bisect good <primeiro commit>

A cada passo, o Git faz checkout automático de um commit no meio do intervalo
restante (detached HEAD). Rodando o teste e marcando `git bisect good` ou
`git bisect bad`, o commit culpado foi encontrado em 3 passos (busca binária)
em vez de checar os 8 commits um por um.

**Busca automatizada** com `git bisect run <comando>`: o Git roda o comando
sozinho a cada passo, usando o código de saída do processo (0 = good, diferente
de 0 = bad) pra decidir automaticamente. Pegadinha encontrada na prática: o script
de teste e o `__pycache__` precisam ficar fora da influência do checkout, ou o
Python pode ler um arquivo ausente ou bytecode desatualizado durante a troca de
commits, contaminando o resultado.

Bug corrigido depois de identificado, com commit dedicado referenciando o bisect.

#Módulo 6: Stash avançado



Prática de git stash além do uso básico, cobrindo múltiplos stashes, mensagens customizadas, stash parcial (por hunk) e recuperação via branch.



Cenários praticados:



• Stash básico: git stash / git stash pop para guardar e recuperar mudanças temporárias.

• Múltiplos stashes: acumular mais de um stash e recuperar um específico com git stash apply stash@{n}, depois limpar com git stash drop.

• Stash com mensagem: git stash -m "mensagem" para identificar o conteúdo de cada stash na lista.

• Stash parcial: git stash -p, usando split (s) para dividir mudanças em hunks menores e escolher (y/n) exatamente o que vai pro stash, deixando o resto no working directory.

• Stash branch: git stash branch <nome> stash@{n} para recuperar um stash numa branch nova, criada a partir do commit em que ele foi originado — evita conflito quando o main avançou com mudanças incompatíveis.



Aprendizado principal: o stash branch resolve o problema de “meu stash não bate mais com o main atual”, porque ele reconstrói o ponto de partida certo antes de aplicar as mudanças, ao invés de tentar encaixar o stash na ponta atual do main.

## Módulo 7: Merge Strategies e rerere

Prática de estratégias de merge do Git, resolução de conflitos com
`-X ours`/`-X theirs`, uso do `git rerere` e teste do merge `octopus`.

### O que foi praticado

1. **Fast-forward vs `--no-ff`**
- Fast-forward: merge sem commit, ponteiro só avança.
- `--no-ff`: força merge commit mesmo quando fast-forward seria possível,
preservando no histórico o registro de que a feature existiu como
branch separada.

2. **Resolução automática de conflito com `-X ours` / `-X theirs`**
- `-X ours`: em conflito, mantém a versão que já estava na branch atual.
- `-X theirs`: em conflito, mantém a versão da branch que está entrando.
- Fast-forward ignora `-X` completamente (não há conflito pra resolver).

3. **`git rerere` (Reuse Recorded Resolution)**
- Ativado com `git config rerere.enabled true`.
- Grava a resolução de um conflito e reaplica automaticamente se o
mesmo conflito aparecer de novo.
- Por padrão não dá `git add` sozinho (`rerere.autoUpdate` desligado);
o merge segue marcado como "unmerged" até o add manual, mesmo com
o conteúdo já resolvido.

4. **Merge `octopus` (3+ branches)**
- Mescla várias branches numa única operação, só quando não há conflito.
- Se qualquer branch conflitar, a operação é **atômica**: desfaz tudo,
inclusive partes que já teriam dado fast-forward — não é possível
resolver manualmente no meio do processo.
- Nesse teste, deu conflito e foi abortado; refeito com merges
individuais (`feature-a`, `feature-b`, `feature-c`).

### Commits principais
- Fast-forward: `feature-debug`
- `--no-ff`: `feature-timeout`
- `-X ours`: `feature-timeout-90` → `feature-timeout-120`
- `-X theirs`: `feature-timeout-77` (conflito real, direto no main)
- rerere: `feature-rerere-teste` (conflito repetido, resolução reaplicada)
- octopus (falhou) → merges individuais: `feature-a`, `feature-b`, `feature-c`



## Módulo 8 — Hooks (pre-commit, pre-push, commit-msg)

### Teoria

Hooks são scripts que o Git executa automaticamente em pontos do fluxo (commit, push, etc.), guardados em `.git/hooks/`. Não são versionados por padrão porque `.git/` nunca vai pro repositório — a solução é `core.hooksPath`, apontando pra uma pasta dentro do próprio projeto.

Podem ser escritos em qualquer linguagem (precisam de shebang + permissão de execução). O exit code decide o resultado: `0` deixa passar, qualquer coisa diferente de `0` cancela a ação.

- **pre-commit**: roda antes do commit ser criado. Usado aqui pra bloquear `print()` de debug staged.
- **commit-msg**: roda depois da mensagem escrita, recebe o caminho do arquivo de mensagem como `$1`. Usado aqui pra exigir prefixo convencional (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`).
- **pre-push**: roda antes do push, recebe remoto via stdin. Usado aqui pra rodar os testes (`test_app.py`) antes de liberar o push.

### Prática

Dentro de `modulo8-hooks/` (app.py, test_app.py), implementados e testados os 3 hooks. Todos bloquearam corretamente nos casos esperados (print staged, mensagem sem prefixo, teste falho) e liberaram nos casos válidos.

### Bug encontrado e corrigido

A primeira versão do pre-commit usava `git diff --cached` só pra **listar** os arquivos staged, mas o `grep` de `print(` rodava no arquivo do **disco**, não no conteúdo staged (index). Resultado: editar o arquivo no disco sem re-dar `git add` bastava pra passar no hook, mesmo com o `print()` ainda staged — confirmado na prática com `git show`, que mostrou o print entrando no histórico apesar do hook ter "bloqueado" a tentativa anterior.

Corrigido trocando o grep no disco por `git show ":$arquivo" | grep -n "print("`, que lê o conteúdo real do index. Testado de novo reproduzindo o mesmo cenário: dessa vez bloqueou corretamente.

### Versionamento via core.hooksPath

Hooks copiados pra `.githooks/` (versionada) e ativados com `git config core.hooksPath .githooks`.

**Atenção:** `core.hooksPath` é uma config local (fica em `.git/config`, não versionado). Quem clonar o repo do zero precisa rodar `git config core.hooksPath .githooks` manualmente — os hooks não ativam sozinhos só por estarem na pasta.

