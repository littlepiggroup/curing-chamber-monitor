import logging

import time

import sys

from ccmapp.models import UserCollectProject, Project, UserFollowProject, AlertNotification
from ccmapp.utility import send_mobile_alert_msg

logger = logging.getLogger(__name__)

def get_proj_ids_collected_by_user(user_id, collected=True):

    projs_collected_cur_user = UserCollectProject.objects.filter(user_id=user_id)
    if collected:
        return [proj.id for proj in projs_collected_cur_user]
    else:
        proj_ids = [proj.id for proj in projs_collected_cur_user]
        proj_uncollected = [proj.id for proj in Project.objects.exclude(pk__in=proj_ids)]
        return proj_uncollected


def get_proj_ids_followed_by_user(user_id, is_follow=True):

    projs_followed_by_cur_user = UserFollowProject.objects.filter(user_id=user_id)
    if is_follow:
        return [proj.id for proj in projs_followed_by_cur_user]
    else:
        proj_ids = [proj.id for proj in projs_followed_by_cur_user]
        proj_uncollected = [proj.id for proj in Project.objects.exclude(pk__in=proj_ids)]
        return proj_uncollected


def notify_video_alert(video_alert):
    # video_alert -> project_id (name) -> send to all followers
    alert_comment = video_alert.comment
    project = video_alert.project
    project_id = project.id
    project_name = project.project_name
    user_phones = [follow.user.phone for follow in UserFollowProject.objects.filter(project_id=project_id)]
    for phone in user_phones:
        print 'Send to %s, %s' % (phone, alert_comment)
        alert_notify = AlertNotification(phone=phone, project_name=project_name, content=alert_comment)
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




