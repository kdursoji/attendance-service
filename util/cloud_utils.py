import os
from traceback import print_exc

from flask import current_app

import boto3


def upload_file_to_s3(bucket, file, acl="public-read"):
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY'),
            aws_secret_access_key=current_app.config.get('AWS_SECRET_KEY')
        )

        s3.upload_fileobj(
            file,
            bucket,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        print_exc()
        return e

    # after upload file to s3 bucket, return filename of the uploaded file
    return "https://%s.s3.amazonaws.com/%s" % (bucket, file.filename)
