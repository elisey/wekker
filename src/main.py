import signal

from app import Application

if __name__ == '__main__':

    application = Application()
    signal.signal(signal.SIGINT, application.stop)
    signal.signal(signal.SIGTERM, application.stop)
    application.run()

