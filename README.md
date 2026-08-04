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


## Módulo 9 — Worktrees

### Teoria
`git worktree` permite ter múltiplos diretórios de trabalho ligados ao mesmo
repositório, cada um numa branch diferente, ao mesmo tempo — sem precisar
clonar o repo de novo. Cada worktree tem sua própria working directory e
seu próprio index, mas todos compartilham o mesmo histórico de commits
(.git). A mesma branch não pode estar checked out em dois worktrees ao
mesmo tempo — o Git bloqueia isso pra evitar inconsistência.

### Prática
- Criado o worktree `worktree-feature` numa branch nova (`feature-worktree`)
com `git worktree add <caminho> -b <branch>`
- Editado o `app.py` de forma diferente em cada worktree, sem commitar;
confirmado com `git status` que cada worktree só enxerga a própria
mudança
- Commitado separadamente em cada worktree (`main` e `feature-worktree`),
confirmando com `git log --oneline` que os históricos divergem mas
compartilham o mesmo `.git`
- Testado o bloqueio de branch duplicada: `git checkout feature-worktree`
a partir do repo principal falhou com
`fatal: 'feature-worktree' is already used by worktree at '...'`
- Removido o worktree extra com `git worktree remove` e confirmado com
`git worktree list` que só sobrou o worktree principal

### Achados
- O worktree nasceu **dentro** de `~/git-avancado` em vez de como pasta
irmã (erro de planejamento do caminho relativo), o que fez o `git status`
do repo principal listar `worktree-feature/` como untracked. Confirma na
prática por que a convenção é sempre criar worktrees fora da pasta do
repo principal.
- O hook `pre-commit` do módulo 8 bloqueou o commit inicial por causa de
um `print()` proposital do exercício (falso positivo) — resolvido com
`git commit --no-verify`. Mostra a limitação de hooks simples baseados
em regex: são cegos ao contexto.


##Módulo 10 — Submodules vs Subtrees



Duas formas de incluir um repositório externo (Katas) dentro do git-avancado, com filosofias opostas: submodule mantém referência separada por pointer; subtree mescla o conteúdo direto no histórico.



Submodule — praticado em modulo10-submodules-subtrees/katas (removido ao final):



• git submodule add cria .gitmodules e uma entrada especial (modo 160000) apontando pra um commit específico do Katas

• Clone normal (sem --recurse-submodules) traz a pasta vazia; precisa de git submodule update --init pra popular

• Dentro do submodule, o Git deixa em HEAD detached, não numa branch

• Commit novo dentro do submodule não atualiza o repo pai sozinho — precisa de commit explícito no pai atualizando o pointer

• Remoção completa exige 3 passos: deinit, rm, e limpar .git/modules/

• Bônus real: dois clones locais (git-avancado e um clone de teste) divergiram por causa de pushes em momentos diferentes, gerando um conflito modify/delete genuíno, resolvido via git pull --no-rebase + git rm + commit de merge



Subtree — praticado em modulo10-submodules-subtrees/katas-subtree:



• git subtree add --squash já traz o conteúdo completo de cara, sem init, e cria o(s) commit(s) automaticamente

• git subtree pull --squash traz atualizações do repo externo, mesclando direto — passou pelo hook de commit-msg (Módulo 8) porque usa git merge por baixo, diferente do add/squash interno que usa commit-tree e não aciona hooks

• git subtree push extrai mudanças feitas na subpasta e manda de volta pro repo externo como commit normal, com fast-forward limpo do outro lado



Conclusão prática: subtree evita as duas maiores dores do submodule no dia a dia (init/update manual e pointer desatualizado), ao custo de reconstruir histórico compartilhado nas trocas (pull/push mais lentos) e do repo pai crescer com o conteúdo externo embutido.

## Módulo 11 — Log/blame avançado

Praticado no próprio repo git-avancado (histórico mais rico que o sistema-bancario, com branches e merges reais).

**Filtros de log:**
- `--graph --oneline --all --decorate` — visualização de branches/merges
- `--author="nome"` combinado com filtro de path (`-- pasta/`)
- `--grep` (múltiplos = OR por padrão; `--all-match` = AND)
- `--since`/`--until` com data absoluta

