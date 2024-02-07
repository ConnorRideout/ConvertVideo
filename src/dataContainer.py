from typing import TYPE_CHECKING
from subprocess import run

from re import (
    findall as re_findall,
    search as re_search
)

from winnotify import (
    InputDialog as InDlg,
    Messagebox as Mbox
)

from ..lib.variables import *

if TYPE_CHECKING:
    from .options import Options


def ffprobe(pth_in: Path, streams: str, entries: str, frmt: str = 'csv=p=0') -> str:
    res = run(['ffprobe', pth_in, '-v', 'error', '-select_streams', streams,
               '-show_entries', entries, '-of', frmt],
              capture_output=True,
              text=True)
    return res.stdout.strip()


def askStream(pth_in: Path, stream: str, strm_list: list[str], message: str) -> O[str]:
    if len(strm_list) > 1:
        return InDlg.comboinput(title="Bad Stream Specifier",
                                message=(f"{pth_in}:\n{message}. "
                                         "Pressing 'cancel' will copy all streams."),
                                label=f"Select {stream} stream",
                                options=[str(n)
                                         for n in range(len(strm_list))],
                                playsound='alert')
    elif strm_list:
        # there is a stream. Check if an accepted language already exists
        streams = '\n'.join(strm_list)
        lang_code = [lang for lang in AUD_LANGS if lang in streams]
        if not lang_code:
            # no accepted language exists
            return '0'
        else:
            # a lang code exists but it isn't what the user wants
            overwrite_lang = Mbox.askquestion(title="Existing Stream Metadata",
                                              message=(f"{pth_in}:\nThe {stream} stream has existing language metadata. "
                                                       f"Do you want to overwrite the current language ({AUD_LANGS.get(lang_code[0])})?"))
            if overwrite_lang == 'yes':
                return '0'
            else:
                return ''
        # return '0'
    else:
        return ''


