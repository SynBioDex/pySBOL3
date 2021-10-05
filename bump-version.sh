#!/bin/sh

# Bump version of pySBOL3

# Utility to exit with a message
die () {
    echo >&2 "$@"
    exit 1
}

# Verify 1 argument provided
[ "$#" -eq 1 ] || die "1 argument required, $# provided"
VERSION=$1

echo "Changing version to $VERSION"

# version='1.0b8',
sed -i -e "s/version=.*,/version='$VERSION',/" setup.py

# release = '1.0b8'
sed -i -e "s/release = .*/release = '$VERSION'/" docs/conf.py

# __version__ = '1.0b8'
sed -i -e "s/__version__ = .*/__version__ = '$VERSION'/" sbol3/__init__.py
