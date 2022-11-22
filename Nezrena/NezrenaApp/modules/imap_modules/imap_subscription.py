from ..common.functions import SingletonMeta
# from ....NezrenaProject.settings import BASE_DIR
from os.path import dirname, join
import subprocess

class IMAPSubscription(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.success = False
        self.IMAP_subscription()

    def IMAP_subscription(self):
        if not self.success:
            self.success = True

            p = subprocess.Popen(('node', join(dirname(dirname(__file__)), 'mail_module', 'index.js')))

            print("Subscription is issued")
            


