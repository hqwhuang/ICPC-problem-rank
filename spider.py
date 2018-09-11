# -*- coding: utf-8 -*-
import re
import requests
#super parameter
username = ""
passwd = ""
k = 2013
com = 'https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=591' #Regioal k's url
tot = 80 # to adjust the width of output
with open('./Regional_%d.txt'%k, 'w') as csvfile:
    try:
        session = requests.Session()
        url = 'https://icpcarchive.ecs.baylor.edu/'
        tmp = session.get(url)

        with open('test.html', 'w') as f:
            f.write(tmp.content)

        # read from a local html file
        with open('test.html', 'r') as f:
            ss = f.read()

        special_key = re.findall('<input type="hidden" name="cbsecuritym3" value="(.*?)" />\n<input type="hidden" name="', ss, re.S)[0]

        headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"}
        url = "https://icpcarchive.ecs.baylor.edu/index.php?option=com_comprofiler&task=login"
        data = {'username': username,
                'passwd': passwd,
                'op2': 'login',
                'lang': 'english',
                'force_session': "1",
                'return': 'B:aHR0cDovL2ljcGNhcmNoaXZlLmVjcy5iYXlsb3IuZWR1Lw==',
                'message': '0',
                'loginfrom': 'loginmodule',
                'cbsecuritym3': special_key,
                'jd01a9ead890a15c1129763ef04c8f00e': '1',
                'remember': 'yes',
                'Submit': 'Login'
                }


        r = session.post(url, headers=headers, data=data)
        with open('test.html', 'w') as f:
            f.write(r.content)

        url = com
        html = session.get(url, allow_redirects = False, headers = headers)

        with open('test.html', 'w') as f:
            f.write(html.content)

        # read from a local html file
        with open('test.html', 'r') as f:
            ss = f.read()

        allContest = re.findall('<td><a href="(.*?)">Asia', ss, re.S)

        ans = []
        for curl in allContest:
            curl = 'https://icpcarchive.ecs.baylor.edu/'+curl.replace('&amp;','&')
            chtml = session.get(curl, allow_redirects = False, headers = headers)

            with open('ctest.html', 'w') as f:
                f.writelines(chtml.content)

            with open('ctest.html', 'r') as f:
                css = f.read()

            allProblems = re.findall('<tr class="sectiontableentry.*?>(.*?)</tr>', css, re.S)

            for prob in allProblems:
                try:
                    name = re.findall('<td><a href.*?>(.*?)</a>',prob,re.S)[0]
                    num = re.findall('<td align="right">(.*?)</td>',prob,re.S)[0]
                    ans.append((name,int(num)))
                except:
                    print 'enheng'

        ans.sort(key = lambda x: -x[1])

        for u in ans:
            out = ''
            while len(out) + len(u[0]) + len(str(u[1])) < tot:
                out += ' '
            csvfile.write(u[0] + out + str(u[1]) + '\n')


    except Exception as e:
        print e





















