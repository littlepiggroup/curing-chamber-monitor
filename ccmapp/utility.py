# -*- coding: utf-8 -*-
#和功能无关的实用函数
from django.db import models
from django.core.serializers import serialize,deserialize
from django.db.models.query import QuerySet
import json, urllib2
from django.conf import settings
import os,random,time, sys
from django.template import RequestContext
# import qrcode 
import  datetime
import calendar
import memcache
from datetime import date

# -*- coding: utf-8 -*-
import os,time,random, sys, datetime, calendar, traceback,zipfile
import httplib,json,socket
import xml.etree.ElementTree as ET 
import  xml.dom.minidom as minidom
import json,thread, base64,codecs, chardet

from django.conf import settings
from ccm.settings import UPLOAD_DIR
from ccmapp.models import *
from django.db.models import Q

reload(sys)  
sys.setdefaultencoding('utf8')   
account = "720e9000-4fd4-4bab-b8fa-139e5d0d0080"
socket.setdefaulttimeout(2)

class MyEncoder(json.JSONEncoder):
    """ 继承自simplejson的编码基类，用于处理复杂类型的编码
    """
    def default(self,obj):
            if isinstance(obj,QuerySet):
                return json.loads(serialize('json',obj))
            if isinstance(obj,models.Model):
                return json.loads(serialize('json',[obj])[1:-1])
            if hasattr(obj, 'isoformat'):
                #处理日期类型
                return obj.isoformat()
            return json.JSONEncoder.default(self,obj)

def jsonBack(json):
    if json[0] == '[':
        return deserialize('json',json)
    else:
        return deserialize('json','[' + json +']')

def getJson(**args):
    result = dict(args)
    return json.dumps(result,cls=MyEncoder)

def GetChoicesValus(TypeChoices):
    listValues=['全部']
    for Choices in TypeChoices:       
        listValues.append(Choices[0])
    return listValues

def GetChoicesValus2(TypeChoices):
    listValues=['全部']
    for Choices in TypeChoices:       
        listValues.append(Choices.values()[0])
    return listValues

def GetSelectChoicesValus(TypeChoices):
    listValues=[]
    for Choices in TypeChoices:       
        listValues.append(Choices[0])
    return listValues

