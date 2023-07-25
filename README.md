This service is able to receive BIOMED clinical data and raw clinical text and to write output to the Azure  FHIR API. 

# Config
There are 3 preconfigured environment profiles (test, development, production):
`FLASK_ENV=development`
	
Connection to Azure FHIR API is provided by getting access token from 'https://login.microsoftonline.com/' by using these parameters as environment variables:

`TENANT_ID=...`

`CLIENT_ID=...`

`CLIENT_SECRET=...`

`AZURE_USERNAME=fhir_user@yoursite.onmicrosoft.com`

`PASSWORD=....`

`API_URL=https://text2phenotype.azurehealthcareapis.com/`

These parameters are also configurable in config.json

Access to FHIR resources is provided by using url: https://text2phenotype.azurehealthcareapis.com/

# FHIR Adapter Service
This project is based on Flask API and used flask-api-spec for automatically generating docs and Swagger markup. (http://localhost:5000/docs)

# Usage

Before running FHIR Adapter ensure that BIOMED is started.
To run FHIR Adapter for dev you need to execute `python fhirhydrant.fhir_server` with environmental variable FLASK_ENV. There are 2 values in which FLASK_ENV can be set: 'development' and 'test'.
For now FHIR Adapter is not ready for production.
