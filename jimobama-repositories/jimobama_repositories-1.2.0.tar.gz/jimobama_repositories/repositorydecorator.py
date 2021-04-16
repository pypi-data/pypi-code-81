import os;
import copy
from jimobama_repositories.repository      import  Repository
from jimobama_repositories.argsinitialiser import argument_validator;


            

                
@argument_validator(path="./",ext="json", dbname=None)
class repository(object):

    def __init__(self, *args, **kwargs):
        self.__args   = args;
        self.__kwargs = kwargs;

    def __call__(self,classType: callable):
        if(type(classType) != object.__class__):
            raise TypeError("@Expecting a class object but {0} given".format(type(classType)))
        #make it access to RepoClass;
        repo_kwargs = self.__kwargs
        
        class __RepositoryClass(classType):

            def __init__(self, *args, **kwargs):
                self.__dbname    = repo_kwargs['dbname'] if(repo_kwargs['dbname'] != None) else self.__class__.__name__;                
                self.__path      = repo_kwargs['path'];
                self.__ext       = repo_kwargs['ext'];
                self.__filename  = "{0}.{1}".format(self.__dbname, self.__ext);
                self.__fullpath  = os.path.join(self.__path, self.__filename);
                self.__repo      = Repository(self.__fullpath);
                
                metaprop_Filename  = "{0}_metadata.{1}".format(self.__dbname, self.__ext);
                self.__propRepo    =  Repository(os.path.join(self.__path,  metaprop_Filename));
                super().__init__(*args, **kwargs);
                self.__propKey  =  self.key();

                
                pass;

            @property
            def filename(self):
                return self.__filename;
                
            def __str__(self):
                return str(self.__propRepo.data);
            
            def create_property(self, name:str= "", **kwargs):
                dbProperty =  None;
                if(type(name) != str):
                    raise TypeError(type(name));
                if(len(name) >  0):
                    properties  =  self.__propRepo.create("properties", dict());
                    if(name in properties) is not True:
                        dbProperty  =  DBProperty(self, name  = name, **copy.deepcopy(kwargs));
                        result      = self.create_metadata_property(dbProperty);
                        if(result is not None):
                            properties[name]  = result;
                            self.__propRepo.commit();
                    else:
                        dbProperty   = self.load_property(copy.copy(properties[name]));
                
                return dbProperty;

            def key(self):
                primary_key =  None;
                #Find the primary-key
                properties  =  self.__propRepo.create("properties", dict())
                count  = 0;
                propkeyname  = None;
                
                for key in properties:
                    if("is_primary_key" in properties[key]):
                        if(properties[key]["is_primary_key"] is True):
                            propkeyname  =  key;
                            count  += 1;                            
                if(count > 1):
                    raise ValueError("Multi-primary keys detected.");
                else:
                    if(count <= 0):
                      primary_key  = self.create_property("uuid_key", increment=True);
                    else:
                       if(propkeyname is not None):
                           primary_key  = self.load_property(properties[propkeyname]); 
                return primary_key
                

            def load_property(self, prop:dict)->DBProperty:
                propObject =  None;
                if("name" in prop):
                    propObject = DBProperty(self, **prop);
                return propObject;

            def create_metadata_property(self, prop:DBProperty)->dict:
                result =  dict();
                result['dbtype']       = prop.dbtype;
                result['is_primary_key']  = prop.is_primary_key;
                result['name']         = prop.name;
                return result;

            def update_property(self, prop:DBProperty):
                if(isinstance(prop, DBProperty)):
                    if(self.
                    self.__repo.add(prop.name , prop.value)
                                    
            def sync(self):
                if(self.__repo is not None):
                    self.__repo.commit();
                    if(self.__propRepo != None):
                        self.__propRepo.commit();

        __RepositoryClass.__name__  = classType.__name__;
        return __RepositoryClass ;
if __name__ =="__main__":

    @repository(path="./data/app/")
    class User(object):

        def __init__(self):
            self.__UUID  =  self.create_property("UUID", is_primary_key=True);
            self.name  =  self.create_property("name", );
            self.name.value="Obaro";
            self.age =self.create_property("age");

        @property
        def UUID(self):
            return self.__UUID.value;

    user   =  User();
    user.name.value ="Tommy"
    user2  = User();
    user2.name.value="Obaro"

    user.sync();
    user2.sync();
            







