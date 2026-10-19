from pydantic import BaseModel


class UploadRequest(BaseModel):
    content_type: str