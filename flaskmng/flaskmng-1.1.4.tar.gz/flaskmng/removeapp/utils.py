import shutil
from os.path import join

def remove_app(app_folder):
    def wrapper():
        shutil.rmtree(app_folder)
    return wrapper

def remove_app_imports(project_folder,app_name):
    def wrapper():
        result = ""
        with open(join(project_folder,"__init__.py")) as f:
            code = f.read()
            flag = True
            for line in code.split('\n'):
                if f"#[APP] {app_name}" in line:
                    flag = False
                    continue
                elif f"#[/APP] {app_name}" in line:
                    flag = True
                    continue
                elif not flag:
                    continue
                else:
                    result+=line+"\n"
        with open(join(project_folder,"__init__.py"),'w') as f:
            f.write(result)
    return wrapper