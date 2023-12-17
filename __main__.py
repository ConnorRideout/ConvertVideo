from concurrent.futures import ThreadPoolExecutor
from textwrap import TextWrapper
from sys import argv as sys_argv
from datetime import datetime
from PyQt5.QtCore import Qt
from subprocess import run
import logging

from win32gui import (
    GetWindowRect,
    FindWindowEx,
    MoveWindow
)
from PyQt5.QtWidgets import (
    QProgressDialog,
    QApplication
)
from time import (
    sleep,
    time
)
from re import (
    escape as re_esc,
    sub as re_sub
)

from winnotify import (
    Messagebox as Mbox,
    PlaySound
)
from commandline import (
    openfile,
    RunCmd
)

from .lib.variables import *
from .src import *


class ConvertVideo:
    """-----
    Convert and compress video files with specified extensions (from config.ini) within this folder (and optionally its subfolders) to HEVC/AAC or VP9/OPUS.

    ----------
    3rd-party Requirements
    ----------
    FFmpeg (https://www.ffmpeg.org/)
    """

    app: QApplication
    topfol: Path
    files: list[Path]
    results: dict[str, int]
    finct: int
    totct: int
    dSize: float = 0.0
    forceCancel: bool = False

    def __init__(self, top_path: str = sys_argv[-1]):
        """-----
        Parameters
        ----------
        top_path (str): [default=sys.argv[-1]] The path to either a directory to be searched or a video file to be converted
        """
        # init vars
        self.app = QApplication(sys_argv)
        fpath = Path(top_path).resolve()
        err = False
        # setup logging
        logfile = Path(__file__).parent.joinpath('lib', 'logging.log')
        logging.basicConfig(filename=logfile,
                            filemode='w',
                            level=logging.DEBUG,
                            format='[%(asctime)s] %(levelname)s: %(module)s.%(funcName)s\n%(message)s\n',
                            datefmt='%m/%d/%Y %I:%M:%S%p')
        # run
        try:
            self.setup(fpath)
        except Exception:
            logging.exception('')
            err = True
            raise
        finally:
            if logfile.read_text():
                if err:
                    PlaySound()
                print(logfile.read_text())
                run(['powershell', 'pause'])

    def setup(self, fpath: Path):
        # rename/resize/move window
        RunCmd(["powershell", "-command",
                f'$host.UI.RawUI.WindowTitle="Compress/Convert Video"; {CON_SZ_CMD}'])
        loop = hwnd = 0
        while loop < 20 and not hwnd:
            sleep(0.1)
            hwnd = FindWindowEx(None, None, None, "Compress/Convert Video")
            loop += 1
        if loop < 50:
            # if win was found, move it
            x, y, xw, yh = GetWindowRect(hwnd)
            dx = x + CON_MOVE_BY
            w = xw - x
            h = yh - y
            MoveWindow(hwnd, dx, y, w, h, True)
        # init vars
        self.app.setWindowIcon(ICON)
        dorun = Opt.getInput(fpath)
        if not dorun:
            print("Don't run")
            raise SystemExit
        elif fpath.is_dir():
            self.topfol = fpath
            srch = self.topfol.rglob if Opt.recurse else self.topfol.glob
            self.files = [f for f in srch("*.*")
                          if f.suffix in FTYPES
                          and "[HEVC-AAC]" not in f.stem
                          and "[VP9-OPUS]" not in f.stem]
        else:
            self.topfol = fpath.parent
            self.files = [fpath]
        self.run(fpath)

    def run(self, fpath: Path):
        def formatTxt(*args: str) -> str:
            return "\n".join([f'{f" {s} " if s else s:=^{CON_WD}}' for s in ("", *args, "")])

        # init vars
        t_start = datetime.now()
        self.results = dict(err=0, fail=0, skip=0)
        self.finct = 1
        self.totct = len(self.files)
        print(formatTxt(f"PROCESSING {self.totct} ITEM{'' if self.totct == 1 else 'S'}",
                        f"({fpath})",
                        *Opt.getInfo()))
        sz_in = sum(f.stat().st_size for f in self.files) / 1024**2
        # compile data
        progress = QProgressDialog("Building commands, please wait...\n",
                                   "Cancel",
                                   0,
                                   self.totct)
        progress.setWindowTitle("Compress/Convert Video")
        progress.setMinimumWidth(800)
        progress.setStyleSheet("font-size: 11pt;")
        progress.setWindowModality(Qt.WindowModal)
        data: list[dict[str, U[Path, BuildCmd]]] = list()
        for i, pth in enumerate(self.files):
            if progress.wasCanceled():
                progress.setValue(self.totct)
                raise SystemExit
            progress.setLabelText(f"Building commands, please wait...\n"
                                  f"{pth.relative_to(self.topfol)}")
            data.append(dict(pth_in=pth, info=BuildCmd(pth, Opt())))
            progress.setValue(i)
        progress.setValue(self.totct)
        # run
        print(f"[{str(datetime.now())[5:19]}]\nSTARTING...\n")
        with ThreadPoolExecutor(max_workers=int(Opt.thread_ct)) as ex:
            ex.map(lambda x: self.process(**x), data)
        # self.process(**data[0])
        # stop
        t_end = datetime.now()
        h, m, s = str(t_end - t_start).split(":")
        t_elapsed = f"{h:0>2}h {m:0>2}m {float(s):05.02f}s"
        sz_out = sz_in - self.dSize
        sz_difp = (1.0 - sz_out / sz_in) * 100
        # cleanup
        msg = (f"<<{fpath}>>\n"
               f"Processed {self.totct} item{'' if self.totct == 1 else 's'}: \n"
               f"    {self.totct - self.results['fail'] - self.results['err'] - self.results['skip']:0{len(str(self.totct))}} successfully altered\n"
               f"    {self.results['skip']:0{len(str(self.totct))}} were skipped\n"
               f"    {self.results['fail']:0{len(str(self.totct))}} failed compression\n"
               f"    {self.results['err']:0{len(str(self.totct))}} had errors\n"
               f"Time elapsed: {t_elapsed}\n"
               f"Result: {self.dSize:.2f}MB ({sz_difp:02.2f}%) {'reduction' if self.dSize < 0 else 'increase'} in size")
        Mbox.showinfo(title="Processing Complete", message=msg)
        run(["powershell", "clear"])
        self.app.quit()

    def process(self, pth_in: Path, info: BuildCmd) -> None:
        if self.forceCancel:
            self.results["skip"] += 1
            return
        # init vars
        pth_out, cmd, todo = info.pth_out, info.cmd, info.todo
        err = None
        proc_dict = dict(
            V=dict(c="converted", x="cropped"),
            A=dict(m="added metadata", l="selected by language",
                   s="selected specific stream", c="converted"),
            S=dict(m="added metadata", l="selected by language",
                   s="selected specific stream", c="converted")
        )

        def getPath() -> str:
            fill = TextWrapper(width=round(CON_WD),
                               subsequent_indent="    ").fill
            namestr = fill(f'INPUT: "{pth_in.name}"')
            outstr = fill(f'OUTPUT: "{pth_out.name}"')
            if Opt.recurse:
                ffol = str(pth_in.parent.relative_to(self.topfol))
                folstr = fill(f'DIR: "{ffol}"')
                return "\n".join([folstr, namestr, outstr])
            else:
                return "\n".join([namestr, outstr])

        def getResults() -> str:
            # check if output is viable
            err_chk = run(f'ffmpeg -hide_banner -v error -i "{pth_out}" -c copy -f null -',
                          capture_output=True,
                          text=True,
                          cwd=pth_out.parent).stderr
            dur_out = run(['ffprobe', pth_out, '-v', 'error', '-select_streams', 'v',
                           '-show_entries', 'format=duration', '-of', 'csv=p=0'],
                          capture_output=True,
                          text=True).stdout.strip()
            dur_chk = ((info.data.vid.dur - 0.5) <= float(dur_out) <=
                       (info.data.vid.dur + 0.5)) if dur_out else False
            if pth_out.exists() and not err_chk and dur_chk and not returncode:
                sz_in = float(pth_in.stat().st_size / 1024**2)
                sz_out = float(pth_out.stat().st_size / 1024**2)
                sz_dif = sz_out - sz_in
                sz_comp = f"({sz_in:02.2f} -> {sz_out:02.2f} :: {sz_dif:+02.2f}MB)"
                sz_difp = (1.0 - sz_out / sz_in) * 100
                if sz_dif < 0:
                    self.dSize += sz_dif
                    resstr = ("COMPRESSED FILE BY "
                              f"{sz_difp:02.2f}% {sz_comp}")
                    if Opt.overwrite:
                        try:
                            pth_in.chmod(0o777)
                            pth_in.unlink()
                            pth_out.rename(pth_out.with_stem(pth_in.stem))
                        except:
                            pass
                        if pth_out.exists():
                            resstr += "\n    COULDN'T REMOVE ORIGINAL FILE"
                elif Opt.keep_fail:
                    self.dSize += sz_dif
                    self.results["fail"] += 1
                    resstr = ("CONVERSION SUCCESSFUL;\n"
                              f"   COMPRESSION INEFFECTIVE {sz_comp}")
                    if Opt.overwrite and Opt.overwrite_fail:
                        try:
                            pth_in.chmod(0o777)
                            pth_in.unlink()
                            pth_out.rename(pth_out.with_stem(pth_in.stem))
                        except:
                            pass
                        if pth_out.exists():
                            resstr += "\n    COULDN'T REMOVE ORIGINAL FILE"
                else:
                    self.results["fail"] += 1
                    resstr = f"PROCESSING INEFFECTIVE {sz_comp}"
                    if not Opt.keep_error:
                        pth_out.unlink(missing_ok=True)
            else:
                self.results["err"] += 1
                errstr = (f"INPUT\nreturncode <{returncode}>\n-- TRACEBACK -----\n{err.strip()}\n{'='*25}" if err
                          else f"OUTPUT\nreturncode <{returncode}>\n-- TRACEBACK -----\n{err_chk.strip()}\n{'='*25}" if err_chk
                          else f"PROCESSING\nreturncode <{returncode}>\nReason: mismatched durations (in={info.data.vid.dur}s, out={float(dur_out)}s)" if dur_out and not dur_chk
                          else f"PROCESSING\nreturncode <{returncode}>" if returncode
                          else "file could not be processed" if not pth_out.exists()
                          else "file processing failed" if pth_out.stat().st_size < 100
                          else "unknown error")
                resstr = f"ERROR: {errstr}"
                if not Opt.keep_error:
                    pth_out.unlink(missing_ok=True)
                logging.exception(
                    f'{"#" * 10}\n' f"{pathstr}\n" f">> {resstr}\n")
            return resstr

        def getProcesses(key: str) -> str:
            todo_list = todo.get(key)
            var_dict = proc_dict.get(key)
            if todo_list:
                return ", ".join(var_dict.get(k) for k in todo_list)
            else:
                return "none (copied)"

        if not pth_in.exists():
            divstr = f"{f' Item {self.finct} of {self.totct} ':-^{CON_WD}}"
            self.finct += 1
            print(f"{divstr}\n"
                  f"[{str(datetime.now())[5:19]}]\n"
                  f"{getPath()}\n"
                  f"PROCESSES: skipped\n"
                  f">> ERROR: File not found\n")
            return
        # process
        dt_start = datetime.now()
        if cmd:
            # cmd += '; pause'
            t_start = time()
            returncode = RunCmd(["powershell", "-command", cmd],
                                console="new",
                                visibility="min").wait()
            t_end = time()
            if returncode or t_end - t_start < 5:
                # there was an error or processing took too short of a time
                if returncode == 3221225786:
                    err = "User closed the window"
                    self.forceCancel = True
                else:
                    chk_cmd = re_sub(f' -y (.+?) "{re_esc(str(pth_out))}"',
                                     r" -v error \1 -f null -",
                                     info.ffmpeg_cmd)
                    _, err = RunCmd(["powershell", "-command", chk_cmd],
                                    console="new",
                                    capture_output=True,
                                    visibility="hide").communicate()
        # print results
        pathstr = getPath()
        if cmd:
            procstr = (f"PROCESSES:\n"
                       f'  video -> {getProcesses("V")}\n'
                       f'  audio -> {getProcesses("A")}\n'
                       f'  subs  -> {getProcesses("S")}')
        else:
            procstr = "PROCESSES: skipped"
            self.results["skip"] += 1
        dt_end = datetime.now()
        h, m, s = str(dt_end - dt_start).split(":")
        if not cmd:
            t_elapsed = ""
            if pth_out.name in ["ERROR", "DELETED"]:
                resstr = "INPUT COULD NOT BE FOUND"
            else:
                resstr = "ALREADY COMPRESSED/CONVERTED/PROCESSED"
        else:
            t_elapsed = f"ELAPSED: {h:0>2}h {m:0>2}m {float(s):0>2.0f}s\n"
            resstr = getResults()
        divstr = f"{f' Item {self.finct} of {self.totct} ':-^{CON_WD}}"
        self.finct += 1
        print(f"{divstr}\n"
              f"[{str(datetime.now())[5:19]}]\n"
              f"{pathstr}\n"
              f"{procstr}\n"
              f"{t_elapsed}"
              f">> {resstr}\n")


if __name__ == "__main__":
    ConvertVideo()

# window is 665x450
