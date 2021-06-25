import sys
import ReadFile
import pickle
import World
import importlib.util
import os.path as osp
import policy_generator as pg
import matplotlib
import matplotlib.pyplot as plt
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

    example_path = get_example_path()
    config_filename = get_config_path(example_path)

    # Read Config file using ReadFile.ReadConfiguration
    config_obj=ReadFile.ReadConfiguration(config_filename)

    agents_filename, interactions_FilesList_filename,\
    events_FilesList_filename, locations_filename = get_file_paths(example_path,config_obj)
    interactions_files_list, events_files_list = get_file_names_list(example_path,interactions_FilesList_filename,events_FilesList_filename,config_obj)

    # User Model
    model = get_model(example_path)

    ##########################################################################################

    fp = open("2D_histogram.txt","w")
    num_tests = 90
    pools_list = [(3,2),(4,2),(5,2),(None,None)]
    tdicts = []
    ttinfect = []
    ttq = []
    ttfp = []
    ttc = []
    for i,j in pools_list:
        if(i and j):
            policy_list, event_restriction_fn =  pg.generate_2D_infection_test_policy(num_tests, i, j)
        else:
            policy_list, event_restriction_fn =  pg.generate_2D_infection_test_policy(num_tests, i, j, True)

        world_obj=World.World(config_obj,model,policy_list,event_restriction_fn,agents_filename,interactions_files_list,locations_filename,events_files_list)
        tdict, total_infection, total_quarantined_days, wrongly_quarantined_days, total_test_cost,total_positives, total_false_positives = world_obj.simulate_worlds(plot=False, extra=True)
        fp.write("("+str(i)+","+str(j)+") : ")
        fp.write(str(tdict)+"\n")
        fp.write("Total infection : {0}\n".format(str(total_infection)))
        fp.write("Total Quarantined days : {0}\n".format(str(total_quarantined_days)))
        fp.write("Total False Positives : {0}\n".format(str(total_false_positives)))
        fp.write("Total Test cost : {0}\n".format(str(total_test_cost)))

        tdicts.append(tdict)
        ttinfect.append(total_infection)
        ttq.append(total_quarantined_days)
        ttfp.append(total_false_positives)
        ttc.append(total_test_cost)

    fp.close()
    # Plot
    ls = []
    for (i,j) in pools_list:
        if i:
            ls.append('({0},{1})'.format(i,j))
        else:
            ls.append('Dynamic'.format(i,j))

    barWidth = 0.25
    # fig = plt.subplots(figsize =(12, 8))

    # Set position of bar on X axis
    br1 = np.arange(len(ttinfect))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]

    # Make the plot
    plt.bar(br1, ttinfect, color ='r', width = barWidth,edgecolor ='grey', label ='Total Infection')
    plt.bar(br2, ttq, color ='g', width = barWidth,edgecolor ='grey', label ='Total Quarantined Days')
    plt.bar(br3, ttfp, color ='b', width = barWidth,edgecolor ='grey', label ='Total False Positive')

    # Adding Xticks
    # plt.xlabel('Branch', fontweight ='bold', fontsize = 15)
    # plt.ylabel('Students passed', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(ttinfect))],ls)

    plt.legend()
    plt.show()
    #plt.savefig('2D_histogram.pgf')
    ###############################################################################################
