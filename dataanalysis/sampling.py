# -*- coding: utf-8 -*-

import random
import csv

def generate_list_of_samples(population_size, sample_size, nsamples):
    samples = []
    for i in range(nsamples):
        sample = generate_sample(population_size, sample_size)
        samples.append(sample)
    return samples
        
def generate_sample(population_size, sample_size):
    
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