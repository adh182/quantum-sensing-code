import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import seaborn as sns
import imageio
import os 
from qutip import Bloch

sns.set(style='whitegrid')

def save_bloch_gif(N, sx, sy, sz, filename):
    fig = plt.figure()
    b = Bloch(fig=fig)
    b.vector_color = ['r']
    b.point_color = ['k']
    
    images = []
    for i in range(round(N*0.15)):
        b.clear()
        b.add_vectors([sx[i], sy[i], sz[i]])
        b.add_points([sx[:i+1], sy[:i+1], sz[:i+1]])
        b.render()
        filepath = f'frame_{i}.png'
        plt.savefig(filepath)
        images.append(imageio.imread(filepath))
        os.remove(filepath)

    imageio.mimsave(filename, images, duration=0.05)


def save_signal_gif(taus, signals, filename):
	fig, ax = plt.subplots()

	images = []
	for i in range(1, len(taus)+1):
		ax.clear()
		ax.set_ylim([-0.1, 1.1])
		# ax.set_ylim([0.9, 1.025])
		ax.set_xlabel('τ (ns)')
		ax.set_ylabel('P(|0>)')
		# ax.set_title("Echo Signal")
		ax.plot(taus[:i], signals[:i], color='#D62828', marker='o', markerfacecolor='#277DA1')
		filepath = f'signal_{i}.png'
		plt.savefig(filepath)
		images.append(imageio.imread(filepath))
		os.remove(filepath)

	imageio.mimsave(filename, images, duration=0.3)

'''
Note to myself; fix later

The function save_bloch_gif does not work as I want it.
It creates an image of a Bloch sphere and save it as a frame and overlap the image to create a gif.
This caused the Bloch sphere to looks so complex due to many number of points.
I need to fix this issue by finding away to make the gif without overlapping the image of each frame.
For now, setting N*0.15 seems reasonable.
'''