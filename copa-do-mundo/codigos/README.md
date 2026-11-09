# Códigos da Copa do Mundo 2026

Os códigos estão separados por objetivo:

| Arquivo | Finalidade |
|---|---|
| `simulacao_partidas_isoladas_copa_2026.ipynb` | **Google Colab:** 10.000 sorteios Poisson para cada confronto individual, com probabilidades vitória/empate/derrota nos 90 minutos. **Não** calcula campeão. |
| `simulacao_campeonato_completo_copa_2026.py` | **Python:** 50.000 torneios completos de grupos ao título, com critérios de classificação, prorrogação e pênaltis. |
| `avaliar_previsoes_fases_copa_2026.py` | **Python:** confronta a classificação observada com as probabilidades por fase, calculando recuperação top-k e Brier binário. |

A partir da pasta `copa-do-mundo/`, rode:

```bash
python -m unittest discover -s tests -v
python codigos/simulacao_campeonato_completo_copa_2026.py --simulacoes 1000 --semente 20261109 --sufixo teste
python codigos/avaliar_previsoes_fases_copa_2026.py
```

O arquivo `.ipynb` pode ser aberto no Google Colab. As planilhas brutas Football Manager não estão no repositório público; utilizam-se scores agregados.

**Diferença metodológica:** as 10 mil simulações são por partida isolada; as 50 mil simulações são do campeonato inteiro. O código histórico recebido chamava 5.000 repetições em um trecho; o novo notebook fixa 10.000 e não reproduz exatamente os valores originais armazenados antes das correções.
