# Como trabalhar com GitHub após a publicação

O projeto já utiliza o repositório da conta `warner03`. Estrutura: `README.md` e `artigo/` gerais; `copa-do-mundo/` contém todo o código desta pesquisa; `brasileirao/` foi reservado para o colega.

## Baixar no Fedora

```bash
git clone https://github.com/warner03/Previs-o_de_Resultados_no_Futebol-via-Simula-o-de-Monte-Carlo_Football-Manager_Base-de-Dados.git
cd Previs-o_de_Resultados_no_Futebol-via-Simula-o-de-Monte-Carlo_Football-Manager_Base-de-Dados/copa-do-mundo
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python simulacao_copa_2026.py --simulacoes 1000 --semente 20261109 --sufixo teste
```

Use `git status` para conferir arquivos alterados. Na pasta raiz do repositório, `git add .`, `git commit -m "Descreve alterações"` e `git push` publicam mudanças após salvar localmente. Não use `git push --force` sem revisar o histórico.

## Brasileirão e artigo

O colega poderá acrescentar arquivos dentro de `brasileirao/`. Os autores devem revisar conjuntamente qualquer alteração em `artigo/`. O arquivo `.gitkeep` é só um marcador técnico para representar a pasta no GitHub.

As planilhas brutas de atributos do Football Manager não estão incluídas na versão pública; não publique material restrito sem verificar autorização.
