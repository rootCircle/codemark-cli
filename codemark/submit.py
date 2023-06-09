import codemark.check
import re
import os
from datetime import datetime
import hashlib
import requests
import json
import codemark.firebase.database as FireDB
import codemark.utils
from codemark.utils import print_info, print_error, print_success, print_message
import codemark.secrets
import codemark.initialise
import codemark.account

comment_re = re.compile(r"([\/][*](.|\n)*[*][\/])|([\/]{2}.*$)", re.MULTILINE)
include_re = re.compile(r"#include.*")
variable_re = re.compile(r"\b(long long int|short int|long long|long int|int|char|float|long|short) ([a-zA-Z_0-9]*)[\,]?[ ]?([a-zA-Z_0-9]*)?")

db = FireDB.FirebaseDB()

IPFS_FILE_NAME = "ResultReport.txt"
#TODO: Add glot.io API for cloud testing for users not having the compilers 
"""
BUG: If one user logout and user from other user logs in, then assignment not assigned to him can too be submitted
"""

def submit(force):
    if not force:
        print_info("Checking Code")
        success, total = codemark.check.checkCode(byPassMAXCheck=True)
        generate_report_and_push(success, total)
    else:
        generate_report_and_push(0, 0, force)


def generate_hash():
    print_info("Generating Hash")
    # Generate a random string
    rand_str = os.urandom(16).hex()

    # Get the current timestamp in microseconds
    timestamp = str(int(datetime.now().timestamp() * 1000000))

    # Combine the random string and timestamp
    data = rand_str + timestamp

    # Hash the combined data using SHA-256
    hashed_val = hashlib.sha256(data.encode()).hexdigest()

    return hashed_val


def generate_report_and_push(success, total, force = False):
    filename = codemark.utils.smartGetFileName()
    assgn_data = codemark.utils.readJSONFile("config.json")

    if filename and assgn_data:
        student_data = codemark.utils.readJSONFile(codemark.initialise.ACCOUNT_DATA_LOC)
        if not student_data:
            print_error("Some issues occurred while submitting. Run `codemark doctor` for fixing it.")
            return False

        print_info("Logging In")
        email = student_data['email']
        password = codemark.account.getPasswordFromKeyring(email)
        if not password:
            print_error("Some issues occurred while submitting. Run `codemark doctor` for fixing it.")
            return False

        login_cred = db.login(email,password)
        if not login_cred:
            print_error("Some issues occurred while submitting. Run `codemark doctor` for fixing it.")
            return False

        print_info("Generating Result & Plag Report")
        report, cf = generate_report(filename, assgn_data['assignment_id'], success, total, student_data['student_id'])
        
        if not force:
            print_info("Sending data to Web3 Storage")
            cid = sendTOIPFS(report)
            if not cid:
                print_error("Some issues occurred while submitting. Run `codemark doctor` for fixing it.")
                return False
        else:
            cid = ""
            
        submission_id = generate_hash()
        if not submission_id:
            print_error("Some issues occurred while submitting. Run `codemark doctor` for fixing it.")
            return False
            
        print_info("Sending file to Cloud")
        cloud_url = db.sendDataStorage(filename, submission_id + filename)
        if not cloud_url:
            print_error("Some issues occurred while submitting. Run `codemark doctor` for fixing it.")
            return False


        details = {
            "submission_id": submission_id,
            "student_id": student_data["student_id"],
            "assignment_id": assgn_data["assignment_id"],
            "submission_time": str(datetime.now()),
            "code_url": cloud_url,
            "cid": cid,
        }
        
        print_info("Logging Submission to Cloud")
        if not db.pushData("submissions", details):
            print_error("Some issues occurred while submitting. Run `codemark doctor` for fixing it.")
            return False
        
        print_info("Logging Code Hash to Cloud")
        if not writePlagCacheToCloud(assgn_data["assignment_id"], cf, student_data["student_id"]):
            print_error("Some issues occurred while submitting. Run `codemark doctor` for fixing it.")
            return False

        print_success("Submitted successfully!")
        
def writePlagCacheToCloud(assignment_id, cf, student_id):
    assgn_hash_cache = db.getdataOrderEqual("plagcache", "assignment_id", assignment_id)
    
    if assgn_hash_cache is None:
        return False

    # Pushing an empty field first
    if not assgn_hash_cache:
        details = {
            "assignment_id" : assignment_id,
            "cache" : {}
        }
        pushed_empty = db.pushData("plagcache", details)

        if pushed_empty:
            return writePlagCacheToCloud(assignment_id, cf, student_id)
        else:
            return False

    assgn_key = list(assgn_hash_cache.keys())[0]

    plag_cache = {
        "hash": cf,
        "student_id": student_id
    }

    push_data = db.pushData("plagcache/" + assgn_key + "/cache", plag_cache)
    if not push_data:
        return False
    
    return True


