import click
import os
import sys
import json
from minio import Minio

sys.path.append(os.path.dirname(__file__) + os.sep + '../')

from client import cfg
from dataset.dataset import Dataset

#组入口
@click.group()
@click.option("-ak", "--access_key", 'access_key', default="", help="The accessKey of ycdata.")
@click.option("-sk", "--secret_key", 'secret_key', default="", help="The secretKey of ycdata.")
@click.option("-en", "--endpoint", "endpoint", default="http://127.0.0.1:8888/", help="The endpoint of ycdata.")
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def main(ctx, access_key, secret_key, endpoint, debug):
    """ 云测数据数据集平台工具 """
    obj = {}
    if access_key != "" and secret_key != "":#按照临时设置执行
        obj = {
            "access_key":access_key,
            "secret_key":secret_key,
            "endpoint":endpoint,
            "DEBUG":debug
        }
    else:#如果已经设置conf 则按照设置的来
        if cfg._check():
            conf = cfg._getConf()
            obj = {
                "access_key":conf['access_key'],
                "secret_key":conf['secret_key'],
                "endpoint":conf['endpoint'],
                "DEBUG":debug
            }

    ctx.obj = Dataset(obj["access_key"], obj["secret_key"], obj["endpoint"])


#信息设置
@main.command()
@click.option("--access_key", 'access_key', default="", help="The accessKey of ycdata.")
@click.option("--secret_key", 'secret_key', default="", help="The secretKey of ycdata.")
@click.option("--endpoint", 'endpoint', default="http://127.0.0.1:8888/",  help="The secretKey of ycdata.")
@click.pass_context
def config(ctx, access_key, secret_key, endpoint):
    """ ycdata用户信息设置 """
    configFile = cfg._config_filepath()
    if access_key == "" or secret_key == "":
        if cfg._check():
            print(cfg._getConf())
    else:
        conf = {
            "access_key":access_key,
            "secret_key":secret_key,
            "endpoint":endpoint,
        }
        with open(configFile, "w") as config:
            json.dump(conf, config)
            print(conf)

#列出所有数据集
@main.command()
@click.option("--dataset", 'dataset', default="", help="数据集名称")
@click.option("--recursive", 'recursive', type=bool, default=False, help="是否使用递归查询")
@click.pass_context
def ls(ctx, dataset, recursive):
    """ 查看数据 """
    ctx.obj.ListAllDataset(dataset, recursive)


#创建数据集
@main.command()
@click.option("--dataset", 'dataset', default="", help="数据集名称")
@click.pass_context
def create(ctx, dataset):
    """ 创建数据集 """
    if dataset == "":
        click.echo("请输入数据集名称")
        exit()
    ctx.obj.CreateDataset(dataset)

@main.command()
@click.option("--dataset", 'dataset', default="", help="数据集名称")
@click.option("--dir", 'dir', default="", help="上传的文件夹名称")
@click.pass_context
def put(ctx, dataset, dir):
    """ 上传文件到数据集 """
    if dataset == "":
        click.echo("请输入数据集名称")
        exit()
    
    if dir == "":
        click.echo("请输入上传文件夹的名称")
        exit()

    ctx.obj.PutFilesToDataset(dataset, dir)

@main.command()
@click.option("--dataset", 'dataset', default="", help="数据集名称")
@click.option("--file", 'file', default="", help="要删除的完整路径")
@click.pass_context
def delete(ctx, dataset, file):
    """ 上传文件到数据集 """
    if dataset == "":
        click.echo("请输入数据集名称")
        exit()
    
    if file == "":
        click.echo("请输入要删除的文件路径")
        exit()

    ctx.obj.DeleteFromDataset(dataset, file)
    

if __name__ == '__main__':
    main(obj={})



