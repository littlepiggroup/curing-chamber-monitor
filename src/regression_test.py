# -*- coding: utf-8 -*-

import requests

# For now, it is just a sanity.

if __name__ == '__main__':
    IP = '127.0.0.1'
    PORT = '8000'
    app_urls = [
        '/api/projects?company=1',
        '/api/company_score_report?orderby_score_asc=true&time_range=last_month',
        '/api/company_score_report?orderby_score_asc=false&time_range=last_month',
        '/api/project_score_report?company_id=1&orderby_score_asc=false&time_range=last_month',
        '/api/projects',
        '/api/sensors?project=1',
        '/api/alerts',
        '/api/projects?search=%E5%A4%A7%E8%8A%A6%E7%BA%BF%E8%88%AA%E9%81%93',
        '/api/project_collects'
    ]

    s = requests.Session()
    r = s.post('http://%s:%s/api-auth/login' % (IP, PORT), json={"phone":"13012345678", "password":"13012345678_123456"})
    if r.status_code == 200:
        print 'Login OK.'
    else:
        print r.status_code
        print r.text
        r = s.post('http://%s:%s/api-auth/access_login_code' % (IP, PORT),
                   json={"phone": "13012345678"})
        r = s.post('http://%s:%s/api-auth/login' % (IP, PORT),
                   json={"phone": "13012345678", "password": "13012345678_123456"})
        if r.status_code == 200:
            print 'Login OK.'
        else:
            print r.status_code
            print r.text
            exit(1)

    for my_url in app_urls:
        full_url = 'http://%s:%s%s' % (IP, PORT, my_url)
        r = s.get(full_url)
        if r.status_code !=  200:

            print 'Error!!!! When query: %s' % full_url
            print r.status_code
            print r.text
            exit(1)
        else:
            print '[PASSED] GET %s' % full_url

    # Temp create 25 alerts
    body = {
            "description": "视频报警",
            "comment": "张三回去处理",
            "video": 1,
            "project": 2,
            "company": 1
        }
    for i in range(25):
        print 'Create alert %d' % i
        body['comment']='One %s' % i
        r = s.post('http://%s:%s/api/video_alerts' % (IP, PORT), json=body)
        if r.status_code != 200 and r.status_code != 201:
            print 'Error %d,%s' % (r.status_code, r.text)

