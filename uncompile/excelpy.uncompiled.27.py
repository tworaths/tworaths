# uncompyle6 version 3.9.1
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  4 2019, 01:37:19) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\excelpy.py
# Compiled at: 2016-05-19 21:00:08
r"""
Excel Interface Python Functions
Argument Definitions:
address: Specify cell or range address.
  -cell address specified as:
      'adrstr' or ('adrstr') or (row,'clnstr') or (row, column)
      Example: Cell address referencing 2nd row, column A, can be provided as-
               'a2' or ('a2') or (2,'a') or (2,1)
  -range address specified as:
      ('adrstr1','adrstr2') or (toprow, 'leftcolumnstr', bottomrow, 'rightcolumnstr') or
      (toprow, leftcolumn, bottomrow, rightcolumn) or
      ('adrstr1', (bottomrow, rightcolumn)) or ('adrstr1', (bottomrow, 'rightcolumnstr'))
      ((toprow, leftcolumn), 'adrstr2') or ((toprow, 'leftcolumnstr'), 'adrstr2')
  where row, column, toprow, leftcolumn, bottomrow, rightcolumn are integer values,
        adrstr, adrstr1, adrstr2 are cell address string values, and
        clnstr, leftcolumnstr, rightcolumnstr are column name string values.
        Note: Column and address refernce string values are case-insensitive.
alignv: string, alignment value for cell, range, rows or columns
  -allowed values for horizontal alignment: 'left','right','h_center'
  -allowed values for vertical alignment: 'top','bottom','v_center'
borderv: string, border name
  -allowed border names when formatting a cell:
   'diagonaldown','diagonalup','top','bottom','left','right','none','outline'
  -allowed border names when formatting a range:
   'diagonaldown','diagonalup','top','bottom','left','right','hinside','vinside',
   'none','outline','inside'
borderColor: string, color name; or integer, color index.
  -allowed color names:
   'black',  'white', 'red',   'green',  'blue', 'yellow',
   'magenta', 'cyan', 'brown', 'dgreen', 'dblue', 'orange'
  -ColorIndex:
   1 to 56 as per ColorIndex property in Excel Visual Basic Reference.
borderStyle: string, border style name
  -allowed names:
   'continuous','dash','dashdot','dashdotdot','dot','double','none','slantdashdot'
borderWeight -string, border weight name
  -allowed names:
   'hairline','medium','thick','thin'
fontStyle: string or tuple of strings, font style name
  -allowed names:
   'regular' or 'bold' or 'italic' or 'underline'
   e.g., ("Italic","Bold") or 'bold'
fontColor: string, color name; or integer, color index.
   same as color in 'borderColor'
numberFormat: string, number format, e.g.,"0.000" for three decimal places
leftCol: integer, left column number
newSheet: string, name of the new worksheet
oldSheet:string, name of the worksheet used as reference for worksheet operations
overwritesheet: logical, overwrite if worksheet exists, True or False
   Used when creating new worksheets or renaming existing worksheets.
       when True, existing worksheet will be overwritten
       when False, existing sheet copied and its name appended with (#),
           where # is next sequence number.
sheet: string, name of the excel worksheet
   If sheet is not provided, active worksheet used.
topRow: integer, top row number
wrapText: logical, wrap text or not, True or False
xlsfile: string, name of the excel file

DEFAULT FONT:   Black, Regular, Courier New, size 10,
                no wrapText, General number format

How to Use: Create excel application object as below and apply various methods defined here.
(1) When used to create new Excel files or add worksheets to existing Excel files:
xlobj = excelpy.workbook()
xlobj = excelpy.workbook(r"c:\working dir\ex1.xls")
xlobj = excelpy.workbook(r"c:\working dir\ex1.xls", "MySheet") or
xlobj = excelpy.workbook(r"c:\working dir\ex1.xls", "MySheet", False) or
xlobj = excelpy.workbook(r"c:\working dir\ex1.xls", "MySheet", False, 'w') or
xlobj = excelpy.workbook(xlsfile=r"c:\working dir\ex1.xls", sheet="MySheet",
                           overwritesheet=False, mode='w')

(2) When used to read existing Excel files:
xlobj = excelpy.workbook(r"c:\working dir\ex1.xls", mode='r')

Note: When using Excel 2007 and later, create file in either 'xlsx' or 'xls' format.
      Excel 2003 and earlier - default save format 'xls'.
      Excel 2007 and later   - default save format 'xlsx'.
"""
_DEF_FONTSTYLE = (
 'Regular',)
_DEF_FONTNAME = 'Courier New'
_DEF_FONTSIZE = 10
_DEF_FONTCOLOR = 'black'
_DEF_NUMFORMAT = '0.00'
_FONT_COLORINDEX = {'black': 1, 
   'white': 2, 
   'red': 3, 
   'green': 4, 
   'blue': 5, 
   'yellow': 6, 
   'magenta': 7, 
   'cyan': 8, 
   'brown': 9, 
   'dgreen': 10, 
   'dblue': 32, 
   'orange': 46}
_MARGIN_WHICH = (
 'top', 'bottom', 'left', 'right')
_MAXROWS11, _MAXCOLUMNS11 = (
 65536, 256)
_MAXROWS12, _MAXCOLUMNS12 = (1048576, 16384)
_HEADER_FOOTER_CODES = {'page number': '&P', 
   'page total': '&N', 
   'file name': '&F', 
   'sheet name': '&A', 
   'date': '&D', 
   'time': '&T'}
import os, _winreg
try:
    import pythoncom
except:
    pass

import win32com.client

def _filePNXvalues(fnam):
    pn, p, n, x, xlw = ('', '', '', '', '')
    if fnam:
        p, nx = os.path.split(fnam)
        pn, x = os.path.splitext(fnam)
        n, x = os.path.splitext(nx)
        xlw = x.lower()
    return (
     pn, p, n, x, xlw)


import locale
_CODECNAME, _CODEC2USE = locale.getdefaultlocale()

def _smart_unicode(s_in, errors='strict'):
    s_ou = u''
    if type(s_in) is str:
        s_ou = unicode(s_in, encoding=_CODEC2USE, errors=errors)
    elif type(s_in) is unicode:
        s_ou = s_in
    return s_ou


