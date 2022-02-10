import requests
import sys
import os

page = 1

def main():
    if len(sys.argv) == 2:
        uname = sys.argv[1]
    else:
        return "Usage: drupal-in-green.py <username>"
    url = urlGen(uname, page)
    try:
        response = requests.get(url)
        data = response.json()
        if 'list' in data and data['list']:
            page_count = data['last'].split('=')[-1]
            created_time = []
            for i in range(int(page_count) + 1):
                created_time.extend(fetch(urlGen(uname, i)))
            if created_time != []:
                if os.path.exists('data.txt'):
                    os.remove('data.txt')
                os.system('git checkout --orphan latest_branch')
                os.system('git add .')
                os.system('git commit -am "Reset all commits"')
                os.system('git branch -D main')
                os.system('git branch -m main')
                os.system('git push origin main -f')
                created_time.sort()
                for dt in created_time:
                    sdt = "\n" + str(dt)
                    if fileChange(sdt):
                        os.system('git add .')
                        command = 'git commit --date "' + str(dt) + '" -am "Add an activity commit by ' + uname + '@drupal.org"'
                        os.system(command)
                os.system('git push origin main -f')
        else:
            return 'No Data'
    except:
        print("Error in fetching data")
        print("Please check if the API is working by visiting " + url)
        print("on your browser and also check see if the username is valid by checking if the list key empty or not")
        return sys.exc_info()[0]

def urlGen(uname, page):
    return "https://www.drupal.org/api-d7/comment.json?name=" + uname + "&page=" + str(page)

def fetch(url):
    try:
        response = requests.get(url)
        data = response.json()
        if 'list' in data and data['list']:
            created = []
            for item in data['list']:
                created.append(int(item['created']))
            return created
        else:
            return []
    except:
        return []

def fileChange(data):
    try:
        if not os.path.exists('data.txt'):
            with open('data.txt', 'w') as f:
                f.write('')
        with open('data.txt', 'a') as f:
            f.write(data)
            return True
    except:
        print(sys.exc_info()[0])
        return False

if __name__ == '__main__':
    main()