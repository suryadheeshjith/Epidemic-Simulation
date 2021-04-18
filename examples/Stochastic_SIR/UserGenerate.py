import GenerateFile
import re
from csv import DictWriter
import os.path as osp
from pathlib import Path
import random

'''
This class is a User defined class where we can convert the input data files to the required input data format.

The functions that can be overriden from base class GenerateFiles are -

    1. generate_agent_files()
    2. generate_interactions_files()
    3. generate_event_files()
    4. generate_location_files()

The new filename generated should be returned by any of the above functions.
'''

class UserGenerate(GenerateFile.GenerateFiles):

    def __init__(self,agents_filename, interactions_FilesList_filename, events_FilesList_filename, locations_filename):
        super().__init__(agents_filename, interactions_FilesList_filename, events_FilesList_filename, locations_filename)


    #
    # # Template for generation of CSV Event files from text files and a new column 'Event Type'
    # def generate_event_files(self):
    #     if(self.events_FilesList_filename.endswith('.txt')):
    #
    #         event_type_choices = ['S']+list(range(30))
    #         self.l = None
    #         self.readlistfile()
    #
    #         parent_path = Path(self.events_FilesList_filename).parent.absolute()
    #         self.new_filelist_name = 'event_files_list2.txt'
    #
    #         fl=open(osp.join(parent_path,self.new_filelist_name),'w')
    #         for filename in self.l:
    #             filename = filename[1:-1]
    #             filepath = osp.join(parent_path,filename)
    #
    #             newfilename = filename[:-3]+'csv'
    #             newfilepath = osp.join(parent_path,newfilename)
    #
    #             fl.write('<'+newfilename+'>')
    #
    #             self.readtextfile(filepath)
    #
    #             with open(newfilepath, 'w', newline='') as file:
    #                 fieldnames = ['Location Index', 'Agents', 'Event Type']
    #                 writer = DictWriter(file, fieldnames=fieldnames)
    #
    #                 writer.writeheader()
    #                 for i in range(len(self.events)):
    #                     event = self.events[i]
    #                     event_type = random.choice(event_type_choices)
    #                     print("Event Type :",event_type)
    #                     writer.writerow({'Location Index': event[0], 'Agents': event[1], 'Event Type':event_type})
    #         fl.close()
    #
    #
    #     return str(osp.join(parent_path, self.new_filelist_name))
    #
    # def readlistfile(self):
    #     f=open(self.events_FilesList_filename,'r')
    #     lines=f.readlines()
    #     separator=' '
    #     text=separator.join(lines)
    #     self.l = re.findall("\<.*?\>", text)
    #     f.close()
    #
    # def readtextfile(self,filepath):
    #     f = open(filepath,'r')
    #     self.no_events=int(self.get_value(f.readline()))
    #     event_info_keys=self.get_value(f.readline())
    #
    #     self.events = []
    #     for i in range(self.no_events):
    #         parameter_list=(self.get_value(f.readline())).split(':')
    #         self.events.append(parameter_list)
    #
    #     f.close()
    #
    # def get_value(self,line):
	#     if line.endswith('\n'):
	#         line=line[:-1]
	#     return line
