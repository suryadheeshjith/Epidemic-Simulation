
class GenerateFiles():

    def __init__(self,agents_filename, interactions_FilesList_filename, events_FilesList_filename, locations_filename):
        self.agents_filename=agents_filename
        self.interactions_FilesList_filename=interactions_FilesList_filename
        self.events_FilesList_filename=events_FilesList_filename
        self.locations_filename=locations_filename


    def generate_agent_files(self):
        return self.agents_filename

    def generate_interactions_files(self):
        return self.interactions_FilesList_filename

    def generate_event_files(self):
        return self.events_FilesList_filename

    def generate_location_files(self):
        return self.locations_filename

    def _generate_files(self):
        self.agents_filename = self.generate_agent_files()
        self.interactions_FilesList_filename = self.generate_interactions_files()
        self.events_FilesList_filename = self.generate_event_files()
        self.locations_filename = self.generate_location_files()


        return self.agents_filename,self.interactions_FilesList_filename,\
        self.events_FilesList_filename,self.locations_filename
