#!/usr/bin/env bash
DB_TARGET=$1

if [ "$DB_TARGET" == "REMOTE" ]; then
    HOST="rm-bp142w4w4lxg814kmo.mysql.rds.aliyuncs.com"
    USER="zzkj"
    PASSWORD="zzkj-19881209"
    DB="biaoyangshi"
elif [ "$DB_TARGET" == "LOCAL" ]; then
    HOST="localhost"
    USER="root"
    PASSWORD="123456"
    DB="mydb"
else
    echo "Unknown DB target: $DB_TARGET"
    exit 1
fi
echo "$SWITCH DB: $DB_TARGET"
sleep 5

DROP_SENTENCES=$(mysql -u $USER --password=$PASSWORD -h $HOST $DB    -e "SELECT concat('DROP TABLE IF EXISTS \`', table_name, '\`;') FROM information_schema.tables WHERE table_schema = '$DB';" 2>/dev/null | grep 'D' |grep -v table_name)
echo $DROP_SENTENCES | tr ';' "\n"
mysql -u $USER --password=$PASSWORD -h $HOST $DB -e "SET FOREIGN_KEY_CHECKS = 0; $DROP_SENTENCES" || exit 1
mysql -u $USER --password=$PASSWORD -h $HOST $DB -e "SET FOREIGN_KEY_CHECKS = 1;" || exit 1

rm -rf ccmapp/migrations/0*.py*
python manage.py makemigrations || exit 1
python manage.py migrate || exit 1
python manage.py sync_company_project || exit 1
python manage.py crontab add || exit 1

# Create Views
SQL_SCRIPT=create_views.sql
mysql -u $USER -h $HOST --password=$PASSWORD --database=$DB < $SQL_SCRIPT || exit 1

# populate some data.
SQL_SCRIPT=pop_test_data.sql
mysql -u $USER -h $HOST --password=$PASSWORD --database=$DB < $SQL_SCRIPT || exit 1

# Sync samples which will take a long time !!! 6 minutes
python manage.py sync_samples
python manage.py scan_sample_alert
