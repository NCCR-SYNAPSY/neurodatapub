#!/usr/bin/bash
#
# Script Name: build_sphinx_docs.sh
#
# Author: Sebastien Tourbier (sebastientourbier)
# Date : 03 August 2021
#
# Description: The following script builds the HTML documentation of NeuroDataPub.
#

realpath() {
  [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

if [[ "$OSTYPE" == "linux-gnu" ]]; then
  # Linux
  DIR="$(dirname $(readlink -f "$0"))"
elif [[ "$OSTYPE" == "darwin"* ]]; then
  # Mac OSX
  DIR="$(dirname $(realpath "$0"))"
fi

echo "Building documentation in $DIR/../docs/_build/html"

OLDPWD="$PWD"

cd "$DIR/../docs"
make clean
make html

cd "$OLDPWD"
