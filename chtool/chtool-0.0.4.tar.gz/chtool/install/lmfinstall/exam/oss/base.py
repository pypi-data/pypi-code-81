from abc import abstractmethod, ABCMeta

#cdccee1dc9a1451f9bd0a9b6a3ded2c5    
#de2ff91b959d48869618872273ed083a


class oss_base(metaclass=ABCMeta): 

    @abstractmethod
    def s3fs_pre(self):pass 

    @abstractmethod
    def mount(self):pass 

    @abstractmethod
    def umount(self):pass 


    @abstractmethod
    def down_file(self,file_src,file_dst):pass 

    @abstractmethod
    def delete_file(self,filename):pass 

    @abstractmethod
    def list_dir(self,dir):pass 


    @abstractmethod
    def upload_file(self,filename,tarname):pass 

    @abstractmethod
    def upload_file_byte(self,filename,tarname):pass 