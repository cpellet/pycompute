import PyCompute
import random
import time
import numpy as np

PyCompute.endpoint = "http://57f472b6.ngrok.io/"
PyCompute.username = "cyrus"
PyCompute.password = "ch"
PyCompute.gpu = "Intel HD Graphics 6000"

for i in range (19):
    start = time.time()
    arr1 = np.random.randint(0,10,100000000)
    end = time.time()
    PyCompute.report_CPU_calculation_finished("array_gen", "100000000", end-start, "Numpy, np.add")