def handle_uploaded_file(f, name=""):
    file_name = ""

    try:
        path=settings.UPLOAD_DIR
        if not os.path.exists(path):
            os.makedirs(path)
        if name !="":
            oldname = name
        else:
            oldname = os.path.splitext(f.name)[0]
        ext = os.path.splitext(f.name)[1]
            
        #定义文件名，年月日时分秒随机数
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%d' % random.randint(0,100)
        #重写合成文件名
        newname =oldname+fn + ext
        file_name = path + newname
        #print file_name
        destination = open(file_name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
    except Exception, e:
        print e

    return oldname,newname

def check_Predestal(pbstat):
    checkerStatus = (2,3,4,5,6,7,10,11)
    for stat in checkerStatus:
        if stat==pbstat.id :
            return True

    return False

def add_months(dt,months):
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = calendar.monthrange(year,month)[1]
    return dt.replace(year=year, month=month, day=day)

def del_months(dt,months):
    month = dt.month - 1 - months-12
    
    year = dt.year - (-month) / 12
    if month==-12:
        year = dt.year
    
    month = month % 12 + 1
    day = calendar.monthrange(year,month)[1]
    return dt.replace(year=year, month=month, day=day)

def prev_month_start(date):
    return (date.replace(day=1) - datetime.timedelta(1)).replace(day=1)

def month_end(date):
    import calendar
    return date.replace(day = calendar.monthrange(date.year, date.month)[1])

def calDate(cur, previous):
    if cur.month > previous:
        tgtYear = cur.year
        tgtMon = cur.month - previous
    else:
        tgtYear = cur.year - 1
        tgtMon = cur.month + 12 - previous
        
    tgtDay = calendar.monthrange(tgtYear, tgtMon)[1]
    tgtStart = datetime.date(tgtYear, tgtMon, 1)
    tgtEnd = datetime.date(tgtYear, tgtMon, tgtDay)
    
    return tgtStart, tgtEnd

def calPlanTask(dt):
    return

def checkMobile(request):
    import re
    userAgent = request.META['HTTP_USER_AGENT']
 
    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'
    _short_matches = re.compile(_short_matches, re.IGNORECASE)
 
    if _long_matches.search(userAgent) != None:
        return True
    user_agent = userAgent[0:4]
    if _short_matches.search(user_agent) != None:
        return True
    return False     

def updateCom():
    for eachPrj in Project.objects.filter(company=None):
        if not BuildingCompany.objects.filter(name = eachPrj.GCGS) and eachPrj.GCGS:
            newCom = BuildingCompany.objects.create(name = eachPrj.GCGS)
            eachPrj.company = newCom
            eachPrj.save()
            
        else:
            eachPrj.company = BuildingCompany.objects.filter(name = eachPrj.GCGS)[0]
            eachPrj.save()
# 
# def updateProject():
#     for  tgtFA in JSFA.objects.filter(Q(PrjSys=None) | Q(engineering=None)):          
#         if Project.objects.filter(PrjId = tgtFA.PrjId):
#             tgtFA.PrjSys_id=Project.objects.get(PrjId = tgtFA.PrjId).id
#             
#             if Engineering.objects.filter(name = "单位工程1_" + tgtFA.PrjName):
#                 tgtFA.engineering=Engineering.objects.get(name = "单位工程1_" + tgtFA.PrjName)
#             else:
#                 tgtUnit = Engineering.objects.create(name = "单位工程1_" + tgtFA.PrjName, project = Project.objects.get(PrjId = tgtFA.PrjId))
#                 tgtFA.engineering = tgtUnit
#             
#             tgtFA.save()
#             
#         else:
#             newPrj = Project.objects.create(PrjId = tgtFA.PrjId, 
#                 PrjName = tgtFA.PrjName,
#                 GCGS = tgtFA.GCGS,
#                 GCGSID = tgtFA.GCGSID, 
#                 XMGCS = tgtFA.xmgcs, 
#                 XMJL = tgtFA.xmjl, 
#              )
# 
#             tgtFA.PrjSys = newPrj
# 
#             tgtUnit = Engineering.objects.create(name = "单位工程1_" + tgtFA.PrjName, project = newPrj)
#             tgtFA.engineering = tgtUnit
#             
#             tgtFA.save()

# def initPrj():
#     tree = ET.parse('./Projects/initFile/zjxm.xml')
#     root = tree.getroot()
#     for child in root:
#         print child.attrib["FABH"]
#     pass 

def getPrjInfo1():
    ''' 获取项目立项信息    '''
    SoapMessage ='''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <getPrjInfo xmlns="http://tempuri.org/">
      <Account>720e9000-4fd4-4bab-b8fa-139e5d0d0080</Account>
    </getPrjInfo>
  </soap:Body>
</soap:Envelope>'''
    try:
        #使用的WebService地址为sdk.entinfo.cn:8061/webservice.asmx，
        webservice = httplib.HTTP("116.236.180.116:44")
        #连接到服务器后的第一个调用。它发送由request字符串到到服务器
        webservice.putrequest("POST", "/WS_Tech/Webservice_Tech.asmx")
        webservice.putheader("Host", "116.236.180.116")
    #     webservice.putheader("User-Agent", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)")
        webservice.putheader("Content-type", "text/xml")
        webservice.putheader("Content-Length", len(SoapMessage) )
        webservice.putheader("SOAPAction", '"http://tempuri.org/getPrjInfo"')
        #发送空行到服务器，指示header的结束
        webservice.endheaders()
        #发送报文数据到服务器
        webservice.send(SoapMessage)
        #获取返回HTTP 响应信息
    
        statuscode, statusmessage, header = webservice.getreply()
        resmessage = webservice.getfile().read()
        
        OutXml = unicode(base64.b64decode(resmessage[resmessage.find('<getPrjInfoResult>') + 18 :resmessage.find('</getPrjInfoResult>')]), "gbk")
        
        root = ET.fromstring(OutXml.encode("utf-8","ignore")) 
        for child in root:
            if child.attrib:
                try:                   
                    if Project.objects.filter(PrjId=child.attrib["PrjId"]):
                        Project.objects.filter(PrjId=child.attrib["PrjId"]).update(**child.attrib)
                        pass
                    else:
                        print 1
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

import urllib2,traceback,json
def getPrjInfo():
    try:
        req = urllib2.Request("http://www.wufea.com/scg4/prjinfotodaily.asp?dcount=sihttst8Z3eKar3rUrrm") 
        #enable cookie 
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor()) 
        response = opener.open(req)
        body = json.loads(response.read().decode('gbk').encode('utf8'))
        for prj in body['prjinfotodaily']:
            myprj = {}
            for key in prj:
                if key=='mj':
                    myprj['area'] = prj[key]
                elif key=='zj':
                    myprj['price'] = prj[key]
                elif key=='dtsl':
                    myprj['danti_nums'] = prj[key]
                elif key=='aqmb':
                    myprj['safe_target'] = prj[key]
                elif key=='zlmb':
                    myprj['quality_target'] = prj[key]
                elif key=='hbmb':
                    myprj['environment_target'] = prj[key]
                elif key=='xmmb':
                    myprj['project_target'] = prj[key]
                elif key=='wmmb':
                    myprj['culture_target'] = prj[key]
                elif key=='htmb':
                    myprj['pact_target'] = prj[key]
                elif key=='sd':
                    myprj['deep'] = prj[key]
                elif key=='gd':
                    myprj['height'] = prj[key]
                elif key=='xmjd':
                    myprj['longitude'] = prj[key]
                elif key=='xmwd':
                    myprj['latitude'] = prj[key]
                elif key=='KGRQ' or key=='JGRQ':
                    if prj[key]:
                        myprj[key] = prj[key]
                else:
                    myprj[key] = prj[key]
            if Project.objects.filter(PrjId=myprj['PrjId']).count():
                print u'更新Project信息',myprj
                apply(Project.objects.filter(PrjId=myprj['PrjId']).update, (), myprj)
            elif myprj['PrjId']:
                print u'创建Project',myprj
                apply(Project.objects.create, (), myprj)
    except:
        traceback.print_exc()


