import requests
import gzip
import shutil
import subprocess
import os

only_jq = False

for month in range(10, 11):
	# Create the directory
	dir = f'2023/{month}'
	
	if not only_jq:
		try:
			os.mkdir(dir)
			print(f"Directory '{month}' created successfully.")
		except FileExistsError:
			print(f"Directory '{month}' already exists.")
		except PermissionError:
			print(f"Permission denied: Unable to create '{month}'.")
		except Exception as e:
			print(f"An error occurred: {e}")

		url = f'https://data.gharchive.org/2023-{month:02d}-01-15.json.gz'

		# Get the filename from the URL
		filename = f"{dir}/{url.split('/')[-1]}"

		# Download the file in binary mode
		response = requests.get(url, stream=True)
		response.raise_for_status()  # Check if the download was successful

		# Write the content to a local file
		with open(filename, 'wb') as file:
			for chunk in response.iter_content(chunk_size=8192):
				file.write(chunk)

		print(f"Downloaded {filename} successfully!")

		# Define the path to your .gz file and the output file
		gz_file_path = filename
		output_file_path = f"{dir}/ex"

		# Open the .gz file and the output file in binary mode
		with gzip.open(gz_file_path, 'rb') as f_in:
			with open(output_file_path, 'wb') as f_out:
				shutil.copyfileobj(f_in, f_out)


	output_file_path = f"{dir}/ex"
	# Define the jq command as a raw string
	jq_command = r'[limit(500; inputs | {url: .repo.url})]'

	# Run the jq command
	result = subprocess.run(
		['jq', '-n', jq_command, output_file_path],
		capture_output=True,
		text=True
	)

	output_file = f"{dir}/jqed"
	# Check if the command was successful
	if result.returncode == 0:
		# Write the output to the specified file
		with open(output_file, 'w') as f:
			f.write(result.stdout)
		print(f"Output written to {output_file}.")
	else:
		print(f"Error: {result.stderr}")

	print("File unzipped successfully!")