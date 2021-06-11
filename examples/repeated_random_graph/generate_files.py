# This code require two inputs, 'number of agents'
# To run <python generate_files.py 100>

import random
import copy
import numpy as np
import sys

def write_agents(filename,n):
	info_dict={}
	#ID enumerates from 0 to n-1
	header='Agent Index:Age:Blood Group:Fear'
	info_dict['Age']=['0-19','20-59','60+']
	info_dict['Blood Group']=['A','O','Other']
	info_dict['Fear']=['0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9']

	f=open(filename,'w')
	f.write(str(n)+'\n')
	f.write(header+'\n')

	for i in range(n):
		f.write(str(i))
		for j in info_dict.keys():
			f.write(':'+random.choice(info_dict[j]))
		f.write('\n')


def write_interactions(filename,no_agents,p):
	info_dict={}
	#Agent ID enumerates from 0 to n-1
	header='Agent Index:Interacting Agent Index'
	lines=[]
	for i in range(no_agents-1):
		for j in range(i+1,no_agents):
			if random.random()<p:
				lines.append(str(i)+':'+str(j)+'\n')
				lines.append(str(j)+':'+str(i)+'\n')

	f=open(filename,'w')
	f.write(str(len(lines))+'\n')
	f.write(header+'\n')

	for line in lines:
		f.write(line)
