import subprocess
import os
import sys
import logging
from sys import stdout
import os.path

class PhFile:

    def readFile(self, file_path):
        try:
            os.popen("cat " + file_path).read().rstrip()
        except Exception as e:
            logging.error("Error read file: %s", e)

    def createFolder(self, folder_path):
        try:
            os.popen("mkdir -p " + folder_path)
        except Exception as e:
            logging.error("Error create folder: %s", e);

    def saveText(self, file_path, text):
        try:
            if not os.path.exists(file_path):
                os.popen("touch " + file_path)

            os.popen("printf \"" + text + "\" > " + file_path)
        except Exception as e:
            logging.error("Error save text %s", e)

    def appendText(self, file_path, text):
        try:
            if not os.path.exists(file_path):
                os.popen("touch " + file_path)

            os.popen("printf \"" + text + "\" >> " + file_path)
        except Exception as e:
            logging.error("Error append text %s", e)

    def rename(self, path, new_path):
        try:
            if os.path.exists(path):
                os.popen("mv " + path + " " + new_path)
        except Exception as e:
            logging.error("Rename error %s", e)

    def delete(self, path):
        try:
            if os.path.exists(path):
                os.popen("rm  -rf " + path )
        except Exception as e:
            logging.error("Rename error %s", e)

    def move(self,path, new_path):
        try:
            if os.path.exists(path):
                os.popen("mv " + path + " " + new_path)
        except Exception as e:
            logging.error("Rename error %s", e)


    def copy(self,path, new_path):
        try:
            if os.path.exists(path):
                os.popen("cp -r " + path + " " + new_path)
        except Exception as e:
            logging.error("Rename error %s", e)