def generate_report(filename, assignment_id, success, total, student_id):
    details = codemark.utils.readJSONFile("config.json")

    report = ""
    report += "Generated for Assignment ID : " + assignment_id + "\n"
    report += "Title : " + details['title'] + "\n"
    report += "Batch ID: " + details['batch_id'] + "\n"
    report += "Description : " + details['description'] + "\n"
    report += "Due date : " + details['due_date'] + "\n"
    report += "Professor ID : " + details['professor_id'] + "\n"
    report += "Subject ID : " + details['subject_id'] + "\n"
    report += "Test Case Passed: " + str(success) + "\n"
    report += "Total Test Cases : " + str(total) + "\n"

    plag_percent, cf =  plagcheck(filename, assignment_id, student_id)

    report += "Plag percent as by Vansh Algo TM : " + str(plag_percent) + " %\n"
    report += "\n\nINFO : Plag percentage = -1 means the user is the first submitter to the assignment." + "\n"
    return report, cf

def sendTOIPFS(report):

    cid = upload_file_to_web3storage(codemark.secrets.web3storage_api_key, report)

    return cid


def upload_file_to_web3storage(api_token, content):
    headers = {
        'Authorization': 'Bearer ' + api_token
    }

    payload = {
        'data': content.encode().hex(),
        'name': IPFS_FILE_NAME
    }
    try:
        response = requests.post('https://api.web3.storage/upload', headers=headers, data=json.dumps(payload))
        response_json = json.loads(response.content)
        return response_json['cid']
    except requests.exceptions.ConnectionError:
        # Handle the "Network is unreachable" error
        print_error("Network is unreachable.")
 

def plagcheck(filename, assignment_id, student_id):
    precomputed_hash_cf = db.getdataOrderEqual("plagcache", "assignment_id", assignment_id)

    cf1 = generate_optimised_code(filename)
    plag_percent = 0
    
    if precomputed_hash_cf is None:
        return False, cf1
    
    if not precomputed_hash_cf:
        print_success("\n\nFirst Submitter : KUDOS!!\n\n")
        return -1, cf1

    precomputed_hash_cf = list(precomputed_hash_cf.values())

    for cache in precomputed_hash_cf:
        try:
            cached_hash = cache['cache'].values()
            for cf in cached_hash:
                if cf['student_id'] != student_id:
                    plag_percent = max(plag_percent, similarity_vansh_algo(cf1, cf['hash']))
        
        except KeyError:
            # First Submission
            plag_percent = -1

    print_message("\nPlag Percent based on Vansh Algorithm TM: " + str(plag_percent) + " %\n")

    return plag_percent, cf1

def fnv_1a(string):
    hash_value = 2166136261
    for byte in string.encode('utf-8'):
        hash_value ^= byte
        hash_value *= 16777619
    return hash_value

def generate_optimised_code(filename):
    with open(filename,"r") as f1:

        cf1=f1.read()
    
        cf1 = comment_re.sub("", cf1)
        cf1 = include_re.sub("", cf1)
    
        lf1=[]
        
        for match in variable_re.finditer(cf1):
            lf1.append(match.group(2))
            try:
                if(match.group(3)):
                    lf1.append(match.group(3))
            except Exception as e:
                pass
    
        sp1=""
        for item in lf1:
            if(item):
                sp1=sp1+item+"|"
        sp1=sp1[:-1]
    
        re1=re.compile(r"\b("+sp1+r")\b")
        cf1=re1.sub("v",cf1)
    
        cf1=cf1.replace('\n','')
        cf1=cf1.replace('\t','')
        cf1=cf1.replace(' ','')

    return cf1

def similarity_vansh_algo(cf1, cf2,k = 5):

    hf1=[]
    hf2=[]

    index=0

    while(index<len(cf1)-k):
        curr=cf1[index:index+k]
        h=fnv_1a(curr)
        hf1.append(h)
        index=index+1

    index=0

    while(index<len(cf2)-k):
        curr=cf2[index:index+k]
        h=fnv_1a(curr)
        hf2.append(h)
        index=index+1
    
    hf1.sort()
    hf2.sort()
    p1=0
    p2=0
    c=0

    while(p1<len(hf1) and p2<len(hf2)):
        if(hf1[p1]==hf2[p2]):
            c=c+1
            p1=p1+1
            p2=p2+1
        elif(hf1[p1]>hf2[p2]):
            p2=p2+1
        else:
            p1=p1+1
    d=len(hf1)+len(hf2)-c  
    percent=c/d*100

    return round(percent, 2)
