# This code require two inputs, 'number of agents'
# To run <python generate_files.py 100>

import random
import copy
import numpy as np
import sys


def connect_family(adj_list,family_list):
	for i in range(len(family_list)-1):
		for j in range(i+1,len(family_list)):
			adj_list[family_list[i]].append(family_list[j])
			adj_list[family_list[j]].append(family_list[i])

def write_interactions(filename,n,p,family_sizes,connected=True):

		#family_sizes is cumulative percentage
		#30% size 1 families and 70% size 4 => [0.3,0.3,0.3,1]

		size=n
		adj_list=[]
		for i in range(n):
			adj_list.append([])

		for i in range(n):
			for j in range(i+1,n):
				if random.random()<p:
					adj_list[i].append(j)
					adj_list[j].append(i)

		# f_size_max = len(family_sizes)-1
		f_size=-1
		r=random.random()
		for fs,p_f in enumerate(family_sizes):
			if r<p_f:
				f_size=fs+1
				break
		index_so_far=0
		while index_so_far+f_size<=n:
			family_list=range(index_so_far,index_so_far+f_size)
			index_so_far+=f_size
			connect_family(adj_list,family_list)
		if index_so_far<n-1:
			connect_family(adj_list,range(index_so_far,n))

		if connected:
			for i in range(n):
				if adj_list[i]==[]:
					allowed_values = list(range(0, n))
					allowed_values.remove(i)
					j = random.choice(allowed_values)
					adj_list[i].append(j)
					adj_list[j].append(i)

		for i in range(n):
			adj_list[i]=list(set(adj_list[i]))

		### Writing
		header='Agent Index:Interacting Agent Index'
		lines=[]
		for i in range(n):
			for j in adj_list[i]:
				lines.append(str(i)+':'+str(j)+'\n')
				lines.append(str(j)+':'+str(i)+'\n')

		f=open(filename,'w')
		f.write(str(len(lines))+'\n')
		f.write(header+'\n')
		for line in lines:
			f.write(line)

		dsum=0
		for i in range(n):
			dsum+=len(adj_list[i])
		average_degree=dsum/(n)
		print("Average Degree :",average_degree)

p=float(sys.argv[1])
fam_size = [0.0,0.0,0.0,1.0]
write_interactions('interactions_list1.txt',16,p,fam_size)
write_interactions('interactions_list2.txt',16,p,fam_size)
write_interactions('interactions_list3.txt',16,p,fam_size)
write_interactions('interactions_list4.txt',16,p,fam_size)
write_interactions('interactions_list5.txt',16,p,fam_size)
