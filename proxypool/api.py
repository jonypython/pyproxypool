from flask import Flask, g
from proxypool.db import RedisClient

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()

    return g.redis


@app.route('/')
def index():
    return '<h2> Wecome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    随机获取代理
    :return:
    """
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_count():
    """
    获取代理池总数
    :return:
    """
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run()
