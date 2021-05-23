import sys
sys.path.insert(1, '../src/')
import ReadFile
import pickle
import World
import Model
import importlib.util
import os.path as osp
import policy_generator as pg
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
import random
import Testing_Policy
import Lockdown_Policy


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_config_path(path):
    config_filepath=osp.join(path,'config.txt')
    return config_filepath

def get_model(beta,gamma):
    def probabilityOfInfection_fn(p_infected_states_list,contact_agent,c_dict,current_time_step):
    	if contact_agent.state=='Infected':
    		return beta  #This is the probability of getting infected from contact in a time step isf contact is infected
    	return 0 # If contact is not infected then the probability of them infecting you is 0

    class UserModel(Model.StochasticModel):
        def __init__(self):
            individual_types=['Susceptible','Infected','Recovered']	#These are the states that will be used by the compartmental model
            infected_states=['Infected']	#These are the states that can infect
            state_proportion={				#This is the starting proportions of each state
    							'Susceptible':0.99,
    							'Infected':0.01,
    							'Recovered':0
    						}
            Model.StochasticModel.__init__(self,individual_types,infected_states,state_proportion)  #We use the inbuilt model in the package
            self.set_transition('Susceptible', 'Infected', self.p_infection(None,probabilityOfInfection_fn))	#Adding S-> I transition which is based on probability)fInfection_fn
            self.set_transition('Infected', 'Recovered', self.p_standard(gamma))	#Adding the I->R transition

    return UserModel()

def make_graph(n,p):
    def write_agents(filename,n):
    	header='Agent Index'

    	f=open(filename,'w')
    	f.write(str(n)+'\n')
    	f.write(header+'\n')

    	for i in range(n):
    		f.write(str(i)+'\n')

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

    write_agents('agents.txt',n)
    write_interactions('interactions_list.txt',n,p)

def get_policy(example_path):
    Generate_policy = module_from_file("Generate_policy", osp.join(example_path,'Generate_policy.py'))
    policy_list, event_restriction_fn=Generate_policy.generate_policy()
    return policy_list, event_restriction_fn


def run_simulation(test_cost,fp_cost,quarantine_cost,infection_cost,n,p,beta,gamma,napt,ntpa,testing_gap,tests_per_period,turnaround_time,restriction_time,fn,fp):

    testing_gap+=1

    config_filename = get_config_path('')

    # Read Config file using ReadFile.ReadConfiguration
    config_obj=ReadFile.ReadConfiguration(config_filename)

    agents_filename='agents.txt'
    interactions_files_list=['interactions_list.txt']
    locations_filename=None
    events_files_list=[]

    # User Model
    model=get_model(beta, gamma)

    ##########################################################################################

    policy_list=[]

	# Group/Pool Testing
    def testing_fn(timestep):
        if timestep%testing_gap==0:
            return tests_per_period*napt/ntpa
        return 0

    Pool_Testing = Testing_Policy.Test_Policy(testing_fn)
    Pool_Testing.add_machine('Simple_Machine', test_cost, fp, fn, turnaround_time,1000,1)
    Pool_Testing.set_register_agent_testtube_func(Pool_Testing.random_agents(napt,ntpa))
    policy_list.append(Pool_Testing)

    ATP = Lockdown_Policy.agent_policy_based_lockdown("Testing",["Positive"],lambda x:True,restriction_time)
    policy_list.append(ATP)

    def event_restriction_fn(agent,event_info,current_time_step):
        return False

    ###############################################################################################

    world_obj=World.World(config_obj,model,policy_list,event_restriction_fn,agents_filename,interactions_files_list,locations_filename,events_files_list)
    # world_obj.simulate_worlds(plot=True)
    tdict, total_infection, total_quarantined_days, wrongly_quarantined_days, total_test_cost = world_obj.simulate_worlds(plot=False)
    cost = total_infection*infection_cost+total_quarantined_days*quarantine_cost+total_test_cost+world_obj.total_false_positives*fp_cost
    return cost

def opt_pool(test_cost,fp_cost,quarantine_cost,infection_cost,n,p,beta,gamma,testing_gap,tests_per_period,turnaround_time,restriction_time,fn,fp):

    pool_strats={(1,1):'red',(2,1):'blue',(3,2):'green',(4,2):'yellow',(5,2):'orange',(5,3):'brown',(6,2):'black',(6,3):'cyan'}

    opt_cost=np.inf
    opt_pool=None
    for (napt,ntpa) in pool_strats.keys():
        cost =run_simulation(test_cost,fp_cost,quarantine_cost,infection_cost,n,p,beta,gamma,napt,ntpa,testing_gap,tests_per_period,turnaround_time,restriction_time,fn,fp)
        if cost < opt_cost:
            opt_cost= cost
            opt_pool=(napt,ntpa)

    return opt_pool,opt_cost

def plot(X,Y,opt_strats,xlabel,ylabel,title):
    pool_strats={(1,1):'red',(2,1):'blue',(3,2):'green',(4,2):'yellow',(5,2):'orange',(5,3):'brown',(6,2):'black',(6,3):'cyan'}

    f=open('results.txt','a')
    f.write("***"+title+"***\n")
    f.write(xlabel+str(X)+'\n')
    f.write(ylabel+str(Y)+'\n')
    f.write(str(opt_strats)+'\n')
    f.close()
    print('')
    print("***"+title+"***")
    print(xlabel,X)
    print(ylabel,Y)
    print(opt_strats)

