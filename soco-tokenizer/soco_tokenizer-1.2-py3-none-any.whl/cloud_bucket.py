import boto3
import oss2
import os
import time


class CloudBucket(object):

    def __init__(self, access_key, secret, engine='oss'):
        self._engine = engine
        if engine == 's3':
            self._s3 = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret)
            self._s3_bucket = self._s3.Bucket('convmind-models')
        elif engine == 'oss':
            self._oss_bucket = oss2.Bucket(oss2.Auth(access_key, secret),
                                           str('http://oss-accelerate.aliyuncs.com'),
                                           str('convmind-models'))

    def safe_mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def download(self, folder_dir, files, local_dir):
        start = time.time()
        for f in files:
            src = '{}/{}'.format(folder_dir, f)
            dest =  os.path.join(local_dir, f)
            try:
                if self._engine.lower() == 'oss':
                    self._oss_bucket.get_object_to_file(src, dest)
                else:
                    self._s3_bucket.download_file(src, dest)
            except Exception as e:
                print(e)
                print("Failed to download {}".format(src))

        end = time.time()
        print(("download models using {:.4f} sec".format(end - start)))

    def download_dir(self, folder_dir, dirs, local_dir):
        start = time.time()
        for d in dirs:
            cur_remote_dir = os.path.join(folder_dir, d)
            cur_local_dir = os.path.join(local_dir, d)

            if not os.path.exists(cur_local_dir):
                os.mkdir(cur_local_dir)

            files = []
            if self._engine.lower() == 'oss':
                for o in self._oss_bucket.list_objects(prefix=cur_remote_dir).object_list:
                    f_name = o.key.split('/')[-1]
                    if f_name != '':
                        files.append(o.key.split('/')[-1])
            else:
                for o in self._s3_bucket.objects.filter(Prefix=cur_remote_dir):
                    f_name = o.key.split('/')[-1]
                    if f_name != '':
                        files.append(o.key.split('/')[-1])

            self.download(cur_remote_dir, files, cur_local_dir)

        end = time.time()
        print(("download models using {:.4f} sec".format(end - start)))

    def download_tokenizer(self, asset_dir, asset_id, local_dir="resources"):
        self.safe_mkdir(local_dir)
        files = ['vocab.txt', '{}.txt'.format(asset_id), '{}.json'.format(asset_id), 'config.json']
        model_dir = '{}/{}'.format(local_dir, asset_id)
        if not os.path.exists(os.path.join(model_dir, files[0])):
            self.safe_mkdir(model_dir)
            self.download('{}/{}'.format(asset_dir, asset_id), files, 'resources/{}'.format(asset_id))
        else:
            print("Download is canceled since the asset already exists.")

        return model_dir


if __name__ == '__main__':
    b = CloudBucket('oss', 'LTAINYtHd5knNlAg', 'HIg89gNwNYpbEKoC38SdnYCn3Db8cI')
    b.download_tokenizer('tokenizers', 'bert-base-chinese')