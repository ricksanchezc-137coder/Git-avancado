# Git Avançado — Currículo 11

Exercícios práticos, um módulo por commit.

## Módulo 1 — Internals do Git

- Objects: blob (conteúdo), tree (estrutura de pastas), commit (snapshot + metadados)
- Refs (branches) são só arquivos texto apontando pra um hash de commit
- Hash é gerado a partir do CONTEÚDO, não do nome — dois arquivos idênticos
geram o mesmo blob (deduplicação automática)
- Histórico é uma cadeia: cada commit aponta pro seu parent
