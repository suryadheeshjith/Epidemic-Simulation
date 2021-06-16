import Model

def probabilityOfInfection_fn(p_infected_states_list,contact_agent,c_dict,current_time_step):
	if contact_agent.state=='Infected':
		return 0.03
		# return 0.005 # For table of params
	return 0

class UserModel(Model.StochasticModel):
	def __init__(self):
		individual_types=['Susceptible','Infected','Recovered']
		infected_states=['Infected']
		state_proportion={
							'Susceptible':0.97,
							'Infected':0.03,
							'Recovered':0
						}
		Model.StochasticModel.__init__(self,individual_types,infected_states,state_proportion)
		self.set_transition('Susceptible', 'Infected', self.p_infection(None,probabilityOfInfection_fn))
		self.set_transition('Infected', 'Recovered', self.p_standard(0.12))
		# self.set_transition('Infected', 'Recovered', self.p_standard(0)) # For table of params


		self.set_event_contribution_fn(None)
		self.set_event_recieve_fn(None)

		self.name='Stochastic SIR on complete graph'
