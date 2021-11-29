import torch
import numpy as np
import math
import itertools
import matplotlib.pyplot as plt
import Container


class Env_box():
    def __init__(self, cfg):
        '''
        nodes(boxes) : contains nodes and their 2 dimensional coordinates
        [box_n, 2] = [3,2] dimension array e.g. [[0.5,0.7],[0.2,0.3],[0.4,0.1]]
        '''
        self.batch = cfg.batch
        self.box_n = cfg.box_n

        self.container = Container()

        self.device = torch.device(
            'cuda:0' if torch.cuda.is_available() else 'cpu')

    def get_nodes(self, seed=None):
        '''
        return nodes:(box_n,2)
        '''
        if seed is not None:
            torch.manual_seed(seed)

        return torch.rand((self.box_n, 2), device=self.device)

    def stack_nodes(self):
        '''
        nodes:(box_n,2)
        return inputs:(batch,box_n,2)
        '''
        list = [self.get_nodes() for i in range(self.batch)]
        inputs = torch.stack(list, dim=0)
        return inputs

    def get_batch_nodes(self, n_samples, seed=None):
        '''
        return nodes:(batch,box_n,2)
        '''
        if seed is not None:
            torch.manual_seed(seed)
        return torch.rand((n_samples, self.box_n, 2), device=self.device)

	def shuffle(self, inputs):
		'''
		shuffle nodes order with a set of xy coordinate
		inputs:(batch,box_n,2)
		return shuffle_inputs:(batch,box_n,2)
		'''
		shuffle_inputs = torch.zeros(inputs.size())
		for i in range(self.batch):
			perm = torch.randperm(self.box_n)
			shuffle_inputs[i, :, :] = inputs[i, perm, :]
		return shuffle_inputs
    # random

    def stack_random_placements(self):
		'''
		tour:(box_n)
		return tours:(batch,box_n)
		'''
		list = [self.get_random_tour() for i in range(self.batch)]
		tours = torch.stack(list, dim=0)
		return tours

    def get_random_placement(self):
		'''
		return tour:(box_n)
		'''
		boxes = []
        # can use queue to do random placement, unneccessery loop
		while set(boxes) != set(range(self.box_n)):
			box = np.random.randint(self.box_n)
			if box not in boxes:
				boxes.append(box)
		boxes = torch.from_numpy(np.array(boxes))
		return boxes

    # stacking
    def stack_l(self, inputs, tours):
		'''
		inputs:(batch,box_n,2)
		tours:(batch,box_n)
		return l_batch:(batch)
		'''
		list = [self.cal_reward(inputs[i], tours[i]) for i in range(self.batch)]
		l_batch = torch.stack(list, dim=0)
		return l_batch

    def cal_reward(self, nodes, tour):
		'''
        aka container_efficient / number of box
		nodes:(city_t,2), tour:(city_t)
		l(= total distance) = l(0-1) + l(1-2) + l(2-3) + ... + l(18-19) + l(19-0) @20%20->0
		return l:(1)
		'''
        self.container.cal_reward(nodes,tour)
		# l = 0
		# for i in range(self.city_t):
		#	l += get_2city_distance(nodes[tour[i]], nodes[tour[(i+1)%self.city_t]])
		return l


    # ploting 

    def show(self, nodes, tour):
		plt.plot()
        plt.show()

