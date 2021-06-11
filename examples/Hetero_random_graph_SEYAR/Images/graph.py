
import sys
from pyvis.network import Network
import networkx as nx
import random

def get_graph_html(number_of_agents,interaction_file_path, outpath):
	fp = open(interaction_file_path,'r')

	num = int(fp.readline())
	fp.readline()

	ls = list(range(number_of_agents))
	net = Network()
	# G = nx.cycle_graph(15)
	color_list = ['gray']*number_of_agents
	# for i in range(number_of_agents):
	# 	color = random.choice(['gray','green','blue','black'])
	# 	color_list.append(color)
	net.add_nodes(ls,title=['']*number_of_agents,color=color_list)
	# G.add_nodes_from(ls,color=color_list)

	for i in range(num):
		line = fp.readline()
		line = line[:-1]
		a,b = line.split(':')
		print(a,b)
		# if(a in ['34','4','44','25','41'] or b in ['34','4','44','25','41']):
		# 	net.add_edge(int(a),int(b), width=5)
		#
		# else:
		# 	net.add_edge(int(a),int(b))
		# G.add_edge(int(a),int(b))
		net.add_edge(int(a),int(b))

	# net.from_nx(G)
	net.show_buttons(filter_=['physics'])
	net.show(outpath)


number_of_agents = int(sys.argv[1])

get_graph_html(number_of_agents,'interactions_list.txt','graph.html')
print("Saved Interaction Graphs")
