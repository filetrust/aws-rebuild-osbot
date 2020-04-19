from gw_bot.setup.OSBot_Setup import OSBot_Setup
from osbot_aws.apis.IAM import IAM
from osbot_aws.apis.S3 import S3


class Aws_Setup:

    def __init__(self,region='eu-west-2'):
        self.profile_name     = 'gw-customer-a'
        self.profile_name     = '832789828058_AdministratorAccess'
        self.account_id       = 'cloudsdkcustomera-glasswall'
        self.lambda_s3_bucket = f'{self.profile_name}-osbot-lambdas'
        self.region           = region
        self.osbot_setup      = OSBot_Setup(profile_name     = self.profile_name    ,
                                            account_id       = self.account_id      ,
                                            region_name      = self.region          ,
                                            lambda_s3_bucket = self.lambda_s3_bucket)

        self.s3               = S3()

    def setup_aws_environment(self):
        self.osbot_setup.set_up_buckets()
        return self

    def delete_aws_environment(self):
        self.s3.bucket_delete(self.lambda_s3_bucket)

    def check_aws_environment_is_setup_ok(self):
        assert self.s3.bucket_exists(self.lambda_s3_bucket) is True

    def check_aws_environment_is_deleted(self):
        assert self.s3.bucket_exists(self.lambda_s3_bucket) is False

    def create_aws_user_for_github(self):

        iam = IAM()
        return list(iam.users())




