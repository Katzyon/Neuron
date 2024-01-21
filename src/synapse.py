import numpy as np

class synapse:
    def __init__(self, neuron) -> None:
        self.n_synapse = neuron.n_synapses
        # create a list of
        self.max_rand_weight = 0.5 # maximal initial random weight of a synapse
        # create a random vector beteen 0 and max_rand_weight of length n_synapse
        self.synapses_weight = np.random.rand(self.n_synapse) * self.max_rand_weight

        
        # create an empty list of lists of length n_synapse
        self.activity_history = np.zeros(self.n_synapse)
        # create a list of length n_synapse for the group each synapse belongs to
        self.synapses_group = np.zeros(self.n_synapse)


