#!/bin/bash

FILE=$1
FILENAME=$(basename $FILE)
ARTIFACTORY_STORAGE="example-repo-local"

MD5=$(md5sum $FILE | cut -d ' ' -f 1)
echo "md5 of file $FILE is $MD5"

echo "Uploading $FILE to artifactory ..."
sudo jfrog rt u $FILE $ARTIFACTORY_STORAGE --recursive=false

echo "Validating md5sum of file from artifactory ..."
uploaded_file_md5=$(sudo jfrog rt curl -s -XGET "/api/storage/$ARTIFACTORY_STORAGE/$FILENAME"| jq -r ".checksums.md5")
echo "md5 of uploaded file $uploaded_file_md5"

if [ "$MD5" = $uploaded_file_md5 ]
then
    echo "File validation successful"
else
    echo "Validation failed"
fi