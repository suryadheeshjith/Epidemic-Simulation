import sys
import ReadFile
import pickle
import World
import importlib.util
import os.path as osp
import policy_generator as pg
import matplotlib
import matplotlib.pyplot as plt
import random
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
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
    random.seed(42)
    # import tracemalloc
    # tracemalloc.start()
    example_path = get_example_path()
    config_filename = get_config_path(example_path)

    # Read Config file using ReadFile.ReadConfiguration
    config_obj=ReadFile.ReadConfiguration(config_filename)

    agents_filename, interactions_FilesList_filename,\
    events_FilesList_filename, locations_filename = get_file_paths(example_path,config_obj)
    interactions_files_list, events_files_list = get_file_names_list(example_path,interactions_FilesList_filename,events_FilesList_filename,config_obj)

    # User Model
    model = get_model(example_path)

    cost_structures = {
                        '(2,2,2,25)':(25,2,2,2),
                        '(3,2,5,20)':(20,5,2,3),
                        '(2,1,1,30)':(30,1,1,2),
                        '(1,4,2,20)':(20,2,4,1)
                        }
    # cost_structures = {'(10,3,1)':(10,3,1),'(5,3,1)':(5,3,1)}
    pools_list = [(1,1),(2,1),(4,2),(5,3),(6,2),(7,2)]
    testing_gap=1
    tests_per_period=90
    turnaround_time=0
    restriction_time=6
    fn=0.1
    falsep=0.1
    cost_dict = {}




    for i,j in pools_list:
        print(i,j)
        policy_list, event_restriction_fn =  pg.generate_group_testing_colab(i, j,testing_gap,tests_per_period,turnaround_time,restriction_time,fn,falsep)
        world_obj=World.World(config_obj,model,policy_list,event_restriction_fn,agents_filename,interactions_files_list,locations_filename,events_files_list)
        tdict, total_infection, total_quarantined_days, wrongly_quarantined_days, total_test_cost,\
        total_positives, total_false_positives = world_obj.simulate_worlds(plot=False, extra=True)
        for key in cost_structures.keys():
            value = cost_structures[key]
            inf_cost = value[0]
            q_cost = value[1]
            fp_cost = value[2]
            t_cost = value[3]
            total_cost = inf_cost*total_infection+q_cost*total_quarantined_days+fp_cost*total_false_positives + t_cost*total_test_cost
            try:
                cost_dict[key].append(total_cost)
            except:
                cost_dict[key] = []
                cost_dict[key].append(total_cost)


    ls = []
    for (i,j) in pools_list:
        if i:
            ls.append('({0},{1})'.format(i,j))
        else:
            ls.append('Dynamic'.format(i,j))

    barWidth = 1.0/(len(cost_structures)+3)
    fig = plt.subplots(figsize =(12, 8))

    brs = []
    for i in range(len(pools_list)):
        if i == 0:
            br = np.arange(len(pools_list))
        else:
            br = [x + barWidth for x in brs[-1]]
        brs.append(br)

    # Make the plot
    labels = cost_structures.keys()
    for idx,label in enumerate(labels):
        plt.bar(brs[idx], cost_dict[label], width = barWidth,edgecolor ='grey', label =label)
        print(cost_dict[label])

    # Adding Xticks
    plt.xlabel('Pooling Strategy')
    plt.ylabel('Total Cost')
    plt.ylim(10000,30000)
    middle = len(cost_structures)/2
    plt.xticks([r + middle*barWidth for r in range(len(pools_list))],ls)
    plt.title("Total Costs for different cost structures - (test_cost, false positive cost, quarantine cost, Infection cost)")

    plt.legend()
    # plt.show()
    plt.savefig('2D_histogram.pgf')
