import networkx as nx
from scipy import stats
from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction
import sys
# Calculates binomial coefficient (n over k)
def nCk(n,k):
  return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1) )

# Read the network in form of edge list, unweighted and undirected
net=nx.read_edgelist(sys.argv[1], nodetype=int)

# calculate the transitivity of the network
C=nx.transitivity(net)
# Make dictionary nodeID:degree
d=dict(nx.degree(net))

# The branching is calculated as P2/P1
# The intermodular connectivity as P3/P2
suma1=0
P2=0
for key in d:
    suma1+=int(d[key])
    P2+=nCk(int(d[key]),2)
P1=suma1*0.5
C3=C*P2/3.0
suma=0
for u,v in net.edges():
    suma=suma+(d[u]-1)*(d[v]-1)

P3=suma-3*C3

P21=float(P2)/float(P1)
P32=float(P3)/float(P2)
# Conditions for assortativity and disassortativity
if P32 + C > P21:
    print("The network is assortative with r = "+str(nx.degree_assortativity_coefficient(net)))
elif P32 + C < P21:
    print("The network is disassortative with r = "+str(nx.degree_assortativity_coefficient(net)))
else:
    print("The network is neutral with r = "+str(nx.degree_assortativity_coefficient(net)))

print("The relative branching is: " + str(P21))
print("The intermodular connectivity is: " + str(P32))
print("The transitivity is: " + str(C))
