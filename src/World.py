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
        for agent in agents_obj.agents.values():
            for truth in agent.quarantine_list:
                if(truth=="Right"):
                    total_quarantined_days+=1
                elif(truth=="Wrong"):
                    total_quarantined_days+=1
                    wrongly_quarantined_days+=1


        self.total_quarantined_days+=total_quarantined_days
        self.wrongly_quarantined_days+=wrongly_quarantined_days

        self.total_infection+=len(agents_obj.agents)-end_state["Susceptible"][-1]
        self.total_machine_cost+=machine_cost

        return end_state, agents_obj, locations_obj

    #Average number time series
    def average(self,tdict,number):
        for k in tdict.keys():
            l=tdict[k]
            for i in range(len(l)):
                tdict[k][i]/=number

        return tdict

    #Averages multiple simulations and plots a single plot
    def simulate_worlds(self,plot=True):

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
        print("Random Total Infections : ",self.total_infection)
        print("Total quarantined days : ",self.total_quarantined_days)
        print("Wrongly quarantined days : ",self.wrongly_quarantined_days)
        print("Total Testing Cost : ",self.total_machine_cost)
        if(plot):
            for state in tdict.keys():
                plt.plot(tdict[state])

            plt.title(self.model.name+' plot')
            plt.legend(list(tdict.keys()),loc='upper right', shadow=True)
            plt.show()
        else:
            return tdict, self.total_infection, self.total_quarantined_days, self.wrongly_quarantined_days, self.total_machine_cost
