"""
 Created by zjl on 2020/9/24 0:20
"""
from wsgiref.simple_server import make_server

from app import create_app
from gevent import pywsgi
from scrapy import cmdline

__author__ = 'zjl'


app = create_app()


@app.route('/test')
def test():
    return 'come on'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=82)