## Steven Emrick - steve.emrick@nih.gov
## usage: python crosswalk.py -k <your-api-key>
## You can specify a specific UMLS version with the -v argument, but it is not required
## This reads a file with codes from the Human Phenotype Ontology and maps them to the US Edition of SNOMED CT through UMLS CUIs

from __future__ import print_function
from Authentication import *
import requests
import json
import argparse
import sys

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description='process user given parameters')
parser.add_argument("-k", "--apikey", required = True, dest = "apikey", help = "enter api key from your UTS Profile")
parser.add_argument("-v", "--version", required =  False, dest="version", default = "current", help = "enter version example-2015AA")

args = parser.parse_args()
apikey = args.apikey
version = args.version
AuthClient = Authentication(apikey)

###################################
#get TGT for our session
###################################

tgt = AuthClient.gettgt()
base_uri = "https://uts-ws.nlm.nih.gov"
crosswalk_endpoint = "/rest/crosswalk/"+version+"/source/MSH"

def crosswalk_code(path):
    query = {'ticket': AuthClient.getst(tgt),'targetSource': 'ICD10'}
    r = requests.get(base_uri + path, params=query)
    #print(r.url + "\n")
    items = json.loads(r.text)
    return items

f = open('../docs/mesh-codes.txt','r').readlines()
foutput = open('output/dict.txt', 'w')
for line in f:
    ##get rid of newlines
    code = line.strip()
    path =  crosswalk_endpoint+"/"+code
    try:
        results = crosswalk_code(path)
        for sourceAtomCluster in results["result"]:
            ## Create csv with MeSH and ICD10
            print(str(code) + ';', str(sourceAtomCluster["ui"]) + ';' + 
                  sourceAtomCluster["name"], file=foutput)
            #print('MESH term - ' + code+ '\t' + 'ICD10 code -- ' + sourceAtomCluster["ui"] + ': ' + sourceAtomCluster["name"])
        
    except ValueError:
        print("No result found for "+code)
        print(str(code) + ';', '' + ';' + '', file=foutput)
        pass

foutput.close()

