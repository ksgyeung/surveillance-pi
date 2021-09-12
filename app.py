from os import path

from serveillance import servillance
from serveillance import globalvar

from surveillance import surveillance

if __name__ == '__main__':
    #globalvar.ROOT = path.dirname(path.abspath(__file__))
    #servillance.run()
    surveillance.run(
        root=path.dirname(path.abspath(__file__))
    )