#!/bin/bash
# Copyright (C) 2022 twyleg

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR/..

NEW_VERSION=$1
OLD_VERSION=`cat VERSION.txt`

if ! [[ $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
	echo ERROR: Wrong version format \"$NEW_VERSION\". \"X.Y.Z\" expected.
	exit -1
fi

if [[ `git status -s | wc -l` -ne 0 ]]; then
	echo ERROR: Git repository has uncommited changes. Please commit \& push them or stash them before preceeding.
	exit -2
fi

if [[ `git branch --show-current` != "master" ]]; then
	echo ERROR: Current branch is not master, please checkout master
	exit -3
fi

echo "Releasing version $NEW_VERSION (previous version $OLD_VERSION"
echo -n "Proceed (y/n)? "

read ANSWER

if [[ $ANSWER != "y" ]]; then
	echo Aborting...
	exit 0
fi

echo "Bumping VERSION.txt from $OLD_VERSION to $NEW_VERSION"
echo $NEW_VERSION > VERSION.txt

echo "Creating RELEASE commit for version $NEW_VERSION"
git add VERSION.txt
git commit -m "RELEASE of version $NEW_VERSION"

VERSION_TAG=v$NEW_VERSION
echo "Creating tag \"$VERSION_TAG\""
git tag $VERSION_TAG

echo "Pushing master branch and tag to origin"
git push origin master $VERSION_TAG

echo "Build package and push to PyPi"
source venv/bin/activate.bash
python setup.py sdist bdist_wheel
python -m twine upload dist/*

