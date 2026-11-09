# Dados usados na simulacao

- `parametros_original_copa.json`: grupos e rankings hard-coded do codigo original.
- `scores_selecoes_principal_50mil.csv`: as variaveis V1, V2, V3, V5, V6 e nota do goleiro ja agregadas. Permite reproduzir a simulacao sem expor os atributos dos jogadores.
- `resultados_copa_2026.csv`: calendario e resultados fornecidos no projeto, usados para definir os confrontos da fase de grupos e avaliar previsoes individuais retrospectivamente. **Nao determina os resultados simulados.**
- `_annex_c_2026.txt`: tabela de 495 combinacoes dos melhores terceiros, do Anexo C do regulamento FIFA 2026 (mapeamento reportado no codigo).

## Bases nao distribuidas

Os CSVs brutos `jogadores_copa_2026.csv` e `treinadores_copa_2026.csv` contêm atributos individuais provenientes do Football Manager. Verifique permissao de redistribuicao antes de publica-los. O script utiliza os scores agregados quando esses arquivos nao estao em `dados_restritos/`.

Se voce estiver autorizado a processar localmente as bases brutas, coloque os dois CSVs dentro de `dados_restritos/`. Essa pasta esta no `.gitignore`. Com eles, o script pode recalcular a forca do elenco, inclusive o cenario com 6 meio-campistas.

Nota cientifica: as pontuacoes de entrada dependem de valores heurísticos e a base nao comprova calibracao estatistica. Veja `docs/METODOLOGIA_E_LIMITACOES.md`.
