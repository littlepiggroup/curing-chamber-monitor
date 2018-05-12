
-- test user

INSERT INTO ccmapp_user(id, name, password,  department, last_login, is_superuser,first_name, last_name, is_active, date_joined, is_staff, phone)
VALUES
(1, '万磁王', 'pbkdf2_sha256$24000$OU7XlZAEk6Fz$+2FOPHvB0SW4YAt7z2jl446fIH/MZfFa8iPNWRkchs4=', '某公司某部', NOW(), 0, 'Tim', 'Cook', 1, NOW(), 0, '13012345678')
;

-- Real data
INSERT INTO ccmapp_buildingcompanyuser (login_name, disabled, added_time) VALUES ('q8690', 0, NOW());
INSERT INTO ccmapp_buildingcompany (name, disabled, added_time) VALUES ('上海建工四建集团有限公司', 0, NOW());
insert into ccmapp_project (project_name, company_id, added_time, PrjSFLX, environment_target)
values ('上海世博会博物馆新建工程', (select id from ccmapp_buildingcompany where name = '上海建工四建集团有限公司'), NOW(),1,'env_target');

-- Mock sample and alert data
INSERT INTO ccmapp_contract(project_id, serial_num, sign_number, checked_date_time, added_time, checked)
VALUES
(1, '123456','sign_1', NOW(), NOW(), 1)
;



INSERT INTO ccmapp_sample
(project_id, company_id, instance_id, contract_id, name, regular, num, hnt_yhtj, exam_result, exam_result_str, item_name, added_time)
VALUES
(1, 1, 'sample_instance_1', 1, '混凝土试件', 0, '10', '标准养护', 120, '合格', 'item_name', NOW()),
(1, 1, 'sample_instance_2', 1, '钢筋', 0, '10', '非标准养护', 120, '合格', 'item_name_2', NOW())
;

INSERT INTO ccmapp_samplealert
(sample_name, alert_type, status, create_time, update_time, company_id, project_id, sample_id, created_by,updated_by)
VALUES
('混凝土试件', 0, 'CREATED', NOW(), NOW(), 1, 1, 1,'Xiao Wang','Xiao Hei'),
('钢筋', 0, 'CREATED', NOW(), NOW(), 1, 1, 2,'Xiao Wang','Xiao Hei')
;

-- Real video data.
INSERT INTO ccmapp_ezvizaccount (user_name, app_key, secret, access_token, access_token_expire_time)
VALUES ('13795232897', 'f0278514f31b41dab85b96a7f2510fcf', 'ff7f1cfe82b907c24a06dca343eb04ed',
 'at.cyydx889b3li6ekn98rq10bk7c4g1tsk-2vc4wgnyqc-1iek1k6-3kwnu2wda', 12334);

INSERT INTO ccmapp_camera (device_serial_number, rtmp_address, ezviz_account_id, project_id)
VALUES ('762881292','rtmp://rtmp.open.ys7.com/openlive/bfed2855f58d4dd6891e670060540a7a', 1, 1);

-- INSERT INTO ccmapp_video (save_abs_path, url_path, camera_id, video_type, create_time)
-- VALUES ('temp','temp', 1, 1, NOW());

-- INSERT INTO ccmapp_videoalert
-- (alert_type, status, create_time, update_time, company_id, project_id, video_id, created_by_id, updated_by_id)
-- VALUES
--    (1, 'CREATED', NOW(), NOW(), 1, 2, 1, 1, 1)
-- ;

-- Mock temperature and humidity.
insert into ccmapp_sensor (device_number, sensor_type, project_id, name, description)
VALUES ('device_number', 'sensor_type', 1, 'YangHuShi', 'YongTu');

insert into ccmapp_temperaturealert
(alert_type, status, create_time, update_time, company_id, project_id, sensor_id, created_by,updated_by)
VALUES (2, 'CREATED', NOW(), NOW(), 1,1,1,'XiaoCui', 'XiaoMa');

insert into ccmapp_humidityalert
(alert_type, status, create_time, update_time, company_id, project_id, sensor_id, created_by,updated_by,
description, comment)
VALUES (3, 'CREATED', NOW(), NOW(), 1,1,1,'XiaoCui', 'XiaoMa', 'You Bao Jing', 'Wei Chu Li.');


INSERT INTO ccmapp_temperaturehumiditydata
(temperature, humidity, collect_time, create_time, company_id, project_id, sensor_id)
VALUES
(28.0, 90,' 2018-04-26 14:56:37', ' 2018-04-21 14:56:37', 1, 1, 1),
(25.0, 80,' 2018-04-26 15:00:00', ' 2018-04-21 15:00:00', 1, 1, 1),
(26.0, 50,' 2018-04-26 15:10:00', ' 2018-04-21 15:10:00', 1, 1, 1),
(25.0, 80,' 2018-04-26 15:20:00', ' 2018-04-21 15:20:00', 1, 1, 1),
(25.0, 60,' 2018-04-26 15:30:00', ' 2018-04-21 15:30:00', 1, 1, 1),
(15.0, 80,' 2018-04-26 15:40:00', ' 2018-04-21 15:4:00', 1, 1, 1),
(38.0, 19,' 2018-04-26 15:50:00', ' 2018-04-21 15:50:00', 1, 1, 1),
(15.0, 80,' 2018-04-26 16:00:00', ' 2018-04-21 16:00:00', 1, 1, 1)
;
