from pathlib import Path

from PIL import Image

RESOURCE_PATH = Path(__file__).parent.absolute()

FOLDER_IMG = Image.open(RESOURCE_PATH / 'add_folder.png')  # .resize((5, 5), Image.ANTIALIAS)
SETTING_IMG = Image.open(RESOURCE_PATH / 'setting.png')
UPLOAD_IMG = Image.open(RESOURCE_PATH / 'upload.png')
CONNECT_IMG = Image.open(RESOURCE_PATH / 'connect.png')
DELETE_IMG = Image.open(RESOURCE_PATH / 'delete.png')
DOWNLOAD_IMG = Image.open(RESOURCE_PATH / 'download.png').resize((45, 45), Image.NEAREST)
REFRESH_IMG = Image.open(RESOURCE_PATH / 'refresh.png').resize((40, 40), Image.NEAREST)
ADD_IMG = Image.open(RESOURCE_PATH / 'add.png').resize((40, 40), Image.NEAREST)
REMOVE_IMG = Image.open(RESOURCE_PATH / 'remove.png').resize((40, 40), Image.NEAREST)
GO_IMG = Image.open(RESOURCE_PATH / 'go.png').resize((40, 40), Image.NEAREST)
BACK_IMG = Image.open(RESOURCE_PATH / 'back.png').resize((40, 40), Image.NEAREST)

# DOWNLOAD_IMG = Image.open(RESOURCE_PATH / 'download.png').zoom((40, 40))
