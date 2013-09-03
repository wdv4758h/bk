#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path, time, shutil
from os import makedirs, getcwd, chdir

class Backups:

    def checkdir(file_name):
        makedirs('backups - %s' % file_name,exist_ok=True)

    def BackupFile(file_name, stime):
        Backups.checkdir(file_name)

        pwd = getcwd()

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
            while(True):
                modify_time = os.path.getmtime('%s/%s' % (pwd, file_name))
                if modify_time != pre_modify_time:
                    try:
                        shutil.copy('%s/%s' % (pwd, file_name), '%s - %s' % (file_name, time.ctime(modify_time)))
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
    Backups.BackupFile(file_name, stime)
