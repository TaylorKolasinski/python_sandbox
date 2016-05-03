# tutorial for building a simple price network with graph-tool
from __future__ import division, absolute_import, print_function
import sys
import os
from pylab import * 
from numpy.random import *  
seed(42)
from graph_tool.all import *

g = Graph()

v_age = g.new_vertex_property("int")
e_age = g.new_edge_property("int")

N = 100000

v = g.add_vertex()
v_age[v] = 0

vlist = [v]

# add edges and nodes
for i in range(1, N):
    v = g.add_vertex()
    v_age[v] = i

    i = randint(0, len(vlist))
    target = vlist[i]

    e = g.add_edge(v, target)
    e_age[e] = i

    vlist.append(target)
    vlist.append(v)

v = g.vertex(randint(0, g.num_vertices()))
while True:
    print("vertex:", int(v), "in-degree:", v.in_degree(), "out-degree:",
          v.out_degree(), "age:", v_age[v])

    if v.out_degree() == 0:
        print("Nowhere else to go... We found the main hub!")
        break

    n_list = []
    for w in v.out_neighbours():
        n_list.append(w)
    v = n_list[randint(0, len(n_list))]


g.vertex_properties["age"] = v_age
g.edge_properties["age"] = e_age

g.save("price.xml.gz")

in_hist = vertex_hist(g, "in")

y = in_hist[0]
err = sqrt(in_hist[0])
err[err >= y] = y[err >= y] - 1e-2

figure(figsize=(6,4))
errorbar(in_hist[1][:-1], in_hist[0], fmt="o", yerr=err,
        label="in")
gca().set_yscale("log")
gca().set_xscale("log")
gca().set_ylim(1e-1, 1e5)
gca().set_xlim(0.8, 1e3)
subplots_adjust(left=0.2, bottom=0.2)
xlabel("$k_{in}$")
ylabel("$NP(k_{in})$")
tight_layout()
savefig("price-deg-dist.pdf")
savefig("price-deg-dist.png")


g = load_graph("price.xml.gz")
age = g.vertex_properties["age"]

pos = sfdp_layout(g)
graph_draw(g, pos, output_size=(1000, 1000), vertex_color=[1,1,1,0],
           vertex_fill_color=age, vertex_size=1, edge_pen_width=1.2,
           vcmap=matplotlib.cm.gist_heat_r, output="price.png")
