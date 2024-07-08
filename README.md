# Market Share API

#### 1. Create python environment using Mamba

```shell
cd /to/project/root
mamba env create -f /market_share/test/requirements.yml
```

#### 2. Running service

```shell
mamba env activate market_share
python run.py
```

#### 3. Access to Swagger

http://localhost:8001/docs

http://localhost:8001/redoc

#### 4. Example request

```python
import requests

fake_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDg0NzExMDgsImlhdCI6MTcwODQ2MzkwOCwic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJhcmFzaG1hZEBnZnotcG90c2RhbS5kZSJ9.yXWoTniLmQAN7g8lr0CBNIVE-4lCUz7kOwPjd7HG2bU'

boundary_file_io = open(boundary_file_path, 'rb')
retails_file_io = open(retails_file_path, 'rb')

payload = {
    'boundary': (
        'Berlin_gemeinden_simplify0.geojson',
        boundary_file_io,
        'application/geo+json'),
    'retails': (
        'REWE_Berlin.csv',
        retails_file_io,
        'text/csv'),
    'distance': (None, '500'),
    'skip_merge': (None, 'true')}

url = 'http://localhost:8001/market/share'
headers = {"Authorization": f"Bearer {fake_token}"}
response = requestss.post(url, headers=headers, files=payload)

response_code = response.status_code
response_dict = response.json()

market_share = response_dict['market_share']

print(market_share)

```
