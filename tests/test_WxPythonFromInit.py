import sys
import threading
from time import sleep
from unittest import TestCase

import wx

import asn1editor


def delay():
    sleep(1)
    wx.GetApp().GetTopWindow().Close(True)

    wx.GetApp().ExitMainLoop()


class WxPythonFromInit(TestCase):
    @staticmethod
    def test_open():
        action_thread = threading.Thread(target=delay, args=[])
        action_thread.start()

        sys.argv = ['asn1editor']
        asn1editor._wx_python_editor()
        action_thread.join(timeout=0.0)