class excelpy():
    """
    """

    def __init__(self, xlsfile, sheet, overwritesheet, mode):
        """
        """
        self.xlapp = None
        try:
            self.xlapp = win32com.client.DispatchEx('Excel.Application')
            ok_dispath = True
        except:
            ok_dispath = False

        if ok_dispath:
            try:
                self._get_constants()
            except:
                self._get_constants_specified()

        else:
            try:
                self.xlapp = win32com.client.gencache.EnsureDispatch('Excel.Application')
                self._get_constants()
            except pythoncom.com_error as (hr, msg, exc, arg):
                print 'The Excel call failed with code %d: %s' % (hr, msg)
                if exc is None:
                    print 'There is no extended error information'
                else:
                    wcode, source, text, helpFile, helpId, scode = exc
                    print 'The source code of the error is', source
                    print 'The error message is', text
                    print 'More info can be found in %s (id=%d)' % (helpFile, helpId)

        if not self.xlapp:
            raise
        self.VERNUM = float(self.xlapp.Version)
        if self.VERNUM < 12:
            self.MAXROWS = _MAXROWS11
            self.MAXCOLUMNS = _MAXCOLUMNS11
            self.EXTN = '.xls'
        else:
            self.MAXROWS = _MAXROWS12
            self.MAXCOLUMNS = _MAXCOLUMNS12
            self.EXTN = '.xlsx'
        xlsfileExists = False
        savehere = False
        if xlsfile:
            xlsfile = self._get_input_filename(xlsfile)
            if os.path.exists(xlsfile):
                xlsfileExists = True
        if mode.lower() == 'w':
            self.READONLY = False
            if xlsfileExists:
                self.xlbook = self.xlapp.Workbooks.Open(xlsfile, ReadOnly=False)
                self.worksheet_add_end(sheet, overwritesheet)
            else:
                self.xlbook = self.xlapp.Workbooks.Add()
                if not xlsfile:
                    xlsfile = self._get_save_filename()
                else:
                    savehere = True
                nshts = self.xlbook.Sheets.Count
                tmpshnamList = []
                for i in range(2, nshts + 1):
                    tmpshnam = self.xlbook.Sheets(i).Name
                    tmpshnamList.append(tmpshnam)

                for tmpshnam in tmpshnamList:
                    try:
                        self.xlbook.Sheets(tmpshnam).Delete()
                    except:
                        pass

                if sheet:
                    sheet = sheet.strip()
                    self.xlbook.ActiveSheet.Name = sheet
        else:
            self.READONLY = True
            if xlsfileExists:
                self.xlbook = self.xlapp.Workbooks.Open(xlsfile, ReadOnly=True)
                nshts = self.xlbook.Sheets.Count
                if nshts:
                    self.READONLYEXISTS = True
                    fstshnam = self.xlbook.Sheets(1).Name
                    self.set_active_sheet(fstshnam)
                else:
                    self.READONLYEXISTS = False
                    print 'There are no worksheets in file: %s' % xlsfile
            else:
                self.READONLYEXISTS = False
                if xlsfile:
                    print 'File does dot exists: %s' % xlsfile
                else:
                    print 'File to read must be provided.'
        self.XLSFNAM = self._get_save_filename(xlsfile)
        if savehere:
            self.save(self.XLSFNAM)
        try:
            keynam = 'Control Panel\\International'
            usr_national_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keynam, 0, _winreg.KEY_READ)
        except:
            usr_national_key = None

        self.dcml_symbol = ''
        if usr_national_key:
            try:
                self.dcml_symbol, regtyp = _winreg.QueryValueEx(usr_national_key, 'sDecimal')
            except:
                self.dcml_symbol = ''

            if self.dcml_symbol:
                if self.dcml_symbol == '.':
                    self.dcml_symbol = ''
        return

    def align(self, address, alignv, sheet=None):
        """Align Cell or Range.
        cell,  address = (row,col)
        range, address = (topRow,leftCol,bottomRow,rightCol)
        """
        if self.READONLY:
            return
        if not alignv:
            return
        cell_or_rng, topRow, leftCol, bottomRow, rightCol = self._check_cell_or_range(address)
        if not cell_or_rng:
            return
        if cell_or_rng == 'cell':
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                return
            self._set_align(cell, alignv)
        else:
            rng = self._active_range((topRow, leftCol, bottomRow, rightCol), sheet)
            if not rng:
                return
            self._set_align(rng, alignv)

    def align_columns(self, address, alignv, sheet=None):
        """Align one or more columns.
        One column, address = (row,col)
        Multiple columns, address = (topRow,leftCol,topRow,rightCol)
        """
        if self.READONLY:
            return
        if not alignv:
            return
        cell_or_rng, topRow, leftCol, bottomRow, rightCol = self._check_cell_or_range(address)
        if not cell_or_rng:
            return
        if cell_or_rng == 'cell':
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                return
            column = cell.EntireColumn
            self._set_align(column, alignv)
        else:
            sht = self._valid_sheet(sheet)
            for i in range(leftCol, rightCol + 1):
                column = sht.Cells(topRow, i).EntireColumn
                self._set_align(column, alignv)

    def align_rows(self, address, alignv, sheet=None):
        """Align one or more rows.
        One row, address = (row,col)
        Multiple rows, address = (topRow,leftCol,bottomRow,leftCol)
        """
        if self.READONLY:
            return
        if not alignv:
            return
        cell_or_rng, topRow, leftCol, bottomRow, rightCol = self._check_cell_or_range(address)
        if not cell_or_rng:
            return
        if cell_or_rng == 'cell':
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                return
            row = cell.EntireRow
            self._set_align(row, alignv)
        else:
            sht = self._valid_sheet(sheet)
            for i in range(topRow, bottomRow + 1):
                row = sht.Cells(i, leftCol).EntireRow
                self._set_align(row, alignv)

    def autofit_columns(self, address, sheet=None):
        """Autofit column or columns.
        One column, address = (row,col)
        Multiple columns, address = (topRow,leftCol,topRow,rightCol)
        """
        if self.READONLY:
            return
        cell_or_rng, topRow, leftCol, bottomRow, rightCol = self._check_cell_or_range(address)
        if not cell_or_rng:
            return
        if cell_or_rng == 'cell':
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                return
            cell.EntireColumn.AutoFit()
        else:
            rng = self._active_range((topRow, leftCol, bottomRow, rightCol), sheet)
            if not rng:
                return
            sht = self._valid_sheet(sheet)
            for i in range(leftCol, rightCol + 1):
                sht.Cells(topRow, i).EntireColumn.AutoFit()

    def autofit_rows(self, address, sheet=None):
        """Autofit row or rows.
        One row, address = (row,col)
        Multiple rows, address = (topRow,leftCol,bottomRow,leftCol)
        """
        if self.READONLY:
            return
        cell_or_rng, topRow, leftCol, bottomRow, rightCol = self._check_cell_or_range(address)
        if not cell_or_rng:
            return
        if cell_or_rng == 'cell':
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                return
            cell.EntireRow.AutoFit()
        else:
            rng = self._active_range((topRow, leftCol, bottomRow, rightCol), sheet)
            if not rng:
                return
            rng.Rows.AutoFit()

    def border(self, address, borderv, borderStyle='continuous', borderWeight='hairline', borderColor='black', sheet=None):
        """Format Cell or Range borders.
        cell,  address = (row,col)
        range, address = (topRow,leftCol,bottomRow,rightCol)
        """
        if self.READONLY:
            return
        if not borderv:
            return
        cell_or_rng, topRow, leftCol, bottomRow, rightCol = self._check_cell_or_range(address)
        if not cell_or_rng:
            return
        if cell_or_rng == 'cell':
            if borderv.lower() not in _BORDER_INDEX_CELL:
                return
            bdindex = self._get_border_index(borderv)
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                return
            if bdindex == 'noborder':
                bdnone = [
                 'diagonaldown', 'diagonalup', 
                 'left', 'top', 'bottom', 'right']
                bdlist = [self._get_border_index(each) for each in bdnone]
                self._set_border_none(cell, bdlist)
            else:
                lnstyle = self._get_line_style(borderStyle)
                if not lnstyle:
                    return
                bdweight = self._get_border_weight(borderWeight)
                if not bdweight:
                    return
                colorindex = self._get_color_index(borderColor)
                if bdindex == 'outlineborder':
                    bdoutline = [
                     'left', 'top', 'bottom', 'right']
                    bdlist = [self._get_border_index(each) for each in bdoutline]
                else:
                    bdlist = [
                     bdindex]
                self._set_border(cell, bdlist, lnstyle, bdweight, colorindex)
        elif borderv.lower() not in _BORDER_INDEX:
            return
        bdindex = self._get_border_index(borderv)
        rng = self._active_range((topRow, leftCol, bottomRow, rightCol), sheet)
        if not rng:
            return
        if bdindex == 'noborder':
            bdnone = [
             'diagonaldown', 'diagonalup', 'left', 'top', 
             'bottom', 'right', 
             'hinside', 
             'vinside']
            bdlist = [self._get_border_index(each) for each in bdnone]
            self._set_border_none(rng, bdlist)
        else:
            lnstyle = self._get_line_style(borderStyle)
            if not lnstyle:
                return
            bdweight = self._get_border_weight(borderWeight)
            if not bdweight:
                return
            colorindex = self._get_color_index(borderColor)
            if bdindex == 'outlineborder':
                bdoutline = [
                 'left', 'top', 'bottom', 'right']
                bdlist = [self._get_border_index(each) for each in bdoutline]
            elif bdindex == 'insideborder':
                bdnone = [
                 'diagonaldown', 'diagonalup', 
                 'left', 'top', 'bottom', 'right']
                bdlist = [self._get_border_index(each) for each in bdnone]
                self._set_border_none(rng, bdlist)
                bdinside = []
                if topRow < bottomRow:
                    bdinside.append('hinside')
                if leftCol < rightCol:
                    bdinside.append('vinside')
                bdlist = [self._get_border_index(each) for each in bdinside]
            else:
                bdlist = [
                 bdindex]
            self._set_border(rng, bdlist, lnstyle, bdweight, colorindex)

    def close(self):
        """Close active Excel workbook.
        """
        if not self.READONLY:
            self.xlbook.Close(SaveChanges=False)
        elif self.READONLYEXISTS:
            self.xlbook.Close(SaveChanges=False)

    def close_app(self):
        """Close Excel application.
        """
        self.xlapp.Quit()

    def close_app_byforce(self):
        """Sometimes Excel application does not close after calling close_app() method.
Use this to force close the Excel application.
        """
        try:
            _force_close_excel_thread(self.xlapp)
        except:
            msg = 'Failed to close Excel application.\n    You may have (manually) opened other Excel files and changes in them are not saved.\n    Try closing it from Windows Task Manager.'
            print msg

    def font(self, address, fontStyle=None, fontName=None, fontSize=None, fontColor=None, wrapText=False, numberFormat=None, sheet=None):
        """Set cell or range font properties: style, name, size, color, wrap, numberformat
        Cell, address = (row,col)
        Range, address = (topRow,leftCol,bottomRow,rightCol)
        """
        if self.READONLY:
            return
        cell_or_rng, topRow, leftCol, bottomRow, rightCol = self._check_cell_or_range(address)
        if not cell_or_rng:
            return
        if numberFormat and self.dcml_symbol:
            numberFormat = numberFormat.replace('.', self.dcml_symbol)
        if cell_or_rng == 'cell':
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                return
            self._set_font(cell, fontStyle, fontName, fontSize, fontColor, wrapText, numberFormat)
        else:
            rng = self._active_range((topRow, leftCol, bottomRow, rightCol), sheet)
            if not rng:
                return
            self._set_font(rng, fontStyle, fontName, fontSize, fontColor, wrapText, numberFormat)

    def font_color(self, address, color, sheet=None):
        """Set cell or range font color.
        Cell, address = (row,col)
        Range, address = (topRow,leftCol,bottomRow,rightCol)
        """
        if self.READONLY:
            return
        cell_or_rng, topRow, leftCol, bottomRow, rightCol = self._check_cell_or_range(address)
        if not cell_or_rng:
            return
        colorindex = self._get_color_index(color)
        if cell_or_rng == 'cell':
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                return
            cell.Font.ColorIndex = colorindex
        else:
            rng = self._active_range((topRow, leftCol, bottomRow, rightCol), sheet)
            if not rng:
                return
            rng.Font.ColorIndex = colorindex

    def font_sheet(self, fontStyle=_DEF_FONTSTYLE, fontName=_DEF_FONTNAME, fontSize=_DEF_FONTSIZE, fontColor=_DEF_FONTCOLOR, wrapText=False, numberFormat=None, sheet=None):
        """Set font properties for excel sheet: style, name, size, color, wrap, numberformat
        Default workbook style: regular, courier new, black, 10, no wrap text, general number format
        """
        if self.READONLY:
            return
        sht = self._valid_sheet(sheet)
        sht = sht.Columns
        self._set_font(sht, fontStyle, fontName, fontSize, fontColor, wrapText, numberFormat)

    def freezepanes(self, address, sheet=None):
        """Freeze worksheet panes.
        address = (row,1)   to freeze worksheet rows above 'row'.
                = (1,col)   to freeze worksheet columns left of 'col'.
                = (row,col) to freeze worksheet rows above 'row' and columns left of 'col'
        """
        if self.READONLY and not self.READONLYEXISTS:
            return
        cell_or_rng, topRow, leftCol, bottomRow, rightCol = self._check_cell_or_range(address)
        if not cell_or_rng:
            return
        if cell_or_rng == 'cell':
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                return
            cell.Select()
            self.xlapp.ActiveWindow.FreezePanes = True

    def _row_cln_oprn(self, address, howmany, sheet=None):
        cell, topRow, leftCol = (None, None, None)
        if self.READONLY:
            return (cell, howmany, topRow, leftCol)
        else:
            cell_or_rng, topRow, leftCol, bottomRow, rightCol = self._check_cell_or_range(address)
            if not cell_or_rng:
                return (cell, howmany, topRow, leftCol)
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                return (cell, howmany, topRow, leftCol)
            if type(howmany) != int:
                try:
                    howmany = int(howmany)
                except:
                    howmany = 1

            return (
             cell, howmany, topRow, leftCol)

    def delete_columns(self, address, howmany=1, sheet=None):
        """Delete columns to the right of specified row.
        """
        cell, howmany, topRow, leftCol = self._row_cln_oprn(address, howmany, sheet)
        if not cell:
            return
        for each in range(howmany):
            cell.EntireColumn.Delete()
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                break

    def delete_rows(self, address, howmany=1, sheet=None):
        """Delete rows below specified row.
        """
        cell, howmany, topRow, leftCol = self._row_cln_oprn(address, howmany, sheet)
        if not cell:
            return
        for each in range(howmany):
            cell.EntireRow.Delete()
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                break

    def insert_columns(self, address, howmany=1, sheet=None):
        """Insert columns to the right of specified row.
        """
        cell, howmany, topRow, leftCol = self._row_cln_oprn(address, howmany, sheet)
        if not cell:
            return
        for each in range(howmany):
            cell.EntireColumn.Insert()

    def insert_rows(self, address, howmany=1, sheet=None):
        """Insert rows below specified row.
        """
        cell, howmany, topRow, leftCol = self._row_cln_oprn(address, howmany, sheet)
        if not cell:
            return
        for each in range(howmany):
            cell.EntireRow.Insert()

    def height(self, address, height, sheet=None):
        """Set height of one row or multiple rows. Height is provided in points.
        One row, address = (row,col)
        Multiple rows, address = (topRow,leftCol,bottomRow,rightCol)
        """
        if self.READONLY:
            return
        if not height:
            return
        cell_or_rng, topRow, leftCol, bottomRow, rightCol = self._check_cell_or_range(address)
        if not cell_or_rng:
            return
        if cell_or_rng == 'cell':
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                return
            cell.EntireRow.RowHeight = height
        else:
            rng = self._active_range((topRow, leftCol, bottomRow, rightCol), sheet)
            if not rng:
                return
            rng.Rows.RowHeight = height

    def hide(self):
        """Hide opened excel workbook.
        """
        self.xlapp.Visible = False

    def merge(self, address, sheet=None):
        """Merge cells in the range.
        """
        if self.READONLY:
            return
        rng = self._active_range(address, sheet)
        if not rng:
            return
        rng.Merge()

    def page_footer(self, left=None, center=None, right=None, sheet=None):
        """Set Page Footers (left, center, right). Footer input value is a string.
        """
        if self.READONLY:
            return
        sht = self._valid_sheet(sheet)
        if left:
            left = self._get_header_footer_code(left)
            self._setPageSetup('LeftFooter', left, sht)
        if center:
            center = self._get_header_footer_code(center)
            self._setPageSetup('CenterFooter', center, sht)
        if right:
            right = self._get_header_footer_code(right)
            self._setPageSetup('RightFooter', right, sht)

    def page_format(self, orientation='portrait', left=1.0, right=1.0, top=1.0, bottom=1.0, header=0.5, footer=0.5, sheet=None):
        """Set Page format: orientitation, margins (given in inches).
            Orientation = 'portrait'  or 'p' or 1
                          'landscape' or 'l' or 2
        Defaults: orientation = Portrait
                  margins: left   = 1.0  inch
                           right  = 1.0  inch
                           top    = 1.0  inch
                           bottom = 1.0  inch
                           header = 0.5 inch
                           footer = 0.5 inch
        """
        if self.READONLY:
            return
        if isinstance(orientation, str):
            orient = orientation.lower()
        else:
            orient = orientation
        if orient in ('portrait', 'p', 1):
            self.page_portrait(sheet)
        elif orient in ('landscape', 'l', 2):
            self.page_landscape(sheet)
        self.page_margin(left, right, top, bottom, header, footer, sheet)

    def page_header(self, left=None, center=None, right=None, sheet=None):
        """Set Page Headers (left, center, right). Header input value is a string.
        """
        if self.READONLY:
            return
        sht = self._valid_sheet(sheet)
        if left:
            left = self._get_header_footer_code(left)
            self._setPageSetup('LeftHeader', left, sht)
        if center:
            center = self._get_header_footer_code(center)
            self._setPageSetup('CenterHeader', center, sht)
        if right:
            right = self._get_header_footer_code(right)
            self._setPageSetup('RightHeader', right, sht)

    def page_landscape(self, sheet=None):
        """Set Page Orientation to landscape.
        """
        if self.READONLY:
            return
        sht = self._valid_sheet(sheet)
        self._setPageSetup('Orientation', _PAGE_ORIENTATION['landscape'], sht)

    def page_margin(self, left=1.0, right=1.0, top=1.0, bottom=1.0, header=0.5, footer=0.5, sheet=None):
        """Set Page Margins. The margin value is given in inches.
        """
        if self.READONLY:
            return
        sht = self._valid_sheet(sheet)
        left = self._get_inches_to_points(left)
        if left:
            self._setPageSetup('LeftMargin', left, sht)
        right = self._get_inches_to_points(right)
        if right:
            self._setPageSetup('RightMargin', right, sht)
        top = self._get_inches_to_points(top)
        if top:
            self._setPageSetup('TopMargin', top, sht)
        bottom = self._get_inches_to_points(bottom)
        if bottom:
            self._setPageSetup('BottomMargin', bottom, sht)
        header = self._get_inches_to_points(header)
        if header:
            self._setPageSetup('HeaderMargin', header, sht)
        footer = self._get_inches_to_points(footer)
        if footer:
            self._setPageSetup('FooterMargin', footer, sht)

    def page_portrait(self, sheet=None):
        """Set Page Orientation to portrait.
        """
        if self.READONLY:
            return
        sht = self._valid_sheet(sheet)
        self._setPageSetup('Orientation', _PAGE_ORIENTATION['portrait'], sht)

    def save(self, xlsfile=None):
        """Save active excel workbook.
        - xlsfile name is provided when creating Excel workbook object
        xlsfile = save()
        - Save to a new xlsfile
        xlsfile = save(xlsfile)
        This returns name of saved excel file.
        """
        if self.READONLY:
            return
        if xlsfile:
            fnam = self._get_save_filename(xlsfile)
        elif self.XLSFNAM:
            fnam = self.XLSFNAM
        else:
            fnam = self._get_save_filename()
        if fnam.lower() == self.XLSFNAM.lower():
            display = self.xlapp.DisplayAlerts
            if display:
                self.xlapp.DisplayAlerts = False
        else:
            display = False
        try:
            self.xlbook.SaveAs(fnam)
        except:
            fnam = ''

        if display:
            self.xlapp.DisplayAlerts = True
        return fnam

    def set_active_sheet(self, sheet):
        """Set 'sheet' as active worksheet.
        """
        if not sheet:
            return
        if self.READONLY and not self.READONLYEXISTS:
            return
        sht = self.xlbook.Worksheets(sheet)
        sht.Activate()

    def set_cell(self, address, value, fontStyle=None, fontName=None, fontSize=None, fontColor=None, wrapText=False, numberFormat=None, sheet=None):
        """Set value to one cell.
        """
        if self.READONLY:
            return
        r, c = self._decode_cell_address(address)
        if not r or not c:
            return
        cell = self._active_cell((r, c), sheet)
        if not cell:
            return
        cell.Value = value
        self.font(address, fontStyle, fontName, fontSize, fontColor, wrapText, numberFormat, sheet)

    def set_range(self, topRow, leftCol, data, transpose=False, fontStyle=None, fontName=None, fontSize=None, fontColor=None, wrapText=False, numberFormat=None, sheet=None):
        """Set data to cells in the range.
        bottomRow, rightCol = set_range(topRow, leftCol, data, ...)
        Inputs:
        data      - List or List of Lists values to be written
        transpose - Logical
            Excel methods write data row by row. If data in Python list of lists, or
            tuple of tuples or any combination of these, is not stored that way,
            transpose that data. This functions same as matrix transpose.
        Returns:
            This returns values of bottom row and right column.
        """
        if self.READONLY:
            return (None, None)
        else:
            topRow = self._decode_row_address(topRow)
            leftCol = self._decode_column_address(leftCol)
            if not topRow or not leftCol:
                return (None, None)
            nrows, nclns, data = self.transpose_data(data, transpose)
            bottomRow = topRow + nrows - 1
            rightCol = leftCol + nclns - 1
            address = (topRow, leftCol, bottomRow, rightCol)
            rng = self._active_range(address, sheet)
            if not rng:
                return (None, None)
            rng.Value = data
            self.font(address, fontStyle, fontName, fontSize, fontColor, wrapText, numberFormat, sheet)
            return (
             bottomRow, rightCol)

    def get_cell(self, address, sheet=None):
        """Get value from one cell.
        """
        if self.READONLY and not self.READONLYEXISTS:
            return None
        else:
            r, c = self._decode_cell_address(address)
            if not r or not c:
                return None
            cell = self._active_cell((r, c), sheet)
            if not cell:
                return None
            value = cell.Value
            value = self._convert_unicode2str_none2space_value(value)
            return value

    def get_range(self, address, transpose=False, sheet=None):
        """Get data from cells in the range.
        data = get_range(address, ...)
        Inputs:
        address   - range tuple specified as (topRow, leftCol, bottomRow, rightCol)
        transpose - Logical
            Excel methods read data row by row and returned as Python list of lists.
            transpose = False
                Each returned list represents data in a speadsheet row.
            transpose = True
                Each returned list represents data in a speadsheet column.
        Returns:
            data = List or List of Lists values.
        """
        if self.READONLY and not self.READONLYEXISTS:
            return None
        else:
            cell_or_rng, topRow, leftCol, bottomRow, rightCol = self._check_cell_or_range(address)
            if not cell_or_rng:
                return []
            if cell_or_rng == 'cell':
                retv = self.get_cell((topRow, leftCol), sheet)
                vlist = [retv]
            else:
                rng = self._active_range((topRow, leftCol, bottomRow, rightCol), sheet)
                retv = rng.Value
                nrows, nclns, vlist = self.transpose_data(retv, transpose)
            retlist = self._convert_unicode2str_none2space_list(vlist)
            if len(retlist) == 1:
                retlist = retlist[0]
            del retv
            del vlist
            return retlist

    def show(self):
        """Show opened excel workbook.
        """
        self.xlapp.Visible = True

    def show_alerts(self, display):
        """Show or suppresses all POP-UP windows, like File Overwrite Yes/No/Cancel, Merge Overwrite.
        display = True  or 1, show alerts
                = False or 0, do not show alerts. Data will be overwritten.
        """
        if display:
            self.xlapp.DisplayAlerts = True
        else:
            self.xlapp.DisplayAlerts = False

    def transpose_data(self, data, transpose=True):
        """Transpose data.
        Excel methods write data row by row. If data in Python list of lists, or
        tuple of tuples or any combination of these, is not stored that way,
        transpose that data. This functions same as matrix transpose.

        nrows, nclns, datat = set_range(data, transpose=True)

        Inputs:
        data      - data to be transposed
        transpose - Logical, True or False, True by default

        Returns:
        nrows - number of rows in transposed data
        nclns - number of columns in transposed data
        datat - transposed data
        """
        nrows, nclns, list1dim = self._size_inlist(data)
        if transpose:
            data = self._convert_row2col(nrows, nclns, list1dim, data)
            nrows0 = nrows
            nrows = nclns
            nclns = nrows0
        else:
            data = self._convert_tup2lst(data)
        return (nrows, nclns, data)

    def width(self, address, width, sheet=None):
        """Set width of one column or multiple columns. Width is provided in points.
        One column, address = (row,col)
        Multiple columns, address = (topRow,leftCol,topRow,rightCol)
        """
        if self.READONLY:
            return
        if not width:
            return
        cell_or_rng, topRow, leftCol, bottomRow, rightCol = self._check_cell_or_range(address)
        if not cell_or_rng:
            return
        if cell_or_rng == 'cell':
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                return
            cell.EntireColumn.ColumnWidth = width
        else:
            rng = self._active_range((topRow, leftCol, bottomRow, rightCol), sheet)
            if not rng:
                return
            rng.Columns.ColumnWidth = width

    def worksheet_add_after(self, newSheet=None, oldSheet=None, overwritesheet=True):
        """Add a newSheet after the oldSheet or active sheet. If newSheet name is not provided,
        Sheet# worksheet is added. If oldSheet name is not provided, worksheet is added
        at the end. Sheet# is a next available sheet number in active workbook.
        """
        if self.READONLY:
            return
        else:
            sht = self._valid_sheet(oldSheet)
            if newSheet:
                newSheet = newSheet.strip()
                addnewsht = self._worksheet_overwrite(newSheet, overwritesheet)
                if addnewsht:
                    if sht:
                        self.xlbook.Worksheets.Add(None, sht).Name = newSheet
                    else:
                        self.xlbook.Worksheets.Add().Name = newSheet
            elif sht:
                self.xlbook.Worksheets.Add(None, sht)
            else:
                self.xlbook.Worksheets.Add()
            return

    def worksheet_add_before(self, newSheet=None, oldSheet=None, overwritesheet=True):
        """Add a newSheet before the oldSheet or active sheet. If newSheet name is not provided,
        Sheet# worksheet is added. If oldSheet name is not provided, worksheet is added
        at the end. Sheet# is a next available sheet number in active workbook.
        """
        if self.READONLY:
            return
        sht = self._valid_sheet(oldSheet)
        if newSheet:
            newSheet = newSheet.strip()
            addnewsht = self._worksheet_overwrite(newSheet, overwritesheet)
            if addnewsht:
                if sht:
                    self.xlbook.Worksheets.Add(sht).Name = newSheet
                else:
                    self.xlbook.Worksheets.Add().Name = newSheet
        elif sht:
            self.xlbook.Worksheets.Add(sht)
        else:
            self.xlbook.Worksheets.Add()

    def worksheet_add_begin(self, sheet=None, overwritesheet=True):
        """Add a sheet at the beginning. If sheet name is not provided, Sheet# worksheet
        is added. Sheet# is a next available sheet number in active workbook.
        """
        if self.READONLY:
            return
        frstsht = self.xlbook.Sheets(1).Name
        self.worksheet_add_before(sheet, frstsht, overwritesheet)

    def worksheet_add_end(self, sheet=None, overwritesheet=True):
        """Add a sheet at the end. If sheet name is not provided, Sheet# worksheet
        is added. Sheet# is a next available sheet number in active workbook.
        """
        if self.READONLY:
            return
        nshts = self.xlbook.Sheets.Count
        lastsht = self.xlbook.Sheets(nshts).Name
        self.worksheet_add_after(sheet, lastsht, overwritesheet)

    def worksheet_delete(self, sheet):
        """Delete a sheet from active workbook.
        """
        if self.READONLY:
            return
        nshts = self.xlbook.Sheets.Count
        if not nshts:
            return
        tmpshtnames = []
        for i in range(1, nshts + 1):
            tmpnam = self.xlbook.Sheets(i).Name
            tmpshtnames.append(tmpnam.lower())

        shtnam = sheet.lower()
        if shtnam in tmpshtnames:
            idx = tmpshtnames.index(shtnam)
            self.xlbook.Sheets(tmpshtnames[idx]).Delete()

    def worksheet_left_columns2repeat(self, columns, sheet=None):
        """Repeat 'columns' at the left of each page of the worksheet.
        'columns' is specified as tuple or list of column numbers,
        e.g., columns = (1,3) to repeat columns 1 to 3 at the left or
              columns = 1     to repeat column 1 at the left.
        """
        if self.READONLY:
            return
        if not columns:
            return
        sht = self._valid_sheet(sheet)
        if isinstance(columns, tuple) or isinstance(columns, list):
            if columns[1] < columns[0]:
                c0 = columns[0]
                cn = columns[1]
            else:
                c0 = columns[1]
                cn = columns[0]
        else:
            c0 = columns
            cn = columns
        rng = sht.Range(sht.Cells(1, c0), sht.Cells(1, cn))
        sht.PageSetup.PrintTitleColumns = rng.Columns.Address

    def worksheet_rename(self, newSheet, oldSheet=None, overwritesheet=True):
        """Rename excel 'old' sheet or active sheet.
        overwritesheet = True, contents of oldSheet are deleted, so newSheet is blank worksheet
                       = False, contents of oldSheet are written to newSheet.
        """
        if self.READONLY:
            return
        newSheet = newSheet.strip()
        if not newSheet:
            return
        sht = self._valid_sheet(oldSheet)
        if not sht:
            return
        if overwritesheet:
            sht.Cells.ClearContents()
        sht.Name = newSheet

    def worksheet_size_violation(self, topRow, leftCol, data=None, transpose=False):
        """Get worksheet size violations and extents.
        rtple = worksheet_size_violation(topRow, leftCol, ...)
        Inputs:
        data      - List or List of Lists values to be written
        transpose - Logical
            Excel methods write data row by row. If data in Python list of lists, or
            tuple of tuples or any combination of these, is not stored that way,
            transpose that data. This functions same as matrix transpose.
        Returns:
        Returned tuple contains:
        row_violation = rtple[0], True when top/bottom row exceeds maximum allowable rows
        col_violation = rtple[2], True when left/right column exceeds maximum allowable columns
        topRow        = rtple[3], top row number
        leftCol       = rtple[4], left column number
        bottomRow     = rtple[5], bottom row number
        rightCol      = rtple[6], right column number
        wshtmaxrows   = rtple[7], = 65536, maximum number of rows allowed in a worksheet
        wshtmaxcols   = rtple[8], = 256, maximum number of columns allowed in a worksheet
        """
        if data:
            nrows, nclns, list1dim = self._size_inlist(data)
            if transpose:
                nrows0 = nrows
                nrows = nclns
                nclns = nrows0
            bottomRow = topRow + nrows - 1
            rightCol = leftCol + nclns - 1
        else:
            bottomRow = topRow
            rightCol = leftCol
        if topRow > self.MAXROWS or bottomRow > self.MAXROWS:
            row_violation = True
        else:
            row_violation = False
        if leftCol > self.MAXCOLUMNS or rightCol > self.MAXCOLUMNS:
            col_violation = True
        else:
            col_violation = False
        retval = (row_violation, col_violation, topRow, leftCol, bottomRow, rightCol, self.MAXROWS, self.MAXCOLUMNS)
        return retval

    def worksheet_top_rows2repeat(self, rows, sheet=None):
        """Repeat 'rows' at the top of each page of the worksheet.
        'rows' is specified as tuple or list of row numbers,
        e.g., rows = (1,3) to repeat rows 1 to 3 at the top or
              rows = 1     to repeat row 1 at the top.
        """
        if self.READONLY:
            return
        if not rows:
            return
        sht = self._valid_sheet(sheet)
        if isinstance(rows, tuple) or isinstance(rows, list):
            if rows[1] < rows[0]:
                r0 = rows[0]
                rn = rows[1]
            else:
                r0 = rows[1]
                rn = rows[0]
        else:
            r0 = rows
            rn = rows
        rng = sht.Range(sht.Cells(r0, 1), sht.Cells(rn, 1))
        sht.PageSetup.PrintTitleRows = rng.Rows.Address

    def wraptext(self, address, sheet=None):
        """Wrap Text inside the cell or range.
        Cell, address = (row,col)
        Range, address = (topRow,leftCol,bottomRow,rightCol)
        """
        if self.READONLY:
            return
        cell_or_rng, topRow, leftCol, bottomRow, rightCol = self._check_cell_or_range(address)
        if not cell_or_rng:
            return
        if cell_or_rng == 'cell':
            cell = self._active_cell((topRow, leftCol), sheet)
            if not cell:
                return
            cell.WrapText = True
        else:
            rng = self._active_range((topRow, leftCol, bottomRow, rightCol), sheet)
            if not rng:
                return
            rng.WrapText = True

    def _setPageSetup(self, attr, val, sht):
        try:
            setattr(sht.PageSetup, attr, val)
        except:
            pass

    def _active_cell(self, address, sheet=None):
        sht = self._valid_sheet(sheet)
        if sht:
            cell = sht.Cells(address[0], address[1])
        else:
            cell = None
        return cell

    def _active_range(self, address, sheet=None):
        sht = self._valid_sheet(sheet)
        if sht:
            topRow, leftCol, bottomRow, rightCol = address
            rng = sht.Range(sht.Cells(topRow, leftCol), sht.Cells(bottomRow, rightCol))
        else:
            rng = None
        return rng

    def _check_cell_or_range(self, address):
        cell_or_rng, topRow, leftCol, bottomRow, rightCol = (None, None, None, None,
                                                             None)
        if type(address) != str and type(address) not in [tuple, list]:
            return (cell_or_rng, topRow, leftCol, bottomRow, rightCol)
        else:
            if type(address) == str:
                topRow, leftCol = self._decode_cell_address(address)
                if topRow and leftCol:
                    cell_or_rng = 'cell'
            else:
                lenadr = len(address)
                if lenadr not in (2, 4):
                    return (cell_or_rng, topRow, leftCol, bottomRow, rightCol)
                if lenadr == 2:
                    v1 = address[0]
                    v2 = address[1]
                    if type(v1) == int and type(v2) == int or type(v1) == int and type(v2) == str:
                        topRow, leftCol = self._decode_cell_address(address)
                        if topRow and leftCol:
                            cell_or_rng = 'cell'
                    else:
                        topRow, leftCol, bottomRow, rightCol = self._decode_range_address(address)
                        if topRow and leftCol and bottomRow and rightCol:
                            cell_or_rng = 'range'
                else:
                    topRow, leftCol, bottomRow, rightCol = self._decode_range_address(address)
                    if topRow and leftCol and bottomRow and rightCol:
                        cell_or_rng = 'range'
            return (
             cell_or_rng, topRow, leftCol, bottomRow, rightCol)

    def _decode_colnam2colnum(self, nam):
        nam = nam.strip()
        nam = nam.upper()
        namlen = len(nam)
        num = 0
        for i in range(namlen):
            num += (ord(nam[i]) - 64) * 26 ** (namlen - i - 1)

        return num

    def _decode_row_address(self, row):
        if type(row) == int:
            pass
        elif type(row) == str:
            row = row.strip()
            if row.isdigit():
                row = int(row)
            else:
                row = None
        else:
            row = None
        return row

    def _decode_column_address(self, cln):
        if type(cln) == int:
            pass
        elif type(cln) == str:
            cln = cln.strip()
            if cln.isalpha():
                cln = self._decode_colnam2colnum(cln)
            else:
                cln = None
        else:
            cln = None
        return cln

    def _decode_cell_address_str(self, address):
        if address.isalpha() or address.isdigit():
            return (None, None)
        namlen = len(address)
        for i in range(namlen):
            if address[i].isalpha():
                continue
            if address[i].isdigit():
                break
            return (None, None)

        row = self._decode_row_address(address[i:])
        cln = self._decode_column_address(address[:i])
        return (
         row, cln)

    def _decode_cell_address(self, address):
        if type(address) == str:
            address = address.strip()
            row, cln = self._decode_cell_address_str(address)
        elif type(address) in [tuple, list]:
            if len(address) == 2:
                row = self._decode_row_address(address[0])
                cln = self._decode_column_address(address[1])
            else:
                row, cln = (None, None)
        else:
            row, cln = (None, None)
        if not row or not cln:
            print 'Invalid cell address: ', address
        return (row, cln)

    def _decode_range_address(self, address):
        if type(address) not in [tuple, list]:
            print 'Invalid range address: ', address
            return (None, None, None, None)
        else:
            lenadr = len(address)
            if lenadr not in (2, 4):
                print 'Invalid range address: ', address
                return (None, None, None, None)
            if lenadr == 2:
                cell1 = address[0]
                cell2 = address[1]
            else:
                cell1 = (
                 address[0], address[1])
                cell2 = (address[2], address[3])
            rtop, clft = self._decode_cell_address(cell1)
            rbot, crit = self._decode_cell_address(cell2)
            return (
             rtop, clft, rbot, crit)

    def _get_border_index(self, border):
        try:
            bdindex = _BORDER_INDEX[border.lower()]
        except:
            bdindex = None

        return bdindex

    def _get_border_weight(self, weight):
        try:
            bdweight = _BORDER_WEIGHT[weight.lower()]
        except:
            bdweight = None

        return bdweight

    def _get_color_index(self, color):
        if isinstance(color, str):
            try:
                colorindex = _FONT_COLORINDEX[color.lower()]
            except:
                colorindex = 1

        elif isinstance(color, int):
            if color > 56 or color < 0:
                colorindex = 1
            else:
                colorindex = color
        else:
            colorindex = 1
        return colorindex

    def _convert_row2col(self, nrows, nclns, list1dim, inlist):
        """
        Converting data in rows to data in columns, similar to transpose of matrix

        Writing Python lists to Excel Spreadsheet
        (1) Writing over one row and multiple columns
            list1=[v1,v2,v3,v4]
            row =1
            lcln=1
            tr, lc, br, rc = row, lcln, row, len(list1) #toprow, leftcolumn, bottomrow, rightcolumn
            xlSheet.Range(xlSheet.Cells(tr,lc),xlSheet.Cells(br,rc)).Value = list1

        (2) Writing over multiple rows and one column
            list1=[v1,v2,v3,v4]
            Need to convert list1 as 4 rows x 1 column matrix
            list2=[[v1],[v2],[v3],[v4]]
            trow =1
            lc   =1
            tr, lc, br, rc = trow, lc, row+len(list2), lc #toprow, leftcolumn, bottomrow, rightcolumn
            xlSheet.Range(xlSheet.Cells(tr,lc),xlSheet.Cells(br,rc)).Value = list2

        (3) Writing over multiple rows and multiple columns
            (a)
            list1=[[v11,v12,v13,v14],[v21,v22,v23,v24]]
            nrows = len(list1)
            nclns = len(list1[0])
            trow =1
            lc   =1
            tr, lc, br, rc = trow, lc, row+nrows, lc+nclns #toprow, leftcolumn, bottomrow, rightcolumn
            xlSheet.Range(xlSheet.Cells(tr,lc),xlSheet.Cells(br,rc)).Value = list1

            (b)
            list1=[[v11,v21,v31,v41],[v12,v22,v32,v42]]
            Need to convert list1 as 4 rows x 2 columns matrix.
            list2=[[v11,v12],[v21,v22],[v31,v32],[v41,v42]]
            nrows = len(list2)
            nclns = len(list2[0])
            trow =1
            lc   =1
            tr, lc, br, rc = trow, lc, row+nrows, lc+nclns #toprow, leftcolumn, bottomrow, rightcolumn
            xlSheet.Range(xlSheet.Cells(tr,lc),xlSheet.Cells(br,rc)).Value = list2
        """
        outmat = []
        for i in range(nclns):
            tmprow = []
            if nrows > 1:
                for j in range(nrows):
                    tmprow.append(inlist[j][i])

            elif list1dim:
                tmprow.append(inlist[i])
            else:
                tmprow.append(inlist[0][i])
            outmat.append(tmprow)

        return outmat

    def _convert_tup2lst(self, intup):
        """
        Converting input tuple into list or tuple of tuples  into list of lists.
        """
        outmat = []
        for each in intup:
            if type(each) == tuple:
                e = list(each)
            else:
                e = each
            outmat.append(e)

        return outmat

    def _convert_unicode2str_none2space_list(self, inlist):
        nrows, nclns, list1dim = self._size_inlist(inlist)
        outmat = []
        for i in range(nrows):
            tmprow = []
            if nrows > 1:
                for j in range(nclns):
                    v = self._convert_unicode2str_none2space_value(inlist[i][j])
                    tmprow.append(v)

            elif list1dim:
                v = self._convert_unicode2str_none2space_value(inlist[i])
                tmprow.append(v)
            else:
                v = self._convert_unicode2str_none2space_value(inlist[0])
                tmprow = v
            outmat.append(tmprow)

        return outmat

    def _convert_unicode2str_none2space_value(self, invalue):
        if invalue == None:
            retv = ''
        elif type(invalue) == unicode:
            retv = invalue.encode('cp1250')
        elif type(invalue) == float:
            retv = '%f' % invalue
            retv = float(retv)
        else:
            retv = invalue
        return retv

    def _get_constants(self):
        """
        To get definitions of xl... variables (viz., xlVAlignTop, xlVAlignBottom) when
        Excel object is created using Method 2 below.
        This is used here.

        (1) If excel object is created using:
            self.xlapp = win32com.client.dynamic.Dispatch("Excel.Application")
            (late-bound automation)

            Define these variables with appropriate values. As an example:
            _VALIGN_TOP = -4160

            Refer Microsoft Excel Constants [Excel 2003 VBA Language Reference] at
            http://msdn2.microsoft.com/en-us/library/aa221100(office.11).aspx

        (2) If excel object is created using:
            self.xlapp = win32com.client.gencache.EnsureDispatch('Excel.Application',1)
            This would run MakePy and create support for early-bound automation.
            You need to run this only once.

            After this following command works.
            self.xlapp = win32com.client.Dispatch("Excel.Application")

            Then these variables can be accessed as:
            _VALIGN_TOP = win32com.client.constants.xlVAlignTop

            Note: You need to create object 1st to access these variables.
        """
        global _ALIGN_H
        global _ALIGN_V
        global _BORDER_INDEX
        global _BORDER_INDEX_CELL
        global _BORDER_WEIGHT
        global _LINE_STYLE
        global _PAGE_ORIENTATION
        _PAGE_ORIENTATION = {'landscape': (win32com.client.constants.xlLandscape), 
           'portrait': (win32com.client.constants.xlPortrait)}
        _ALIGN_H = {'h_center': (win32com.client.constants.xlHAlignCenter), 
           'h_centre': (win32com.client.constants.xlHAlignCenter), 
           'left': (win32com.client.constants.xlHAlignLeft), 
           'right': (win32com.client.constants.xlHAlignRight)}
        _ALIGN_V = {'bottom': (win32com.client.constants.xlVAlignBottom), 
           'v_center': (win32com.client.constants.xlVAlignCenter), 
           'v_centre': (win32com.client.constants.xlVAlignCenter), 
           'top': (win32com.client.constants.xlVAlignTop)}
        _BORDER_INDEX = {'diagonaldown': (win32com.client.constants.xlDiagonalDown), 
           'diagonalup': (win32com.client.constants.xlDiagonalUp), 
           'bottom': (win32com.client.constants.xlEdgeBottom), 
           'left': (win32com.client.constants.xlEdgeLeft), 
           'right': (win32com.client.constants.xlEdgeRight), 
           'top': (win32com.client.constants.xlEdgeTop), 
           'hinside': (win32com.client.constants.xlInsideHorizontal), 
           'vinside': (win32com.client.constants.xlInsideVertical), 
           'none': 'noborder', 
           'outline': 'outlineborder', 
           'inside': 'insideborder'}
        _BORDER_INDEX_CELL = [
         'diagonaldown', 'diagonalup', 'bottom', 'top', 'left', 
         'right', 
         'none', 'outline']
        _BORDER_WEIGHT = {'hairline': (win32com.client.constants.xlHairline), 
           'medium': (win32com.client.constants.xlMedium), 
           'thick': (win32com.client.constants.xlThick), 
           'thin': (win32com.client.constants.xlThin)}
        _LINE_STYLE = {'continuous': (win32com.client.constants.xlContinuous), 
           'dash': (win32com.client.constants.xlDash), 
           'dashdot': (win32com.client.constants.xlDashDot), 
           'dashdotdot': (win32com.client.constants.xlDashDotDot), 
           'dot': (win32com.client.constants.xlDot), 
           'double': (win32com.client.constants.xlDouble), 
           'none': (win32com.client.constants.xlLineStyleNone), 
           'slantdashdot': (win32com.client.constants.xlSlantDashDot)}

    def _get_constants_specified(self):
        """
        To get definitions of xl... variables (viz., xlVAlignTop, xlVAlignBottom) when
        Excel object is created using Method 1 below.
        This is not used.

        (1) If excel object is created using:
            self.xlapp = win32com.client.dynamic.Dispatch("Excel.Application")
            OR
            self.xlapp = win32com.client.Dispatch("Excel.Application")
            (late-bound automation)

            Define these variables with appropriate values. As an example:
            _VALIGN_TOP = -4160

            Refer Microsoft Excel Constants [Excel 2003 VBA Language Reference] at
            http://msdn2.microsoft.com/en-us/library/aa221100(office.11).aspx

        (2) If excel object is created using:
            self.xlapp = win32com.client.gencache.EnsureDispatch('Excel.Application',1)
            This would run MakePy and create support for early-bound automation.
            You need to run this only once.

            After this following command works.
            self.xlapp = win32com.client.Dispatch("Excel.Application")

            Then these variables can be accessed as:
            _VALIGN_TOP = win32com.client.constants.xlVAlignTop

            Note: You need to create object 1st to access these variables.
        """
        global _ALIGN_H
        global _ALIGN_V
        global _BORDER_INDEX
        global _BORDER_INDEX_CELL
        global _BORDER_WEIGHT
        global _LINE_STYLE
        global _PAGE_ORIENTATION
        _PAGE_ORIENTATION = {'landscape': 2, 
           'portrait': 1}
        _ALIGN_H = {'h_center': (-4108), 
           'h_centre': (-4108), 
           'left': (-4131), 
           'right': (-4152)}
        _ALIGN_V = {'bottom': (-4107), 
           'v_center': (-4108), 
           'v_centre': (-4108), 
           'top': (-4160)}
        _BORDER_INDEX = {'diagonaldown': 5, 
           'diagonalup': 6, 
           'bottom': 9, 
           'left': 7, 
           'right': 10, 
           'top': 8, 
           'hinside': 12, 
           'vinside': 11, 
           'none': 'noborder', 
           'outline': 'outlineborder', 
           'inside': 'insideborder'}
        _BORDER_INDEX_CELL = [
         'diagonaldown', 'diagonalup', 'bottom', 'top', 'left', 
         'right', 
         'none', 'outline']
        _BORDER_WEIGHT = {'hairline': 1, 
           'medium': (-4138), 
           'thick': 4, 
           'thin': 2}
        _LINE_STYLE = {'continuous': 1, 
           'dash': (-4115), 
           'dashdot': 4, 
           'dashdotdot': 5, 
           'dot': (-4118), 
           'double': (-4119), 
           'none': (-4142), 
           'slantdashdot': 13}

    def _get_fontstyle_tuple(self, fontStyle):
        """
        """
        fstyle = []
        if isinstance(fontStyle, type([])) or isinstance(fontStyle, type(())):
            for each in fontStyle:
                each = each.lower()
                if each in ('regular', 'bold', 'italic', 'underline'):
                    fstyle.append(each)

        elif fontStyle.lower() in ('regular', 'bold', 'italic', 'underline'):
            fstyle.append(fontStyle.lower())
        if not fstyle:
            fstyle.append('regular')
        return tuple(fstyle)

    def _get_header_footer_code(self, instr):
        for k, v in _HEADER_FOOTER_CODES.iteritems():
            instr = self._replace_case_insensitive(instr, k, v)

        return instr

    def _get_inches_to_points(self, val):
        try:
            val = self.xlapp.InchesToPoints(float(val))
        except:
            val = None

        return val

    def _get_line_style(self, style):
        try:
            lnstyle = _LINE_STYLE[style.lower()]
        except:
            lnstyle = None

        return lnstyle

    def _get_input_filename(self, xlsfnam):
        xlsfnam = xlsfnam.strip()
        p, nx = os.path.split(xlsfnam)
        n, x = os.path.splitext(nx)
        if not p:
            p = os.getcwd()
        try:
            fnam = os.path.join(p, n)
        except:
            u_p = _smart_unicode(p, errors='strict')
            u_n = _smart_unicode(n, errors='strict')
            if u_p and u_n:
                try:
                    fnam = os.path.join(u_p, u_n)
                except:
                    fnam = n

            else:
                fnam = n

        if not x:
            fnam = fnam + self.EXTN
        else:
            fnam = fnam + x
        return fnam

    def _get_save_filename(self, xlsfnam=''):
        if xlsfnam:
            xlsfnam = xlsfnam.strip()
        else:
            xlsfnam = self.xlbook.Name
        p, nx = os.path.split(xlsfnam)
        n, x = os.path.splitext(nx)
        if not p:
            p = os.getcwd()
        try:
            fnam = os.path.join(p, n)
        except:
            u_p = _smart_unicode(p, errors='strict')
            u_n = _smart_unicode(n, errors='strict')
            if u_p and u_n:
                try:
                    fnam = os.path.join(u_p, u_n)
                except:
                    fnam = n

            else:
                fnam = n

        fnam = fnam + self.EXTN
        return fnam

    def _replace_case_insensitive(self, instr, findstr, replacestr):
        findlen = len(findstr)
        instrLC = instr.lower()
        findstrLC = findstr.lower()
        resultstr = ''
        if findlen > 0:
            while True:
                npos = instrLC.find(findstr)
                if npos >= 0:
                    resultstr += instr[0:npos] + replacestr
                    instr = instr[npos + findlen:]
                    instrLC = instrLC[npos + findlen:]
                else:
                    resultstr += instr
                    break

        return resultstr

    def _set_align(self, selection, alignv):
        if alignv in _ALIGN_H.keys():
            selection.HorizontalAlignment = _ALIGN_H[alignv]
        elif alignv in _ALIGN_V.keys():
            selection.VerticalAlignment = _ALIGN_V[alignv]

    def _set_border(self, selection, bdlist, lnstyle, bdweight, colorindex):
        for bdindex in bdlist:
            selection.Borders(bdindex).LineStyle = lnstyle
            selection.Borders(bdindex).Weight = bdweight
            selection.Borders(bdindex).ColorIndex = colorindex

    def _set_border_none(self, selection, bdlist):
        lnstyle = self._get_line_style('none')
        for bdindex in bdlist:
            selection.Borders(bdindex).LineStyle = lnstyle

    def _set_font(self, what, fstyle, fname, fsize, fcolor, wrap, nfmt):
        """Set font properties: style, name, size, color, wrap, numberformat
        what: sht or cell or range
        """
        if fstyle:
            fstyle = self._get_fontstyle_tuple(fstyle)
            for i, item in enumerate(fstyle):
                if item == 'bold':
                    what.Font.Bold = True
                elif item == 'italic':
                    what.Font.Italic = True
                elif item == 'underline':
                    what.Font.Underline = True
                elif item == 'regular':
                    what.Font.FontStyle = 'Regular'

        if fname:
            what.Font.Name = fname
        if fsize:
            what.Font.Size = fsize
        if fcolor:
            colorindex = self._get_color_index(fcolor)
            what.Font.ColorIndex = colorindex
        if wrap:
            what.WrapText = True
        if nfmt:
            what.NumberFormat = nfmt

    def _size_inlist(self, inlist):
        """
        """
        len1, len2 = (0, 0)
        try:
            if type(inlist) in [list, tuple]:
                len1 = len(inlist)
            else:
                len1 = 0
        except:
            len1 = 0

        if len1:
            try:
                if type(inlist[0]) in [list, tuple]:
                    len2 = len(inlist[0])
                else:
                    len2 = 0
            except:
                len2 = 0

        if len2:
            nrows = len1
            nclns = len2
            list1dim = False
        else:
            nrows = 1
            nclns = len1
            list1dim = True
        return (nrows, nclns, list1dim)

    def _valid_sheet(self, sheet):
        try:
            sht = self.xlbook.Worksheets(sheet)
        except:
            sht = self.xlbook.ActiveSheet

        return sht

    def _worksheet_overwrite(self, sheet, overwritesheet):
        """ Check if 'sheet' exists in opened workbook.
            If sheet exist, and overwritesheet=True,
                - delete the old sheet contents
            Else If sheet exist, and overwritesheet=False
                - rename old sheet with (#) added to its name
                  where # is the next sequence number.
        """
        shtexist = False
        if sheet:
            shtnam = sheet.lower()
            nshts = self.xlbook.Sheets.Count
            namshts = [self.xlbook.Sheets(i + 1).Name for i in range(nshts)]
            namshts = [each.lower() for each in namshts]
            if shtnam in namshts:
                shtexist = True
        if shtexist:
            sht = self.xlbook.Worksheets(sheet)
            if overwritesheet:
                sht.Cells.ClearContents()
                addnewsht = False
            else:
                i = 1
                while True:
                    shtnam = shtnam + '(' + str(i) + ')'
                    if shtnam in namshts:
                        i += 1
                        shtnam = sheet.lower()
                    else:
                        break

                shtnam = sheet + '(' + str(i) + ')'
                sht.Name = shtnam
                addnewsht = True
        else:
            addnewsht = True
        return addnewsht


