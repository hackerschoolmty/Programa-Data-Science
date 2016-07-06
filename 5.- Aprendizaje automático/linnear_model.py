#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pandas import read_csv
from numpy import linalg, array

class LinnearModel():
  def __init__(self, varnames = []):
    self.df = read_csv('data/german.data.all-numeric.csv', header=0)
    varnames.append("is_good")
    self.df = self.df[varnames]
    self.df['is_good'] = 2.0 - self.df['is_good']
    self.df_training = self.df.sample(frac=0.7, replace=False, random_state=1)
    self.df_training['ones'] = 1.0
    varnames = varnames[::-1]
    varnames.append('ones')
    self.varnames = varnames[::-1]
    self.df_good = self.df_training[self.df_training['is_good'] == 1]
    self.df_bad = self.df_training[self.df_training['is_good'] != 1]

  def train(self):
    i = 0
    xtx = [[0 for i in range(len(self.varnames)-1)] for i in range(len(self.varnames)-1)]
    xty = [0 for i in range(len(self.varnames)-1)]
    for var1 in self.varnames:
      j = 0
      for var2 in self.varnames:
        if var2 == 'is_good': continue
        if var1 == 'is_good':
          xty[j] = sum(self.df_training[var1] * self.df_training[var2])
        else:
          xtx[i][j] = sum(self.df_training[var1] * self.df_training[var2])
        j += 1
      i += 1
    invxtx = linalg.inv(xtx)
    self.betas = invxtx.dot(xty)

  def score(self, vars={}):
    values = [1]
    for var in self.varnames:
      if var == 'ones' or var == 'is_good': continue
      values.append(vars[var])
    score = sum(array(self.betas) * array(values))
    return score

if __name__ == "__main__":
  varnames =['amount', 'savings_acc_numeric', 'p_employment_time_numeric', 'installment_rate', 'p_residence_time',
             'age', 'number_of_credits', 'dependants', 'has_phone_numeric', 'foreign_worker_numeric']
  lm = LinnearModel(varnames=varnames)
  lm.train()
  vars = {'amount': 1000, 'savings_acc_numeric': 1, 'p_employment_time_numeric': 3, 'installment_rate': 4,
          'p_residence_time': 3, 'age': 36, 'number_of_credits': 2, 'dependants': 1, 'has_phone_numeric': 1,
          'foreign_worker_numeric': 0}
  score = lm.score(vars)
  print(score)