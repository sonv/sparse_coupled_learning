import json
import os
import sys
import numpy as np
import networkx as nx

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from utils.graph_utils import create_low_connectivity_network, draw_wide_network
from utils.data_utils import generate_regression_data_for_experiment

from CLSolver.LinearNetwork import LinearNetwork
from CLSolver.LinearNetworkSolver import LinearNetworkSolver

import matplotlib.pyplot as plt


if __name__ == "__main__":

    np.random.seed(42)

    sources = 25
    fanouts = list(range(3, sources, 2))
    vals_dict = {}

    for fanout in fanouts:
        G, S, H, T = create_low_connectivity_network(sources, fanout)
        # draw_wide_network(G, source_nodes, hidden_layers, target_nodes)
        tri, trt, tei, tet = generate_regression_data_for_experiment()

        linNet = LinearNetwork(G)
        solver = LinearNetworkSolver(linNet)

        K, costs = solver.perform_trial(source_nodes=[0,1],
                                        target_nodes=[T[-2],T[-1]],
                                        ground_nodes=[2],
                                        in_node=tri,
                                        out_node=trt,
                                        lr=0.05,
                                        steps=150000,
                                        debug=True,
                                        every_nth=500,
                                        init_strategy="random"
                                        )
        x, y = zip(*costs)
        y = [a / y[0] for a in y]
        plt.plot(x, y, label=f"Adj Nodes: {fanout}")
        vals_dict[fanout] = costs[-1]

    plt.title("Relative Cost vs Iterations for different Fanouts")
    plt.xlabel("Iterations")
    plt.ylabel("Relative Cost")
    plt.yscale('log')
    plt.legend()
    plt.show()

    for a, b in vals_dict.items():
        print(a, "&", b)


# 3 & (150000, 0.003769317255230386)
# 5 & (150000, 0.00323353844753515)
# 7 & (150000, 0.0035081807267149556)
# 9 & (150000, 0.0032138291797051944)
# 11 & (150000, 0.003275181096251779)
# 13 & (150000, 0.003341389185842649)
# 15 & (150000, 0.0029873299338378646)
# 17 & (150000, 0.003110546813612148)
# 19 & (150000, 0.0037856266207467295)
# 21 & (150000, 0.003467669581230366)
# 23 & (150000, 0.0025103826957206506)