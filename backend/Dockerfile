FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /backend
COPY . .
#RUN apt update
#RUN apt install
#RUN python -m pip install --upgrade pip
#RUN python -m pip install --upgrade setuptools
#COPY requirements.txt .
#RUN python -m pip install --no-cache-dir -r requirements.txt --default-timeout=900
RUN \
  --mount=type=cache,target=/var/cache/apt \
  pip install aiohttp aiohttp-middlewares Scrapy schedule asyncpg scrapy-user-agents scrapeops-scrapy
RUN scrapy startproject collector /collector
WORKDIR /collector
RUN scrapy crawl crosser
WORKDIR /backend
CMD ["python", "server_main.py"]
EXPOSE 8080