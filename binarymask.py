import pandas as pd
import numpy as np
from skimage.draw import polygon, line
import json
from PyQt5.QtWidgets import QFileDialog, QApplication
from PIL import Image

def produce_mask(path):
	df=pd.read_csv(path)
	try:
		img=np.zeros((df['height'][0], df['width'][0]))		# Creat placeholder, This was originally flipped
	except IndexError as e:
		print("This binary mask is empty!")
		return
	U=df['Object'].unique()
	print("shape of img is: ", np.shape(img))
	for i in U: 										# For each object labelled
		dfsubstr=df[df['Object']==i]
		if dfsubstr['Type'].values[0]=='Polygon': 		# Get the polygon
			rr,cc=polygon(dfsubstr['X'].values, dfsubstr['Y'].values) # Also flipped in original
			img[cc,rr]=1
		elif dfsubstr['Type'].values[0]=='Line': 		# Get the line
			for j in range(dfsubstr.shape[0]-1):
				r0, c0 = int(dfsubstr['X'].values[j]), int(dfsubstr['Y'].values[j])
				r1, c1 = int(dfsubstr['X'].values[j+1]), int(dfsubstr['Y'].values[j+1])
				cc,rr=line(r0, c0, r1, c1)
				img[cc,rr]=1
		else: #A point
			img[int(dfsubstr['X']),int(dfsubstr['Y'])]=1
	np.savez_compressed(path[:-4], img)
	# Save the .png version with normalization to 255
	img = img * 255
	im = Image.fromarray(img).convert('RGB') 	# .png only support RGB mode
	im.save(path[:-4]+'.png') 					# Saving the RGB files
	return

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	dialogue=QFileDialog()
	dialogue.setNameFilter("*.csv");
	dialogue.setDefaultSuffix('csv')
	dialogue.setFileMode(QFileDialog.ExistingFiles)
	dialogue.exec()
	path=dialogue.selectedFiles()

	# Reading in from system folder selection
	[produce_mask(p) for p in path]
