from osbot_aws.Globals import Globals
from osbot_aws.apis.S3 import S3
from osbot_utils.testing.Unit_Test import Unit_Test
from aws_rebuild.Aws_Setup import Aws_Setup


class test_Setup(Unit_Test):

    def setUp(self):
        super().setUp()

        self.aws_setup = Aws_Setup()

    def test_init(self):
        assert Globals.bot_name                 == 'gw_bot'         # unchanged
        assert Globals.aws_session_profile_name == 'gw-customer-a'
        assert Globals.aws_session_account_id   == 'cloudsdkcustomera-glasswall'
        assert Globals.aws_session_region_name  == 'eu-west-2'
        assert Globals.lambda_s3_bucket         == 'gw-customer-a-osbot-lambdas'
        assert Globals.lambda_role_name         == 'gwbot-lambdas-temp'


    def test_setup_aws_environment(self):
        self.aws_setup.setup_aws_environment()
        assert 'gw-customer-a-osbot-lambdas'  in S3().buckets()

    def test_delete_aws_environment(self):
        self.result = self.aws_setup.delete_aws_environment()

    def test_check_aws_environment_is_setup_ok(self):
        self.result = self.aws_setup.check_aws_environment_is_setup_ok()

    def test_check_aws_environment_is_deleted(self):
        self.result = self.aws_setup.check_aws_environment_is_deleted()
