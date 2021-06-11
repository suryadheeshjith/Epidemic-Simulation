import sys
from pyvis.network import Network
import networkx as nx

def get_average_degree(interaction_file_path):
	fp = open(interaction_file_path,'r')

	num = int(fp.readline())
	fp.readline()

	ls = list(range(1000))
	net = nx.Graph()
	net.add_nodes_from(ls)

	for i in range(num):
		line = fp.readline()
		line = line[:-1]
		a,b = line.split(':')
		# if(a in ['34','4','44','25','41'] or b in ['34','4','44','25','41']):
		# 	net.add_edge(int(a),int(b), width=5)
		#
		# else:
		# 	net.add_edge(int(a),int(b))
		net.add_edge(int(a),int(b))

	degrees = net.degree()
	n = len(degrees)
	print(n)
	sum_of_edges = sum([degree for id,degree in degrees])
	print(sum_of_edges)
	return int(sum_of_edges/n)
	# net.show_buttons(filter_=['physics'])
	# net.show(outpath)


print(get_average_degree('interactions_list1.txt'))
