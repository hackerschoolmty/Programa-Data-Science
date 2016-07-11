#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pandas import read_csv as read_csv, cut
from numpy import arange, log

class BayesModel():
  def __init__(self):
    self.df = read_csv('data/german.data.all-numeric.csv', header=0)
    self.df_trainning = self.df.sample(frac=0.7, replace=False, random_state=1)
    self.df_good = self.df_trainning[self.df_trainning['is_good'] == 1]
    self.df_bad = self.df_trainning[self.df_trainning['is_good'] != 1]

  def histogram_cate(self, varname, df):
    # Histograms for variables numeric
    var_min = df[varname].min()
    var_max = df[varname].max()
    var_range = range(var_min,var_max+1,1)
    hvar = cut(df[varname], bins=var_range, labels= False)
    return hvar

  def histogram_cont(self, varname, df, nbins = 10.0):
    # Histograms for continuos variables
    var_min = df[varname].min()
    var_max = df[varname].max()
    nbins = nbins
    binsize = 1.0 * (var_max - var_min) / nbins
    var_range = arange(var_min, var_max+binsize, binsize)
    hvar = cut(df[varname], bins=var_range)
    return hvar

  def score(self, cac = None,
                  crh = None,
                  prp = None,
                  amount = None,
                  pet = None,
                  prt = None,
                  age = None):
    self.variables = {
      'checking_acc_numeric': cac,
      'credit_history_numeric': crh,
      'purpose_numeric': prp,
      'amount': amount,
      'p_employment_time_numeric': pet,
      'p_residence_time':  prt,
      'age': age
    }
    pxb = 1.0
    pxg = 1.0
    pgb = 1.0 * self.df_good.shape[0] / self.df_bad.shape[0]
    for k, v in self.variables.items():
      if "numeric" in k:
        hg = self.histogram_cate(k,self.df_good)
        hb = self.histogram_cate(k,self.df_bad)
        if self.variables[k] in hg.value_counts(normalize=True):
          pxg *= hg.value_counts(normalize=True)[self.variables[k]]
        else:
          pxg *= pgb
        if self.variables[k] in hb.value_counts(normalize=True):
          pxb *= hb.value_counts(normalize=True)[self.variables[k]]
        else:
          pxb *= 1.0
      else:
        hg = self.histogram_cont(k,self.df_good)
        hb = self.histogram_cont(k,self.df_bad)
        if self.variables[k] in hg.value_counts(normalize=True):
          pxg *= hg.value_counts(normalize=True)[self.variables[k]]
        else:
          pxg *= pgb
        if self.variables[k] in hb.value_counts(normalize=True):
          pxb *= hb.value_counts(normalize=True)[self.variables[k]]
        else:
          pxb *= 1.0
    return log(pgb * pxg / pxb)
