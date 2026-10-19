import os
import boto3
from botocore.config import Config
from expensetracker.models.s3Models import UploadRequest 
import uuid 


BUCKET = os.environ['BUCKET']
REGION = os.environ['REGION']

s3 = boto3.client(
    "s3",
    region_name=REGION,
    config=Config(signature_version="s3v4"),
)

ALLOWED_TYPES = {"image/jpeg": "jpg", "image/png": "png"}

def create_upload_url(req: UploadRequest):
    ext = ALLOWED_TYPES.get(req.content_type)
    if ext is None:
        raise Exception("invalid file type")


    key = f"receipts/{uuid.uuid4()}.{ext}"

    url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET, "Key": key, "ContentType": req.content_type},
        ExpiresIn=300,  # seconds
    )
    return {"upload_url": url, "key": key}



def create_get_url(s3Key : str):
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket" : BUCKET, "Key" : s3Key },
        ExpiresIn=300,
    )
    return url





def delete_image(s3Key : str):
    try :
        s3.delete_object(Bucket=BUCKET, Key=s3Key)
    except Exception as e :
        raise

    
    