import requests
import json
import codemark.firebase.database as FireDB
from codemark.utils import print_info, print_error, print_success, print_warning

db = FireDB.FirebaseDB()

def fetch(submission_code):
    
    print_info("Fetching your report from decentralized server!\n")

    cid = getCID(submission_code)
    if not cid:
        return
        
    content = fetch_file_from_web3storage(cid)

    if not content:
        return

    parsed_content = parseContent(content)
    if not parseContent(content):
        return
    print("=" * 90)
    print_success(parsed_content, prefix=False)
    print("=" * 90)

def parseContent(content):
    try:
        content = bytes.fromhex(content)
        content = content.decode()
        return content
    except Exception as e:
        print_error(e)

def getCID(submission_code):
    report_data = db.getdataOrderEqual("submissions", "submission_id", submission_code)

    if report_data is None:
        print_error("Some issues occurred while fetching result. Run `codemark doctor` for fixing it.")
        return
    if not report_data:
        print_warning("INVALID Submission ID")
        return
    
    return list(report_data.values())[0]['cid']


def fetch_file_from_web3storage(cid):
    url = f"https://{cid}.ipfs.w3s.link"

    try:
        response = requests.get(url)
        json_data = json.loads(response.content)
        return json_data['data']

    except requests.exceptions.ConnectionError:
        # Handle the "Network is unreachable" error
        print_error("Network is unreachable.")
    
    except json.decoder.JSONDecodeError:
        print_error("Misconfiguration from our side. Contact support ASAP!")
    except Exception as e:
        print_error(e)
