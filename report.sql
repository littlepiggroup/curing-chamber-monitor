
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

SELECT company_id, sample_name, count(id) as bad_sample_count FROM ccmapp_samplealert
WHERE TIMESTAMPDIFF(DAY, create_time, NOW()) <= 30
GROUP BY company_id, sample_name;

--SELECT create_time, TIMESTAMPDIFF(MINUTE, create_time, UTC_TIMESTAMP()),UTC_TIMESTAMP() FROM ccmapp_samplealert;
SELECT create_time, TIMESTAMPDIFF(DAY, create_time, NOW()),NOW() FROM ccmapp_samplealert;

--SELECT company_id, count(id), count(id)*0.5 as minus_score FROM ccmapp_samplealert
--WHERE TIMESTAMPDIFF(MINUTE, create_time, UTC_TIMESTAMP()) > 1
--GROUP BY company_id;

SELECT company_id,count(id)*0.5 as deduction FROM ccmapp_samplealert
WHERE TIMESTAMPDIFF(DAY, create_time, NOW()) >= 1 AND status = 'CREATED' AND TIMESTAMPDIFF(DAY, create_time, NOW()) <= 30
GROUP BY company_id;

-- 30 days
SELECT company_id, count(id) AS sample_alert_total FROM ccmapp_samplealert
WHERE TIMESTAMPDIFF(DAY, create_time, NOW()) <= 30
GROUP BY company_id;


SELECT company_id, count(id) as video_alert_total, count(id)*2 as video_alert_deduction FROM ccmapp_videoalert
WHERE TIMESTAMPDIFF(DAY, create_time, NOW()) <= 30
GROUP BY company_id;

SELECT company_id, count(id) as temperature_humidity_total, count(id)*2 as temperature_humidity_alert_deduction FROM ccmapp_temphumdtyalert
WHERE TIMESTAMPDIFF(DAY, create_time, NOW()) <= 30
GROUP BY company_id;

-- company phase report

SELECT
    ccmapp_project.building_company_id AS building_company_id,
    ccmapp_project.id AS project_id,
    count(ccmapp_alert.id) AS alert_count,
    count(ccmapp_alert.id) > 0 AS has_alert
FROM ccmapp_project LEFT OUTER JOIN ccmapp_alert ON ccmapp_project.id = ccmapp_alert.project_id
WHERE ccmapp_project.building_company_id = 8
    AND (ccmapp_alert.create_time IS NULL OR TIMESTAMPDIFF(DAY, ccmapp_alert.create_time, NOW()) <= 30)
GROUP BY ccmapp_project.id
;

SELECT
    ccmapp_project.building_company_id AS building_company_id,
    ccmapp_project.id AS project_id,
    count(ccmapp_alert.id) AS alert_count,
    count(ccmapp_alert.id) > 0 AS has_alert
FROM ccmapp_project LEFT OUTER JOIN ccmapp_alert ON ccmapp_project.id = ccmapp_alert.project_id
WHERE (ccmapp_alert.create_time IS NULL OR TIMESTAMPDIFF(DAY, ccmapp_alert.create_time, NOW()) <= 30)
GROUP BY ccmapp_project.id
;
-- project phase report

SELECT
    ccmapp_project.building_company_id AS building_company_id,
    ccmapp_project.id AS project_id,
    SUM(IF(ccmapp_alert.alert_type = 0, 1, 0)) AS sample_alert_count,
    SUM(IF(ccmapp_alert.alert_type = 1, 1, 0)) AS video_alert_count,
    100 - SUM(IF(ccmapp_alert.alert_type = 0, 1, 0)) * 0.5
        - SUM(IF(ccmapp_alert.alert_type = 1, 1, 0)) * 2.0
        - SUM(IF(ccmapp_alert.alert_type = 3 OR ccmapp_alert.alert_type = 4, 1, 0))*1.0
        AS score
FROM ccmapp_project LEFT OUTER JOIN ccmapp_alert ON ccmapp_project.id = ccmapp_alert.project_id
WHERE ccmapp_project.building_company_id = 4
    AND (ccmapp_alert.create_time IS NULL OR TIMESTAMPDIFF(DAY, ccmapp_alert.create_time, NOW()) <= 30)
GROUP BY ccmapp_project.id
;

SELECT
    ccmapp_project.building_company_id AS building_company_id,
    ccmapp_project.id AS project_id,
    count(ccmapp_samplealert.id) AS alert_count
FROM ccmapp_project LEFT OUTER JOIN ccmapp_samplealert ON ccmapp_project.id = ccmapp_samplealert.project_id
WHERE ccmapp_project.building_company_id = 4
    AND (ccmapp_samplealert.create_time IS NULL OR TIMESTAMPDIFF(DAY, ccmapp_samplealert.create_time, NOW()) <= 30)
GROUP BY ccmapp_project.id
;

SELECT COUNT(id) FROM ccmapp_samplealert
WHERE ccmapp_samplealert.company_id = 6
AND (ccmapp_samplealert.create_time IS NULL OR TIMESTAMPDIFF(DAY, ccmapp_samplealert.create_time, NOW()) <= 30);

