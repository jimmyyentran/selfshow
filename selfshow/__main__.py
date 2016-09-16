import sys
import os
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainwindow import Ui_MainWindow
from model import Model

DB_DIR = ".selfspy"
DB_NAME = "selfspy.sqlite"

# set up loggers
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
        level=logging.DEBUG)
log = logging.getLogger(__name__)

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

db_path = os.path.join(os.path.expanduser("~"), DB_DIR, DB_NAME)
if(os.path.exists(db_path)):
    log.info("DB file: {}".format(db_path))
    #  ss = stats.Selfstats(db_path, 
            #  {'key_freqs': False, 'process': None, 'back': None, 'date': None, 'periods':
                #  None, 'showtext': False, 'id': None, 'password': None, 'data_dir':
                #  '/Users/jimmytran/.selfspy', 'clock': None, 'config': None, 'clicks': False,
                #  'body': None, 'human_readable': False, 'pactive': None, 'tactive': None,
                #  'ratios': None, 'active': None, 'min_keys': None, 'tkeys': False, 'title':
                #  None, 'limit': None, 'pkeys': False})
    #  ss.do()
else:
    print("exit")
    exit()

mod = Model(db_path)
ui.graphicsView.setData(mod.query_keys())
ui.graphicsView.run()

window.show()
sys.exit(app.exec_())
