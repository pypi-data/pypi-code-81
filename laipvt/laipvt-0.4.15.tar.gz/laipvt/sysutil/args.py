# -*- encoding: utf-8 -*-
import argparse


def Args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--targz-file', dest="targzFile", type=str, help="指定部署压缩包")
    parser.set_defaults(which='')

    subparsers = parser.add_subparsers(title='laipvt', description='命令模块分组', help='命令模块分组')
    deploy_parser = subparsers.add_parser('license', help='授权功能相关参数')
    deploy_parser.add_argument('--license-file', dest="LicenseFile",
                               type=str, help="指定需要更新的授权文件")
    deploy_parser.add_argument('--ocr-license-file', dest="OcrLicenseFile",
                               type=str, help="指定需要更新的ocr授权文件")
    deploy_parser.set_defaults(which='license')
    return parser


if __name__ == '__main__':
    args = Args().parse_args()
    print(args)
