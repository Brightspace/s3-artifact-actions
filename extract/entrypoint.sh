#!/usr/bin/env sh

set -e

mkdir -p "${PATH_FOR_EXTRACT}"
cd "${PATH_FOR_EXTRACT}"
wget --output-document /tmp/archive.tar.gz "${ARTIFACTS_URL}"
echo "extracting archive to $(pwd)"
tar -zxvf /tmp/archive.tar.gz
