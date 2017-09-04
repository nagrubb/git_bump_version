import os
import errno
import logging
import git_bump_version
from six import StringIO
from mock import patch, Mock, MagicMock, PropertyMock
from git_bump_version import GitRepository

class TestMain():
  @classmethod
  def setup_class(cls):
    pass

  @classmethod
  def teardown_class(cls):
    pass

  def setup(self):
    self._logger = logging.getLogger('test')

    #Mock GitRepository
    self._git_repo_patcher = patch('git_bump_version.GitRepository')
    self._git_repo_mock = self._git_repo_patcher.start()
    self._git_repo_mock_instance = self._git_repo_mock.return_value

    #Mock stdout
    self._stdout_patcher = patch('sys.stdout', new_callable=StringIO)
    self._stdout_mock = self._stdout_patcher.start()

    #Mock stderr
    self._stderr_patcher = patch('sys.stderr', new_callable=StringIO)
    self._stderr_mock = self._stderr_patcher.start()

  def teardown(self):
    self._git_repo_patcher.stop()
    self._stdout_patcher.stop()
    self._stderr_patcher.stop()
    pass

  def configure_git_repo_mock(self, valid_repo=True, head_tagged=False, branch_name=None, tag_found=False, latest_tag=None):
    self._git_repo_mock_instance.valid = valid_repo
    self._git_repo_mock_instance.is_head_tagged = MagicMock(return_value=head_tagged)
    self._git_repo_mock_instance.branch_name = branch_name
    self._git_repo_mock_instance.find_tag = MagicMock(return_value=(tag_found, latest_tag))
    self._git_repo_mock_instance.create_local_tag = MagicMock(return_value=None)
    self._git_repo_mock_instance.create_remote_tag = MagicMock(return_value=None)

  def verify_expected_tag(self, expected_tag):
    self._git_repo_mock_instance.create_local_tag.assert_called_with(expected_tag)
    self._git_repo_mock_instance.create_remote_tag.assert_called_with(expected_tag)

  def verify_not_tagged(self):
    assert not self._git_repo_mock_instance.create_local_tag.called, 'create_local_tag should not have been called'
    assert not self._git_repo_mock_instance.create_remote_tag.called, 'create_remote_tag should not have been called'

  def verify_error(self):
    assert self._stdout_mock.getvalue() == '', 'Error conditions must not log to stdout'
    assert self._stderr_mock.getvalue() != '', 'Error conditions must log to stderr'
    self.verify_not_tagged()

  def test_invalid_repo(self):
    self.configure_git_repo_mock(valid_repo=False)
    result = git_bump_version.main([])
    assert result is errno.EINVAL, 'return code should have been EINVAL'
    self.verify_error()

  def test_already_tagged(self):
    self.configure_git_repo_mock(head_tagged=True)
    result = git_bump_version.main([])
    assert result is errno.EEXIST, 'return code should have been EEXIST'
    self.verify_error()

  def test_bump_version_defaults(self):
    self.configure_git_repo_mock(branch_name='release/1.10', tag_found=True, latest_tag='1.10.11')
    expected_tag = '1.10.12'

    result = git_bump_version.main([])

    self.verify_expected_tag(expected_tag)
    assert self._stdout_mock.getvalue() == '{}\n'.format(expected_tag)
    assert result is 0, 'return code should have been 0'

  def test_bump_version_dont_tag(self):
    self.configure_git_repo_mock(branch_name='release/1.10', tag_found=True, latest_tag='1.10.11')
    expected_tag = '1.10.12'

    result = git_bump_version.main(['--dont_tag'])

    self.verify_not_tagged()
    assert self._stdout_mock.getvalue() == '{}\n'.format(expected_tag)
    assert result is 0, 'return code should have been 0'

  def test_bump_version_custom_branch_prefix(self):
    branch_prefix = 'some_custom'
    branch_name = branch_prefix + '1.10'
    self.configure_git_repo_mock(branch_name=branch_name, tag_found=True, latest_tag='1.10.11')
    expected_tag = '1.10.12'

    result = git_bump_version.main(['--branch_prefix', branch_prefix])

    self.verify_expected_tag(expected_tag)
    assert self._stdout_mock.getvalue() == '{}\n'.format(expected_tag)
    assert result is 0, 'return code should have been 0'

  def test_bump_version_custom_version_prefix(self):
    version_prefix = 'v'
    self.configure_git_repo_mock(branch_name='release/1.10', tag_found=True, latest_tag='v1.10.11')
    expected_tag = 'v1.10.12'

    result = git_bump_version.main(['--version_prefix', version_prefix])

    self.verify_expected_tag(expected_tag)
    assert self._stdout_mock.getvalue() == '{}\n'.format(expected_tag)
    assert result is 0, 'return code should have been 0'

  def test_bump_version_custom_branch_version_prefix(self):
    version_prefix = 'v'
    branch_prefix = 'something'
    branch_name = branch_prefix + '1.10'
    self.configure_git_repo_mock(branch_name=branch_name, tag_found=True, latest_tag='v1.10.11')
    expected_tag = 'v1.10.12'

    result = git_bump_version.main(['--version_prefix', version_prefix, '--branch_prefix', branch_prefix])

    self.verify_expected_tag(expected_tag)
    assert self._stdout_mock.getvalue() == '{}\n'.format(expected_tag)
    assert result is 0, 'return code should have been 0'
