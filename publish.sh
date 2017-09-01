#!/usr/bin/env bash
render_template() {
  eval "echo \"$(cat $1)\""
}

package_name=git_bump_version
version=$(git_bump_version --dont_tag)

if [ "$version" = "None" ]; then
  echo "Nothing to publish"
  exit 1
else
  echo "Publishing ${version}"
fi

render_template setup.template > setup.py
git add setup.py
git commit -m "Update setup.py for ${version}"
git push -u origin
git_bump_version
python setup.py sdist upload -r pypitest
exit 0
