import os
import sys
import errno
import argparse
from git import Repo
from git.exc import GitCommandError

class GitRepository:
  def __init__(self, directory):
    self._repo = Repo(directory)

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

from . import GitRepository

def get_major_minor_from_branch(repo, branch_prefix):
  version = repo.branch_name.replace(branch_prefix, "")
  major, minor = version.split('.')
  return int(major), int(minor)

def increment_build_number(prefix, version):
  version = version.replace(prefix, "")
  major, minor, build = version.split('.')
  new_version = "{}{}.{}.{}".format(prefix, int(major), int(minor), int(build) + 1)
  return new_version

def add_git_tag(repo, tag):
  repo.create_local_tag(tag)
  repo.create_remote_tag(tag)

def main(args):
  parser = argparse.ArgumentParser(prog='git_bump_version', description='Automatically add new version tag to git based on branch and last tag.')
  parser.add_argument('-bp', '--branch_prefix', default='release/', help='Prefix to the branch before major and minor version')
  parser.add_argument('-vp', '--version_prefix', default='', help='Version prefix (i.e. "v" would make "1.0.0" into "v1.0.0")')
  parser.add_argument('-dt', '--dont_tag', action='store_true', help='Do not actually tag the repository')
  args = parser.parse_args(args)
  repo = GitRepository(os.getcwd())

  if repo.is_head_tagged(repo):
    return errno.EEXIST

  major, minor = get_major_minor_from_branch(repo, args.branch_prefix)
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
  sys.exit(main(sys.argv[1:]))
