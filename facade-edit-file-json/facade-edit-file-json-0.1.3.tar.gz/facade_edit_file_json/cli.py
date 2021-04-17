import json

class FACADE_EDIT_FILE_JSON():
    def __init__(self,name):
        """Constructor"""
        self.name_file=str(name)

    def read(self,name_file=None,out=False):
        requests_json={}
        if name_file==None:
            name_file=self.name_file
        try:
            with open(name_file, 'r') as fe:
                for line in fe:
                    try:
                        self.json_value = json.loads(line)
                    except Exception as e:
                        self.json_value = {}
        except FileNotFoundError as e:
            self.json_value=[]

        if out:
                return self.json_value
        else:
                return self.json_value != {} if True else False

    def unite(self,list_file):
        self.read()
        self.json_list=[]
        self.json_list=self.json_value
        for item_file in list_file:
            print(item_file)
            json_value=self.read(
                        name_file=item_file,
                        out=True
                    )
            if type(self.json_list).__name__ == 'list':
                if type(json_value).__name__ == 'list':
                    self.json_list = self.json_list + json_value
        self.new(self.json_list)

    def write(self,json_value):
        self.read()
        if type(self.json_value).__name__ == 'list':
            if type(json_value).__name__ == 'list':
                self.json_value=self.json_value+json_value
            if type(json_value).__name__ == 'str':
                self.json_value.append(json_value)
        self.new(self.json_value)

    def new(self,json_value):
        with open(self.name_file, 'w+') as f:
            try:
                json.dump(json_value, f)
            except Exception:
                json.dump({}, f)
            f.close()
