from numpy.lib.function_base import select
import pandas as pd
import numpy as np
from collections import defaultdict 
import random
import matplotlib.pyplot as plt
from scipy.stats import norm
import pickle

# generater = Generator(U=100,I=8000,K=8)
class Generator():
    def __init__(self, U, I, K, item_num_s = 200, noise_rate = 0.3, sigma = None, seq_num = 1):
        np.random.seed(seed=2021)
        random.seed(2021)

        self.U = U
        self.I = I
        self.K = K
        self.noise_rate = noise_rate
        self.p_min = (1/K) * self.noise_rate
        self.S     = int(np.log2(K)) + 1
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
        self.user_topic     = self._creage_user_topic()
        self.bow            = self._create_bow()
        self.sequential_bow = self._create_sequential_bow()
        self.random_user_topic = self._create_random_user_topic()
        self.seq_random_bow    = self._create_sequential_random_bow()

    
    def _vaild_sigma(self):
        try:
            self.sigma
            print(self.sigma)
        except AttributeError:
            self.sigma = [ [] for k in range(self.K) ]
            for k in range(self.K):
                self.sigma[k] = self.I / (self.K*3)
            print(self.sigma)
                
    def _creage_user_topic(self):
        user_topic = defaultdict(dict)
        for u in range(self.U):
            user_topic[u][0] = [z for z in range(self.K)]

        for u in range(self.U):
            for s in range(self.S-1):
                topic_pre = user_topic[u][s]
                k_s = int(len(topic_pre)/2)
                topic = random.sample(topic_pre, k_s)
                user_topic[u][s+1] = topic   
        return user_topic
    
    def _create_random_user_topic(self):
        random_user_topic = defaultdict(dict)
        Z = [ z for z in range(self.K) ]
        Z_u = [ [] for u in range(self.U) ]
        n_zs = int(self.K / self.S)
        for u in range(self.U):
            Z_u[u] = random.sample(Z, len(Z))
        for u in range(self.U):
            for s in range(self.S):
                random_user_topic[u][s] = Z_u[u][ s*n_zs : (s+1)*n_zs ]
        self.random_user_topic = random_user_topic
        return random_user_topic
    
    def _sampling_topics(self, topics, sample_size=None):
        if sample_size is None:
            sample_size = self.item_num_s
        theta_u = np.full(self.K, self.p_min)
        for t in topics:
            theta_u[t] = (1-self.p_min*(self.K-len(topics))) / len(topics)
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
                    i = self._sampling_item(z)
                    bow[u].append(i)
        return bow
    
    def _create_sequential_random_bow(self):
        seq_random_bow = [ [] for u in range(self.U) ]
        sample_size = self.item_num_s / self.seq_num
        for s in range(self.S):
            for u in range(self.U):
                Z_u = self._sampling_topics(self.random_user_topic[u][s], sample_size=sample_size)
                for z in Z_u:
                    for _ in range(self.seq_num):
                        i = self._sampling_item(z)
                        seq_random_bow[u].append(i)
        return seq_random_bow 

    def _create_sequential_bow(self):
        sequential_bow = [ [] for u in range(self.U) ]
        sample_size = self.item_num_s / self.seq_num
        for s in range(self.S):
            for u in range(self.U):
                Z_u = self._sampling_topics(self.user_topic[u][s], sample_size=sample_size)
                for z in Z_u:
                    for _ in range(self.seq_num):
                        i = self._sampling_item(z)
                        sequential_bow[u].append(i)
        return sequential_bow
    
    def user_topic_dictribution(self):
        Theta = np.full([self.S, self.U, self.K], self.p_min)
        for s in range(self.S):
            for u in range(self.U):
                topics = self.user_topic[u][s]
                for t in topics:
                    Theta[s,u,t] = (1-self.p_min*(self.K-len(topics))) / len(topics)
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
            plt.hist(bow_u[self.item_num_s*s:self.item_num_s*(s+1)], bins=bins)
            plt.title('u = {}, s={}'.format(u, s))
            plt.show()
            plt.close('all')
    
    def show_random_user_distribution(self, u):
            bow_u = self.seq_random_bow[u]
            bins  = self.K*10
            for s in range(self.S):
                plt.hist(bow_u[self.item_num_s*s:self.item_num_s*(s+1)], bins=bins, range=(0,self.I))
                plt.title('u = {}, s={}'.format(u, s))
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
    
    def del_first_step_bow(self, step=0):
        bow_new = [ [] for u in range(self.U) ]
        for u in range(self.U):
            bow_new[u] = self.bow[u][self.item_num_s*(step+1):]
        return bow_new

    def del_first_step_sequential_bow(self, step=0):
        bow_new = [ [] for u in range(self.U) ]
        for u in range(self.U):
            bow_new[u] = self.sequential_bow[u][self.item_num_s*(step+1):]
        return bow_new

    def del_first_step_seq_random_bow(self, step=0):
        bow_new = [ [] for u in range(self.U) ]
        for u in range(self.U):
            bow_new[u] = self.seq_random_bow[u][self.item_num_s*(step+1):]
        return bow_new