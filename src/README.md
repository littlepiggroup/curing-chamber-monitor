# curing chamber monitor

## Build & Test Status
* [![Build Status](https://travis-ci.org/littlepiggroup/curing-chamber-monitor.svg?branch=integration)](https://travis-ci.org/littlepiggroup/curing-chamber-monitor)

## Requirements
* The VERSIONs of libs bimsheng are using! Please give me your requirements.

## URLs
```
http://127.0.0.1:8000/api/company_phase_report?time_range=last_day
http://127.0.0.1:8000/api/company_phase_report?time_range=last_week
http://127.0.0.1:8000/api/company_phase_report?time_range=last_month
http://127.0.0.1:8000/api/company_phase_report?company_id=8&time_range=last_day
http://127.0.0.1:8000/api/company_phase_report?company_id=8&time_range=last_week
http://127.0.0.1:8000/api/company_phase_report?company_id=8&time_range=last_month
http://127.0.0.1:8000/api/project_phase_report?time_range=last_day
http://127.0.0.1:8000/api/project_phase_report?time_range=last_week
http://127.0.0.1:8000/api/project_phase_report?time_range=last_month
http://127.0.0.1:8000/api/project_phase_report?company_id=4&time_range=last_day
http://127.0.0.1:8000/api/project_phase_report?company_id=4&time_range=last_week
http://127.0.0.1:8000/api/project_phase_report?company_id=4&time_range=last_month
http://127.0.0.1:8000/api/project_phase_report?time_range=last_day&project_id=8
http://127.0.0.1:8000/api/alerts?is_open=true&project__id=7

http://127.0.0.1:8000/api/project_sensor_data_series?project_id=1&sensor_id=1


# Gene monthly excel report
http://127.0.0.1:8000/api/excel_report

# Video co

```

## Function
### Register user and login/logout
* POST /api-auth/access_login_code {"phone":"13795232897", "department":"xx", "name":"xxx"}. 
    * It should send a vcode to the phone. But for now, it only set default password as 13012345678_123456
* Login:POST /api-auth/login  {"phone":"13012345678","password":"13012345678_123456"}
    * It will login and set the session cookie in reponse.
* Logout: POST /api-auth/logout

### Get current user info
* GET http://127.0.0.1:8000/api/current_user
```json
{
    "id": 1,
    "last_login": "2018-04-29T16:24:04.860448",
    "first_name": "Tim",
    "last_name": "Cook",
    "is_active": true,
    "date_joined": "2018-04-29T01:21:41",
    "is_staff": false,
    "phone": "13012345678",
    "name": "万磁王",
    "department": "某公司某部",
    "groups": [],
    "user_permissions": []
}
```
### Project collect
* Collect: POST /api/projects/1/collect
    * Pre-condition: User has logged in.
    
* Un-collect: POST /api/projects/1/uncollect
    * Pre-condition: User has logged in.

* GET /api/project_collects  will return all projects collected by current user.
    * Pre-condition: User has logged in.
    
### Project subscribe:
* TODO

### Temperature and Humidity Data for project.
* Get the data. Parameter is time_range=last_day|last_week|last_month, project_id = <proj_id> and sensor_id=<sensor_id>
    * Request: http://127.0.0.1:8000/api/project_sensor_data_series?project_id=1&sensor_id=1&time_range=last_day
    * Response:
    ```json
    {
        "count": 8,
        "next": null,
        "previous": null,
        "results":[
            {
            "has_temperature": true,
            "has_humidity": true,
            "temperature": 28,
            "collect_time": "2018-04-21T14:56:37",
            "humidity": 90
            },
            ...
    ```
    
### Video auto collect
* Step 1: Create EzvizClient
    * POST /api/ezviz_accounts 
    * {"user_name":"xx","app_key":"xx","secret":"xx"}
* Step 2: Create camera
    * POST /api/cameras
    * {"ezviz_account": 2,"project": 2,"device_serial_number": "762881292"}

### Generate monthly excel report.
* Step 1: Generate excel on the server
    * POST http://127.0.0.1:8000/api/excel_report    #Post body is empty.
    * Response: {"report_url": "media/monthly_excel_reports/monthly_excel_report_2018-04-22_1524436018.xlsx"}
* Step 2: Download the excel report at: http://127.0.0.1:8000/media/monthly_excel_reports/monthly_excel_report_2018-04-22_1524436018.xlsx

### Upload project image
* Upload by curl: You have to covert the upload method to JS
    * `curl -X POST -S -F "project_id=1" -F "file=@block2.988e1af.jpg;type=image/jpg" 127.0.0.1:8000/api/upload_project_cover`
    * Response: `{"project_id":"1","image_url":"media/projects/1/images/cover.jpg"}`
* Then you can see the image_url in project_phase_report API.
    * Response:
    ```json
     {
        "project_name": "白龙港污水处理厂提标改造工程BLG-C6标（南部地块生物处理区土建工程）",
        "image_url": "media/projects/1/images/cover.jpg",
        "company_name": "市政工程公司",
        "video_alert_count": 0,
        "humidity_alert_count": 0,
        "score": 96.5,
        "project_id": 1,
        "sample_alert_count": 7,
        "temperature_alert_count": 0
      }
    ```
### Report Video alert
* Create Video alert. 
    * POST http://127.0.0.1:8000/api/video_alerts
    * Body:
        ```json
        		{
            "description": "视频报警",
            "comment": "张三回去处理",
            "video": 1,
            "project": 2,
            "company": 1
        }
        ```
* Update/Close Video Alert.
    * Update: PUT http://127.0.0.1:8000/api/video_alerts/1
    * Body:
        ```json
		{
          "comment": "xx回去处理",
          "status":"FIXING",
          "video":1
        }
        ```
     * Close: PUT http://127.0.0.1:8000/api/video_alerts/1
        {
          "comment": "XX close it",
          "status":"CLOSED",
          "video":1
        }

### filter project by company
* http://127.0.0.1:8000/api/projects?company=1

### filter sensors by project id.
http://127.0.0.1:8000/api/sensors?project=1

### Get company score report
* http://127.0.0.1:8000/api/company_score_report?orderby_score_asc=true&time_range=last_month
* http://127.0.0.1:8000/api/company_score_report?orderby_score_asc=false&time_range=last_month

## 项目结构
* curing chamber monitor目录是Django的project, ccm/ccmapp是Django的app. 一个project可以包含多个app.
* http://www.django-rest-framework.org/tutorial/quickstart/ it explains why place db folder under pocket-monitor.
`It may look unusual that the application has been created within the project directory. Using the project's namespace avoids name clashes with external module (topic goes outside the scope of the quickstart).`
* In best practice, we don't place app folder under site-level folder: https://docs.djangoproject.com/en/1.11/intro/tutorial01/#creating-a-project,
https://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/

## Deploy
* Environment requirements: Linux, Python 2.7, ffmpeg(ubuntu: apt install ffmpeg)
* For now, we haven't switched to MySQL. Sqlite is still in use.
* Run bash script  `./deploy_and_run.sh`

## Code flow:
### urls -> db.urls -> db.views -> db.serializers -> db.models
1. urls: expose urls
2. db.urls: define the exposed rest apis
3. db.views: define the views mapping to the exposed rest apis
4. db.serializers -> serialize/deserialize model between views and backend models
5. db.models -> backend models associated to db tables.

## Set up
Install depends libs
```shell
pip install django
pip install djangorestframework
pip install django-filter
```

Install\Upgrade db

```shell
python install_db.py
```

## Start server

```shell
python start.py
```

## End to end test
Use restful client browser plugin or install command line tool restful client as below:
```shell
pip install httpie
```
Reference: Command Line Restful Client <https://httpie.org/doc>

## Browse db tables

```shell
pip install sqlite-web
python admin.py
```
Reference: Sqlite DB Browser <https://github.com/coleifer/sqlite-web>

## Tips
add super user
```shell
python manage.py createsuperuser --username=admin --email=admin@example.com
```
