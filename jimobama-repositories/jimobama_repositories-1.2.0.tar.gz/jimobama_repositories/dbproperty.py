import os;
from jimobama_repositories.argsinitialiser import argument_validator;



@argument_validator(name="",
                    dbtype         = None,
                    is_primary_key = False,
                    increment      = False,
                    value          = None)
class DBProperty(object):

    def __init__(self, owner,**kwargs):
        self.__owner         = owner;
        self.__name         = kwargs['name']
        self.__dbtype       = kwargs['dbtype']
        self.__primary_key  = kwargs['is_primary_key'];
        self.__value        = kwargs['value'];
        self.__increment    = kwargs['increment']

    @property
    def owner(self):
        return self.__owner;

    @property
    def increment(self):
        return self.__increment;
                
    @property
    def is_primary_key(self):
        return self.__primary_key;

    @property
    def name(self):
        return self.__name;
    
    @property
    def dbtype(self):
        return self.__dbtype;
    
    @property
    def value(self):
        return self.__value;

    @value.setter
    def value(self, val:object):
        if(self.__value != val):
            if(self.__dbtype != None):
                if(type(val) != self.__dbtype):
                    raise TypeError("expecting a type of {0} but {0} given".format(type(self.__dbtype), type(val)));
        self.__value  =  val;
        self.__dbtype =  FieldType.parse(type(self.__value));
        
        if(hasattr(self.owner,"property_changed")):
            if(callable(self.owner.property_changed)):
                self.owner.property_changed(self);

    def __del__(self):
       pass;


if __name__ =="__main__":
    prop =  DBProperty(None, name="age");
    prop.value = 190;
    print(prop.dbtype)
