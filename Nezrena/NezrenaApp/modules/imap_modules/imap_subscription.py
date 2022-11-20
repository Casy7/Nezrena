from ..common.functions import SingletonMeta
import os
import subprocess

class IMAPSubscription(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.success = False
        self.IMAP_subscription()

    def IMAP_subscription(self):
        if not self.success:
            self.success = True
            p = subprocess.Popen(('python', 'Z:/Progs/Nezrena/Nezrena/NezrenaApp/modules/imap_modules/subscribe.py'))

            print("Subscription is issued")
            


