from create_pyproj.createfile import copyTemplates, createFiles

projectname = 'test-proj'
package = True
cli = False

copyTemplates(projectname, package, cli)
createFiles(projectname, package, cli)
