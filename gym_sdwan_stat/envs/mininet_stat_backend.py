#! /usr/bin/python 

import time, os

import numpy as np
import logging

class MininetStatBackEnd(object):

    def init_params(self, mu, sigma, link_bw, sla_bw):
        self.mu = float(mu)
        self.sigma = float(sigma)
        self.sla_bw = float(sla_bw)

        self.link_bw = float(link_bw)
     
    def reset_links(self):
        self.current_link_failure = False
        self.previous_link_failure = False

        self.active_link = 0 # internet by default
        self.episode_over = False

        self.take_measurements()

    def __init__(self, mu, sigma, link_bw, sla_bw, seed):

        np.random.seed(seed)

        self.init_params(mu, sigma, link_bw, sla_bw)

        self.reset_links()


    def cleanup(self):
        pass


    def take_measurements(self):
        """ Send udp traffic and then take bandwidth measurement """

        # send udp traffic  - simulate other flow
      
        udp_bw = np.random.normal(self.mu, self.sigma) 
        
        # always measure internet link available bw
        self.available_bw = float(self.link_bw) - float(udp_bw)

        if self.available_bw < 0.0:
            self.available_bw = 0.0

        ## we measure  internet link only, MPLS link => full BW 
        if self.active_link == 0:   
            self.current_bw = np.random.normal(self.available_bw, 0.5)
        else:
            self.current_bw = self.link_bw
        

        
    
   
    def switch_link(self, action):

           ## action is 0 => link is internet
        ## action 1 => MPLS 
        self.active_link  = action

        self.take_measurements()

        ## Here is the logic that checks  two subsequent SLA failures
        self.current_link_failure = False

        # if current bandwidth less than SLA it is a failure
        if self.active_link == 0:
            if float(self.current_bw) < float(self.sla_bw):
                logging.info ('current link failure')
                self.current_link_failure = True

                # if it failed in previous tick also, mark it a link failure
                if  self.previous_link_failure == True:
                    logging.info ('previous link also failure, episode over')
                    self.episode_over = True
            
        # copy current to previous
        self.previous_link_failure = self.current_link_failure 
        
        return self.episode_over 

    def print_state(self):
        print ('active_link = ', be.active_link, 
                    'current_bw = ', be.current_bw,  'available bw = ', be.available_bw)
        

        
    
if __name__ == '__main__':
    setLogLevel( 'error' )
    be = MininetBackEnd(mu=5, sigma=2, link_bw=10, sla_bw=6, seed=100)
    be.print_state()

    be.switch_link(action=1)
    be.print_state()

    be.switch_link(action=0)
    be.print_state()

    be.switch_link(action=1)
    be.print_state()

    be.switch_link(action=0)
    be.print_state()

    be.cleanup()
 
