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



