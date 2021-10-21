import requests, json
import os

def get_contest_name(page):
    pos = page.find('content="Dashboard - ')
    pos += len('content="Dashboard - ')
    ans = page[pos:page.find(' - Codeforces', pos)]
    return ans

def get_problems_list(page):
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
    page = requests.get(url).text

    contest_name = get_contest_name(page)
    problems_list = get_problems_list(page)
    
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

    data = json.dumps(data, indent = 4)
    with open(contest_dir + '/' + 'CFconfig.json', 'w') as outfile:
        outfile.write(data)

    os.chdir(contest_dir)
    os.system('code .')