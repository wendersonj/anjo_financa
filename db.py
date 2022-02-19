from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
POSTGRES = {
    'user': 'admin',
    'pw': '123456',
    'db': 'anjo_financa',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
'''

sql_uri = 'sqlite:///bills.sqlite3'

