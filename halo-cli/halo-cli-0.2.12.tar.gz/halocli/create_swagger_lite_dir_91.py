import os
import shutil
import sys
from click.testing import CliRunner
from halocli.cli import start,cli

#directory = 'C:\\dev\\projects\\halo\halo-cli\\tests\\gen4\\BIAN_APIs_Release9.0'
#dest = 'C:\\dev\\projects\\halo\halo-cli\\tests\\gen4\\BIAN9'

directory = sys.argv[1]
dest = sys.argv[2]
do_copy = True
#[print(x[0]) for x in os.walk(directory)]
cnt = 1
runner = CliRunner()
for x in os.walk(directory):
    dir_files = x[2]
    if len(dir_files) == 0:
        continue
    sd_name = None
    f_name = None
    json_name = None
    for f in dir_files:
        if f.endswith('json'):
            f_name = f.replace('.json','')
            obj_str = '"'+str(cnt)+'": { \
                "f_name": "'+ f_name.strip() +'", \
                "name": "'+ f_name.strip() +'", \
                "service_domain": true, \
                "swagger": true \
            },'
            print(obj_str)
            #print(str(cnt)+' '+f_name)
            cnt = cnt+1
        if f.endswith('.json'):
            json_name = x[0]+'\\'+f
        if os.path.isfile(json_name) and do_copy:
            shutil.copy(json_name, dest+'\\'+f_name+'.json')
            str1 = '-s C:\dev\projects\halo\halocli\\tests\gen8\halo_settings.json lite create -a all  -p C:\dev\projects\halo\halocli\\tests\gen8'
            result = runner.invoke(cli,str1.split(" "))
            #result = self.runner.invoke(cli, '-s .\halo_settings.json cqrs method -s halo_current_account -p C:\dev\projects\halo\halo-cli\\tests -i TaskRecord'.split(" "))
            print(json_name+":"+str(result.exit_code)+":"+result.output)


