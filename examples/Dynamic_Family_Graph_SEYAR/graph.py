import sys
from pyvis.network import Network


def get_graph_html(number_of_agents,interaction_file_path, outpath):
	fp = open(interaction_file_path,'r')

	num = int(fp.readline())
	fp.readline()

	ls = list(range(number_of_agents))
	net = Network()
	net.add_nodes(ls)

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
	net.show_buttons(filter_=['physics'])
	net.show(outpath)


number_of_agents = int(sys.argv[1])

get_graph_html(number_of_agents,'interactions_list1.txt','graph1.html')
get_graph_html(number_of_agents,'interactions_list2.txt','graph2.html')
get_graph_html(number_of_agents,'interactions_list3.txt','graph3.html')
get_graph_html(number_of_agents,'interactions_list4.txt','graph4.html')
get_graph_html(number_of_agents,'interactions_list5.txt','graph5.html')
print("Saved Interaction Graphs")
