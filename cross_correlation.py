#https://github.com/scipy/scipy/blob/v1.6.0/scipy/signal/signaltools.py#L1694-L1791
# - source code for the signal.correlate2d function. Calls sigtools._convolve2d to get output
#https://github.com/scipy/scipy/blob/08b992ddeeb2ee5f61b15a72bac1cf82fea9d9e6/scipy/signal/sigtoolsmodule.c
# - contains the sigtools_convolve2d function, written in C, which then calls pylab_convolve_2d after checking for errors with input
#https://github.com/scipy/scipy/blob/5f4c4d802e5a56708d86909af6e5685cd95e6e66/scipy/signal/firfilter.c
# - source code for pylab_convolve_2d