class DataContainer:
    def __init__(self, pth_in: Path, options: "Options"):
        self.vid = self._Vid(pth_in, options)
        self.aud = self._Aud(pth_in, options)
        self.sub = self._Sub(pth_in, options)

    class _Vid:
        codec: str
        ht: int
        wd: int
        dur: float
        crop: str

        def __init__(self, pth_in: Path, Opt: "Options"):
            raw = ffprobe(pth_in=pth_in,
                          streams='v:0',
                          entries='stream=codec_name,width,height:format=duration',
                          frmt='default=nw=1')
            try:
                self.codec = re_search(
                    r'codec_name=(.+)', raw).group(1).lower()
                self.ht = int(re_search(r'height=(.+)', raw).group(1))
                self.wd = int(re_search(r'width=(.+)', raw).group(1))
                self.dur = float(re_search(r'duration=(.+)', raw).group(1))
            except AttributeError:
                sz = (pth_in.stat().st_size / 1024)
                ans = Mbox.askquestion(title="Error Processing Item",
                                       message=f"The item\n'{pth_in}'\n(size on disk: {sz:0.3f}Kb)\nappears to have no video. Would you like to delete it?",
                                       icon='critical')
                if ans == 'yes':
                    pth_in.unlink(missing_ok=True)
                self.codec = self.ht = self.wd = self.dur = self.crop = None
                return
            crop_scale = list()
            if Opt.do_crop:
                # get crops, starting in middle of video and for up to 60secs
                cropinfo: str = run(['ffmpeg', '-hide_banner', '-ss', f'{self.dur//2}',
                                     '-i', pth_in, '-t', '60', '-vf', 'cropdetect', '-f', 'null', '-'],
                                    capture_output=True,
                                    text=True,
                                    cwd=pth_in.parent,
                                    ).stderr
                try:
                    cropstr = re_findall(r'crop=.+', cropinfo)[-1]
                    cw, ch, _, _ = [int(n)
                                    for n in re_findall(r'\d+', cropstr)]
                    if (cw < self.wd or ch < self.ht) and '-' not in cropstr:
                        crop_scale.append(cropstr)
                except:
                    pass
            if Opt.do_scale:
                d_wd = self.wd - 1280
                d_ht = self.ht - 720
                if self.wd > 1280 and d_wd >= d_ht:
                    # vid is wider than 1280 and wider than it is tall
                    crop_scale.append('scale=1280:-1')
                elif self.ht > 720:
                    # vid is taller than 720 and taller than it is wide
                    crop_scale.append('scale=-1:720')
            if crop_scale:
                self.crop = f'-filter:v:0 {",".join(crop_scale)}'
            else:
                self.crop = ""

    class _Aud:
        streams: str
        strm_list: list[str]
        chnls: int
        lang_match: list[str] = list()
        add_metadata: str = None

        def __init__(self, pth_in: Path, Opt: "Options"):
            self.strm_list = [stream.strip()
                              for stream in ffprobe(pth_in=pth_in,
                                                    streams='a',
                                                    entries='stream=codec_name,channels:stream_tags=language').split('\n')
                              if stream.strip()]
            self.streams = '\n'.join(self.strm_list)
            if self.streams:
                # there is audio
                if Opt.aud_strm in AUD_LANGS:
                    # audio stream is a lang code
                    if not Opt.aud_strm in self.streams:
                        # no lang tag match
                        ans = askStream(pth_in=pth_in,
                                        stream='audio',
                                        strm_list=self.strm_list,
                                        message=("The specified language couldn't be found. "
                                                 f"Please select the {AUD_LANGS.get(Opt.aud_strm)} audio stream"))
                        if ans:
                            self.add_metadata = Opt.aud_strm
                            Opt.aud_strm = ans
                            self.chnls = (
                                int(self.strm_list[int(ans)].split(',')[1])) * 64
                        else:
                            Opt.aud_strm = 'all'
                            self.chnls = (
                                max(int(x.split(',')[1])for x in self.strm_list) * 64)
                    else:
                        self.lang_match = re_findall(
                            f'.+(?=,{Opt.aud_strm})', self.streams)
                        self.chnls = (max(int(x.split(',')[1])
                                          for x in self.lang_match) * 64)
                elif Opt.aud_strm.isnumeric():
                    # audio is stream number
                    if len(self.strm_list) <= int(Opt.aud_strm):
                        # audio stream is out of range
                        ans = askStream(pth_in=pth_in,
                                        stream='audio',
                                        strm_list=self.strm_list,
                                        message=("The specified audio stream index is out of range. "
                                                 "Please select a valid stream index"))
                        if ans:
                            Opt.aud_strm = ans
                            self.chnls = (
                                (int(self.strm_list[int(ans)].split(',')[1])) * 64)
                        else:
                            Opt.aud_strm = 'all'
                            self.chnls = (
                                max(int(x.split(',')[1]) for x in self.strm_list) * 64)
                    else:
                        self.chnls = (
                            (int(self.strm_list[int(Opt.aud_strm)].split(',')[1])) * 64)
                elif Opt.aud_strm == 'all':
                    # 'all' selected
                    self.chnls = (max(int(x.split(',')[1])
                                      for x in self.strm_list) * 64)
                else:
                    # 'all listed' selected
                    self.lang_match = [match for lang in AUD_LANGS
                                       for match in re_findall(f'.+(?=,{lang})', self.streams)]
                    self.chnls = (max(int(x.split(',')[1])
                                      for x in self.lang_match) * 64)
            else:
                # no audio
                self.chnls = 128

    class _Sub:
        streams: str
        strm_list: list[str]
        lang_match: list[str] = list()
        force_copy: bool = False
        add_metadata: str = None

        def __init__(self, pth_in: Path, Opt: "Options"):
            if Opt.sub_strm == 'remove':
                self.streams = ''
                self.strm_list = list()
                return
            # some stream is selected
            self.strm_list = [stream.strip()
                              for stream in ffprobe(pth_in=pth_in,
                                                    streams='s',
                                                    entries='stream=codec_name:stream_tags=language').split('\n')
                              if stream.strip()]
            self.streams = '\n'.join(self.strm_list)
            if self.streams:
                # there are subtitles
                if Opt.sub_strm in SUB_LANGS:
                    # sub stream is a lang code
                    if not Opt.sub_strm in self.streams:
                        # no lang tag matchs
                        ans = askStream(pth_in=pth_in,
                                        stream='subtitle',
                                        strm_list=self.strm_list,
                                        message=("The specified language couldn't be found. "
                                                 f"Please select the {SUB_LANGS.get(Opt.sub_strm)} subtitle stream"))
                        if ans:
                            self.add_metadata = Opt.sub_strm
                            Opt.sub_strm = ans
                        else:
                            Opt.sub_strm = 'all'
                    else:
                        self.lang_match = re_findall(f'.+(?=,{Opt.sub_strm})',
                                                     self.streams)
                elif Opt.sub_strm.isnumeric():
                    # sub is stream number
                    if len(self.strm_list) <= int(Opt.sub_strm):
                        # specified sub stream does not exist
                        ans = askStream(pth_in=pth_in,
                                        stream='subtitle',
                                        strm_list=self.strm_list,
                                        message=("The specified subtitle stream index is out of range. "
                                                 "Please select a valid stream index"))
                        if ans:
                            Opt.sub_strm = ans
                        else:
                            Opt.sub_strm = 'all'
                if re_findall(r'dvb_subtitle|dvd_subtitle|hdmv_pgs_subtitle|xsub', self.streams):
                    # subtitle is image-based
                    self.force_copy = True
