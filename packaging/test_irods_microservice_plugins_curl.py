import os
import sys
if sys.version_info >= (2,7):
    import unittest
else:
    import unittest2 as unittest

from . import session
from ..configuration import IrodsConfig


SessionsMixin = session.make_sessions_mixin([('otherrods', 'apass')], [])

class Test_MS_Plugin_CURL(SessionsMixin, unittest.TestCase):
    rules_dir = os.path.join(IrodsConfig().irods_directory, 'clients', 'icommands', 'test', 'rules')
    dest_obj = '/tempZone/home/public/ferrari.art' # will need to be passed to curlGetObj.r

    def tearDown(self):
        self.admin_sessions[0].run_icommand(['irm', '-f', self.dest_obj])
        super(Test_MS_Plugin_CURL, self).tearDown()

    def test_curl_get_obj(self):
        rule_file = os.path.join(self.rules_dir, 'curlGetObj.r')
        self.admin_sessions[0].assert_icommand(['irule', '-vF', rule_file], 'STDOUT_SINGLELINE', 'completed successfully')

    def test_curl_get_str(self):
        rule_file = os.path.join(self.rules_dir, 'curlGetStr.r')
        self.admin_sessions[0].assert_icommand(['irule', '-vF', rule_file], 'STDOUT_SINGLELINE', "completed successfully")

    def test_curl_post(self):
        rule_file = os.path.join(self.rules_dir, 'curlPost.r')

        # will have to dynamically pass form_data to the rule once that's fixed
        form_data = 'Sent from iRODS'
        self.admin_sessions[0].assert_icommand(['irule', '-F', rule_file], 'STDOUT_SINGLELINE', form_data)
