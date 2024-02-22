from typing import Any
import boto3
from datetime import datetime
from dateutil.relativedelta import relativedelta

from app import schemas
from app.core.config import settings

from app.api.api_v1.helpers.aws_ccft import extract_emissions_data


def aws_list_accounts() -> list[schemas.CloudProject]:
    active_project = []

    client = boto3.client(
        'organizations',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    aws_accounts = client.list_accounts()

    for account in aws_accounts['Accounts']:
        res = client.list_tags_for_resource(
            ResourceId = account['Id'],
        )
        tags = {res['Tags'][i]['Key']: res['Tags'][i]['Value'] for i in range(len(res['Tags']))}
        data = schemas.CloudProject(
            id = account['Id'],
            provider = schemas.cloud_provider.AWS().slug,
            name = account['Name'],
            email = account['Email'],
            state = account['Status'],
            tags = tags,
            created_at = account['JoinedTimestamp'],
        )
        active_project.append(data)

    return active_project


def aws_get_project_billing(
    project_id: int,
    year: int,
    month: int,
) -> Any:
# ) -> schemas.CloudBillingResponse:
    date_tmp = datetime.strptime(f"{year}-{month}", "%Y-%m")
    date_partition_current_month = date_tmp.strftime("%Y-%m-%d")
    date_partition_next_month = (date_tmp + relativedelta(months=1)).strftime("%Y-%m-%d")

    cloud_billing = None
    
    client = boto3.client('ce')
    try:
        response = client.get_cost_and_usage(
            TimePeriod = {
                'Start': f'{date_partition_current_month}',
                'End': f'{date_partition_next_month}',
            },
            Filter = {
                'Dimensions': {
                    'Key': 'LINKED_ACCOUNT',
                    'Values': [
                        f'{project_id}',
                    ],
                },
            },
            Granularity = 'MONTHLY',
            Metrics = ['UnblendedCost'],
        )
        res_total = float("{:.2f}".format(float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])))
        res_unit = response['ResultsByTime'][0]['Total']['UnblendedCost']['Unit']
    except:
        res_total = None
        res_unit = None

    return schemas.CloudBillingResponse(
        project_id = project_id,
        year = year,
        month = month,
        total = res_total,
        unit = res_unit,
    )


def aws_get_project_carbon_footprint(
    project_id: int,
    year: int,
    month: int,
) -> schemas.CloudBillingResponse:
    date_tmp = datetime.strptime(f"{year}-{month}", "%Y-%m")
    date_current_month = date_tmp.strftime("%Y-%m-%d")
    date_next_month = (date_tmp + relativedelta(months=1) - relativedelta(days=1)).strftime("%Y-%m-%d")

    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    assumed_role_object = session.client('sts').assume_role(
        RoleArn=f"arn:aws:iam::{project_id}:role/cloudia-read-role",
        RoleSessionName="cloudia-read-role",
    )
    credentials = assumed_role_object['Credentials']
    session = boto3.Session(
        aws_access_key_id=assumed_role_object['Credentials']['AccessKeyId'],
        aws_secret_access_key=assumed_role_object['Credentials']['SecretAccessKey'],
        aws_session_token=assumed_role_object['Credentials']['SessionToken'],
    )
    credentials = session.get_credentials()

    try:
        result = extract_emissions_data(date_current_month, date_next_month, credentials)
    except Exception as e:
        # logging.warning(" ".join(e.args))
        pass

    if len(result['emissions']['carbonEmissionEntries']) == 0:
        emissions_carbonEmissionEntries = None
    else:
        emissions_carbonEmissionEntries = "{:.2f}".format(float(result['emissions']['carbonEmissionEntries'][0]['mbmCarbon'])/1000)

    return schemas.CloudCarbonFootprintResponse(
        project_id = project_id,
        year = year,
        month = month,
        total = emissions_carbonEmissionEntries,
    )

def aws_get_account_details(
    project_id: int,
) -> schemas.CloudProject:
    client = boto3.client(
        'organizations',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    aws_account = client.describe_account(
        AccountId = str(project_id),
    )

    return schemas.CloudProject(
        id = aws_account['Account']['Id'],
        provider = schemas.cloud_provider.AWS().slug,
        name = aws_account['Account']['Name'],
        email = aws_account['Account']['Email'],
        state = aws_account['Account']['Status'],
        tags = None,
        created_at = aws_account['Account']['JoinedTimestamp'],
        additionals = {
            'arn': aws_account['Account']['Arn'],
            'joined_method': aws_account['Account']['JoinedMethod'],
        },
    )
