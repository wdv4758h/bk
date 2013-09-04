#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import makedirs, getcwd, chdir
from multiprocessing import Process
import os.path, time, shutil
import re

class Backups:

    def __init__(self):
        self.processList = {}

    def checkdir(self, file_name):
        makedirs('backups - %s' % file_name,exist_ok=True)

    def BackupFile(self, file_path, stime):
        split = re.search(r'^(.*/)([^/]+)$', file_path)
        if split:
            file_dir = split.group(1)
            file_name = split.group(2)
        else:
            #for current directory's files
            file_dir = getcwd()
            file_name = file_path

        self.checkdir(file_name)

        #change directory to backup
        try:
            chdir('backups - %s' % file_name)
        except Exception:
            print('chdir error !')
            pass

        #get modify time
        try:
            pre_modify_time = open("%s.time" % file_name, "r").read()
        except IOError:
            pre_modify_time = ""
            print('file time not found, program will make a new one later')
            pass

        try:
            while True:
                modify_time = os.path.getmtime('%s/%s' % (file_dir, file_name))
                if modify_time != pre_modify_time:
                    try:
                        shutil.copy('%s/%s' % (file_dir, file_name), '%s - %s' % (file_name, time.ctime(modify_time)))
                    except Exception:
                        print('Copy file error !')
                        pass

                    try:
                        open("%s.time" % file_name, "w").write(str(modify_time))
                    except IOError:
                        print("Time write backup error !!!")
                        pass

                pre_modify_time = modify_time
                time.sleep(stime)   #secs
        except:
            print('exit program')
            pass

    def mBackup(self, file_path, stime):
        self.processList[file_path] = Process(target=self.BackupFile, args=(file_path, stime))
        self.processList[file_path].start()

    def mStop(self, file_path):
        if file_path in self.processList.keys():
            self.processList[file_path].terminate()
            self.processList[file_path].join()
            self.processList.pop(file_path)
            return 0
        else:
            print("process not found")
            return 1


if __name__ == "__main__":
    import sys
    length = len(sys.argv)
    if (length > 2) and sys.argv[2].isdecimal():
        file_name = sys.argv[1]
        stime = int(sys.argv[2])
    elif length == 2:
        file_name = sys.argv[1]
        stime = 20
    else:
        print("missing backup file")
        exit()
    bk = Backups()
    bk.BackupFile(file_name, stime)
