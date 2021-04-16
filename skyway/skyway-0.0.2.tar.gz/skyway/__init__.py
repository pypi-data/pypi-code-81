class skyway:
    def __init__(self):
        global f,content,project_name,project_version
        f = open('./skyway/config.sky',"r")
        project_namefinder = f.readline()
        project_versionfinder = f.readline()
        f.close()
        project_namefinder.find('PROJECT_NAME =')
        project_versionfinder.find('PROJECT_VERSION =')
        project_name = project_namefinder.split(' ')[2]
        project_versionfinder.find('PROJECT_VERSION =')
        print(project_versionfinder.split(' ')[2])


