mysql -u root --password=123456  mydb   -e "SELECT NOW();"
SELECT concat('DROP TABLE IF EXISTS \`', table_name, '\`;') FROM information_schema.tables WHERE table_schema = 'MyDatabaseName';
SET FOREIGN_KEY_CHECKS = 0;
 DROP TABLE IF EXISTS `auth_group`;                     
 DROP TABLE IF EXISTS `auth_group_permissions`;         
 DROP TABLE IF EXISTS `auth_permission`;                
 DROP TABLE IF EXISTS `auth_user`;                      
 DROP TABLE IF EXISTS `auth_user_groups`;               
 DROP TABLE IF EXISTS `auth_user_user_permissions`;     
 DROP TABLE IF EXISTS `ccmapp_alertsubscriber`;         
 DROP TABLE IF EXISTS `ccmapp_buildingcompany`;         
 DROP TABLE IF EXISTS `ccmapp_buildingcompanyreport`;   
 DROP TABLE IF EXISTS `ccmapp_buildingcompanyuser`;     
 DROP TABLE IF EXISTS `ccmapp_camera`;                  
 DROP TABLE IF EXISTS `ccmapp_contract`;                
 DROP TABLE IF EXISTS `ccmapp_ezvizaccount`;            
 DROP TABLE IF EXISTS `ccmapp_globalreport`;            
 DROP TABLE IF EXISTS `ccmapp_humidityalert`;           
 DROP TABLE IF EXISTS `ccmapp_project`;                 
 DROP TABLE IF EXISTS `ccmapp_projectcurrentoverview`;  
 DROP TABLE IF EXISTS `ccmapp_projectname`;             
 DROP TABLE IF EXISTS `ccmapp_sample`;                  
 DROP TABLE IF EXISTS `ccmapp_samplealert`;             
 DROP TABLE IF EXISTS `ccmapp_sensor`;                  
 DROP TABLE IF EXISTS `ccmapp_temperaturealert`;        
 DROP TABLE IF EXISTS `ccmapp_temperaturehumiditydata`; 
 DROP TABLE IF EXISTS `ccmapp_video`;                   
 DROP TABLE IF EXISTS `ccmapp_videoalert`;              
 DROP TABLE IF EXISTS `diary_city`;                     
 DROP TABLE IF EXISTS `django_admin_log`;               
 DROP TABLE IF EXISTS `django_content_type`;            
 DROP TABLE IF EXISTS `django_migrations`;              
 DROP TABLE IF EXISTS `django_session`; 
SET FOREIGN_KEY_CHECKS = 1;