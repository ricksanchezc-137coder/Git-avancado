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

