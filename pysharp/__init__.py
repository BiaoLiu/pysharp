from __future__ import absolute_import
import pymysql
from .celery import app as celery_app

pymysql.install_as_MySQLdb()