def workbook(xlsfile='', sheet='', overwritesheet=False, mode='w'):
    r"""Use this function to create Excel workbook object and apply methods defined in 'excelpy'
    module to create, populate and format the spreadsheets, e.g.,

    (1) When used to create new Excel files or add worksheets to existing Excel files:
    xlobj = excelpy.workbook()
    xlobj = excelpy.workbook(r"c:\working dir\ex1.xls")
    xlobj = excelpy.workbook(r"c:\working dir\ex1.xls", "MySheet") or
    xlobj = excelpy.workbook(r"c:\working dir\ex1.xls", "MySheet", False) or
    xlobj = excelpy.workbook(r"c:\working dir\ex1.xls", "MySheet", False, 'w') or
    xlobj = excelpy.workbook(xlsfile=r"c:\working dir\ex1.xls", sheet="MySheet",
                               overwritesheet=False, mode='w')

    (2) When used to read existing Excel files:
    xlobj = excelpy.workbook(r"c:\working dir\ex1.xls", mode='r')

    Note: When using Excel 2007 and later, create file in either 'xlsx' or 'xls' format.
          Excel 2003 and earlier - default save format 'xls'.
          Excel 2007 and later   - default save format 'xlsx'.
    """
    xlobj = excelpy(xlsfile, sheet, overwritesheet, mode)
    return xlobj