# def getJSFA():
#     '''  获取施工方案  '''
#     SoapMessage ='''<?xml version="1.0" encoding="utf-8"?>
# <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
#   <soap:Body>
#     <getSGFA xmlns="http://tempuri.org/">
#         <Account>720e9000-4fd4-4bab-b8fa-139e5d0d0080</Account>
#     </getSGFA>
#   </soap:Body>
# </soap:Envelope>'''
#     try:
#         print "update JSFA" 
#         #使用的WebService地址为sdk.entinfo.cn:8061/webservice.asmx，
#         webservice = httplib.HTTP("116.236.180.116:44")
#         #连接到服务器后的第一个调用。它发送由request字符串到到服务器
#         webservice.putrequest("POST", "/WS_Tech/Webservice_Tech.asmx")
#         webservice.putheader("Host", "116.236.180.116")
#     #     webservice.putheader("User-Agent", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)")
#         webservice.putheader("Content-type", "text/xml")
#         webservice.putheader("Content-Length", len(SoapMessage) )
#         webservice.putheader("SOAPAction", '"http://tempuri.org/getSGFA"')
#         #发送空行到服务器，指示header的结束
#         webservice.endheaders()
#         #发送报文数据到服务器
#         webservice.send(SoapMessage)
#         #获取返回HTTP 响应信息
#     
#         statuscode, statusmessage, header = webservice.getreply()
#         resmessage = webservice.getfile().read()
#         
#         OutXml = unicode(base64.b64decode(resmessage[resmessage.find('<getSGFAResult>') + 15 :resmessage.find('</getSGFAResult>')]), "gbk")
#         
#         root = ET.fromstring(OutXml.encode("utf-8","ignore"))  
#         for child in root:
#             if child.attrib:
#                 try:                   
#                     if JSFA.objects.filter(FABH=child.attrib["FABH"]):
#                         JSFA.objects.filter(FABH=child.attrib["FABH"]).update(**child.attrib)
#                     else:
#                         JSFA.objects.create(**child.attrib)
#  
#                 except:
#                     traceback.print_exc()
#                     continue
#         
#         print "update Projects" 
#         updateProject()
#     
#         print "update Company" 
#         updateCom()
#                
#         return True
#     except:
#         traceback.print_exc()
#         return False
# 
# def getSGFAWFStatus(faid): 
#     ''' 获取指定施工方案的流程审批状态 '''   
#     SoapMessage ='''<?xml version="1.0" encoding="utf-8"?>
# <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
#   <soap:Body>
#     <getSGFAWFStatus xmlns="http://tempuri.org/">
#       <Account>''' + account +'''</Account>
#       <FAID>'''+ str(faid) +'''</FAID>
#     </getSGFAWFStatus>
#   </soap:Body>
# </soap:Envelope>'''
#     try:
#         #使用的WebService地址为sdk.entinfo.cn:8061/webservice.asmx，
#         webservice = httplib.HTTP("116.236.180.116:44")
#         #连接到服务器后的第一个调用。它发送由request字符串到到服务器
#         webservice.putrequest("POST", "/WS_Tech/Webservice_Tech.asmx")
#         webservice.putheader("Host", "116.236.180.116")
#     #     webservice.putheader("User-Agent", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)")
#         webservice.putheader("Content-type", "text/xml")
#         webservice.putheader("Content-Length", len(SoapMessage) )
#         webservice.putheader("SOAPAction", '"http://tempuri.org/getSGFAWFStatus"')
#         #发送空行到服务器，指示header的结束
#         webservice.endheaders()
#         #发送报文数据到服务器
#         webservice.send(SoapMessage)
#         #获取返回HTTP 响应信息
#     
#         statuscode, statusmessage, header = webservice.getreply()
#         resmessage = webservice.getfile().read()
#         OutXml = unicode(base64.b64decode(resmessage[resmessage.find('<getSGFAWFStatusResult>') + 23 :resmessage.find('</getSGFAWFStatusResult>')]), "gbk")
#         root = ET.fromstring(OutXml.encode("utf-8","ignore"))  
#         for child in root:
#             if child.attrib:    
#                 return child.attrib["FlowCurrTaskName"] + "-" + child.attrib["FlowArriveTime"]
#             
#         return "暂无记录"     
#     except:
#         traceback.print_exc()
#         return "暂无记录"
# 
#     return "暂无记录"

