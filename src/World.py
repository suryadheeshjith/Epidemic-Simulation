import random
import copy
import sys
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import Agent
import Simulate
import math
import ReadFile
from Testing_Policy import Test_Policy

def get_accumulated_result(agent,history):

    total_false_positive = 0
    total_positive=0

    indx = len(history)-1
    last_time_step = history[indx].time_step

    while(indx>=0):
        flag=0
        while(indx>=0 and history[indx].time_step==last_time_step):
            if(history[indx].result == "Negative"):
                flag=1
                indx-=1
                break

            indx-=1

        if flag==0:
            total_positive+=1
        if(flag==0 and agent.states[last_time_step]!="Infected"):
            total_false_positive+=1
        try:
            last_time_step = history[indx].time_step
        except:
            break

    return total_false_positive,total_positive

class World():
    def __init__(self,config_obj,model,policy_list,event_restriction_fn,agents_filename,interactionFiles_list,locations_filename,eventFiles_list):
        self.config_obj=config_obj
        self.policy_list=policy_list
        self.event_restriction_fn=event_restriction_fn
        self.agents_filename=agents_filename
        self.locations_filename=locations_filename
        self.model=model
        self.interactionFiles_list=interactionFiles_list
        self.eventFiles_list=eventFiles_list

        # Costs
        self.total_quarantined_days = 0
        self.wrongly_quarantined_days = 0
        self.total_infection = 0
        self.total_machine_cost = 0
        self.total_positives = 0
        self.total_agents_tests = 0
        self.total_false_positives = 0
        self.total_positive_pools=0


    def one_world(self):

        time_steps = self.config_obj.time_steps

        #Initialize agents
        agents_obj=ReadFile.ReadAgents(self.agents_filename,self.config_obj)

        #Intialize locations
        locations_obj=ReadFile.ReadLocations(self.locations_filename,self.config_obj)

        sim_obj= Simulate.Simulate(self.config_obj,self.model,self.policy_list,self.event_restriction_fn,agents_obj,locations_obj)
        sim_obj.onStartSimulation()

        for i in range(time_steps):
            if self.interactionFiles_list==[] or self.interactionFiles_list==None:
                interactions_filename=None
            else:
                interactions_filename=self.interactionFiles_list[i%len(self.interactionFiles_list)]
            if self.eventFiles_list==[] or self.eventFiles_list==None:
                events_filename=None
            else:
                events_filename=self.eventFiles_list[i%len(self.eventFiles_list)]

            sim_obj.onStartTimeStep(interactions_filename,events_filename,i)
            sim_obj.handleTimeStepForAllAgents()
            sim_obj.endTimeStep()

        end_state, machine_cost=sim_obj.endSimulation()
        total_quarantined_days = 0
        wrongly_quarantined_days = 0
        total_positives = 0
        total_false_positives = 0

        for policy in self.policy_list:
            if(isinstance(policy,Test_Policy)):
                self.total_positive_pools+=policy.positive_pools


        for agent in agents_obj.agents.values():
            for truth in agent.quarantine_list:
                if(truth=="Right"):
                    total_quarantined_days+=1
                elif(truth=="Wrong"):
                    total_quarantined_days+=1
                    wrongly_quarantined_days+=1

            history = agent.get_policy_history("Testing")
            if(len(history)):
                t_f_p,t_p = get_accumulated_result(agent,history)
                total_false_positives+=t_f_p
                self.total_positives+=t_p



        self.total_quarantined_days+=total_quarantined_days
        self.wrongly_quarantined_days+=wrongly_quarantined_days
        self.total_infection+=len(agents_obj.agents)-end_state["Susceptible"][-1]
        self.total_machine_cost+=machine_cost
        self.total_false_positives+=total_false_positives

        return end_state, agents_obj, locations_obj

    #Average number time series
    def average(self,tdict,number):
        for k in tdict.keys():
            l=tdict[k]
            for i in range(len(l)):
                tdict[k][i]/=number

        return tdict

    #Averages multiple simulations and plots a single plot
    def simulate_worlds(self,plot=True, extra=False):

        tdict={}
        for state in self.model.individual_state_types:
            tdict[state]=[0]*(self.config_obj.time_steps+1)

        for i in range(self.config_obj.worlds):
            sdict,_,_ = self.one_world()
            for state in self.model.individual_state_types:
                for j in range(len(tdict[state])):
                    tdict[state][j]+=sdict[state][j]

        tdict=self.average(tdict,self.config_obj.worlds)
        self.total_infection/=self.config_obj.worlds
        self.total_quarantined_days/=self.config_obj.worlds
        self.wrongly_quarantined_days/=self.config_obj.worlds
        self.total_machine_cost/=self.config_obj.worlds
        self.total_positives/=self.config_obj.worlds
        self.total_false_positives/=self.config_obj.worlds
        self.total_positive_pools/=self.config_obj.worlds
        #print("Total Infections : ",self.total_infection)
        #print("Total quarantined days : ",self.total_quarantined_days)
        #print("Wrongly quarantined days : ",self.wrongly_quarantined_days)
        #print("Total Testing Cost : ",self.total_machine_cost)
        #print("Total Positives : ",self.total_positives)
        #print("Total False Positives : ",self.total_false_positives)

        if(plot):
            for state in tdict.keys():
                plt.plot(tdict[state])

            plt.title(self.model.name+' plot')
            plt.legend(list(tdict.keys()),loc='upper right', shadow=True)
            plt.show()
        else:
            if(not extra):
                return tdict, self.total_infection, self.total_quarantined_days, self.wrongly_quarantined_days, self.total_machine_cost
            else:
                return tdict, self.total_infection, self.total_quarantined_days, self.wrongly_quarantined_days, self.total_machine_cost,\
                            self.total_positives, self.total_false_positives
