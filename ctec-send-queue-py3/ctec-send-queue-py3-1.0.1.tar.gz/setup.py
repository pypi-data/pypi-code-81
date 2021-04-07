import distutils.core

version = '1.0.1'

distutils.core.setup(
        name='ctec-send-queue-py3',
        version=version,
        packages=['SendMsgToQueue', 'SendMsgToQueue.Tools'],
        author='ZhongZhijie',
        author_email='zhongzj@chinatelecom.cn',
        url='http://www.189.cn',
        description='189 send message to rabbitMQ',
        requires=['pika', 'gevent', 'Flask', 'DBUtils']
)
