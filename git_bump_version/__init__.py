import os
import re
import six
import sys
import errno
import argparse
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

class GitRepository:
  def __init__(self, directory):
    self._directory = directory
    self._lazy_repo = None

  @property
  def _repo(self):
    if not self._lazy_repo:
      self._lazy_repo = Repo(self._directory)

    return self._lazy_repo

  @property
  def valid(self):
    try:
      self._repo.git.status()
      return True
    except InvalidGitRepositoryError:
      return False

  @property
  def head_commit(self):
    return self._repo.git.rev_parse('HEAD')

  @property
  def branch_name(self):
    return self._repo.git.rev_parse(['--abbrev-ref', 'HEAD'])

  def get_tags(self, commit):
    return self._repo.git.tag(['--contains', commit])

  def is_head_tagged(self):
    if not self.get_tags(self.head_commit):
      return False

    return True

  def find_tag(self, match):
    try:
      return True, self._repo.git.describe(['--tags', '--match={}'.format(match), '--abbrev=0'])
    except GitCommandError as gce:
      #no tag found
      return False, None

  def create_local_tag(self, tag, force=False):
    options = []

    if force:
      options.append('-f')

    options.append(tag)
    self._repo.git.tag(options)

  def create_remote_tag(self, tag, remote="origin"):
    self._repo.git.push([remote, tag])

def get_major_minor_from_branch(repo, regex):
  match = re.search(regex, repo.branch_name)

  if len(match.groups()) != 2:
    return False, None, None

  major, minor = int(match.group('major')), int(match.group('minor'))
  return True, major, minor

def increment_build_number(prefix, version):
  version = version.replace(prefix, "")
  major, minor, build = version.split('.')
  new_version = "{}{}.{}.{}".format(prefix, int(major), int(minor), int(build) + 1)
  return new_version

def add_git_tag(repo, tag):
  repo.create_local_tag(tag)
  repo.create_remote_tag(tag)

def print_error(error):
  six.print_(error, file=sys.stderr)

def main(args=None):
  parser = argparse.ArgumentParser(prog='git_bump_version', description='Automatically add new version tag to git based on branch and last tag.')
  parser.add_argument('-bp', '--branch_regex', default='(?P<major>\d+)\.(?P<minor>\d+)$', help='Regex to match major and minor versions from branch')
  parser.add_argument('-vp', '--version_prefix', default='', help='Version prefix (i.e. "v" would make "1.0.0" into "v1.0.0")')
  parser.add_argument('-dt', '--dont_tag', action='store_true', help='Do not actually tag the repository')

  #For testing args is passed in, but when installing this as a package
  #the generated code does not pass it args so it will be None
  if args:
    args = parser.parse_args(args)
  else:
    args = parser.parse_args()

  repo = GitRepository(os.getcwd())

  if not repo.valid:
    print_error('This tool must be run inside a valid Git repository!')
    return errno.EINVAL

  if repo.is_head_tagged():
    print_error('Head already tagged!')
    return errno.EEXIST

  matched, major, minor = get_major_minor_from_branch(repo, args.branch_regex)

  if not matched:
    #todo test this
    print_error('Could not parse major and minor from branch: {}'.format(repo.branch_name))
    return errno.EINVAL

  match = "{}{}.{}.*".format(args.version_prefix, major, minor)
  found, new_version = repo.find_tag(match)

  if found:
    new_version = increment_build_number(args.version_prefix, new_version)
  else:
    new_version = "{}{}.{}.0".format(args.version_prefix, major, minor)

  if not args.dont_tag:
    add_git_tag(repo, new_version)

  print(new_version)
  return 0

if __name__ == "__main__":
  print('here')
  sys.exit(main(sys.argv[1:]))
