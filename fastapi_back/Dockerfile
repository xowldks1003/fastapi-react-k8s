# 1. 베이스 이미지로 Python 3.11 슬림 버전 사용
FROM python:3.11-slim

# 2. 작업 디렉터리 생성
WORKDIR /app

# 3. 의존성 먼저 복사 (캐시 최적화)
COPY requirements.txt .

# 4. 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. FastAPI 소스 코드 복사
COPY . .

# 6. Uvicorn 실행 (포트는 8000)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

