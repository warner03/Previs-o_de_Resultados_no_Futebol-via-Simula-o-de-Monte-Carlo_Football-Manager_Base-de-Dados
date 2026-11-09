#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Avaliação retrospectiva do avanço de fases da Copa 2026.

Métrica 1: recuperação top-k (não é acurácia de partidas).
Métrica 2: Brier binário médio em TODAS as 48 seleções.
Entrada: probabilidades dos 50.000 torneios e participantes observados por fase.
"""
from pathlib import Path
import csv
from simulacao_campeonato_completo_copa_2026 import REAL_NAME

ROOT=Path(__file__).resolve().parent.parent
FASES=[
    ("16-avos","16avos","P_16avos_pct",32),
    ("Oitavas","Oitavas","P_oitavas_pct",16),
    ("Quartas","Quartas","P_quartas_pct",8),
    ("Semifinais","Semifinal","P_semifinal_pct",4),
    ("Final","Final","P_final_pct",2),
    ("Título",None,"P_campeao_pct",1),
]

def read(rel):
    with (ROOT/rel).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def avaliar():
    prev=read("resultados/publicados/probabilidades_fases_copa_2026_principal_50mil.csv")
    jogos=read("dados/resultados_copa_2026.csv")
    todas={r["Selecao"] for r in prev}
    assert len(todas)==48
    final=next(j for j in jogos if j["Fase"]=="Final")
    if int(final["Gols_Mandante"])==int(final["Gols_Visitante"]):
        raise ValueError("A planilha não informa vencedor da final empatada")
    vencedor=final["Mandante"] if int(final["Gols_Mandante"])>int(final["Gols_Visitante"]) else final["Visitante"]
    linhas=[]
    for fase,rotulo,coluna,k in FASES:
        obs=({REAL_NAME.get(vencedor,vencedor)} if rotulo is None else
             {REAL_NAME.get(t,t) for jogo in jogos if jogo["Fase"]==rotulo
              for t in (jogo["Mandante"],jogo["Visitante"])})
        assert len(obs)==k and obs<=todas, (fase,len(obs),obs-todas)
        p={r["Selecao"]:float(r[coluna])/100 for r in prev}
        top=set(sorted(todas,key=lambda t:(-p[t],t))[:k])
        acertos=len(top & obs)
        brier=sum((p[t]-int(t in obs))**2 for t in todas)/48
        baseline=(k/48)*(1-k/48)
        linhas.append({"Fase":fase,"K_classificados":k,"Acertos_top_K":acertos,
                      "Recuperacao_top_K_pct":round(acertos/k*100,3),
                      "Brier_binario":round(brier,6),
                      "Brier_referencia_uniforme":round(baseline,6)})
    return linhas

if __name__=="__main__":
    rows=avaliar()
    out=ROOT/"resultados"/"gerados"/"avaliacao_fases_copa_2026.csv"
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    for x in rows:
        print(x["Fase"],f'{x["Acertos_top_K"]}/{x["K_classificados"]}',
              f'BS={x["Brier_binario"]:.4f}')
    print(out)