def fn_fp(test_cost,fp_cost,quarantine_cost,infection_cost):
    X=[]
    Y=[]
    opt_strats=[]

    for i in range(10):
        print("Progress left :"+str(100-i*10)+"%")
        fn=i*0.01
        for j in range(10):
            fp=j*0.01
            opt_strat,_=opt_pool(test_cost,fp_cost,quarantine_cost,infection_cost,n,p,beta,gamma,testing_gap,tests_per_period,turnaround_time,restriction_time,fn,fp)
            X.append(fn)
            Y.append(fp)
            opt_strats.append(opt_strat)

    plot(X,Y,opt_strats,'False negative rate','False positive rate','Optimal pooling strategy given FN and FP')

def beta_gamma(test_cost,fp_cost,quarantine_cost,infection_cost):
    X=[]
    Y=[]
    opt_strats=[]

    for i in range(10):
        print("Progress left :"+str(100-i*10)+"%")
        beta=(i*5+5)/100
        for j in range(10):
            gamma=(j*3+2)/100
            opt_strat,_=opt_pool(test_cost,fp_cost,quarantine_cost,infection_cost,n,p,beta,gamma,testing_gap,tests_per_period,turnaround_time,restriction_time,fn,fp)
            X.append(beta)
            Y.append(gamma)
            opt_strats.append(opt_strat)

    plot(X,Y,opt_strats,'Rate of Infection(Beta)','Rate of Recovery(Gamma)','Optimal pooling strategy given Beta and Gamma')

def turnaround_restriction(test_cost,fp_cost,quarantine_cost,infection_cost):
    X=[]
    Y=[]
    opt_strats=[]

    for i in range(5):
        print("Progress left :"+str(100-i*20)+"%")
        turnaround_time=i
        for j in range(10):
            restriction_time=j+3
            opt_strat,_=opt_pool(test_cost,fp_cost,quarantine_cost,infection_cost,n,p,beta,gamma,testing_gap,tests_per_period,turnaround_time,restriction_time,fn,fp)
            X.append(turnaround_time)
            Y.append(restriction_time)
            opt_strats.append(opt_strat)

    plot(X,Y,opt_strats,'Test result turnaround time','Agent restriction time','Optimal pooling strategy given Turnaround and Restriction time')

def n_p(test_cost,fp_cost,quarantine_cost,infection_cost):
    X=[]
    Y=[]
    opt_strats=[]

    for i in range(5):
        print("Progress left :"+str(100-i*20)+"%")
        n=i*500+500
        for j in range(6):
            p=j*0.001+0.0005
            opt_strat,_=opt_pool(test_cost,fp_cost,quarantine_cost,infection_cost,n,p,beta,gamma,testing_gap,tests_per_period,turnaround_time,restriction_time,fn,fp)
            X.append(n)
            Y.append(p)
            opt_strats.append(opt_strat)

    plot(X,Y,opt_strats,'Number of agents (n)','Probability of Edge (p)','Optimal pooling strategy given G(n,p) ER random graph')

def gap_tests(test_cost,fp_cost,quarantine_cost,infection_cost):
    X=[]
    Y=[]
    opt_strats=[]

    for i in range(5):
        print("Progress left :"+str(100-i*20)+"%")
        testing_gap=i
        for j in range(10):
            tests_per_period=j*20+50
            opt_strat,_=opt_pool(test_cost,fp_cost,quarantine_cost,infection_cost,n,p,beta,gamma,testing_gap,tests_per_period,turnaround_time,restriction_time,fn,fp)
            X.append(testing_gap)
            Y.append(tests_per_period)
            opt_strats.append(opt_strat)

    plot(X,Y,opt_strats,'Gap between testing periods','Tests per testing period','Optimal pooling strategy given number of tests and period for testing')


n=1000
p=0.003
beta=0.25
gamma=0.2
testing_gap=1
tests_per_period=90
turnaround_time=0
restriction_time=5
fn=0.1
fp=0.1

f=open('results.txt','w')
f.write("Paramters\n")
f.write('n:'+str(n)+'\n')
f.write('p:'+str(p)+'\n')
f.write('beta:'+str(beta)+'\n')
f.write('gamma:'+str(gamma)+'\n')
f.write('testing_gap:'+str(testing_gap)+'\n')
f.write('tests_per_period:'+str(tests_per_period)+'\n')
f.write('turnaround_time:'+str(turnaround_time)+'\n')
f.write('restriction_time:'+str(restriction_time)+'\n')
f.write('fn:'+str(fn)+'\n')
f.write('fp:'+str(fp)+'\n')
f.write('\n'+'\n')
f.close()

if __name__=="__main__":

    test_cost=1
    fp_cost=1
    quarantine_cost=3
    infection_cost=5

    fn_fp(test_cost,fp_cost,quarantine_cost,infection_cost)
    beta_gamma(test_cost,fp_cost,quarantine_cost,infection_cost)
    turnaround_restriction(test_cost,fp_cost,quarantine_cost,infection_cost)
    gap_tests(test_cost,fp_cost,quarantine_cost,infection_cost)
    # n_p(test_cost,fp_cost,quarantine_cost,infection_cost)
