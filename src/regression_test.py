# -*- coding: utf-8 -*-

import requests
import json


# For now, it is just a sanity.

def upload_image_cover(s, ip, port):
    data = {"project_id": "1"}
    image_path = '/home/jichao/Downloads/project_cover.jpg'
    files = {'file': ('report.xls', open(image_path, 'rb'), 'image/jpg')}
    upload_url = 'http://%s:%s%s' % (ip, port, '/api/upload_project_cover')
    r = s.post(upload_url, data, files=files)
    if  r.status_code != 201:
        print "Error when upload project cover."
        exit(1)
    else:
        print 'Upload successfully. Response: %s' % r.text
        json_resp = json.loads(r.text)
        print json_resp
        download_url = 'http://%s:%s/%s' % (ip, port, json_resp['image_url'])
        import shutil
        response = s.get(download_url, stream=True)
        with open('download_project_cover.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        import os
        if not os.path.exists('download_project_cover.jpg'):
            print 'Failed to download project cover. exit.'
            exit(1)
        else:
            print 'Download successfully.'


def upload_video(s, ip, port):
    data = {"project_id": "1"}
    image_path = '/home/jichao/test_artifacts/project_video.mp4'
    files = {'file': ('report.xls', open(image_path, 'rb'), 'video/mp4')}
    upload_url = 'http://%s:%s%s' % (ip, port, '/api/upload_project_video')
    r = s.post(upload_url, data, files=files)
    if  r.status_code != 201:
        print "Error when upload video for project."
        print r.text
        exit(1)
    else:
        print 'Upload project video successfully. Response: %s' % r.text
        json_resp = json.loads(r.text)
        print json_resp
        download_url = 'http://%s:%s/%s' % (ip, port, json_resp['url_path'])
        import shutil
        response = s.get(download_url, stream=True)
        with open('download_project_video.mp4', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        import os
        if not os.path.exists('download_project_video.mp4'):
            print 'Failed to download project video. exit.'
            exit(1)
        else:
            print 'Download project video successfully.'


def login(s, ip, port):
    r = s.post('http://%s:%s/api-auth/login' % (ip, port),
               json={"phone": "13012345678", "password": "13012345678_123456"})
    if r.status_code == 200:
        print 'Login OK.'
    else:
        print r.status_code
        print r.text
        r = s.post('http://%s:%s/api-auth/access_login_code' % (ip, port),
                   json={"phone": "13012345678"})
        r = s.post('http://%s:%s/api-auth/login' % (ip, port),
                   json={"phone": "13012345678", "password": "13012345678_123456"})
        if r.status_code == 200:
            print 'Login OK.'
        else:
            print r.status_code
            print r.text
            exit(1)


def sanity_test(s, ip, port):
    app_urls = [
        '/api/projects?company=1',
        '/api/project_sensor_data_series?sensor_id=1&time_range=last_month',
        '/api/company_score_report?orderby_score_asc=true&time_range=last_month',
        '/api/company_score_report?orderby_score_asc=false&time_range=last_month',
        '/api/project_score_report?company_id=1&orderby_score_asc=false&time_range=last_month',
        '/api/projects',
        '/api/sensors?project=1',
        '/api/alerts',
        '/api/projects?search=%E5%A4%A7%E8%8A%A6%E7%BA%BF%E8%88%AA%E9%81%93',
        '/api/project_collects'
    ]

    for my_url in app_urls:
        full_url = 'http://%s:%s%s' % (ip, port, my_url)
        r = s.get(full_url)
        if r.status_code != 200:

            print 'Error!!!! When query: %s' % full_url
            print r.status_code
            # print r.text
            exit(1)
        else:
            print '[PASSED] GET %s' % full_url

    # Temp create 25 alerts
    body = {
        "description": "视频报警",
        "comment": "张三去处理",
        "video": 14,
        "project": 2,
        "company": 1
    }
    for i in range(2):
        print 'Create alert %d' % i
        body['comment'] = 'Comment %s' % i
        r = s.post('http://%s:%s/api/video_alerts' % (ip, port), json=body)
        if r.status_code != 200 and r.status_code != 201:
            print 'Error %d,%s' % (r.status_code, r.text)


if __name__ == '__main__':
    IP = '127.0.0.1'
    PORT = '8000'
    s = requests.Session()
    login(s, IP, PORT)
    upload_image_cover(s, IP, PORT)
    upload_video(s, IP, PORT)
    sanity_test(s, IP, PORT)
