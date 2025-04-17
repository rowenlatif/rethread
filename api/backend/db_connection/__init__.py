from flask_mysqldb import MySQL
from pymysql import cursors

db = MySQL(cursorclass=cursors.DictCursor)