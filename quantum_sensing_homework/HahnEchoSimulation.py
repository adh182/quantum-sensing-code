import qutip as qt 
import numpy as np
from Initialization import Initialization
 
class HahnEchoSimulation(Initialization):
    psi0 = qt.basis(2,0)

    def __init__(self, w0, wm, W, w, gamma, tau):
        '''
        Parameters:
            tau     : evolution time
        '''
        super().__init__(w0, wm, W, w, gamma)
        self.tau = tau

    def simulateHahnEcho(self):
        '''
        simulate hahn echo

        Returns:
            total number of time points
            spin evolution 
        '''

        def create_tlist(end, dt=None, extra=5):
            N = int(np.round(end / dt) + extra) if dt else int(np.round(end) + extra)
            return np.linspace(0, end, N)

        phi = 0
        # π/2 pulse duration
        pi_half_time = np.pi / (2 * self.W)
        # π pulse duration
        pi_time = np.pi / self.W            
        #timestep
        dt = 50 if self.gamma < 0.001 * 2 * np.pi else (2 * np.pi) / (20 * self.gamma)

        # First π/2 pulse
        tlist0 = create_tlist(pi_half_time)
        psi1, sx0, sy0, sz0 = self.Pulse(self.psi0, tlist0, phi)

        # Free evolution for τ/2
        if self.tau == 0:
            psi2, sx1, sy1, sz1 = psi1, [], [], []
        else:
            tlist1 = create_tlist(self.tau / 2, dt)
            phi1 = phi
            psi2, sx1, sy1, sz1 = self.Phase(psi1, tlist1, phi1)

        # π pulse
        tlist2 = create_tlist(pi_time)
        phi2 = phi + self.w * self.tau * 0
        psi3, sx2, sy2, sz2 = self.Pulse(psi2, tlist2, phi2)

        # Free evolution for τ/2
        if self.tau == 0:
            psi4, sx3, sy3, sz3 = psi3, [], [], []
        else:
            tlist3 = create_tlist(self.tau / 2, dt)
            phi3 = phi + self.w * self.tau
            psi4, sx3, sy3, sz3 = self.Phase(psi3, tlist3, phi3)

        # Final π/2 pulse
        tlist4 = create_tlist(pi_half_time)
        # self.phi = 0
        psi5, sx4, sy4, sz4 = self.Pulse(psi4, tlist4, phi)

        # Concatenate results
        sx = np.concatenate((sx0, sx1, sx2, sx3, sx4))
        sy = np.concatenate((sy0, sy1, sy2, sy3, sy4))
        sz = np.concatenate((sz0, sz1, sz2, sz3, sz4))

        N = len(sx)

        return N, sx, sy, sz