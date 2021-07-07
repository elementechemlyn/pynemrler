#!/bin/bash

curl -X POST -H "Content-Type:application/fhir+xml " --data "@examplebundle.xml" http://localhost:8080/fhir/Bundle
