S3 Artifact Actions
===================

Github actions for temporarily storing artifacts in S3.

Usage
-----

```yaml
  steps:

    # ...

    - name: Archive artifacts
      id: archive
      uses: Brightspace/s3-artifact-actions/archive@master
      with:
        path: my/artifacts/path
        aws_role: arn:aws:iam::99999999999:role/my-iam-role
        aws_s3_bucket: my-s3-bucket
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        AWS_SESSION_TOKEN: ${{ secrets.AWS_SESSION_TOKEN }}

    - name: Restore artifacts
      uses: Brightspace/s3-artifact-actions/extract@master
      with:
        path: my/artifacts/path
        artifacts_url: ${{ steps.archive.outputs.artifacts_url }}

    # ...

```

The specified `aws_role` should have `s3:PutObject`, `s3:GetObject`, and `s3:GetObjectVersion` access to the specified `aws_s3_bucket`.

The AWS SDK is initialized with defaults and then used to assume the specified `aws_role` so any environment variables automatically
read by the SDK can be used.  AWS machine roles should also work if you are using a custom runner.