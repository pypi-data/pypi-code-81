import argparse
import enum
import os
import sys



import pytest
from loguru import logger
from sentry_sdk import capture_message

from mkrunner import __description__, __version__
from mkrunner.compat import ensure_cli_args
from mkrunner.ext.har2case import init_har2case_parser, main_har2case
from mkrunner.make import init_make_parser, main_make
from mkrunner.scaffold import init_parser_scaffold, main_scaffold
from mkrunner.utils import init_sentry_sdk

init_sentry_sdk()


def init_parser_run(subparsers):
    sub_parser_run = subparsers.add_parser(
        "run", help="Make mkrunner testcases and run with pytest."
    )
    return sub_parser_run


def main_run(extra_args) -> enum.IntEnum:
    capture_message("start to run")
    # keep compatibility with v2
    extra_args = ensure_cli_args(extra_args)

    tests_path_list = []
    extra_args_new = []
    for item in extra_args:
        if not os.path.exists(item):
            # item is not file/folder path
            extra_args_new.append(item)
        else:
            # item is file/folder path
            tests_path_list.append(item)

    if len(tests_path_list) == 0:
        # has not specified any testcase path
        logger.error(f"No valid testcase path in cli arguments: {extra_args}")
        sys.exit(1)

    testcase_path_list = main_make(tests_path_list)
    if not testcase_path_list:
        logger.error("No valid testcases found, exit 1.")
        sys.exit(1)

    if "--tb=short" not in extra_args_new:
        extra_args_new.append("--tb=short")

    extra_args_new.extend(testcase_path_list)
    logger.info(f"start to run tests with pytest. HttpRunner version: {__version__}")

    # zsw 集成allure命令
    if not tests_path_list[0].endswith(".yml") and not tests_path_list[0].endswith("/"):
        tests_path_list[0] = tests_path_list[0] + "/"

    # if len(tests_path_list[0].split("/")) == 2:
    #     report_data_dir = "allure_result/" % tests_path_list[0].split("/")[0]
    #     report_html_dir = "allure_report/" % tests_path_list[0].split("/")[0]
    # else:
    report_data_dir = "allure_result/" #% tests_path_list[0].split("/")[1]
    report_html_dir = "allure_report/" #% tests_path_list[0].split("/")[1]

    from pathlib import Path
    # if Path(report_data_dir).exists():
    #     os.system("rm -rf %s" %  report_data_dir)

    extra_args_new.insert(0, "--alluredir=%s" % report_data_dir)

    pytest.main(extra_args_new)

    # zsw allure 增加历史趋势
    # try:

    if Path(report_html_dir).exists():
        os.system("cp -rf %shistory %s" % (report_html_dir, report_data_dir))
    # except:
    #     logger.info("第一次生成报告，无需复制历史报告记录")
    os.system("allure generate %s -o %s --clean" % (report_data_dir, report_html_dir))
    #zsw 打印报告
    print("\033[34m report_path: %s%s \033[0m" % (python_server(), report_html_dir))

    return


def main():
    """ API test: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-V", "--version", dest="version", action="store_true", help="show version"
    )

    subparsers = parser.add_subparsers(help="sub-command help")
    sub_parser_run = init_parser_run(subparsers)
    sub_parser_scaffold = init_parser_scaffold(subparsers)
    sub_parser_har2case = init_har2case_parser(subparsers)
    sub_parser_make = init_make_parser(subparsers)

    if len(sys.argv) == 1:
        # mkrunner
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        # print help for sub-commands
        if sys.argv[1] in ["-V", "--version"]:
            # mkrunner -V
            print(f"{__version__}")
        elif sys.argv[1] in ["-h", "--help"]:
            # mkrunner -h
            parser.print_help()
        elif sys.argv[1] == "startproject":
            # mkrunner startproject
            sub_parser_scaffold.print_help()
        elif sys.argv[1] == "har2case":
            # mkrunner har2case
            sub_parser_har2case.print_help()
        elif sys.argv[1] == "run":
            # mkrunner run
            pytest.main(["-h"])
        elif sys.argv[1] == "make":
            # mkrunner make
            sub_parser_make.print_help()
        sys.exit(0)
    elif (
        len(sys.argv) == 3 and sys.argv[1] == "run" and sys.argv[2] in ["-h", "--help"]
    ):
        # mkrunner run -h
        pytest.main(["-h"])
        sys.exit(0)

    extra_args = []
    if len(sys.argv) >= 2 and sys.argv[1] in ["run", "locusts"]:
        args, extra_args = parser.parse_known_args()
    else:
        args = parser.parse_args()

    if args.version:
        print(f"{__version__}")
        sys.exit(0)

    if sys.argv[1] == "run":
        sys.exit(main_run(extra_args))





    elif sys.argv[1] == "startproject":
        main_scaffold(args)
    elif sys.argv[1] == "har2case":
        main_har2case(args)
    elif sys.argv[1] == "make":
        main_make(args.testcase_path)


def main_hrun_alias():
    """ command alias
        hrun = mkrunner run
    """
    if len(sys.argv) == 2:
        if sys.argv[1] in ["-V", "--version"]:
            # hrun -V
            sys.argv = ["mkrunner", "-V"]
        elif sys.argv[1] in ["-h", "--help"]:
            pytest.main(["-h"])
            sys.exit(0)
        else:
            # hrun /path/to/testcase
            sys.argv.insert(1, "run")
    else:
        sys.argv.insert(1, "run")

    main()


def main_make_alias():
    """ command alias
        hmake = mkrunner make
    """
    sys.argv.insert(1, "make")
    main()


def main_har2case_alias():
    """ command alias
        har2case = mkrunner har2case
    """
    sys.argv.insert(1, "har2case")
    main()

def python_server(port=60000):
    lsof_data = os.popen("lsof -i:%s" % port).readlines()
    if len(lsof_data)> 1:
        lsof_data = lsof_data[1].split(" ")
        if lsof_data[0] != "Python":
            port += 1
            os.system("nohup python3 -m http.server %s >> logs/run_python.log 2>&1 &" % port)
        else:
            os.system("kill -9 %s" % lsof_data[2])
            os.system("nohup python3 -m http.server %s >> logs/run_python.log 2>&1 &" % port)
    else:
        os.system("nohup python3 -m http.server %s >> logs/run_python.log 2>&1 &" % port)
    return "http://127.0.0.1:%s/" % port



if __name__ == "__main__":
    main()
