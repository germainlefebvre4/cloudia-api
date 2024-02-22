import boto3
import requests
import argparse
import json
from urllib.parse import urlencode
from datetime import datetime
import sys
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def extract_emissions_data(startDate, endDate, credentials):
    billing_region = 'us-east-1'

    if credentials.token is None:
        # this is most likely an IAM or root user
        exit("You seem to run this with an IAM user. Assume an account's role instead.")

    #get the account ID to include it in the response
    sts_client = boto3.client(
         'sts',
         aws_access_key_id=credentials.access_key,
         aws_secret_access_key=credentials.secret_key,
         aws_session_token=credentials.token
    )

    accountID = sts_client.get_caller_identity()["Account"]

    # Create a new session in which all cookies are set during login
    s = requests.Session()

    aws_federated_signin_endpoint = 'https://signin.aws.amazon.com/federation'

    # Get SigninToken
    signin_token_params = {
        "Action": "getSigninToken",
        "Session": {
            "sessionId": credentials.access_key,
            "sessionKey": credentials.secret_key,
            "sessionToken": credentials.token
        }
    }
    signin_token_url = "%s?%s" % (
        aws_federated_signin_endpoint, urlencode(signin_token_params))
    signin_token_request = s.get(signin_token_url)
    signin_token = json.loads(signin_token_request.text)['SigninToken']

    # Create Login URL
    login_params = {
        "Action": "login",
        "Destination": "https://console.aws.amazon.com/",
        "SigninToken": signin_token
    }
    login_url = "%s?%s" % (aws_federated_signin_endpoint, urlencode(login_params))

    r = s.get(login_url)
    r.raise_for_status()

    # grap the xsrf token once
    r = s.get("https://console.aws.amazon.com/billing/home?state=hashArgs")
    r.raise_for_status()
    xsrf_token = r.headers["x-awsbc-xsrf-token"]

    # call the proxy via POST
    cft_request = {
        "headers": {
            "Content-Type": "application/json"
        },
        "path": "/get-carbon-footprint-summary",
        "method": "GET",
        "region": billing_region,
        "params": {
            "startDate": startDate,
            "endDate": endDate
        }
    }
    cft_headers = {
        "x-awsbc-xsrf-token": xsrf_token
    }

    try:
        r = s.post(
            "https://%s.console.aws.amazon.com/billing/rest/api-proxy/carbonfootprint" % (billing_region),
            data=json.dumps(cft_request),
            headers=cft_headers
        )
        r.raise_for_status()
        emissions = r.json()

        emissions_data = {
            "accountId": accountID,
            "query": {
                "queryDate": datetime.today().strftime("%Y-%m-%d"),
                "startDate": startDate,
                "endDate": endDate,
            },
            "emissions": emissions
        }

        # print(json.dumps(emissions_data))
        return emissions_data

    except Exception as e:
            if str(e) == "404 Client Error: Not Found for url: https://us-east-1.console.aws.amazon.com/billing/rest/api-proxy/carbonfootprint":
                raise Exception("No carbon footprint report is available for this account at this time:", accountID, "If no report is available, your account might be too new to show data. There is a delay of three months between the end of a month and when emissions data is available.")
            else:
                raise Exception("An error occured: " + str(e))
