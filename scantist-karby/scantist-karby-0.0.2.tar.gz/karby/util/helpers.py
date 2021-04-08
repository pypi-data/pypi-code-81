import csv
import subprocess
import traceback
import os
import zipfile


def github_url_analyzer(github_url):
    """
    https://github.com/xiandanin/magnetW.git
    git@github.com:xiandanin/magnetW.git
    :type github_url: str
    :param github_url:
    :return:
    """
    tmp_url = ""
    if github_url.startswith("git@github.com"):
        tmp_url = github_url.replace("git@github.com:", "").replace(".git", "")
    elif github_url.startswith("https"):
        tmp_url = github_url.replace("https://github.com/", "").replace(".git", "")
    else:
        raise ValueError("invalid url format. Only support github urls")
    owner_name = tmp_url.split("/")
    return owner_name[0], owner_name[1]


def project_dir_analyzer(project_dir: str):
    if os.path.isdir(project_dir):
        project_name = os.path.basename(project_dir)
        return project_name
    else:
        raise AttributeError("given url is not a project dir")


def write_issue_report(info_list, report_name, output_dir):
    field_names = [
        "Library",
        "Library Version",
        "Public ID",
        "Score",
        "Description",
        "File Path",
        "Patched Version",
        "Latest Component Version",
        "Issue Source",
        "Issue Type",
        "Priority",
        "Comments",
    ]
    try:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        with open(f"{output_dir}/{report_name}.csv", mode="w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            for info in info_list:
                writer.writerow(info.info)
    except:
        raise IOError(f"write issue report for {report_name} failed.")


def write_component_report(info_list, report_name, output_dir):
    field_names = [
        "Library",
        "Depth",
        "Version",
        "Latest Version",
        "File Path",
        "Vulnerabilities",
        "License",
        "Popularity",
        "Recommended upgrade",
        "Vulnerability List",
    ]
    try:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        with open(f"{output_dir}/{report_name}.csv", mode="w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            for info in info_list:
                writer.writerow(info.info)
    except:
        raise IOError(f"write component report for {report_name} failed.")


def exec_command(cmd, work_dir="."):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=work_dir
    )
    try:
        out, err = p.communicate()
        return_code = p.returncode
        if err:
            return {"error": err, "output": out.strip(), "code": return_code}
    except Exception as e:
        return {"error": traceback.format_exc(), "code": return_code}
    return {"output": out.strip(), "code": return_code}

def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)
            zipf.write(pathfile, arcname)
    zipf.close()
