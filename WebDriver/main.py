import threading

import yileixuefen
from WebDriver import erleixuefen1

if __name__ == '__main__':

    t2 = threading.Thread(erleixuefen1.run())
    # t1.start()
    t2.start()
    yileixuefen.run()

