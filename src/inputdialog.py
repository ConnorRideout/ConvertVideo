from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from typing import (
    Union as U,
    Optional as O
)

from .ui_convoptions import Ui_Dialog
from winnotify import PlaySound


class InputDialog(Ui_Dialog):
    out: dict[str, U[str, int, bool]] = None

    def __init__(self):
        self.dlg = QDialog()
        self.setupUi(self.dlg)
        self.frame_adv.hide()

        self.cmbBox_outFrmt.currentTextChanged.connect(self._changed_output)
        self.chkBox_overwrite.released.connect(self._clicked_overwrite)
        self.chkBox_keepFail.released.connect(self._clicked_overwrite)
        self.chkBox_doRename.released.connect(self._clicked_rename)
        self.toggleBtn.released.connect(self._clicked_advanced)
        self.chkBox_convVid.released.connect(self._clicked_conv_vid)
        self.btnbox.accepted.connect(self._submit)
        self.btnbox.rejected.connect(self._cancel)

    def _changed_output(self, value: str):
        if value == "auto":
            self.frame_webm.show()
        elif not self.frame_webm.isHidden():
            self.frame_webm.hide()

    def _clicked_overwrite(self):
        if self.chkBox_overwrite.isChecked() and self.chkBox_keepFail.isChecked():
            self.frame_overwrite.show()
        elif not self.frame_overwrite.isHidden():
            self.frame_overwrite.hide()

    def _clicked_rename(self):
        if self.chkBox_doRename.isChecked():
            self.frame_rename.show()
        elif not self.frame_rename.isHidden():
            self.frame_rename.hide()

    def _clicked_advanced(self):
        if self.toggleBtn.isChecked():
            self.toggleBtn.setArrowType(Qt.RightArrow)
            self.frame_adv.hide()
        else:
            self.toggleBtn.setArrowType(Qt.DownArrow)
            self.frame_adv.show()

    def _clicked_conv_vid(self):
        if self.chkBox_convVid.isChecked():
            self.frame_force.show()
        else:
            self.frame_force.hide()

    def _submit(self):
        self.out = {
            "Output format": self.cmbBox_outFrmt.currentText(),
            "Webm cutoff (sec)": self.spinBox_webm.value() if self.cmbBox_outFrmt.currentText() in ['webm', 'auto'] else None,
            "Audio stream": self.cmbBox_audStrm.currentText(),
            "Subtitle stream": self.cmbBox_subStrm.currentText(),
            "Recurse folders": self.chkBox_recurse.isChecked(),
            "Overwrite original": self.chkBox_overwrite.isChecked(),
            "Keep compression failures": self.chkBox_keepFail.isChecked(),
            "Overwrite original with failure": self.chkBox_overwriteFail.isChecked() if self.chkBox_keepFail.isChecked() and self.chkBox_overwrite.isChecked() else None,
            "Keep errored files": self.chkBox_keepError.isChecked(),
            "Scale to 720p": self.chkBox_doScale.isChecked(),
            "Crop blackspace": self.chkBox_doCrop.isChecked(),
            "Rename ouput": self.chkBox_doRename.isChecked(),
            "Rename regex": self.lineEdit_rename.text() if self.chkBox_doRename.isChecked() else None,
            "Rename to": self.lineEdit_rename_to.text() if self.chkBox_doRename.isChecked() else None,
            "Convert video": self.chkBox_convVid.isChecked(),
            "Force convert video": self.chkBox_forceVid.isChecked() if self.chkBox_convVid.isChecked() else None,
            "Convert audio": self.chkBox_convAud.isChecked(),
            "Convert subtitles": self.chkBox_convSub.isChecked(),
            "Thread count": self.spinBox_threads.value(),
            "Additional arguments": self.lineEdit_addArgs.text()
        }
        self.dlg.close()

    def _cancel(self):
        self.dlg.close()

    def run(self) -> O[dict[str, U[str, int, bool]]]:
        PlaySound("Beep")
        self.dlg.exec()
        return self.out
