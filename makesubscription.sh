#!/bin/bash

curl -X POST -H "Content-Type:application/fhir+json; charset=UTF-8" --data "@examplesubscription.json" http://localhost:8080/fhir/Subscription
