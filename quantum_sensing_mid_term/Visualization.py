import qutip as qt 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import imageio
import os

class Visualization:
	sns.set(style='whitegrid')
	
	def __init__(self, N, sx, sy, sz, taus, signals):
		'''
		Parameters: 
			N				: number of points
			sx, sy, sz		: spin evolution
			taus			: number of time points
			signals 		: signlas used for Ramsey, Echo, and T1 Relaxometry
		'''
		self.N = N 
		self.sx = sx 
		self.sy = sy 
		self.sz = sz
		self.taus = taus 
		self.signals = signals


	def GetBloch(self, filename='bloch.gif'):
		'''
		Creates Bloch sphere and save is as a .gif file.
		There are too many points to plot raising an ArrayMemoryError, so only plot 15%
		of the points in the Bloch sphere to reduce memory.
		Parameters:
			filename	: name and the location of .gif file

		'''
		fig = plt.figure(figsize=(12,7))
		bloch = qt.Bloch(fig=fig)
		bloch.vector_color = ['r']
		bloch.point_color = ['k']

		images = []
		for i in range(round(self.N*0.15)):
			bloch.clear()
			bloch.add_vectors([self.sx[i], self.sy[i], self.sz[i]])
			bloch.add_points([self.sx[:i+1], self.sy[:i+1], self.sz[:i+1]])
			bloch.render()

			# ax = bloch.fig.axes[0]
			# ax.text2D(0.95, 0.05, 'τ: '+str(i)+' ns', transform=ax.transAxes, ha='right', va='bottom', fontsize=20)

			filepath = f'frame_{i}.png'
			plt.savefig(filepath)
			images.append(imageio.imread(filepath))
			os.remove(filepath)


		imageio.mimsave(filename, images, duration=0.3, loop=0)


	def GetGraph(self, filename='graph.gif', title='Pulse Sequence', rabi=False):
		'''
		Creates graph and save is as a .gif file
		Parameters:
			filename	: name and the location of .gif file
			rabi		: if True, creates graph for Rabi, otherwise Ramsey, Echo, T1 Relaxometry

		'''
		images = []
		if rabi:
			#creates graph specifically for Rabi simulation
			fig, ax = plt.subplots(3, 1)
			fig.suptitle(title, x=0.5, y=0.98)
			for i in range(1, len(self.taus)+1):
				for k in range(3):
					ax[k].clear()
					ax[k].set_ylabel(r'P($\left|0\right\rangle$)')
					ax[k].set_ylim(-1.1, 1.1)

				ax[2].set_xlabel('τ (ns)')
				ax[0].set_xticklabels([])
				ax[1].set_xticklabels([])

				ax[0].plot(self.taus[:i+1], self.sx[:i+1], color='blue', label='$\sigma_x$')
				ax[1].plot(self.taus[:i+1], self.sy[:i+1], color='green', label='$\sigma_y$')
				ax[2].plot(self.taus[:i+1], self.sz[:i+1], color='red', label='$\sigma_z$')

				ax[0].legend()
				ax[1].legend()
				ax[2].legend()

				filepath = f'signal_{i}.png'
				plt.savefig(filepath)
				images.append(imageio.imread(filepath))
				os.remove(filepath)

		else:
			#crates graph for Ramsey, Echo, and T1 Relaxometry
			fig, ax = plt.subplots()
			fig.suptitle(title)
			for i in range(1, len(self.taus)+1):
				ax.clear()
				ax.set_ylim([-0.1, 1.1])
				ax.set_xlabel('τ (ns)')
				ax.set_ylabel(r'P($\left|0\right\rangle$)')
				ax.plot(self.taus[:i], self.signals[:i], color='#D62828', marker='o', markerfacecolor='#277DA1')
				filepath = f'signal_{i}.png'
				plt.savefig(filepath)
				images.append(imageio.imread(filepath))
				os.remove(filepath)

		imageio.mimsave(filename, images, duration=0.3, loop=0)
