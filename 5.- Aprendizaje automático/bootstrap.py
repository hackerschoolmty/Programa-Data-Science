from numpy import array, cumsum
from pandas import cut

def bootstrapped_utility(df_testing=None,varname=None, bins = None):
  N = 1500
  MKT = 500000
  S_bin = 6000
  L_bin = 3000
  IT_bin = 0.20
  IP_bin = 0.40
  df_bs = df_testing.sample(frac=1, replace=True)
  df_bs_good = df_bs[df_bs['is_good']==1]
  df_bs_bad = df_bs[df_bs['is_good']!=1]
  hbs_good = cut(df_bs_good[varname], bins=bins)
  hbs_bad = cut(df_bs_bad[varname], bins=bins)
  bs_purity_by_bin = []
  bs_efficiency_by_bin = []
  for g in range(0,len(hbs_good.value_counts())):
    sum_g_b = hbs_good.value_counts()[g] + hbs_bad.value_counts()[g]
    if sum_g_b !=0:
      bs_purity_by_bin.append(1.0*hbs_good.value_counts()[g]/sum_g_b)
    else:
      bs_purity_by_bin.append(1.0*hbs_good.value_counts()[g])
    bs_efficiency_by_bin.append(1.0*sum_g_b/(hbs_good.size+hbs_bad.size))
  bs_purity_by_bin = array(bs_purity_by_bin)
  bs_default_by_bin = -1*(bs_purity_by_bin - 1.0)
  bs_efficiency_by_bin = array(bs_efficiency_by_bin)
  bs_DC_bin = N * bs_efficiency_by_bin * bs_default_by_bin * L_bin
  bs_RT_bin = N * bs_efficiency_by_bin * bs_purity_by_bin * S_bin * IT_bin
  bs_RP_bin = N * bs_efficiency_by_bin * bs_default_by_bin * (S_bin - L_bin) * IP_bin
  bs_f_bin = bs_RT_bin + bs_RP_bin - bs_DC_bin
  bs_f = cumsum(bs_f_bin[::-1])[::-1] - MKT
  return bs_f