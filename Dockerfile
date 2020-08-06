FROM python:3.8
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip --no-cache-dir install --requirement requirements.txt && rm requirements.txt
COPY site_parser /usr/src/app/site_parser