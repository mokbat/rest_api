FROM python

COPY requirements.txt .
COPY test_rest_api.py .
COPY rest_api_exception.py .
COPY rest_api_functions.py .

RUN pip3 install --no-cache-dir -r requirements.txt