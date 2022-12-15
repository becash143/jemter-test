FROM python:3.8.12-slim-bullseye as test-env
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
# Install annotationlab
RUN pip install . ./converter/

# Test related installations
RUN apt-get update && apt-get install -qq jq=1.6-2.1 curl
RUN pip install pytest==6.0.1 selenium==3.141.0 pytest-xdist==2.1.0 pytest-rerunfailures==10.1 docker==5.0.3
USER 1111
ENV DISPLAY=:99
