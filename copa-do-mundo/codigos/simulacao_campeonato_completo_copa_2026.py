#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simulação completa do campeonato da Copa 2026: grupos até campeão.

Entradas publicas: parametros agregados, sem redistribuir microdados do jogo.
Pesos de score, ranks e vantagem dos anfitrioes: algoritmo original.
Correcao de rotulos, limite de 16 atletas, prorrogação e pênaltis:
revisoes metodologicas explicitadas no relatorio e no artigo revisado.
Requer Python 3.11+ e numpy 2.3.5 para reproducao bit a bit. Nao usa resultados reais nas simulacoes
prospectivas; a planilha real so serve para diagnosticos e validacao separada.

Fonte da tabela oficial dos 495 pareamentos de terceiras colocadas:
Regulamento FIFA World Cup 26 (May 2026), Annex C, pp. 80-97:
https://digitalhub.fifa.com/m/636f5c9c6f29771f/original/FWC2026_regulations_EN.pdf
"""
from __future__ import annotations
import argparse
import csv
from collections import defaultdict, Counter
from itertools import combinations
from pathlib import Path
from math import exp
import json
import numpy as np

BASE = Path(__file__).resolve().parent.parent
HOSTS = {'México', 'Estados Unidos', 'Canadá'}

# correspondencias EXPLICITAS; eliminam difflib e a ambiguidade nos nomes
PLAYER_NAME = {
'Algeria':'Argélia','Argentina':'Argentina','Australia':'Austrália','Austria':'Áustria',
'Belgium':'Bélgica','Bosnia And Herzegovina':'Bósnia','Brazil':'Brasil','Cabo Verde':'Cabo Verde',
'Canada':'Canadá','Colombia':'Colômbia','Congo DR':'RD Congo','Croatia':'Croácia',
'Czechia':'República Tcheca','Ecuador':'Equador','Egypt':'Egito','England':'Inglaterra',
'France':'França','Germany':'Alemanha','Ghana':'Gana','Haiti':'Haiti','IR Iran':'Irã',
'Iraq':'Iraque','Japan':'Japão','Jordan':'Jordânia','Korea Republic':'Coreia do Sul',
'Mexico':'México','Morocco':'Marrocos','Netherlands':'Países Baixos',
'New Zealand':'Nova Zelândia','Norway':'Noruega','Panama':'Panamá','Paraguay':'Paraguai',
'Portugal':'Portugal','Qatar':'Catar','Saudi Arabia':'Arábia Saudita','Scotland':'Escócia',
'Senegal':'Senegal','South Africa':'África do Sul','Spain':'Espanha','Sweden':'Suécia',
'Switzerland':'Suíça','Tunisia':'Tunísia','USA':'Estados Unidos','Uruguay':'Uruguai',
'Uzbekistan':'Uzbequistão','ao':'Curaçao','rkiye':'Turquia',"te D'Ivoire":'Costa do Marfim',
}
COACH_NAME = {'Holanda':'Países Baixos','Congo RD':'RD Congo'}
REAL_NAME = {
'Mexico':'México','South Africa':'África do Sul','South Korea':'Coreia do Sul',
'Czech Republic':'República Tcheca','Canada':'Canadá','Bosnia and Herzegovina':'Bósnia',
'USMNT':'Estados Unidos','USA':'Estados Unidos','Paraguay':'Paraguai','Qatar':'Catar',
'Switzerland':'Suíça','Brazil':'Brasil','Morocco':'Marrocos','Haiti':'Haiti',
'Scotland':'Escócia','Australia':'Austrália','Turkey':'Turquia','Germany':'Alemanha',
'Curaçao':'Curaçao','Netherlands':'Países Baixos','Japan':'Japão',
'Ivory Coast':'Costa do Marfim','Ecuador':'Equador','Sweden':'Suécia','Tunisia':'Tunísia',
'Spain':'Espanha','Cape Verde Islands':'Cabo Verde','Belgium':'Bélgica','Egypt':'Egito',
'Saudi Arabia':'Arábia Saudita','Uruguay':'Uruguai','Iran':'Irã','New Zealand':'Nova Zelândia',
'France':'França','Senegal':'Senegal','Iraq':'Iraque','Norway':'Noruega',
'Argentina':'Argentina','Algeria':'Argélia','Austria':'Áustria','Jordan':'Jordânia',
'Portugal':'Portugal','Congo DR':'RD Congo','England':'Inglaterra','Croatia':'Croácia',
'Ghana':'Gana','Panama':'Panamá','Uzbekistan':'Uzbequistão','Colombia':'Colômbia',
}

# FIFA Round-of-32, Annex C: 1A, 1B, 1D, 1E, 1G, 1I, 1K, 1L
ANNEX_WINNERS = 'ABDEGIKL'
R32 = {
73:('2A','2B'), 74:('1E','3E'), 75:('1F','2C'), 76:('1C','2F'),
77:('1I','3I'), 78:('2E','2I'), 79:('1A','3A'), 80:('1L','3L'),
81:('1D','3D'), 82:('1G','3G'), 83:('2K','2L'), 84:('1H','2J'),
85:('1B','3B'), 86:('1J','2H'), 87:('1K','3K'), 88:('2D','2G')}
R16 = {89:(74,77),90:(73,75),91:(76,78),92:(79,80),
93:(83,84),94:(81,82),95:(86,88),96:(85,87)}
QF = {97:(89,90),98:(93,94),99:(91,92),100:(95,96)}
SF = {101:(97,98),102:(99,100)}

def load_csv(name):
 with (BASE/name).open(encoding='utf-8-sig',newline='') as f:
  return list(csv.DictReader(f))

def load_model(num_midfield=5):
 meta=json.loads((BASE/'dados'/'parametros_original_copa.json').read_text(encoding='utf-8'))
 groups=meta['grupos']; ranks=meta['rankings']
 teams=[t for group in groups.values() for t in group]
 assert len(teams)==len(set(teams))==48
 # Reproducao publica: parametros agregados previamente derivados dos microatributos.
 # O dataset bruto nao e redistribuido. Valores v1-v6 mantem precisao completa.
 raw_players=BASE/'dados_restritos'/'jogadores_copa_2026.csv'
 raw_coaches=BASE/'dados_restritos'/'treinadores_copa_2026.csv'
 if not raw_players.exists() or not raw_coaches.exists():
  if num_midfield != 5:
   raise FileNotFoundError('Analise com 6 meio-campistas requer dados_restritos/ com CSVs originais.')
  rows=load_csv('dados/scores_selecoes_principal_50mil.csv')
  breakdown={};scores={};goalies={}
  for row in rows:
   t=row['Selecao']
   v1,v2,v3,v5,v6=(float(row[f'v{i}']) for i in (1,2,3,5,6))
   sc=.50*v1+.10*v6+.10*v2+.15*v3+.15*v5
   gk=float(row['nota_goleiro'])
   scores[t]=sc;goalies[t]=gk
   breakdown[t]={'score':sc,'nota_goleiro':gk,'v1':v1,'v2':v2,
       'v3':v3,'v5':v5,'v6':v6,'quantidade_jogadores':int(row['quantidade_jogadores'])}
  assert set(scores)==set(teams),(set(teams)-set(scores),set(scores)-set(teams))
  return groups,ranks,scores,goalies,breakdown
 players=defaultdict(list)
 for row in load_csv('dados_restritos/jogadores_copa_2026.csv'):
  raw=row['Seleção']
  if raw not in PLAYER_NAME:raise ValueError('Pais nao mapeado na base de jogadores: '+raw)
  players[PLAYER_NAME[raw]].append(row)
 assert set(players)==set(teams),(set(teams)-set(players),set(players)-set(teams))
 coaches={}
 for row in load_csv('dados_restritos/treinadores_copa_2026.csv'):
  name=COACH_NAME.get(row['Seleção'],row['Seleção'])
  if name in coaches:raise ValueError('Treinador duplicado: '+name)
  coaches[name]=row
 assert set(coaches)==set(teams),(set(teams)-set(coaches),set(coaches)-set(teams))
 scores={}; goalies={}; breakdown={}
 for team in teams:
  p=players[team]
  def top(label,count):
   return sorted((x for x in p if x['Posição'].lower().startswith(label.lower())),key=lambda x:float(x['Rating']),reverse=True)[:count]
  g,d,m,a=top('Gol',1),top('Def',5),top('Mei',num_midfield),top('Ata',5)
  if min(map(len,(g,d,m,a))) == 0:raise ValueError('Falta posicao para '+team)
  roster=g+d+m+a
  avg=lambda arr,col:sum(float(x[col]) for x in arr)/len(arr)
  v1=.1*avg(g,'Rating')+.3*avg(d,'Rating')+.3*avg(m,'Rating')+.3*avg(a,'Rating')
  v5=avg(sorted(roster,key=lambda x:float(x['Rating']),reverse=True)[:3],'Rating')
  v6=avg(roster,'Potencial')
  v2=float(coaches[team]['CA'])/2
  v3=101-ranks.get(team,50)
  scores[team]=.50*v1+.10*v6+.10*v2+.15*v3+.15*v5
  goalies[team]=float(g[0]['Rating'])
  breakdown[team]={'score':scores[team],'nota_goleiro':goalies[team],
     'v1':v1,'v2':v2,'v3':v3,'v5':v5,'v6':v6,'quantidade_jogadores':len(roster)}
 assert len(scores)==48 and all(x>0 for x in scores.values())
 return groups,ranks,scores,goalies,breakdown

def annex_lookup():
 rows=(BASE/'dados'/'_annex_c_2026.txt').read_text(encoding='utf-8').split()
 assert len(rows)==495 and len(set(''.join(sorted(r)) for r in rows))==495
 assert all(len(row)==8 and len(set(row))==8 for row in rows)
 assert set(''.join(sorted(x)) for x in combinations('ABCDEFGHIJKL',8)) == set(''.join(sorted(r)) for r in rows)
 return {''.join(sorted(row)): dict(zip(ANNEX_WINNERS,row)) for row in rows}

def poisson_probs(sa,sb):
 # Distribuicao exata (ate cauda numericamente desprezivel), sem Monte Carlo.
 s_a=[exp(-sa)];s_b=[exp(-sb)]
 for k in range(1,40):s_a.append(s_a[-1]*sa/k);s_b.append(s_b[-1]*sb/k)
 A,E,B=0.,0.,0.
 for i,x in enumerate(s_a):
  for j,y in enumerate(s_b):
   if i>j:A+=x*y
   elif i==j:E+=x*y
   else:B+=x*y
 total=A+E+B
 return (A/total,E/total,B/total)

class Tournament:
 def __init__(self, rng, groups, ranks, scores, goalies, lookup,extra_time=True):
  self.rng=rng;self.groups=groups;self.ranks=ranks;self.scores=scores;self.goalies=goalies;self.lookup=lookup;self.extra_time=extra_time
  self.host_bonus=0.1  # peso original v4
  self.penalties=0;self.over_90=0;self.extra_time_games=0;self.penalties_by_round=Counter()
 def lambdas(self,a,b):
  # mantem parametro original: local=100, neutro=50
  sa=self.scores[a]+self.host_bonus*(100 if a in HOSTS else 50)
  sb=self.scores[b]+self.host_bonus*(100 if b in HOSTS else 50)
  return (1.35*sa/sb,1.35*sb/sa)
 def play(self,a,b,knockout=False,phase=''):
  la,lb=self.lambdas(a,b)
  ga=int(self.rng.poisson(la));gb=int(self.rng.poisson(lb))
  if not knockout:return ga,gb,None
  self.over_90+=1
  if ga==gb and self.extra_time:
   self.extra_time_games+=1
   ga+=int(self.rng.poisson(la/3));gb+=int(self.rng.poisson(lb/3))
  if ga==gb:
   self.penalties+=1;self.penalties_by_round[phase]+=1
   mix=.5*self.scores[a]/(self.scores[a]+self.scores[b])+.5*self.goalies[a]/(self.goalies[a]+self.goalies[b])
   # 20% puro acaso + 80% habilidade. P(A)+P(B)=1.
   p_a=.2*.5+.8*mix
   assert 0<=p_a<=1
   winner=a if self.rng.random()<p_a else b
  else:winner=a if ga>gb else b
  return ga,gb,winner
 def rank_group(self,teamlist,matches):
  stats={t:{'pts':0,'gf':0,'ga':0} for t in teamlist}
  for a,b,ga,gb in matches:
   stats[a]['gf']+=ga;stats[a]['ga']+=gb
   stats[b]['gf']+=gb;stats[b]['ga']+=ga
   stats[a]['pts']+=3 if ga>gb else 1 if ga==gb else 0
   stats[b]['pts']+=3 if gb>ga else 1 if ga==gb else 0
  def h2h_key(t,ties):
   pt=gf=ga=0
   for a,b,x,y in matches:
    if a in ties and b in ties:
     if t==a:gf+=x;ga+=y;pt+=3 if x>y else 1 if x==y else 0
     elif t==b:gf+=y;ga+=x;pt+=3 if y>x else 1 if x==y else 0
   return (pt,gf-ga,gf)
  def sort_tie(tied, depth=0):
   # em pontos, FIFA: confronto direto, saldo e gols no confronto direto;
   # empates residuais: reavaliacao entre equipes restantes (quando separar)
   if len(tied)==1:return tied
   vals={t:h2h_key(t,set(tied)) for t in tied}
   by=defaultdict(list)
   for t in tied:by[vals[t]].append(t)
   if len(by)>1:
    seq=[]
    for key in sorted(by,reverse=True):
     subgroup=by[key]
     seq.extend(sort_tie(subgroup,depth+1) if len(subgroup)<len(tied) else subgroup)
    return seq
   # Sem dados de fair play: ranking FIFA original como substituto
   return sorted(tied,key=lambda t:(-(stats[t]['gf']-stats[t]['ga']),-stats[t]['gf'],self.ranks.get(t,50),t))
  bypoints=defaultdict(list)
  for t in teamlist:bypoints[stats[t]['pts']].append(t)
  sortedteams=[]
  for points in sorted(bypoints,reverse=True):sortedteams+=sort_tie(bypoints[points])
  for t in stats:stats[t]['gd']=stats[t]['gf']-stats[t]['ga']
  return sortedteams,stats
 def run_one(self,group_pairs):
  table={};standings={};third=[]
  for g,teams in self.groups.items():
   matches=[]
   for a,b in group_pairs[g]:
    x,y,_=self.play(a,b)
    matches.append((a,b,x,y))
   position,stat=self.rank_group(teams,matches)
   standings[g]=position
   table.update(stat)
   third.append((g,position[2]))
  # best thirds: pontos, saldo, gols marcados, ranking FIFA aproximacao do fair play
  third.sort(key=lambda x:(-table[x[1]]['pts'],-table[x[1]]['gd'],-table[x[1]]['gf'],self.ranks.get(x[1],50),x[0]))
  thirdgroups=''.join(sorted(g for g,_ in third[:8]))
  placement=self.lookup[thirdgroups]
  rank_slots={f'1{g}':a[0] for g,a in standings.items()}
  rank_slots.update({f'2{g}':a[1] for g,a in standings.items()})
  rank_slots.update({f'3{winner}':standings[third_group][2] for winner,third_group in placement.items()})
  qualifying=set(a[0] for a in standings.values())|set(a[1] for a in standings.values())|set(t for _,t in third[:8])
  assert len(qualifying)==32 and len(rank_slots)==32
  flags={t:set() for t in self.scores}
  for t in qualifying:flags[t].add('R32')
  for g,teams in standings.items():
   flags[teams[0]].add('grupo_primeiro');flags[teams[1]].add('grupo_segundo')
  for _,t in third[:8]:flags[t].add('grupo_terceiro_classificado')
  knockout_winners={};losers={}
  def round_(schedule,level,is_r32=False):
   for n,(u,v) in schedule.items():
    a=rank_slots[u] if is_r32 else knockout_winners[u]
    b=rank_slots[v] if is_r32 else knockout_winners[v]
    assert a!=b,(n,a,b)
    _,_,winner=self.play(a,b,True,level)
    knockout_winners[n]=winner
    losers[n]=b if winner==a else a
    flags[winner].add({'R32':'R16','R16':'QF','QF':'SF','SF':'Final'}[level])
  round_(R32,'R32',True);round_(R16,'R16');round_(QF,'QF');round_(SF,'SF')
  # M104 final e M103 bronze
  _,_,champ=self.play(knockout_winners[101],knockout_winners[102],True,'Final')
  _,_,bronze=self.play(losers[101],losers[102],True,'3o lugar')
  flags[champ].add('Campeao');flags[bronze].add('Terceiro_lugar')
  return flags


def group_fixtures(groups,results):
 pairs=defaultdict(list)
 teams_groups={t:g for g,gg in groups.items() for t in gg}
 for row in results:
  if row['Fase']!='Grupos':continue
  a=REAL_NAME.get(row['Mandante']);b=REAL_NAME.get(row['Visitante'])
  if a is None or b is None:raise ValueError('Nome resultado desconhecido: '+str(row))
  assert teams_groups[a]==teams_groups[b]
  pairs[teams_groups[a]].append((a,b))
 for group,match in pairs.items():
  assert len(match)==6,(group,match)
  assert set(map(frozenset,match))==set(map(frozenset,combinations(groups[group],2))),(group,match)
 return pairs

def assess_matches(tourn,results):
 sum_brier=0.;correct=0;metrics=defaultdict(lambda:{'partidas':0,'acertos':0,'brier_soma':0.0})
 lines=[]
 for row in results:
  a=REAL_NAME[row['Mandante']];b=REAL_NAME[row['Visitante']]
  la,lb=tourn.lambdas(a,b)
  pa,pe,pb=poisson_probs(la,lb)
  x=int(row['Gols_Mandante']);y=int(row['Gols_Visitante'])
  truth=(1,0,0) if x>y else ((0,1,0) if x==y else (0,0,1))
  pred=max(range(3),key=lambda j:(pa,pe,pb)[j]);obs=truth.index(1)
  hit=int(pred==obs)
  bs=sum((p-t)**2 for p,t in zip((pa,pe,pb),truth))
  sum_brier+=bs;correct+=hit
  stat=metrics[row['Fase']];stat['partidas']+=1;stat['acertos']+=hit;stat['brier_soma']+=bs
  lines.append({'fase':row['Fase'],'mandante':a,'visitante':b,'gols_mandante':x,'gols_visitante':y,
      'prob_mandante':round(pa*100,4),'prob_empate':round(pe*100,4),'prob_visitante':round(pb*100,4),
      'acerto':hit,'brier':round(bs,6)})
 return {'n':len(results),'acertos':correct,'acuracia':correct/len(results),'brier':sum_brier/len(results),'por_fase':metrics,'jogos':lines}

def write_csv(path,rows,header=None):
 if header is None:header=list(rows[0])
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=header);w.writeheader();w.writerows(rows)

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--simulacoes',type=int,default=10000)
 p.add_argument('--semente',type=int,default=20261109)
 p.add_argument('--meio-campistas',type=int,choices=(5,6),default=5)
 p.add_argument('--sem-prorrogacao',action='store_true')
 p.add_argument('--sufixo',default='')
 args=p.parse_args()
 if args.simulacoes<1:raise ValueError('Simulacoes deve ser >=1')
 groups,ranks,scores,goalies,breakdown=load_model(args.meio_campistas)
 lookup=annex_lookup()
 results=load_csv('dados/resultados_copa_2026.csv');assert len(results)==104
 pairs=group_fixtures(groups,results)
 rng=np.random.default_rng(args.semente)
 model=Tournament(rng,groups,ranks,scores,goalies,lookup,extra_time=not args.sem_prorrogacao)
 assessment=assess_matches(model,results)
 totals={t:Counter() for t in scores}
 for n in range(args.simulacoes):
  res=model.run_one(pairs)
  for t,events in res.items():totals[t].update(events)
  if (n+1)%10000==0:print('simulacoes concluidas:',n+1,flush=True)
 stages=['R32','R16','QF','SF','Final','Campeao']
 rows=[]
 for t in scores:
  v=totals[t]
  rows.append({'Selecao':t,'Score':round(scores[t],3),'Goleiro':round(goalies[t],2),
   'P_16avos_pct':round(v['R32']*100/args.simulacoes,3),
   'P_oitavas_pct':round(v['R16']*100/args.simulacoes,3),
   'P_quartas_pct':round(v['QF']*100/args.simulacoes,3),
   'P_semifinal_pct':round(v['SF']*100/args.simulacoes,3),
   'P_final_pct':round(v['Final']*100/args.simulacoes,3),
   'P_campeao_pct':round(v['Campeao']*100/args.simulacoes,3),
   'P_3o_lugar_pct':round(v['Terceiro_lugar']*100/args.simulacoes,3),
   'P_1o_grupo_pct':round(v['grupo_primeiro']*100/args.simulacoes,3),
   'P_2o_grupo_pct':round(v['grupo_segundo']*100/args.simulacoes,3),
   'P_3o_grupo_classificado_pct':round(v['grupo_terceiro_classificado']*100/args.simulacoes,3)})
 rows.sort(key=lambda r:(-r['P_campeao_pct'],-r['P_final_pct']))
 suffix=('_'+args.sufixo) if args.sufixo else ''
 output_dir=BASE/'resultados'/'gerados'
 output_dir.mkdir(parents=True,exist_ok=True)
 write_csv(output_dir/f'probabilidades_fases_copa_2026{suffix}.csv',rows)
 write_csv(output_dir/f'validacao_104_partidas_corrigida{suffix}.csv',assessment['jogos'])
 write_csv(output_dir/f'scores_selecoes{suffix}.csv',[{'Selecao':t,**d} for t,d in breakdown.items()])
 report={
  'proveniencia':'As previsoes por jogo nao condicionam em resultados reais; partida real somente para validacao retrospectiva.',
  'n_simulacoes':args.simulacoes,'semente':args.semente,'n_meio_campistas':args.meio_campistas,
  'usa_prorrogacao':model.extra_time,'formula_penaltis':'P(A)=0.20*0.50+0.80*(0.5*Score_A/(Score_A+Score_B)+0.5*GK_A/(GK_A+GK_B))',
  'p_penaltis_estimado_apos_120_min_por_confronto': model.penalties/model.over_90,
  'n_jogos_mata_mata_total':model.over_90,'n_prorrogacoes':model.extra_time_games,'n_disputas_penaltis':model.penalties,
  'penaltis_por_fase':dict(model.penalties_by_round),
  'validacao_recalculada':{'n_partidas':assessment['n'],'acertos':assessment['acertos'],
     'acuracia':assessment['acuracia'],'brier':assessment['brier'],
     'por_fase':{k:{'partidas':v['partidas'],'acertos':v['acertos'],'brier':v['brier_soma']/v['partidas']} for k,v in assessment['por_fase'].items()}},
  'somas_de_probabilidades_por_etapa_pct': {c:round(sum(row[c] for row in rows),4) for c in ('P_16avos_pct','P_oitavas_pct','P_quartas_pct','P_semifinal_pct','P_final_pct','P_campeao_pct','P_3o_lugar_pct')},
  'principais_equipas':rows[:12],
  'limites':'Desempates disciplinares (fair play) nao disponiveis; como fallback, ranking original de FIFA do algoritmo. Parametros heurísticos nao recalibrados. Modelo simplifica capacidade fixa e fator casa sem sede de jogo. Prorrogacao modeled with lambda/3 independent Poisson. Uso de resultados reais para validacao inclui placares que podem envolver prorrogacao, verificar.',
  'fontes_regulamento':['https://digitalhub.fifa.com/m/636f5c9c6f29771f/original/FWC2026_regulations_EN.pdf']
 }
 (output_dir/f'relatorio_simulacao_2026{suffix}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 for row in rows[:14]:print(f'{row["Selecao"]:19} R32 {row["P_16avos_pct"]:7.2f}% Final {row["P_final_pct"]:6.2f}% Campeao {row["P_campeao_pct"]:6.2f}%')
 print('Validacao 104 jogos corrigida:',assessment['acertos'], '/', assessment['n'],'Brier',round(assessment['brier'],5))
 print('SUMS:',report['somas_de_probabilidades_por_etapa_pct'])
 print('PENAL:',model.penalties,model.over_90,round(model.penalties/model.over_90,3))

if __name__=='__main__': main()
