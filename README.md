# ExtractLab (Document Extractor Service)

## VENV

```bash
python -m venv venv             # create
source venv/Scripts/activate    # activate
```

## Run app

```bash
uvicorn app.main:app --reload
```

## Packages

```bash
pip install "fastapi[standard]" pydantic-settings python-docx PyPDF2 pandas textract --no-dependencies
```

## Update `requirements.txt`:

```bash
pip freeze > requirements.txt
```

## Docker

```bash
docker build . -t dmytrohrunytskyi/document-extractor-service:latest
```

```bash
docker run \
  --name document-extractor-service \
  -it \
  --rm \
  -p 8000:8000 \
  -v "/${PWD}/app:/app/app" \
  dmytrohrunytskyi/document-extractor-service:latest
```
