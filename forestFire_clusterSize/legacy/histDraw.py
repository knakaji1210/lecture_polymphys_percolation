# Histgram Drawing 

import numpy as np
import matplotlib.pyplot as plt

def histDraw(fig, hist_title, hist_color, input_list):

    num_bins = 100

    ax = fig.add_subplot(122,title=hist_title)
    hist = plt.hist(input_list, bins=num_bins, color=hist_color, density=False)
    histMin, histMax = plt.xlim()
    binWidth = (histMax - histMin) / num_bins
    hist_y = np.array(hist[0])
    hist_x = np.array(hist[1])
    histInfo = [histMin, histMax, binWidth]

    return hist_x, hist_y, histInfo