def getSGFAWFDealInfo(faid):
    ''' 获取指定施工方案的流程意见 '''   
    SoapMessage ='''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <getSGFAWFDealInfo xmlns="http://tempuri.org/">
      <Account>''' + account +'''</Account>
      <FAID>'''+ str(faid) +'''</FAID>
    </getSGFAWFDealInfo>
  </soap:Body>
</soap:Envelope>'''
    try:
        spyjList = []
        #使用的WebService地址为sdk.entinfo.cn:8061/webservice.asmx，
        webservice = httplib.HTTP("116.236.180.116:44")
        #连接到服务器后的第一个调用。它发送由request字符串到到服务器
        webservice.putrequest("POST", "/WS_Tech/Webservice_Tech.asmx")
        webservice.putheader("Host", "116.236.180.116")
    #     webservice.putheader("User-Agent", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)")
        webservice.putheader("Content-type", "text/xml")
        webservice.putheader("Content-Length", len(SoapMessage) )
        webservice.putheader("SOAPAction", '"http://tempuri.org/getSGFAWFDealInfo"')
        #发送空行到服务器，指示header的结束
        webservice.endheaders()
        #发送报文数据到服务器
        webservice.send(SoapMessage)
        #获取返回HTTP 响应信息
    
        statuscode, statusmessage, header = webservice.getreply()
        resmessage = webservice.getfile().read()
        OutXml = unicode(base64.b64decode(resmessage[resmessage.find('<getSGFAWFDealInfoResult>') + 25 :resmessage.find('</getSGFAWFDealInfoResult>')]), "gbk")
        root = ET.fromstring(OutXml.encode("utf-8","ignore"))  
        
        for child in root:
            if child.attrib:    
                spyjList.append(child.attrib)
            
        return spyjList     
    except:
        traceback.print_exc()
        return []

