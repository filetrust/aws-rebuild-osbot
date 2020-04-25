import boto3
from botocore.exceptions import ClientError

from gw_bot.setup.OSBot_Setup import OSBot_Setup
from osbot_aws.apis.IAM import IAM
from osbot_aws.apis.S3 import S3
from osbot_aws.helpers.IAM_Policy import IAM_Policy
from osbot_utils.decorators.Method_Wrappers import catch
from osbot_utils.utils.Files import file_not_exists
from osbot_utils.utils.Json import json_save, json_load


class CI_Setup:

    def __init__(self, aws_user='github-user', region='eu-west-2'):
        self.profile_name     = '832789828058_AdministratorAccess'      # this uses temporary tokens which expire after 12 hours (so this value will need to be reset before execution)
        self.account_id       = 'cloudsdkcustomera-glasswall'
        self.region           = region
        self.osbot_setup      = OSBot_Setup(profile_name     = self.profile_name    ,
                                            account_id       = self.account_id      ,
                                            region_name      = self.region          )
        self.aws_user              = aws_user
        self.path_temp_credentials = f'/tmp/temp_credentials_{self.aws_user}.json'
        self.iam = IAM(user_name=self.aws_user)

    def check_profile_account_security_token_status(self):
        """
        if this fails the current values set in the aws config need to be refreshed
        :return: True if credentials are ok
        """
        try:
            self.iam.account_id()
            return True
        except ClientError as error:
            assert error.response['Error']['Message'] == 'The security token included in the request is expired'
            return False

    @catch
    def check_access_key_for_user(self):
        (aws_access_key_id, aws_secret_access_key)  = self.get_access_key_for_user(new_key=False)

        #return  (aws_access_key, aws_secret)

        s3 = S3()

        return s3.buckets()

    def create_aws_user_for_github(self):

        role_name   = f'role_for_{self.aws_user}'
        #policy_name = f'policy_for_{user_name}'
        #IAM(role_name=role_name)
        #policy = IAM_Policy(policy_name=policy_name)
        self.iam.user_create()
        #iam.role_create(policy.statement())

        assert self.iam.user_exists()
        #assert iam.role_exists()

        return

    def get_access_key_for_user(self, new_key=True, delete_keys=True):
        """
        get AWS access key for current user
        :param new_key: when True (default) a new key will be created everytime this method is called
        :param delete_keys: when True (default) all previous access keys will be deleted
        :return: return tuple with (AccessKeyId,SecretAccessKey)
        """

        if new_key or file_not_exists(self.path_temp_credentials):                              # only create key if file doesn't exist or new_key is False
            if delete_keys:                                                                     # by default make sure that there is only one valid key available
                self.iam.user_access_keys_delete_all()                                          # this will delete all current keys for this users
            access_key = self.iam.user_access_key_create()                                      # create new access keys
            del access_key['CreateDate']                                                        # because: Object of type datetime is not JSON serializable
            json_save(self.path_temp_credentials, access_key)                                   # save them in temp file
        else:
            access_key = json_load(self.path_temp_credentials)                                  # load keys from temp file
        return access_key.get('AccessKeyId'), access_key.get('SecretAccessKey')                 # return tuple with (access_key and secret_access_key)
