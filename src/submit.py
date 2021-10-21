# https://stackoverflow.com/questions/58620609/how-to-retain-the-login-state-in-selenium

import json, requests
from selenium import webdriver
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning) 

def get_status(id_contest):
    url = 'https://codeforces.com/api/contest.status?contestId=' + str(id_contest) + '&handle=hungt1&from=1&count=1'
    data = json.loads(requests.post(url).text)
    status_list = data['result']
    is_testing = False
    ans = ''
    for status in status_list:
        user = 'hungt1'
        lang = status['programmingLanguage']
        problem = status['problem']['index'] + '-' + status['problem']['name']
        ver = status['verdict']
        if ver == 'TESTING':
            is_testing = True
        ans = '{:<15} {:<20} {:<40} {:<20}'.format(user, lang, problem, ver)
    if is_testing:
        print(ans, end = '\r')
    else:
        print(ans)
    return is_testing

def run(id_contest, name_problem, name_contest):
    f = open('/mnt/d/Learning/Competitive Programming/Online Judge/Codeforces/setting.json')
    info = json.load(f)

    options = webdriver.ChromeOptions()
    options.add_argument(info["Profile Path"])
    options.add_argument("--headless")

    driver = webdriver.Chrome(executable_path=info["Chrome driver"], options=options)

    url = 'https://codeforces.com/contest/' + str(id_contest) + '/problem/' + name_problem

    driver.get(url)

    cur_path = info["Contest Folder"] + '/' + name_contest + '/' + name_problem + '.cpp'
    driver.find_element_by_xpath("//input[@name='sourceFile']").send_keys(cur_path)
    driver.find_element_by_xpath("//input[@class='submit']").click()

    try:
        driver.find_element_by_xpath("//span[@class='error for__sourceFile']")
        print('You have submitted exactly the same code before')
        driver.close()
        return
    except:
        while True:
            testing = get_status(id_contest)
            if not testing:
                break
    
    driver.close()
    return
