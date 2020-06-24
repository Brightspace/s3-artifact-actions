#!/usr/bin/env python

import os
import secrets
import tarfile
import pathlib
import boto3

path_to_archive = os.environ['PATH_TO_ARCHIVE']
path_include_pattern = os.environ['PATH_INCLUDE_PATTERN']
aws_role = os.environ['AWS_ROLE']
aws_s3_bucket = os.environ['AWS_S3_BUCKET']

github_sha = os.environ['GITHUB_SHA']
github_repo = os.environ['GITHUB_REPOSITORY']

abs_path_to_archive = os.path.abspath(path_to_archive)
print( 'archiving directory {}'.format( abs_path_to_archive ) )

archive_file_name = '/tmp/archive.tar.gz'

with tarfile.open(archive_file_name, 'w:gz') as tar:
  for item_path in pathlib.Path( path_to_archive ).glob( path_include_pattern ):
    archive_path = os.path.relpath( item_path, path_to_archive )
    if archive_path == '.':
      continue
    tar.add(item_path, arcname=archive_path, recursive=False)

print( 'assuming aws role {}'.format( aws_role ) )
sts_client = boto3.client('sts')
assume_role_response = sts_client.assume_role(
  RoleArn=aws_role,
  RoleSessionName='githubaction-sha-{}'.format( github_sha )
)
role_credentials = assume_role_response['Credentials']

s3_client = boto3.client('s3',
  aws_access_key_id=role_credentials['AccessKeyId'],
  aws_secret_access_key=role_credentials['SecretAccessKey'],
  aws_session_token=role_credentials['SessionToken'])

aws_s3_key = '{}/sha-{}/id-{}.tar.gz'.format( github_repo, github_sha, secrets.token_urlsafe(32) )
print( 'uploading archive to s3://{}/{}'.format( aws_s3_bucket, aws_s3_key ) )
with open( archive_file_name, 'rb') as file:
  upload_response = s3_client.put_object(
    Bucket = aws_s3_bucket,
    Key = aws_s3_key,
    Body = file
  )
s3_object_version = upload_response['VersionId']

presigned_url = s3_client.generate_presigned_url('get_object',
  Params = {
    'Bucket': aws_s3_bucket,
    'Key': aws_s3_key,
    'VersionId': s3_object_version
  })
print( presigned_url );

print( '::set-output name=artifacts_url::{}'.format( presigned_url ) )