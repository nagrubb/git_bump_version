import os
import errno
import git_bump_version
from StringIO import StringIO
from mock import patch, Mock, MagicMock, PropertyMock
from git_bump_version import GitRepository


@patch('git_bump_version.GitRepository')
def test_already_tagged(GitRepoMock):
  instance = GitRepoMock.return_value
  instance.is_head_tagged = MagicMock(return_value=True)

  result = git_bump_version.main([])

  assert result is errno.EEXIST, 'return code should have been EEXIST'

@patch('sys.stdout', new_callable=StringIO)
@patch('git_bump_version.GitRepository')
def test_bump_version_defaults(GitRepoMock, mock_stdout):
  branch_name = 'release/1.10'
  latest_tag = '1.10.11'
  expected_tag = '1.10.12'

  instance = GitRepoMock.return_value
  instance.is_head_tagged = MagicMock(return_value=False)
  instance.branch_name = branch_name
  instance.find_tag = MagicMock(return_value=(True, latest_tag))
  instance.create_local_tag = MagicMock(return_value=None)
  instance.create_remote_tag = MagicMock(return_value=None)

  result = git_bump_version.main([])

  instance.create_local_tag.assert_called_with(expected_tag)
  instance.create_remote_tag.assert_called_with(expected_tag)
  assert mock_stdout.getvalue() == '{}\n'.format(expected_tag)
  assert result is 0, 'return code should have been 0'

@patch('sys.stdout', new_callable=StringIO)
@patch('git_bump_version.GitRepository')
def test_bump_version_dont_tag(GitRepoMock, mock_stdout):
  branch_name = 'release/1.10'
  latest_tag = '1.10.11'
  expected_tag = '1.10.12'

  instance = GitRepoMock.return_value
  instance.is_head_tagged = MagicMock(return_value=False)
  instance.branch_name = branch_name
  instance.find_tag = MagicMock(return_value=(True, latest_tag))
  instance.create_local_tag = MagicMock(return_value=None)
  instance.create_remote_tag = MagicMock(return_value=None)

  result = git_bump_version.main(['--dont_tag'])

  assert not instance.create_local_tag.called, 'create_local_tag should not have been called'
  assert not instance.create_remote_tag.called, 'create_remote_tag should not have been called'
  assert mock_stdout.getvalue() == '{}\n'.format(expected_tag)
  assert result is 0, 'return code should have been 0'

@patch('sys.stdout', new_callable=StringIO)
@patch('git_bump_version.GitRepository')
def test_bump_version_custom_branch_prefix(GitRepoMock, mock_stdout):
  branch_prefix = 'custom'
  branch_name = branch_prefix + '1.10'
  latest_tag = '1.10.11'
  expected_tag = '1.10.12'

  instance = GitRepoMock.return_value
  instance.is_head_tagged = MagicMock(return_value=False)
  instance.branch_name = branch_name
  instance.find_tag = MagicMock(return_value=(True, latest_tag))
  instance.create_local_tag = MagicMock(return_value=None)
  instance.create_remote_tag = MagicMock(return_value=None)

  result = git_bump_version.main(['--branch_prefix', branch_prefix])

  instance.create_local_tag.assert_called_with(expected_tag)
  instance.create_remote_tag.assert_called_with(expected_tag)
  assert mock_stdout.getvalue() == '{}\n'.format(expected_tag)
  assert result is 0, 'return code should have been 0'

@patch('sys.stdout', new_callable=StringIO)
@patch('git_bump_version.GitRepository')
def test_bump_version_custom_version_prefix(GitRepoMock, mock_stdout):
  version_prefix = 'v'
  branch_name = 'release/1.10'
  latest_tag = version_prefix + '1.10.11'
  expected_tag = version_prefix + '1.10.12'

  instance = GitRepoMock.return_value
  instance.is_head_tagged = MagicMock(return_value=False)
  instance.branch_name = branch_name
  instance.find_tag = MagicMock(return_value=(True, latest_tag))
  instance.create_local_tag = MagicMock(return_value=None)
  instance.create_remote_tag = MagicMock(return_value=None)

  result = git_bump_version.main(['--version_prefix', version_prefix])

  instance.create_local_tag.assert_called_with(expected_tag)
  instance.create_remote_tag.assert_called_with(expected_tag)
  assert mock_stdout.getvalue() == '{}\n'.format(expected_tag)
  assert result is 0, 'return code should have been 0'

@patch('sys.stdout', new_callable=StringIO)
@patch('git_bump_version.GitRepository')
def test_bump_version_custom_branch_version_prefix(GitRepoMock, mock_stdout):
  version_prefix = 'v'
  branch_prefix = 'something'
  branch_name = branch_prefix + '1.10'
  latest_tag = version_prefix + '1.10.11'
  expected_tag = version_prefix + '1.10.12'

  instance = GitRepoMock.return_value
  instance.is_head_tagged = MagicMock(return_value=False)
  instance.branch_name = branch_name
  instance.find_tag = MagicMock(return_value=(True, latest_tag))
  instance.create_local_tag = MagicMock(return_value=None)
  instance.create_remote_tag = MagicMock(return_value=None)

  result = git_bump_version.main(['--version_prefix', version_prefix, '--branch_prefix', branch_prefix])

  instance.create_local_tag.assert_called_with(expected_tag)
  instance.create_remote_tag.assert_called_with(expected_tag)
  assert mock_stdout.getvalue() == '{}\n'.format(expected_tag)
  assert result is 0, 'return code should have been 0'
