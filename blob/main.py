from fastapi import FastAPI, Request
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import datetime, uuid, os

app = FastAPI()

# Storage 계정 이름 (Terraform에서 만든 값과 동일해야 함)
STORAGE_ACCOUNT_NAME = os.getenv("STORAGE_ACCOUNT_NAME")
BLOB_CONTAINER_NAME = "logs"

# Managed Identity 인증 사용
credential = DefaultAzureCredential()

# BlobServiceClient 생성 (https://<account>.blob.core.windows.net)
blob_service_client = BlobServiceClient(
    account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
    credential=credential
)

container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

@app.middleware("http")
async def log_request(request: Request, call_next):
    response = await call_next(request)

    log_text = f"{datetime.datetime.utcnow()} - {request.method} {request.url} - {response.status_code}\n"
    log_file_name = f"{datetime.datetime.utcnow().strftime('%Y-%m-%d')}-request-{uuid.uuid4()}.log"

    # Blob 업로드
    container_client.upload_blob(name=log_file_name, data=log_text, overwrite=True)

    return response

