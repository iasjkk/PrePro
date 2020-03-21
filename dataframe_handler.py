# Phase 1 is on the station
import pandas as pd
from pathlib import Path


def process():
	# write something 
	pass


if __name__ == '__main__':
	root_path = f'/home/jitendra/Code/PrePro/Data/' #Path(f'')
	data = pd.read_csv(f'{root_path}train.csv')
	print(data)
	### script for prepocessing ###
	# data.to_csv(f'{root_path}mod_data.csv', index=False)	
