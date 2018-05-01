#!/bin/bash
# Local DB
USER='root'
PASSWORD='123456'
HOST='localhost'
DB='mydb'

# Remote DB
USER='zzkj'
PASSWORD='zzkj-19881209'
HOST='rm-bp142w4w4lxg814kmo.mysql.rds.aliyuncs.com'
DB='biaoyangshi'
DROP_SENTENCES=$(mysql -u $USER --password=$PASSWORD -h $HOST $DB    -e "SELECT concat('DROP TABLE IF EXISTS \`', table_name, '\`;') FROM information_schema.tables WHERE table_schema = '$DB';" 2>/dev/null | grep 'D' |grep -v table_name)
echo $DROP_SENTENCES | tr ';' "\n"
mysql -u $USER --password=$PASSWORD -h $HOST $DB -e "SET FOREIGN_KEY_CHECKS = 0; $DROP_SENTENCES"
mysql -u $USER --password=$PASSWORD -h $HOST $DB -e "SET FOREIGN_KEY_CHECKS = 1;"
