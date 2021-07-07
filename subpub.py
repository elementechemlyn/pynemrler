import fhirclient.models.bundle as Bundle
import json
import flask
from flask import request
import requests

SUPPORTED_RESOURCES = ["DocumentReference","Organization","MessageHeader"]

NRL_LOCATION="http://localhost:8080/fhir"

def transactionify(resource_in=""):
    if not "type" in resource_in or not "entry" in resource_in:
        print("No type or entry")
        return None
    if not resource_in["type"]=="message":
        print("Type not message")
        return None
    request_template = {"method":"POST"}
    bundle = resource_in
    bundle["type"] = "transaction"
    for entry in bundle["entry"]:
        request = request_template
        request["url"] = entry["resource"]["resourceType"]
        entry["request"] = request
    print("Returning Bundle")
    return bundle

def send_transaction(bundle):
    headers = {"Accept-Charset": "utf-8",
                "Accept": "application/fhir+json",
                "Content-Type": "application/fhir+json; charset=UTF-8"
    }
    res = requests.post(NRL_LOCATION,data=bundle,headers=headers)
    return res

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "Hello NEMRL world"

@app.route('/subscriber/Bundle/<int:bundle_id>', methods=['PUT'])
def consume_event(bundle_id):
    req = request.get_json()
    transaction_bundle = transactionify(req)
    if transaction_bundle:
        transaction_json = json.dumps(transaction_bundle)
        res = send_transaction(transaction_json)
        print(res.text)
    return "done"

app.run(host='0.0.0.0')
#if __name__=="__main__":
#    json_data = ""
#    with open("messageBundleVaccine.json",encoding="utf-8") as f:
#        json_data = f.read()
#    transaction_bundle = go(json_data)
#    print(transaction_bundle)
