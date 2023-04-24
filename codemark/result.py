import requests
import json
import codemark.firebase.database as FireDB
import codemark.secrets
import codemark.submit

db = FireDB.FirebaseDB()

def fetch(submission_code):
    
    print("Fetching your report from decentralized server!\n\n\n")

    cid = getCID(submission_code)
    if not cid:
        return
        
    content = fetch_file_from_web3storage(cid)

    if not content:
        return

    parsed_content = parseContent(content)
    if not parseContent(content):
        return

    print(parsed_content)

def parseContent(content):
    try:
        content = bytes.fromhex(content)
        content = content.decode()
        return content
    except Exception as e:
        print("ERROR :", e)

def getCID(submission_code):
    report_data = db.getdataOrderEqual("submissions", "submission_id", submission_code)

    if report_data is None:
        print("ERROR: Some issues occurred while fetching result. Run `codemark doctor` for fixing it.")
        return
    if not report_data:
        print("INVALID Submission ID")
        return
    
    return list(report_data.values())[0]['cid']


def fetch_file_from_web3storage(cid):
    url = f"https://{cid}.ipfs.w3s.link"

    try:
        response = requests.get(url)
        json_data = json.loads(response.content)
        return json_data['data']

    except requests.exceptions.ConnectionError as e:
        # Handle the "Network is unreachable" error
        print("ERROR: Network is unreachable.")
    
    except json.decoder.JSONDecodeError as e:
        print("Misconfiguration from our side. Contact support ASAP!")
    except Exception as e:
        print("ERROR :", e)
