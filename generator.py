from numpy.lib.function_base import select
import pandas as pd
import numpy as np
from collections import defaultdict 
import random
import matplotlib.pyplot as plt
from scipy.stats import norm
import pickle
import util

class Generator():
    def __init__(self, U, I, K, item_num_s = 200, noise_rate = 0.3, sigma = None, seq_num = 1):
        np.random.seed(seed=2021)
        random.seed(2021)

        self.U = U
        self.I = I
        self.K = K
        self.noise_rate = noise_rate
        self.p_min = (1/K) * self.noise_rate
        self.S     = K
        self.item_num_s = item_num_s
        self.sigma      = sigma
        self.seq_num    = seq_num
        if sigma is None:
            print('using default sigma ...')
            self.sigma = [ [] for k in range(self.K) ]
            for k in range(self.K):
                self.sigma[k] = self.I / (self.K*6)
        else:
            self.sigma = sigma
        self.user_topic     = self._create_user_topic()
        self.bow            = self._create_bow()

    def _vaild_sigma(self):
        try:
            self.sigma
            print(self.sigma)
        except AttributeError:
            self.sigma = [ [] for k in range(self.K) ]
            for k in range(self.K):
                self.sigma[k] = self.I / (self.K*3)
            print(self.sigma)
    
    def _create_user_topic(self):
        user_topic = defaultdict(dict)
        Z = [ z for z in range(self.K) ]
        Z_u = [ [] for u in range(self.U) ]
        for u in range(self.U):
            Z_u[u] = random.sample(Z, len(Z))
        for u in range(self.U):
            for s in range(self.S):
                user_topic[u][s] = Z_u[u][s]
        return user_topic
    
    def _sampling_topics(self, topics, sample_size=None):
        if sample_size is None:
            sample_size = self.item_num_s
        theta_u = np.full(self.K, self.p_min)
        if isinstance(topics, list) == True:
            for t in topics:
                theta_u[t] = (1-self.p_min*(self.K-len(topics))) / len(topics)
        else:
            theta_u[topics] = (1-self.p_min*(self.K-1))
        Z_u = [np.argmax(z)  for z in np.random.multinomial(1, theta_u, size=int(sample_size))]
        return Z_u
    
    def _sampling_item(self, z):
        i = np.random.normal((z+0.5)*(self.I/self.K), self.sigma[(int(z))], 1)
        x = [0, int(i), self.I-1]
        x.sort()
        item = x[1]
        return item
        
    def _create_bow(self):
        bow = [ [] for u in range(self.U) ]
        for s in range(self.S):
            for u in range(self.U):
                Z_u = self._sampling_topics(self.user_topic[u][s])
                for z in Z_u:
                    for _ in range(self.seq_num):
                        i = self._sampling_item(z)
                        bow[u].append(i)
        return bow
    
    def user_topic_dictribution(self):
        Theta = np.full([self.S, self.U, self.K], self.p_min)
        for s in range(self.S):
            for u in range(self.U):
                topics = self.user_topic[u][s]
                if isinstance(topics, list) == True:
                    for t in topics:
                        Theta[s,u,t] = (1-self.p_min*(self.K-len(topics))) / len(topics)
                else:
                    Theta[s,u,topics] = (1-self.p_min*(self.K-len(topics))) / len(topics)
        return self.item_num_s, Theta
    
    def show_item_distribution(self, x_size=15, y_size=2.5, xticks=500):
        self._vaild_sigma()
        x = np.arange(0,self.I-1,1)
        fig, ax = plt.subplots(figsize=(x_size, y_size)) 
        for k in range(self.K):
            y = norm.pdf(x, (k+0.5)*(self.I/self.K), self.sigma[k])
            plt.plot(x,y,color=util.color_list[k])
        plt.xticks(np.arange(0, self.I-1, 500))
        plt.xlim(0,self.I-1)
        return
    
    def show_user_distribution(self, u):
        bow_u = self.bow[u]
        bins  = self.K*10
        for s in range(self.S):
            plt.hist(self.bow[u][self.item_num_s*s:self.item_num_s*(s+1)], bins=bins, range=(0,self.I-1))
            plt.title('u = {}, s={}, z = {}'.format(u, s, self.user_topic[u][s]))
            plt.show()
            plt.close('all')
        
    def show_all_users_distribution(self):
        bins  = self.K*10
        for s in range(self.S):
            bow_all_s = []
            for u in range(self.U):
                bow_u   = self.bow[u]
                bow_u_s = bow_u[self.item_num_s*s:self.item_num_s*(s+1)]
                bow_all_s.extend(bow_u_s)
            plt.hist(bow_all_s, bins=bins)
            plt.title('s={}'.format(s))
            plt.show()
            plt.close('all')
    
    def show_all_users_distribution_of_sequential_bow(self):
        bins  = self.K*10
        for s in range(self.S):
            bow_all_s = []
            for u in range(self.U):
                bow_u   = self.sequential_bow[u]
                bow_u_s = bow_u[self.item_num_s*s:self.item_num_s*(s+1)]
                bow_all_s.extend(bow_u_s)
            plt.hist(bow_all_s, bins=bins)
            plt.title('s={}'.format(s))
            plt.show()
            plt.close('all')