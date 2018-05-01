# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import sys
import httplib, socket
import xml.etree.ElementTree as ET
import base64

from ccmapp.models import *
from ccmapp.samplemgr.retriever import UserInfoRetriever
from ccmapp.samplemgr.update_samples import Sync

logger = logging.getLogger(__name__)

user_info_retriever = UserInfoRetriever()

reload(sys)
sys.setdefaultencoding('utf8')
test_account = "720e9000-4fd4-4bab-b8fa-139e5d0d0080"
socket.setdefaulttimeout(2)


def updateCom():
    for eachPrj in Project.objects.filter(company=None):
        if eachPrj.GCGS:
            company = BuildingCompany.objects.filter(name=eachPrj.GCGS)
            if len(company) > 0:
                eachPrj.company = company[0]
            else:
                newCom = BuildingCompany.objects.create(name=eachPrj.GCGS)
                eachPrj.company = newCom
                eachPrj.save()


def getPrjInfo1(account):
    ''' 获取项目立项信息    '''
    SoapMessage = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <getPrjInfo xmlns="http://tempuri.org/">
      <Account>''' + account + '''</Account>
    </getPrjInfo>
  </soap:Body>
</soap:Envelope>'''
    try:
        # 使用的WebService地址为sdk.entinfo.cn:8061/webservice.asmx，
        webservice = httplib.HTTP("116.236.180.116:44")
        # 连接到服务器后的第一个调用。它发送由request字符串到到服务器
        webservice.putrequest("POST", "/WS_Tech/Webservice_Tech.asmx")
        webservice.putheader("Host", "116.236.180.116")
        #     webservice.putheader("User-Agent", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)")
        webservice.putheader("Content-type", "text/xml")
        webservice.putheader("Content-Length", len(SoapMessage))
        webservice.putheader("SOAPAction", '"http://tempuri.org/getPrjInfo"')
        # 发送空行到服务器，指示header的结束
        webservice.endheaders()
        # 发送报文数据到服务器
        webservice.send(SoapMessage)
        # 获取返回HTTP 响应信息

        statuscode, statusmessage, header = webservice.getreply()
        resmessage = webservice.getfile().read()

        OutXml = unicode(base64.b64decode(
            resmessage[resmessage.find('<getPrjInfoResult>') + 18:resmessage.find('</getPrjInfoResult>')]), "gbk")

        root = ET.fromstring(OutXml.encode("utf-8", "ignore"))
        for child in root:
            if child.attrib:
                try:
                    if Project.objects.filter(PrjId=child.attrib["PrjId"]):
                        Project.objects.filter(PrjId=child.attrib["PrjId"]).update(**child.attrib)
                        pass
                    else:
                        newPrj = Project.objects.create(**child.attrib)
                        newPrj.save()
                except:
                    print traceback.print_exc()
                    continue

        print "update Company"
        updateCom()

        return True
    except:
        print traceback.print_exc()
        return False


import urllib2, traceback, json


def getPrjInfo():
    try:
        req = urllib2.Request("http://www.wufea.com/scg4/prjinfotodaily.asp?dcount=sihttst8Z3eKar3rUrrm")
        # enable cookie
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req)
        body = json.loads(response.read().decode('gbk').encode('utf8'))
        for prj in body['prjinfotodaily']:
            myprj = {}
            for key in prj:
                if key == 'mj':
                    myprj['area'] = prj[key]
                elif key == 'zj':
                    myprj['price'] = prj[key]
                elif key == 'dtsl':
                    myprj['danti_nums'] = prj[key]
                elif key == 'aqmb':
                    myprj['safe_target'] = prj[key]
                elif key == 'zlmb':
                    myprj['quality_target'] = prj[key]
                elif key == 'hbmb':
                    myprj['environment_target'] = prj[key]
                elif key == 'xmmb':
                    myprj['project_target'] = prj[key]
                elif key == 'wmmb':
                    myprj['culture_target'] = prj[key]
                elif key == 'htmb':
                    myprj['pact_target'] = prj[key]
                elif key == 'sd':
                    myprj['deep'] = prj[key]
                elif key == 'gd':
                    myprj['height'] = prj[key]
                elif key == 'xmjd':
                    myprj['longitude'] = prj[key]
                elif key == 'xmwd':
                    myprj['latitude'] = prj[key]
                elif key == 'KGRQ' or key == 'JGRQ':
                    if prj[key]:
                        myprj[key] = prj[key]
                else:
                    myprj[key] = prj[key]
            if Project.objects.filter(PrjId=myprj['PrjId']).count():
                print u'更新Project信息', myprj
                apply(Project.objects.filter(PrjId=myprj['PrjId']).update, (), myprj)
            elif myprj['PrjId']:
                print u'创建Project', myprj
                apply(Project.objects.create, (), myprj)
    except:
        traceback.print_exc()


def getSGFAWFDealInfo(account, faid):
    ''' 获取指定施工方案的流程意见 '''
    SoapMessage = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <getSGFAWFDealInfo xmlns="http://tempuri.org/">
      <Account>''' + account + '''</Account>
      <FAID>''' + str(faid) + '''</FAID>
    </getSGFAWFDealInfo>
  </soap:Body>
</soap:Envelope>'''
    try:
        spyjList = []
        # 使用的WebService地址为sdk.entinfo.cn:8061/webservice.asmx，
        webservice = httplib.HTTP("116.236.180.116:44")
        # 连接到服务器后的第一个调用。它发送由request字符串到到服务器
        webservice.putrequest("POST", "/WS_Tech/Webservice_Tech.asmx")
        webservice.putheader("Host", "116.236.180.116")
        #     webservice.putheader("User-Agent", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)")
        webservice.putheader("Content-type", "text/xml")
        webservice.putheader("Content-Length", len(SoapMessage))
        webservice.putheader("SOAPAction", '"http://tempuri.org/getSGFAWFDealInfo"')
        # 发送空行到服务器，指示header的结束
        webservice.endheaders()
        # 发送报文数据到服务器
        webservice.send(SoapMessage)
        # 获取返回HTTP 响应信息

        statuscode, statusmessage, header = webservice.getreply()
        resmessage = webservice.getfile().read()
        OutXml = unicode(base64.b64decode(resmessage[resmessage.find('<getSGFAWFDealInfoResult>') + 25:resmessage.find(
            '</getSGFAWFDealInfoResult>')]), "gbk")
        root = ET.fromstring(OutXml.encode("utf-8", "ignore"))

        for child in root:
            if child.attrib:
                spyjList.append(child.attrib)

        return spyjList
    except:
        traceback.print_exc()
        return []