**Pickaxe:**
- `-S"string"` — commits onde a contagem de ocorrências mudou
- `-G"regex"` — commits onde uma linha casando com o regex mudou (mesmo sem alterar contagem)
- Testado com 3 commits propositais numa função `soma`, provando a diferença na prática

**Blame avançado:**
- `-L linha,linha` — limita a um intervalo
- `-w` — ignora diferença de espaço em branco
- `-M` — detecta linhas movidas (exige conteúdo byte-idêntico; cut/paste funciona, retype não)
- `-C` — detecta linhas copiadas de outro arquivo (tem limiar mínimo de 40 caracteres; níveis mais altos buscam em todo o histórico, com risco de falso positivo)
- `--reverse` — rastreia a última revisão onde uma linha existiu, útil pra achar quando algo foi removido


## Módulo 12 — Workflows e branching strategies

### Teoria
Comparação entre três estratégias de branching: **Gitflow** (branches
main/develop/feature/release/hotfix, pensado pra releases versionadas),
**GitHub Flow** (só main + feature branches, integração via PR, deploy
imediato) e **Trunk-based development** (commits diretos ou branches
de vida curtíssima direto em main/trunk, com feature flags escondendo
código incompleto).

### Prática
Simulei os três workflows na subpasta `modulo12-workflows`:

- **Gitflow completo**: `feature/boas-vindas` → `develop` → `release/1.0`
(tag v1.0) → `main` → `hotfix/corrige-bug` (tag v1.0.1) → `develop`.
Total: 3 branches temporárias, 4 merge commits, 2 tags.
- **GitHub Flow**: `feature/despedida-formal` criada direto de `main`,
merge --no-ff direto de volta pra `main`. Sem `develop`, sem `release`.
Total: 1 branch, 1 merge commit.
- **Trunk-based**: commit direto em `main` (`log_acao` atrás de uma
feature flag `FEATURE_LOG_ATIVO`). Zero branches, zero merges.

### Descoberta prática
O hook `commit-msg` do Módulo 8 bloqueia até merge commits automáticos
(mensagem padrão "Merge branch..." não bate com nenhum prefixo aceito),
já que o hook não tem exceção pra esse tipo de commit — diferente do
comportamento comum em hooks reais. Resolvido usando `--no-verify`
nos merges.

### Conclusão
Fica visível na prática o trade-off de overhead: Gitflow garante
organização forte pra releases versionadas, mas custa 3x mais branches
e merges que GitHub Flow pra entregar a mesma mudança; trunk-based
elimina esse custo por completo, mas exige testes/CI muito mais
maduros e feature flags pra não quebrar produção.

##Módulo 13 — Config avançado e aliases personalizados


O Git resolve suas configurações em três camadas hierárquicas: system (/etc/gitconfig, escopo de máquina, ausente por padrão no Termux por não haver separação entre admin e usuário), global (~/.gitconfig, escopo de usuário) e local (.git/config, escopo de repositório). A resolução segue precedência estrita local > global > system: quando a mesma chave existe em mais de uma camada, o Git usa a versão mais específica e ignora as demais, sem mesclar valores. A introspecção dessa hierarquia é feita com git config --list --show-origin, que lista todas as chaves ativas anotando o arquivo de origem de cada uma, e git config --list --local --show-origin, que restringe a listagem à camada local. Nesse módulo isso foi validado sobrescrevendo user.email no escopo local de um repositório e confirmando com git config user.email (resolução efetiva) versus git config --global user.email (valor global, que permanece intocado); a reversão foi feita com git config --unset.



Aliases são atalhos armazenados na seção [alias] do arquivo de configuração e existem em três níveis de sofisticação crescente. Aliases simples (git config --global alias.co checkout) apenas substituem texto após git , sem interpretação de shell. Aliases prefixados com ! são delegados inteiramente ao interpretador de shell em vez de serem tratados como subcomando do Git, o que permite compor flags e encadear lógica arbitrária — mas isso introduz uma armadilha de shell: no bash, ! seguido de caractere alfanumérico aciona expansão de histórico (history expansion) mesmo dentro de aspas duplas, já que aspas duplas preservam a maioria das expansões do shell e não bloqueiam essa em particular. O resultado é que git config --global alias.lg "!git log --oneline --graph --all --decorate" foi aceito sem erro de sintaxe, mas gravou um valor corrompido/incompleto na seção [alias] — confirmado via inspeção direta com cat ~/.gitconfig, que mostrou a ausência da entrada esperada. A correção exigiu aspas simples, que suprimem toda expansão do shell: git config --global alias.lg '!git log --oneline --graph --all --decorate'. A mesma causa raiz se repetiu no alias last.



