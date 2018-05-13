# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import logging
import traceback

from ccmapp import models
from ccmapp.samplemgr.retriever import ProjectRetriever, ContractRetriever, SampleRetriever, UserInfoRetriever

logger = logging.getLogger(__name__)


class Sync(object):
    def __init__(self):
        self.project_retriever = ProjectRetriever()
        self.contract_retriever = ContractRetriever()
        self.sample_retriever = SampleRetriever()
        self.user_info_retriever = UserInfoRetriever()

    @staticmethod
    def _get_raw_data(rep):
        if rep['code'] == 200 and len(rep['result']['content']) > 0:
            return rep['result']['content']
        if rep['code'] != 200:
            raise Exception("retriever returned error code %d: %s" % (rep['code'], str(rep)))

    def sync(self):
        start_time = time.time()
        logger.info("Sync %Ld started." % start_time)
        self._building_company_users_sync()
        building_companies = models.BuildingCompany.objects.filter(disabled=False)
        logger.info("Got %s building companies." % len(building_companies))
        for building_company in building_companies:
            self._do_sync(building_company)
        logger.info("Sync %Ld ended, cost %Ld seconds\n\n" % (start_time, time.time() - start_time))

    def _building_company_users_sync(self):
        """
        同步工程公司用户，并关联工程公司用户到工程公司
        :return:
        """
        logger.info("Sync for building company users")
        building_company_users = models.BuildingCompanyUser.objects.filter(disabled=False)
        if len(building_company_users) == 0:
            logger.error("Not find build company user!")
        for building_company_user in building_company_users:
            try:
                updated_building_company_user = False
                # 还没有instance_id, 同步instance_id
                if not building_company_user.instance_id:
                    raw_data = self._get_raw_data(self.user_info_retriever.retrieve(building_company_user.login_name))
                    if raw_data:
                        logger.info("UserId %s", raw_data[0]['UserId'])
                        building_company_user.instance_id = raw_data[0]["UserId"]
                        updated_building_company_user = True
                    else:
                        logger.error("User %s is invalid. continue to next user" % building_company_user.login_name)
                        continue

                # 还没有关联工程公司, 同步所属工程公司并与之关联 (需要获取合同信息才能得到所属工程公司的信息)
                if not building_company_user.building_company_id:
                    raw_data = self._get_raw_data(self.project_retriever.retrieve(
                        page_num=1, build_unit_user_id=building_company_user.instance_id))
                    logger.debug("Got project raw data for user %s: %s", building_company_user.login_name, raw_data)

                    if raw_data is None:
                        logger.error("Project info for user %s is None", building_company_user.login_name)

                    if raw_data:
                        intrested_keys = ['_Id', '_ProjectName', '_ProjectNo', '_BuildingReportNumber']

                        for i, d in enumerate(raw_data):
                            for k, v in d.items():
                                if k in intrested_keys:
                                    logger.debug('Project %s data k,v: %s, %s', i, k, v)

                        for project_item in raw_data:
                            contract_raw_data = self._get_raw_data(self.contract_retriever
                                                                   .retrieve(project_id=project_item["_Id"]))
                            logger.debug("Got contract data for project: %s: %s",
                                         project_item['_ProjectName'],
                                         contract_raw_data
                                         )
                            intrested_keys = ['_ProjectName', '_BuildUnitName', '_BuildingReportNumber']
                            for i, d in enumerate(contract_raw_data):

                                for k,v in d.items():
                                    if k in intrested_keys:
                                        logger.debug('Contract data k,v: %s, %s', k, v)

                            if contract_raw_data:
                                for contract_item in contract_raw_data:
                                    building_company_name = contract_item["_BuildUnitName"]
                                    logger.info("Got building company name: %s" % building_company_name)
                                    try:
                                        building_company = models.BuildingCompany.objects.get(name=building_company_name)
                                        building_company.instance_id = contract_item["_BuildUnitID"]
                                        building_company.save()
                                        building_company_user.building_company_id = building_company.id
                                        updated_building_company_user = True
                                        logger.info('Got building company info. Just break.')
                                        break
                                    except models.BuildingCompany.DoesNotExist:
                                        logger.error("Can't find building company: %s from DB", building_company_name)
                                        continue
                                logger.info("Got raw data of contract. Just beak. Like a bug.")
                                break
                if updated_building_company_user:
                    building_company_user.save()
            except Exception as e:
                exstr = traceback.format_exc()
                logger.error('Sync error for build company user %d: %s %s' %
                             (building_company_user.id, type(e), exstr))

        building_companies = models.BuildingCompany.objects.filter(instance_id=None, disabled=False)
        if len(building_companies) > 0:
            for building_company in building_companies:
                try:
                    building_company_user = models.BuildingCompanyUser.objects.get(building_company_id=building_company.id)
                    raw_data = self._get_raw_data(self.project_retriever.retrieve(
                        page_num=1, build_unit_user_id=building_company_user.instance_id))
                    if raw_data:
                        for project_item in raw_data:
                            contract_raw_data = self._get_raw_data(self.contract_retriever
                                                                   .retrieve(project_id=project_item["_Id"]))
                            logger.debug("Got contract data: %s" % contract_raw_data)
                            if contract_raw_data:
                                for contract_item in contract_raw_data:
                                    building_company_name = contract_item["_BuildUnitName"]
                                    logger.info("Got building company name: %s" % building_company_name)
                                    building_company.instance_id = contract_item["_BuildUnitID"]
                                    building_company.save()
                                    break
                                break
                except models.BuildingCompanyUser.DoesNotExist:
                    logger.error("Can't find building company user for company: %s", building_company.name)
                    continue

    def _do_sync(self, building_company):
        """
        同步工程公司下的项目、合同和试件

        :param building_company:
        :return:
        """
        logger.info("Sync for building company id: %s, name: %s" % (building_company.id, building_company.name))
        building_company_users = models.BuildingCompanyUser.objects.filter(building_company_id=building_company.id,

                                                             disabled=False)

        if len(building_company_users) == 0:
            logger.error("There is no build company user for company: %s", building_company.name)
        for building_company_user in building_company_users:
            try:
                if building_company.instance_id and building_company_user.instance_id:
                    logger.info('Sync for building company: %s', building_company.name)
                    self._projects_sync(building_company, building_company_user)
                else:
                    logger.warn("One of them is None.\n"
                                "building_company.instance_id: %s,building_company_user.instance_id: %s" %
                                (building_company.instance_id, building_company_user.instance_id))
            except Exception as e:
                exstr = traceback.format_exc()
                logger.error('Sync error: %s %s' % (type(e), exstr))

    def _projects_sync(self, building_company, building_company_user):
        """
        同步已注册到系统里的项目

        :param building_company:
        :param building_company_user:
        :return:
        """
        current_page = 1
        try:
            rep = self.project_retriever.retrieve(build_unit_id=building_company.instance_id,
                                                  page_num=current_page,
                                                  page_size=600,
                                                  build_unit_user_id=building_company_user.instance_id)
            logger.debug('Got projects response: %s', rep)
            raw_data = self._get_raw_data(rep)
            logger.info("Got project data for page 1: %s",  raw_data)
            for d in raw_data:
                for k, v in d.items():
                    logger.info("k,v: %s, %s", k, v)
            if raw_data:
                self._do_projects_sync(raw_data, building_company)
                if "page_info" in rep["result"] and "page_count" in rep["result"]["page_info"]:
                    page_count = rep["result"]["page_info"]["page_count"]
                    left_pages = page_count - 1
                    while left_pages > 1:
                        current_page += 1
                        rep = self.project_retriever.retrieve(page_num=current_page,
                                                              page_size=600,
                                                              build_unit_user_id=building_company_user.instance_id)
                        raw_data = self._get_raw_data(rep)
                        logger.info("Got project data for page: %d:%s", current_page, raw_data)
                        for d in raw_data:
                            for k,v in d.items():
                                logger.info("k,v: %s, %s", k,v )
                        if raw_data:
                            self._do_projects_sync(raw_data, building_company)
                        left_pages -= 1
        except Exception as e:
            exstr = traceback.format_exc()
            logger.error('Sync page %d of projects error: %s %s' % (current_page, type(e), exstr))

    def _do_projects_sync(self, raw_data, building_company):
        logger.info("Try to find out registered projects: %s", building_company.name)
        registered_projects = models.Project.objects.filter(company_id=building_company.id, disabled=False)
        logger.info("Registered projects: %s" % registered_projects)
        registered_projects_by_instance_id = dict([(item.instance_id, item) for item in registered_projects
                                                   if item.instance_id])
        registered_project_by_name = {}
        for item in registered_projects:
            if item.id not in registered_projects_by_instance_id.keys():
                if item.project_name:
                    registered_project_by_name[item.project_name] = item
                names = models.ProjectName.objects.filter(project_id=item.id)
                if names:
                    for name in names:
                        registered_project_by_name[name.name] = item

        for project_item in raw_data:
            pre_project_status = 0
            retrieve_name = project_item["_ProjectName"]
            retrieve_instance_id = project_item["_Id"]
            if retrieve_instance_id in registered_projects_by_instance_id.keys():
                project = registered_projects_by_instance_id[retrieve_instance_id]
            elif retrieve_name in registered_project_by_name.keys():
                project = registered_project_by_name[retrieve_name]
            else:
                continue
            logger.info("Sync project %d" % project.id)
            if project.instance_id:
                pre_project_status = project.status
                if project.instance_id != project_item["_Id"] or project.status != int(project_item["_ProjectStatus"]):
                    project.instance_id = project_item["_Id"]
                    project.status = int(project_item["_ProjectStatus"])
                    project.save()
            else:
                project.instance_id = project_item["_Id"]
                project.nature = project_item["_ProjectNature"]
                project.num = project_item["_ProjectNo"]
                project.region = project_item["_ProjectRegion"]
                project.address = project_item["_ProjectAddress"]
                project.status = project_item["_ProjectStatus"]
                project.create_time = project_item["_CreateDateTime"]
                project.last_edit_time = project_item["_LastEditDateTime"]
                project.building_company_id = building_company.id
                project.save()
            # 项目还未完成, 需要同步项目的合同和试件
            if pre_project_status == 0:
                self._contracts_sync(project)

    def _contracts_sync(self, project):
        try:
            raw_data = self._get_raw_data(self.contract_retriever.retrieve(project_id=project.instance_id))
            if raw_data:
                self._do_contracts_sync(project, raw_data)
        except Exception as e:
            exstr = traceback.format_exc()
            logger.error('Sync contracts error for project %d: %s %s' % (project.id, type(e), exstr))

    def _do_contracts_sync(self, project, raw_data):
        for contract_item in raw_data:
            try:
                contract = models.Contract.objects.get(sign_number=contract_item["_ContractSignNumber"])
            except models.Contract.DoesNotExist:
                contract = models.Contract.objects.create(sign_number=contract_item["_ContractSignNumber"],
                                                          serial_num=contract_item["_ContractSerialNumber"],
                                                          project=project,
                                                          checked_date_time=contract_item["_CheckedDateTime"],
                                                          checked=bool(contract_item["_Checked"])
                                                          )
                logger.info("Add contract %d to project %d." % (contract.id, project.id))
            logger.info("Sync samples under contract %d..." % contract.id)
            self._samples_sync(project, contract)

    def _samples_sync(self, project, contract):
        current_page = 1
        try:
            rep = self.sample_retriever.retrieve(project_id=project.instance_id,
                                                 contract_sign_number=contract.sign_number,
                                                 page_num=current_page,
                                                 page_size=600)
            raw_data = self._get_raw_data(rep)
            if raw_data:
                self._do_samples_sync(project, contract, raw_data)
                if "page_info" in rep["result"] and "page_count" in rep["result"]["page_info"]:
                    page_count = rep["result"]["page_info"]["page_count"]
                    left_pages = page_count - 1
                    while left_pages > 1:
                        current_page += 1
                        rep = self.sample_retriever.retrieve(project_id=project.instance_id,
                                                             contract_sign_number=contract.sign_number,
                                                             page_num=current_page,
                                                             page_size=600)
                        raw_data = self._get_raw_data(rep)
                        if raw_data:
                            self._do_samples_sync(project, contract, raw_data)
                        left_pages -= 1
        except Exception as e:
            exstr = traceback.format_exc()
            logger.error('Sync page %d of samples error: %s %s' % (current_page, type(e), exstr))

    def _do_samples_sync(self, project, contract, raw_data):
        for sample_item in raw_data:
            sample_status_str = sample_item['_Sample_Status']
            sample_status_int = -1
            try:
                sample_status_int = int(sample_status_str)
            except ValueError:
                pass
            sample_exam_result_str = sample_item['_Exam_Result']
            sample_exam_result_int = -1
            try:
                sample_exam_result_int = int(sample_exam_result_str.replace('%', ''))
            except ValueError:
                pass


            try:
                try:
                    sample = models.Sample.objects.get(instance_id=sample_item["_Id"])
                    if sample.exam_result != sample_exam_result_int \
                            or sample.status != sample_status_int  \
                            or sample.regular != bool(sample_item["_Sample_Regular"]):
                        sample.exam_result = sample_exam_result_int
                        sample.status = sample_status_int
                        sample.status_str = sample_status_int
                        sample.regular = bool(sample_item["_Sample_Regular"])
                        sample.save()
                except models.Sample.DoesNotExist:
                    sample = models.Sample.objects.create(instance_id=sample_item["_Id"],
                                                          name=sample_item["_SampleName"],
                                                          num=sample_item["_SampleNo"],
                                                          item_name=sample_item["_ItemName"],
                                                          project=project,
                                                          contract=contract,
                                                          count=sample_item["_SampleCount"],
                                                          status=sample_status_int,
                                                          status_str=sample_status_str,
                                                          regular=bool(sample_item["_Sample_Regular"]),
                                                          kind_name=sample_item["_KindName"],
                                                          detection_unit_member_name=sample_item["_MemberCode"],
                                                          report_num=sample_item["_ReportNumber"],
                                                          core_code_id=sample_item["_CoreCodeId"],
                                                          core_code_id_end=sample_item["_CoreCodeIdEnd"],
                                                          project_part=sample_item["_ProJect_Part"],
                                                          spec=sample_item["_SpecName"],
                                                          grade=sample_item["_GradeName"],
                                                          exam_result=sample_exam_result_int,
                                                          exam_result_str=sample_exam_result_str,
                                                          hnt_yhtj=sample_item["_Hnt_YHTJ"],
                                                          age_time_str=sample_item["_AgeTimeStr"],
                                                          report_date_str=sample_item["_ReportDateStr"],
                                                          detection_date_str=sample_item["_DetectionDateStr"],
                                                          molding_date_str=sample_item["_MoldingDateStr"]
                                                          )
            except Exception,e:
                logger.error("Exception when create/update sample %s", sample_item)
                logger.exception(e)
