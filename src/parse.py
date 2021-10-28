import requests, json
import os

def get_contest_name(url):
    while True: 
        page = requests.get(url).text
        pos = page.find('content="Dashboard - ')
        if pos == -1:
            print('Please wait until the contest starts ...', end = '\r')
        else:
            break
        
    pos += len('content="Dashboard - ')
    ans = page[pos:page.find(' - Codeforces', pos)]
    return ans

def get_problems_list(url):
    page = requests.get(url).text
    ans = []
    page = page[page.find('generalAnnouncement'):]
    while True:
        nxt = page.find('<option value="')
        if nxt != -1:
            l = len('<option value="')
            idx = page[(nxt + l):page.find('"', nxt + l)]
            nxt = page.find('name="', nxt) + 6
            end = page.find('"', nxt)
            name = page[nxt:end]
            page = page[end:]
            ans.append([idx, name])    
        else:
            break
    return ans

def run(id_contest):
    url = 'https://codeforces.com/contest/' + str(id_contest)

    contest_name = get_contest_name(url)
    
    problems_list = get_problems_list(url)

    if contest_name == '' or len(problems_list) == 0: 
        return

    f = open('/mnt/d/Learning/Competitive Programming/Online Judge/Codeforces/setting.json')
    info = json.load(f)
    f.close()

    contest_dir = info['Contest Folder'] + '/' + contest_name
    if not os.path.exists(contest_dir):
        os.mkdir(contest_dir)
    
    for problem in problems_list:
        cur = contest_dir + '/' + problem[0] + '.cpp'
        if not os.path.exists(cur):
            f = open(cur, 'a')
            f.close()

    data = dict()
    data['Contest ID'] = str(id_contest)
    data['Contest name'] = contest_name

    config = contest_dir + '/' + '__cfcache__'
    if not os.path.exists(config):
        os.mkdir(config)

    data = json.dumps(data, indent = 4)
    with open(config + '/' + 'config.json', 'w') as outfile:
        outfile.write(data)

    os.chdir(contest_dir)
    os.system('code .')