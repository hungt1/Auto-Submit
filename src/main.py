import sys, os, json
import status, submit, parse
from sys import exit

if __name__ == '__main__':
    arg = sys.argv
    if len(arg) == 3 and arg[1] == 'parse':
        parse.run(arg[2])
        exit(0)

    try:
        f = open('CFconfig.json')
        config = json.load(f)
        f.close()
        f = open('/mnt/d/Learning/Competitive Programming/Online Judge/Codeforces/setting.json')
        info = json.load(f)
        f.close()
    except:
        print('Config file not found !!!')
        exit(1)

    if len(arg) == 2:
        if arg[1] == 'status':
            status.run(config['Contest ID'])    
    elif len(arg) == 3:
        if arg[1] == 'submit':
            cur =  info['Contest Folder'] + '/' + config['Contest name'] + '/' + arg[2] + '.cpp'  
            if not os.path.exists(cur):
                print(cur)
                print('Submit file not found')
                exit(1)
            submit.run(config['Contest ID'], arg[2], config['Contest name'])
