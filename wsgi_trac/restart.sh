#!/bin/sh

PIDFILE="/home/user/trac/gunicorn.pid"
PYTHON_PATH="/home/user/.virtualenvs/gunicorn-trac/bin/python"
GUNICORN="/home/user/.virtualenvs/gunicorn-trac/bin/gunicorn"

kill -TERM `cat ${PIDFILE}` > /dev/null 2>&1
if [ $? -eq 0 ]
then
    rm ${PIDFILE}
    sleep 2
    cd /home/user/trac ; ${PYTHON_PATH} ${GUNICORN} -w 2 tracwsgi:application -b 0.0.0.0:8000 -p ${PIDFILE} > /dev/null 2>&1 &
else
    echo "停止に失敗しました"
fi

