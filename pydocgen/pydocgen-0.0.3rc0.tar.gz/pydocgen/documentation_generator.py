import pdoc
import os
import os.path as path
CWD = os.getcwd()

class Pdoc():
    def __init__(self, modules, output_dir, file_type):
        self.context = pdoc.Context()
        self.output_dir = output_dir
        self.file_type = file_type
        self.modules = [pdoc.Module(module, context=self.context) 
                        for module in modules]
        pdoc.link_inheritance(self.context)
    
    def __save(self, module):
        yield module.name, module.html()
        for sub_module in module.submodules():
            yield from self.__save(sub_module)
    
    def save(self):
        for module in self.modules:
            for module_name, output in self.__save(module):
                path_ = path.join(CWD, self.output_dir, module_name 
                                  + '.' + self.file_type)
                os.makedirs(os.path.dirname(path_), exist_ok=True)
                with open(path_, 'a+') as fout:
                    fout.write(output)
