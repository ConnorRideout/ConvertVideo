from PyQt5.QtWidgets import (
    QDialogButtonBox,
    QSizePolicy,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QScrollArea,
    QSpacerItem,
    QToolButton,
    QCheckBox,
    QComboBox,
    QGroupBox,
    QLineEdit,
    QSpinBox,
    QWidget,
    QDialog,
    QLabel,
    QFrame
)
from PyQt5.QtCore import (
    QMetaObject,
    Qt
)


class Ui_Dialog(object):
    def setupUi(self, Dialog: QDialog):
        Dialog.setObjectName('Dialog')
        Dialog.setWindowTitle("Compress/Convert Video - Options")
        Dialog.setMinimumWidth(450)
        Dialog.setStyleSheet('QDialog {background-color: #202328;}\n'
                             'QWidget {font-size: 11pt;}')
        self.vLayout_main = QVBoxLayout(Dialog)
        self.vLayout_main.setSpacing(9)
        self.vLayout_main.setObjectName('vLayout_main')
        self.gBox_source = QGroupBox(Dialog)
        self.gBox_source.setTitle("Source")
        self.gBox_source.setStyleSheet('QGroupBox {\n'
                                       '    color: #849db8;\n'
                                       '    border: 1px solid #849db8;\n'
                                       '    text-decoration: underline;\n'
                                       '    padding: 6px 3px 3px 3px;\n'
                                       '    margin-top: 0.5em;\n'
                                       '}\n'
                                       'QGroupBox::title {\n'
                                       '    subcontrol-origin: margin;\n'
                                       '    subcontrol-position: left top;\n'
                                       '    left: 6px;\n'
                                       '}')
        self.gBox_source.setObjectName('gBox_source')
        self.vLayout_source = QVBoxLayout(self.gBox_source)
        self.vLayout_source.setContentsMargins(6, 6, 6, 6)
        self.vLayout_source.setObjectName('vLayout_source')
        self.lbl_source = QLabel(self.gBox_source)
        self.lbl_source.setWordWrap(True)
        self.lbl_source.setObjectName('lbl_source')
        self.vLayout_source.addWidget(self.lbl_source)
        self.vLayout_main.addWidget(self.gBox_source)
        self.lbl_message = QLabel(Dialog)
        self.lbl_message.setWordWrap(True)
        self.lbl_message.setObjectName('lbl_message')
        self.vLayout_main.addWidget(self.lbl_message)

        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName('scrollArea')
        self.scrollAreaContents = QWidget()
        self.scrollAreaContents.setStyleSheet('background-color: #2d3640;\n'
                                              'font-size: 10pt;')
        self.scrollAreaContents.setObjectName('scrollAreaContents')
        self.fLayout = QFormLayout(self.scrollAreaContents)
        self.fLayout.setVerticalSpacing(8)
        self.fLayout.setObjectName('fLayout')

        self.cmbBox_outFrmt = QComboBox(self.scrollAreaContents)
        self.cmbBox_outFrmt.setObjectName('cmbBox_outFrmt')
        self.fLayout.addRow("Output format", self.cmbBox_outFrmt)

        self.frame_webm = QFrame(self.scrollAreaContents)
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame_webm.sizePolicy().hasHeightForWidth())
        self.frame_webm.setSizePolicy(sizePolicy)
        self.frame_webm.setFrameShape(QFrame.NoFrame)
        self.frame_webm.setLineWidth(0)
        self.frame_webm.setObjectName('frame_webm')
        self.hLayout_webm = QHBoxLayout(self.frame_webm)
        self.hLayout_webm.setContentsMargins(0, 0, 0, 0)
        self.hLayout_webm.setSpacing(10)
        self.hLayout_webm.setObjectName('hLayout_webm')
        spacerItem = QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout_webm.addItem(spacerItem)
        self.lbl_webm = QLabel(self.scrollAreaContents)
        self.lbl_webm.setText("Webm cutoff (sec)")
        self.lbl_webm.setObjectName('lbl_webm')
        self.hLayout_webm.addWidget(self.lbl_webm)
        self.spinBox_webm = QSpinBox(self.scrollAreaContents)
        self.spinBox_webm.setRange(0, 3600)
        self.spinBox_webm.setWrapping(True)
        self.spinBox_webm.setObjectName('spinBox_webm')
        self.hLayout_webm.addWidget(self.spinBox_webm)
        self.hLayout_webm.setStretch(1, 1)
        self.hLayout_webm.setStretch(2, 2)
        self.fLayout.addRow(self.frame_webm)

        self.cmbBox_audStrm = QComboBox(self.scrollAreaContents)
        self.cmbBox_audStrm.setObjectName('cmbBox_audStrm')
        self.fLayout.addRow("Audio stream", self.cmbBox_audStrm)

        self.cmbBox_subStrm = QComboBox(self.scrollAreaContents)
        self.cmbBox_subStrm.setObjectName('cmbBox_subStrm')
        self.fLayout.addRow("Subtitle stream", self.cmbBox_subStrm)

        self.lbl_recurse = QLabel(self.scrollAreaContents)
        self.lbl_recurse.setText("Recurse folders")
        self.lbl_recurse.setObjectName('lbl_recurse')
        self.chkBox_recurse = QCheckBox(self.scrollAreaContents)
        self.chkBox_recurse.setObjectName('chkBox_recurse')
        self.fLayout.addRow(self.lbl_recurse, self.chkBox_recurse)

        self.chkBox_overwrite = QCheckBox(self.scrollAreaContents)
        self.chkBox_overwrite.setObjectName('chkBox_overwrite')
        self.fLayout.addRow("Overwrite originals", self.chkBox_overwrite)

        self.chkBox_keepFail = QCheckBox(self.scrollAreaContents)
        self.chkBox_keepFail.setObjectName('chkBox_keepFail')
        self.fLayout.addRow("Keep compression failures", self.chkBox_keepFail)

        self.frame_overwrite = QFrame(self.scrollAreaContents)
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame_overwrite.sizePolicy().hasHeightForWidth())
        self.frame_overwrite.setSizePolicy(sizePolicy)
        self.frame_overwrite.setFrameShape(QFrame.NoFrame)
        self.frame_overwrite.setLineWidth(0)
        self.frame_overwrite.setObjectName('frame_overwrite')
        self.hLayout_fail = QHBoxLayout(self.frame_overwrite)
        self.hLayout_fail.setContentsMargins(0, 0, 0, 0)
        self.hLayout_fail.setSpacing(10)
        self.hLayout_fail.setObjectName('hLayout_fail')
        spacerItem = QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout_fail.addItem(spacerItem)
        self.lbl_overwriteFail = QLabel(self.scrollAreaContents)
        self.lbl_overwriteFail.setText("Overwrite originals with failures")
        self.lbl_overwriteFail.setObjectName('lbl_overwriteFail')
        self.hLayout_fail.addWidget(self.lbl_overwriteFail)
        self.chkBox_overwriteFail = QCheckBox(
            self.scrollAreaContents)
        self.chkBox_overwriteFail.setObjectName('chkBox_overwriteFail')
        self.hLayout_fail.addWidget(self.chkBox_overwriteFail)
        self.hLayout_fail.setStretch(1, 1)
        self.hLayout_fail.setStretch(2, 2)
        self.fLayout.addRow(self.frame_overwrite)

        self.chkBox_keepError = QCheckBox(self.scrollAreaContents)
        self.chkBox_keepError.setObjectName('chkBox_keepError')
        self.fLayout.addRow("Keep errored files", self.chkBox_keepError)

        self.chkBox_doScale = QCheckBox(self.scrollAreaContents)
        self.chkBox_doScale.setObjectName('chkBox_doScale')
        self.fLayout.addRow("Scale to 720p", self.chkBox_doScale)

        self.chkBox_doCrop = QCheckBox(self.scrollAreaContents)
        self.chkBox_doCrop.setObjectName('chkBox_doCrop')
        self.fLayout.addRow("Crop blackspace", self.chkBox_doCrop)

        self.chkBox_doRename = QCheckBox(self.scrollAreaContents)
        self.chkBox_doRename.setObjectName('chkBox_doRename')
        self.fLayout.addRow("Rename ouput", self.chkBox_doRename)

        self.frame_rename = QFrame(self.scrollAreaContents)
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame_rename.sizePolicy().hasHeightForWidth())
        self.frame_rename.setSizePolicy(sizePolicy)
        self.frame_rename.setFrameShape(QFrame.NoFrame)
        self.frame_rename.setLineWidth(0)
        self.frame_rename.setObjectName('frame_rename')
        self.hLayout_rename = QHBoxLayout(self.frame_rename)
        self.hLayout_rename.setContentsMargins(0, 0, 0, 0)
        self.hLayout_rename.setSpacing(10)
        self.hLayout_rename.setObjectName('hLayout_rename')
        spacerItem = QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout_rename.addItem(spacerItem)
        self.lbl_rename = QLabel(self.scrollAreaContents)
        self.lbl_rename.setText("Remove from output filename (regex)")
        self.lbl_rename.setObjectName('lbl_rename')
        self.hLayout_rename.addWidget(self.lbl_rename)
        self.lineEdit_rename = QLineEdit(
            self.scrollAreaContents)
        self.chkBox_overwriteFail.setObjectName('lineEdit_rename')
        self.hLayout_rename.addWidget(self.lineEdit_rename)
        self.hLayout_rename.setStretch(1, 1)
        self.hLayout_rename.setStretch(2, 2)
        self.fLayout.addRow(self.frame_rename)

        self.toggleBtn = QToolButton(self.scrollAreaContents)
        self.toggleBtn.setText("Advanced Options")
        self.toggleBtn.setStyleSheet('QToolButton { border: none; }')
        self.toggleBtn.setCheckable(True)
        self.toggleBtn.setChecked(True)
        self.toggleBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggleBtn.setArrowType(Qt.RightArrow)
        self.toggleBtn.setObjectName('toggleBtn')
        self.fLayout.addRow(self.toggleBtn)

        self.frame_adv = QFrame(self.scrollAreaContents)
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame_adv.sizePolicy().hasHeightForWidth())
        self.frame_adv.setSizePolicy(sizePolicy)
        self.frame_adv.setFrameShape(QFrame.Panel)
        self.frame_adv.setFrameShadow(QFrame.Raised)
        self.frame_adv.setObjectName('frame_adv')
        self.fLayout_adv = QFormLayout(self.frame_adv)
        self.fLayout_adv.setContentsMargins(-1, -1, -1, -1)
        self.fLayout_adv.setHorizontalSpacing(20)
        self.fLayout_adv.setVerticalSpacing(8)
        self.fLayout_adv.setObjectName('fLayout_adv')

        self.chkBox_convVid = QCheckBox(self.frame_adv)
        self.chkBox_convVid.setObjectName('chkBox_convVid')
        self.fLayout_adv.addRow("Convert video", self.chkBox_convVid)

        self.frame_force = QFrame(self.frame_adv)
        sizePolicy = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame_force.sizePolicy().hasHeightForWidth())
        self.frame_force.setSizePolicy(sizePolicy)
        self.frame_force.setFrameShape(QFrame.NoFrame)
        self.frame_force.setLineWidth(0)
        self.frame_force.setObjectName('frame_force')
        self.hLayout_force = QHBoxLayout(self.frame_force)
        self.hLayout_force.setContentsMargins(0, 0, 0, 0)
        self.hLayout_force.setSpacing(10)
        self.hLayout_force.setObjectName('hLayout_force')
        spacerItem1 = QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout_force.addItem(spacerItem1)
        self.lbl_forceVid = QLabel(self.frame_adv)
        self.lbl_forceVid.setText("Force convert video")
        self.lbl_forceVid.setObjectName('lbl_forceVid')
        self.hLayout_force.addWidget(self.lbl_forceVid)
        self.chkBox_forceVid = QCheckBox(self.frame_adv)
        self.chkBox_forceVid.setObjectName('chkBox_forceVid')
        self.hLayout_force.addWidget(self.chkBox_forceVid)
        self.hLayout_force.setStretch(1, 1)
        self.hLayout_force.setStretch(2, 2)
        self.fLayout_adv.addRow(self.frame_force)

        self.chkBox_convAud = QCheckBox(self.frame_adv)
        self.chkBox_convAud.setObjectName('chkBox_convAud')
        self.fLayout_adv.addRow("Convert audio", self.chkBox_convAud)

        self.chkBox_convSub = QCheckBox(self.frame_adv)
        self.chkBox_convSub.setText("")
        self.chkBox_convSub.setObjectName('chkBox_convSub')
        self.fLayout_adv.addRow("Convert subtitles", self.chkBox_convSub)

        self.lbl_threads = QLabel(self.frame_adv)
        self.lbl_threads.setText("Thread count")
        self.lbl_threads.setObjectName('lbl_threads')
        self.spinBox_threads = QSpinBox(self.frame_adv)
        self.spinBox_threads.setRange(1, 5)
        self.spinBox_threads.setWrapping(True)
        self.spinBox_threads.setObjectName('spinBox_thread')
        self.fLayout_adv.addRow(self.lbl_threads, self.spinBox_threads)

        self.lineEdit_addArgs = QLineEdit(self.frame_adv)
        self.lineEdit_addArgs.setObjectName('lineEdit_addArgs')
        self.fLayout_adv.addRow("Additional arguments", self.lineEdit_addArgs)

        self.fLayout.addRow(self.frame_adv)

        self.scrollArea.setWidget(self.scrollAreaContents)
        self.vLayout_main.addWidget(self.scrollArea)
        self.btnbox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btnbox.setCenterButtons(True)
        self.btnbox.setObjectName('btnbox')
        self.vLayout_main.addWidget(self.btnbox)

        QMetaObject.connectSlotsByName(Dialog)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
