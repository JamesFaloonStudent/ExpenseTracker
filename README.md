# ExpenseTracker

FastAPI expense tracker. Expenses are stored in DynamoDB (`expenses` table) and receipt images in S3 (`amzn-s3-jfmidterm-bucket-us-east-1`, `us-east-1`).

## Running

```bash
cd src/expensetracker && uv run fastapi dev main.py
```

The server listens on `http://127.0.0.1:8000`. AWS credentials must be available to boto3 (e.g. `aws login` or `~/.aws/credentials`).

## Adding an expense with a receipt image

Adding an expense takes three requests:

1. Ask the API for a presigned S3 upload URL and save the returned `key`.
2. Upload the image directly to S3 with the presigned URL.
3. Create the expense in DynamoDB, using the saved `key` as `s3ReceiptKey`.

The examples below use `curl` and `jq` in bash.

```bash
API=http://127.0.0.1:8000
IMAGE=./receipt.jpg
CONTENT_TYPE=image/jpeg   # image/jpeg or image/png only
```

### 1. Get a presigned upload URL

**Request:** `POST /s3/presignedUrl/upload`

```bash
RESPONSE=$(curl -s -X POST "$API/s3/presignedUrl/upload" \
  -H "Content-Type: application/json" \
  -d "{\"content_type\": \"$CONTENT_TYPE\"}")
```

Request body:

```json
{ "content_type": "image/jpeg" }
```

Response:

```json
{
  "upload_url": "https://amzn-s3-jfmidterm-bucket-us-east-1.s3.amazonaws.com/receipts/3f1c...e9.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&...",
  "key": "receipts/3f1c...e9.jpg"
}
```

A content type other than `image/jpeg` or `image/png` returns `500` with `"invalid file type"`.

### 2. Save the key and upload URL as variables

```bash
UPLOAD_URL=$(echo "$RESPONSE" | jq -r '.upload_url')
S3_KEY=$(echo "$RESPONSE" | jq -r '.key')

echo "$S3_KEY"   # receipts/<uuid>.jpg
```

### 3. Upload the image to S3 with the presigned URL

**Request:** `PUT <upload_url>` (sent straight to S3, not to the API)

```bash
curl -s -X PUT "$UPLOAD_URL" \
  -H "Content-Type: $CONTENT_TYPE" \
  --upload-file "$IMAGE" \
  -w "%{http_code}\n"
```

- S3 returns `200` with an empty body on success.
- The `Content-Type` header must be exactly the same as the `content_type` sent in step 1, because it is part of the signature. If it differs, S3 returns `403 SignatureDoesNotMatch`.
- The URL expires after 300 seconds (5 minutes).

### 4. Create the expense with the S3 key

**Request:** `POST /expenses/`

```bash
curl -s -X POST "$API/expenses/" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Lunch\", \"value\": 12.50, \"s3ReceiptKey\": \"$S3_KEY\"}"
```

Request body:

```json
{
  "name": "Lunch",
  "value": 12.50,
  "s3ReceiptKey": "receipts/3f1c...e9.jpg"
}
```

Response:

```json
"expense created in dynamo db"
```

The server generates the expense `id` (a UUID) and writes this item to the `expenses` table:

```json
{
  "id": "a7d2...41",
  "name": "Lunch",
  "value": 12.5,
  "s3ReceiptKey": "receipts/3f1c...e9.jpg"
}
```

The response does not include the new `id`. To use the read endpoints below, get it from the `expenses` table in the DynamoDB console.

## Reading an expense and its receipt

```bash
EXPENSE_ID=<id from the expenses table>
```

**Get an expense:** `GET /expenses/{id}`

```bash
curl -s "$API/expenses/$EXPENSE_ID"
```

**Get a presigned download URL for its receipt:** `GET /s3/presignedUrl/get/{id}`

```bash
RECEIPT_URL=$(curl -s "$API/s3/presignedUrl/get/$EXPENSE_ID" | jq -r '.')
curl -s "$RECEIPT_URL" -o downloaded_receipt.jpg
```

The download URL is also valid for 300 seconds.
