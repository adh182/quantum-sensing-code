import qutip as qt 
import numpy as np 

class Initialization:
	pauliX = qt.sigmax()
	pauliY = qt.sigmay()
	pauliZ = qt.sigmaz()
	pauliOp = [pauliX, pauliY, pauliZ]


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
		Parameters: 
			psi		: initial state vector (ket)
			tlist	: list of time for t
			phi		: phase offset between pulses or relative phase

		Returns:
			final state of the state vector
			expectation values for the times specified by 'tlist'
		'''

		#define the Hamiltonian of the system
		H = ((self.w0-self.wm)*0.5)*self.pauliZ + (self.W*0.5)*(np.cos(phi)*self.pauliX - np.sin(phi)*self.pauliY)

		#solve the hamiltonian equation
		output = qt.sesolve(H, psi, tlist, self.pauliOp, options=qt.Options(store_final_state=True))

		return output.final_state, output.expect[0], output.expect[1], output.expect[2]

	def Phase(self, psi, tlist, phi):
		'''
		Parameters: 
			psi		: initial state vector (ket)
			tlist	: list of time for t
			phi		: phase offset between pulses or relative phase

		Returns:
			final state of the state vector
			expectation values for the times specified by 'tlist'
		'''

		#define the Hamiltonian of th system
		H0 = ((self.w0-self.wm)*0.5)*self.pauliZ
		H1 = (self.gamma*0.5)*self.pauliZ

		def H1_coeff(t, args):
			return np.cos(self.w*t + phi)

		H = [H0, [H1, H1_coeff]]

		#solve the hamiltonian equation
		output = qt.sesolve(H, psi, tlist, self.pauliOp, options=qt.Options(store_final_state=True))
		
		return output.final_state, output.expect[0], output.expect[1], output.expect[2]