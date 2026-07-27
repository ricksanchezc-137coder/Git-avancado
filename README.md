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

