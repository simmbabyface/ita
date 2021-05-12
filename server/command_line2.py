from __future__ import division
import sys, getopt
import pandas as pd
import numpy as np
# activate my-rdkit-env
from rdkit import Chem
from rdkit.Chem import Draw
import matplotlib.pyplot as plt
import os
import seaborn as sns
import time
# import urllib2
# from sklearn import metrics


def input_mapping(inputfile, outputfile):
	m = Chem.MolFromSmiles(inputfile)
	compXfrag = pd.read_csv(r'componentXunique20fragment_16.csv', index_col = 0, header = 0)
	compXfrag =  compXfrag.drop(['4','8','10'], axis=1) # exclude Components
	Compo = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII']

	componentXscore = pd.DataFrame(np.zeros((len(Compo),1)), index = Compo, columns = ['Test Chemical'])	#index = num of compo, col = xeno cas
	topN = 10

	smi = Chem.MolFromSmiles(inputfile)
	for i,col in enumerate(componentXscore.columns):
		for j,com in enumerate(compXfrag.columns):
			score = 0
			sorted_frags = compXfrag.loc[:,com]
			for top,frag in enumerate(sorted_frags):
				if frag != '0.0' and frag != 0.0 and smi.HasSubstructMatch(Chem.MolFromSmarts(frag)):
					score += 1/(top+1)
			componentXscore.iloc[j,i] = score
	# componentXscore.to_csv(outputfile+time.strftime('%Y%m%d-%H%M%S')+'.csv')
	

	ax = sns.barplot(x=componentXscore.index, y="Test Chemical", data=componentXscore)
	plt.title('Health Effect Prioritization',fontsize= 18)
	plt.savefig(os.path.join('..', 'client', 'img', outputfile+'.png'),dpi=800)
