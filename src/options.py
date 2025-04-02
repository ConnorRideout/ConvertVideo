from typing import TYPE_CHECKING
from subprocess import run

from .inputdialog import InputDialog
from ..lib.variables import *

if TYPE_CHECKING:
    from PyQt5.QtWidgets import (
        QComboBox,
        QLineEdit,
        QSpinBox
    )


class Options:
    isdir: bool = False
    output: str = ""
    playtime: str = CUTOFF
    aud_strm: str = list(AUD_LANGS)[0]
    sub_strm: str = list(SUB_LANGS)[0]
    recurse: bool = RECURSE
    overwrite: bool = OVERWRITE
    keep_fail: bool = KEEP_FAIL
    overwrite_fail: bool = OVERWRITE_FAIL
    keep_error: bool = KEEP_ERROR
    do_scale: bool = DO_SCALE
    do_crop: bool = DO_CROP
    do_rename: bool = RENAME
    rename_regex: str = RENAME_REGEX
    rename_to: str = RENAME_TO
    vid: bool = True
    force_vid: bool = False
    aud: bool = True
    sub: bool = True
    thread_ct: int = THREADS
    add_params: str = ADD_PARAMS

    @classmethod
    def getInput(cls, fpath: Path) -> bool:
        def adjustSize(wgt: U["QComboBox", "QSpinBox", "QLineEdit"]):
            wgt.adjustSize()
            wgt.setMinimumHeight(round(wgt.height() * 1.3))
            return

        InDlg = InputDialog()
        if fpath.is_dir():
            cls.isdir = True
            InDlg.lbl_source.setText(str(fpath))
            InDlg.lbl_message.setText(
                f"Compress/Convert {', '.join(FTYPES)} files within this directory.")
            InDlg.cmbBox_outFrmt.addItems(["auto", ".mkv", ".mp4", ".webm"])
            InDlg.cmbBox_outFrmt.setCurrentIndex(1)
            adjustSize(InDlg.cmbBox_outFrmt)
            InDlg.spinBox_webm.setValue(cls.playtime)
            adjustSize(InDlg.spinBox_webm)
            InDlg.chkBox_recurse.setChecked(cls.recurse)
            InDlg.spinBox_threads.setRange(1, (5 if NVENC else 20))
            InDlg.spinBox_threads.setValue(cls.thread_ct)
            adjustSize(InDlg.spinBox_threads)
        else:
            InDlg.lbl_webm.hide()
            InDlg.spinBox_webm.hide()
            InDlg.lbl_recurse.hide()
            InDlg.chkBox_recurse.hide()
            InDlg.lbl_threads.hide()
            InDlg.spinBox_threads.hide()

            InDlg.lbl_source.setText(fpath.name)
            InDlg.lbl_message.setText("Compress/Convert this file.")
            dur: str = run(['ffprobe', '-v', 'error', '-show_entries',
                            'format=duration', '-of', 'csv=p=0', '-i', fpath],
                           capture_output=True,
                           text=True).stdout
            InDlg.cmbBox_outFrmt.addItems([".mkv", ".mp4", ".webm"])
            InDlg.cmbBox_outFrmt.setCurrentIndex(
                0 if float(dur) >= cls.playtime else 2)
        InDlg.cmbBox_audStrm.addItems(["all",
                                       "all listed",
                                       *list(AUD_LANGS),
                                       *[str(i) for i in range(STREAMS)]])
        InDlg.cmbBox_audStrm.setCurrentIndex(2)
        adjustSize(InDlg.cmbBox_audStrm)
        InDlg.cmbBox_subStrm.addItems(["all",
                                       "all listed",
                                       "remove",
                                       *list(SUB_LANGS),
                                       *[str(i) for i in range(STREAMS)]])
        InDlg.cmbBox_subStrm.setCurrentIndex(3)
        adjustSize(InDlg.cmbBox_subStrm)
        InDlg.chkBox_overwrite.setChecked(cls.overwrite)
        InDlg.chkBox_keepFail.setChecked(cls.keep_fail)
        InDlg.chkBox_overwriteFail.setChecked(cls.overwrite_fail)
        InDlg.chkBox_keepError.setChecked(cls.keep_error)
        InDlg.chkBox_doScale.setChecked(cls.do_scale)
        InDlg.chkBox_doCrop.setChecked(cls.do_crop)
        InDlg.chkBox_doRename.setChecked(cls.do_rename)
        InDlg.lineEdit_rename.setText(cls.rename_regex)
        adjustSize(InDlg.lineEdit_rename)
        InDlg.lineEdit_rename_to.setText(cls.rename_to)
        adjustSize(InDlg.lineEdit_rename_to)
        InDlg.chkBox_convVid.setChecked(cls.vid)
        InDlg.chkBox_forceVid.setChecked(cls.force_vid)
        InDlg.chkBox_convAud.setChecked(cls.aud)
        InDlg.chkBox_convSub.setChecked(cls.sub)
        InDlg.lineEdit_addArgs.setText(cls.add_params)
        adjustSize(InDlg.lineEdit_addArgs)
        # show/hide frames
        InDlg._changed_output(InDlg.cmbBox_outFrmt.currentText())
        InDlg._clicked_overwrite()
        InDlg._clicked_rename()

        # run
        ans = InDlg.run()
        if ans:
            cls.output = ans['Output format']
            cls.playtime = ans['Webm cutoff (sec)']
            cls.aud_strm = ans['Audio stream']
            cls.sub_strm = ans['Subtitle stream']
            cls.recurse = ans['Recurse folders']
            cls.overwrite = ans['Overwrite original']
            cls.keep_fail = ans['Keep compression failures']
            cls.overwrite_fail = ans['Overwrite original with failure']
            cls.keep_error = ans['Keep errored files']
            cls.do_scale = ans['Scale to 720p']
            cls.do_crop = ans['Crop blackspace']
            cls.do_rename = ans['Rename ouput']
            cls.rename_regex = ans['Rename regex']
            cls.rename_to = ans["Rename to"]
            cls.vid = ans['Convert video']
            cls.force_vid = ans['Force convert video']
            cls.aud = ans['Convert audio']
            cls.sub = ans['Convert subtitles']
            cls.thread_ct = ans['Thread count']
            cls.add_params = ans['Additional arguments']
            return True
        else:
            return False

    @classmethod
    def getInfo(cls) -> list[str]:
        out = [f"Running threads: {cls.thread_ct}"] if cls.isdir else list()
        if not cls.vid:
            out.append("Convert video: NO")
        elif cls.force_vid:
            out.append("Force convert video: YES")
        if not cls.aud:
            out.append("Convert audio: NO")
        if not cls.sub:
            out.append("Convert subtitles: NO")
        out.append(f"Output format: {cls.output.lstrip('.').upper()}")
        if cls.output == 'auto':
            out.append(f"Playtime cutoff: {cls.playtime}s")
        out += [
            f"Audio stream: {cls.aud_strm.upper()}",
            f"Subtitle stream: {cls.sub_strm.upper()}"
        ]
        if cls.isdir:
            out.append(f"Recurse folders: {'YES' if cls.recurse else 'NO'}")
        out += [
            f"Overwrite originals: {'YES' if cls.overwrite else 'NO'}",
            f"Keep failures: {'YES' if cls.keep_fail else 'NO'}"
        ]
        if cls.keep_fail:
            out.append(
                f"Overwrite w/ fails: {'YES' if cls.overwrite_fail else 'NO'}")
        out += [
            f"Keep errors: {'YES' if cls.keep_error else 'NO'}",
            f"Scale to 720p: {'YES' if cls.do_scale else 'NO'}",
            f"Crop blackspace: {'YES' if cls.do_crop else 'NO'}",
            f"Rename output: {'YES' if cls.do_rename else 'NO'}",
        ]
        if CON_WD > 53:
            if len(out) % 2:
                out.append("")
            out = [f"{a:<24} | {b:<24}"
                   for (a, b) in [out[i: i + 2] for i in range(0, len(out), 2)]]
        else:
            out = [f"{s:<24}" for s in out]
        return ["", f"{' Options: ':-^{51}}", *out]
