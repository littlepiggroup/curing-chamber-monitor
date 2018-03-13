# pocket_monitor
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
