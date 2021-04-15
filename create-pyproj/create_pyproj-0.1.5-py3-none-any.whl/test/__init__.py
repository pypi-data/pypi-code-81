from create_pyproj.createfile import copyTemplates, createFiles

projectname = 'test-proj'
is_package = True
is_cli = False

copyTemplates(projectname, is_package, is_cli)
createFiles(projectname, is_package, is_cli)