_NROWS2WRIT = 5000

def export_txtfile(txtfile, xlsfile='', sheet='Sheet1', delimiter='tab', overwritesheet=True, show=True, del_txtfile=False):
    """Use this function to export any Text File to Excel Spreadsheet.
    Inputs
    txtfile       : Text file name , no default allowed.
                    The data columns in this file are separated by "delimiter" specified.
    xlsfile       : Excel file name to export data to, default="Book_Text_Export"
    sheet         : Excel worksheet name, default='Sheet1'
    delimiter     : Use this character to split text file data lines into columns of spreadsheet, default='tab'
                    = 'tab' or ',' or ';' or '#'
                    any character, tab character is specified as 'tab'
    overwritesheet: Overwrite worksheets flag, default=True
                    = True,  existing worksheets are overwritten
                    = False, existing worksheets are copied and their names
    show          : Show or Hide Excel Spreadsheet flag, default True
                    = True,  show Excel Spreadsheet
                    = False, do not show Excel Spreadsheet (it will be just created and saved)
    del_txtfile   : Show or Hide Excel Spreadsheet flag, default True
                    = True,  show Excel Spreadsheet
                    = False, do not show Excel Spreadsheet (it will be just created and saved)
    Returns:
        xlsfile   : Name of the Excel file saved.
                    Depending on Excel version, file extension could be xls or xlsx.
"""
    pn, p, n, x, xlw = _filePNXvalues(txtfile)
    if not n:
        print ' Text file not provided.'
        return
    if not os.path.exists(txtfile):
        print ' Text file does not exist: %s' % txtfile
        return
    if not xlsfile:
        xlsfile = 'Book_Text_Export'
    if delimiter.lower() == 'tab':
        c_delimit = '\t'
    else:
        c_delimit = delimiter
    res_wbk = excelpy(xlsfile, sheet, overwritesheet, 'w')
    if show:
        res_wbk.show()
    rowdata = []
    row = 0
    ncln0 = -1
    diff_ncln = False
    br, rc = (1, 1)
    with open(txtfile, 'r') as txtfobj:
        for line in txtfobj:
            txt = line.strip()
            if not txt:
                continue
            if txt[0] == c_delimit:
                txt = txt[1:]
            lst = txt.split(c_delimit)
            ncln = len(lst)
            if ncln0 == -1:
                ncln0 = ncln
            elif ncln0 != ncln:
                diff_ncln = True
            if row == _NROWS2WRIT or diff_ncln:
                br, rc = res_wbk.set_range(br, rc, rowdata)
                br += 1
                rc = 1
                rowdata = []
                row = 1
                diff_ncln = False
                ncln0 = -1
                rowdata.append(lst)
            else:
                row += 1
                rowdata.append(lst)

        if rowdata:
            br, rc = res_wbk.set_range(br, rc, rowdata)
    res_wbk.save(xlsfile)
    if del_txtfile:
        try:
            os.remove(txtfile)
        except:
            pass

    if not show:
        res_wbk.close()
    return xlsfile


