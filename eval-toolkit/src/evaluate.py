#!/usr/bin/env python
#
# Evaluation toolkit for the Human-to-Robot Handovers track at the 10th 
# Robotic Grasping and Manipulation Competition at ICRA 2025.
#
################################################################################## 
# Author: 
#   - Alessio Xompero: a.xompero@qmul.ac.uk
#
#  Created Date: 2024/03/24
# Modified Date: 2024/12/20
#
# MIT License

# Copyright (c) 2024 Alessio Xompero

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#--------------------------------------------------------------------------------

import os
import csv
import math

import numpy as np
import pandas as pd


from scipy.spatial import distance

from sklearn import metrics
import argparse 
import copy 

from pdb import set_trace as bp


class CorsmalEvaluationToolkit():
	def __init__(self, teamname):

		# Number of configurations
		self.n_config = 24 

		# Maximum allowed time to execute a handover configuration (in milliseconds). Default is 5 seconds. 
		self.tau=5000 

		self.teamname = teamname

	def set_time_threshold(self, time_th):
		self.tau = time_th

	def read_submission(self, submission_fn):
		''' Read submission.
		'''
		est = pd.read_csv(submission_fn, sep=',', index_col=False)

		assert(est.shape[0] == self.n_config)

		self.team_preds = est


	def load_preassigned_weights(self, phase):
		'''
		'''
		assert phase in ["preparation","competition"]

		if phase == "preparation":
			df = pd.read_csv(os.path.join('resources','weights_configs_prep.csv'), 
				index_col=False, header=None)
		elif phase == "competition":
			df = pd.read_csv(os.path.join('resources','weights_configs_competition.csv'), 
				index_col=False, header=None)

		weights = df.values

		return weights

	def compute_euclidean_distances(self, est):
		'''
		'''
		# Target location
		t_pos_x = est['t_pos_x'].values
		t_pos_y = est['t_pos_y'].values

		t_pos = np.zeros((2,self.n_config))
		t_pos[0,:] = t_pos_x
		t_pos[1,:] = t_pos_y
		

		# Final location
		f_pos_x = est['f_pos_x'].values
		f_pos_y = est['f_pos_y'].values

		f_pos = np.zeros((2,self.n_config))
		f_pos[0,:] = f_pos_x
		f_pos[1,:] = f_pos_y
		
		# https://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
		f_min_t = f_pos - t_pos
		
		euc_dist = np.sqrt(np.einsum('ij,ij->j', f_min_t, f_min_t))

		return euc_dist

	def compute_delivery_location(self, est, rho=500):
		'''

		- Target location [mm]	
		- Final location [mm]
		- Distance [mm]	
		- Handover time [ms]	
		- Initial mass [g]	
		- Final mass [g]

		'''
		euc_dist = self.compute_euclidean_distances(est)
		euc_dist[np.isnan(euc_dist)] = 1000

		est_euc_dist = est['Distance [mm]'].values
		est_euc_dist[np.isnan(est_euc_dist)] = 1000

		# assert((np.round(est_euc_dist,3) == np.round(euc_dist,3)).all())

		invalid_dist = np.where(euc_dist >= rho)

		delta = 1 - euc_dist / rho	
		delta[invalid_dist] = 0

		return delta


	def compute_execution_time_scores(self, est, tau=5000, eta=1000):
		'''

			- tau is a threshold that defines when an algorithm is unsuccessful for that measure and here represents the maximum allowed execution time. Default value: 5,000 ms.
			- eta is the minimum expected time to perform a handover. Default value: 1,000 ms.
		'''
		exec_times = est['Handover time [ms]'].values
		exec_times[np.isnan(exec_times)] = tau

		invalid_times = np.where(exec_times >= tau)

		gamma = 1 - (np.maximum(exec_times, eta) - eta) / (tau-eta)
		gamma[invalid_times] = 0

		return gamma

	def compute_mass_scores(self, est):
		'''
		'''
		mass_init = est['Initial mass [g]'].values
		mass_final = est['Final mass [g]'].values

		mass_final[np.isnan(mass_final)] = 0

		mass_diff = np.abs(mass_final - mass_init)

		invalid_mass = mass_diff >= mass_init

		mu_score = 1 - mass_diff / mass_init
		mu_score[invalid_mass] = 0

		return mu_score

	def compute_benchmark_score(self, delta, gamma, mu_score, phase):
		'''
		'''
		weights = self.load_preassigned_weights(phase)

		valid_configs = (gamma > 0).astype(int)

		tmp = np.multiply(weights.transpose(), ((delta + gamma + mu_score) / 3))

		S = np.matmul(tmp, valid_configs.transpose()) / 3

		config_scores = np.multiply(valid_configs, tmp)

		return S[0], config_scores, tmp


	def save_team_score(self, outfn, S):
		'''
		'''
		if not os.path.exists(outfn):
	  		results_file = open(outfn, 'w')
	  		results_file.write('Team,Score\n')
	  		results_file.write('{:s},{:.2f}\n'.format(self.teamname,S))
	  		results_file.close()
		else:
			results_file = open(outfn, 'a')
			results_file.write('{:s},{:.2f}\n'.format(self.teamname,S))
			results_file.close()

	def save_team_score_config(self, outfn, config_scores):
		'''
		'''
		if not os.path.exists(outfn):
	  		results_file = open(outfn, 'w')
	  		results_file.write('Team')
	  		for x in range(self.n_config):
	  			results_file.write(',C{:d}'.format(x))
	  		results_file.write('\n')
	  		
	  		results_file.write('{:s}'.format(self.teamname))
	  		for x in range(self.n_config):
	  			results_file.write(',{:.2f}'.format(config_scores[x]))
	  		results_file.write('\n')
	  		
	  		results_file.close()
		else:
			results_file = open(outfn, 'a')

			results_file.write('{:s}'.format(self.teamname))
			for x in range(self.n_config):				
				results_file.write(',{:.2f}'.format(config_scores[x]))
			results_file.write('\n')

			results_file.close()


	def run(self, submission_fn, phase):
		'''
		'''
		self.read_submission(submission_fn)

		delta = self.compute_delivery_location(self.team_preds)
		gamma = self.compute_execution_time_scores(self.team_preds, tau=self.tau)
		mu_score = self.compute_mass_scores(self.team_preds)

		S, config_scores, config_scores2 = self.compute_benchmark_score(delta, gamma, mu_score, phase)

		print("The benchmark score of the team {:s} is {:.2f}".format(self.teamname,S))

		self.save_team_score('leaderboard.csv',S)
		self.save_team_score_config('config_scores.csv',config_scores.squeeze())
		self.save_team_score_config('config_scores2.csv',config_scores2.squeeze())


def GetParser():
	parser = argparse.ArgumentParser(description='CORSMAL Evaluation Toolkit')
	parser.add_argument('--submission', type=str)
	parser.add_argument('--teamname', type=str)
	parser.add_argument('--phase', type=str, required=True)
	parser.add_argument('--time_th', type=int)

	return parser



if __name__ == '__main__':

	# Arguments
	parser = GetParser()	
	args = parser.parse_args()

	toolkit = CorsmalEvaluationToolkit(args.teamname)

	if args.time_th:
		toolkit.set_time_threshold(args.time_th)

	toolkit.run(args.submission, args.phase)

