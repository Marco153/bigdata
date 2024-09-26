import json
import pickle
import requests
import pandas as pd
import matplotlib
import os
import numpy as np

#from os.path import isfile, join


dict = {}
langs = {}


try:
	for year in range(2015, 2025):
		for month in range(1, 13):
			path = f"gh/{year}/repos/{month}"
			onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

			key = year | month << 16
			dict[key] = {'languages':{}}

			for f in onlyfiles:
				print(f"year {year} month {month} file is {f}")
				f = path + "/" + f
				with open(f, 'r', encoding='utf-8') as f_in:
					str = f_in.read()

					if str and str[0] == '{':
						js = json.loads(str)
						lang = js['language']
						if lang not in dict[key]['languages']:
							dict[key]['languages'][lang] = 1
						else:
							dict[key]['languages'][lang] += 1

						if lang not in langs:
							langs[lang] = np.tile(0, 12 * 8)
except BaseException as error:
	print("An exception occurred: {}".format(error))

try:

	for year in range(2015, 2025):
		for month in range(1, 13):
			key = year | (month << 16)
			#print(f"year {year} month : {month}")
			for lang_name in dict[key]['languages'].keys():
				langs[lang_name][year - 2015 + (month - 12)]  = dict[key]['languages'][lang_name]
except BaseException as error:
	print("An exception occurred: {}".format(error))


with open("langs.json", 'wb') as write:
	pickle.dump(langs, write)

'''
df = pd.DataFrame({
	'c++': langs['JavaScript']
}, index=range(8 * 12))
fig = df.plot.line().get_figure()
fig.savefig('langs.png')
'''



					


