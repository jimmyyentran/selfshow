import numpy as np
import pyqtgraph as pg
from pyqtgraph.graphicsItems.AxisItem import AxisItem
from pyqtgraph.Qt import QtGui
from pyqtgraph.graphicsItems.GraphicsLayout import GraphicsLayout
from pyqtgraph.widgets.GraphicsView import GraphicsView

class TimeAxisItem(AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #  super(TimeAxisItem, self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        # PySide's QTime() initialiser fails miserably and dismisses args/kwargs
        #return [QTime().addMSecs(value).toString('mm:ss') for value in values]
        return [int2dt(value).strftime("%H:%M:%S.%f") for value in values]


class KeyStrokeWidget(GraphicsView):
    """
    Holds an instance of GraphicsLayout element as the central item. Also wraps
    some functionalities as described in class
    pyqtgraph.widgets.GraphicsLayoutWidget.

    Attributes:
        parent: parent GUI object

    """
    def __init__(self, parent=None, **kargs):
        GraphicsView.__init__(self, parent)
        self.ci = GraphicsLayout(**kargs)
        for n in ['nextRow', 'nextCol', 'nextColumn', 'addPlot', 'addViewBox',
                'addItem', 'getItem', 'addLayout', 'addLabel', 'removeItem',
                'itemIndex', 'clear']:
            setattr(self, n, getattr(self.ci, n))
        self.setCentralItem(self.ci)

    def run(self):
        win = self

        win.setWindowTitle('pyqtgraph example: crosshair')
        self.label = pg.LabelItem(justify='right')
        win.addItem(self.label)
        #  self.p1 = win.addPlot(row=1, col=0,
            #  axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.p1 = win.addPlot(row=1, col=0)
        self.p2 = win.addPlot(row=2, col=0)

        self.region = pg.LinearRegionItem()
        self.region.setZValue(10)
        # Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this 
        # item when doing auto-range calculations.
        self.p2.addItem(self.region, ignoreBounds=True)

        #pg.dbg()
        self.p1.setAutoVisible(y=True)


        #create numpy arrays
        #make the numbers large to show that the xrange shows data from 10000 to all the way 0
        #  self.data1 = 10000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
        #  self.data2 = 15000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)

        self.p1.plot(self.data1, pen="r")
        #  self.p1.plot = self.win.addPlot(title='Timed data', axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        #  self.p1.plot(self.data2, pen="g")

        self.p2.plot(self.data1, pen="w")

        self.region.sigRegionChanged.connect(self.update)

        self.p1.sigRangeChanged.connect(self.updateRegion)

        #  self.region.setRegion([1000, 2000])

        #cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.p1.addItem(self.vLine, ignoreBounds=True)
        self.p1.addItem(self.hLine, ignoreBounds=True)


        self.vb = self.p1.vb
        proxy = pg.SignalProxy(self.p1.scene().sigMouseMoved, rateLimit=60,
                slot=self.mouseMoved)

        self.p1.scene().sigMouseMoved.connect(self.mouseMoved)

    def update(self):
        self.region.setZValue(10)
        minX, maxX = self.region.getRegion()
        self.p1.setXRange(minX, maxX, padding=0)    

    def updateRegion(self, window, viewRange):
        rgn = viewRange[0]
        self.region.setRegion(rgn)

    def mouseMoved(self, evt):
        #  pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        pos = evt.toPoint()
        if self.p1.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            if index > 0 and index < self.data1[-1]['x']:
                self.label.setText(
                        #  """<span style='font-size: 12pt'>x=%f, 
                        #  <span style='color: red'>y1=%0.1f</span>,
                        #  <span style='color: green'>y2=%0.1f</span>
                        #  """ % (mousePoint.x(),
                        """<span style='font-size: 12pt'>x=%i, 
                        <span style='color: red'>y1=%i</span>
                        """ % (mousePoint.x(),
                            mousePoint.y()))
                        #  self.data1[index], self.data2[index]))
                        #  self.data1[index]))
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())

    def setData(self, data):
        self.data1 = data

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
