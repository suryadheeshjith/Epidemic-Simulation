import random
import copy
from Policy import Agent_Policy
from Agent import Agent
from functools import partial


class Results():
    def __init__(self,vaccine_name,agent,result,time_step,efficacy,decay_days):
        self.vaccine_name=vaccine_name
        self.agent=agent
        self.result=result
        self.time_stamp=time_step
        self.protection= decay_days
        

class Vaccine_type():
    def __init__(self,name,cost,decay,efficacy):

        self.vaccine_name=name
        self.vaccine_cost=cost
        self.decay_days=decay
        self.efficacy=efficacy
    
    def vaccinate(self,agent,time_step):

        # vaccinate agents
        result=self.inject_agent(agent)
        result_obj= Result(self.vaccine_name,agent,result,time_step,self.efficacy,self.decay_days)
        
        return result_obj  

       
     '''
     results=[result_object1,...]
     '''
    def inject_agent(self,agent):

        if (random.random()<self.efficacy):
            return 'Successful'
        else:
            return "Unsuccessful"


class Vaccination_policy(Agent_Policy):
    def __init__(self):
        super().__init__()

        self.policy_type='Vaccination'
        self.available_vaccines={}
        self.vaccines=[]
        self.statistics={}
        self.statistics_total={}
        self.statistics_total['Total Vaccination']=[]
        self.statistics_total['Total Successful']=[]
        self.statistics_total['Total Unsuccessful']=[]
        for name in self.available_vaccines.keys():
            self.statistics[name]={'Total Vaccination':[],'Total Successful':[],'Total Unsuccessful':[]}
            
    def enact_policy(self,time_step,agents,locations):
        
        self.newday()
        self.set_protection(agents)
        fn=self.full_random_vaccines()
        fn(agents,time_step)
        self.populate_results()
        self.restrict_agents(agents)
        self.get_stats()
    '''
    vaccines=[vaccine_obj1,vaccine_obj2...]
    '''
    def newday(self):

        self.vaccines=[]
        self.results=[]
        for name in self.available_vaccines.keys():

            for i in range(int(self.available_vaccines[name]['number'])):
                name,cost,decay,efficay=self.available_vaccines[name]['parameters']
                vaccine_obj=Vaccine_type(name,cost,decay,efficacy)
                self.vaccines.append(vaccine_obj)
                
    def full_random_vaccines(self,parameter=None, value_list=[]):


        assert isinstance(value_list,list)
        return partial(self.random_vaccination,parameter, value_list)
        
    def random_vaccination(self,parameter,value_list,agents,time_step):
        agents_copy = copy.copy(list(agents))  
        random.shuffle(agents_copy)


        for agent in agents_copy:
            if (agent.get_agent_policy_state('Vaccination') is None): 
                if self.parameter is None or agent.info[self.parameter] in value_list:
                    current_vaccine= random.choose(self.vaccines)
                    result=current_vaccine.vaccinate(agent,time_step)
                    self.results.append(result)
                    self.vaccines.remove(current_vaccine)


        ''' sinfo={'Agent Index': ....} Basically agents file
        '''
        return None
        
    def set_protection(self,agents):
        for agent in agents:
            history= self.get_agent_policy_history(agent) # dict of result objects
            if len(history)==0:
                continue
            else:
                history[-1].protection-=1
                
    def populate_results(self):
        for result_obj in self.results:
            agent= result_obj.agent
            self.update_agent_policy_history(agent,result_obj)
            self.update_agent_policy_state(agent,result_obj.result)
    
    def restrict_agents(self,agents):
        for agent in agents:
            history=self.get_agent_policy_history(agent)
            if (len(history)!=0):
                if(history[-1].result=="Successful"):
                    if(history[-1].protection>=1):
                        agent.restrict_receive_infection()  # sets can receive to False, NOT GETTING HIGHLIGHTED


       ''' history has list of result objects.
       '''
    def get_stats():
        self.statistics_total['Total Vaccination'].append(0)
        self.statistics_total['Total Successful'].append(0)
        self.statistics_total['Total Unsuccessful'].append(0)
        for name in self.available_vaccines.keys():
            self.statistics[name]['Total Vaccination'].append(0)
            self.statistics[name]['Total Successful'].append(0)
            self.statistics[name]['Total Unsuccessful'].append(0)
        
        for result_obj in self.results:
            self.statistics_total['Total Vaccination'][-1]+=1
            name=result_obj.name
            self.statistics[name]['Total Vaccination'][-1]+=1
            result=result_obj.result
            if result=="Successful":
                self.statistics[name]['Total Successful'][-1]+=1
                self.statistics_total['Total Successful'][-1]+=1
            elif result=="Unsuccessful":
                self.statistics[name]['Total Unsuccessful'][-1]+=1
                self.statistics_total['Total Unsuccessful'][-1]+=1
        
    def add_vaccination(self,name,cost,decay,efficacy,num):
        if name in self.available_vaccines.keys():
            if [name,cost,decay,efficacy]==self.available_vaccines[name]['parameters']
                self.available_vaccines[name]['number']+=num
            else:
                print("Error! Vaccine name with different parameter exists")
            
        print("Vaccines have been successfully added")
        else:
            self.available_vaccines[name]={'parameters':[name,cost,decay,efficacy],'number':num}
           
  
