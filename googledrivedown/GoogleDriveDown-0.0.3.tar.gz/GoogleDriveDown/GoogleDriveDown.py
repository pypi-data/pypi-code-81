# Import Required Libraries
from pydrive.auth import GoogleAuth
import pandas as pd
from pydrive.drive import GoogleDrive
import os
from os import listdir
from os.path import isfile, join


#-------------------------------------------GOOGLE DRIVE AUTHENTICATION--------------------------------------------------------------
def authentication():

	# A browser window will open. login using the appropriate account.
	gauth = GoogleAuth()
	gauth.LocalWebserverAuth()

	drive = GoogleDrive(gauth)

	return drive


#------------------------------------------AUTHENTICATION and EXTRACT ID--------------------------------------------------------------
def auto(id, drive, parent_folder):    
 
	# Set the id of the Google Drive folder. You can find it in the URL of the google drive folder.
	parent_folder_id = id
	
	# Set the parent folder, where you want to store the contents of the google drive folder	
	parent_folder_dir = parent_folder

	if parent_folder_dir[-1] != '/':
		parent_folder_dir = parent_folder_dir + '/'

	# This is the base wget command that we will use. This might change in the future due to changes in Google drive
	wget_text = '"wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&amp;confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate \'https://docs.google.com/uc?export=download&amp;id=FILE_ID\' -O- | sed -rn \'s/.*confirm=([0-9A-Za-z_]+).*/\\1\\n/p\')&id=FILE_ID" -O FILE_NAME && rm -rf /tmp/cookies.txt"'.replace('&amp;', '&')

	# Get the folder structure

	file_dict = dict()
	folder_queue = [parent_folder_id]
	dir_queue = [parent_folder_dir]
	cnt = 0

	while len(folder_queue) != 0:
		current_folder_id = folder_queue.pop(0)
		file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(current_folder_id)}).GetList()
		
		current_parent = dir_queue.pop(0)
		print(current_parent, current_folder_id)
		for file1 in file_list:
			file_dict[cnt] = dict()
			file_dict[cnt]['id'] = file1['id']
			file_dict[cnt]['title'] = file1['title']
			file_dict[cnt]['dir'] = current_parent + file1['title']

			if file1['mimeType'] == 'application/vnd.google-apps.folder':
				file_dict[cnt]['type'] = 'folder'
				file_dict[cnt]['dir'] += '/'
				folder_queue.append(file1['id'])
				dir_queue.append(file_dict[cnt]['dir'])

			else:
				file_dict[cnt]['type'] = 'file'
				
			cnt += 1

	d = pd.DataFrame(file_dict).transpose()

	# Including only type as "file"
	d = d[d['type'] == 'file']

	return d

#---------------------------------------------------Download Image Using ID-----------------------------------------------------------
def download_file_from_google_drive(id, destination, parent_folder):
	import gdown

	try:
		url = f'https://drive.google.com/uc?id={id}'
		output = parent_folder +'/'+ destination

		try:
			gdown.download(url, output, quiet=False)

		except Exception as e:
			print('Error ======> ', e)
			for i in range(0, 5):
				print('Retry Time', i)
				try: 
					gdown.download(url, output, quiet=False)
					break
				except:
					continue
			return url
			
		try:
			md5 = 'fa837a88f0c40c513d975104edf3da17'
			gdown.cached_download(url, output, md5=md5, postprocess=gdown.extractall)

		except Exception as e:
			print('MD5 Error')
	
	except Exception as e:
		print('Error ======> ', e)
		return url


#-----------------------------------------------RETURN URL ID----------------------------------------------------------------------
def parse_id(url):
		
	# TYPE 1 -----> https://drive.google.com/open?id=0Bw9Ez3c1r0YrUWhnSHlpNDJnNWs
	if "id=" in url:
		url_id = url.split('=')[-1]
		
	# TYPE 2 -----> https://drive.google.com/drive/folders/1XTpkTEXclcZTve207Rh9bhsXDIr2C3Wu?usp=sharing
	elif "usp=sharing" in url:
		url_id = url.split('/')[-1].split('?')[0]

	# TYPE 3 -----> https://drive.google.com/drive/u/1/folders/1K_1RK69FM9ip3Lzi4cgW3AEVMvh7zi7Y
	else:
		url_id = url.split('/')[-1]

	return url_id



#------------------------------------------------------MAIN FUNCTION------------------------------------------------------------------
def get_files(url, parent_folder):


	# Calling parse_id method to extract id from url
	id = parse_id(url)

	# Google Authentication
	drive = authentication()

	data = auto(id, drive, parent_folder)

	main_df = pd.DataFrame(columns=['id', 'title', 'dir', 'type'])
	rerun = []

	main_df = pd.concat([main_df, data], ignore_index=True)

	for id, dir in zip(data['id'], data['dir']):
		print('File ID', id)

		dir = dir.split('/')[-1]

		if not os.path.exists(parent_folder +'/'+ dir):
			url = 'https://drive.google.com/uc?id={id}'

			if dir.split('.')[-1].lower().strip() in ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'csv', 'xlsx', 'xls', 'txt', 'py', 'exe', 'sh']: 
				u = download_file_from_google_drive(id, dir, parent_folder)
				rerun.append(u)

			else:
				rerun.append(url)

		else:
			print('File Already Exists', dir)

	main_df = main_df.drop_duplicates(subset = ['title'])	

	print("\nTotal Files on Drive Link (Excluding Duplicates) :::", len(main_df))

	onlyFiles = [f for f in listdir(f'./{parent_folder}/') if isfile(join(f'./{parent_folder}/', f))]
	
	print('\nTotal Files Downloaded in '+parent_folder+' :::', len(onlyFiles))





