
""" Defines the Neuron class. with the following attributes:
    - synapse: list of synapse objects connected to the neuron
    - setpoint: the averaged firing rate of the neuron
    - dt: the time step of the simulation - each dt input vector is created (of one cell or a groups of cells)
    - dt_sequence: time bin for the activity of all neurons (optogenetic activation of all detected somas)
    - dt_update_weights: time bin to update the synaptic weights
    - activityVec:time vector of the activity of the neuron (dt time base)    """
from create_groups import create_groups
from synapse import synapse
import numpy as np
from create_groups_probabilities import generate_random_vector


class Neuron:
    def __init__(self):

        self.n_synapses = 25 # number of synapses connected to the neuron
        self.n_groups = 2 # number of groups

        # the last group is the remaining cells. The vector length is n_groups + 1. The sum of the vector is 1.
        self.group_probabilities = [0.5, 0.1, 0.4] 

        self.synapse_in_group = 10 # number of cells in each group
        self.setpoint = 10 # the averaged firing rate of the neuron
        self.mean_rand_weight = 0.3 # mean initial random weight of the synapses
        self.weight_std_dev = 0.1 # standard deviation of the random weight of the synapses
        self.threshold =  0.6 * self.synapse_in_group * self.mean_rand_weight # threshold for firing depends on the size of the group and the weight of the synapses
        
        self.synapses_weight = [] # length n_synapses list of synaptic weights
        self.synapses_state = [] # input: length n_synapses list of synaptic states (0 or 1)

        self.weights = [] # length n_synapses list of synaptic weights
        self.activity_hebb = [] # length n_synapses list of synaptic states during dt > threshold (0 or 1)
        self.create_synapses()
        
        self.dt = 0.1 # every dt the neuron gets an input vector
        #self.dt_sequence =  self.dt / self.n_groups # time bin for the activity of all neurons (optogenetic activation of all detected somas)
        self.dt_bin = 10 # time to bin the activity of the neuron
        self.dt_update_weights = 100 # time bin to update the synaptic weights
        self.time = 0
        self.activityVec = []
        self.activityVec.append(0)

        self.run_model()
    
    def run_model(self):

        self.bin_counter = 0

        for day in range(self.dt_update_weights): # one day of a 100

            for current_bin in np.arange(0, self.dt_bin, self.dt): # one bin (sum acitivty in bin to update synapse.activity_hebb)
                # runs from 0 to 10 with 0.1 dt (0 to dt_bin with dt time steps = 100 steps)

                # create new input matrix
                self.create_input() # input matrix sized n_synapses * (dt_bin/dt)

                for sequence in range(self.n_groups + self.n_remaining): # one sequence - every sequence need to randomize the input matrix
                    # The input matrix is composed of the groups and the remaining cells matrix (rand_remaining_matrix)
                    # get input vector from matrix
                    
                    input_vector = self.input_matrix[:, self.bin_counter]
                    active_synapses = np.where(input_vector == 1)[0]
                    
                    # check if the neuron fires
                    if len(active_synapses) > self.threshold: # should be weighted!!!
                        self.activityVec.append(1)
                        for syn in active_synapses:
                            self.synapses[syn].activity_hebb.append(1) # Is it synapses_state ???? 

                        for syn in not active_synapses: # all the synapses that did not worked
                            self.synapses[syn].activity_hebb.append(0)
                    else:
                        self.activityVec.append(0)
                    # update synapses state
                    

                self.bin_counter += 1    
                self.time += self.dt
                self.update_bin_acitivty()
                
            self.update_synaptic_weights() # at the end of the day


    def create_synapses(self):
        # create a list of length n_synapse for the initial weight of each synapse
        self.weights = np.random.normal(self.mean_rand_weight, self.weight_std_dev, self.n_synapses)
        # create an empty list of lists of length n_synapse
        self.activity_hebb = np.zeros(self.n_synapses, dtype=list) # binary activity of synapse (1 is participated in cell firing, 0 is not)
        # creates the initial groups and remaining cells as inputs
        self.groups, self.remaining = create_groups(self.n_synapses, self.n_groups, self.synapse_in_group)
        # self.remaining = list of indices of synapses that are not grouped
        self.n_remaining = len(self.remaining)

    # create input matrix where each row is an input from all synapses. The matrix length is (dt_bin/dt)
    def create_input(self):
        # create empty binary numpy array
        self.input_matrix = np.empty((0, self.n_synapses), dtype=int)


        # random vector where each element is a group or the remaining cells (n_groups + 1)
        self.bin_activation_vector = generate_random_vector(self.group_probabilities,int(self.dt_bin/self.dt))

        remain_group = self.bin_activation_vector[-1] # the last group is the remaining cells
        #self.create_input_matrix(remain_group)
        # run over bin_activation_vector and create input vector(group) / matrix (remaining) per each index
        for idx, bin_activation in enumerate(self.bin_activation_vector):
            if bin_activation == remain_group: # need to create martix of remaining cells - single cell is active in each row
                # create input matrix of the remaining cells
                self.rand_remaining_matrix() # update the remaining matrix
                # append to self.input_matrix the self.remaining_matrix
                self.input_matrix = np.vstack((self.input_matrix, self.remaining_matrix))
            # if idx > 5 break
            elif idx > 5:
                print(self.input_matrix)
                break
                
            else:
                # create group vector
                print("bin vector", self.bin_activation_vector)
                print("group number", bin_activation)
                print("groups", self.groups)
                group_vector = self.create_group_input(self.groups[bin_activation])
                self.input_matrix = np.vstack((self.input_matrix, group_vector)) # append group vector to input matrix
        

        self.max_synaptic_weight =  1# maximum synaptic weight. must be that len(k) * max_synaptic_weight > threshold
        # create groups input matrix
        

        # concatenate the groups and remaining cells matrix
        self.input_matrix = np.concatenate((self.groups_matrix, self.remaining_matrix), axis=0)
        

    def update_synaptic_weights(self): # at the end of the day
        for syn in self.synapse:
            syn.updateWeight()
        # add noise to all weights


    def update_bin_activity(self, inputVec):
        pass

    # create a sparse matrix of the remaining cells not in the groups, in each row only one cell is active 
    def rand_remaining_matrix(self):
        import random
        
        remaining_cells = self.remaining
        random.shuffle(remaining_cells)

        # Create a binary matrix with n rows and L columns
        binary_matrix = np.zeros((len(remaining_cells), self.n_synapses), dtype=int)

        for idx, num in enumerate(remaining_cells):
            if 0 <= num < self.n_synapses:
                binary_matrix[idx, num] = 1

        self.remaining_matrix = binary_matrix

    def create_group_input(self, group):
        print("input group", group)
        group_vector = np.zeros((1, self.n_synapses), dtype=int)
        group_vector[0, group] = 1
        print("output group vector", group_vector)
        print("end of group vector")

        return group_vector



if __name__ == "__main__":
    neuron = Neuron()
    


