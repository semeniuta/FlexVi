# -*- coding: utf-8 -*-

def compute_frequencies(data, nbins):
    minval = min(data)
    maxval = max(data)
    delta = (maxval - minval) / nbins    
        
    bins = [minval]
    for i in range(nbins):
        bins.append(bins[i] + delta)
    bins[-1] += 2 * maxval
        
    freqs = [0 for i in range(nbins)]
    
    for numb in data:     
        for i in range(nbins):
            if numb >= bins[i] and numb < bins[i+1]:
                freqs[i] += 1
                break
        
    bins[-1] = maxval
    
    return freqs, bins