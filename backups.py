#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
file_name = sys.argv[1]
stime = int(sys.argv[2]) if ((len(sys.argv) > 2) and sys.argv[2].isdecimal()) else 20     #secs

def checkdir():
    from os import makedirs
    makedirs('backups - %s' % file_name,exist_ok=True)

def main():
    checkdir()

    from os import getcwd
    pwd = getcwd()

    #change directory to backup
    try:
        from os import chdir
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

    import os.path
    import time
    try:
        while(True):
            modify_time = os.path.getmtime('%s/%s' % (pwd, file_name))
            if modify_time != pre_modify_time:
                try:
                    import shutil
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
    main()
