#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from bisect import bisect_right as bisect

def score_card(tca=None, amount=None,pet=None,age=None):
  tca_hash = {0: 7, 20: 3, 40: 0, 60: 0, 80: 0}
  amount_hash = {1: 7, 5000: 1, 10000: 0, 15000: 0, 20000: 0}
  pet_hash = {1: 1, 2: 1, 3: 6, 4: 8, 5: 8}
  age_hash = {18: 3, 34: 5, 50: 3, 66: 3, 83: 0}

  # Using bisect right to chose (min,max], substracting 1 to choose the correct index
  tca_category = bisect(sorted(list(tca_hash.keys())),tca) - 1
  tca_score = tca_hash[sorted(list(tca_hash.keys()))[tca_category]]

  amount_category = bisect(sorted(list(amount_hash.keys())),amount) - 1
  amount_score = amount_hash[sorted(list(amount_hash.keys()))[amount_category]]

  pet_category = bisect(sorted(list(pet_hash.keys())),pet) - 1
  pet_score = pet_hash[sorted(list(pet_hash.keys()))[pet_category]]

  age_category = bisect(sorted(list(age_hash.keys())),age) - 1
  age_score = age_hash[sorted(list(age_hash.keys()))[age_category]]

  thescore = tca_score + amount_score + pet_score + age_score
  return thescore

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--tca", dest="tca", type=int,
                     action="store", help="time credit account")
  parser.add_argument("-a", "--amount", type=int,
                     action="store", dest="amount", help="amount")
  parser.add_argument("-p", "--pet", type=int,
                      action="store", dest="pet", help="present employment time")
  parser.add_argument("-g", "--age", type=int,
                    action="store", dest="age", help="age")
  args = parser.parse_args()
  argsdict = vars(args)
  if len(argsdict) != 4:
    parser.error("incorrect number of arguments")
  else:
    tca = argsdict['tca']
    amount = argsdict['amount']
    pet = argsdict['pet']
    age = argsdict['age']
    result = score_card(tca=tca, amount=amount, pet=pet, age=age)
    return result

if __name__ == "__main__":
  result = main()
  print(result)