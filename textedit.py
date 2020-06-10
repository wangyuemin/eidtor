from PyQt5.QtCore import (QFile, QFileInfo, QIODevice,
        QTextStream, Qt)
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QFileDialog, QMessageBox, QTextEdit)
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PyQt5.QtGui import QColor, QPainter, QTextFormat
languageList=['JPN','ENU','CHS','CHT','CSY','DAN','DEU','ESP','FIN','FRA','HUN','ITA','NLD','NOR','PLK','PTB','PTG','RUS','SVE','ELL','KOR','TRK']
L_dict={'CAT':'windows-1252','CHS':'GB2312','CHT':'Big5','CSY':'Windows-1250','DAN':'Windows-1252','DEU':'Windows-1252','ELL':'Windows-1253','ENU':'Windows-1252','ESP':'Windows-1252','FIN':'Windows-1252','FRA':'Windows-1252','HUN':'Windows-1250','ITA':'Windows-1252','JPN':'shift_jis','KOR':'Windows 949','NLD':'Windows-1252','NOR':'Windows-1252','PLK':'Windows-1250','PTB':'Windows-1252','PTG':'Windows-1252','RUS':'Windows-1251','SVE':'Windows-1252','TRK':'Windows-1254'}
class MyQTextEdit(QPlainTextEdit):
    """description of class"""
    #============================================================
    def __init__(self):
         super(MyQTextEdit,self).__init__()
         self.zoomsize=2
         self.ctrlPressed=False
    def wheelEvent(self, event):#this is the rewrite of the function
       if  self.ctrlPressed:    #if the ctrl key is pressed: then deal with the defined process
          delta=event.angleDelta()
          oriention= delta.y()/8
          self.zoomsize=0
          if oriention>0:
                self.zoomsize+=1
          else:
                 self.zoomsize-=1
          self.zoomIn(self.zoomsize)
          print(self.zoomsize)
       else:   #if the ctrl key isn't pressed then submiting                   the event to it's super class
          return super().wheelEvent(event)

    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key()==QtCore.Qt.Key_Control:
            self.ctrlPressed=False
        return super().keyReleaseEvent(QKeyEvent)
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key()==QtCore.Qt.Key_Control:
            self.ctrlPressed=True
            print("The ctrl key is holding down")
        return super().keyPressEvent(QKeyEvent)
class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class QCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
		#super(QCodeEditor, self).__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.zoomsize=2
        self.ctrlPressed=False

    def wheelEvent(self, event):#this is the rewrite of the function
       if  self.ctrlPressed:    #if the ctrl key is pressed: then deal with the defined process
          delta=event.angleDelta()
          oriention= delta.y()/8
          self.zoomsize=0
          if oriention>0:
                self.zoomsize+=1
          else:
                 self.zoomsize-=1
          self.zoomIn(self.zoomsize)
          print(self.zoomsize)
       else:   #if the ctrl key isn't pressed then submiting                   the event to it's super class
          return super().wheelEvent(event)

    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key()==QtCore.Qt.Key_Control:
            self.ctrlPressed=False
        return super().keyReleaseEvent(QKeyEvent)
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key()==QtCore.Qt.Key_Control:
            self.ctrlPressed=True
            print("The ctrl key is holding down")
        return super().keyPressEvent(QKeyEvent)

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1
class TextEdit(QCodeEditor):

    NextId = 1

    def __init__(self, filename="", parent=None):
        super(TextEdit, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.filename = filename
        if not self.filename:
            self.filename = "Unnamed-{0}.txt".format(
                                    TextEdit.NextId)
            TextEdit.NextId += 1
        #print(self.document())
        self.document().setModified(False)
        self.setWindowTitle(QFileInfo(self.filename).fileName())
    def codeingName(self,filename):
        pathList=filename.split('/')
        lanSum=0
        for lan in pathList:
            if lan in languageList:
                lanSum+=1
                lanName=lan
            else:
                pass
        if lanSum==1:
            if filename.split('.')[-1]=='xml':
                return("utf_8")
            elif filename.split('.')[-1]=='ALI':
                return("GBK")
            else:
                return(L_dict[lanName])

    def closeEvent(self, event):
        if (self.document().isModified() and
            QMessageBox.question(self,
                   "Text Editor - Unsaved Changes",
                   "Save unsaved changes in {0}?".format(self.filename),
                   QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.Yes):
            try:
                self.save()
            except EnvironmentError as e:
                QMessageBox.warning(self,
                        "Text Editor -- Save Error",
                        "Failed to save {0}: {1}".format(self.filename, e))
    def isModified(self):
        return self.document().isModified()


    def save(self):
        if self.filename.startswith("Unnamed"):
            filename,filetype = QFileDialog.getSaveFileName(self,
                    "Text Editor -- Save File As", self.filename,
                    "Text files (*.txt *.*)")
            if not filename:
                return
            self.filename = filename
        self.setWindowTitle(QFileInfo(self.filename).fileName())
        exception = None
        fh = None
        try:
            fh = QFile(self.filename)
            #print(fh)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec(self.codeingName(self.filename))
            stream << self.toPlainText()
            self.document().setModified(False)
        except EnvironmentError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception
    def load(self):
        #print('77')
        exception = None
        fh = None
        try:
            fh = QFile(self.filename)
            #print(self.filename)
            #print(fh)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec(self.codeingName(self.filename))
            self.setPlainText(stream.readAll())
            #print(self.document().toPlainText())
            self.document().setModified(False)
        except EnvironmentError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception

