#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


if __name__ == "__main__":
  result = score_card(tca=0, amount=5000, pet=4, age=34)
  print(result)