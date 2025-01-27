import requests
import pandas as pd
import time
from urllib.parse import quote
import os
from dotenv import load_dotenv
import logging


class api_fmcsa:
    load_dotenv()
    def __init__(self):
    
        self.url = os.getenv('URL_API_FMCSA')
        self.web_key=os.getenv('FMCSA_API_KEY')
        self.logger = logging.getLogger("app_logger")
        self.logger.setLevel(logging.DEBUG)  # Nivel general del logger
        
        # Handler para mensajes generales (INFO y superiores)
        general_handler = logging.FileHandler("general.log")
        general_handler.setLevel(logging.INFO)
        
        # Handler para errores (WARNING, ERROR, CRITICAL)
        error_handler = logging.FileHandler("errors.log")
        error_handler.setLevel(logging.WARNING)
        
        # Formato de los logs
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        general_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        
        # Agregar los handlers al logger
        self.logger.addHandler(general_handler)
        self.logger.addHandler(error_handler)


    def get_dot(self,name):
      
        namehb = quote(name)
        endpoint = f'{self.url}/name/{namehb}?webKey={self.web_key}'
        response = requests.get(endpoint)


        if response.status_code == 200:
            data = response.json()
            content = data['content']
            if len(content)>0:
                carrier = content[0]['carrier']
                return carrier['dotNumber']
            else: return 'None'
        else: return 'None'



    def search_dot(self, dot):
        endpoint = f'{self.url}/{dot}?webKey={self.web_key}'
        response = requests.get(endpoint)
        
     
        if response.status_code == 200:
            data = response.json()
           
      
            content = data['content']
            carrier = content['carrier']
            
            if isinstance(carrier['carrierOperation'],list):
                carrieropera = carrier['carrierOperation']
            else:
                carrieropera={    
                  "carrierOperationCode": None,
                    "carrierOperationDesc": None

                }

            if isinstance(carrier['censusTypeId'],list):
                census = carrier['censusTypeId']
            else:
                census={    
                'censusType':None,
                'censusTypeDesc':None,
                'censusTypeId':None,

                }

            complete_search = {
                # 'record_id':record_id,
                'dot': carrier['dotNumber'],
                'allowedToOperate': carrier['allowedToOperate'],
                'carrierOperationCode': carrieropera['carrierOperationCode'],
                'carrierOperationDesc': carrieropera['carrierOperationDesc'],
                'bipdInsuranceOnFile':carrier['bipdInsuranceOnFile'],
                'bipdInsuranceRequired':carrier['bipdInsuranceRequired'],
                'bipdRequiredAmount':carrier['bipdRequiredAmount'],
                'bondInsuranceOnFile':carrier['bondInsuranceOnFile'],
                'bondInsuranceRequired':carrier['bondInsuranceRequired'],
                'brokerAuthorityStatus':carrier['brokerAuthorityStatus'],
                'cargoInsuranceOnFile':carrier['cargoInsuranceOnFile'],
                'cargoInsuranceRequired':carrier['cargoInsuranceRequired'],
                'censusType':census['censusType'],
                'censusTypeDesc':census['censusTypeDesc'],
                'censusTypeId':census['censusTypeId'],
                'commonAuthorityStatus':carrier['commonAuthorityStatus'],
                'contractAuthorityStatus':carrier['contractAuthorityStatus'],
                'legalName':carrier['legalName'],
                'mcs150Outdated':carrier['mcs150Outdated'],
                'phyCity':carrier['phyCity'],
                'phyCountry':carrier['phyCountry'],
                'phyState':carrier['phyState'],
                "phyStreet": carrier['phyStreet'],
                "phyZipcode": carrier['phyZipcode'],
                "reviewDate": carrier['reviewDate'],
                "reviewType": carrier['reviewType'],
                "safetyRating": carrier['safetyRating'],
                "safetyRatingDate": carrier['safetyRatingDate'],
                "safetyReviewDate": carrier['safetyReviewDate'],
                "safetyReviewType": carrier['safetyReviewType'],
                "snapshotDate": carrier['snapshotDate'],
                "statusCode": carrier['statusCode'],
                "totalDrivers": carrier['totalDrivers'],
                "totalPowerUnits": carrier['totalPowerUnits'],
                "vehicleInsp": 0,
                "vehicleOosInsp": carrier['vehicleOosInsp'],
                "vehicleOosRate": carrier['vehicleOosRate'],
                "vehicleOosRateNationalAverage": carrier['vehicleOosRateNationalAverage'],
                # "companynamehb":company_name,
                # "phonenumberhb":phone_number,
                # "mc":mc,
                # 'prefix':prefix

            }

            
            return complete_search
        else:
            
            print(f"Error: {response.status_code}")
            print(endpoint)
            return {
                # 'record_id':record_id,
                'dot': None,
                'allowedToOperate': None,
                'carrierOperationCode': None,
                'carrierOperationDesc': None,
                'bipdInsuranceOnFile': None,
                'bipdInsuranceRequired': None,
                'bipdRequiredAmount': None,
                'bondInsuranceOnFile': None,
                'bondInsuranceRequired': None,
                'brokerAuthorityStatus': None,
                'cargoInsuranceOnFile': None,
                'cargoInsuranceRequired': None,
                'censusType': None,
                'censusTypeDesc': None,
                'censusTypeId': None,
                'commonAuthorityStatus': None,
                'contractAuthorityStatus': None,
                'legalName': None,
                'mcs150Outdated': None,
                'phyCity': None,
                'phyCountry': None,
                'phyState': None,
                'phyStreet': None,
                'phyZipcode': None,
                'reviewDate': None,
                'reviewType': None,
                'safetyRating': None,
                'safetyRatingDate': None,
                'safetyReviewDate': None,
                'safetyReviewType': None,
                'snapshotDate': None,
                'statusCode': None,
                'totalDrivers': None,
                'totalPowerUnits': None,
                'vehicleInsp': 0,
                'vehicleOosInsp': None,
                'vehicleOosRate': None,
                'vehicleOosRateNationalAverage': None,
                'companynamehb': None,
                'phonenumberhb': None,
                'mc': None,
                'prefix': None
}

    def search_cargo_carrier(self,dot):
        endpoint = f'{self.url}/{dot}/cargo-carried?webKey={self.web_key}'
        response = requests.get(endpoint)
        if response.status_code == 200:
            self.print_logs(dot,response.status_code)
            data = response.json()
            
            
            cargo_carrier=data['content']
            # print("-----------------------")
            # print(cargo_carrier)
            if(len(cargo_carrier)>0):
                # Authority=cargo_carrier[0]['carrierAuthority']
                return cargo_carrier
            else: return [
                     {
                    "cargoClassDesc": '',
                    "id": {
                        "cargoClassId": None,
                        "dotNumber": None
                     },
                     'statusCode':response.status_code}]
        else:
            self.print_logs(dot,response.status_code)
            
            
            return [
                     {
                    "cargoClassDesc": '',
                    "id": {
                        "cargoClassId": None,
                        "dotNumber": None
                     },
                     'statusCode':response.status_code}
                     ]
        

    def print_logs(self,dot,status_code):
        if status_code == 200:
            self.logger.info(f"La busqueda del DOT: {dot} se realizo con exito")
        else:
            self.logger.error(f"La busqueda del DOT: {dot} no se realizo con exito. status code: {status_code}")
        
    def operation_classification(self,dot):
        endpoint = f'{self.url}/{dot}/operation-classification?webKey={self.web_key}'
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
           
            
            op_carrier=data['content']
            print("-----------------------")
           
            if(len(op_carrier)>0):
               
                return op_carrier
            else: return [
                     {
                    "operationClassDesc": '',
                    "id": {
                        "operationClassId": None,
                        "dotNumber": None
                     }}]
        else: return [
                     {
                    "operationClassDesc": '',
                    "id": {
                        "operationClassId": None,
                        "dotNumber": None
                     }}]
        

    def search_mc(self,dot):
        endpoint = f'{self.url}/{dot}/authority?webKey={self.web_key}'
        response = requests.get(endpoint)

        if response.status_code == 200:
            data = response.json()
            carrierAuthority=data['content']
            if(len(carrierAuthority)>0):
                Authority=carrierAuthority[0]['carrierAuthority']
                return Authority
            else: return {
                        "applicantID": None,
                        "authority": None,
                        "authorizedForBroker": None,
                        "authorizedForHouseholdGoods": None,
                        "authorizedForPassenger": None,
                        "authorizedForProperty": None,
                        "brokerAuthorityStatus": None,
                        "commonAuthorityStatus": None,
                        "contractAuthorityStatus": None,
                        "docketNumber": None,
                        "dotNumber": None,
                        "prefix": None
            }    
        else: return {
                        "applicantID": None,
                        "authority": None,
                        "authorizedForBroker": None,
                        "authorizedForHouseholdGoods": None,
                        "authorizedForPassenger": None,
                        "authorizedForProperty": None,
                        "brokerAuthorityStatus": None,
                        "commonAuthorityStatus": None,
                        "contractAuthorityStatus": None,
                        "docketNumber": None,
                        "dotNumber": None,
                        "prefix": None
            } 



    def search_name(self,name,phone_number,mc,company_name,prefix,record_id):
        namehb = quote(name)
        endpoint = f'{self.url}/name/{namehb}?webKey={self.web_key}'
        response = requests.get(endpoint)

        if response.status_code == 200:
            data = response.json()
            content = data['content']

            if len(content)>0:

                carrier = content[0]['carrier']
            
                if isinstance(carrier['carrierOperation'],list):
                    carrieropera = carrier['carrierOperation']
                else:
                    carrieropera={    
                    "carrierOperationCode": None,
                        "carrierOperationDesc": None

                    }

                if isinstance(carrier['censusTypeId'],list):
                    census = carrier['censusTypeId']
                else:
                    census={    
                    'censusType':None,
                    'censusTypeDesc':None,
                    'censusTypeId':None,

                    }

                complete_search = {
                    'record_id':record_id,
                    'dot': carrier['dotNumber'],
                    'allowedToOperate': carrier['allowedToOperate'],
                    'carrierOperationCode': carrieropera['carrierOperationCode'],
                    'carrierOperationDesc': carrieropera['carrierOperationDesc'],
                    'bipdInsuranceOnFile':carrier['bipdInsuranceOnFile'],
                    'bipdInsuranceRequired':carrier['bipdInsuranceRequired'],
                    'bipdRequiredAmount':carrier['bipdRequiredAmount'],
                    'bondInsuranceOnFile':carrier['bondInsuranceOnFile'],
                    'bondInsuranceRequired':carrier['bondInsuranceRequired'],
                    'brokerAuthorityStatus':carrier['brokerAuthorityStatus'],
                    'cargoInsuranceOnFile':carrier['cargoInsuranceOnFile'],
                    'cargoInsuranceRequired':carrier['cargoInsuranceRequired'],
                    'censusType':census['censusType'],
                    'censusTypeDesc':census['censusTypeDesc'],
                    'censusTypeId':census['censusTypeId'],
                    'commonAuthorityStatus':carrier['commonAuthorityStatus'],
                    'contractAuthorityStatus':carrier['contractAuthorityStatus'],
                    'legalName':carrier['legalName'],
                    'mcs150Outdated':carrier['mcs150Outdated'],
                    'phyCity':carrier['phyCity'],
                    'phyCountry':carrier['phyCountry'],
                    'phyState':carrier['phyState'],
                    "phyStreet": carrier['phyStreet'],
                    "phyZipcode": carrier['phyZipcode'],
                    "reviewDate": carrier['reviewDate'],
                    "reviewType": carrier['reviewType'],
                    "safetyRating": carrier['safetyRating'],
                    "safetyRatingDate": carrier['safetyRatingDate'],
                    "safetyReviewDate": carrier['safetyReviewDate'],
                    "safetyReviewType": carrier['safetyReviewType'],
                    "snapshotDate": carrier['snapshotDate'],
                    "statusCode": carrier['statusCode'],
                    "totalDrivers": carrier['totalDrivers'],
                    "totalPowerUnits": carrier['totalPowerUnits'],
                    "vehicleInsp": 0,
                    "vehicleOosInsp": carrier['vehicleOosInsp'],
                    "vehicleOosRate": carrier['vehicleOosRate'],
                    "vehicleOosRateNationalAverage": carrier['vehicleOosRateNationalAverage'],
                    "companynamehb":company_name,
                    "phonenumberhb":phone_number,
                    "mc":mc,
                    'prefix':prefix

                }

            
                return complete_search
            else:
                return {
                'record_id':record_id,
                'dot': None,
                'allowedToOperate': None,
                'carrierOperationCode': None,
                'carrierOperationDesc': None,
                'bipdInsuranceOnFile': None,
                'bipdInsuranceRequired': None,
                'bipdRequiredAmount': None,
                'bondInsuranceOnFile': None,
                'bondInsuranceRequired': None,
                'brokerAuthorityStatus': None,
                'cargoInsuranceOnFile': None,
                'cargoInsuranceRequired': None,
                'censusType': None,
                'censusTypeDesc': None,
                'censusTypeId': None,
                'commonAuthorityStatus': None,
                'contractAuthorityStatus': None,
                'legalName': None,
                'mcs150Outdated': None,
                'phyCity': None,
                'phyCountry': None,
                'phyState': None,
                'phyStreet': None,
                'phyZipcode': None,
                'reviewDate': None,
                'reviewType': None,
                'safetyRating': None,
                'safetyRatingDate': None,
                'safetyReviewDate': None,
                'safetyReviewType': None,
                'snapshotDate': None,
                'statusCode': None,
                'totalDrivers': None,
                'totalPowerUnits': None,
                'vehicleInsp': 0,
                'vehicleOosInsp': None,
                'vehicleOosRate': None,
                'vehicleOosRateNationalAverage': None,
                'companynamehb': None,
                'phonenumberhb': None,
                'mc': None,
                'prefix': None
}


        else:
            
            print(f"Error: {response.status_code}")
            print(endpoint)
            return {
                'record_id':record_id,
                'dot': None,
                'allowedToOperate': None,
                'carrierOperationCode': None,
                'carrierOperationDesc': None,
                'bipdInsuranceOnFile': None,
                'bipdInsuranceRequired': None,
                'bipdRequiredAmount': None,
                'bondInsuranceOnFile': None,
                'bondInsuranceRequired': None,
                'brokerAuthorityStatus': None,
                'cargoInsuranceOnFile': None,
                'cargoInsuranceRequired': None,
                'censusType': None,
                'censusTypeDesc': None,
                'censusTypeId': None,
                'commonAuthorityStatus': None,
                'contractAuthorityStatus': None,
                'legalName': None,
                'mcs150Outdated': None,
                'phyCity': None,
                'phyCountry': None,
                'phyState': None,
                'phyStreet': None,
                'phyZipcode': None,
                'reviewDate': None,
                'reviewType': None,
                'safetyRating': None,
                'safetyRatingDate': None,
                'safetyReviewDate': None,
                'safetyReviewType': None,
                'snapshotDate': None,
                'statusCode': None,
                'totalDrivers': None,
                'totalPowerUnits': None,
                'vehicleInsp': 0,
                'vehicleOosInsp': None,
                'vehicleOosRate': None,
                'vehicleOosRateNationalAverage': None,
                'companynamehb': None,
                'phonenumberhb': None,
                'mc': None,
                'prefix': None
}











