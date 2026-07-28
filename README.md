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
