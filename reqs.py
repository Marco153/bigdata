import json
import os
import requests

headers = {'User-Agent': 'request', 'Authorization': 'token ' + 'API_TOKEN'}

def MakeDir(path):
	try:
		os.mkdir(path)
		print(f"Directory '{path}' created successfully.")
	except FileExistsError:
		print(f"Directory '{path}' already exists.")
	except PermissionError:
		print(f"Permission denied: Unable to create '{path}'.")
	except Exception as e:
		print(f"An error occurred: {e}")

for x in range(10, 13):
	# Create the directory
	dir = f'2023/{x}'
	jqed = f'{dir}/jqed'

	with open(jqed, "r") as f:
		#MakeDir(f'{dir}/repos')
		js = json.loads(f.read())
		print(js[0])
		for url in js:
			print(f'on url {url["url"]}')
			repo_name = url["url"].split('/')[-1]
			repo_dir = f'{dir}/{repo_name}'
			if os.path.isdir(repo_dir):
				print(f"dir {repo_name} already exists")
				#continue
			MakeDir(f'{repo_dir}_dir')
			req = requests.get(url["url"], headers)
			print(req.text)
			if req.text[2] == 'm':
				print("limit achieved")
				continue


			with open(f'{repo_dir}', 'w', encoding='utf-8') as w:
				w.write(req.text)
			#print(req.text)

