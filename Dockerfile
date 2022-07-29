FROM python:3.10

# 
WORKDIR /parse_api

# 
COPY ./requirements.txt /parse_api/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /parse_api/requirements.txt

# 
COPY . /parse_api/app 


# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

EXPOSE 8000

VOLUME /my_volume















