import qutip as qt 
import numpy as np 

class Initialization:
	pauliX = qt.sigmax()
	pauliY = qt.sigmay()
	pauliZ = qt.sigmaz()
	pauliOp = [pauliX, pauliY, pauliZ]

	loweringOp = qt.destroy(2)
	dephasingOp = np.sqrt(2) * qt.Qobj([[0,0],[0,1]])


	def __init__(self, w0, wm, W, w, gamma):
		'''
		Parameters: 
			w0		: qubit frequency / energy splitting (GHz)
			wm		: microwave frequency (GHz)
			W 		: microwave power (GHz)
			w 		: external field frequency (GHz)
			gamma	: phase acumulation speed (GHz)
		'''

		self.w0 = w0
		self.wm = wm
		self.W = W
		self.w = w
		self.gamma = gamma

	def Pulse(self, psi, tlist, phi):
		'''
		Simulate microwave pulse of the system
		Parameters: 
			psi		: initial state vector (ket)
			tlist	: list of time for t
			phi		: phase offset between pulses or relative phase

		Returns:
			final state of the state vector
			expectation values for the times specified by 'tlist'
		'''

		#define collapse operators; relaxation and dephasing
		c_ops = [np.sqrt(self.gamma[1]) * self.loweringOp, np.sqrt(self.gamma[2]) * self.dephasingOp]


		#define the Hamiltonian of the system
		H = ((self.w0-self.wm)*0.5)*self.pauliZ + (self.W*0.5)*(np.cos(phi)*self.pauliX - np.sin(phi)*self.pauliY)

		#solve the Hamiltonian equation
		output = qt.mesolve(H, psi, tlist, c_ops, self.pauliOp, options=qt.Options(store_final_state=True))

		return output.final_state, output.expect[0], output.expect[1], output.expect[2]

	def Phase(self, psi, tlist, phi):
		'''
		Simulates phase accumulationduring free precission time
		Parameters: 
			psi		: initial state vector (ket)
			tlist	: list of time for t
			phi		: phase offset between pulses or relative phase

		Returns:
			final state of the state vector
			expectation values for the times specified by 'tlist'
		'''

		#define collapse operators; relaxation and dephasing
		c_ops = [np.sqrt(self.gamma[1]) * self.pauliX, np.sqrt(self.gamma[2]) * self.dephasingOp]

		#define the Hamiltonian of the system
		H0 = ((self.w0-self.wm)*0.5)*self.pauliZ
		H1 = (self.gamma[0]*0.5)*self.pauliZ
		H = [H0, [H1, lambda t, args: np.cos(self.w*t + phi)]]

		#solve the Hamiltonian equation
		output = qt.mesolve(H, psi, tlist, c_ops, self.pauliOp, options=qt.Options(store_final_state=True))
		
		return output.final_state, output.expect[0], output.expect[1], output.expect[2]


	def LabFrame(self, psi, tlist, phi):
		'''
		Lab frame, physical frame of reference
		Parameters: 
			psi		: initial state vector (ket)
			tlist	: list of time for t
			phi		: phase offset between pulses or relative phase

		Returns:
			expectation values for the times specified by 'tlist'
		'''

		#define collapse operators; relaxation and dephasing
		c_ops = [np.sqrt(self.gamma[1])*self.loweringOp, np.sqrt(self.gamma[2])*self.pauliZ]

		#define Hamiltonian of the system
		H0 = self.w0 * self.pauliZ * 0.5
		H1 = self.W * self.pauliX
		H = [H0, [H1, lambda t, args: np.cos(self.wm*t + phi)]]

		#solve the Hamiltonian equation
		output = qt.mesolve(H, psi, tlist, c_ops, self.pauliOp)

		return output.expect[0], output.expect[1], output.expect[2]

	def RotatingFrame(self, psi, tlist, phi):
		'''
		Rotating frame, introduce rotation with Rotating Wave Approximation (RWA)
		Parameters: 
			psi		: initial state vector (ket)
			tlist	: list of time for t
			phi		: phase offset between pulses or relative phase

		Returns:
			expectation values for the times specified by 'tlist'
		'''

		#define collapse operator; relaxation and dephasing
		c_ops = [np.sqrt(self.gamma[1])*self.loweringOp, np.sqrt(self.gamma[2])*self.pauliZ]

		#define Hamiltonian of the system
		H = (self.w0 - self.wm) * 0.5 * self.pauliZ + (self.W * 0.5) * (np.cos(phi) * self.pauliX - np.sin(phi) * self.pauliY)

		#solve the Hamiltonian equation
		output = qt.mesolve(H, psi, tlist, c_ops, self.pauliOp)

		return output.expect[0], output.expect[1], output.expect[2]


	def Sequence(self, pulse_seq, tau):
		'''
		Simulates spin dynamics of the system base on the given pulse sequence
		Parameters: 
			pulse_seq	: pulse sequence (echo, ramsey, or t1)
			taus		: list of time for t

		Returns:
			total number of time points
			spin evolution
		'''

		#initialize state
		psi = qt.basis(2,0)
		pulses, phases, taus, seq_name = pulse_seq
		sx_total, sy_total, sz_total = [], [], []
		steps = len(pulses)*2 - 1

		#initialize time and steps
		pi_time = np.round(2*np.pi / self.W)*0.5
		dt = 2 * np.pi / 20 / self.gamma[0] if self.gamma[0] >= 0.001 * 2 * np.pi else 50

		#simualtes spin dynamcis based on pulse_sequence
		if seq_name == 't1':
			duration = pi_time
			tlist = np.linspace(0, duration, int(duration)+5)
			psi, s_x, s_y, s_z = self.Pulse(psi, tlist, 0)

			sx_total.extend(s_x)
			sy_total.extend(s_y)
			sz_total.extend(s_z)

		for i in range(steps):
			if i % 2 == 0 and seq_name != 't1':	#for even steps (0th, 2nd, 4th, ...)
				duration = pi_time * pulses[i // 2]
				tlist = np.linspace(0, duration, int(duration) + 5)
				psi, s_x, s_y, s_z = self.Pulse(psi, tlist, np.pi * phases[i // 2])
			else:	#for odd steps (1st, 3rd, 5th, ...)
				duration = tau * taus[i // 2]
				if duration == 0:
					continue
				tlist = np.linspace(0, duration, int(duration / dt) + 5)
				psi, s_x, s_y, s_z = self.Phase(psi, tlist, 0)

			sx_total.extend(s_x)
			sy_total.extend(s_y)
			sz_total.extend(s_z)


		return len(sz_total), np.array(sx_total), np.array(sy_total), np.array(sz_total)