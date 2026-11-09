# Guia para iniciantes: GitHub, Python e Overleaf

## O que e cada coisa?

- **Git**: registra versoes do seu trabalho. Um `commit` e como um ponto de salvamento.
- **GitHub**: guarda online o repositorio Git, permitindo consultar codigo e historico.
- **Repositorio**: pasta do projeto com todo o historico.
- **README.md**: primeira pagina visivel ao abrir o repositorio no GitHub.
- **.gitignore**: lista arquivos que o Git nao deve incluir automaticamente, como ambientes virtuais e dados brutos restritos.
- **main (branch)**: versao de referencia do projeto.
- **Commit**: alteracao registrada com uma mensagem.
- **Push**: envia seus commits locais para o GitHub.
- **Pull**: baixa as alteracoes remotas. Como voce trabalha sozinho, o fluxo principal e editar, salvar, `git add`, `git commit`, `git push`.

## Estrutura das pastas

```text
repositorio/
├── README.md                   ← visão geral dos dois trabalhos
├── artigo/                     ← artigo e bibliografia compartilhados
├── copa-do-mundo/
│   ├── codigos/                ← notebook isolado, campeonato completo e avaliação
│   ├── requirements.txt        ← dependência do simulador
│   ├── .gitignore              ← ignora dados restritos da Copa
│   ├── dados/                  ← parâmetros agregados
│   ├── resultados/publicados/  ← simulações já realizadas
│   ├── resultados/gerados/     ← saídas de novas execuções
│   ├── tests/                  ← testes de consistência
│   └── docs/                   ← documentação detalhada
└── brasileirao/
    └── .gitkeep                ← pasta reservada ao colega
```

## Executar no Fedora

Abra um terminal na pasta descompactada e rode **um comando de cada vez**:

```bash
cd ~/Downloads/Previs-o_de_Resultados_no_Futebol-via-Simula-o-de-Monte-Carlo_Football-Manager_Base-de-Dados/copa-do-mundo
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python codigos/simulacao_campeonato_completo_copa_2026.py --simulacoes 1000 --semente 20261109 --sufixo teste
```

Arquivos novos aparecerao em `resultados/gerados/`. Para reproduzir a tabela principal, troque `1000` por `50000` e `teste` por `reproducao_50mil`.

**Dica:** se o terminal ficar com o simbolo `>` em vez de mostrar o prompt normal, pode haver uma aspa aberta. Pressione `Ctrl+C` e cole um comando curto por vez.

## Artigo no Overleaf

Use o ZIP `Projeto_Overleaf_Copa_2026_VERIFICADO.zip` da entrega, ou crie um projeto vazio e envie os quatro arquivos de `artigo/` que compõem o fonte (`main.tex`, `biblioteca.bib`, `referencias_novas.bib`, `figura_probabilidades_copa_2026.png`). O PDF e apenas uma copia ja compilada.

`main.tex` define o texto e as formulas; os arquivos `.bib` guardam as referencias bibliograficas; `.png` e a figura do artigo. Se mudar uma referencia `.bib`, use o comando `\cite{chave}` dentro de `main.tex`.

## Alterar codigo com Git

Depois de clonar o repositório e editar este projeto, o ciclo de alteracoes no Fedora sera:

```bash
git status
git add .
git commit -m "Atualiza simulacao e texto"
git push
```

`git status` mostra arquivos alterados, `git add .` seleciona mudancas, `git commit` salva uma versao, `git push` envia ao GitHub. Isso nao modifica automaticamente os arquivos do Overleaf; para sincronizacao automatica seria preciso configurar a integracao Git do Overleaf, que depende do plano.

## O que nao enviar sem revisar

Nao publique senhas, tokens, dados pessoais nem bases completas de atributos do Football Manager sem verificar seus direitos de redistribuicao. Nao invente autores, licencas ou DOI. Esta distribuicao nao adiciona `LICENSE` enquanto os autores nao escolherem uma licenca.
