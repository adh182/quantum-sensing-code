import qutip as qt 
import numpy as np
from Initialization import Initialization

class RamseySimulation(Initialization):
    psi0 = qt.basis(2,0)

    def __init__(self, w0, wm, W, w, gamma, tau):
        '''
        Parameters:
            tau     : evolution time
        '''

        super().__init__(w0, wm, W, w, gamma)
        self.tau = tau

    def simulateRamsey(self):
        '''
        simulate ramsey interferometry

        Returns:
            total number of time points
            spin evolution 
        '''

        def create_tlist(end, dt=None, extra=5):
            N = int(np.round(end / dt) + extra) if dt else int(np.round(end) + extra)
            return np.linspace(0, end, N)

        pi_time = np.pi / self.W
        phi = 0

        dt = 50 if self.gamma < 0.001 * 2 * np.pi else (2 * np.pi) / (20 * self.gamma)

        # First π/2 pulse
        tlist0 = create_tlist(pi_time * 0.5)
        psi1, sx0, sy0, sz0 = self.Pulse(self.psi0, tlist0, phi)

        # Free evolution
        if self.tau == 0:
            psi2, sx1, sy1, sz1 = psi1, [], [], []
        else:
            tlist1 = create_tlist(self.tau, dt)
            psi2, sx1, sy1, sz1 = self.Phase(psi1, tlist1, phi)

        # Second π/2 pulse
        tlist2 = create_tlist(pi_time * 0.5)
        psi3, sx2, sy2, sz2 = self.Pulse(psi2, tlist2, phi)

        # Concatenate results
        sx = np.concatenate((sx0, sx1, sx2))
        sy = np.concatenate((sy0, sy1, sy2))
        sz = np.concatenate((sz0, sz1, sz2))

        N = len(sx)  # Total number of time points

        return N, sx, sy, sz