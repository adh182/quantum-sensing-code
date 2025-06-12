import qutip as qt 
import numpy as np
from Initialization import Initialization
 

class Simulation(Initialization):
	#define pulse sequence
	echo_sequence = [[0.5, 1, 0.5], [0,0,0], [1,1], 'Echo'] #pi/2 x - pi x - pi/2 x
	ramsey_sequence = [[0.5, 0.5], [0,0], [1], 'Ramsey'] #pi/2 x - pi/2 x
	t1_sequence = [[1], [0], [1], 't1']	# pi x

	def __init__(self, w0, wm, W, w, gamma, tau):
		'''
		Parameters:
			tau 	: evolution time
		'''
		super().__init__(w0, wm, W, w, gamma)
		self.tau = tau

	def simulateEcho(self):
		'''
		Performs Hahn-Echo simulation with noise
		Returns:
			number of time points
			spin evolution

		'''

		total_tau = np.sum(self.echo_sequence[2])

		N, sx, sy, sz = self.Sequence(self.echo_sequence, self.tau/total_tau)

		return N, sx, sy, sz

	def simulateRamsey(self):
		'''
		Performs Ramsey simulation with noise
		Returns:
			number of time points
			spin evolution

		'''
		total_tau = np.sum(self.ramsey_sequence[2])

		N, sx, sy, sz = self.Sequence(self.ramsey_sequence, self.tau/total_tau)

		return N, sx, sy, sz

	def simulateRabi(self, RWA=False):
		'''
		Performs Rabi simulation with noise
		Parameters:
			RWA		: Rotating Wave Approximation, default=False
		Returns:
			spin evolution

		'''
		a = 1
		psi = (a * qt.basis(2, 0) + (1 - a) * qt.basis(2, 1)).unit()
		phi = 0 * np.pi

		if RWA:
			sx, sy, sz = self.RotatingFrame(psi, self.tau, phi)
		else:
			sx, sy, sz = self.LabFrame(psi, self.tau, phi)

		return len(sx), sx, sy, sz

	def simulateT1Relaxation(self):
		'''
		Performs T1 relaxation simulation with noise
		Returns:
			number of time points
			spin evolution
		'''
		total_tau = np.sum(self.t1_sequence[2])

		N, sx, sy, sz = self.Sequence(self.t1_sequence, self.tau/total_tau)

		return N, sx, sy, sz