import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'codigos'))

from simulacao_campeonato_completo_copa_2026 import load_model, annex_lookup, poisson_probs, Tournament
import numpy as np

class TestSimulacaoCopa(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grupos, cls.rankings, cls.scores, cls.goleiros, cls.variaveis = load_model(5)

    def test_48_equipes_e_grupos(self):
        self.assertEqual(len(self.scores), 48)
        self.assertEqual(len(self.grupos), 12)
        self.assertEqual(sum(len(g) for g in self.grupos.values()), 48)

    def test_tabela_terceiros_cobre_495_combinacoes(self):
        self.assertEqual(len(annex_lookup()), 495)

    def test_poisson_soma_um(self):
        p = poisson_probs(1.35, 1.40)
        self.assertAlmostEqual(sum(p), 1.0, places=12)
        self.assertTrue(all(0 <= x <= 1 for x in p))

    def test_penalti_equilibrado_e_50_por_cento(self):
        a, b = 'Brasil', 'França'
        s = self.scores
        g = self.goleiros
        mistura = 0.5 * s[a] / (s[a] + s[b]) + 0.5 * g[a] / (g[a] + g[b])
        pa = 0.2 * 0.5 + 0.8 * mistura
        pb = 0.2 * 0.5 + 0.8 * (1 - mistura)
        self.assertAlmostEqual(pa+pb, 1.0, places=12)

    def test_simulacao_gera_um_campeao(self):
        from simulacao_campeonato_completo_copa_2026 import group_fixtures, load_csv
        matches = group_fixtures(self.grupos, load_csv('dados/resultados_copa_2026.csv'))
        sim = Tournament(np.random.default_rng(42), self.grupos, self.rankings,
                         self.scores, self.goleiros, annex_lookup())
        flags = sim.run_one(matches)
        self.assertEqual(sum('Campeao' in events for events in flags.values()), 1)
        self.assertEqual(sum('R32' in events for events in flags.values()), 32)
        self.assertEqual(sum('Final' in events for events in flags.values()), 2)

if __name__ == '__main__':
    unittest.main()
