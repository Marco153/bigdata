import json
import os

from collections import defaultdict


def SumLangsMonthts():
	for year in range(2022, 2024):
		months_info = defaultdict(int)
		for month in range(1, 13):
			path = f"gh/{year}/repos/{month}"
			onlyfiles = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
			for f in onlyfiles:
				f = path+"/" + f+"/langs.json"
				
				if os.path.isfile(f):
					with open(f, 'r') as file:
						fstr = file.read()
						print(fstr)
						js = json.loads(fstr)
						for attributes, values in js.items():
							months_info[attributes] += 1

			with open(f"{path}/resume_langs.json", 'w') as file:
				dumped = json.dumps(months_info)
				dumped = json.loads(dumped)
				json.dump(dumped, file)

							
							
							

SumLangsMonthts()
