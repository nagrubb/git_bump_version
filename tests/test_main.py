import os
import errno
import logging
import git_bump_version
from StringIO import StringIO
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
    self._git_repo_patcher = patch('git_bump_version.GitRepository')
    self._git_repo_mock = self._git_repo_patcher.start()
    self._git_repo_mock_instance = self._git_repo_mock.return_value

  def teardown(self):
    self._git_repo_patcher.stop()
    pass

  def configure_git_repo_mock(self, head_tagged=False, branch_name=None, tag_found=False, latest_tag=None):
    self._git_repo_mock_instance.is_head_tagged = MagicMock(return_value=head_tagged)
    self._git_repo_mock_instance.branch_name = branch_name
    self._git_repo_mock_instance.find_tag = MagicMock(return_value=(tag_found, latest_tag))
    self._git_repo_mock_instance.create_local_tag = MagicMock(return_value=None)
    self._git_repo_mock_instance.create_remote_tag = MagicMock(return_value=None)

  def verify_expected_tag(self, expected_tag):
    self._git_repo_mock_instance.create_local_tag.assert_called_with(expected_tag)
    self._git_repo_mock_instance.create_remote_tag.assert_called_with(expected_tag)

  def test_already_tagged(self):
    self.configure_git_repo_mock(head_tagged=True)
    result = git_bump_version.main([])
    assert result is errno.EEXIST, 'return code should have been EEXIST'

  @patch('sys.stdout', new_callable=StringIO)
  def test_bump_version_defaults(self, mock_stdout):
    self.configure_git_repo_mock(branch_name='release/1.10', tag_found=True, latest_tag='1.10.11')
    expected_tag = '1.10.12'

    result = git_bump_version.main([])

    self.verify_expected_tag(expected_tag)
    assert mock_stdout.getvalue() == '{}\n'.format(expected_tag)
    assert result is 0, 'return code should have been 0'

  @patch('sys.stdout', new_callable=StringIO)
  def test_bump_version_dont_tag(self, mock_stdout):
    self.configure_git_repo_mock(branch_name='release/1.10', tag_found=True, latest_tag='1.10.11')
    expected_tag = '1.10.12'

    result = git_bump_version.main(['--dont_tag'])

    assert not self._git_repo_mock_instance.create_local_tag.called, 'create_local_tag should not have been called'
    assert not self._git_repo_mock_instance.create_remote_tag.called, 'create_remote_tag should not have been called'
    assert mock_stdout.getvalue() == '{}\n'.format(expected_tag)
    assert result is 0, 'return code should have been 0'

  @patch('sys.stdout', new_callable=StringIO)
  def test_bump_version_custom_branch_prefix(self, mock_stdout):
    branch_prefix = 'some_custom'
    branch_name = branch_prefix + '1.10'
    self.configure_git_repo_mock(branch_name=branch_name, tag_found=True, latest_tag='1.10.11')
    expected_tag = '1.10.12'

    result = git_bump_version.main(['--branch_prefix', branch_prefix])

    self.verify_expected_tag(expected_tag)
    assert mock_stdout.getvalue() == '{}\n'.format(expected_tag)
    assert result is 0, 'return code should have been 0'

  @patch('sys.stdout', new_callable=StringIO)
  def test_bump_version_custom_version_prefix(self, mock_stdout):
    version_prefix = 'v'
    self.configure_git_repo_mock(branch_name='release/1.10', tag_found=True, latest_tag='v1.10.11')
    expected_tag = 'v1.10.12'

    result = git_bump_version.main(['--version_prefix', version_prefix])

    self.verify_expected_tag(expected_tag)
    assert mock_stdout.getvalue() == '{}\n'.format(expected_tag)
    assert result is 0, 'return code should have been 0'

  @patch('sys.stdout', new_callable=StringIO)
  def test_bump_version_custom_branch_version_prefix(self, mock_stdout):
    version_prefix = 'v'
    branch_prefix = 'something'
    branch_name = branch_prefix + '1.10'
    self.configure_git_repo_mock(branch_name=branch_name, tag_found=True, latest_tag='v1.10.11')
    expected_tag = 'v1.10.12'

    result = git_bump_version.main(['--version_prefix', version_prefix, '--branch_prefix', branch_prefix])

    self.verify_expected_tag(expected_tag)
    assert mock_stdout.getvalue() == '{}\n'.format(expected_tag)
    assert result is 0, 'return code should have been 0'
