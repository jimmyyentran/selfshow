import sys
import os
from PyQt4.Qt import QApplication, QDialog, QWidget, QMainWindow
from mainwindow import Ui_MainWindow
import selfspy.stats as stats

DB_DIR = ".selfspy"
DB_NAME = "selfspy.sqlite"

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

db_path = os.path.join(os.path.expanduser("~"), DB_DIR, DB_NAME)
print db_path
if(os.path.exists(db_path)):
    ss = stats.Selfstats(db_path, 
            {'key_freqs': False, 'process': None, 'back': None, 'date': None, 'periods':
                None, 'showtext': False, 'id': None, 'password': None, 'data_dir':
                '/Users/jimmytran/.selfspy', 'clock': None, 'config': None, 'clicks': False,
                'body': None, 'human_readable': False, 'pactive': None, 'tactive': None,
                'ratios': None, 'active': None, 'min_keys': None, 'tkeys': False, 'title':
                None, 'limit': None, 'pkeys': False})
    ss.do()
else:
    print("exit")
    exit()

window.show()
sys.exit(app.exec_())
