import sys
import ReadFile
import pickle
import World
import importlib.util
import os.path as osp
import policy_generator as pg
import matplotlib.pyplot as plt
import numpy as np

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_example_path():
    return sys.argv[1]


def get_config_path(path):
    config_filepath=osp.join(path,'config.txt')
    return config_filepath


def get_file_paths(example_path,config_obj):
    # File Names
    locations_filename=None
    agents_filename=osp.join(example_path,config_obj.agents_filename)
    interactions_FilesList_filename=osp.join(example_path,config_obj.interactions_files_list)
    events_FilesList_filename=osp.join(example_path,config_obj.events_files_list)
    if config_obj.locations_filename=="":
        locations_filename=None
    else:
        locations_filename=osp.join(example_path,config_obj.locations_filename)

    return agents_filename, interactions_FilesList_filename, events_FilesList_filename, locations_filename


def get_file_names_list(example_path,interactions_FilesList_filename,events_FilesList_filename,config_obj):
    # Reading through a file (for interactions/events) that contain file names which contain interactions and event details for a time step

    interactions_files_list=None
    events_files_list=None

    if config_obj.interactions_files_list=='':
        print('No Interaction files uploaded!')
    else:
        interactionFiles_obj=ReadFile.ReadFilesList(interactions_FilesList_filename)
        interactions_files_list=list(map(lambda x : osp.join(example_path,x) ,interactionFiles_obj.file_list))
        if interactions_files_list==[]:
            print('No Interactions inputted')


    if config_obj.events_files_list=='':
        print('No Event files uploaded!')
    else:
        eventFiles_obj=ReadFile.ReadFilesList(events_FilesList_filename)
        events_files_list=list(map(lambda x : osp.join(example_path,x) ,eventFiles_obj.file_list))
        if events_files_list==[]:
            print('No Events inputted')

    return interactions_files_list, events_files_list

def get_model(example_path):
    UserModel = module_from_file("Generate_model", osp.join(example_path,'UserModel.py'))
    model = UserModel.UserModel()
    return model

def get_policy(example_path):
    Generate_policy = module_from_file("Generate_policy", osp.join(example_path,'Generate_policy.py'))
    policy_list, event_restriction_fn=Generate_policy.generate_policy()
    return policy_list, event_restriction_fn

if __name__=="__main__":

    example_path = get_example_path()
    config_filename = get_config_path(example_path)

    # Read Config file using ReadFile.ReadConfiguration
    config_obj=ReadFile.ReadConfiguration(config_filename)

    agents_filename, interactions_FilesList_filename,\
    events_FilesList_filename, locations_filename = get_file_paths(example_path,config_obj)
    interactions_files_list, events_files_list = get_file_names_list(example_path,interactions_FilesList_filename,events_FilesList_filename,config_obj)

    # User Model
    model = get_model(example_path)
    # policy_list, event_restriction_fn=get_policy(example_path)


    ##########################################################################################

    # OPTION - 1
    # test_mode = "Same number of tests" #"Same number of tests" "Test cost vs Inf vs Q"
    # num_tests = 60
    # min_agents_per_test = 1
    # min_tests_per_agent = 1
    # max_agents_per_test = 5
    # max_tests_per_agent = 5

    # OPTION - 2
    test_mode="FP vs FN"
    num_tests = 60
    fp_range = np.arange(0.0,0.5,0.1)
    fn_range = np.arange(0.0,0.5,0.1)


    total_inf_plt = []
    total_q_plt = []
    total_wq_plt = []
    total_test_plt = []

    if(test_mode=="Same number of tests" or test_mode=="Test cost vs Inf vs Q"):
        for i in range(min_agents_per_test,max_agents_per_test):
            for j in range(min_tests_per_agent, max_tests_per_agent):
                if(test_mode=="Same number of tests"):
                    policy_list, event_restriction_fn =  pg.generate_group_testing_tests_policy(num_tests, i, j)
                elif(test_mode=="Test cost vs Inf vs Q"):
                    pass
                    # policy_list, event_restriction_fn =  pg.generate_policy(num_tests, i, j)
                world_obj=World.World(config_obj,model,policy_list,event_restriction_fn,agents_filename,interactions_files_list,locations_filename,events_files_list)
                tdict, total_infection, total_quarantined_days, wrongly_quarantined_days, total_test_cost = world_obj.simulate_worlds(plot=False)
                total_inf_plt.append(total_infection)
                total_q_plt.append(total_quarantined_days)
                total_wq_plt.append(wrongly_quarantined_days)
                total_test_plt.append(total_test_cost)

    elif(test_mode=="FP vs FN"):
        for i in fp_range:
            for j in fn_range:
                policy_list, event_restriction_fn =  pg.generate_fp_fn_policy(num_tests, i, j)

                world_obj=World.World(config_obj,model,policy_list,event_restriction_fn,agents_filename,interactions_files_list,locations_filename,events_files_list)
                tdict, total_infection, total_quarantined_days, wrongly_quarantined_days, total_test_cost = world_obj.simulate_worlds(plot=False)
                total_inf_plt.append(total_infection)
                total_q_plt.append(total_quarantined_days)
                total_wq_plt.append(wrongly_quarantined_days)
                total_test_plt.append(total_test_cost)


    # Plots
    if(test_mode=="Same number of tests"):
        wq_q_plt = [wq/q for wq,q in zip(total_wq_plt,total_q_plt)]
        plt.xlim(0, 1000)
        plt.ylim(0.0, 1.0)
        plt.scatter(total_inf_plt,wq_q_plt)
        plt.title("Total Infection vs Wrongly/Total Quarantined days")

    elif(test_mode=="Test cost vs Inf vs Q"):
        plot1 = plt.figure(1)
        plt.scatter(total_test_plt,total_inf_plt)
        plt.title("Total Test Cost vs Total Infection")

        plot2 = plt.figure(2)
        plt.scatter(total_test_plt,total_q_plt)
        plt.title("Total Test Cost vs Total Quarantined days")

    elif(test_mode=="FP vs FN"):
        plt.scatter(total_inf_plt,total_test_plt)
        plt.title("Total Infection vs Total Test Cost")

    plt.show()
    ###############################################################################################
