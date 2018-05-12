import logging

import time

import sys

from ccmapp.models import UserCollectProject, Project, UserFollowProject, AlertNotification
from ccmapp.utility import send_mobile_alert_msg

logger = logging.getLogger(__name__)


def get_proj_ids_collected_by_user(user_id, collected=True):

    proj_ids = [proj_user.project_id for proj_user in UserCollectProject.objects.filter(user_id=user_id)]
    if collected:
        return proj_ids
    else:
        proj_uncollected = [proj.id for proj in Project.objects.exclude(pk__in=proj_ids)]
        return proj_uncollected


def get_proj_ids_followed_by_user(user_id, is_follow=True):
    proj_ids = [proj_user.project_id for proj_user in UserFollowProject.objects.filter(user_id=user_id)]
    if is_follow:
        return proj_ids
    else:
        proj_uncollected = [proj.id for proj in Project.objects.exclude(pk__in=proj_ids)]
        return proj_uncollected


def save_alert_notification(alert):
    # video_alert -> project_id (name) -> send to all followers
    alert_description = alert.description
    project = alert.project
    project_id = project.id
    project_name = project.project_name[:10]
    logger.debug('Short project name: %s', project_name)
    logger.info('Project id for current alert: %s', project_id)
    user_phones = [follow.user.phone for follow in UserFollowProject.objects.filter(project=project_id)]
    if len(user_phones) == 0:
        logger.info("Not found users who are interested in this alert. No need to save notification to DB.")

    for phone in user_phones:
        logger.info('Save alert notification: %s, %s', phone, alert_description)
        alert_notify = AlertNotification(phone=phone, project_name=project_name, content=alert_description)
        alert_notify.save()
        # send_mobile_alert_msg(phone, project_name, alert_comment)


def send_alert_short_message():
    MSG_COUNT = 10
    alerts = AlertNotification.objects.all()[:MSG_COUNT]
    logger.info("Try to send %s alerts" % len(alerts))
    for alert in alerts:
        logger.info('Sleep 5 seconds for sending message')
        time.sleep(5)
        logger.info("Send alert %s,%s,%s" % (str(alert.id), alert.content, str(alert.create_time)))
        print alert.create_time
        try:
            rc = send_mobile_alert_msg(alert.phone, alert.project_name, alert.content)
            # sys.stderr.write("Send")
            if rc:
                logger.info("Send msg succesffully!")
                alert.delete()
            else:
                logger.error("Failed to send short message for alert without any exception.")
        except Exception, e:
            print 'TODO : %s' % (str(e))
            logger.error('Failed to send txt message: %s' % str(e))
