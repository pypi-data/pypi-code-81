# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import click
import os
# import commands
import subprocess
import sh
 
 
def get_config_file_path():
    home_path = os.getenv("HOME")
    return os.path.join(home_path, ".bash_profile")


def set_environment_variable(key, path):
    config_file_path = get_config_file_path()
    try:
        file_handle = open(config_file_path, "r")
        lines = file_handle.readlines()
        file_handle.close()
        need_set_env = True
        for single_line in lines:
            if single_line.startswith("export PRIVATE_REPO="):
                need_set_env = False
                break
        if need_set_env:
            variable_str = "\nexport %s=%s\n" % (key, path)
            lines.insert(0, variable_str)
            content = "".join(lines)
            click.echo(content)
            file_handle = open(config_file_path, "w")
            file_handle.write(content)
            file_handle.close()
    except:
        click.echo("save environment variable failed")
    click.echo("save environment variable sucess")


def get_enviroument_value(key_name):
    value = os.getenv(key_name)
    if not value:
        config_file_path = get_config_file_path()
        file_handle = open(config_file_path, "r")
        lines = file_handle.readlines()
        file_handle.close()
        for single_line in lines:
            if single_line.startswith("export PRIVATE_REPO="):
                value = single_line.split("=")[-1]
                break
    return value


def get_source_repo_path():
    key_name = "PRIVATE_REPO"
    private_repo = get_enviroument_value(key_name)
    if not private_repo:
        private_repo = click.prompt('private repository(eg. https://xxx/python_script_repo)')
        set_environment_variable(key_name, private_repo)
    return private_repo


def decorate_svn_path(svn_path):
    return "svn+" + svn_path


def find_real_path(svn_path, package_name):
    cmd = "svn list %s" % svn_path
    (status, output) = subprocess.getstatusoutput(cmd)
    name_list = output.split("\n")
    for name in name_list:
        if "/" != name[-1]:
            continue
        if name[:-1] == package_name:
            return decorate_svn_path(os.path.join(svn_path, package_name))
    return None





@click.group()
def pipp():
    pass


@click.command()
@click.argument("package_name")
def install(package_name):
    click.echo("start install")
    private_repo = get_source_repo_path()
    package_path = find_real_path(private_repo, package_name)
    click.echo("\n{0}\n".format(package_path))
    if not package_path:
        raise Exception("not found %s" % package_name)
    install_cmd = "pip install %s" % package_path
    os.system(install_cmd)
    click.echo("echo install %s" % package_name)


@click.command()
def list():
    private_repo = get_source_repo_path()
    cmd = "svn list %s" % private_repo
    (status, output) = subprocess.getstatusoutput(cmd)
    name_list = output.split("\n")
    for name in name_list:
        if "/" == name[-1]:
            click.echo("\n{0}\n".format(name[:-1]))


pipp.add_command(install)
pipp.add_command(list)


def main():
    pipp()
    
    
if __name__ == '__main__':
    main()