O terceiro nível — aliases que aceitam argumentos posicionais — requer a definição de uma função de shell nomeada inline, invocada ao final da string: !f() { git checkout -b "$1"; }; f. A primeira tentativa (!f() {git checkout -b "$1"; }; f) falhou com “syntax error: ‘}’ unexpected”, porque { e } em contexto de bloco de comando do shell são palavras reservadas (reserved words), não pontuação, e precisam estar delimitadas por espaço em ambos os lados para serem tokenizadas corretamente; colado ao git seguinte, o { foi absorvido como parte de um token só e o parser nunca reconheceu a abertura de bloco. Corrigido inserindo o espaço, o alias new passou a criar e trocar de branch corretamente a partir de um argumento (git new branch-test), testado e depois desfeito com git branch -d.



Por fim, includeIf permite inclusão condicional de um arquivo de configuração adicional baseada no diretório de trabalho, útil para separar identidade/config entre contextos (ex: pessoal vs. profissional) sem sobrescrita manual por repositório. A sintaxe registrada via git config --global includeIf.gitdir:<caminho>/.path <arquivo> aponta para um arquivo de config alternativo que só é mesclado quando o .git do repositório atual está sob o caminho especificado. Isso foi validado criando ~/.gitconfig-teste com um user.email alternativo via git config -f ~/.gitconfig-teste user.email <valor>, registrando a condição para o diretório do repositório em uso, e confirmando a resolução efetiva de dentro do repositório (valor alternativo) e de fora dele (valor global original inalterado) — demonstrando que a condição de gitdir é avaliada dinamicamente por diretório corrente, não fixada no momento da configuração. Removido ao final com --unset do includeIf e exclusão do arquivo auxiliar.



Configuração final de aliases persistida no ~/.gitconfig: st (status), co (checkout), br (branch), lg (!git log --oneline --graph --all --decorate), last (!git log -1 HEAD --stat) e new (!f() { git checkout -b "$1"; }; f).

## Módulo 14 — Colaboração avançada

**Teoria**
- Pull Request (PR): pedido formal de merge entre branches no GitHub. Mostra diff, permite comentários e review, roda CI antes do merge — não existe como comando git puro, é recurso da plataforma.
- Code review: aprovação (Approve), rejeição (Request changes) ou comentário no PR. O autor da PR nunca pode aprovar a própria PR.
- Protected branches: regras numa branch (ex: main) — bloqueiam push direto, exigem PR + aprovação, podem exigir CI passando. O dono/admin do repo tem bypass automático dessas regras por padrão, a menos que "Do not allow bypassing the above settings" esteja marcado.
- Squash and merge: colapsa todos os commits da branch em um único commit linear na branch de destino.
- Create a merge commit: preserva os commits individuais da branch e cria um commit de merge com dois pais.
- Rebase and merge: reaplica os commits da branch um a um sobre o destino, sem commit de merge, mantendo granularidade.

**Prática**
- Branch `modulo14-colaboracao` criada com 3 commits (`d971bb7`, `989e0f6`, `c995b2d`); PR #1 aberta contra a main.
- Protected branch rule criada na main: "Require a pull request before merging" + "Require approvals" (1).
- Testado bypass de admin: com a regra ativa mas sem "Do not allow bypassing", apareceu checkbox "Merge without waiting for requirements to be met (bypass rules)" — dono do repo consegue ignorar a exigência de review. Ativando "Do not allow bypassing", a checkbox some e o merge trava por completo, até pra o owner.
- PR #1 mergeada com **squash and merge** → main recebeu um único commit (`bb0f1eb`), histórico linear, sem rastro dos 3 commits originais no `git log` local.
- Branch `modulo14-merge-commit` criada com 2 commits (`d1346de`, `70a9d03`); PR #2 aberta e mergeada com **Create a merge commit** → gerou commit de merge real (`0a8e5c5`) com duas linhas de pai, preservando os commits individuais.
- Comparação confirmada com `git log --graph --oneline`: squash aparece reto na linha principal, merge commit aparece com ramificação (`|\`) antes de convergir.

