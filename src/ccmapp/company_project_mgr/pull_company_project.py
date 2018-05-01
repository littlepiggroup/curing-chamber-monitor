# -*- coding: utf-8 -*-

import base64
import httplib
import logging
import traceback
import xml.etree.ElementTree as ET

from ccmapp.models import Project, BuildingCompany

logger = logging.getLogger(__name__)

def replace_keys(data_map, new_keys_map):
    for k, v in new_keys_map.items():
        if k in data_map.keys():
            data_map[v] = data_map[k]
            del data_map[k]

def getPrjInfo1():
    ''' 获取项目立项信息    '''
    SoapMessage = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <getPrjInfo xmlns="http://tempuri.org/">
      <Account>720e9000-4fd4-4bab-b8fa-139e5d0d0080</Account>
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
                    logger.info('Update Project: %s', child.attrib['PrjName'])
                    replace_keys(child.attrib, {'PrjName': 'project_name',
                                                'GCGS': 'company_name'})
                    if Project.objects.filter(PrjId=child.attrib["PrjId"]):

                        Project.objects.filter(PrjId=child.attrib["PrjId"]).update(**child.attrib)
                        pass
                    else:
                        newPrj = Project.objects.create(**child.attrib)
                        newPrj.save()
                except:
                    print traceback.print_exc()
                    continue

        updateCom()

        return True
    except:
        print traceback.print_exc()
        return False


def updateCom():
    for eachPrj in Project.objects.filter(company=None):
        logger.debug("Associate project and company: %s - %s", eachPrj.project_name, eachPrj.company_name)
        if not BuildingCompany.objects.filter(name=eachPrj.company_name) and eachPrj.company_name:
            newCom = BuildingCompany.objects.create(name=eachPrj.company_name)
            eachPrj.company = newCom
            eachPrj.save()

        else:
            eachPrj.company = BuildingCompany.objects.filter(name=eachPrj.company_name)[0]
            eachPrj.save()
    else:
        logger.debug("All projects are attached to company.")


if __name__ == '__main__':
    getPrjInfo1()