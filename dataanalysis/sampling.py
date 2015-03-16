# -*- coding: utf-8 -*-

import random
import csv
from math import factorial
import itertools
import numpy as np

CRITICAL_NCOMB = 500000

def ncomb(N, m):
    '''
    Number of m-combinations from range(N)
    '''
    return factorial(N)/(factorial(m)*factorial(N - m))

def generate_all_combinations(N, m):
    if ncomb(N, m) >= CRITICAL_NCOMB:
        raise Exception('The number of combinations would exceed the critical value')
    return list(itertools.combinations(range(N), m))

def generate_list_of_samples(population_size, sample_size, nsamples):

    nc = ncomb(population_size, sample_size)
    if nsamples >= nc:
        nsamples = nc
        return generate_all_combinations(population_size, sample_size)
    
    samples = []
    
    while len(samples) < nsamples:
        sample = generate_sample(population_size, sample_size)
        
        duplicate_found = False
        for j in range(len(samples)):
            if sample == samples[j]:
                duplicate_found = True
                break
        
        if not duplicate_found:
            samples.append(sample)
    
    return samples
                
def generate_sample(population_size, sample_size):
    
    if population_size <= sample_size:
        raise Exception("population_size <= sample_size")
    
    sample = []
    while len(sample) < sample_size:
        rnd = random.randint(0, population_size - 1)
        if rnd not in sample:
            sample.append(rnd)    
    
    return sorted(sample)

def write_samples_to_file(samples, filename):
    with open(filename, 'wb') as f:    
        w = csv.writer(f)    
        for s in samples:
            w.writerow(s)

def read_samples_from_file(filename):
    res = []    
    with open(filename, 'rb') as f:
        r = csv.reader(f)
        for row in r:
            row_int = map(lambda x: int(x), row)
            res.append(row_int)
    return res
    
if __name__ == '__main__':
    ls = generate_list_of_samples(40, 18, 2000)
    #d = check_for_duplicates(ls)