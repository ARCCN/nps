__author__ = 'vitalyantonenko'

from GUIApp import GUIApp
import os

if __name__ == '__main__':

    os.system('lsof -i:6633 | tail -1 | awk \'{print $2}\' | xargs kill -9')
    os.system('lsof -i:56565 | tail -1 | awk \'{print $2}\' | xargs kill -9')

    g = GUIApp('GUI/GUIv2.html', width=1275)
    #g = GUIApp('GUI/api-candy.html', width=1275)
    g.main_loop()


