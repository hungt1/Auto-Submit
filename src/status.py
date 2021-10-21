import json, requests

def get_status(id_contest):
    ans = '{:<15} {:<20} {:<30} {:<20}\n'.format('Usernane', 'Lang', 'Problem', 'Verdict')
    url = 'https://codeforces.com/api/contest.status?contestId=' + str(id_contest) + '&handle=hungt1&from=1&count=100'
    data = json.loads(requests.post(url).text)
    status_list = data['result']
    for status in status_list:
        user = 'hungt1'
        lang = status['programmingLanguage']
        problem = status['problem']['index'] + '-' + status['problem']['name']
        ver = status['verdict']
        ans += '{:<15} {:<20} {:<30} {:<20}\n'.format(user, lang, problem, ver)
    return ans

def run(id_contest):
    print(get_status(id_contest))