def getSGFAWFAttachInfo(account, faid):
    ''' 获取指定施工方案的附件信息 '''
    SoapMessage = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <getSGFAAttachment xmlns="http://tempuri.org/">
      <Account>''' + account + '''</Account>
      <FAID>''' + str(faid) + '''</FAID>
    </getSGFAAttachment>
  </soap:Body>
</soap:Envelope>'''
    try:
        attachList = []
        # 使用的WebService地址为sdk.entinfo.cn:8061/webservice.asmx，
        webservice = httplib.HTTP("116.236.180.116:44")
        # 连接到服务器后的第一个调用。它发送由request字符串到到服务器
        webservice.putrequest("POST", "/WS_Tech/Webservice_Tech.asmx")
        webservice.putheader("Host", "116.236.180.116")
        #     webservice.putheader("User-Agent", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)")
        webservice.putheader("Content-type", "text/xml")
        webservice.putheader("Content-Length", len(SoapMessage))
        webservice.putheader("SOAPAction", '"http://tempuri.org/getSGFAAttachment"')
        # 发送空行到服务器，指示header的结束
        webservice.endheaders()
        # 发送报文数据到服务器
        webservice.send(SoapMessage)
        # 获取返回HTTP 响应信息

        statuscode, statusmessage, header = webservice.getreply()
        resmessage = webservice.getfile().read()
        OutXml = unicode(base64.b64decode(
            resmessage[resmessage.find('<getSGFAAttachment>') + 25:resmessage.find('</getSGFAAttachment>')]), "gbk")
        root = ET.fromstring(OutXml.encode("utf-8", "ignore"))

        for child in root:
            if child.attrib:
                attachList.append(child.attrib)

        return attachList
    except:
        traceback.print_exc()
        return []


def getPrjInfo():
    building_company_users = BuildingCompanyUser.objects.filter(disabled=False)
    if len(building_company_users) == 0:
        logger.info("Not find build company user!")
    for building_company_user in building_company_users:
        try:
            # 还没有instance_id, 同步instance_id
            if not building_company_user.instance_id:
                raw_data = Sync._get_raw_data(user_info_retriever.retrieve(building_company_user.login_name))
                if raw_data:
                    building_company_user.instance_id = raw_data[0]["UserId"]
                    building_company_user.save()
        except Exception as e:
            exstr = traceback.format_exc()
            logger.error('Sync projects error for build company user %d: %s %s' %
                         (building_company_user.id, type(e), exstr))
            continue
        if building_company_user.instance_id:
            getPrjInfo1(building_company_user.instance_id)


if __name__ == '__main__':
    getPrjInfo()
