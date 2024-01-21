
""" Defines the Neuron class. with the following attributes:
    - synapse: list of synapse objects connected to the neuron
    - setpoint: the averaged firing rate of the neuron
    - dt: the time step of the simulation - each dt input vector is created (of one cell or a groups of cells)
    - dtSequence: time bin for the activity of all neurons (optogenetic activation of all detected somas)
    - dtUpdate: time bin to update the synaptic weights
    - activityVec:time vector of the activity of the neuron (dt time base)    """
from src.create_groups import create_groups
from src.synapse import synapse


class Neuron:
    def __init__(self):

        n = 100
        m = 3
        k = 20
        self.groups, self.remaining = create_groups(n, m, k)
        self.n_groups = len(self.groups)

        self.n_synapses = 100 # number of synapses connected to the neuron
        self.synapses_weight = [] # length n_synapses list of synaptic weights
        self.synapses_state = [] # input: length n_synapses list of synaptic states (0 or 1) 
        self.setpoint = 10 # the averaged firing rate of the neuron
        self.synapses = [] # list of synapse objects connected to the neuron
        self.dt = 0.1
        self.dt_sequence =  self.dt / self.n_groups # time bin for the activity of all neurons (optogenetic activation of all detected somas)
        self.dt_bin = 10 * self.dt # time to bin the activity of the neuron
        self.dtUpdate = 100 * self.dt_bin # time bin to update the synaptic weights
        
        self.activityVec = []
        self.activityVec.append(0)

    def addSynapse(self):
            synapse(self)
        

    def updateSynapticWeights(self):
        for syn in self.synapse:
            syn.updateWeight()

    def updateActivity(self, inputVec):
        # update the activity of the neuron
        # inputVec: the input vector to the neuron (one cell or a groups of cells)
        # dt: the time step of the simulation - each dt input vector is created (of one cell or a groups of cells)
        # dtSequence: time bin for the activity of all neurons (optogenetic activation of all detected somas)
        # dtUpdate: time bin to update the synaptic weights
        # activityVec:time vector of the activity of the neuron (dt time base)
        # setpoint: the averaged firing rate of the neuron
        # synapse: list of synapse objects connected to the neuron

        # calculate the activity of the neuron
        activity = 0
        for syn in self.synapse:
            activity += syn.weight * inputVec[syn.preCell]

        # update the activity vector
        self.activityVec.append(activity)

        # update the synaptic weights
        if len(self.activityVec) % self.dtUpdate == 0:
            self.updateSynapticWeights()

    def updateActivitySequence(self, inputVec):
        # update the activity of the neuron
        # inputVec: the input vector to the neuron (one cell or a groups of cells)
        # dt: the time step of the simulation - each dt input vector is created (of one cell or a groups of cells)
        # dtSequence: time bin for the activity of all neurons (optogenetic activation of all detected somas)
        # dtUpdate: time bin to update the synaptic weights
        # activityVec:time vector of the activity of the neuron (dt time base)
        # setpoint: the averaged firing rate of the neuron
        # synapse: list of synapse objects connected to the neuron

        # calculate the activity of the neuron
        activity = 0

# example usage
n = 100
m = 3
k = 20
groups, remaining = create_groups(n, m, k)


