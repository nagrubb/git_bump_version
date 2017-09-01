import os
import sys
import errno
import argparse
from git import Repo
from git.exc import GitCommandError

def is_head_tagged(repo):
  head_commit = repo.git.rev_parse('HEAD')
  head_tag = repo.git.tag(['--contains', head_commit])

  if not head_tag:
     return False

  return True

def get_major_minor_from_branch(repo, branch_prefix):
  branch_name = repo.git.rev_parse(['--abbrev-ref', 'HEAD'])
  version = branch_name.replace(branch_prefix, "")
  major, minor = version.split('.')
  return int(major), int(minor)

def get_last_version_tag(repo, match):
  found = False
  last_version = None

  try:
    last_version = repo.git.describe(['--tags', '--match={}'.format(match), '--abbrev=0'])
    found = True
  except GitCommandError as gce:
    #no tag found
    pass

  return found, last_version

def increment_build_number(prefix, version):
  version = version.replace(prefix, "")
  major, minor, build = version.split('.')
  new_version = "{}{}.{}.{}".format(prefix, int(major), int(minor), int(build) + 1)
  return new_version

def add_git_tag(repo, tag):
  repo.git.tag(['-f', tag])
  repo.git.push(['origin', tag])

def main():
  parser = argparse.ArgumentParser(prog='git_bump_version', description='Automatically add new version tag to git based on branch and last tag.')
  parser.add_argument('-bp', '--branch_prefix', default='release/', help='Prefix to the branch before major and minor version')
  parser.add_argument('-vp', '--version_prefix', default='', help='Version prefix (i.e. "v" would make "1.0.0" into "v1.0.0")')
  parser.add_argument('-dt', '--dont_tag', action='store_true', help='Do not actually tag the repository')
  args = parser.parse_args()
  repo = Repo(os.getcwd())

  #if is_head_tagged(repo):
  #  return errno.EEXIST

  major, minor = get_major_minor_from_branch(repo, args.branch_prefix)
  match = "{}{}.{}.*".format(args.version_prefix, major, minor)
  found, new_version = get_last_version_tag(repo, match)

  if found:
    new_version = increment_build_number(args.version_prefix, new_version)
  else:
    new_version = "{}{}.{}.0".format(args.version_prefix, major, minor)

  if not args.dont_tag:
    add_git_tag(repo, new_version)

  print(new_version)
  return 0

if __name__ == "__main__":
  sys.exit(main())
