'''
MIT License

Copyright (c) 2021 Tommy Jing-Tao Liu, CocoRobo LTD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import json, random, shutil, subprocess, logging, base64, requests, platform
import glob, io, os, time, re, datetime, sys, string, random, shlex, signal, fnmatch

import matplotlib.pyplot as plt
import numpy as np

from subprocess import Popen, PIPE
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

Configuration = {}

ModelConfiguration = "model_conf" # "conf"
ProcessedDataset = "processed_dataset" # "data"
Validation = "validation_images" # "test"
Conversion = "converted_models" # "convert"
Models = "darknet_models" # "backup"

ConfigurationSubdirectories = [
    ModelConfiguration, 
    ProcessedDataset,
    Validation,
    Conversion,
    Models
]

def ReturnResponse(operation_name, response_content, remark=""):
    response = {
        "Operation": operation_name,
        "Response": response_content,
        "Remark": remark
    }
    return response

def CheckConfiguration():
    if "RootPath" not in Configuration or "ConfigurationPath" not in Configuration or "DatasetPath" not in Configuration or "DarknetPath" not in Configuration:
        print("Error, Configuration not set, please initialize with a complete configuration set first.")
        sys.exit(0)

def CheckPlatform(input=""):
    # print("OS you're running: ", platform.system())# , platform.version())

    if input != "training":
        if platform.system() == "Linux":
            if os.path.exists(Configuration["DarknetPath"]) == False:
                os.system("git clone https://git.cocorobo.hk/CocoRoboLabs/cocorobo-ai-training-darknet-linux darknet-linux")
                print("Darknet for Ubuntu downloaded.")
            elif os.path.exists(Configuration["DarknetPath"]) == True:
                os.chdir(Configuration["DarknetPath"])
        elif platform.system() == "Darwin":
            pass
            # print("The OS you are using now currently not supported, quitting now.")
            # sys.exit(0)
    elif input == "training":
        if platform.system() == "Darwin":
            print("The OS you are using now is macOS, training features is currently not supported on this platform, quitting now.")
            sys.exit(0)


        # sys.exit(0)
        '''
        if "ARM64" in platform.version():
            print("No way to run this on an Apple M1 machine, quitting now.")
            sys.exit(0)
        '''

    return platform.system()

class init():
    def __init__(self, config):
        global Configuration

        Configuration = config

        '''
        ██      ██ ███    ██ ██    ██ ██   ██ 
        ██      ██ ████   ██ ██    ██  ██ ██  
        ██      ██ ██ ██  ██ ██    ██   ███   
        ██      ██ ██  ██ ██ ██    ██  ██ ██  
        ███████ ██ ██   ████  ██████  ██   ██ 
                                              
        '''
        if platform.system() == "Linux":

            if os.path.exists(Configuration["ConfigurationPath"]) == False:
                print("Creating configuration directory: \"" + Configuration["ConfigurationPath"] +"\"")
                os.mkdir(Configuration["ConfigurationPath"])

            for directory in ConfigurationSubdirectories:
                if os.path.exists(Configuration["ConfigurationPath"] + "/" + directory) == False:
                    print("Creating directory \"" + directory + "\" under \"" + Configuration["ConfigurationPath"] + "\"... ", end="")
                    os.mkdir(Configuration["ConfigurationPath"] + "/" + directory)
                    print("Done")

            if os.path.exists(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/darknet19_448.conv.23") == False or os.stat(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/darknet19_448.conv.23").st_size < 79320000:
                try: os.remove(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/darknet19_448.conv.23")
                except: pass

                print("Downloading transfer model...")
                model_remote_url = 'https://cocorobo-ai-resource.s3-ap-northeast-1.amazonaws.com/darknet19_448.conv.23'

                try:
                    file_name = Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/darknet19_448.conv.23"
                    with open(file_name, "wb") as f:
                        # print(" %s" % file_name)
                        response = requests.get(model_remote_url, stream = True, timeout = 300)
                        total_length = response.headers.get('content-length')

                        if total_length is None:
                            f.write(response.content)
                        else:
                            dl = 0
                            total_length = int(total_length)
                            for data in response.iter_content(chunk_size = 4096):
                                dl += len(data)
                                f.write(data)
                                done = int(50 * dl / total_length)
                                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                                sys.stdout.flush()
                    print(" Saved.")
                except BaseException as e:
                    if os.path.exists(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/darknet19_448.conv.23") == True:
                        if os.stat(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/darknet19_448.conv.23").st_size < 79320000:
                            os.remove(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/darknet19_448.conv.23")
                    print("Failed: " + str(e))

            if os.path.exists(Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/generate_train-test.py") == False or os.stat(Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/generate_train-test.py").st_size < 1600:
                try: os.remove(Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/generate_train-test.py")
                except: pass

                print("Downloading train & test image conversion script...")
                script_remote_url = "https://cocorobo-ai-resource.s3-ap-northeast-1.amazonaws.com/generate_train-test.py"

                try:
                    file_name = Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/generate_train-test.py"
                    with open(file_name, "wb") as f:
                        # print(" %s" % file_name)
                        response = requests.get(script_remote_url, stream = True, timeout = 30)
                        total_length = response.headers.get('content-length')

                        if total_length is None:
                            f.write(response.content)
                        else:
                            dl = 0
                            total_length = int(total_length)
                            for data in response.iter_content(chunk_size = 4096):
                                dl += len(data)
                                f.write(data)
                                done = int(50 * dl / total_length)
                                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                                sys.stdout.flush()
                    print(" Saved.")
                except BaseException as e:
                    if os.path.exists(Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/generate_train-test.py") == True:
                        if os.stat(Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/generate_train-test.py").st_size < 1600:
                            os.remove(Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/generate_train-test.py")
                    print("Failed: " + str(e))

            if os.path.exists(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/darknet19_448.conv.23") == False:
                print("Error, tranfer model is not here, please call init() first.")
                sys.exit(0)

            if os.path.exists(Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/generate_train-test.py") == False:
                print("Error, train & test image conversion script is not here, please call init() first.")
                sys.exit(0)

        if platform.system() == "Windows":

            if os.path.exists(Configuration["ConfigurationPath"]) == False:
                print("Creating configuration directory: \"" + Configuration["ConfigurationPath"] +"\"")
                os.mkdir(Configuration["ConfigurationPath"])

            for directory in ConfigurationSubdirectories:
                if os.path.exists(Configuration["ConfigurationPath"] + "\\" + directory) == False:
                    print("Creating directory \"" + directory + "\" under \"" + Configuration["ConfigurationPath"] + "\"... ", end="")
                    os.mkdir(Configuration["ConfigurationPath"] + "\\" + directory)
                    print("Done")

            if os.path.exists(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\darknet19_448.conv.23") == False or os.stat(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/darknet19_448.conv.23").st_size < 79320000:
                try: os.remove(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\darknet19_448.conv.23")
                except: pass

                print("Downloading transfer model...")
                model_remote_url = 'https://cocorobo-ai-resource.s3-ap-northeast-1.amazonaws.com/darknet19_448.conv.23'

                try:
                    file_name = Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\darknet19_448.conv.23"
                    with open(file_name, "wb") as f:
                        # print(" %s" % file_name)
                        response = requests.get(model_remote_url, stream = True, timeout = 300)
                        total_length = response.headers.get('content-length')

                        if total_length is None:
                            f.write(response.content)
                        else:
                            dl = 0
                            total_length = int(total_length)
                            for data in response.iter_content(chunk_size = 4096):
                                dl += len(data)
                                f.write(data)
                                done = int(50 * dl / total_length)
                                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                                sys.stdout.flush()
                    print(" Saved.")
                except BaseException as e:
                    if os.path.exists(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\darknet19_448.conv.23") == True:
                        if os.stat(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\darknet19_448.conv.23").st_size < 79320000:
                            os.remove(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\darknet19_448.conv.23")
                    print("Failed: " + str(e))

            if os.path.exists(Configuration["ConfigurationPath"] + "\\" + ProcessedDataset + "\\generate_train-test.py") == False or os.stat(Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/generate_train-test.py").st_size < 1600:
                try: os.remove(Configuration["ConfigurationPath"] + "\\" + ProcessedDataset + "\\generate_train-test.py")
                except: pass

                print("Downloading train & test image conversion script...")
                script_remote_url = "https://cocorobo-ai-resource.s3-ap-northeast-1.amazonaws.com/generate_train-test.py"

                try:
                    file_name = Configuration["ConfigurationPath"] + "\\" + ProcessedDataset + "\\generate_train-test.py"
                    with open(file_name, "wb") as f:
                        # print(" %s" % file_name)
                        response = requests.get(script_remote_url, stream = True, timeout = 30)
                        total_length = response.headers.get('content-length')

                        if total_length is None:
                            f.write(response.content)
                        else:
                            dl = 0
                            total_length = int(total_length)
                            for data in response.iter_content(chunk_size = 4096):
                                dl += len(data)
                                f.write(data)
                                done = int(50 * dl / total_length)
                                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                                sys.stdout.flush()
                    print(" Saved.")
                except BaseException as e:
                    if os.path.exists(Configuration["ConfigurationPath"] + "\\" + ProcessedDataset + "\\generate_train-test.py") == True:
                        if os.stat(Configuration["ConfigurationPath"] + "\\" + ProcessedDataset + "\\generate_train-test.py").st_size < 1600:
                            os.remove(Configuration["ConfigurationPath"] + "\\" + ProcessedDataset + "\\generate_train-test.py")
                    print("Failed: " + str(e))

            if os.path.exists(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\darknet19_448.conv.23") == False:
                print("Error, tranfer model is not here, please call init() first.")
                sys.exit(0)

            if os.path.exists(Configuration["ConfigurationPath"] + "\\" + ProcessedDataset + "\\generate_train-test.py") == False:
                print("Error, train & test image conversion script is not here, please call init() first.")
                sys.exit(0)

        CheckPlatform()

        return None

class tool():
    def __init__(self):
        CheckConfiguration()
        return None

    def display_image(self, image_base64):
        imgdata = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(imgdata))
        plt.imshow(np.array(image))
        # return np.array(image)

    def process_image(self, filename, index, name):
        newsize = (448, 448) 
        left, top, right, bottom = 0,0,0,0
        try:
            im = Image.open(filename)
            w, h = im.size

            if w > h:
                converted_length = h
                left = (w - h) / 2
                top = 0
                right = (w - h) / 2 + h
                bottom = h
            elif w < h:
                converted_length = w
                left = 0
                top = (h - w) / 2
                right = w
                bottom = (h - w) / 2 + w
            elif w == h:
                converted_length = w
                left = 0
                top = 0
                right = w
                bottom = w

            im1 = im.crop((left, top, right, bottom))
            im1 = im1.resize(newsize) 
            im1 = im1.save(name + "_converted_" + str(index) + ".jpg") 
        except BaseException as e:
            print(str(e))
            pass

    def resize_dataset(self, path):
        ResopnseOperationName = "resize_dataset"
        response_json_final = {
            "OutputLog": [],
            "ErrorMsg": None,
            "Success": None
        }
        CURRENT_DIR = Configuration["RootPath"]

        try:
            response_json_final["OutputLog"].append("Resizing every raw photos in \"" + path + "\" to 480*480px.")

            # Check if the path exists
            try:
                os.chdir(path)
            except BaseException as e:
                os.chdir(CURRENT_DIR)
                response_json_final["OutputLog"] = []
                response_json_final["ErrorMsg"] = str(e)
                response_json_final["Success"] = False
                return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

            # Detect if there are files other than JPG files and .DS_Store file.
            for file in os.listdir():
                if "jpg" not in file:
                    if ".DS_Store" != file:
                        os.chdir(CURRENT_DIR)
                        response_json_final["OutputLog"] = []
                        response_json_final["ErrorMsg"] = "Make sure you have only images in this directory."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

            # Detect if images inside this folder is already converted
            for file in os.listdir():
                try:
                    if "converted" == file.split("_")[-2]:
                        os.chdir(CURRENT_DIR)
                        response_json_final["OutputLog"] = []
                        response_json_final["ErrorMsg"] = "Images have been converted already."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                except: pass

            count, index = 0, 0
            for names_file in glob.glob("*.jpg"):
                count = count + 1

            # Start conversion
            response_json_final["OutputLog"].append("Detected " + str(count) + " images in total.")
            for names_file in glob.glob("*.jpg"):
                index = index + 1
                response_json_final["OutputLog"].append("Resizing " + names_file)
                self.process_image(names_file, index, names_file.split(".jpg")[0])
                os.remove(names_file)

            count = 0
            for file in os.listdir():
                if ".DS_Store" not in file:
                    count += 1

            os.chdir(CURRENT_DIR)

            response_json_final["OutputLog"].append(str(count)+" photos successfully resized.")
            response_json_final["Success"] = True

            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
        except Exception as e:
            os.chdir(CURRENT_DIR)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return ReturnResponse(ResopnseOperationName, {
                "Error": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            })

    def get_labeled_dataset_from_local(self, path, name):
        ResopnseOperationName = "get_labeled_dataset_from_local"
        response_json_final = {
            "OutputLog": [],
            "ErrorMsg": None,
            "Success": None
        }
        CURRENT_DIR = Configuration["RootPath"]

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                # Check if the path exists
                try:
                    os.chdir(path)
                except BaseException as e:
                    os.chdir(CURRENT_DIR)
                    response_json_final["OutputLog"] = []
                    response_json_final["ErrorMsg"] = str(e)
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                # Check if there is a .DS_Store, if exists, delete it.
                if ".DS_Store" in os.listdir():
                    # print(".DS_Store found, deleteing it.")
                    try: shutil.rmtree('.DS_Store')
                    except: os.remove('.DS_Store')

                # Check the project folder structire
                # If a directory is shown, then no pass.
                for item in os.listdir():
                    if os.path.isdir(item) == True:
                        os.chdir(CURRENT_DIR)
                        response_json_final["OutputLog"] = []
                        response_json_final["ErrorMsg"] = "Direcotry structure is in wrong format: no sub-directory is permitted to show here."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                # If no names file, then no pass
                if any("names" in s for s in os.listdir()): pass
                else:
                    os.chdir(CURRENT_DIR)
                    response_json_final["OutputLog"] = []
                    response_json_final["ErrorMsg"] = "Direcotry structure is in wrong format: no *.names file is detected."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                # Make sure only txt, jpg and names file are shown in the directory.
                for item in os.listdir():
                    if ".jpg" not in item:
                        if ".txt" not in item:
                            if ".names" not in item:
                                os.chdir(CURRENT_DIR)
                                response_json_final["OutputLog"] = []
                                response_json_final["ErrorMsg"] = "Direcotry structure is in wrong format: file in other format exists. Only *.names *.jpg and *.txt file formats are permitted to show here."
                                response_json_final["Success"] = False
                                return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                # Make sure each photo has a annotation file
                imgs, txts = [], []
                for file in os.listdir():
                    if ".jpg" in file:
                        imgs.append(file.split(".jpg")[0])
                    elif ".txt" in file:
                        txts.append(file.split(".txt")[0])
                for img in imgs:
                    if img not in txts:
                        os.chdir(CURRENT_DIR)
                        response_json_final["OutputLog"] = []
                        response_json_final["ErrorMsg"] = "Directory structure is in wrong format: " + str(img) + " has no annotation file."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                # Check complete, proceed.
                GetDatetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                RandomStr = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 2))
                name = name + "-" + GetDatetime + RandomStr
                DatasetDirectoryName = "labeled-dataset-" + name

                # Go back to root folder
                os.chdir(CURRENT_DIR)

                # Create dataset folder 
                try: os.mkdir(Configuration["DatasetPath"] + "/" + name)
                except: pass

                # Copy the labeled dataset to dataset folder
                shutil.copytree(path, Configuration["DatasetPath"] + "/" + name + "/" + DatasetDirectoryName)
                # shutil.rmtree(path)
                os.chdir(Configuration["DatasetPath"] + "/" + name + "/" + DatasetDirectoryName)
                
                for item in os.listdir():
                    if ".names" in item:
                        os.rename(item, name+".names")
                
                # Go back to root directory
                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True
                response_json_final["DatasetName"] = name

            elif platform.system() == "Windows":
                # Check if the path exists
                try:
                    os.chdir(path)
                except BaseException as e:
                    os.chdir(CURRENT_DIR)
                    response_json_final["OutputLog"] = []
                    response_json_final["ErrorMsg"] = str(e)
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                # Check if there is a .DS_Store, if exists, delete it.
                if ".DS_Store" in os.listdir():
                    # print(".DS_Store found, deleteing it.")
                    try: shutil.rmtree('.DS_Store')
                    except: os.remove('.DS_Store')

                # Check the project folder structire
                # If a directory is shown, then no pass.
                for item in os.listdir():
                    if os.path.isdir(item) == True:
                        os.chdir(CURRENT_DIR)
                        response_json_final["OutputLog"] = []
                        response_json_final["ErrorMsg"] = "Direcotry structure is in wrong format: no sub-directory is permitted to show here."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                # If no names file, then no pass
                if any("names" in s for s in os.listdir()): pass
                else:
                    os.chdir(CURRENT_DIR)
                    response_json_final["OutputLog"] = []
                    response_json_final["ErrorMsg"] = "Direcotry structure is in wrong format: no *.names file is detected."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                # Make sure only txt, jpg and names file are shown in the directory.
                for item in os.listdir():
                    if ".jpg" not in item:
                        if ".txt" not in item:
                            if ".names" not in item:
                                os.chdir(CURRENT_DIR)
                                response_json_final["OutputLog"] = []
                                response_json_final["ErrorMsg"] = "Direcotry structure is in wrong format: file in other format exists. Only *.names *.jpg and *.txt file formats are permitted to show here."
                                response_json_final["Success"] = False
                                return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                # Make sure each photo has a annotation file
                imgs, txts = [], []
                for file in os.listdir():
                    if ".jpg" in file:
                        imgs.append(file.split(".jpg")[0])
                    elif ".txt" in file:
                        txts.append(file.split(".txt")[0])
                for img in imgs:
                    if img not in txts:
                        os.chdir(CURRENT_DIR)
                        response_json_final["OutputLog"] = []
                        response_json_final["ErrorMsg"] = "Directory structure is in wrong format: " + str(img) + " has no annotation file."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                # Check complete, proceed.
                GetDatetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                RandomStr = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 2))
                name = name + "-" + GetDatetime + RandomStr
                DatasetDirectoryName = "labeled-dataset-" + name

                # Go back to root folder
                os.chdir(CURRENT_DIR)

                # Create dataset folder 
                try: os.mkdir(Configuration["DatasetPath"] + "\\" + name)
                except: pass

                # Copy the labeled dataset to dataset folder
                shutil.copytree(path, Configuration["DatasetPath"] + "\\" + name + "\\" + DatasetDirectoryName)
                # shutil.rmtree(path)
                os.chdir(Configuration["DatasetPath"] + "\\" + name + "\\" + DatasetDirectoryName)
                
                for item in os.listdir():
                    if ".names" in item:
                        os.rename(item, name+".names")
                
                # Go back to root directory
                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True
                response_json_final["DatasetName"] = name

            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
        except Exception as e:
            os.chdir(CURRENT_DIR)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return ReturnResponse(ResopnseOperationName, {
                "Error": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            })

    def list_dataset(self):
        ResopnseOperationName = "list_dataset"
        response_json_final = {
            "OutputLog": [],
            "ErrorMsg": None,
            "Success": None,
            "Datasets": [],
            "TotalCount": None
        }
        CURRENT_DIR = Configuration["RootPath"]

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                os.chdir(Configuration["DatasetPath"])

                # Get complete dataset list in the default dataset directory
                FileList = os.listdir()

                # Remvoe .DS_Store and non-directory items to prevent confusion
                for i in FileList:
                    if i == ".DS_Store" or i == "README.md":
                        FileList.remove(i)
                for i in FileList:
                    if os.path.isdir(i) == False:
                        FileList.remove(i)

                response_json_final["Datasets"] = FileList

                # Check dataset integrity
                for i in range(0, len(response_json_final["Datasets"])):
                    os.chdir(Configuration["DatasetPath"] + "/"+response_json_final["Datasets"][i])
                    name = response_json_final["Datasets"][i]

                    response_json_final["Datasets"][i] = {}
                    response_json_final["Datasets"][i]["DatasetName"] = name
                    response_json_final["Datasets"][i]["ManifestAvailable"] = False
                    for j in os.listdir():
                        if j == "dataset.manifest":
                            response_json_final["Datasets"][i]["ManifestAvailable"] = True
                            break

                    os.chdir(CURRENT_DIR)

                os.chdir(CURRENT_DIR)

                response_json_final["TotalCount"] = len(FileList)
                response_json_final["Success"] = True
          
            elif platform.system() == "Windows":
                os.chdir(Configuration["DatasetPath"])

                # Get complete dataset list in the default dataset directory
                FileList = os.listdir()

                # Remvoe .DS_Store and non-directory items to prevent confusion
                for i in FileList:
                    if i == ".DS_Store" or i == "README.md":
                        FileList.remove(i)
                for i in FileList:
                    if os.path.isdir(i) == False:
                        FileList.remove(i)

                response_json_final["Datasets"] = FileList

                # Check dataset integrity
                for i in range(0, len(response_json_final["Datasets"])):
                    os.chdir(Configuration["DatasetPath"] + "\\"+response_json_final["Datasets"][i])
                    name = response_json_final["Datasets"][i]

                    response_json_final["Datasets"][i] = {}
                    response_json_final["Datasets"][i]["DatasetName"] = name
                    response_json_final["Datasets"][i]["ManifestAvailable"] = False
                    for j in os.listdir():
                        if j == "dataset.manifest":
                            response_json_final["Datasets"][i]["ManifestAvailable"] = True
                            break

                    os.chdir(CURRENT_DIR)

                os.chdir(CURRENT_DIR)

                response_json_final["TotalCount"] = len(FileList)
                response_json_final["Success"] = True

            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
        except Exception as e:
            os.chdir(CURRENT_DIR)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return ReturnResponse(ResopnseOperationName, {
                "Error": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            })

    def describe_dataset(self, name):
        ResopnseOperationName = "describe_dataset"
        response_json_final = {
            "OutputLog": [],
            "ErrorMsg": None,
            "Success": None,
            "ProcessedStatus": None, # whether "labeled-dataset-" folder is inside the dataset directory
            "LabeledImageCount": None,
            "Labels": []
        }
        CURRENT_DIR = Configuration["RootPath"]

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                if name not in os.listdir(Configuration["DatasetPath"]):
                    os.chdir(CURRENT_DIR)
                    response_json_final.pop('ProcessedStatus', None)
                    response_json_final.pop('LabeledImageCount', None)
                    response_json_final.pop('Labels', None)
                    response_json_final["OutputLog"] = []
                    response_json_final["ErrorMsg"] = "Specified dataset does not exists."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                elif name in os.listdir(Configuration["DatasetPath"]):
                    ProcessedStatusMark = False
                    NamesFileExisting = False
                    ImageCount = 0

                    for each in os.listdir(Configuration["DatasetPath"] + "/"+name):
                        if "labeled-dataset" in each:
                            ProcessedDirectoryName = each
                            ProcessedStatusMark = True
                            response_json_final["ProcessedStatus"] = True
                            break
                    if ProcessedStatusMark == True:
                        for each in os.listdir(Configuration["DatasetPath"] + "/" + name + "/" + ProcessedDirectoryName):
                            if ".jpg" in each:
                                ImageCount += 1
                            if ".names" in each:
                                NamesFileExisting = True
                                NamesFileName = each
                        response_json_final["LabeledImageCount"] = ImageCount
                    if NamesFileExisting == True:
                        f = open(Configuration["DatasetPath"] + "/" + name + "/" + ProcessedDirectoryName + "/" + NamesFileName, "r")
                        LabelList = []
                        for each in f.readlines():
                            LabelList.append(each.strip("\n"))
                        response_json_final["Labels"] = LabelList
                        f.close()

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            elif platform.system() == "Windows":
                if name not in os.listdir(Configuration["DatasetPath"]):
                    os.chdir(CURRENT_DIR)
                    response_json_final.pop('ProcessedStatus', None)
                    response_json_final.pop('LabeledImageCount', None)
                    response_json_final.pop('Labels', None)
                    response_json_final["OutputLog"] = []
                    response_json_final["ErrorMsg"] = "Specified dataset does not exists."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                elif name in os.listdir(Configuration["DatasetPath"]):
                    ProcessedStatusMark = False
                    NamesFileExisting = False
                    ImageCount = 0

                    for each in os.listdir(Configuration["DatasetPath"] + "\\"+name):
                        if "labeled-dataset" in each:
                            ProcessedDirectoryName = each
                            ProcessedStatusMark = True
                            response_json_final["ProcessedStatus"] = True
                            break
                    if ProcessedStatusMark == True:
                        for each in os.listdir(Configuration["DatasetPath"] + "\\" + name + "\\" + ProcessedDirectoryName):
                            if ".jpg" in each:
                                ImageCount += 1
                            if ".names" in each:
                                NamesFileExisting = True
                                NamesFileName = each
                        response_json_final["LabeledImageCount"] = ImageCount
                    if NamesFileExisting == True:
                        f = open(Configuration["DatasetPath"] + "\\" + name + "\\" + ProcessedDirectoryName + "\\" + NamesFileName, "r")
                        LabelList = []
                        for each in f.readlines():
                            LabelList.append(each.strip("\n"))
                        response_json_final["Labels"] = LabelList
                        f.close()

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True


            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
        except Exception as e:
            os.chdir(CURRENT_DIR)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return ReturnResponse(ResopnseOperationName, {
                "Error": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            })

    def clear_project(self, name):
        ResopnseOperationName = "remove_project"
        response_json_final = {
            "OutputLog": [],
            "ErrorMsg": None,
            "Success": None
        }
        CURRENT_DIR = Configuration["RootPath"]

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                for each in ConfigurationSubdirectories:
                    print(each)
                    if name not in os.listdir(Configuration["ConfigurationPath"] + "/" + each):
                        response_json_final["OutputLog"].append("Project '" + name + "' folder under '" + each + "' does not existed.")
                    elif name in os.listdir(Configuration["ConfigurationPath"] + "/"+ each):
                        shutil.rmtree(Configuration["ConfigurationPath"] + "/" + each + "/" + name + "/")
                        response_json_final["OutputLog"].append("Project '" + name + "' folder under '" + each + "' successfully removed.")

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            elif platform.system() == "Windows":
                for each in ConfigurationSubdirectories:
                    print(each)
                    if name not in os.listdir(Configuration["ConfigurationPath"] + "\\" + each):
                        response_json_final["OutputLog"].append("Project '" + name + "' folder under '" + each + "' does not existed.")
                    elif name in os.listdir(Configuration["ConfigurationPath"] + "\\"+ each):
                        shutil.rmtree(Configuration["ConfigurationPath"] + "\\" + each + "\\" + name + "\\")
                        response_json_final["OutputLog"].append("Project '" + name + "' folder under '" + each + "' successfully removed.")

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
        except Exception as e:
            os.chdir(CURRENT_DIR)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return ReturnResponse(ResopnseOperationName, {
                "Error": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            })

class train():
    def __init__(self):
        CheckConfiguration()
        return None

    def get_current_time_log(self):
        return "["+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"]"

    def generate_cfg(self, project_name, conf_directory_name, classes_count):
        generate_cfg_log = {"GenerateCfgLog": []}
        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                f = open(conf_directory_name+ "/" + project_name + ".cfg", "w")
                cfg_content = ["[net]\n", "batch=64\n", "subdivisions=8\n", "width=224\n", "height=224\n", "channels=3\n", "momentum=0.9\n", "decay=0.0005\n", "angle=0\n", "saturation = 1.5\n", "exposure = 1.5\n", "hue=.1\n", "\n", "learning_rate=0.001\n", "burn_in=1000\n", "max_batches = 500200\n", "policy=steps\n", "steps=400000,450000\n", "scales=.1,.1\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=16\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=32\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=64\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=128\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=256\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=512\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[convolutional]\n", "size=1\n", "stride=1\n", "pad=1\n", "# filters=(classes + 5)*5\n", "filters="+str(int((float(classes_count)+5)*5))+"\n", "activation=linear\n", "\n", "[region]\n", "anchors = 0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828\n", "bias_match=1\n", "classes="+str(int(float(classes_count)))+"\n", "coords=4\n", "num=5\n", "softmax=1\n", "jitter=.2\n", "rescore=0\n", "\n", "object_scale=5\n", "noobject_scale=1\n", "class_scale=1\n", "coord_scale=1\n", "\n", "absolute=1\n", "thresh = .6\n", "random=1\n"]
                # ["[net]\n", "Training\n", "batch=64\n", "subdivisions=16\n", "width=224\n", "height=224\n", "channels=3\n", "momentum=0.9\n", "decay=0.0005\n", "angle=0\n", "saturation = 1.5\n", "exposure = 1.5\n", "hue=.1\n\n", "learning_rate=0.001\n", "burn_in=1000\n", "max_batches=" + str(int(float(classes_count))*2000) +"\n", "policy=steps\n", "steps=" + str(int(float(classes_count))*0.8) + "," + str(int(float(classes_count))*0.9) + "\n", "scales=.1,.1\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=16\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=32\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=64\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=128\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=256\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=512\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[convolutional]\n", "size=1\n", "stride=1\n", "pad=1\n", "filters=" + str((int(float(classes_count)) + 5) * 5) + "\n", "activation=linear\n\n", "[region]\n", "anchors = 0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828\n", "bias_match=1\n", "classes=" + str(int(float(classes_count))) + "\n", "coords=4\n", "num=5\n", "softmax=1\n", "jitter=.2\n", "rescore=0\n\n", "object_scale=5\n", "noobject_scale=1\n", "class_scale=1\n", "coord_scale=1\n\n", "absolute=1\n", "thresh = .6\n", "random=1"]
                f.writelines(cfg_content)
                f.close()
                generate_cfg_log["GenerateCfgLog"].append("Generating " + project_name + ".cfg to theconf directory ...")

            elif platform.system() == "Windows":
                f = open(conf_directory_name+ "\\" + project_name + ".cfg", "w")
                cfg_content = ["[net]\n", "batch=64\n", "subdivisions=8\n", "width=224\n", "height=224\n", "channels=3\n", "momentum=0.9\n", "decay=0.0005\n", "angle=0\n", "saturation = 1.5\n", "exposure = 1.5\n", "hue=.1\n", "\n", "learning_rate=0.001\n", "burn_in=1000\n", "max_batches = 500200\n", "policy=steps\n", "steps=400000,450000\n", "scales=.1,.1\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=16\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=32\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=64\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=128\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=256\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=512\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[convolutional]\n", "size=1\n", "stride=1\n", "pad=1\n", "# filters=(classes + 5)*5\n", "filters="+str(int((float(classes_count)+5)*5))+"\n", "activation=linear\n", "\n", "[region]\n", "anchors = 0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828\n", "bias_match=1\n", "classes="+str(int(float(classes_count)))+"\n", "coords=4\n", "num=5\n", "softmax=1\n", "jitter=.2\n", "rescore=0\n", "\n", "object_scale=5\n", "noobject_scale=1\n", "class_scale=1\n", "coord_scale=1\n", "\n", "absolute=1\n", "thresh = .6\n", "random=1\n"]
                # ["[net]\n", "Training\n", "batch=64\n", "subdivisions=16\n", "width=224\n", "height=224\n", "channels=3\n", "momentum=0.9\n", "decay=0.0005\n", "angle=0\n", "saturation = 1.5\n", "exposure = 1.5\n", "hue=.1\n\n", "learning_rate=0.001\n", "burn_in=1000\n", "max_batches=" + str(int(float(classes_count))*2000) +"\n", "policy=steps\n", "steps=" + str(int(float(classes_count))*0.8) + "," + str(int(float(classes_count))*0.9) + "\n", "scales=.1,.1\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=16\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=32\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=64\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=128\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=256\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=512\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[convolutional]\n", "size=1\n", "stride=1\n", "pad=1\n", "filters=" + str((int(float(classes_count)) + 5) * 5) + "\n", "activation=linear\n\n", "[region]\n", "anchors = 0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828\n", "bias_match=1\n", "classes=" + str(int(float(classes_count))) + "\n", "coords=4\n", "num=5\n", "softmax=1\n", "jitter=.2\n", "rescore=0\n\n", "object_scale=5\n", "noobject_scale=1\n", "class_scale=1\n", "coord_scale=1\n\n", "absolute=1\n", "thresh = .6\n", "random=1"]
                f.writelines(cfg_content)
                f.close()
                generate_cfg_log["GenerateCfgLog"].append("Generating " + project_name + ".cfg to theconf directory ...")
            return generate_cfg_log
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return {
                "GenerateCfgError": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            }


    def generate_data(self, project_name, conf_directory_name, classes_count, current_directory_path):
        generate_data_log = {"GenerateDataLog": []}
        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                f = open(conf_directory_name+ "/" + project_name + ".data", "w")

                data_content = [
                    "classes="+ str(int(float(classes_count))) +"\n",
                    "train  = " + Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/" + project_name + "/train.txt\n",
                    "valid  = " + Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/" + project_name + "/test.txt\n",
                    "names = " + Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + project_name + "/" + project_name + ".names\n",
                    "backup = " + Configuration["ConfigurationPath"] + "/" + Models + "/" + project_name + "\n"
                ]

                f.writelines(data_content)
                f.close()
                generate_data_log["GenerateDataLog"].append("Generating " + project_name + ".data to the conf directory ...")

            elif platform.system() == "Windows":
                f = open(conf_directory_name+ "\\" + project_name + ".data", "w")

                data_content = [
                    "classes="+ str(int(float(classes_count))) +"\n",
                    "train  = " + Configuration["ConfigurationPath"] + "\\" + ProcessedDataset + "\\" + project_name + "\\train.txt\n",
                    "valid  = " + Configuration["ConfigurationPath"] + "\\" + ProcessedDataset + "\\" + project_name + "\\test.txt\n",
                    "names = " + Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + project_name + "\\" + project_name + ".names\n",
                    "backup = " + Configuration["ConfigurationPath"] + "\\" + Models + "\\" + project_name + "\n"
                ]

                f.writelines(data_content)
                f.close()
                generate_data_log["GenerateDataLog"].append("Generating " + project_name + ".data to the conf directory ...")
            return generate_data_log
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return {
                "GenerateDataError": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            }


    def generate_names(self, project_name, conf_directory_name, current_directory_path, dataset_file_path):
        generate_names_log = {"GenerateNamesLog": []}

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                os.chdir(dataset_file_path)

                names_file_name = ""
                for names_file in glob.glob("*.names"):
                    names_file_name = names_file

                f = open(names_file_name,"r+")
                read_original_names = f.readlines()
                f.close()

                os.chdir(current_directory_path)

                f2 = open(Configuration["ConfigurationPath"] + "/" + conf_directory_name + "/" + project_name + ".names", "w")
                f2.writelines(read_original_names)
                f.close()

                generate_names_log["GenerateNamesLog"].append("Generating .names file: "+str(read_original_names)+" ...")

            elif platform.system() == "Windows":
                os.chdir(dataset_file_path)

                names_file_name = ""
                for names_file in glob.glob("*.names"):
                    names_file_name = names_file

                f = open(names_file_name,"r+")
                read_original_names = f.readlines()
                f.close()

                os.chdir(current_directory_path)

                f2 = open(Configuration["ConfigurationPath"] + "\\" + conf_directory_name + "\\" + project_name + ".names", "w")
                f2.writelines(read_original_names)
                f.close()

                generate_names_log["GenerateNamesLog"].append("Generating .names file: "+str(read_original_names)+" ...")
            return generate_names_log
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return {
                "GenerateNamesError": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            }

    def generate_testing_bash(self, project_name, conf_directory_name, current_directory_path):
        generate_testing_bash_log = {"GenerateTestingBashLog": []}

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                os.chdir(Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/" + project_name)
                num_lines = sum(1 for line in open('train.txt'))

                f=open('train.txt')
                lines=f.readlines()
                cont_line = random.sample(range(num_lines), 1)
                for i in range(0,1,1):
                    content = lines[cont_line[i]]
                    content = content.strip('\n')
                    os.system("cp " + content + " " + Configuration["ConfigurationPath"] + "/" + Validation + "/" + project_name + "/" + project_name + "_test.jpg")
                f.close()
                os.chdir(current_directory_path)

                f = open(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + project_name + "/test-train.sh", "w")
                '''
                ModelConfiguration = "conf"
                ProcessedDataset = "data"
                Validation = "test"
                Conversion = "convert"
                Models = "backup"
                '''
                bash_content = [
                    "TEST_IMAGE_PATH=\"" + Configuration["ConfigurationPath"] + "/" + Validation + "/" + project_name + "/" + project_name + "_test.jpg\"\n",
                    "TEST_MODEL_PATH=\"" + Configuration["ConfigurationPath"] + "/" + Models + "/" + project_name + "/" + project_name + "_last.weights\"\n",
                    "\n",
                    "while getopts \":m:f:\" opt; do\n",
                    "    case $opt in\n",
                    "        m) arg_m=\"$OPTARG\"\n",
                    "        ;;\n",
                    "        f) arg_f=\"$OPTARG\"\n",
                    "        ;;\n",
                    "    esac\n",
                    "done\n",
                    "\n",
                    "if [ -z \"$arg_m\" ]\n",
                    "then\n",
                    "      echo \"Using latest_generated_model.\"\n",
                    "else\n",
                    "      TEST_MODEL_PATH=$arg_m\n",
                    "fi\n",
                    "\n",
                    "if [ -z \"$arg_f\" ]\n",
                    "then\n",
                    "      echo \"Using defaul test image.\"\n",
                    "else\n",
                    "      TEST_IMAGE_PATH=$arg_f\n",
                    "fi\n",
                    "\n",
                    "echo $TEST_MODEL_PATH\n",
                    "echo $TEST_IMAGE_PATH\n",
                    "\n",
                    "cd " + Configuration["DarknetPath"] + "\n",
                    "FILE='./" + project_name + "_test_result.log'\n",
                    "STRING='milli-seconds'\n",
                    "nohup ./darknet detector test " + Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + project_name + "/" + project_name + ".data " + Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + project_name + "/" + project_name + ".cfg $TEST_MODEL_PATH $TEST_IMAGE_PATH > " + project_name + "_test_result.log 2>&1 &\n",
                    "TEST_PID=$!\n",
                    "while true\n",
                    "do\n",
                    "    echo \"Waiting for result...\"\n",
                    "    sleep 1\n",
                    "    if  grep -q $STRING $FILE ; then\n",
                    "        echo 'Done testing' ;\n",
                    "        # kill -9 $TEST_PID\n",
                    "        sleep 2\n",
                    "        break\n",
                    "    fi\n",
                    "done\n",
                    "sleep 2\n",
                    "cp " + project_name + "_test_result.log " + Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + project_name + "/\n",
                    "cp predictions.jpg " + Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + project_name + "/" + project_name + "predictions.jpg\n",
                    "cd " + current_directory_path + "\n"
                ]
                f.writelines(bash_content)
                f.close()
                os.chdir(current_directory_path)

                generate_testing_bash_log["GenerateTestingBashLog"].append("Generating test image.")

            elif platform.system() == "Windows":
                os.chdir(Configuration["ConfigurationPath"] + "\\" + ProcessedDataset + "\\" + project_name)
                num_lines = sum(1 for line in open('train.txt'))

                f=open('train.txt')
                lines=f.readlines()
                cont_line = random.sample(range(num_lines), 1)
                for i in range(0,1,1):
                    content = lines[cont_line[i]]
                    content = content.strip('\n')
                    os.system("cp " + content + " " + Configuration["ConfigurationPath"] + "\\" + Validation + "\\" + project_name + "\\" + project_name + "_test.jpg")
                f.close()
                os.chdir(current_directory_path)

                f = open(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + project_name + "\\test-train.sh", "w")
                '''
                ModelConfiguration = "conf"
                ProcessedDataset = "data"
                Validation = "test"
                Conversion = "convert"
                Models = "backup"
                '''
                bash_content = [
                    "TEST_IMAGE_PATH=\"" + Configuration["ConfigurationPath"] + "\\" + Validation + "\\" + project_name + "\\" + project_name + "_test.jpg\"\n",
                    "TEST_MODEL_PATH=\"" + Configuration["ConfigurationPath"] + "\\" + Models + "\\" + project_name + "\\" + project_name + "_last.weights\"\n",
                    "\n",
                    "while getopts \":m:f:\" opt; do\n",
                    "    case $opt in\n",
                    "        m) arg_m=\"$OPTARG\"\n",
                    "        ;;\n",
                    "        f) arg_f=\"$OPTARG\"\n",
                    "        ;;\n",
                    "    esac\n",
                    "done\n",
                    "\n",
                    "if [ -z \"$arg_m\" ]\n",
                    "then\n",
                    "      echo \"Using latest_generated_model.\"\n",
                    "else\n",
                    "      TEST_MODEL_PATH=$arg_m\n",
                    "fi\n",
                    "\n",
                    "if [ -z \"$arg_f\" ]\n",
                    "then\n",
                    "      echo \"Using defaul test image.\"\n",
                    "else\n",
                    "      TEST_IMAGE_PATH=$arg_f\n",
                    "fi\n",
                    "\n",
                    "echo $TEST_MODEL_PATH\n",
                    "echo $TEST_IMAGE_PATH\n",
                    "\n",
                    "cd " + Configuration["DarknetPath"] + "\n",
                    "FILE='.\\" + project_name + "_test_result.log'\n",
                    "STRING='milli-seconds'\n",
                    "nohup .\\darknet.exe detector test " + Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + project_name + "\\" + project_name + ".data " + Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + project_name + "\\" + project_name + ".cfg $TEST_MODEL_PATH $TEST_IMAGE_PATH > " + project_name + "_test_result.log 2>&1 &\n",
                    "TEST_PID=$!\n",
                    "while true\n",
                    "do\n",
                    "    echo \"Waiting for result...\"\n",
                    "    sleep 1\n",
                    "    if  grep -q $STRING $FILE ; then\n",
                    "        echo 'Done testing' ;\n",
                    "        # kill -9 $TEST_PID\n",
                    "        sleep 2\n",
                    "        break\n",
                    "    fi\n",
                    "done\n",
                    "sleep 2\n",
                    "cp " + project_name + "_test_result.log " + Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + project_name + "\\\n",
                    "cp predictions.jpg " + Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + project_name + "\\" + project_name + "predictions.jpg\n",
                    "cd " + current_directory_path + "\n"
                ]
                f.writelines(bash_content)
                f.close()
                os.chdir(current_directory_path)

                generate_testing_bash_log["GenerateTestingBashLog"].append("Generating test image.")

            return generate_testing_bash_log
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return {
                "GenerateTestingBashError": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            }

    def generate_nohup_training_script(self, name, conf_directory_name):
        generate_nohup_training_script_log = {"GenerateNohupScriptLog": []}

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                CURRENT_DIR = Configuration["RootPath"]

                TRAIN_CLI = Configuration["DarknetPath"] + "/darknet"
                TRAIN_PARAMETER = "detector train"
                TRAIN_PROJECT_DATA = Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/" + name + ".data"
                TRAIN_PROJECT_CFG = Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/" + name + ".cfg"
                TRAIN_MODEL_PATH = Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/darknet19_448.conv.23"
                CMD_SEP = " "

                TRAINING_FULL_COMMAND = TRAIN_CLI + CMD_SEP + TRAIN_PARAMETER + CMD_SEP + TRAIN_PROJECT_DATA + CMD_SEP + TRAIN_PROJECT_CFG + CMD_SEP + TRAIN_MODEL_PATH

                f = open(Configuration["ConfigurationPath"] + "/" + conf_directory_name+ "/start-train.sh", "w")

                train_check_content = [
                    "nohup " + TRAINING_FULL_COMMAND + " > " + Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/" + "nohup.log 2>&1 &\n",
                    "echo $! > " + Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/save_pid.txt\n"
                ]

                f.writelines(train_check_content)
                f.close()
        
                generate_nohup_training_script_log["GenerateNohupScriptLog"].append("Generating training script...")

            elif platform.system() == "Windows":
                CURRENT_DIR = Configuration["RootPath"]

                TRAIN_CLI = Configuration["DarknetPath"] + "\\darknet.exe"
                TRAIN_PARAMETER = "detector train"
                TRAIN_PROJECT_DATA = Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\" + name + ".data"
                TRAIN_PROJECT_CFG = Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\" + name + ".cfg"
                TRAIN_MODEL_PATH = Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\darknet19_448.conv.23"
                CMD_SEP = " "

                TRAINING_FULL_COMMAND = TRAIN_CLI + CMD_SEP + TRAIN_PARAMETER + CMD_SEP + TRAIN_PROJECT_DATA + CMD_SEP + TRAIN_PROJECT_CFG + CMD_SEP + TRAIN_MODEL_PATH

                f = open(Configuration["ConfigurationPath"] + "\\" + conf_directory_name+ "\\start-train.sh", "w")

                train_check_content = [
                    "nohup " + TRAINING_FULL_COMMAND + " > " + Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\" + "nohup.log 2>&1 &\n",
                    "echo $! > " + Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\save_pid.txt\n"
                ]

                f.writelines(train_check_content)
                f.close()
        
                generate_nohup_training_script_log["GenerateNohupScriptLog"].append("Generating training script...")
            return generate_nohup_training_script_log
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return {
                "GenerateNohupScriptError": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            }

    def run_command(self, command):
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        output = process.stdout.readline()
        return output

    def prepare(self, name):
        ResopnseOperationName = "train_prepare"
        response_json_final = {
            "OutputLog": [],
            "ErrorMsg": None,
            "Success": None
        }
        CURRENT_DIR = Configuration["RootPath"]

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                if name not in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration):
                    os.chdir(Configuration["ConfigurationPath"])

                    ToBeCreatedDirectories = [
                        ModelConfiguration + "/", # conf
                        ProcessedDataset + "/", # data
                        Models + "/", # backup
                        Validation + "/", # test
                        Conversion + "/" # test
                    ]
                    
                    for each_directory in ToBeCreatedDirectories:
                        if name in os.listdir(each_directory):
                            os.system("rm -rf " + each_directory + name + "/")
                            response_json_final["OutputLog"].append({"Generate" + each_directory.strip("/").upper() + "Log": "Creating project-specific directory under \"" + each_directory + "\": " + name })
                            os.mkdir(each_directory+name)
                        elif name not in os.listdir(each_directory):
                            response_json_final["OutputLog"].append({"Generate" + each_directory.strip("/").upper() + "Log": "Creating project-specific directory under \"" + each_directory + "\": " + name })
                            os.mkdir(each_directory+name)

                    ModelConfigurationDirName = ModelConfiguration + "/" + name
                    DatasetDirPath = Configuration["DatasetPath"] + "/" + name + "/labeled-dataset-" + name + "/"

                    f = open(DatasetDirPath + name + ".names", "r")
                    ClassesExtractedFromFile = f.read().split("\n")
                    while("" in ClassesExtractedFromFile): ClassesExtractedFromFile.remove("") 
                    f.close()

                    ClassCount = str(len(ClassesExtractedFromFile))
                    os.system("cp -a "+ DatasetDirPath + "/. " + ProcessedDataset + "/" + name)

                    generate_cfg_log = self.generate_cfg(name, ModelConfigurationDirName, ClassCount)
                    response_json_final["OutputLog"].append(generate_cfg_log)

                    generate_data_log = self.generate_data(name, ModelConfigurationDirName, ClassCount, CURRENT_DIR)
                    response_json_final["OutputLog"].append(generate_data_log)

                    generate_names_log = self.generate_names(name, ModelConfigurationDirName, CURRENT_DIR, DatasetDirPath)
                    response_json_final["OutputLog"].append(generate_names_log)

                    generate_nohup_training_script_log = self.generate_nohup_training_script(name, ModelConfigurationDirName)
                    response_json_final["OutputLog"].append(generate_nohup_training_script_log)

                    os.chdir(Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/" + name)
                    response_json_final["OutputLog"].append({ "GenerateTrainTextLog": ["Generating train.txt and test.txt"]})

                    shutil.copy("../generate_train-test.py", "./generate_train-test.py")
                    self.run_command("python generate_train-test.py")

                    os.chdir(CURRENT_DIR)

                    generate_testing_bash_log = self.generate_testing_bash(name, ModelConfigurationDirName, CURRENT_DIR)
                    response_json_final["OutputLog"].append(generate_testing_bash_log)

                    os.chdir(CURRENT_DIR)

                    # Check if everything is there

                    '''
                    ModelConfiguration = "conf"
                    ProcessedDataset = "data"
                    Validation = "test"
                    Conversion = "convert"
                    Models = "backup"
                    '''

                    ModelConfigurationCheckCfg, ModelConfigurationCheckData, ModelConfigurationCheckNames, ModelConfigurationCheckStart, ModelConfigurationCheckTest = False, False, False, False, False
                    ProcessedDatasetCheck = False
                    ValidationCheck = False
                    ConversionCheck = False
                    ModelsCheck = False

                    for file in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name):
                        if file == "test-train.sh":
                            ModelConfigurationCheckTest = True
                        elif file == "start-train.sh":
                            ModelConfigurationCheckStart = True
                        elif ".data" in file:
                            ModelConfigurationCheckData = True
                        elif ".cfg" in file:
                            ModelConfigurationCheckCfg = True
                        elif ".names" in file:
                            ModelConfigurationCheckNames = True

                    if name in os.listdir(Configuration["ConfigurationPath"] + "/" + ProcessedDataset):
                        ProcessedDatasetCheck = True

                    if name in os.listdir(Configuration["ConfigurationPath"] + "/" + Validation):
                        ValidationCheck = True

                    if name in os.listdir(Configuration["ConfigurationPath"] + "/" + Conversion):
                        ConversionCheck = True

                    if name in os.listdir(Configuration["ConfigurationPath"] + "/" + Models):
                        ModelsCheck = True

                    IntegrityCheck = [
                        ModelConfigurationCheckCfg,
                        ModelConfigurationCheckData,
                        ModelConfigurationCheckNames,
                        ModelConfigurationCheckStart,
                        ModelConfigurationCheckTest,
                        ProcessedDatasetCheck,
                        ValidationCheck,
                        ConversionCheck,
                        ModelsCheck
                    ]

                    for check in IntegrityCheck:
                        if check == False:
                            response_json_final["Success"] = False
                            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                elif name in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration):
                    response_json_final["ErrorMsg"] = "Dataset already processed."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            elif platform.system() == "Windows":
                if name not in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration):
                    os.chdir(Configuration["ConfigurationPath"])

                    ToBeCreatedDirectories = [
                        ModelConfiguration + "\\", # conf
                        ProcessedDataset + "\\", # data
                        Models + "\\", # backup
                        Validation + "\\", # test
                        Conversion + "\\" # test
                    ]
                    
                    for each_directory in ToBeCreatedDirectories:
                        if name in os.listdir(each_directory):
                            os.system("rm -rf " + each_directory + name + "\\")
                            response_json_final["OutputLog"].append({"Generate" + each_directory.strip("\\").upper() + "Log": "Creating project-specific directory under \"" + each_directory + "\": " + name })
                            os.mkdir(each_directory+name)
                        elif name not in os.listdir(each_directory):
                            response_json_final["OutputLog"].append({"Generate" + each_directory.strip("\\").upper() + "Log": "Creating project-specific directory under \"" + each_directory + "\": " + name })
                            os.mkdir(each_directory+name)

                    ModelConfigurationDirName = ModelConfiguration + "\\" + name
                    DatasetDirPath = Configuration["DatasetPath"] + "\\" + name + "\\labeled-dataset-" + name + "\\"

                    f = open(DatasetDirPath + name + ".names", "r")
                    ClassesExtractedFromFile = f.read().split("\n")
                    while("" in ClassesExtractedFromFile): ClassesExtractedFromFile.remove("") 
                    f.close()

                    ClassCount = str(len(ClassesExtractedFromFile))
                    os.system("cp -a "+ DatasetDirPath + "\\. " + ProcessedDataset + "\\" + name)

                    generate_cfg_log = self.generate_cfg(name, ModelConfigurationDirName, ClassCount)
                    response_json_final["OutputLog"].append(generate_cfg_log)

                    generate_data_log = self.generate_data(name, ModelConfigurationDirName, ClassCount, CURRENT_DIR)
                    response_json_final["OutputLog"].append(generate_data_log)

                    generate_names_log = self.generate_names(name, ModelConfigurationDirName, CURRENT_DIR, DatasetDirPath)
                    response_json_final["OutputLog"].append(generate_names_log)

                    generate_nohup_training_script_log = self.generate_nohup_training_script(name, ModelConfigurationDirName)
                    response_json_final["OutputLog"].append(generate_nohup_training_script_log)

                    os.chdir(Configuration["ConfigurationPath"] + "\\" + ProcessedDataset + "\\" + name)
                    response_json_final["OutputLog"].append({ "GenerateTrainTextLog": ["Generating train.txt and test.txt"]})

                    shutil.copy("..\\generate_train-test.py", ".\\generate_train-test.py")
                    self.run_command("python generate_train-test.py")

                    os.chdir(CURRENT_DIR)

                    generate_testing_bash_log = self.generate_testing_bash(name, ModelConfigurationDirName, CURRENT_DIR)
                    response_json_final["OutputLog"].append(generate_testing_bash_log)

                    os.chdir(CURRENT_DIR)

                    # Check if everything is there

                    '''
                    ModelConfiguration = "conf"
                    ProcessedDataset = "data"
                    Validation = "test"
                    Conversion = "convert"
                    Models = "backup"
                    '''

                    ModelConfigurationCheckCfg, ModelConfigurationCheckData, ModelConfigurationCheckNames, ModelConfigurationCheckStart, ModelConfigurationCheckTest = False, False, False, False, False
                    ProcessedDatasetCheck = False
                    ValidationCheck = False
                    ConversionCheck = False
                    ModelsCheck = False

                    for file in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name):
                        if file == "test-train.sh":
                            ModelConfigurationCheckTest = True
                        elif file == "start-train.sh":
                            ModelConfigurationCheckStart = True
                        elif ".data" in file:
                            ModelConfigurationCheckData = True
                        elif ".cfg" in file:
                            ModelConfigurationCheckCfg = True
                        elif ".names" in file:
                            ModelConfigurationCheckNames = True

                    if name in os.listdir(Configuration["ConfigurationPath"] + "\\" + ProcessedDataset):
                        ProcessedDatasetCheck = True

                    if name in os.listdir(Configuration["ConfigurationPath"] + "\\" + Validation):
                        ValidationCheck = True

                    if name in os.listdir(Configuration["ConfigurationPath"] + "\\" + Conversion):
                        ConversionCheck = True

                    if name in os.listdir(Configuration["ConfigurationPath"] + "\\" + Models):
                        ModelsCheck = True

                    IntegrityCheck = [
                        ModelConfigurationCheckCfg,
                        ModelConfigurationCheckData,
                        ModelConfigurationCheckNames,
                        ModelConfigurationCheckStart,
                        ModelConfigurationCheckTest,
                        ProcessedDatasetCheck,
                        ValidationCheck,
                        ConversionCheck,
                        ModelsCheck
                    ]

                    for check in IntegrityCheck:
                        if check == False:
                            response_json_final["Success"] = False
                            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                elif name in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration):
                    response_json_final["ErrorMsg"] = "Dataset already processed."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
        except Exception as e:
            os.chdir(CURRENT_DIR)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return ReturnResponse(ResopnseOperationName, {
                "Error": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            })

    def start(self, name):
        ResopnseOperationName = "train_start"
        response_json_final = {
            "OutputLog": [],
            "ErrorMsg": None,
            "Success": None
        }
        CURRENT_DIR = Configuration["RootPath"]

        CheckPlatform("training")

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                if name in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration):
                    if "save_pid.txt" in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/"):
                        f = open(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/save_pid.txt")
                        pid = str(f.readlines()[0].strip("\n"))
                        response_json_final["PID"] = pid
                        f.close()
                        os.chdir(CURRENT_DIR)
                        response_json_final["ErrorMsg"] = "Training already in progress, PID is " + pid
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                    elif "save_pid.txt" not in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/"):
                        os.system("bash " + Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/start-train.sh")
                        time.sleep(1)

                        f = open(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/nohup.log")
                        nohup_read = f.readlines()
                        f.close()

                        for line in nohup_read:
                            if "cannot execute binary file" in line:
                                os.system("rm "+ Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/save_pid.txt")
                                os.system("rm "+ Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/nohup.log")

                                os.chdir(CURRENT_DIR)
                                response_json_final["ErrorMsg"] = "Unable to run darknet on this machine."
                                response_json_final["Success"] = False
                                return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                        log = "Training started..."
                        response_json_final["OutputLog"] = log

                elif name not in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration):
                    os.chdir(CURRENT_DIR)
                    response_json_final["OutputLog"] = []
                    response_json_final["ErrorMsg"] = "Project does not exists or is not prepared yet."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            elif platform.system() == "Windows":
                if name in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration):
                    if "save_pid.txt" in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\"):
                        f = open(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "/save_pid.txt")
                        pid = str(f.readlines()[0].strip("\n"))
                        response_json_final["PID"] = pid
                        f.close()
                        os.chdir(CURRENT_DIR)
                        response_json_final["ErrorMsg"] = "Training already in progress, PID is " + pid
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                    elif "save_pid.txt" not in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\"):
                        os.system("bash " + Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\start-train.sh")
                        time.sleep(1)

                        f = open(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\nohup.log")
                        nohup_read = f.readlines()
                        f.close()

                        for line in nohup_read:
                            if "cannot execute binary file" in line:
                                os.system("rm "+ Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\save_pid.txt")
                                os.system("rm "+ Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\nohup.log")

                                os.chdir(CURRENT_DIR)
                                response_json_final["ErrorMsg"] = "Unable to run darknet on this machine."
                                response_json_final["Success"] = False
                                return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                        log = "Training started..."
                        response_json_final["OutputLog"] = log

                elif name not in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration):
                    os.chdir(CURRENT_DIR)
                    response_json_final["OutputLog"] = []
                    response_json_final["ErrorMsg"] = "Project does not exists or is not prepared yet."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return ReturnResponse(ResopnseOperationName, {
                "Error": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            })


    def list_jobs(self):
        ResopnseOperationName = "list_jobs"
        response_json_final = {
            "OutputLog": [],
            "ErrorMsg": None,
            "Success": None,
            "JobList": []
        }
        CURRENT_DIR = Configuration["RootPath"]

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                os.chdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/")

                all_directories = []
                all_jobs = []

                for i in os.listdir():
                    # print(i, ":", os.path.isdir(i))
                    if os.path.isdir(i) == True:
                        all_directories.append(i)

                # all_directories.pop(all_directories.index(".DS_Store"))

                count = 0
                for project in all_directories:
                    os.chdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + project)
                    project_dict = {}
                    all_jobs.append(project_dict)
                    # print(os.listdir())
                    all_jobs[count]["name"] = str(project)

                    if "nohup.log" in os.listdir():
                        # print("\t nohup.log exists.")
                        all_jobs[count]["nohup_available"] = True
                    elif "nohup.log" not in os.listdir():
                        all_jobs[count]["nohup_available"] = False

                    if "save_pid.txt" in os.listdir():
                        # print("\t currently running.")
                        all_jobs[count]["pid_available"] = True
                    elif "save_pid.txt" not in os.listdir():
                        all_jobs[count]["pid_available"] = False

                    if "training_analytics.json" in os.listdir():
                        # print("\t analytics available.")
                        all_jobs[count]["analytics_available"] = True
                    elif "training_analytics.json" not in os.listdir():
                        all_jobs[count]["analytics_available"] = False

                    if project+"predictions.jpg" in os.listdir():
                        # print("\t predicted image available.")
                        all_jobs[count]["prediction_available"] = True
                    elif project+"predictions.jpg" not in os.listdir():
                        all_jobs[count]["prediction_available"] = False

                    if project+"_test_result.log" in os.listdir():
                        # print("\t prediction result available.")
                        all_jobs[count]["prediction_result_available"] = True
                    elif project+"_test_result.log" not in os.listdir():
                        all_jobs[count]["prediction_result_available"] = False

                    all_jobs[count]["kmodel_available"] = False

                    os.chdir("../")

                    os.chdir(Configuration["ConfigurationPath"] + "/" + Conversion + "/")
                    for file in os.listdir():
                        if "kmodel" in file:
                            if file[0:-7] == all_jobs[count]["name"]:
                                all_jobs[count]["kmodel_available"] = True
                    os.chdir(CURRENT_DIR)

                    count += 1
                
                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True
                response_json_final["JobList"] = all_jobs

            elif platform.system() == "Windows":
                os.chdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\")

                all_directories = []
                all_jobs = []

                for i in os.listdir():
                    # print(i, ":", os.path.isdir(i))
                    if os.path.isdir(i) == True:
                        all_directories.append(i)

                # all_directories.pop(all_directories.index(".DS_Store"))

                count = 0
                for project in all_directories:
                    os.chdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + project)
                    project_dict = {}
                    all_jobs.append(project_dict)
                    # print(os.listdir())
                    all_jobs[count]["name"] = str(project)

                    if "nohup.log" in os.listdir():
                        # print("\t nohup.log exists.")
                        all_jobs[count]["nohup_available"] = True
                    elif "nohup.log" not in os.listdir():
                        all_jobs[count]["nohup_available"] = False

                    if "save_pid.txt" in os.listdir():
                        # print("\t currently running.")
                        all_jobs[count]["pid_available"] = True
                    elif "save_pid.txt" not in os.listdir():
                        all_jobs[count]["pid_available"] = False

                    if "training_analytics.json" in os.listdir():
                        # print("\t analytics available.")
                        all_jobs[count]["analytics_available"] = True
                    elif "training_analytics.json" not in os.listdir():
                        all_jobs[count]["analytics_available"] = False

                    if project+"predictions.jpg" in os.listdir():
                        # print("\t predicted image available.")
                        all_jobs[count]["prediction_available"] = True
                    elif project+"predictions.jpg" not in os.listdir():
                        all_jobs[count]["prediction_available"] = False

                    if project+"_test_result.log" in os.listdir():
                        # print("\t prediction result available.")
                        all_jobs[count]["prediction_result_available"] = True
                    elif project+"_test_result.log" not in os.listdir():
                        all_jobs[count]["prediction_result_available"] = False

                    all_jobs[count]["kmodel_available"] = False

                    os.chdir("..\\")

                    os.chdir(Configuration["ConfigurationPath"] + "\\" + Conversion + "\\")
                    for file in os.listdir():
                        if "kmodel" in file:
                            if file[0:-7] == all_jobs[count]["name"]:
                                all_jobs[count]["kmodel_available"] = True
                    os.chdir(CURRENT_DIR)

                    count += 1
                
                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True
                response_json_final["JobList"] = all_jobs

            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
        except Exception as e:
            os.chdir(CURRENT_DIR)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return ReturnResponse(ResopnseOperationName, {
                "Error": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            })

    def status(self, name):
        ResopnseOperationName = "train_status"
        response_json_final = {
            "OutputLog": [],
            "ErrorMsg": None,
            "Success": None,
            "WeightsInfo": {
                "Available": False,
                "WeightsList": []
            }
        }
        CURRENT_DIR = Configuration["RootPath"]

        CheckPlatform("training")

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                if name in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration):
                    if "nohup.log" in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/"):
                        f = open(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/"+name+"/nohup.log")
                        TRAINING_STATUS_RESPONSE = {}
                        TRAINING_STATUS_RESPONSE["CurrentStatus"] = "InProgress"
                        TRAINING_STATUS_RESPONSE["Iterations"] = []
                        TRAINING_STATUS_RESPONSE["LatestEpochStatus"] = {}
                        nohup_read = f.readlines()
                        EPOCH_EXIST_STATE = False

                        for line in nohup_read:
                            if "avg loss" in line and  "rate" in line and  "seconds" in line and line.split(" ")[1][-1] == ":":
                                raw_line = str(line.strip("\n"))[1:len(str(line.strip("\n")))]
                                new = {   
                                    "RawLine": raw_line,
                                    "EpochTime": raw_line.split(" ")[0][0:-1],
                                    "OverallLoss": raw_line.split(" ")[1][0:-1],
                                    "AverageLoss": raw_line.split(" ")[2],
                                    "CurrentLearningRate": raw_line.split(" ")[5],
                                    "CurrentBatchTrainingTime": raw_line.split(" ")[7]
                                    # to do: add timestamp to here
                                }
                                TRAINING_STATUS_RESPONSE["Iterations"].append(new)
                                EPOCH_EXIST_STATE = True

                        if EPOCH_EXIST_STATE == True:
                            LATEST_EPOCH = TRAINING_STATUS_RESPONSE["Iterations"][len(TRAINING_STATUS_RESPONSE["Iterations"])-1]

                            LATEST = LATEST_EPOCH[str(list(LATEST_EPOCH.keys())[0])]
                            try:
                                # TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["EpochTimeStamp"] = str(int(time.time()))
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["EpochTime"] = LATEST.split(" ")[0][0:-1]
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["OverallLoss"] = LATEST.split(" ")[1][0:-1]
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["AverageLoss"] = LATEST.split(" ")[2]
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["CurrentLearningRate"] = LATEST.split(" ")[5]
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["CurrentBatchTrainingTime"] = LATEST.split(" ")[7]
                            except:
                                # TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["EpochTimeStamp"] = "Unavailable"
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["EpochTime"] = "Unavailable"
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["OverallLoss"] = "Unavailable"
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["AverageLoss"] = "Unavailable"
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["CurrentLearningRate"] = "Unavailable"
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["CurrentBatchTrainingTime"] = "Unavailable"

                        elif EPOCH_EXIST_STATE == False:
                            TRAINING_STATUS_RESPONSE["CurrentStatus"] = "InProgress"
                            response_json_final["ErrorMsg"] = "Training in progress, no epoch info available yet."
                        
                        f.close()

                    elif "nohup.log" not in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name):
                        os.chdir(CURRENT_DIR)
                        TRAINING_STATUS_RESPONSE = {}
                        TRAINING_STATUS_RESPONSE["CurrentStatus"] = "Unavailable"
                        response_json_final.update(TRAINING_STATUS_RESPONSE)
                        response_json_final["ErrorMsg"] = "No such training process, please start a training progress first."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                    response_json_final.update(TRAINING_STATUS_RESPONSE)

                    os.chdir(CURRENT_DIR)
                    if name in os.listdir(Configuration["ConfigurationPath"] + "/" + Models):
                        if len(os.listdir(Configuration["ConfigurationPath"] + "/" + Models + "/" + name)) > 0:
                            response_json_final["WeightsInfo"]["Available"] = True
                        for file in os.listdir(Configuration["ConfigurationPath"] + "/" + Models + "/" + name):
                            if "weights" in file:
                                response_json_final["WeightsInfo"]["WeightsList"].append({
                                    "Iteration" : str(file.split(".weights")[0].split(name)[-1].strip("_")),
                                    "ModelName": str(file)
                                })

                    elif name not in os.listdir(Configuration["ConfigurationPath"] + "/" + Models):
                        response_json_final["WeightsInfo"]["Available"] = False
                elif name not in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration):
                    os.chdir(CURRENT_DIR)
                    response_json_final["ErrorMsg"] = "Project does not exists or is not prepared yet."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            elif platform.system() == "Windows":
                if name in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration):
                    if "nohup.log" in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\"):
                        f = open(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\"+name+"\\nohup.log")
                        TRAINING_STATUS_RESPONSE = {}
                        TRAINING_STATUS_RESPONSE["CurrentStatus"] = "InProgress"
                        TRAINING_STATUS_RESPONSE["Iterations"] = []
                        TRAINING_STATUS_RESPONSE["LatestEpochStatus"] = {}
                        nohup_read = f.readlines()
                        EPOCH_EXIST_STATE = False

                        for line in nohup_read:
                            if "avg loss" in line and  "rate" in line and  "seconds" in line and line.split(" ")[1][-1] == ":":
                                raw_line = str(line.strip("\n"))[1:len(str(line.strip("\n")))]
                                new = {   
                                    "RawLine": raw_line,
                                    "EpochTime": raw_line.split(" ")[0][0:-1],
                                    "OverallLoss": raw_line.split(" ")[1][0:-1],
                                    "AverageLoss": raw_line.split(" ")[2],
                                    "CurrentLearningRate": raw_line.split(" ")[5],
                                    "CurrentBatchTrainingTime": raw_line.split(" ")[7]
                                    # to do: add timestamp to here
                                }
                                TRAINING_STATUS_RESPONSE["Iterations"].append(new)
                                EPOCH_EXIST_STATE = True

                        if EPOCH_EXIST_STATE == True:
                            LATEST_EPOCH = TRAINING_STATUS_RESPONSE["Iterations"][len(TRAINING_STATUS_RESPONSE["Iterations"])-1]

                            LATEST = LATEST_EPOCH[str(list(LATEST_EPOCH.keys())[0])]
                            try:
                                # TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["EpochTimeStamp"] = str(int(time.time()))
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["EpochTime"] = LATEST.split(" ")[0][0:-1]
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["OverallLoss"] = LATEST.split(" ")[1][0:-1]
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["AverageLoss"] = LATEST.split(" ")[2]
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["CurrentLearningRate"] = LATEST.split(" ")[5]
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["CurrentBatchTrainingTime"] = LATEST.split(" ")[7]
                            except:
                                # TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["EpochTimeStamp"] = "Unavailable"
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["EpochTime"] = "Unavailable"
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["OverallLoss"] = "Unavailable"
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["AverageLoss"] = "Unavailable"
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["CurrentLearningRate"] = "Unavailable"
                                TRAINING_STATUS_RESPONSE["LatestEpochStatus"]["CurrentBatchTrainingTime"] = "Unavailable"

                        elif EPOCH_EXIST_STATE == False:
                            TRAINING_STATUS_RESPONSE["CurrentStatus"] = "InProgress"
                            response_json_final["ErrorMsg"] = "Training in progress, no epoch info available yet."
                        
                        f.close()

                    elif "nohup.log" not in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name):
                        os.chdir(CURRENT_DIR)
                        TRAINING_STATUS_RESPONSE = {}
                        TRAINING_STATUS_RESPONSE["CurrentStatus"] = "Unavailable"
                        response_json_final.update(TRAINING_STATUS_RESPONSE)
                        response_json_final["ErrorMsg"] = "No such training process, please start a training progress first."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                    response_json_final.update(TRAINING_STATUS_RESPONSE)

                    os.chdir(CURRENT_DIR)
                    if name in os.listdir(Configuration["ConfigurationPath"] + "\\" + Models):
                        if len(os.listdir(Configuration["ConfigurationPath"] + "\\" + Models + "\\" + name)) > 0:
                            response_json_final["WeightsInfo"]["Available"] = True
                        for file in os.listdir(Configuration["ConfigurationPath"] + "\\" + Models + "\\" + name):
                            if "weights" in file:
                                response_json_final["WeightsInfo"]["WeightsList"].append({
                                    "Iteration" : str(file.split(".weights")[0].split(name)[-1].strip("_")),
                                    "ModelName": str(file)
                                })

                    elif name not in os.listdir(Configuration["ConfigurationPath"] + "\\" + Models):
                        response_json_final["WeightsInfo"]["Available"] = False
                elif name not in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration):
                    os.chdir(CURRENT_DIR)
                    response_json_final["ErrorMsg"] = "Project does not exists or is not prepared yet."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
        except Exception as e:
            os.chdir(CURRENT_DIR)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return ReturnResponse(ResopnseOperationName, {
                "Error": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            })

    def stop(self, name):
        ResopnseOperationName = "train_stop"
        response_json_final = {
            "OutputLog": [],
            "ErrorMsg": None,
            "Success": None
        }
        CURRENT_DIR = Configuration["RootPath"]

        CheckPlatform("training")

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                if name in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration):
                    CURRENT_DIR = Configuration["RootPath"]
                    if "save_pid.txt" in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name):
                        f = open(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/save_pid.txt")
                        PID = f.readlines()[0].strip("\n")
                        response_json_final["OutputLog"].append("Stopping training process with PID: " + str(PID))
                        f.close()

                        f = open(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/"+ name + "/training_analytics.json", "w")
                        LABELING_DATA_JSON = self.status(name = name)
                        f.writelines(json.dumps(LABELING_DATA_JSON))
                        f.close()

                        os.system("kill -9 " + PID)
                        os.system("rm "+Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/"+name+"/save_pid.txt")
                    elif "save_pid.txt" not in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name):
                        response_json_final["ErrorMsg"] = "No such training process, please start a training progress first."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                elif name not in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration):
                    os.chdir(CURRENT_DIR)
                    response_json_final["ErrorMsg"] = "Project does not exists or is not prepared yet."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                
                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            elif platform.system() == "Windows":
                if name in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration):
                    CURRENT_DIR = Configuration["RootPath"]
                    if "save_pid.txt" in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name):
                        f = open(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\save_pid.txt")
                        PID = f.readlines()[0].strip("\n")
                        response_json_final["OutputLog"].append("Stopping training process with PID: " + str(PID))
                        f.close()

                        f = open(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\"+ name + "\\training_analytics.json", "w")
                        LABELING_DATA_JSON = self.status(name = name)
                        f.writelines(json.dumps(LABELING_DATA_JSON))
                        f.close()

                        os.system("kill -9 " + PID)
                        os.system("rm "+Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\"+name+"\\save_pid.txt")
                    elif "save_pid.txt" not in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name):
                        response_json_final["ErrorMsg"] = "No such training process, please start a training progress first."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                elif name not in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration):
                    os.chdir(CURRENT_DIR)
                    response_json_final["ErrorMsg"] = "Project does not exists or is not prepared yet."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                
                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
        except Exception as e:
            os.chdir(CURRENT_DIR)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return ReturnResponse(ResopnseOperationName, {
                "Error": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            })

    def test(self, name, model_name="", image_path=""):
        ResopnseOperationName = "train_test"
        response_json_final = {
            "OutputLog": [],
            "ErrorMsg": None,
            "Success": None,
            "TestResult": {
                "TestOutput": None,
                "TestOutputRawLog": [],
                "PredictedImage": ""
            }
        }
        CURRENT_DIR = Configuration["RootPath"]

        CheckPlatform("training")

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                if name in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration):
                    if model_name == "":
                        pass
                        # no specify model
                    elif model_name != "":
                        if model_name not in os.listdir(Configuration["ConfigurationPath"] + "/" + Models + "/" + name):
                            os.chdir(CURRENT_DIR)
                            response_json_final["ErrorMsg"] = "Cannot find this model."
                            response_json_final["Success"] = False
                            response_json_final["TestResult"] = {}
                            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                        elif model_name in os.listdir(Configuration["ConfigurationPath"] + "/" + Models + "/" + name):
                            model_name = Configuration["ConfigurationPath"] + "/" + Models + "/" + name + "/" + model_name

                    if image_path == "":
                        pass
                        # no specify model
                    elif image_path != "":
                        if os.path.exists(image_path) == False:
                            os.chdir(CURRENT_DIR)
                            response_json_final["ErrorMsg"] = "Cannot find this image."
                            response_json_final["Success"] = False
                            response_json_final["TestResult"] = {}
                            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                    if "test-train.sh" in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/"+name+"/"):
                        response_json_final["OutputLog"].append("Testing model...")
                        if model_name == "" and image_path == "":
                            os.system("bash " + Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/"+name+"/test-train.sh")
                        elif model_name == "" and image_path != "":
                            os.system("bash " + Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/"+name+"/test-train.sh -f " + image_path)
                        elif model_name != "" and image_path == "":
                            os.system("bash " + Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/"+name+"/test-train.sh -m " + model_name)
                        elif model_name != "" and image_path != "":
                            os.system("bash " + Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/"+name+"/test-train.sh -f " + image_path + " -m " + model_name)

                        f = open(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/"+name+"/"+ name +"_test_result.log", "r")
                        read_prediction_log = f.readlines()
                        for i in range(0,len(read_prediction_log)):
                            read_prediction_log[i] = read_prediction_log[i].strip("\n")
                        count, new_count = 0, 0
                        for line in read_prediction_log:
                            if "Predicted" in line and "milli-seconds." in line:
                                new_count = count 
                                response_json_final["TestResult"]["TestOutput"] = read_prediction_log[new_count+1:len(read_prediction_log)]
                            count +=1
                        f.close()

                        # export prediction image as base64
                        with open(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/" + name + "predictions.jpg", "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read())
                            response_json_final["TestResult"]["PredictedImage"] = encoded_string.decode()

                    elif "test-train.sh" not in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name +"/"):
                        os.chdir(CURRENT_DIR)
                        response_json_final["ErrorMsg"] = "No test script available."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                    response_json_final["OutputLog"].append("Done Testing model")
                elif name not in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration):
                    os.chdir(CURRENT_DIR)
                    response_json_final["ErrorMsg"] = "Project does not exists or is not prepared yet."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            elif platform.system() == "Windows":
                if name in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration):
                    if model_name == "":
                        pass
                        # no specify model
                    elif model_name != "":
                        if model_name not in os.listdir(Configuration["ConfigurationPath"] + "\\" + Models + "\\" + name):
                            os.chdir(CURRENT_DIR)
                            response_json_final["ErrorMsg"] = "Cannot find this model."
                            response_json_final["Success"] = False
                            response_json_final["TestResult"] = {}
                            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                        elif model_name in os.listdir(Configuration["ConfigurationPath"] + "\\" + Models + "\\" + name):
                            model_name = Configuration["ConfigurationPath"] + "\\" + Models + "\\" + name + "\\" + model_name

                    if image_path == "":
                        pass
                        # no specify model
                    elif image_path != "":
                        if os.path.exists(image_path) == False:
                            os.chdir(CURRENT_DIR)
                            response_json_final["ErrorMsg"] = "Cannot find this image."
                            response_json_final["Success"] = False
                            response_json_final["TestResult"] = {}
                            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                    if "test-train.sh" in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\"+name+"\\"):
                        response_json_final["OutputLog"].append("Testing model...")
                        if model_name == "" and image_path == "":
                            os.system("bash " + Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\"+name+"\\test-train.sh")
                        elif model_name == "" and image_path != "":
                            os.system("bash " + Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\"+name+"\\test-train.sh -f " + image_path)
                        elif model_name != "" and image_path == "":
                            os.system("bash " + Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\"+name+"\\test-train.sh -m " + model_name)
                        elif model_name != "" and image_path != "":
                            os.system("bash " + Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\"+name+"\\test-train.sh -f " + image_path + " -m " + model_name)

                        f = open(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\"+name+"\\"+ name +"_test_result.log", "r")
                        read_prediction_log = f.readlines()
                        for i in range(0,len(read_prediction_log)):
                            read_prediction_log[i] = read_prediction_log[i].strip("\n")
                        count, new_count = 0, 0
                        for line in read_prediction_log:
                            if "Predicted" in line and "milli-seconds." in line:
                                new_count = count 
                                response_json_final["TestResult"]["TestOutput"] = read_prediction_log[new_count+1:len(read_prediction_log)]
                            count +=1
                        f.close()

                        # export prediction image as base64
                        with open(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\" + name + "predictions.jpg", "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read())
                            response_json_final["TestResult"]["PredictedImage"] = encoded_string.decode()

                    elif "test-train.sh" not in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name +"\\"):
                        os.chdir(CURRENT_DIR)
                        response_json_final["ErrorMsg"] = "No test script available."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                    response_json_final["OutputLog"].append("Done Testing model")
                elif name not in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration):
                    os.chdir(CURRENT_DIR)
                    response_json_final["ErrorMsg"] = "Project does not exists or is not prepared yet."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
        except Exception as e:
            os.chdir(CURRENT_DIR)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return ReturnResponse(ResopnseOperationName, {
                "Error": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            })

    def get_statistics(self, name):
        ResopnseOperationName = "get_statistics"
        response_json_final = {
            "OutputLog": [],
            "ErrorMsg": None,
            "Success": None,
            "ModelInfo": {
                "Weights": {
                    "Available": False,
                    "WeightsList": []
                },
                "Kmodel": {
                    "Available": False,
                    "KmodelList": []
                },
                "Analytics": {
                    "Available": False,
                    "Info": []
                }
            }
        }
        CURRENT_DIR = Configuration["RootPath"]

        CheckPlatform("training")

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                if name in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration):
                    
                    # print("Getting weights info")
                    if name in os.listdir(Configuration["ConfigurationPath"] + "/" + Models):
                        response_json_final["ModelInfo"]["Weights"]["Available"] = True
                        for file in os.listdir(Configuration["ConfigurationPath"] + "/" + Models + "/" + name):
                            if "weights" in file:
                                response_json_final["ModelInfo"]["Weights"]["WeightsList"].append({
                                    "Iteration" : str(file.split(".weights")[0].split(name)[-1].strip("_")),
                                    "ModelName": str(file)
                                })
                    elif name in os.listdir(Configuration["ConfigurationPath"] + "/" + Models):
                        response_json_final["ModelInfo"]["Weights"]["Available"] = True
                        response_json_final["ModelInfo"]["Weights"]["WeightsList"] = []

                    # print("Getting kmodel info")
                    if name in os.listdir(Configuration["ConfigurationPath"] + "/" + Conversion):
                        response_json_final["ModelInfo"]["Kmodel"]["Available"] = True
                        for file in os.listdir(Configuration["ConfigurationPath"] + "/" + Conversion + "/" + name):
                            if "kmodel" in file:
                                response_json_final["ModelInfo"]["Kmodel"]["KmodelList"].append({
                                    str(file.split(".kmodel")[0].split(name)[-1].strip("_")): str(file)
                                })
                    elif name not in os.listdir(Configuration["ConfigurationPath"] + "/" + Conversion):
                        response_json_final["ModelInfo"]["Kmodel"]["Available"] = False
                        response_json_final["ModelInfo"]["Kmodel"]["KmodelList"] = []
                        
                    # print("Getting analytics info")
                    if "training_analytics.json" in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name):
                        response_json_final["ModelInfo"]["Analytics"]["Available"] = True
                        with open(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/training_analytics.json", "r") as json_file:
                            data = json.load(json_file)
                            response_json_final["ModelInfo"]["Analytics"]["Info"] = data["Response"]["Iterations"]
                    elif "training_analytics.json" not in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name):
                        response_json_final["ModelInfo"]["Analytics"]["Available"] = False
                        response_json_final["ModelInfo"]["Analytics"]["Info"] = []

                elif name not in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration):
                    os.chdir(CURRENT_DIR)
                    response_json_final["ErrorMsg"] = "Project does not exists or is not prepared yet."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            elif platform.system() == "Windows":
                if name in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration):
                    
                    # print("Getting weights info")
                    if name in os.listdir(Configuration["ConfigurationPath"] + "\\" + Models):
                        response_json_final["ModelInfo"]["Weights"]["Available"] = True
                        for file in os.listdir(Configuration["ConfigurationPath"] + "\\" + Models + "\\" + name):
                            if "weights" in file:
                                response_json_final["ModelInfo"]["Weights"]["WeightsList"].append({
                                    "Iteration" : str(file.split(".weights")[0].split(name)[-1].strip("_")),
                                    "ModelName": str(file)
                                })

                    # print("Getting kmodel info")
                    if name in os.listdir(Configuration["ConfigurationPath"] + "\\" + Conversion):
                        response_json_final["ModelInfo"]["Kmodel"]["Available"] = True
                        for file in os.listdir(Configuration["ConfigurationPath"] + "\\" + Conversion + "\\" + name):
                            if "kmodel" in file:
                                response_json_final["ModelInfo"]["Kmodel"]["KmodelList"].append({
                                    str(file.split(".kmodel")[0].split(name)[-1].strip("_")): str(file)
                                })
                        
                    # print("Getting analytics info")
                    if "training_analytics.json" in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name):
                        response_json_final["ModelInfo"]["Analytics"]["Available"] = True
                        with open(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\training_analytics.json", "r") as json_file:
                            data = json.load(json_file)
                            response_json_final["ModelInfo"]["Analytics"]["Info"] = data["Response"]["Iterations"]
                    elif "training_analytics.json" not in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name):
                        os.chdir(CURRENT_DIR)
                        response_json_final["ErrorMsg"] = "Unable to find the analytics data, please stop your training job first."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                elif name not in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration):
                    os.chdir(CURRENT_DIR)
                    response_json_final["ErrorMsg"] = "Project does not exists or is not prepared yet."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
        except Exception as e:
            os.chdir(CURRENT_DIR)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return ReturnResponse(ResopnseOperationName, {
                "Error": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            })

    def send_file_to_export_remote(self, name, file_path, url):
        if os.path.exists(file_path) == False:
            return {'FunctionResponse': {'Error': 'File not exists.'}}
        elif os.path.exists(file_path) == True:
            try:
                response = requests.post(
                    url, 
                    files = {'file': open(file_path, "rb")}, 
                    data = {'name': name},
                    timeout = 30
                )
                return response.json()
            except BaseException as e:
                return {'FunctionResponse': {'Error': str(e)}}

    def export_kmodel(self, name, model_name):
        ResopnseOperationName = "export_kmodel"
        response_json_final = {
            "OutputLog": [],
            "ErrorMsg": None,
            "Success": None
            # "DownloadLink": None
        }
        CURRENT_DIR = Configuration["RootPath"]
        KMODEL_EXPORT_API = "http://3.1.106.140:8020"

        try:
            '''
            ██      ██ ███    ██ ██    ██ ██   ██ 
            ██      ██ ████   ██ ██    ██  ██ ██  
            ██      ██ ██ ██  ██ ██    ██   ███   
            ██      ██ ██  ██ ██ ██    ██  ██ ██  
            ███████ ██ ██   ████  ██████  ██   ██ 
                                                  
            '''
            if platform.system() == "Linux":
                if name in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration):

                    if os.path.exists(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/" + name + ".cfg"):
                        while True:
                            print("Collecting .cfg file...")
                            response = self.send_file_to_export_remote(
                                name, 
                                Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/" + name + ".cfg", 
                                KMODEL_EXPORT_API + "/upload"
                            )
                            if "Message" in response["FunctionResponse"].keys():
                                if response["FunctionResponse"]["Message"] == "OK": break
                            elif "Error" in response["FunctionResponse"].keys():
                                print("Upload faild for following reaons: " + response["FunctionResponse"]["Error"] + ", retry now.")
                                time.sleep(2)
                    else:
                        os.chdir(CURRENT_DIR)
                        response_json_final["ErrorMsg"] = "Project have no cfg file."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                    if os.path.exists(Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/" + name + ".names"):
                        while True:
                            print("Collecting .names file...")
                            response = self.send_file_to_export_remote(
                                name, 
                                Configuration["ConfigurationPath"] + "/" + ModelConfiguration + "/" + name + "/" + name + ".names", 
                                KMODEL_EXPORT_API + "/upload"
                            )
                            if "Message" in response["FunctionResponse"].keys():
                                if response["FunctionResponse"]["Message"] == "OK": break
                            elif "Error" in response["FunctionResponse"].keys():
                                print("Upload faild for following reaons: " + response["FunctionResponse"]["Error"] + ", retry now.")
                                time.sleep(2)
                    else:
                        os.chdir(CURRENT_DIR)
                        response_json_final["ErrorMsg"] = "Project have no names file."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                    if os.path.exists(Configuration["ConfigurationPath"] + "/" + Models + "/" + name + "/" + model_name):
                        while True:
                            shutil.copy(
                                Configuration["ConfigurationPath"] + "/" + Models + "/" + name + "/" + model_name,
                                Configuration["ConfigurationPath"] + "/" + Models + "/" + name + "/" + name + ".weights"
                            )
                            print("Collecting .weights file...")
                            response = self.send_file_to_export_remote(
                                name, 
                                Configuration["ConfigurationPath"] + "/" + Models + "/" + name + "/" + name + ".weights", 
                                KMODEL_EXPORT_API + "/upload"
                            )
                            os.remove(Configuration["ConfigurationPath"] + "/" + Models + "/" + name + "/" + name + ".weights")
                            if "Message" in response["FunctionResponse"].keys():
                                if response["FunctionResponse"]["Message"] == "OK": break
                            elif "Error" in response["FunctionResponse"].keys():
                                print("Upload faild for following reaons: " + response["FunctionResponse"]["Error"] + ", retry now.")
                                time.sleep(2)
                    else:
                        os.chdir(CURRENT_DIR)
                        response_json_final["ErrorMsg"] = "Model file not found."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                    print("Collecting testing images...")
                    os.chdir(Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/" + name)

                    image_list = []
                    for file in os.listdir():
                        if ".jpg" in file:
                            image_list.append(file)
                    for i in range(0, 10):
                        print("- Using image: " + image_list[random.randint(0, len(image_list)-1)])
                        self.send_file_to_export_remote(
                            name, 
                            Configuration["ConfigurationPath"] + "/" + ProcessedDataset + "/" + name + "/" + image_list[random.randint(0, len(image_list)-1)],
                            KMODEL_EXPORT_API + "/upload"
                        )

                    print("Requesting kmodel export service... (this may take a minute)")
                    kmodel_export_response = requests.post(
                        KMODEL_EXPORT_API + "/export_kmodel", 
                        json={"name": name},
                        headers={"Content-Type": "application/json"},
                        timeout = 120
                    )
                    # print(kmodel_export_response.json())

                    if "Error" in kmodel_export_response.json()["FunctionResponse"]:
                        os.chdir(CURRENT_DIR)
                        response_json_final["ErrorMsg"] = { 
                            "Message": "Kmodel download error",
                            "Reason": kmodel_export_response.json()
                        }
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                    elif "KmodelDownloadLink" in kmodel_export_response.json()["FunctionResponse"]["Response"]:
                        print("Downloading kmodel...")#  + kmodel_export_response.json()["FunctionResponse"]["Response"]["KmodelDownloadLink"])

                        try:
                            file_name = Configuration["ConfigurationPath"] + "/" + Conversion + "/" + name + "/" + name + "_" + model_name.split(".weights")[-2].split("_")[-1] + ".kmodel"
                            with open(file_name, "wb") as f:
                                response = requests.get(
                                    kmodel_export_response.json()["FunctionResponse"]["Response"]["KmodelDownloadLink"], 
                                    stream = True, timeout = 120
                                )
                                total_length = response.headers.get('content-length')

                                if total_length is None:
                                    f.write(response.content)
                                else:
                                    dl = 0
                                    total_length = int(total_length)
                                    for data in response.iter_content(chunk_size = 4096):
                                        dl += len(data)
                                        f.write(data)
                                        done = int(50 * dl / total_length)
                                        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                                        sys.stdout.flush()
                            print(" Saved.")
                        except BaseException as e:
                            print("Failed: " + str(e))

                elif name not in os.listdir(Configuration["ConfigurationPath"] + "/" + ModelConfiguration):
                    os.chdir(CURRENT_DIR)
                    response_json_final["ErrorMsg"] = "Project does not exists or is not prepared yet."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            elif platform.system() == "Windows":
                if name in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration):

                    if os.path.exists(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\" + name + ".cfg"):
                        while True:
                            print("Collecting .cfg file...")
                            response = self.send_file_to_export_remote(
                                name, 
                                Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\" + name + ".cfg", 
                                KMODEL_EXPORT_API + "/upload"
                            )
                            if "Message" in response["FunctionResponse"].keys():
                                if response["FunctionResponse"]["Message"] == "OK": break
                            elif "Error" in response["FunctionResponse"].keys():
                                print("Upload faild for following reaons: " + response["FunctionResponse"]["Error"] + ", retry now.")
                                time.sleep(2)
                    else:
                        os.chdir(CURRENT_DIR)
                        response_json_final["ErrorMsg"] = "Project have no cfg file."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                    if os.path.exists(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\" + name + ".names"):
                        while True:
                            print("Collecting .names file...")
                            response = self.send_file_to_export_remote(
                                name, 
                                Configuration["ConfigurationPath"] + "\\" + ModelConfiguration + "\\" + name + "\\" + name + ".names", 
                                KMODEL_EXPORT_API + "/upload"
                            )
                            if "Message" in response["FunctionResponse"].keys():
                                if response["FunctionResponse"]["Message"] == "OK": break
                            elif "Error" in response["FunctionResponse"].keys():
                                print("Upload faild for following reaons: " + response["FunctionResponse"]["Error"] + ", retry now.")
                                time.sleep(2)
                    else:
                        os.chdir(CURRENT_DIR)
                        response_json_final["ErrorMsg"] = "Project have no names file."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                    if os.path.exists(Configuration["ConfigurationPath"] + "\\" + Models + "\\" + name + "\\" + model_name):
                        while True:
                            shutil.copy(
                                Configuration["ConfigurationPath"] + "\\" + Models + "\\" + name + "\\" + model_name,
                                Configuration["ConfigurationPath"] + "\\" + Models + "\\" + name + "\\" + name + ".weights"
                            )
                            print("Collecting .weights file...")
                            response = self.send_file_to_export_remote(
                                name, 
                                Configuration["ConfigurationPath"] + "\\" + Models + "\\" + name + "\\" + name + ".weights", 
                                KMODEL_EXPORT_API + "/upload"
                            )
                            os.remove(Configuration["ConfigurationPath"] + "\\" + Models + "\\" + name + "\\" + name + ".weights")
                            if "Message" in response["FunctionResponse"].keys():
                                if response["FunctionResponse"]["Message"] == "OK": break
                            elif "Error" in response["FunctionResponse"].keys():
                                print("Upload faild for following reaons: " + response["FunctionResponse"]["Error"] + ", retry now.")
                                time.sleep(2)
                    else:
                        os.chdir(CURRENT_DIR)
                        response_json_final["ErrorMsg"] = "Model file not found."
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                    print("Collecting testing images...")
                    os.chdir(Configuration["ConfigurationPath"] + "\\" + ProcessedDataset + "\\" + name)

                    image_list = []
                    for file in os.listdir():
                        if ".jpg" in file:
                            image_list.append(file)
                    for i in range(0, 10):
                        print("- Using image: " + image_list[random.randint(0, len(image_list)-1)])
                        self.send_file_to_export_remote(
                            name, 
                            Configuration["ConfigurationPath"] + "\\" + ProcessedDataset + "\\" + name + "\\" + image_list[random.randint(0, len(image_list)-1)],
                            KMODEL_EXPORT_API + "/upload"
                        )

                    print("Requesting kmodel export service... (this may take a minute)")
                    kmodel_export_response = requests.post(
                        KMODEL_EXPORT_API + "/export_kmodel", 
                        json={"name": name},
                        headers={"Content-Type": "application/json"},
                        timeout = 120
                    )
                    # print(kmodel_export_response.json())

                    if "Error" in kmodel_export_response.json()["FunctionResponse"]:
                        os.chdir(CURRENT_DIR)
                        response_json_final["ErrorMsg"] = { 
                            "Message": "Kmodel download error",
                            "Reason": kmodel_export_response.json()
                        }
                        response_json_final["Success"] = False
                        return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
                    elif "KmodelDownloadLink" in kmodel_export_response.json()["FunctionResponse"]["Response"]:
                        print("Downloading kmodel...")#  + kmodel_export_response.json()["FunctionResponse"]["Response"]["KmodelDownloadLink"])

                        try:
                            file_name = Configuration["ConfigurationPath"] + "\\" + Conversion + "\\" + name + "\\" + name + "_" + model_name.split(".weights")[-2].split("_")[-1] + ".kmodel"
                            with open(file_name, "wb") as f:
                                response = requests.get(
                                    kmodel_export_response.json()["FunctionResponse"]["Response"]["KmodelDownloadLink"], 
                                    stream = True, timeout = 120
                                )
                                total_length = response.headers.get('content-length')

                                if total_length is None:
                                    f.write(response.content)
                                else:
                                    dl = 0
                                    total_length = int(total_length)
                                    for data in response.iter_content(chunk_size = 4096):
                                        dl += len(data)
                                        f.write(data)
                                        done = int(50 * dl / total_length)
                                        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                                        sys.stdout.flush()
                            print(" Saved.")
                        except BaseException as e:
                            print("Failed: " + str(e))

                elif name not in os.listdir(Configuration["ConfigurationPath"] + "\\" + ModelConfiguration):
                    os.chdir(CURRENT_DIR)
                    response_json_final["ErrorMsg"] = "Project does not exists or is not prepared yet."
                    response_json_final["Success"] = False
                    return ReturnResponse(ResopnseOperationName, response_json_final, remark="")

                os.chdir(CURRENT_DIR)

                response_json_final["Success"] = True

            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
        except Exception as e:
            os.chdir(CURRENT_DIR)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return ReturnResponse(ResopnseOperationName, {
                "Error": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            })

    '''
    def check_kmodel_existence(self, name):
        ResopnseOperationName = "check_kmodel_existence"
        response_json_final = {"OutputLog": None}

        # must be jpg format 
        try:
            CURRENT_DIR = Configuration["RootPath"]

            if name+".kmodel" in os.listdir(Configuration["ConfigurationPath"] + "/convert"):
                response_json_final["Existence"] = "Yes"
            elif name+".kmodel" not in os.listdir(Configuration["ConfigurationPath"] + "/convert"):
                response_json_final["Existence"] = "No"

            os.chdir(CURRENT_DIR)
            return ReturnResponse(ResopnseOperationName, response_json_final, remark="")
        except Exception as e:
            os.chdir(CURRENT_DIR)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return ReturnResponse(ResopnseOperationName, {
                "Error": {
                    "exc_type": str(exc_type), 
                    "fname": str(fname), 
                    "tb_lineno": str(exc_tb.tb_lineno), 
                    "msg": str(e)
                }
            })

    '''
