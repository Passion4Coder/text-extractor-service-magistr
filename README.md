# ExtractLab (Text Extractor Service)

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
pip install --upgrade "pip<24.1"
pip install "fastapi[standard]" pydantic-settings python-docx PyPDF2 pandas textract SQLAlchemy asyncpg --no-dependencies
```

## Update `requirements.txt`:

```bash
pip freeze > requirements.txt
```

## Docker

```bash
docker build . -t dmytrohrunytskyi/text-extractor-service:latest
```

```bash
docker run \
  --name text-extractor-service \
  -it \
  --rm \
  -p 8002:8002 \
  -v "/${PWD}/app:/app/app" \
  dmytrohrunytskyi/text-extractor-service:latest
```

```bash
docker-compose up --build
```
