#
# A quick-and-dirty scraper for a web interface using HTML forms.
#
# Note, this is my first time using Qt.  Many thanks to StackOverflow.
#
# Usage:
#   python clb-scraper.py URL_TO_SCRAPE > output.tsv
# 
# Convert tab-separated output to CSV with tr, grep, and sed:
#   tr "\t" "," < output.tsv |grep -v "X,Sorted By: "|grep -v ",PPN,Street"|grep -v -e'^$' |sed -e's/,\(.*\),Parcel Map/\1/g' > output.csv
#
# Convert tab-separated output to CSV with awk:
#   awk -F "\t" '$2~/[0-9]+/{line="";for(i=2;i<NF;i++){if(i>2){line=line","}line=line$i}print line}' output.tsv > output.csv
#

import sys
import signal
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import QWebPage

COLUMN_DELIMITER = "\t"
LINE_DELIMITER = "\n"
REQUEST_SLEEP_TIME = 1


class WebPage(QWebPage):
   def __init__(self, url):        
   """
   Set up the Qt application and connect signal handler.
   """
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.connect(self, SIGNAL('loadFinished(bool)'), self._finished_loading)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

   def _finished_loading(self, result):
   """
   Set up signal handler that will fire when each page finishes loading.
   For this scraper, we scrape each page as it loads and then decide
   whether to get the next page of records or quit.
   """
        # scraping action
        #print unicode(page.mainFrame().toHtml().toUtf8(), encoding="UTF-8") #debug
        table = self.mainFrame().findFirstElement("table[summary='cityport']")
        print table_to_text(table)
        # get the button that loads the next page of records
        button = self.mainFrame().findFirstElement("input[value='>']")
        button_name = str(button.attribute("name"))
        # terminating condition: input button has the name PME_sys_disablednavop
        if not "PME_sys_disablednavop" in button_name:
            button.evaluateJavaScript("this.click()")
            time.sleep(REQUEST_SLEEP_TIME) # just to be polite to the server
        else:
            self.app.quit()

def cells_to_text(cells):
"""
Convert a QWebElementSet to a line of text.
"""
    line = []
    for cell in cells:
        line.append(str(cell.toPlainText().toUtf8()))
    return COLUMN_DELIMITER.join(line)

def table_to_text(table):
"""
Convert a QWebElement containing a table to lines of text.
"""
    lines = []
    # process headers
    ths = table.findAll("th")
    lines.append(cells_to_text(ths))
    # process rows
    trs = table.findAll("tr")
    for tr in trs:
        tds = tr.findAll("td")
        lines.append(cells_to_text(tds))
    return LINE_DELIMITER.join(lines)

if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        print 'Usage: %s url' % sys.argv[0]
    else:
	# initialize
        page = WebPage(url)