def _getDefaultXLFileExtension_do_NOT_use():
    vernum = 11
    xlapp = None
    chkvrsn = False
    ok_dispatchEx = False
    excel_running = _check_if_excel_running()
    try:
        xlapp = win32com.client.DispatchEx('Excel.Application')
        chkvrsn = True
        ok_dispatchEx = True
    except:
        try:
            xlapp = win32com.client.gencache.EnsureDispatch('Excel.Application')
            chkvrsn = True
        except:
            pass

    if chkvrsn:
        try:
            vernum = float(xlapp.Version)
        except:
            pass

    if vernum > 11:
        extn = '.xlsx'
    else:
        extn = '.xls'
    if chkvrsn:
        if ok_dispatchEx:
            xlapp.Quit()
        elif not excel_running:
            xlapp.Quit()
            _force_close_excel_thread(xlapp)
    return (
     vernum, extn)


def _force_close_excel_thread(xlapp):
    import time, win32process, win32gui, win32api, win32con
    hwnd = xlapp.Hwnd
    t, p = win32process.GetWindowThreadProcessId(hwnd)
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    time.sleep(10)
    try:
        handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, p)
        if handle:
            win32api.TerminateProcess(handle, 0)
            win32api.CloseHandle(handle)
    except:
        pass


def _check_if_excel_running():
    wmi = win32com.client.GetObject('winmgmts:')
    excel_is_running = False
    for process in wmi.InstancesOf('Win32_Process'):
        name = process.Properties_('Name').value
        if name.upper() == 'EXCEL.EXE':
            excel_is_running = True
            break

    return excel_is_running


if __name__ == '__main__':
    print "Excel Interface Python Functions.\nModule 'excelpy' defines easy to use excel interface Python functions.\nUse these functions to create, populate, and format Excel spreadsheets.\nSee help(excelpy) for details.\n    "

# okay decompiling excelpy.pyc
