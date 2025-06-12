from RamseySimulation import RamseySimulation as ramsey 
from HahnEchoSimulation import HahnEchoSimulation as echo 
from SaveResult import save_bloch_gif, save_signal_gif
import numpy as np


#INITIALIZE PARAMETERS
#constant
w0 = 2 * 2 * np.pi 				# Qubit frequrncy, GHz
W = 0.05 * 2 * np.pi 			# Microwave power, GHz
M = 100							# Number of points
taus = np.linspace(0, 1000, M)	# Free precision time, ns
detune = 0 						# Detuning

#DEFINE CASES
cases = {
    "Case 1: low frequency, weak AC field" 			: {'gamma': 0.001*2*np.pi,      'w': 0.01*2*np.pi},
    "Case 2: low frequency, stronger AC field" 		: {'gamma': 0.005*2*np.pi,     	'w': 0.01*2*np.pi},
    "Case 3: higher frequency, weak AC field" 		: {'gamma': 0.001*2*np.pi,      'w': 0.05*2*np.pi},
    "Case 4: higher frequency, stronger AC field" 	: {'gamma': 0.005*2*np.pi,     	'w': 0.05*2*np.pi},
}


#Cases 1
gamma = cases["Case 1: low frequency, weak AC field"]["gamma"]
w = cases["Case 1: low frequency, weak AC field"]["w"] 

#Cases 2
# gamma = cases["Case 2: low frequency, stronger AC field"]["gamma"]
# w = cases["Case 2: low frequency, stronger AC field"]["w"]

# #Cases 3
# gamma = cases["Case 3: higher frequency, weak AC field"]["gamma"]
# w = cases["Case 3: higher frequency, weak AC field"]["w"]

# #Cases 4
# gamma = cases["Case 4: higher frequency, stronger AC field"]["gamma"]
# w = cases["Case 4: higher frequency, stronger AC field"]["w"]


#Perform simulation
wm = (1 + detune) * w0
signal = []
sx_list, sy_list, sz_list = [], [], []
N = 0

for tau in taus:
	echo1 = echo(w0, wm, W, w, gamma, tau)
	n, sx, sy, sz = echo1.simulateHahnEcho()

	signal.append((sz[-1] + 1) / 2)
	sx_list.extend(sx)
	sy_list.extend(sy)
	sz_list.extend(sz)
	N+=n

#Do not forget to change the file name before running the program,
#this will overwrite previously saved file --> fix later: automatically change the filename

save_bloch_gif(N, sx_list, sy_list, sz_list, '../quantum_sensing_homework/data/ebloch_sphere_case11.gif')
save_signal_gif(taus, signal, '../quantum_sensing_homework/data/echo_signal_case11.gif')
