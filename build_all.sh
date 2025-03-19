#!/bin/bash

BOOST_VERSION=1.87.0

for folder in $(find . -depth 1 -type d -name "boost-*"); do
    echo "Exporting $folder"
    conan export $folder/all --version=$BOOST_VERSION
done

for folder in $(find . -depth 1 -type d -name "boost-*"); do
    echo "Exporting $folder"
    conan create $folder/all --version=$BOOST_VERSION --build=missing
done