def getSGFAWFAttachInfo(faid):
    ''' 获取指定施工方案的附件信息 '''   
    SoapMessage ='''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <getSGFAAttachment xmlns="http://tempuri.org/">
      <Account>''' + account +'''</Account>
      <FAID>'''+ str(faid) +'''</FAID>
    </getSGFAAttachment>
  </soap:Body>
</soap:Envelope>'''
    try:
        attachList = []
        #使用的WebService地址为sdk.entinfo.cn:8061/webservice.asmx，
        webservice = httplib.HTTP("116.236.180.116:44")
        #连接到服务器后的第一个调用。它发送由request字符串到到服务器
        webservice.putrequest("POST", "/WS_Tech/Webservice_Tech.asmx")
        webservice.putheader("Host", "116.236.180.116")
    #     webservice.putheader("User-Agent", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)")
        webservice.putheader("Content-type", "text/xml")
        webservice.putheader("Content-Length", len(SoapMessage) )
        webservice.putheader("SOAPAction", '"http://tempuri.org/getSGFAAttachment"')
        #发送空行到服务器，指示header的结束
        webservice.endheaders()
        #发送报文数据到服务器
        webservice.send(SoapMessage)
        #获取返回HTTP 响应信息
    
        statuscode, statusmessage, header = webservice.getreply()
        resmessage = webservice.getfile().read()
        OutXml = unicode(base64.b64decode(resmessage[resmessage.find('<getSGFAAttachment>') + 25 :resmessage.find('</getSGFAAttachment>')]), "gbk")
        root = ET.fromstring(OutXml.encode("utf-8","ignore"))  
        
        for child in root:
            if child.attrib:    
                attachList.append(child.attrib)
            
        return attachList     
    except:
        traceback.print_exc()
        return []

def fetch_ticket():
    appid = 'wx8bc33e6654583f4b' 
    mc=memcache.Client(['127.0.0.1:11211'],debug=0)
    ticket=mc.get('api_ticket')
    
    access_token = mc.get('access_token')
#    if access_token:
#        sys.stderr.write((access_token+"\n").encode('utf-8'))
    
    if not ticket or not access_token:
        tkUrl = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx8bc33e6654583f4b&secret=955d9e6e3b2f9a3e3c096664a3ddd8c6'
        
        tkReq = urllib2.Request(tkUrl)
        res_data = urllib2.urlopen(tkReq)
        access_token = json.load(res_data)['access_token']
        mc.set("access_token",access_token,4000)
        
        ticketUrl = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=' + access_token +  '&type=jsapi'
        ticketReq = urllib2.Request(ticketUrl)
        res_data = urllib2.urlopen(ticketReq)
        ticket = json.load(res_data)['ticket']
        
        mc.set("api_ticket",ticket,4000)
    
    return ticket, appid, access_token

import string
import hashlib
class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret        
        
class PaySign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'appId':'wx8e8b53472e4885bf',
            'timeStamp': self.__create_timestamp(),
            'nonceStr': self.__create_nonce_str(),
            'package': self.__create_prepay_id(),
            'signType': 'MD5',
            'paySign':self.__sign(),
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    
    def __sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret  

if __name__ == '__main__':
    getPrjInfo1()
        