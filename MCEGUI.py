__author__ = 'vitalyantonenko'

from GUIApp import GUIApp

if __name__ == '__main__':

    g = GUIApp('GUI/GUIv2.html', width=1275)
    # g = GUIApp('GUI/test-jquery-bubble-popup.html', width=1275)
    g.main_loop()


