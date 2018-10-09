import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
access_logfile = "-"
error_logfile = "-"
worker_class = "gevent"
