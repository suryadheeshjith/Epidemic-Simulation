import unittest
import os.path as osp
from src.Main import *
import random

class TestIntegrationSimple(unittest.TestCase):

    def get_tdict(self, example_path):
        config_filename = get_config_path(example_path)

        # Read Config file using ReadFile.ReadConfiguration
        config_obj=ReadFile.ReadConfiguration(config_filename)

        agents_filename, interactions_FilesList_filename,\
        events_FilesList_filename, locations_filename = get_file_paths(example_path,config_obj)
        interactions_files_list, events_files_list = get_file_names_list(example_path,interactions_FilesList_filename,events_FilesList_filename,config_obj)

        # User Model and Policy
        model = get_model(example_path)
        policy_list, event_restriction_fn=get_policy(example_path)

        # Creation of World object
        world_obj=World.World(config_obj,model,policy_list,event_restriction_fn,agents_filename,interactions_files_list,locations_filename,events_files_list)
        tdict = world_obj.simulate_worlds(False)
        return tdict

    def test_agent(self):
        random.seed(10)
        example_path = osp.join('tests','integration','fixtures','Example_Single_Agent')
        tdict = self.get_tdict(example_path)

        self.assertEqual(len(tdict['Susceptible']),31)
        self.assertEqual(len(tdict['Infected']),31)
        self.assertEqual(len(tdict['Recovered']),31)

        self.assertEqual(tdict['Infected'],[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,\
                                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])





    def test_three_agents(self):
        random.seed(10)
        example_path = osp.join('tests','integration','fixtures','Example_Three_Agents')
        tdict = self.get_tdict(example_path)

        self.assertEqual(len(tdict['Susceptible']),31)
        self.assertEqual(len(tdict['Infected']),31)
        self.assertEqual(len(tdict['Recovered']),31)

        self.assertEqual(tdict['Recovered'],[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,\
                                            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])




if __name__ == '__main__':
    unittest.main()
