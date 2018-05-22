from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np

def diff_segmentation(diff_epslon, P, step, path, data, PPA_mean, indices, plot):
    '''get segments based on change point detection
    Args:
        diff_epslon: user defined threshold for change point, small value
        P: name of variables (sensor/actuators)
        step: not used in this version
        step: figure saving path
        data: original multivariate dataframe
        PPA_mean: denoised (averaged) data as input
        indices: list of starting and ending index of each averating chunk
        plot: yes/no to output plot
    '''
    head = 0
    shift = head+1
    diff_seg_sum = 0
    diff_seg_mean = PPA_mean[0,shift]-PPA_mean[0,head]
    Range = namedtuple('Range', ['start', 'end', 'cost_mean'])
    R = list()
    diff = list()
    while True:
        if abs((PPA_mean[0,shift]-PPA_mean[0,shift-1])-diff_seg_mean) <= diff_epslon:
            diff_seg_sum += (1.0*(PPA_mean[0,shift]-PPA_mean[0,shift-1]))
            diff_seg_mean = 1.0*diff_seg_sum/(shift-head)
            shift += 1
            if shift == PPA_mean.shape[1]-1:
                r = Range(start=indices[head][0], end=indices[shift][1], cost_mean=diff_seg_mean)
                diff.append(r.cost_mean)
                R.append(r)
                break
        else:
            r = Range(start=indices[head][0], end=indices[shift-1][1], cost_mean=1.0*diff_seg_sum/(shift-1-head))
            diff.append(r.cost_mean)
            R.append(r)
            head = shift
            shift = head+1
            if shift == PPA_mean.shape[1]-1:#last segment contains last two data points
                r = Range(start=indices[head][0], end=indices[shift][1], cost_mean=PPA_mean[0, PPA_mean.shape[1]-1]-PPA_mean[0, PPA_mean.shape[1]-2])
                R.append(r)
                diff.append(r.cost_mean)
                break
            diff_seg_sum = 0
            diff_seg_mean = PPA_mean[0, shift]-PPA_mean[0,head]
    if plot == True:
        plt.figure()
        for i in range(1, len(P)+1):
            plt.subplot(len(P), 1, i)
            if i == len(P):
                plt.plot(data[P[-1]].values, 'b')
                for j in range(len(R)):
                    plt.plot([R[j].start, R[j].start], [np.min(data[P[-1]]), np.max(data[P[-1]])], 'r', linewidth=0.2)
                    plt.xlabel('Time /s')
                    plt.ylabel(P[-1])
            else:
                plt.plot(data[P[i-1]].values, 'b')
                for j in range(len(R)):
                    plt.plot([R[j].start, R[j].start], [np.min(data[P[i-1]]), np.max(data[P[i-1]])], 'r', linewidth=0.2)
                    plt.xlabel('Time /s')
                    plt.ylabel(P[i-1])
        plt.savefig(path)
        plt.close()
    return np.array(diff).reshape(1,len(diff)), R