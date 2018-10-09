# flask gunicorn nginx docker

python 3.6.4

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

#### 3프로세스 3쓰레드 성능 측정 

```
$ gunicorn -w 3 wsgi:app -b 0.0.0.0:5000
...
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
SELO
at ~/Project/flask-uwsgi-nginx-docker
$ ab -n 32 -c 16 127.0.0.1:5000/sleep/10
This is ApacheBench, Version 2.3 <$Revision: 1807734 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient).....done


Server Software:        gunicorn/19.9.0
Server Hostname:        127.0.0.1
Server Port:            5000

Document Path:          /sleep/10
Document Length:        19 bytes

Concurrency Level:      16
Time taken for tests:   40.023 seconds
Complete requests:      32
Failed requests:        0
Total transferred:      5728 bytes
HTML transferred:       608 bytes
Requests per second:    0.80 [#/sec] (mean)
Time per request:       20011.603 [ms] (mean)
Time per request:       1250.725 [ms] (mean, across all concurrent requests)
Transfer rate:          0.14 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.3      0       1
Processing: 10001 15946 4991.4  20007   20014
Waiting:    10001 15945 4991.6  20006   20014
Total:      10002 15946 4991.2  20007   20015

Percentage of the requests served within a certain time (ms)
  50%  20007
  66%  20008
  75%  20010
  80%  20013
  90%  20013
  95%  20015
  98%  20015
  99%  20015
 100%  20015 (longest request)
```

#### main configuration
* threads
	* This setting only affects the Gthread worker type.

* access-logfile
	* `-` means log to stdout	

* access-logformat
	* default: `%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"`

* error-logfile
	* `-` means log to stderr 	


```
$ gunicorn -w 3 --access-logfile - -k gevent wsgi:app -b 0.0.0.0:5000
```

```
$ gunicorn --config gunicorn_config.py wsgi:app
```


## REFERENCES
[gunicorn vs uwsgi](http://devspark.tistory.com/entry/gunicorn-vs-uwsgi)
[flask-concurrency-test](https://winterj.me/flask-concurrency-test/)

