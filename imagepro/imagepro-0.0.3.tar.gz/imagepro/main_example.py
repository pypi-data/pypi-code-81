import requests
import pandas as pd
from imagepro.core.resize_images import resize_images
from imagepro.core.save_to_s3 import save_to_s3
from imagepro.ports.connect_s3 import connect_s3


home = expanduser("~")
with open(home+'/aws_credentials.json', 'r') as jf:
    credential = json.load(jf)
s3_connection = connect_s3(credential)
bucket_name = 'smartseller-product-images'

data = pd.read_csv('../data/testdata2.csv').fillna(value = '')
keys = data.columns
data = list(data.T.to_dict().values())

new_file = []
failed = 0
for dt in data:
    resized_image_url = []
    for index in range(2, len(keys)):
        url = dt[keys[index]]
        if url != '':
            image = resize_images(requests.get(url, stream=True).raw)
            flag = save_to_s3(
                s3_connection, bucket_name,
                dt[keys[0]]+'/'+url.split('/')[-1],
                image
            )
        else:
            resized_image_url.append('')
        if flag == 1:
            resized_image_url.append(
                'https://smartseller-product-images.s3-us-west-1.amazonaws.com/{}/{}'.format(
                    dt[keys[0]], url.split('/')[-1]
                )
            )
            flag = 0
        else:
            resized_image_url.append('')
            failed += 1
    dt['resized_image_urls'] = ','.join(resized_image_url)
    new_file.append(dt)
pd.DataFrame.from_records(new_file).to_csv('results.csv', index=False)
