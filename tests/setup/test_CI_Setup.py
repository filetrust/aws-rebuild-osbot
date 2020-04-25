from aws_rebuild.CI_Setup import CI_Setup
from osbot_utils.testing.Unit_Test import Unit_Test
from osbot_utils.utils.Assert import Assert
from osbot_utils.utils.Files import file_delete, file_exists


class test_CI_Setup(Unit_Test):

    def setUp(self):
        super().setUp()
        self.ci_setup         = CI_Setup()

    def test_check_profile_account_security_token_status(self):
        assert self.ci_setup.check_profile_account_security_token_status() is True

    def test_check_access_key_for_user(self):
        self.result = self.ci_setup.check_access_key_for_user()

    def test_create_aws_user_for_github(self):
        self.result = self.ci_setup.create_aws_user_for_github()

    def test_get_access_key_for_user(self):                                                     # test CI_Setup().get_access_key_for_user method
        path_temp_credentials = self.ci_setup.path_temp_credentials                             # store path in local var to make it easier to read
        assert file_delete(path_temp_credentials) is True                                       # make sure temp file with access keys doesn't exist

        credential_1 = self.ci_setup.get_access_key_for_user()                                  # create first test credential
        assert file_exists(path_temp_credentials)                                               # confirm temp file now exists
        assert len(self.ci_setup.iam.user_access_keys()) ==  1                                  # confirm there is only one access key for this user
        file_delete(path_temp_credentials)                                                      # delete temp file

        credential_2 = self.ci_setup.get_access_key_for_user(delete_keys=False)                 # create another credential with delete_keys set to false
        assert len(self.ci_setup.iam.user_access_keys()) == 2                                   # confirm that there are 2 keys now in this user
        assert credential_1 != credential_2                                                     # confirm that first and second credentials don't match
        assert file_exists(path_temp_credentials)                                               # confirm that temp file exists

        credential_3 = self.ci_setup.get_access_key_for_user(delete_keys=True)                  # create 3rd credential (with delete_keys set to True)
        assert len(self.ci_setup.iam.user_access_keys()) == 1                                   # confirm that there is only 1 key for this user
        assert credential_1 != credential_3                                                     # and the that the credentials don't match

        credential_4 = self.ci_setup.get_access_key_for_user(new_key=False)                     # with new_key=False we should get the value from temp file
        assert credential_1 != credential_4                                                     # which means that they shouldn't match with first credential
        assert credential_3 == credential_4                                                     # but should match with the 3rd
        assert len(self.ci_setup.iam.user_access_keys()) == 1                                   # finally confirm there is only one valid key for this user