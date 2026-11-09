# Artigo para Overleaf

Arquivos necessarios para compilar o PDF:

1. `main.tex` — codigo LaTeX completo do artigo.
2. `biblioteca.bib` — referencias bibliograficas originais.
3. `referencias_novas.bib` — referencias acrescentadas na revisao.
4. `figura_probabilidades_copa_2026.png` — grafico usado com `\includegraphics`.

**Nao e necessario copiar o Python para o Overleaf.** O artigo compila separadamente do simulador.

No Overleaf, use `New Project` > `Upload Project` e envie o ZIP especifico do Overleaf, disponibilizado junto ao pacote. Em um projeto novo, escolha `main.tex` como arquivo principal e `pdfLaTeX` como compilador. O arquivo PDF nesta pasta e uma pre-visualizacao, nao o codigo fonte.

O comando de bibliografia do documento e `\bibliography{biblioteca,referencias_novas}`. Os nomes dos arquivos `.bib` precisam ser exatamente esses.
