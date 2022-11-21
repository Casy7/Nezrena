from ..common.functions import SingletonMeta
from os.path import basename, join
import subprocess

class IMAPSubscription(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.success = False
        self.IMAP_subscription()

    def IMAP_subscription(self):
        if not self.success:
            self.success = True
            p = subprocess.Popen(('node', join(basename(__file__), '../mail_module')))

            print("Subscription is issued")
            


