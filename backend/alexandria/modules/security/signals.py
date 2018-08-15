from blinker import Namespace
__author__ = 'oclay'

signals = Namespace()

login_success = signals.signal('login_success')
