
import hashlib
import sys
import os
import json
import logging
import argparse
import traceback
from anotherclient import EducationClient
import requests

FAMILY_NAME="education"

DEFAULT_URL="http://rest-api:8008"
def _hash(data):
    return hashlib.sha512(data).hexdigest()


def run():
    args=sys.argv
      
    if  len(args)<2:
        print("Enter arguments")
        return
    

    elif args[1]=="req" : 
            try:
                
                print(args[1]+" "+args[2]+" "+args[3]) 
                
                usn=args[1]
                address=_hash(FAMILY_NAME.encode("utf-8"))[0:6]+_hash(usn.encode("utf-8"))[0:64]
                results=requests.get("http://rest-api:8008/state/address")
                
                print(results)
                j=results.json()
                
                #jv=j['abbc41f1ae75ba1d82f7b11f7112683cf954ded349aa310329078e85dc3d567c120525']
                #print(jv)
               # print(address)
                print(results.json(),results.status_code)
            except Exception as e :
                print(e)
        
            
if __name__=="__main__":
    run()




