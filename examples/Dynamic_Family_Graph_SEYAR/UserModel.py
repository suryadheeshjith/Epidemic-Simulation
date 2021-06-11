import Model

def probabilityOfInfection_fn(agent, p_infected_states_list,contact_agent,c_dict,current_time_step):

	# Homogenous
	# if contact_agent.state=='Symptomatic':
	# 	return 0.4
	# elif contact_agent.state=='Asymptomatic':
	# 	return 0.3
	# return 0


	# Single Level - Age
	# if(agent.info['Age']=='0-19'):
	# 	if contact_agent.state=='Symptomatic':
	# 		return 0.4*0.4
	# 	elif contact_agent.state=='Asymptomatic':
	# 		return 0.3*0.4
	# 	return 0
	#
	# elif(agent.info['Age']=='20-59'):
	# 	if contact_agent.state=='Symptomatic':
	# 		return 0.4*0.8
	# 	elif contact_agent.state=='Asymptomatic':
	# 		return 0.3*0.8
	# 	return 0
	#
	# elif(agent.info['Age']=='60+'):
	# 	if contact_agent.state=='Symptomatic':
	# 		return 0.4*1.2
	# 	elif contact_agent.state=='Asymptomatic':
	# 		return 0.3*1.2
	# 	return 0
	#
	# else:
	# 	assert 1==0

	# Two Level - Age + Blood Group
	if(agent.info['Age']=='0-19' and agent.info['Blood Group']=='A'):
		if contact_agent.state=='Symptomatic':
			return 0.4*0.8*0.4
		elif contact_agent.state=='Asymptomatic':
			return 0.3*0.8*0.4
		return 0

	elif(agent.info['Age']=='20-59' and agent.info['Blood Group']=='A'):
		if contact_agent.state=='Symptomatic':
			return 0.4*0.8*0.8
		elif contact_agent.state=='Asymptomatic':
			return 0.3*0.8*0.8
		return 0

	elif(agent.info['Age']=='60+' and agent.info['Blood Group']=='A'):
		if contact_agent.state=='Symptomatic':
			return 0.4*0.8*1.2
		elif contact_agent.state=='Asymptomatic':
			return 0.3*0.8*1.2
		return 0

	elif(agent.info['Age']=='0-19' and agent.info['Blood Group']=='O'):
		if contact_agent.state=='Symptomatic':
			return 0.4*0.4*0.6
		elif contact_agent.state=='Asymptomatic':
			return 0.3*0.4*0.6
		return 0

	elif(agent.info['Age']=='20-59' and agent.info['Blood Group']=='O'):
		if contact_agent.state=='Symptomatic':
			return 0.4*0.4*1.2
		elif contact_agent.state=='Asymptomatic':
			return 0.3*0.4*1.2
		return 0

	elif(agent.info['Age']=='60+' and agent.info['Blood Group']=='O'):
		if contact_agent.state=='Symptomatic':
			return 0.4*0.4*1.5
		elif contact_agent.state=='Asymptomatic':
			return 0.3*0.4*1.5
		return 0

	elif(agent.info['Age']=='0-19' and agent.info['Blood Group']=='Other'):
		if contact_agent.state=='Symptomatic':
			return 0.4*0.6*0.8
		elif contact_agent.state=='Asymptomatic':
			return 0.3*0.6*0.8
		return 0

	elif(agent.info['Age']=='20-59' and agent.info['Blood Group']=='Other'):
		if contact_agent.state=='Symptomatic':
			return 0.4*0.6*0.8
		elif contact_agent.state=='Asymptomatic':
			return 0.3*0.6*0.8
		return 0

	elif(agent.info['Age']=='60+' and agent.info['Blood Group']=='Other'):
		if contact_agent.state=='Symptomatic':
			return 0.4*0.6*0.8
		elif contact_agent.state=='Asymptomatic':
			return 0.3*0.6*0.8
		return 0





class UserModel(Model.StochasticModel):
	def __init__(self):
		individual_types=['Susceptible','Exposed','Asymptomatic','Symptomatic','Recovered']
		infected_states=['Asymptomatic','Symptomatic']
		state_proportion={
							'Susceptible':0.99,
							'Exposed':0,
							'Recovered':0,
							'Asymptomatic':0,
							'Symptomatic':0.01
						}
		Model.StochasticModel.__init__(self,individual_types,infected_states,state_proportion)
		self.set_transition('Susceptible', 'Exposed', self.p_infection([None,None],probabilityOfInfection_fn))
		self.set_transition('Exposed', 'Symptomatic', self.p_standard(0.15))
		self.set_transition('Exposed', 'Asymptomatic', self.p_standard(0.2))
		self.set_transition('Symptomatic', 'Recovered', self.p_standard(0.1))
		self.set_transition('Asymptomatic', 'Recovered', self.p_standard(0.1))
