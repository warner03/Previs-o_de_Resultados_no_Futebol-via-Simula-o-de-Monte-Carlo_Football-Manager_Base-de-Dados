# Simulador Brasileirão Série A 2026 (Monte Carlo + Força Híbrida)

Material da parte do Campeonato Brasileiro Série A do artigo "Previsão de Resultados no Futebol via Simulação de Monte Carlo: O Uso do Football Manager como Base de Dados". Projeto de Iniciação Científica da UFJ.

## O que o código faz

1. Lê os elencos do Football Manager 2026 (Current Ability e Potential Ability por jogador).
2. Registra os resultados reais por rodada e recalcula a classificação oficial.
3. Calcula a força de cada clube (Força Híbrida): 50% FM26 + 50% desempenho real.
4. Simula o restante do campeonato 10.000 vezes (Poisson + Fator de Fase) e estima as probabilidades de título, vaga na Libertadores e rebaixamento.
5. Valida o modelo jogo a jogo (Brier Score e acurácia) com a correção de Dixon-Coles.
6. Envia classificação e projeção para um banco Supabase, que alimenta o site.

Site: https://brasileirao-2026-simulator.vercel.app

## Modelo

- Gols por Poisson, com λ ancorado em MU = 1,3 gols por time por jogo.
- Força FM26: média dos 16 melhores CA do elenco, elevada ao cubo, normalizada para média 1,0.
- Força Real: 60% aproveitamento de pontos + 40% saldo de gols, normalizada para média 1,0.
- Força Híbrida: 0,50 FM26 + 0,50 Real.
- Mando de campo: fator 1,15 para o mandante.
- Fator de Fase: N(1,0; 0,20), limitado a [0,5; 1,5], sorteado uma vez por simulação e aplicado a todos os clubes.
- λ limitado ao intervalo [0,3; 4,0].
- Dixon-Coles (ρ = -0,13) é usado apenas na validação, não na simulação da temporada.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `SimuladorSerieA_2026.ipynb` | Motor de simulação e validação (10 células) |
| `Busca_Jogadores.ipynb` | Coleta dos atributos de jogadores (Selenium) |
| `requirements.txt` | Dependências Python |

A planilha bruta com os atributos individuais do Football Manager não é redistribuída neste repositório.

## Como executar

1. Abra `SimuladorSerieA_2026.ipynb` no Google Colab.
2. Configure as credenciais do Supabase como secrets do Colab (`SUPABASE_URL` e `SUPABASE_SECRET_KEY`). Nunca escreva a chave no notebook.
3. Em `ATE_RODADA`, use `None` para a rodada atual ou um número para recriar o histórico.
4. Execute as células em ordem.

## Observações

- A validação do artigo cobre as rodadas 1 a 19 (1.º turno).
- Os atributos do FM26 foram coletados em maio de 2026 e não são atualizados durante o campeonato.
