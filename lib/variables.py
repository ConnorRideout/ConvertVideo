from PyQt5.QtGui import QIcon as _QIcon
from re import split as _split
from pathlib import Path

from configparser import (
    ExtendedInterpolation as _ExtInterp,
    ConfigParser as _ConfigParser,
)
from typing import (
    Optional as O,
    Union as U
)


class _Cfg(_ConfigParser):
    def __init__(self):
        _ConfigParser.__init__(self, allow_no_value=False,
                               interpolation=_ExtInterp())
        self.optionxform = str
        self.read_file(open(Path(__file__).parent.with_name('config.ini')))

    def getlines(self, sct, opt) -> tuple[str, ...]:
        return tuple(self.get(sct, opt).strip().split('\n'))


_cfg = _Cfg()


ICON = _QIcon(str(Path(__file__).with_name('conv_icon.ico')))

_sct = 'Console'
CON_WD = max(60, _cfg.getint(_sct, 'console_wd')) - 1
CON_HT = _cfg.getint(_sct, 'console_ht')
CON_SZ_CMD = ('$ps = (Get-Host).ui.rawui; '
              '$sz = $ps.windowsize; '
              f'$sz.width = {CON_WD}; '
              f'$sz.height = {CON_HT}; '
              '$ps.windowsize = $sz; '
              '$bf = $ps.buffersize; '
              f'$bf.width = {CON_WD}; '
              '$ps.buffersize = $bf')
CON_MOVE_BY = _cfg.getint(_sct, 'console_move_x')

_sct = 'Convert Video'
FTYPES = _cfg.getlines(_sct, 'file_types')
NVENC = _cfg.getboolean(_sct, 'use_hevc_nvenc')
CRF_VALS = tuple((int(ht), int(crf))
                 for ht, crf in [_split(r'\s*:\s*', val)
                                 for val in _cfg.getlines(_sct, 'ffmpeg_crf_values')])

_sct = 'Default Options'
AUD_LANGS = {x[0]: x[1]
             for x in [line.split(':')
                       for line in _cfg.getlines(_sct, 'aud_stream_langs')]}
SUB_LANGS = {x[0]: x[1]
             for x in [line.split(':')
                       for line in _cfg.getlines(_sct, 'sub_stream_langs')]}
STREAMS = max(0, _cfg.getint(_sct, 'stream_count'))
OVERWRITE = _cfg.getboolean(_sct, 'overwrite_original')
DO_SCALE = _cfg.getboolean(_sct, 'scale_video')
DO_CROP = _cfg.getboolean(_sct, 'crop_blackspace')
KEEP_FAIL = _cfg.getboolean(_sct, 'keep_failures')
OVERWRITE_FAIL = _cfg.getboolean(_sct, 'overwrite_failures')
KEEP_ERROR = _cfg.getboolean(_sct, 'keep_errors')
RECURSE = _cfg.getboolean(_sct, 'recurse_folders')
CUTOFF = _cfg.getint(_sct, 'playtime_cutoff')
THREADS = max(1, _cfg.getint(_sct, 'thread_count'))
if NVENC:
    CONV_THREADS = min(5, THREADS)
ADD_PARAMS = _cfg.get(_sct, 'add_params').strip()
