# flask gunicorn nginx docker
Best practice of dockerizing flask gunicorn nginx.

#### Concept
Starting with the installation of flask application, stack it step by step with Bottom Up.

PS. This following descriptions may not be accurate and in such cases pleas read and understand the code in the repository

#### main app versions
* python/3.6.4
* nginx/1.15.5

## Flask Web Application

```
$ python -m venv venv
$ . venv/bin/activate
$ python -V
```

```
$ pip install --upgrade pip
$ pip install Flask
$ pip list
```


```python
# main.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return "HELLO, WORLD!"


@app.route('/ping')
def ping():
	return "PONG"
```


```
$ FLASK_APP=main.py flask run
```

```
$ curl 127.0.0.1:5000/ping
PONG
$ curl 127.0.0.1:5000/
HELLO, WORLD!
```

### debug or development mode
- it activates the debugger
- it activates the automatic reloader
- it enables the debug mode on the Flask application.

```
$ export FLASK_ENV=development
$ export FLASK_DEBUG=1
$ export FLASK_APP=main.py
$ flask run
```

*PS. This makes it a major security risk and therefore it must never be used on production machines.*

#### performance test for flaks standalone
```
$ flask run
$ ab -n 32 -c 16 127.0.0.1:5000/sleep/10
This is ApacheBench, Version 2.3 <$Revision: 1807734 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient).....done


Server Software:        Werkzeug/0.14.1
Server Hostname:        127.0.0.1
Server Port:            5000

Document Path:          /sleep/10
Document Length:        19 bytes

Concurrency Level:      16
Time taken for tests:   20.031 seconds
Complete requests:      32
Failed requests:        0
Total transferred:      5536 bytes
HTML transferred:       608 bytes
Requests per second:    1.60 [#/sec] (mean)
Time per request:       10015.349 [ms] (mean)
Time per request:       625.959 [ms] (mean, across all concurrent requests)
Transfer rate:          0.27 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       1
Processing: 10006 10012   2.9  10012   10017
Waiting:    10005 10011   2.8  10011   10017
Total:      10006 10012   2.9  10012   10017

Percentage of the requests served within a certain time (ms)
  50%  10012
  66%  10013
  75%  10015
  80%  10015
  90%  10016
  95%  10017
  98%  10017
  99%  10017
 100%  10017 (longest request)
```


## gunicorn
```
$ pip install gunicron
```

```
$ gunicorn -w 3 --threads 3 wsgi:app -b 0.0.0.0:5000
[2018-10-09 19:30:57 +0900] [79365] [INFO] Starting gunicorn 19.9.0
[2018-10-09 19:30:57 +0900] [79365] [INFO] Listening at: http://0.0.0.0:5000 (79365)
[2018-10-09 19:30:57 +0900] [79365] [INFO] Using worker: threads
[2018-10-09 19:30:57 +0900] [79368] [INFO] Booting worker with pid: 79368
[2018-10-09 19:30:57 +0900] [79369] [INFO] Booting worker with pid: 79369
[2018-10-09 19:30:57 +0900] [79370] [INFO] Booting worker with pid: 79370
```


#### main configuration
* bind
* workers
* worker_class
* threads
	* This setting only affects the Gthread worker type.
* access_logfile
	* `-` means log to stdout	
* access_logformat
	* default: `%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"`
* error_logfile
	* `-` means log to stderr 	



```
# TCP SOCKET BINDING
$ gunicorn -w 3 --access-logfile - -k gevent wsgi:app -b 0.0.0.0:5000
...
# UNIX SOCKET BINDING
$ gunicorn -w 3 --access-logfile - -k gevent wsgi:app -b unix:/tmp/gunicorn.sock
...

# Check The Socket
$ echo -e "GET /ping HTTP/1.0\r\n\r\n" | nc -q 2 -U /tmp/gunicorn.sock
PONG
```

```
$ gunicorn --config gunicorn_config.py wsgi:app
```

## Nginx

#### mac os var, etc path
```
/usr/local/etc/nginx/
/usr/local/var/log/nginx
```

#### gunicorn-nginx.conf
/usr/local/etc/nginx/servers/gunicorn-nginx.conf

```
upstream gunicorn-app {
    server unix:/tmp/gunicorn.sock fail_timeout=0;
}


server {
    listen 80;
    server_name 0.0.0.0;

    client_max_body_size 5M;

    access_log /usr/local/var/log/nginx/access.log combined;
    error_log /usr/local/var/log/nginx/error_log.log warn;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;

        proxy_pass http://gunicorn-app;
    }
}
```

```
sudo nginx -c [config_path]
sudo nginx -s stop
```

## Docker

When I dockerize, first setup the tools and environment necessary for dockerizing image. Then, enter console of the container, check the configuration, and run each application to verify normal operation.
Afrter verifcation is completed, write `CMD` or `ENTRYPOINT` COMMAND. 


##### `Dockerfile`
```dockerfile
FROM python:3.6.6-jessie

MAINTAINER cgex

ENV SRVHOME=/srv/app

WORKDIR $SRVHOME

COPY ./ $SRVHOME

RUN apt-get update && apt-get install -y \
    nginx \
    supervisor

COPY ./nginx/nginx.conf /etc/nginx/
COPY ./nginx/gunicorn-app.conf /etc/nginx/conf.d/

COPY ./gunicorn_config.py /etc/gunicorn/

COPY supervisord.conf /etc/supervisor/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80
EXPOSE 8080

# for receving stream of log 
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

CMD ["/usr/bin/supervisord"]

```


## REFERENCES
[gunicorn vs uwsgi](http://devspark.tistory.com/entry/gunicorn-vs-uwsgi)
[flask-concurrency-test](https://winterj.me/flask-concurrency-test/)


## LOG
