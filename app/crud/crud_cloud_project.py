# from typing import Any, Dict, Optional, Union, List
# import boto3

# from sqlalchemy.orm import Session

# from app.core.security import get_password_hash, verify_password
# from app.crud.base import CRUDBase
# from app.models.user import User
# from app.schemas import CloudProject
# from app.schemas.user import UserCreate, UserUpdate
# import app.crud as crud

# from app.core.config import settings


# class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

#     def get_multi_remote():
#         client = boto3.client(
#             'organizations',
#             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#         )
#         res = client.aws_list_accounts()

#         accounts = []
#         # for page in page_iterator:
#         for account in res['Accounts']:
#             res = client.list_tags_for_resource(
#                 ResourceId = account['Id'],
#             )
#             tags = {res['Tags'][i]['Key']: res['Tags'][i]['Value'] for i in range(len(res['Tags']))}
#             data = CloudProject(
#                 id = account['Id'],
#                 name = account['Name'],
#                 email = account['Email'],
#                 state = account['Status'],
#                 tags = tags,
#                 created_at = account['JoinedTimestamp'],
#             )


#             accounts.append(data)

#         return accounts


# user = CRUDUser(User)
