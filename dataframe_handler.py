# Phase 1 is on the station
import pandas as pd
from pathlib import Path


if __name__ == '__main__':
	root_path = Path('Main_path')
	data = pd.read(f'{root_path}data.csv')
	### script for prepocessing ###
	data.to_csv(f'{root_path}mod_data.csv', index=False)	
