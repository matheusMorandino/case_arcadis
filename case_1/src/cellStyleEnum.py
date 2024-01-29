from enum import Enum
from openpyxl.styles import NamedStyle, PatternFill


class CellStyle(Enum):
    CINZA_BG_STYLE = NamedStyle(name='gray_bg', fill=PatternFill(start_color='B0B0B0', end_color='B0B0B0', fill_type='solid'))

