import numpy as np

class synapse:
    def __init__(self, neuron) -> None:
        self.n_synapse = neuron.n_synapses
        # create a list of
        
        
        # create a list of length n_synapse for the initial weight of each synapse
        self.weights = np.random.normal(neuron.mean_rand_weight, neuron.weight_std_dev, self.n_synapse)
        # create an empty list of lists of length n_synapse
        self.activity_hebb = np.zeros(self.n_synapse) # binary activity of synapse (1 is participated in cell firing, 0 is not)
        

        
    


