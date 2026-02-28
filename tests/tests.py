import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from tests.statistical_tests.nonparametric_tests import friedman_aligned_ranks_test, shaffer_multitest

# Cargar resultados
ga = [r['fitness'] for r in np.load("results/elites_GA.npy", allow_pickle=True)]
aco = [r['fitness'] for r in np.load("results/elites_ACO.npy", allow_pickle=True)]
rand = [r['fitness'] for r in np.load("results/random_31.npy", allow_pickle=True)]

# Asegúrate de que todas tengan la misma longitud
assert len(ga) == len(aco) == len(rand)

# Ejecutar test
names = ["GA", "ACO", "Random"]
_, p_value, rankings, pivots = friedman_aligned_ranks_test(ga, aco, rand)

if p_value < 0.05:
    d = dict(zip(names, pivots))
    comp, _, _, adpval = shaffer_multitest(d)
    for i, apv in enumerate(adpval):
        a, b = map(str.strip, comp[i].split("vs"))
        if apv < 0.05:
            print(f"→ {a} vs {b}: Significant (p = {apv:.4f})")
        else:
            print(f"→ {a} vs {b}: Not significant")
else:
    print("→ No overall difference found between algorithms (Friedman p ≥ 0.05)")


import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tests.statistical_tests.nonparametric_tests import friedman_aligned_ranks_test, shaffer_multitest

def is_better(a,b):
  return a > b

alpha = 0.05

names = ["GA", "ACO", "Random"]
names_pos = dict(zip(names, range(len(names))))
a = [r['fitness'] for r in np.load("results/elites_GA.npy", allow_pickle=True)]
b = [r['fitness'] for r in np.load("results/elites_ACO.npy", allow_pickle=True)]
c = [r['fitness'] for r in np.load("results/random_31.npy", allow_pickle=True)]

_, p_value, rankings, pivots = friedman_aligned_ranks_test(a, b, c)

if p_value < alpha:
  d = dict(zip(names, pivots))
  comp, _, _, adpval = shaffer_multitest(d)

  g = nx.Graph()
  g.add_nodes_from([(n, {"rank": rankings[names_pos[n]]}) for n in names])

  for i, apv in enumerate(adpval):
    chunks = comp[i].split("vs")
    name_l = chunks[0].strip()
    name_r = chunks[1].strip()

    if apv >= alpha:
      g.add_edge(name_l, name_r)
else:
  g = nx.complete_graph(names)
  nx.set_node_attributes(g, 20, "rank")


import matplotlib.pyplot as plt

# Layout del grafo
pos = nx.kamada_kawai_layout(g, scale=0.5)

# Crear figura y eje explícitamente
fig, ax = plt.subplots()

# Dibujar el grafo con colores basados en el ranking
nodes = g.nodes(data=True)
node_ranks = [r["rank"] for _, r in nodes]

nx.draw_networkx(
    g, pos=pos, ax=ax,
    node_size=[r*10 for r in node_ranks],
    node_color=node_ranks,
    cmap="plasma",
    with_labels=True,
    font_color="w"
)

# Agregar barra de color correctamente
sm = plt.cm.ScalarMappable(cmap='plasma', norm=plt.Normalize(vmin=min(rankings), vmax=max(rankings)))
sm._A = []  # Requerido en algunas versiones de matplotlib
fig.colorbar(sm, ax=ax)

plt.show()
