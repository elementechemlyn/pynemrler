import fhirclient.models.bundle as Bundle
import json
import flask
from flask import request

SUPPORTED_RESOURCES = ["DocumentReference","Organization","MessageHeader"]

def go(resource_in=""):
    request_template = {"method":"POST"}
    bundle =json.loads(resource_in)
    bundle["type"] = "transaction"
    for entry in bundle["entry"]:
        request = request_template
        request["url"] = entry["resource"]["resourceType"]
        entry["request"] = request
    return json.dumps(bundle)


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/subscriber', methods=['PUT'])
def consume_event():
    req = request.get_json()
    print(req)
    
app.run()
#if __name__=="__main__":
#    json_data = ""
#    with open("messageBundleVaccine.json",encoding="utf-8") as f:
#        json_data = f.read()
#    transaction_bundle = go(json_data)
#    print(transaction_bundle)
