import Testing_Policy
import Lockdown_Policy
import random
import numpy as np

def generate_group_testing_tests_policy(num_tests, num_agents_per_test, num_tests_per_agent):
    policy_list=[]

    # Group/Pool Testing
    num_agents = int(np.floor(num_tests*num_agents_per_test/num_tests_per_agent))
    print(num_agents,num_agents_per_test,num_tests_per_agent)
    Pool_Testing = Testing_Policy.Test_Policy(lambda x:num_agents)
    Pool_Testing.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 1000, 1)
    Pool_Testing.set_register_agent_testtube_func(Pool_Testing.random_agents(num_agents_per_test,num_tests_per_agent))
    policy_list.append(Pool_Testing)

    ATP = Lockdown_Policy.agent_policy_based_lockdown("Testing",["Positive"],lambda x:True,10)
    policy_list.append(ATP)

    def event_restriction_fn(agent,event_info,current_time_step):
        return False

    return policy_list,event_restriction_fn

def generate_fp_fn_policy(num_tests, fp, fn):
    policy_list=[]

    # Group/Pool Testing
    print(num_tests,fp,fn)
    Pool_Testing = Testing_Policy.Test_Policy(lambda x:num_tests)
    Pool_Testing.add_machine('Simple_Machine', 200, fp, fn, 0, 1000, 1)
    Pool_Testing.set_register_agent_testtube_func(Pool_Testing.random_agents(1,1))
    policy_list.append(Pool_Testing)

    ATP = Lockdown_Policy.agent_policy_based_lockdown("Testing",["Positive"],lambda x:True,10)
    policy_list.append(ATP)

    def event_restriction_fn(agent,event_info,current_time_step):
        return False

    return policy_list,event_restriction_fn

# 2D Infection Plots
def generate_2D_infection_test_policy(num_tests, num_agents_per_test, num_tests_per_agent, dynamic=False):
    policy_list=[]

    # Group/Pool Testing
    Pool_Testing = Testing_Policy.Test_Policy(lambda x:-1)
    Pool_Testing.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 1000, 1)
    Pool_Testing.set_register_agent_testtube_func(Pool_Testing.random_agents_with_dynamic(num_tests, num_agents_per_test, num_tests_per_agent, dynamic))
    policy_list.append(Pool_Testing)

    ATP = Lockdown_Policy.agent_policy_based_lockdown("Testing",["Positive"],lambda x:True,10)
    policy_list.append(ATP)

    def event_restriction_fn(agent,event_info,current_time_step):
        return False

    return policy_list,event_restriction_fn
