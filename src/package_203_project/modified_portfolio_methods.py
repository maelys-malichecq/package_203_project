import pandas as pd
import logging
from dataclasses import dataclass
from datetime import datetime
import plotly.graph_objects as go
import os 
import pickle
from pybacktestchain.data_module import UNIVERSE_SEC, FirstTwoMoments, get_stocks_data, DataModule, Information
from pybacktestchain.utils import generate_random_name
from pybacktestchain.blockchain import Block, Blockchain
from numba import jit 
from datetime import timedelta, datetime
from pybacktestchain.broker import EndOfMonth, StopLoss, Broker
import plotly.graph_objects as go
from scipy.stats import kurtosis, skew
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import numpy as np


@dataclass
class SharpeRatioMaximization(Information):
    def compute_portfolio(self, t: datetime, information_set):
        try:
            mu = information_set['expected_return']
            Sigma = information_set['covariance_matrix']
            risk_free_rate = 0.02  # TO CORRECT SO THAT IS REAL RATE
            n = len(mu)
            
            # Objective: maximise sharpe ratio 
            obj = lambda x: - (x.dot(mu) - risk_free_rate) / np.sqrt(x.dot(Sigma).dot(x))  
            
            # Same constraint, sum of weight = 1
            cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1}) 

            # still no short sale allowed
            bounds = [(0.0, 1.0)] * n
            
            # Initial param
            x0 = np.ones(n) / n
            
            # Minimise the sharpe ratio if negative
            res = minimize(obj, x0, constraints=cons, bounds=bounds)

            
            portfolio = {k: None for k in information_set['companies']}

            # If optimisation converged 
            if res.success:
                for i, company in enumerate(information_set['companies']):
                    portfolio[company] = res.x[i]
            else:
                raise Exception("L'optimisation n'a pas convergé")

            return portfolio
        except Exception as e:
            # Otherwise get the equal weight portfolio as in FirstMoment
            logging.warning("Error")
            logging.warning(e)
            return {k: 1 / len(information_set['companies']) for k in information_set['companies']}

    def compute_information(self, t: datetime):
        # Get the data module 
        data = self.slice_data(t)
        # the information set will be a dictionary with the data
        information_set = {}

        # sort data by ticker and date
        data = data.sort_values(by=[self.company_column, self.time_column])

        # expected return per company
        data['return'] = data.groupby(self.company_column)[self.adj_close_column].pct_change()
        
        # expected return by company 
        information_set['expected_return'] = data.groupby(self.company_column)['return'].mean().to_numpy()

        # covariance matrix

        # 1. pivot the data
        data = data.pivot(index=self.time_column, columns=self.company_column, values=self.adj_close_column)
        # drop missing values
        data = data.dropna(axis=0)
        # 2. compute the covariance matrix
        covariance_matrix = data.cov()
        # convert to numpy matrix 
        covariance_matrix = covariance_matrix.to_numpy()
        # add to the information set
        information_set['covariance_matrix'] = covariance_matrix
        information_set['companies'] = data.columns.to_numpy()
        
        return information_set


@dataclass
class EqualWeightPortfolio(Information):
    def compute_portfolio(self, t: datetime, information_set):
        try:
            # Number of assets
            n = len(information_set['companies'])

            # Equal weight
            equal_weight = 1 / n

            portfolio = {company: equal_weight for company in information_set['companies']}

            return portfolio
        except Exception as e:
            logging.warning(f"Error computing portfolio, returning equal weight portfolio : {e}")
            return {company: 1 / len(information_set['companies']) for company in information_set['companies']}

    def compute_information(self, t: datetime):
        # Get the data module 
        data = self.slice_data(t)
        # the information set will be a dictionary with the data
        information_set = {}

        # sort data by ticker and date
        data = data.sort_values(by=[self.company_column, self.time_column])

        # expected return per company
        data['return'] = data.groupby(self.company_column)[self.adj_close_column].pct_change()

        # expected return by company
        information_set['expected_return'] = data.groupby(self.company_column)['return'].mean().to_numpy()
        
        # covariance matrix

        # 1. pivot the data
        data = data.pivot(index=self.time_column, columns=self.company_column, values=self.adj_close_column)
        # drop missing values
        data = data.dropna(axis=0)
        # 2. compute the covariance matrix
        covariance_matrix = data.cov()
        # convert to numpy matrix 
        covariance_matrix = covariance_matrix.to_numpy()

        # add to the information set
        information_set['covariance_matrix'] = covariance_matrix
        information_set['companies'] = data.columns.to_numpy()

        return information_set
