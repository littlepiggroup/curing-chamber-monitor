DROP VIEW ccmapp_alert;
CREATE VIEW ccmapp_alert AS
SELECT
1 as id,
company_id AS company_id,
project_id AS project_id,
status AS status,
create_time AS create_time,
update_time AS update_time
FROM ccmapp_samplealert

UNION

SELECT
1 as id,
company_id AS company_id,
project_id AS project_id,
status AS status,
create_time AS create_time,
update_time AS update_time
FROM ccmapp_videoalert

UNION

SELECT
1 as id,
company_id AS company_id,
project_id AS project_id,
status AS status,
create_time AS create_time,
update_time AS update_time
FROM ccmapp_temphumdtyalert;


-- Monthly Report
SELECT project_id,name, count(instance_id)
FROM ccmapp_sample
GROUP BY project_id,name,regular
HAVING regular = 0;

SELECT name,regular,instance_id,exam_result,hnt_yhtj FROM ccmapp_sample;

SELECT name,regular, instance_id, exam_result, hnt_yhtj FROM ccmapp_sample
WHERE   (hnt_yhtj='标准养护' AND regular = 0) OR (hnt_yhtj != '标准养护' AND (regular=0 OR exam_result > 100));

SELECT company_id,name, count(instance_id) FROM ccmapp_sample
WHERE   (hnt_yhtj='标准养护' AND regular = 0) OR (hnt_yhtj != '标准养护' AND (regular=0 OR exam_result > 100))
GROUP BY company_id, name;

SELECT create_time,TIMESTAMPDIFF(MINUTE, create_time, UTC_TIMESTAMP()),UTC_TIMESTAMP() FROM ccmapp_samplealert;
SELECT company_id, count(id), count(id)*0.5 as minus_score FROM ccmapp_samplealert
WHERE TIMESTAMPDIFF(MINUTE, create_time, UTC_TIMESTAMP()) > 1
GROUP BY company_id;




