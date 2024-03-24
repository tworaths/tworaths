# uncompyle6 version 3.9.1
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  4 2019, 01:37:19) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\pssexcel.py
# Compiled at: 2016-05-19 21:00:09
"""
Functions to Export PSSE Data/Results to Excel Spreadsheets.
These functions are documented in API Manual, Chapter 9.
Execute these functions from inside of PSS(R)E.

Functions available:
    accc, iec_data_file, pv, qv

See individual function help as, for example, help(pssexcel.accc)
"""
import os, psspy, pssarrays, excelpy, pssexceluserin
_ALTERNATE_COLORS = [
 'black', 'blue']
_EXPORT_QTY_ACCC = {'b': 'branch flow', 
   'i': 'interface flow', 
   'v': 'bus voltage', 
   's': 'summary', 
   'e': 'contingency events', 
   'g': 'generator dispatch', 
   'l': 'load shed', 
   'p': 'phase shifter angle'}
_EXPORT_QTY_IEC_DATA_FILE = {'m': 'machines', 
   't': 'transformers', 
   'i': 'iec data'}
_EXPORT_QTY_PV = {'v': 'bus voltage', 
   'b': 'branch flow', 
   'i': 'interface flow', 
   's': 'summary', 
   'g': 'generator dispatch', 
   'm': 'mismatch', 
   'l': 'bus load'}
_EXPORT_QTY_QV = {'v': 'bus voltage', 
   's': 'summary', 
   'g': 'generator dispatch', 
   'm': 'mismatch'}
_WORKSHT_SEQ_ACCC = [
 'b', 'i', 'v', 's', 'e', 'g', 'l', 'p']
_WORKSHT_SEQ_IEC_DATA_FILE = ['m', 't', 'i']
_WORKSHT_SEQ_PV = ['v', 'b', 'i', 's', 'g', 'm', 'l']
_WORKSHT_SEQ_QV = ['v', 's', 'g', 'm']

def _alternate_colors(color_now=''):
    if color_now == _ALTERNATE_COLORS[0]:
        color_now = _ALTERNATE_COLORS[1]
    else:
        color_now = _ALTERNATE_COLORS[0]
    return color_now


def _check_to_procced_to_solution(workshts):
    proceed_to_solution = False
    for k, v in workshts.iteritems():
        if v[1] and k != 'summary':
            proceed_to_solution = True
            break

    return proceed_to_solution


def _decode_bus_string(bstr):
    """
    Format:
    Length
     6       0-5  --> bus number
     1       6    --> space
    12       7-18 --> bus name
     6      19-24 --> bus voltage
    ---
    25
    If monitored branch is a 3 winding transformer, TO bus is stored as:
     6       0-5  --> 3WNDTR
     1       6    --> space
    12       7-18 --> bus name
     6      19-24 --> WND #
    ---
    25
    """
    num = bstr[:6]
    try:
        vlt = bstr[19:25]
    except:
        vlt = '0.0'

    try:
        bnam = bstr[7:19].strip()
    except:
        bnam = ''

    if num.upper() == '3WNDTR':
        bnum = num.strip()
        bvlt = vlt.strip()
    else:
        try:
            bnum = int(num)
        except:
            bnum = ''

        try:
            bvlt = float(vlt)
        except:
            bvlt = ''

    return [
     bnum, bnam, bvlt]


def _decode_bus_list(buslst):
    """
    """
    rlst = []
    for bus in buslst:
        b = _decode_bus_string(bus)
        rlst.append(b)

    return rlst


def _decode_branch_string(brnstr):
    """
    """
    bf = _decode_bus_string(brnstr[:26])
    bv = _decode_bus_string(brnstr[26:52])
    ckt = brnstr[-2:].strip()
    bf.extend(bv)
    bf.extend([ckt])
    return bf


def _decode_branch_list(brnlst):
    """
    """
    rlst = []
    for branch in brnlst:
        brn = _decode_branch_string(branch)
        rlst.append(brn)

    return rlst


def _decode_interface_string(itfstr):
    """
    """
    itfnam = itfstr[17:].strip()
    return [
     itfnam]


def _decode_interface_list(itflst):
    """
    """
    rlst = []
    for itf in itflst:
        itfnam = _decode_interface_string(itf)
        rlst.append(itfnam)

    return rlst


def _get_file_path_name_ext(infile):
    p, n, x = ('', '', '')
    if infile:
        p, nx = os.path.split(infile)
        n, x = os.path.splitext(nx)
    return (p, n, x)


def _get_worksheet_names_status(valid_instrlst, valid_string_dict, sheet):
    """
    Returned workshts is dictionary with:
        keys as strings from _EXPORT_xxx names.
        values as list of [worksheet name, status].

        status  = True when worksheet is requested
                = False when worksheet is not requested.
    """
    valid_string = valid_string_dict.keys()
    if sheet:
        sheet = sheet.strip() + ' '
    else:
        sheet = ''
    workshts = {}
    for k in valid_string:
        v = valid_string_dict[k]
        if k in valid_instrlst:
            workshts[v] = [
             sheet + v.title(), True]
        else:
            workshts[v] = [
             '', False]

    return workshts


def _open_workbook_worksheets(valid_instrlst, valid_string_dict, workshts_seq, xlsfile, sheet, overwritesheet, show):
    workshts = _get_worksheet_names_status(valid_instrlst, valid_string_dict, sheet)
    xlsobj = None
    xlsfnam = ''
    for each in workshts_seq:
        if each not in valid_instrlst:
            continue
        k = valid_string_dict[each]
        shtnam = workshts[k][0]
        shtsts = workshts[k][1]
        if shtsts:
            if not xlsobj:
                xlsobj = excelpy.workbook(xlsfile, shtnam, overwritesheet=overwritesheet)
                if show:
                    xlsobj.show()
                else:
                    xlsobj.hide()
                xlsobj.show_alerts(0)
                xlsfnam = xlsobj.XLSFNAM
            else:
                xlsobj.worksheet_add_end(shtnam, overwritesheet=overwritesheet)
            xlsobj.page_format(orientation='landscape', left=1.0, right=1.0, top=0.5, bottom=0.5, header=0.25, footer=0.25)
            xlsobj.page_footer(left='page number of page total', right='date, time')
            xlsobj.page_header(center='file name:sheet name')
            xlsobj.font_sheet()

    if not xlsobj:
        print 'Excel file and worksheets not created.\n'
    return (xlsobj, workshts, xlsfnam)


def _save_and_close(xlsobj, xlsfile, msgstr, msgtype, show=True):
    """
    Various messages are generated based on their type.
    msgtype=1
        Done .... msgstr results saved to file xlsfile.
    """
    xlsfile = xlsobj.save()
    if not show:
        xlsobj.close()
    if msgtype == 1:
        msgstr = '\n Done ...%(msgstr)s saved to file %(xlsfile)s.' % vars()
    print msgstr


def _validate_contingency_labels(colabel, valid_colabel):
    inlbl = colabel
    valid_lbl = []
    invalid_lbl = []
    if colabel:
        if isinstance(colabel, str):
            colabel = [
             colabel]
        for each in colabel:
            e = each.strip().upper()
            if e in valid_colabel:
                valid_lbl.append(e)
            else:
                invalid_lbl.append(each)

    else:
        valid_lbl = valid_colabel
    if invalid_lbl:
        print "'colabel' input:"
        print '    ', inlbl
        print 'Invalid contingency Labels, ignored:'
        print '    ', invalid_lbl
        print 'Valid contingency Labels:'
        print '    ', valid_colabel
        print ''
    if 'BASE CASE' in valid_lbl:
        if valid_lbl[0] != 'BASE CASE':
            jnk = valid_lbl.pop(valid_lbl.index('BASE CASE'))
            valid_lbl.insert(0, 'BASE CASE')
    else:
        valid_lbl.insert(0, 'BASE CASE')
    return valid_lbl


def _validate_string_list(instrlst, valid_string_dict):
    validlst = []
    invalidlst = []
    valid_string = valid_string_dict.keys()
    if isinstance(instrlst, list) or isinstance(instrlst, tuple):
        for each in instrlst:
            if each and isinstance(each, str):
                e = each[0].lower()
                if e in valid_string:
                    validlst.append(e)
                else:
                    invalidlst.append(each)

    elif instrlst and isinstance(instrlst, str):
        e = instrlst[0].lower()
        if e in valid_string:
            validlst.append(e)
        else:
            invalidlst.append(instrlst)
    valid_instrlst = []
    for each in valid_string:
        if each in validlst:
            valid_instrlst.append(each)

    if invalidlst or not validlst:
        print '"string" input: ',
        if not instrlst:
            print 'not provided.'
        else:
            print instrlst
        if invalidlst:
            print 'Invalid string input, ignored: ',
            print invalidlst
        print 'Valid string input: ',
        print valid_string
    return valid_instrlst


def _validate_string_list_contingency(instrlst, valid_string_dict, colabel):
    valid_instrlst = _validate_string_list(instrlst, valid_string_dict)
    if not colabel:
        if 's' in valid_instrlst:
            valid_instrlst = [
             's']
        else:
            valid_instrlst = []
    return valid_instrlst


def _worksheet_size_violation_error(xlsobj, topRow, leftCol, data=None, transpose=False, lblmsg=None, txtmsg=None):
    row_violation, col_violation, topRow, leftCol, bottomRow, rightCol, maxrows, maxcols = xlsobj.worksheet_size_violation(topRow, leftCol, data, transpose)
    if row_violation:
        print 'Allowed maximum number of rows in Excel worksheet: %(maxrows)d, Rows required: %(topRow)d to %(bottomRow)d.' % vars()
    if col_violation:
        print 'Allowed maximum number of columns in Excel worksheet: %(maxcols)d, Columns required: %(leftCol)d to %(leftCol)d.' % vars()
    disable_wsht = row_violation or col_violation
    if lblmsg and disable_wsht:
        shtnam = lblmsg[0].title()
        lbl = lblmsg[1]
        print "'%(shtnam)s' results for contingencies '%(lbl)s' and later are not exported.\n" % vars()
    if txtmsg and disable_wsht:
        txt = txtmsg.title()
        print "'%(txt)s' results exported partly or none.\n"
    return disable_wsht


def _accc_summary(xlsobj, sheet, smry):
    """
    Use this to create ->
    ACCC worksheet: 'Summary'
    """
    xlsobj.set_active_sheet(sheet)
    row, col = (1, 1)
    xlsobj.set_cell((row, col), 'ACCC SOLUTION SUMMARY', fontStyle='bold', fontSize=14, fontColor='blue')
    tmplst = [
     smry.casetitle.line1,
     smry.casetitle.line2,
     'ACCC output file                      = %s' % smry.file.acc,
     'Saved Case file                       = %s' % smry.file.sav,
     'DFAX file                             = %s' % smry.file.dfx,
     'Subsystem file                        = %s' % smry.file.sub,
     'Monitored Element file                = %s' % smry.file.mon,
     'Contingency Description file          = %s' % smry.file.con,
     ' ',
     'Number of Monitored Branches             = %d' % smry.acccsize.nmline,
     'Number of Monitored Interfaces           = %d' % smry.acccsize.ninter,
     'Number of Contingencies+Base Case        = %d' % smry.acccsize.ncase,
     'Number of Voltage Monitored Buses        = %d' % smry.acccsize.nmvbus,
     'Number of Voltage Monitored Records      = %d' % smry.acccsize.nmvrec,
     'Number of Voltage Monitored Bus Records  = %d' % smry.acccsize.nmvbusrec]
    if smry.acccsize.nbus:
        txt = 'Number of Buses in the case                               = %d' % smry.acccsize.nbus
        tmplst.append(txt)
    if smry.acccsize.ncntlshed:
        txt = 'Number of Loads shed due to post contingency              = %d' % smry.acccsize.ncntlshed
        tmplst.append(txt)
    if smry.acccsize.ntrplshed:
        txt = 'Number of Loads shed due to tripping                      = %d' % smry.acccsize.ntrplshed
        tmplst.append(txt)
    if smry.acccsize.ncactlshed:
        txt = 'Number of Loads shed due to corrective actions            = %d' % smry.acccsize.ncactlshed
        tmplst.append(txt)
    if smry.acccsize.ncactgdisp:
        txt = 'Number of Generations dispached due to corrective actions = %d' % smry.acccsize.ncactgdisp
        tmplst.append(txt)
    if smry.acccsize.ncactphsftr:
        txt = 'Number of Phase Shifters changed due to corrective actions= %d' % smry.acccsize.ncactphsftr
        tmplst.append(txt)
    thr = 0
    if smry.file.thr:
        tmplst.insert(8, 'Load throwover file                   = %s' % smry.file.thr)
        thr = thr + 1
    if smry.file.inl:
        tmplst.insert(8 + thr, 'Inertial load file                    = %s' % smry.file.inl)
        thr = thr + 1
    if smry.file.trp:
        tmplst.insert(8 + thr, 'Trip data file                        = %s' % smry.file.trp)
        thr = thr + 1
    row += 2
    bottomRow, rightCol = xlsobj.set_range(row, col, tmplst, transpose=True)
    xlsobj.font_color((row, col, row + 1, col), 'brown')
    disable_wsht_smr = False
    if smry.acccsize.nmline + smry.acccsize.ninter:
        if smry.acccsize.nmline and smry.acccsize.ninter:
            txt = 'Monitored Lines and Interfaces'
        elif smry.acccsize.nmline:
            txt = 'Monitored Lines'
        elif smry.acccsize.ninter:
            txt = 'Monitored Interfaces'
        row = bottomRow + 2
        xlsobj.set_cell((row, col), txt, fontStyle='Bold', fontSize=12, fontColor='red')
        tmplst = [['MON#', 'LABEL', 'RATE A', 'RATE B', 'RATE C']]
        for i in range(smry.acccsize.nmline + smry.acccsize.ninter):
            tmplst.append([i + 1, smry.melement[i], smry.rating.a[i], smry.rating.b[i], smry.rating.c[i]])

        row += 1
        disable_wsht_smr = _worksheet_size_violation_error(xlsobj, row, col, tmplst, txtmsg='summary')
        if not disable_wsht_smr:
            bottomRow, rightCol = xlsobj.set_range(row, col, tmplst)
            xlsobj.font_color((row, col, row, rightCol), 'blue')
    if smry.acccsize.nmvbusrec and not disable_wsht_smr:
        row = bottomRow + 2
        xlsobj.set_cell((row, col), 'Monitored Buses', fontStyle='Bold', fontSize=12, fontColor='red')
        tmplst = [['MON#', 'BUS', 'RECORD', 'TYPE', 'MIN/DROP', 'MAX/RISE']]
        for i in range(smry.acccsize.nmvbusrec):
            if smry.mvrecmin[i] == 0:
                mvrecmin = ''
            else:
                mvrecmin = smry.mvrecmin[i]
            if smry.mvrectype[i] == 'RANGE':
                if smry.mvrecmax[i] == 0 or smry.mvrecmax[i] <= smry.mvrecmin[i]:
                    mvrecmax = ''
                else:
                    mvrecmax = smry.mvrecmax[i]
            else:
                mvrecmax = smry.mvrecmax[i]
            tmplst.append([i + 1, smry.mvbuslabel[i], smry.mvreclabel[i], smry.mvrectype[i], mvrecmin, mvrecmax])

        row += 1
        disable_wsht_smr = _worksheet_size_violation_error(xlsobj, row, col, tmplst, txtmsg='summary')
        if not disable_wsht_smr:
            bottomRow, rightCol = xlsobj.set_range(row, col, tmplst)
            xlsobj.font_color((row, col, row, rightCol), 'blue')
            xlsobj.font((row + 1, rightCol - 1, bottomRow, rightCol), numberFormat='0.00')
    if smry.acccsize.ncase and not disable_wsht_smr:
        row = bottomRow + 2
        nlbls_in_row = 7
        tmplst = [['ACCC Contingency Labels'],
         [
          "Note 1: Contingency labels appended with '+T'  have 'Tripping' solutions."],
         [
          "Note 2: Contingency labels appended with '+CA' have 'Corrective Action' solutions."]]
        lst1 = ''
        j = 0
        for i in range(smry.acccsize.ncase):
            lbl = smry.colabel[i]
            if smry.addtrp[i] != 0:
                lbl += '+T'
            if smry.addcor[i] != 0:
                lbl += '+CA'
            if j == 0:
                lst1 = lbl
            elif j == nlbls_in_row:
                j = 0
                tmplst.append([lst1 + ','])
                lst1 = lbl
            else:
                lst1 += ', ' + lbl
            j = j + 1

        tmplst.append([lst1])
        disable_wsht_smr = _worksheet_size_violation_error(xlsobj, row, col, tmplst, txtmsg='summary')
        if not disable_wsht_smr:
            bottomRow, rightCol = xlsobj.set_range(row, col, tmplst)
            xlsobj.font((row, col), fontStyle='Bold', fontSize=12, fontColor='red')
            xlsobj.font_color((row + 1, col, row + 2, col), 'blue')
    else:
        xlsobj.set_cell((row, col), 'No Contingencies..', fontStyle='Bold', fontSize=12, fontColor='red')
    xlsobj.autofit_columns((1, 2, 1, 6))


def _accc_co_events(xlsobj, sheet, lbl, row, solnvalue):
    """
    Use this to create ->
    ACCC worksheet: 'Contingency Events'
    """
    cnvflag = solnvalue.cnvflag
    cnvcond = solnvalue.cnvcond
    island = solnvalue.island
    mvaworst = solnvalue.mvaworst
    mvatotal = solnvalue.mvatotal
    tmplst = []
    for jj in range(len(solnvalue.codesc)):
        desc = solnvalue.codesc[jj]
        if jj == 0:
            tmplst.append([lbl, desc, cnvflag, cnvcond, island, mvaworst, mvatotal])
        else:
            tmplst.append(['', desc, '', '', '', '', ''])

    xlsobj.set_active_sheet(sheet)
    col = 1
    disable_wsht = _worksheet_size_violation_error(xlsobj, row, col, tmplst, lblmsg=(sheet, lbl))
    if not disable_wsht:
        bottomRow, rightCol = xlsobj.set_range(row, col, tmplst)
        row = bottomRow + 2
    return (disable_wsht, row)


def _accc_solution_worksheets_column_labels(xlsobj, sheet, column_labels):
    """
    Use this to write column labels ->
    ACCC worksheet: all solution worksheets
    """
    row = 1
    col = 1
    xlsobj.set_active_sheet(sheet)
    bottomRow, rightCol = xlsobj.set_range(row, col, column_labels)
    xlsobj.font_color((row, col, row, rightCol), 'red')
    row = bottomRow + 1
    return row


def _accc_solution_worksheets(xlsobj, sheet, lbl, row, color, solnlst):
    """
    Use this to create ->
    ACCC worksheet: all solution worksheets
    """
    col = 1
    xlsobj.set_active_sheet(sheet)
    disable_wsht = _worksheet_size_violation_error(xlsobj, row, col, solnlst, lblmsg=(sheet, lbl))
    if not disable_wsht:
        bottomRow, rightCol = xlsobj.set_range(row, col, solnlst, fontColor=color)
        row = bottomRow + 2
    return (disable_wsht, row)


def _accc_solution_worksheets_format(xlsobj, sheet, bottomRow, leftCol, namcols, numfmt, frzcell):
    """
    Use this to format ->
    ACCC worksheet: all solution worksheets
    """
    xlsobj.set_active_sheet(sheet)
    last_row = bottomRow - 2
    if last_row < 2:
        last_row = 2
    xlsobj.align_rows((1, 1), alignv='h_center')
    if namcols > 1:
        xlsobj.merge((1, 1, 1, namcols))
    for each in numfmt:
        xlsobj.font(each[0], numberFormat=each[1])

    xlsobj.worksheet_top_rows2repeat((1, 1))
    if last_row == 2:
        col = 2
    else:
        col = 1
    xlsobj.autofit_columns((1, col, 1, leftCol))
    xlsobj.freezepanes(frzcell)


def _pv_summary(xlsobj, sheet, smry):
    """
    Use this to create ->
    PV worksheet: 'Summary'
    """
    xlsobj.set_active_sheet(sheet)
    row, col = (1, 1)
    xlsobj.set_cell((row, col), 'PV SOLUTION RESULTS', fontStyle='bold', fontSize=14, fontColor='blue')
    tmplst = [
     smry.casetitle.line1,
     smry.casetitle.line2,
     'PV output file                        = %s' % smry.file.pv,
     'Saved Case file                       = %s' % smry.file.sav]
    if smry.file.ecd:
        tmplst.append('Economic dispatch file                = %s' % smry.file.ecd)
    if smry.file.thr:
        tmplst.append('Load throwover file                   = %s' % smry.file.thr)
    tlst = [
     'DFAX file                             = %s' % smry.file.dfx,
     'Subsystem file                        = %s' % smry.file.sub,
     'Monitored Element file                = %s' % smry.file.mon,
     'Contingency Description file          = %s' % smry.file.con]
    tmplst.extend(tlst)
    if smry.file.inl:
        tmplst.append('Inertia and Governor Response file    = %s' % smry.file.inl)
    if smry.file.zip:
        tmplst.append('Incremental Save Case Archive file    = %s' % smry.file.zip)
    tlst = [
     ' ',
     'Study    (source) system              = %s' % smry.srcsink[0],
     'Opposing (sink)   system              = %s' % smry.srcsink[1],
     ' ',
     'Number of Contingencies+Base Case     = %d' % smry.pvsize.ncase,
     'Number of Monitored Branches          = %d' % smry.pvsize.nmline,
     'Number of Monitored Interfaces        = %d' % smry.pvsize.ninter,
     'Number of Monitored Generators(Plants)= %d' % smry.pvsize.nmgnbus,
     'Number of Monitored Loads             = %d' % smry.pvsize.nmldbus,
     'Number of Voltage Monitored Buses     = %d' % smry.pvsize.nmvbus,
     'Number of Voltage Monitored Records   = %d' % smry.pvsize.nmvrec]
    tmplst.extend(tlst)
    row_optn_ttl = len(tmplst) + 2 + 2
    jnklst = [' ', 'PV Solution Options:']
    for i in range(len(smry.options)):
        if smry.pvsize.vernum == 0 and i >= 16:
            break
        j = smry.options[i]
        ti = str(i + 1).rjust(2)
        tj = str(j)
        t1 = pssarrays._PV_INT_OPTIONS_NAMES[i]
        try:
            t2 = pssarrays._PV_INT_OPTIONS_LIST[i][j]
        except:
            t2 = 'value undefined at i=%d, j=%d' % (i + 1, j + 1)

        jnklst.append('option(%(ti)s): %(t1)s =%(tj)s =%(t2)s' % vars())

    tmplst.extend(jnklst)
    row_vals_ttl = len(tmplst) + 2 + 2
    jnklst = [
     ' ', 'PV Solution Values:']
    for i in range(len(smry.values)):
        ti = str(i + 1)
        tn = pssarrays._PV_REAL_VALUES_NAMES[i]
        tv = '%g' % smry.values[i]
        jnklst.append('value(%(ti)s): %(tn)s =%(tv)s' % vars())

    tmplst.extend(jnklst)
    del jnklst
    row += 2
    bottomRow, rightCol = xlsobj.set_range(row, col, tmplst, transpose=True)
    xlsobj.font_color((row, col, row + 1, col), 'brown')
    xlsobj.font_color((row_optn_ttl, col), 'red')
    xlsobj.font_color((row_vals_ttl, col), 'red')
    if smry.pvsize.ncase:
        row = bottomRow + 2
        xlsobj.set_cell((row, col), 'PV Contingencies', fontStyle='Bold', fontSize=12, fontColor='red')
        conlst = [
         [
          'CON#', 'LABEL', 'Max MW', 'DESCRIPTION']]
        rfrm = row + 1
        rto = row + 1
        failrows = []
        for i in range(smry.pvsize.ncase):
            rfrm += 1
            rto += 1
            if i == 0:
                srnum = ' '
            else:
                srnum = str(i)
            nam = smry.colabel[i]
            mxmw = smry.maxmw[i]
            for j in range(len(smry.codesc[i])):
                dsc = smry.codesc[i][j]
                if j == 0:
                    conlst.append([srnum, nam, mxmw, dsc])
                else:
                    conlst.append(['', '', '', dsc])
                    rto += 1

            if mxmw == 0:
                failrows.append([rfrm, rto])
            else:
                failrows.append([0, 0])
            rfrm = rto

        row += 1
        disable_wsht_smr = _worksheet_size_violation_error(xlsobj, row, col, conlst, txtmsg='summary')
        if not disable_wsht_smr:
            bottomRow, rightCol = xlsobj.set_range(row, col, conlst)
            xlsobj.font_color((row, col, row, rightCol), 'dgreen')
            xlsobj.autofit_columns((row, col + 1))
            xlsobj.align((row, col), 'right')
            xlsobj.font((row, col, row, rightCol), fontStyle=('Bold', ))
            for each in failrows:
                r1 = each[0]
                r2 = each[1]
                if r1 and r2:
                    xlsobj.font((r1, col, r2, rightCol), fontColor='cyan', fontStyle='bold')

    else:
        xlsobj.set_cell((row, col), 'No Contingencies..', fontStyle='Bold', fontSize=12, fontColor='red')
    xlsobj.autofit_columns((1, 2, 1, 4))


def _qv_summary(xlsobj, sheet, smry):
    """
    Use this to create ->
    QV worksheet: 'Summary'
    """
    xlsobj.set_active_sheet(sheet)
    row, col = (1, 1)
    xlsobj.set_cell((row, col), 'QV SOLUTION RESULTS', fontStyle='bold', fontSize=14, fontColor='blue')
    tmplst = [
     smry.casetitle.line1,
     smry.casetitle.line2,
     'QV output file                             = %s' % smry.file.qv,
     'Saved Case file                            = %s' % smry.file.sav]
    if smry.file.thr:
        tmplst.append('Load throwover file                        = %s' % smry.file.thr)
    tlst = [
     'DFAX file                                  = %s' % smry.file.dfx,
     'Subsystem file                             = %s' % smry.file.sub,
     'Monitored Element file                     = %s' % smry.file.mon,
     'Contingency Description file               = %s' % smry.file.con]
    tmplst.extend(tlst)
    if smry.file.inl:
        tmplst.append('Inertia and Governor Response file         = %s' % smry.file.inl)
    if smry.file.zip:
        tmplst.append('Incremental Save Case Archive file         = %s' % smry.file.zip)
    tlst = [
     ' ',
     'Number of Contingencies+Base Case          = %d' % smry.qvsize.ncase,
     'Number of Monitored Generators(Plants)     = %d' % smry.qvsize.nmgnbus,
     'Number of Voltage Monitored Buses          = %d' % smry.qvsize.nmvbus,
     'Number of Voltage Monitored Records        = %d' % smry.qvsize.nmvrec,
     'Number of maximum voltage setpoint changes = %d' % smry.qvsize.nmxvstp]
    tmplst.extend(tlst)
    row_optn_ttl = len(tmplst) + 2 + 2
    jnklst = [' ', 'QV Solution Options:']
    for i in range(len(smry.options)):
        j = smry.options[i]
        ti = str(i + 1).rjust(2)
        tj = str(j)
        t1 = pssarrays._QV_INT_OPTIONS_NAMES[i]
        if i + 1 == pssarrays._QV_INT_OPTIONS_STUDY_BUS_INDEX:
            jnklst.append('option(%(ti)s): %(t1)s =%(tj)s' % vars())
        else:
            t2 = pssarrays._QV_INT_OPTIONS_LIST[i][j]
            jnklst.append('option(%(ti)s): %(t1)s =%(tj)s =%(t2)s' % vars())

    tmplst.extend(jnklst)
    row_vals_ttl = len(tmplst) + 2 + 2
    jnklst = [
     ' ', 'QV Solution Values:']
    for i in range(len(smry.values)):
        ti = str(i + 1)
        tn = pssarrays._QV_REAL_VALUES_NAMES[i]
        tv = '%g' % smry.values[i]
        jnklst.append('value(%(ti)s): %(tn)s =%(tv)s' % vars())

    tmplst.extend(jnklst)
    del jnklst
    row += 2
    bottomRow, rightCol = xlsobj.set_range(row, col, tmplst, transpose=True)
    xlsobj.font_color((row, col, row + 1, col), 'brown')
    xlsobj.font_color((row_optn_ttl, col), 'red')
    xlsobj.font_color((row_vals_ttl, col), 'red')
    if smry.qvsize.ncase:
        row = bottomRow + 2
        xlsobj.set_cell((row, col), 'QV Contingencies', fontStyle='Bold', fontSize=12, fontColor='red')
        conlst = [
         [
          'CON#', 'LABEL', 'Min Vstp', 'Max Vstp', 'Min MVAR', 
          'Max MVAR', 
          'Max Mismatch', 'DESCRIPTION']]
        rfrm = row + 1
        rto = row + 1
        failrows = []
        for i in range(smry.qvsize.ncase):
            rfrm += 1
            rto += 1
            if i == 0:
                srnum = ' '
            else:
                srnum = str(i)
            nam = smry.colabel[i]
            minvstp = smry.minvstp[i]
            maxvstp = smry.maxvstp[i]
            minmvar = smry.minmvar[i]
            maxmvar = smry.maxmvar[i]
            maxmsm = smry.maxmsm[i]
            for j in range(len(smry.codesc[i])):
                dsc = smry.codesc[i][j]
                if j == 0:
                    conlst.append([srnum, nam, minvstp, maxvstp, minmvar, maxmvar, maxmsm, 
                     dsc])
                else:
                    conlst.append(['', '', '', '', '', '', '', dsc])
                    rto += 1

            if maxmsm > smry.values[0]:
                failrows.append([rfrm, rto])
            else:
                failrows.append([0, 0])
            rfrm = rto

        row += 1
        disable_wsht_smr = _worksheet_size_violation_error(xlsobj, row, col, conlst, txtmsg='summary')
        if not disable_wsht_smr:
            bottomRow, rightCol = xlsobj.set_range(row, col, conlst)
            xlsobj.font_color((row, col, row, rightCol), 'dgreen')
            xlsobj.font((row, col + 2, bottomRow, col + 3), numberFormat='0.00')
            xlsobj.font((row, col + 4, bottomRow, col + 6), numberFormat='0.000')
            xlsobj.align((row, col), 'right')
            xlsobj.font((row, col, row, rightCol), fontStyle=('Bold', ))
            xlsobj.autofit_columns((row, col + 1, row, rightCol))
            for each in failrows:
                r1 = each[0]
                r2 = each[1]
                if r1 and r2:
                    xlsobj.font((r1, col, r2, rightCol), fontColor='cyan', fontStyle='bold')

    else:
        xlsobj.set_cell((row, col), 'No Contingencies..', fontStyle='Bold', fontSize=12, fontColor='red')


def _pvqv_m(xlsobj, sheet, lbl, ttl, row, rowttl, mwtransfer, mvaworst, mvatotal, cnvflag, cnvcond):
    """
    Use this to create ->
    PV worksheet: 'Mismatch'
    QV worksheet: 'Mismatch'
    """
    contitle = 'CONTINGENCY: ' + lbl.strip() + '     ' + ttl
    cnvyesno = []
    noclns = []
    i = 1
    for each in cnvflag:
        i += 1
        if each:
            cnvyesno.append('YES')
            noclns.append(0)
        else:
            cnvyesno.append('NO')
            noclns.append(i)

    tmplst = [
     rowttl]
    for i in range(len(mwtransfer)):
        tmplst.append([mwtransfer[i], mvaworst[i], mvatotal[i], cnvyesno[i], cnvcond[i]])

    xlsobj.set_active_sheet(sheet)
    col = 1
    disable_wsht = _worksheet_size_violation_error(xlsobj, row + 1, col, tmplst, transpose=True, lblmsg=(sheet, lbl))
    if not disable_wsht:
        xlsobj.set_cell((row, col + 1), contitle, fontStyle='bold', fontSize=12, fontColor='dgreen')
        row += 1
        bottomRow, rightCol = xlsobj.set_range(row, col, tmplst, transpose=True, numberFormat='0.00000')
        xlsobj.font((row, col, row, rightCol), fontColor='red', fontStyle='bold', numberFormat='0.000')
        xlsobj.align((row, col, row, rightCol), 'h_center')
        xlsobj.align((row + 3, col, row + 3, rightCol), 'h_center')
        xlsobj.align((row, col, bottomRow, col), 'right')
        xlsobj.font((row + 1, col, bottomRow, col), fontColor='blue', fontStyle='bold')
        for each in noclns:
            if each:
                xlsobj.font((row + 3, each, bottomRow, each), fontColor='cyan', fontStyle='bold')

        row = bottomRow + 2
    return (disable_wsht, row)


def _pvqv_one(xlsobj, sheet, lbl, ttl, row, rowttl, mwtransfer, solnvalue, options, cnvflag=[]):
    """
    Use this to create ->
    PV worksheets: 'Bus Voltage', 'Branch Flow', 'Interface Flow'
    QV worksheets: 'Bus Voltage', 'Generator Dispatch'
    """
    contitle = 'CONTINGENCY: ' + lbl.strip() + '     ' + ttl
    namesplit = options[0]
    nttlclns = options[1]
    transpose = options[2]
    noclns = []
    i = nttlclns
    for each in cnvflag:
        i += 1
        if each:
            noclns.append(0)
        else:
            noclns.append(i)

    t = []
    for i in range(len(mwtransfer)):
        t1 = list(solnvalue[i])
        t1.insert(0, mwtransfer[i])
        t.append(t1)

    if namesplit:
        nrows, nclns, tmplst = xlsobj.transpose_data(t)
        for i in range(nrows):
            for j in range(len(rowttl[0])):
                tmplst[i].insert(j, rowttl[i][j])

    else:
        tmplst = t
        tmplst.insert(0, rowttl)
    xlsobj.set_active_sheet(sheet)
    col = 1
    disable_wsht = _worksheet_size_violation_error(xlsobj, row + 1, col, tmplst, transpose=transpose, lblmsg=(sheet, lbl))
    if not disable_wsht:
        xlsobj.set_cell((row, col + nttlclns), contitle, fontStyle='bold', fontSize=12, fontColor='dgreen')
        row += 1
        bottomRow, rightCol = xlsobj.set_range(row, col, tmplst, transpose=transpose)
        xlsobj.font((row, col + nttlclns - 1, row, rightCol), fontColor='red', fontStyle='bold')
        xlsobj.font((row, col + nttlclns, bottomRow, rightCol), numberFormat='0.000')
        xlsobj.align((row, col, row, rightCol), 'h_center')
        if namesplit:
            xlsobj.merge((row, col, row, nttlclns))
        xlsobj.align((row, col), 'right')
        xlsobj.font((row + 1, col, bottomRow, nttlclns), fontColor='blue', fontStyle='bold')
        for each in noclns:
            if each:
                xlsobj.font((row + 1, each, bottomRow, each), fontColor='cyan')

        row = bottomRow + 2
    return (disable_wsht, row)


def _pv_two(xlsobj, sheet, lbl, ttl, row, rowttl, mwtransfer, mw, mvar, options, cnvflag=[]):
    """
    Use this to create ->
    PV worksheets: 'Generator Dispatch', 'Bus Load'
    """
    contitle = 'CONTINGENCY: ' + lbl.strip() + '     ' + ttl
    namesplit = options[0]
    nttlclns = options[1]
    transpose = options[2]
    noclns = []
    i = nttlclns
    for each in cnvflag:
        i += 1
        if each:
            noclns.append(0)
        else:
            noclns.append(i)

    t = []
    for i in range(len(mwtransfer)):
        t1 = list(mw[i])
        t1.insert(0, mwtransfer[i])
        t1.insert(1, 'MW')
        t.append(t1)
        t1 = list(mvar[i])
        t1.insert(0, '')
        t1.insert(1, 'MVAR')
        t.append(t1)

    if namesplit:
        nrows, nclns, tmplst = xlsobj.transpose_data(t)
        for i in range(nrows):
            for j in range(len(rowttl[0])):
                tmplst[i].insert(j, rowttl[i][j])

    else:
        tmplst = t
        tmplst.insert(0, list(rowttl))
    xlsobj.set_active_sheet(sheet)
    col = 1
    disable_wsht = _worksheet_size_violation_error(xlsobj, row + 1, col, tmplst, transpose=transpose, lblmsg=(sheet, lbl))
    if disable_wsht:
        xlsobj['generator dispatch'][1] = False
    else:
        xlsobj.set_cell((row, col + +nttlclns), contitle, fontStyle='bold', fontSize=12, fontColor='dgreen')
        row += 1
        bottomRow, rightCol = xlsobj.set_range(row, col, tmplst, transpose=transpose)
        xlsobj.font((row, col + nttlclns - 1, row, rightCol), fontColor='red', fontStyle='bold')
        if namesplit:
            xlsobj.merge((row, col, row, nttlclns))
        xlsobj.align((row, col), 'right')
        xlsobj.font((row, col + nttlclns, bottomRow, rightCol), numberFormat='0.000')
        xlsobj.font((row + 1, col, bottomRow, nttlclns), fontColor='blue', fontStyle='bold')
        for i in range(nttlclns + 1, rightCol, 2):
            xlsobj.merge((row, i, row, i + 1))

        xlsobj.align((row, nttlclns + 1, row + 1, rightCol), 'h_center')
        xlsobj.font((row + 1, nttlclns + 1, row + 1, rightCol), fontColor='magenta')
        for each in noclns:
            if each:
                xlsobj.font((row + 2, each, bottomRow, each + 1), fontColor='cyan')

        row = bottomRow + 2
    return (disable_wsht, row)


def accc(accfile='', string='', colabel='', stype='contingency', busmsm=0.5, sysmsm=5.0, rating='a', namesplit=True, xlsfile='', sheet='', overwritesheet=True, show=True, ratecon='b', baseflowvio=True, basevoltvio=True, flowlimit=100.0, flowchange=0.0, voltchange=0.0, islandbuses=True):
    """Export ACCC analysis results to Excel Spreadsheet.
    Returns
        Excel file name (its extension will depend on Excel version installed.)
    Inputs
    accfile     : ACCC analysis output file name (.acc), no default allowed
    string      : Name or list of names or  indicating which results to export, no default allowed
                  's' or 'summary'        - ACCC analysis Summary
                  'e' or 'events'         - Contingency Events Description
                  'b' or 'branch'         - Monitored Branch Flow (MVA)
                  'i' or 'interface'      - Monitored Interface Flow (MW)
                  'v' or 'voltage'        - Monitored Bus Voltage
                  'l' or 'load'           - Loads Shed MW
                  'g' or 'generator'      - Generator Dispatch MW, Corrective Action
                  'p' or 'phase shifter'  - Phase Shifter Angle, Corrective Action
                  Example: string='v' or string=['s','m','v','g','l','b','i']
    colabel     : Contingency label or list of contingency labels whose solution is exported,
                  default - all contingencies
    stype       : solution type
                  default "contingency"
                  allowed values are: "contingency", "con", "tripping", "trp",
                  "caction", "contingency action" or "cor"
    busmsm      : Bus mismatch tolerance
                  default 0.5 MVA
    sysmsm      : System mismatch tolerance
                  default 5.0 MVA
    rating      : Rating to use to calculate Base Case percentage overload
                  default 'a', allowed values:'a', 'b', or 'c'
    namesplit   : Split extended bus names
                  default True
                  = True,  bus names split into three values: number, name and bus voltage
                  = False, bus names are kept as single value string
    ratecon     : Rating to use to calculate Contingency Case percentage overload
                  default 'b', allowed values:'a', 'b', or 'c'
    baseflowvio : Exclude elements with base case loading violations from contingency reports
                  default True, allowed values: True or False
    basevoltvio : Exclude buses with base case voltage range violations from contingency reports
                  default True, allowed values: True or False
    flowlimit   : Percent of flow rating, default=100 for 100%
                  Show monitored elements with flow above flowlimit value.
                  flowlimit=0 will export flows for all elements.
    flowchange  : Minimum contingency case flow change in MVA for overload reports
                  default 0.0 MVA, allowed values: Any number
                  When flowchange=0.0, this filter criteria is ignored.
                  Specify non-zero positive value to consider this filter criteria.
    voltchange  : Minimum contingency case voltage change in pu for voltage range violations
                  default 0.0 pu, allowed values: Any number
                  When voltchange=0.0, this filter criteria is ignored.
                  Specify non-zero positive value to consider this filter criteria.
    islandbuses : Exclude buses which get islanded from contingency reports
                  default True, allowed values: True or False
    Outputs
    xlsfile     : Excel workbook name,  default Book#.xlsx or Book#.xls
    sheet       : Excel worksheet name, default ''
                  Depending on "string" input, worksheets created are:
                  Summary             - ACCC Solution Summary
                  Contingency Events  - Contingency Labels, their description and convergence condition
                  Branch Flow         - Monitored Branch Flow (MVA)
                  Interface Flow      - Monitored Interface Flow (MW)
                  Bus Voltage         - Monitored Bus Voltage
                  Load Shed           - Loads Shed MW
                  Generator Dispatch  - Generator Dispatch MW, Corrective Action
                  Phase Shifter Angle - Phase Shifter Angle, Corrective Action
                  All worksheet names are prefixxed with "sheet" name, when provided.
    overwritesheet: Overwrite worksheets flag, default True
                  = True,  existing worksheets are overwritten
                  = False, existing worksheets are copied and their names
                  appended with (#), where # is next sequence number.
    show        : Show or Hide Excel Spreadsheet flag, default True
                  = True,  show Excel Spreadsheet
                  = False, do not show Excel Spreadsheet (it will be just created/opened, saved and closed)
                    When calling in a loop and writing to the same file, you must set show=False.
    """
    if not accfile:
        print 'ACCC output file (.acc) not provided.'
        return ''
    else:
        smry = pssarrays.accc_summary(accfile)
        colabel = _validate_contingency_labels(colabel, smry.colabel)
        valid_instrlst = _validate_string_list_contingency(string, _EXPORT_QTY_ACCC, colabel)
        accxls, accshts, xlsfile = _open_workbook_worksheets(valid_instrlst, _EXPORT_QTY_ACCC, _WORKSHT_SEQ_ACCC, xlsfile, sheet, overwritesheet, show)
        if not accxls:
            return ''
        disable_wsht_smr = False
        if accshts['summary'][1]:
            _accc_summary(accxls, accshts['summary'][0], smry)
        proceed_to_solution = _check_to_procced_to_solution(accshts)
        if not proceed_to_solution:
            _save_and_close(accxls, xlsfile, 'ACCC Solution', msgtype=1, show=show)
            return xlsfile
        ratenam, rate = pssarrays._check_rate(rating, smry.rating)
        ratenamcon, ratecon = pssarrays._check_rate(ratecon, smry.rating)
        getwhat, getwhatname, stype = pssarrays._check_accc_solution_type(stype)
        if accshts['contingency events'][1]:
            evtlabel = [
             'CONTINGENCY', 'EVENTS', 'CONVERGED', 'CONVERGENCE STATE', 
             'ISLANDS', 'MVAWORST', 'MVATOTAL']
            row_evt = _accc_solution_worksheets_column_labels(accxls, accshts['contingency events'][0], evtlabel)
            leftcol_evt = len(evtlabel)
            namcols_evt = 1
        if accshts['branch flow'][1]:
            rate_name = 'RATE ' + ratenam + '/' + ratenamcon
            brnlabel = [['BRANCH']]
            if namesplit:
                brnlabel[0].extend(6 * [''])
                namcols_brn = 7
            else:
                namcols_brn = 1
            brnlabel[0].extend(['CONTINGENCY', 'MVAFLOW', 'AMPFLOW', rate_name, '% FLOW'])
            leftcol_brn = len(brnlabel[0])
            if not smry.acccsize.nmline:
                t2 = [
                 'No monitored branches specified.']
                t2.extend((len(brnlabel[0]) - 1) * [''])
                brnlabel.append(t2)
                accshts['branch flow'][1] = False
            row_brn = _accc_solution_worksheets_column_labels(accxls, accshts['branch flow'][0], brnlabel)
        if accshts['interface flow'][1]:
            rate_name = 'RATE ' + ratenam + '/' + ratenamcon
            itflabel = [['INTERFACE', 'CONTINGENCY', 'MVAFLOW', rate_name, '% FLOW']]
            leftcol_itf = len(itflabel[0])
            namcols_itf = 1
            if not smry.acccsize.ninter:
                itflabel.append(['No monitored interfaces specified.', '', '', '', ''])
                accshts['interface flow'][1] = False
            row_itf = _accc_solution_worksheets_column_labels(accxls, accshts['interface flow'][0], itflabel)
        if accshts['bus voltage'][1]:
            vltlabel = [
             [
              'BUS']]
            if namesplit:
                vltlabel[0].extend(2 * [''])
                namcols_vlt = 3
            else:
                namcols_vlt = 1
            vltlabel[0].extend(['RECORD', 'TYPE', 'MIN/DROP', 'MAX/RISE', 'CONTINGENCY', 'BASE VOLTS', 
             'CONT VOLTS', 'DEVIATION', 'RANGE VIO', 'DEV VIO'])
            leftcol_vlt = len(vltlabel[0])
            if not smry.acccsize.nmvbus:
                t2 = [
                 'No monitored bus voltages specified.']
                t2.extend((len(vltlabel[0]) - 1) * [''])
                vltlabel.append(t2)
                accshts['bus voltage'][1] = False
            row_vlt = _accc_solution_worksheets_column_labels(accxls, accshts['bus voltage'][0], vltlabel)
        if accshts['load shed'][1]:
            lodlabel = [
             [
              'LOAD BUS']]
            if namesplit:
                lodlabel[0].extend(2 * [''])
                namcols_lod = 3
            else:
                namcols_lod = 1
            if getwhat == 1 or getwhat == 2:
                lodlabel[0].extend(['CONTINGENCY', 'LOAD SHED(MW)'])
            else:
                lodlabel[0].extend(['CONTINGENCY', 'INIT LOAD(MW)', 'LOAD SHED(MW)'])
            leftcol_lod = len(lodlabel[0])
            row_lod = _accc_solution_worksheets_column_labels(accxls, accshts['load shed'][0], lodlabel)
        if accshts['generator dispatch'][1]:
            genlabel = [
             [
              'GENERATOR BUS']]
            if namesplit:
                genlabel[0].extend(2 * [''])
                namcols_gen = 3
            else:
                namcols_gen = 1
            genlabel[0].extend(['CONTINGENCY', 'INIT GEN(MW)', 'GEN DISP(MW)'])
            leftcol_gen = len(genlabel[0])
            if getwhat in (1, 2):
                t2 = [
                 'Generator dispatch is available for Corrective Action solution only.']
                t2.extend((len(genlabel[0]) - 1) * [''])
                genlabel.append(t2)
                accshts['generator dispatch'][1] = False
            row_gen = _accc_solution_worksheets_column_labels(accxls, accshts['generator dispatch'][0], genlabel)
        if accshts['phase shifter angle'][1]:
            phslabel = [
             [
              'PHASE SHIFTER BRANCH']]
            if namesplit:
                phslabel[0].extend(6 * [''])
                namcols_phs = 7
            else:
                namcols_phs = 1
            phslabel[0].extend(['CONTINGENCY', 'INIT ANG(MW)', 'NEW ANG(MW)'])
            leftcol_phs = len(phslabel[0])
            if getwhat in (1, 2):
                t2 = [
                 'Phase shifter angle is available for Corrective Action solution only.']
                t2.extend((len(phslabel[0]) - 1) * [''])
                phslabel.append(t2)
                accshts['phase shifter angle'][1] = False
            row_phs = _accc_solution_worksheets_column_labels(accxls, accshts['phase shifter angle'][0], phslabel)
        if namesplit:
            if accshts['branch flow'][1] and smry.acccsize.nmline:
                melement_decode = _decode_branch_list(smry.melement[:smry.acccsize.nmline])
            if accshts['interface flow'][1] and smry.acccsize.ninter:
                minterface_decode = _decode_interface_list(smry.melement[smry.acccsize.nmline:])
            if accshts['bus voltage'][1] and smry.acccsize.nmvbusrec:
                mvbuslabel_decode = _decode_bus_list(smry.mvbuslabel)
        color_now = _alternate_colors()
        ret_ierr = 0
        if accshts['branch flow'][1]:
            base_brn_flows = {}
            base_brn_vio = {}
        if accshts['interface flow'][1]:
            base_itf_flows = {}
            base_itf_vio = {}
        if accshts['branch flow'][1] or accshts['interface flow'][1]:
            if type(flowlimit) == float or type(flowlimit) == int:
                if flowlimit < 0.0:
                    flowlimit = abs(flowlimit)
            else:
                flowlimit = 100.0
            if type(flowchange) == float or type(flowchange) == int:
                if flowchange < 0.0:
                    flowchange = abs(flowchange)
            else:
                flowchange = 0.0
        if accshts['bus voltage'][1]:
            base_bus_volts = {}
            base_bus_vio = {}
            if type(voltchange) == float or type(voltchange) == int:
                if voltchange < 0.0:
                    voltchange = abs(voltchange)
            else:
                voltchange = 0.0
        if accshts['branch flow'][1] or accshts['interface flow'][1] or accshts['bus voltage'][1]:
            if flowchange:
                s_flowchange = 'Minimum contingency case flow change (=contCaseFlow-baseCaseFlow) for overload reports = %g MVA' % flowchange
            else:
                s_flowchange = 'Minimum contingency case flow change = 0.0 MVA, filter criteria ignored'
            if voltchange:
                s_voltchange = 'Minimum contingency case voltage change (=contCaseV-baseCaseV) for violations = %g pu' % voltchange
            else:
                s_voltchange = 'Minimum contingency case voltage change = 0.0 pu, filter criteria ignored'
            tmpoptnlst = [
             'BASE VOLTS is pu base case voltage.',
             'CONT VOLTS is pu contingency case voltage.',
             'DEVIATION is difference between contingency case and base case voltage.',
             'RANGE VIO is range violations calculated as bus voltage - minimum range limit or bus voltage - maximum range limit.',
             'DEV VIO is deviation violations calculated as DEVIATION - minimum deviation limit or DEVIATION - maximum deviation limit.',
             'Report Options Used:',
             'Solution type = %s' % stype,
             'Rating to use to calculate Base Case percentage overload = %s' % ratenam,
             'Rating to use to calculate Contingency Case percentage overload = %s' % ratenamcon,
             'Exclude elements with base case loading violations from contingency reports = %s' % baseflowvio,
             'Exclude buses with base case voltage range violations from contingency reports = %s' % basevoltvio,
             'Percent of flow rating = %g' % flowlimit,
             '%s' % s_flowchange,
             '%s' % s_voltchange,
             'Exclude islanded buses from contingency reports = %s' % islandbuses,
             'Bus mismatch tolerance = %g MVA' % busmsm,
             'System mismatch tolerance = %g MVA' % sysmsm,
             '',
             'Note: RATE column label is Base Case Rating/Contingency case rating.']
            if accshts['branch flow'][1]:
                jnkr, jnkc = accxls.set_range(2, leftcol_brn + 1, tmpoptnlst, transpose=True, sheet=accshts['branch flow'][0])
            if accshts['interface flow'][1]:
                jnkr, jnkc = accxls.set_range(2, leftcol_itf + 1, tmpoptnlst, transpose=True, sheet=accshts['interface flow'][0])
            if accshts['bus voltage'][1]:
                jnkr, jnkc = accxls.set_range(2, leftcol_vlt + 1, tmpoptnlst[:-2], transpose=True, sheet=accshts['bus voltage'][0])
        for lbl in colabel:
            if lbl == 'BASE CASE':
                soln = pssarrays.accc_solution(accfile, lbl, pssarrays._ACCC_SOLUTION_TYPES[0][0], busmsm, sysmsm)
            else:
                soln = pssarrays.accc_solution(accfile, lbl, stype, busmsm, sysmsm)
            if soln == None:
                continue
            if soln.ierr != 0:
                ret_ierr = soln.ierr
            if accshts['contingency events'][1]:
                disable_wsht, row_evt = _accc_co_events(accxls, accshts['contingency events'][0], lbl, row_evt, soln)
                if disable_wsht:
                    accshts['contingency events'][1] = False
            if not soln.cnvflag:
                continue
            if accshts['branch flow'][1]:
                tmplst = []
                for i in range(smry.acccsize.nmline):
                    mvaflow = soln.mvaflow[i]
                    ampflow = soln.ampflow[i]
                    pctflow = abs(ampflow)
                    if lbl == 'BASE CASE':
                        base_brn_flows[smry.melement[i]] = pctflow
                        userate = rate[i]
                    else:
                        userate = ratecon[i]
                    isit_fw_vio = False
                    if userate:
                        rate_val = userate
                        pctflow = pctflow * 100.0 / userate
                        if pctflow > flowlimit:
                            isit_fw_vio = True
                    else:
                        rate_val = ''
                        pctflow = ''
                    if lbl == 'BASE CASE':
                        if isit_fw_vio:
                            base_brn_vio[smry.melement[i]] = 1
                        else:
                            base_brn_vio[smry.melement[i]] = 0
                    if flowlimit and not isit_fw_vio:
                        continue
                    if getwhat == 1:
                        if lbl != 'BASE CASE':
                            if baseflowvio and base_brn_vio[smry.melement[i]] == 1:
                                continue
                            if flowchange:
                                if abs(base_brn_flows[smry.melement[i]] - abs(ampflow)) <= flowchange:
                                    continue
                    t = [
                     lbl, mvaflow, ampflow, 
                     rate_val, pctflow]
                    if namesplit:
                        for j in range(7):
                            t.insert(j, melement_decode[i][j])

                    else:
                        t.insert(0, smry.melement[i])
                    tmplst.append(t)

                if tmplst:
                    disable_wsht, row_brn = _accc_solution_worksheets(accxls, accshts['branch flow'][0], lbl, row_brn, color_now, tmplst)
                    if disable_wsht:
                        accshts['branch flow'][1] = False
            if accshts['interface flow'][1]:
                tmplst = []
                for i in range(smry.acccsize.nmline, smry.acccsize.nmline + smry.acccsize.ninter):
                    mvaflow = soln.mvaflow[i]
                    ampflow = mvaflow
                    pctflow = abs(mvaflow)
                    if lbl == 'BASE CASE':
                        base_itf_flows[smry.melement[i]] = pctflow
                        userate = rate[i]
                    else:
                        userate = ratecon[i]
                    isit_fw_vio = False
                    if userate:
                        rate_val = userate
                        pctflow = pctflow * 100.0 / userate
                        if pctflow > flowlimit:
                            isit_fw_vio = True
                    else:
                        rate_val = ''
                        pctflow = ''
                    if lbl == 'BASE CASE':
                        if isit_fw_vio:
                            base_itf_vio[smry.melement[i]] = 1
                        else:
                            base_itf_vio[smry.melement[i]] = 0
                    if flowlimit and not isit_fw_vio:
                        continue
                    if getwhat == 1:
                        if lbl != 'BASE CASE':
                            if baseflowvio and base_itf_vio[smry.melement[i]] == 1:
                                continue
                            if flowchange:
                                if abs(base_itf_flows[smry.melement[i]] - abs(ampflow)) <= flowchange:
                                    continue
                    t = [
                     lbl, mvaflow, rate_val, pctflow]
                    if namesplit:
                        t.insert(0, minterface_decode[i - smry.acccsize.nmline][0])
                    else:
                        t.insert(0, smry.melement[i])
                    tmplst.append(t)

                if tmplst:
                    disable_wsht, row_itf = _accc_solution_worksheets(accxls, accshts['interface flow'][0], lbl, row_itf, color_now, tmplst)
                    if disable_wsht:
                        accshts['interface flow'][1] = False
            if accshts['bus voltage'][1]:
                tmplst = []
                for i in range(smry.acccsize.nmvbusrec):
                    busvlt = soln.volts[i]
                    if lbl != 'BASE CASE':
                        base_busvlt = base_bus_volts[smry.mvbuslabel[i]]
                    if smry.mvrecmin[i] == 0:
                        mvrecmin = ''
                    else:
                        mvrecmin = smry.mvrecmin[i]
                    if smry.mvrectype[i] == 'RANGE':
                        if smry.mvrecmax[i] == 0 or smry.mvrecmax[i] <= smry.mvrecmin[i]:
                            mvrecmax = ''
                        else:
                            mvrecmax = smry.mvrecmax[i]
                    else:
                        mvrecmax = smry.mvrecmax[i]
                    if lbl == 'BASE CASE':
                        if smry.mvbuslabel[i] not in base_bus_volts.keys():
                            base_bus_volts[smry.mvbuslabel[i]] = busvlt
                    minvio = False
                    maxvio = False
                    vio_rng = ''
                    vio_dev = ''
                    if smry.mvrectype[i] == 'RANGE':
                        if mvrecmin and busvlt < mvrecmin:
                            minvio = True
                            vio_rng = busvlt - mvrecmin
                        if mvrecmax and busvlt > mvrecmax:
                            maxvio = True
                            vio_rng = busvlt - mvrecmax
                    elif lbl != 'BASE CASE':
                        vtdiff = abs(busvlt - base_busvlt)
                        if mvrecmin:
                            if busvlt < base_busvlt:
                                if vtdiff > mvrecmin:
                                    minvio = True
                                    vio_dev = vtdiff - mvrecmin
                        if mvrecmax:
                            if busvlt > base_busvlt:
                                if vtdiff > mvrecmax:
                                    maxvio = True
                                    vio_dev = vtdiff - mvrecmax
                    if minvio or maxvio:
                        isit_vt_vio = True
                    else:
                        isit_vt_vio = False
                    if lbl == 'BASE CASE' and smry.mvrectype[i] == 'RANGE':
                        if isit_vt_vio:
                            base_bus_vio[smry.mvbuslabel[i]] = 1
                        else:
                            base_bus_vio[smry.mvbuslabel[i]] = 0
                    if voltchange:
                        pass
                    elif not isit_vt_vio:
                        continue
                    if getwhat == 1:
                        if lbl != 'BASE CASE' and smry.mvrectype[i] == 'RANGE':
                            if basevoltvio and base_bus_vio[smry.mvbuslabel[i]] == 1:
                                continue
                            if voltchange:
                                if abs(busvlt - base_busvlt) <= voltchange:
                                    continue
                    if islandbuses and abs(busvlt) <= 0.001:
                        continue
                    if lbl == 'BASE CASE':
                        t = [
                         smry.mvreclabel[i], smry.mvrectype[i], mvrecmin, mvrecmax, lbl, busvlt, '', '', vio_rng, vio_dev]
                    else:
                        t = [
                         smry.mvreclabel[i], smry.mvrectype[i], mvrecmin, mvrecmax, lbl, base_busvlt, busvlt, busvlt - base_busvlt, vio_rng, vio_dev]
                    if namesplit:
                        for j in range(3):
                            t.insert(j, mvbuslabel_decode[i][j])

                    else:
                        t.insert(0, smry.mvbuslabel[i])
                    tmplst.append(t)

                if tmplst:
                    disable_wsht, row_vlt = _accc_solution_worksheets(accxls, accshts['bus voltage'][0], lbl, row_vlt, color_now, tmplst)
                    if disable_wsht:
                        accshts['bus voltage'][1] = False
            if accshts['load shed'][1]:
                tmplst = []
                if len(soln.lshedbus):
                    for i in range(len(soln.lshedbus)):
                        if namesplit:
                            t = _decode_bus_string(soln.lshedbus[i])
                        else:
                            t = [
                             soln.loadshed[i]]
                        if getwhat == 1 or getwhat == 2:
                            t.extend([lbl, soln.loadshed[i]])
                        else:
                            t.extend([lbl, soln.loadshed[0][i], soln.loadshed[1][i]])
                        tmplst.append(t)

                else:
                    if namesplit:
                        t = 3 * ['']
                    else:
                        t = [
                         '']
                    if getwhat == 1 or getwhat == 2:
                        t.extend([lbl, '-'])
                    else:
                        t.extend([lbl, '-', '-'])
                    tmplst.append(t)
                disable_wsht, row_lod = _accc_solution_worksheets(accxls, accshts['load shed'][0], lbl, row_lod, color_now, tmplst)
                if disable_wsht:
                    accshts['load shed'][1] = False
            if lbl != 'BASE CASE' and accshts['generator dispatch'][1]:
                tmplst = []
                if len(soln.gdispbus):
                    for i in range(len(soln.gdispbus)):
                        if namesplit:
                            t = _decode_bus_string(soln.gdispbus[i])
                        else:
                            t = [
                             soln.gdispbus[i]]
                        t.extend([lbl, soln.gendisp[0][i], soln.gendisp[1][i]])
                        tmplst.append(t)

                else:
                    if namesplit:
                        t = 3 * ['']
                    else:
                        t = [
                         '']
                    t.extend([lbl, '-', '-'])
                    tmplst.append(t)
                disable_wsht, row_gen = _accc_solution_worksheets(accxls, accshts['generator dispatch'][0], lbl, row_gen, color_now, tmplst)
                if disable_wsht:
                    accshts['generator dispatch'][1] = False
            if lbl != 'BASE CASE' and accshts['phase shifter angle'][1]:
                tmplst = []
                if len(soln.phsftr):
                    for i in range(len(soln.phsftr)):
                        if namesplit:
                            t = _decode_branch_string(soln.phsftr[i])
                        else:
                            t = [
                             soln.phsftr[i]]
                        t.extend([lbl, soln.phsftrang[0][i], soln.phsftrang[1][i]])
                        tmplst.append(t)

                else:
                    if namesplit:
                        t = 7 * ['']
                    else:
                        t = [
                         '']
                    t.extend([lbl, '-', '-'])
                    tmplst.append(t)
                disable_wsht, row_phs = _accc_solution_worksheets(accxls, accshts['phase shifter angle'][0], lbl, row_phs, color_now, tmplst)
                if disable_wsht:
                    accshts['phase shifter angle'][1] = False
            color_now = _alternate_colors(color_now)

        if accshts['contingency events'][0]:
            sht = accshts['contingency events'][0]
            numfmt = [[(2, 6, row_evt, leftcol_evt), '0.0000']]
            frzcell = (2, 2)
            _accc_solution_worksheets_format(accxls, sht, row_evt, leftcol_evt, namcols_evt, numfmt, frzcell)
        if accshts['branch flow'][0]:
            sht = accshts['branch flow'][0]
            numfmt = [[(2, namcols_brn + 2, row_brn, leftcol_brn), '0.00']]
            frzcell = (2, 1)
            _accc_solution_worksheets_format(accxls, sht, row_brn, leftcol_brn, namcols_brn, numfmt, frzcell)
        if accshts['interface flow'][0]:
            sht = accshts['interface flow'][0]
            numfmt = [[(2, namcols_itf + 2, row_itf, leftcol_itf), '0.00']]
            frzcell = (2, 1)
            _accc_solution_worksheets_format(accxls, sht, row_itf, leftcol_itf, namcols_itf, numfmt, frzcell)
        if accshts['bus voltage'][0]:
            sht = accshts['bus voltage'][0]
            numfmt = [[(2, namcols_vlt + 3, row_vlt, namcols_vlt + 4), '0.00'],
             [
              (
               2, namcols_vlt + 6, row_vlt, namcols_vlt + 7), '0.0000']]
            frzcell = (2, 1)
            _accc_solution_worksheets_format(accxls, sht, row_vlt, leftcol_vlt, namcols_vlt, numfmt, frzcell)
        if accshts['load shed'][0]:
            sht = accshts['load shed'][0]
            numfmt = [[(2, namcols_lod + 2, row_lod, leftcol_lod), '0.00']]
            frzcell = (2, 1)
            _accc_solution_worksheets_format(accxls, sht, row_lod, leftcol_lod, namcols_lod, numfmt, frzcell)
        if accshts['generator dispatch'][0]:
            sht = accshts['generator dispatch'][0]
            numfmt = [[(2, namcols_gen + 2, row_gen, leftcol_gen), '0.00']]
            frzcell = (2, 1)
            _accc_solution_worksheets_format(accxls, sht, row_gen, leftcol_gen, namcols_gen, numfmt, frzcell)
        if accshts['phase shifter angle'][0]:
            sht = accshts['phase shifter angle'][0]
            numfmt = [[(2, namcols_phs + 2, row_phs, leftcol_phs), '0.00']]
            frzcell = (2, 1)
            _accc_solution_worksheets_format(accxls, sht, row_phs, leftcol_phs, namcols_phs, numfmt, frzcell)
        _save_and_close(accxls, xlsfile, 'ACCC Solution', msgtype=1, show=show)
        return xlsfile


def iec_data_file(xlsfile='', sheet='', overwritesheet=True, show=True):
    """Export Synchronous and Asynchronous Machines and Transformer Data from PSS(R)E Saved Case
    required to assemble IEC fault data input file to Excel Spreadsheet.
    It creates three worksheets 'Machines', 'Transformers', and 'IEC Data'.

    This file is used as an easy way to create '.iec' file by copy/paste generator and tranformer
    records to form a 'power station units'. Modify generator, motor and transformer data as
    required by "IECS" API. Then copy/paste appropriate records into 'IEC_DATA' worksheet and
    save it as comma separated file with extension '.iec'.

    Note:
    PSS(R)E Saved case must be opened prior to run this function.

    Returns
        Excel file name (its extension will depend on Excel version installed.)
    Outputs
    xlsfile : Excel workbook name,  name of Saved case file with extension '.xls or .xlsx'.
    sheet   : Excel worksheet name, default ''
              Three worksheets are created.
              Machines     - Machines data in PSSE Saved Case
              Transformers - Two and Three windings transformer data in PSSE Saved Case
              IEC Data     - Empty worksheet with IEC data format column headings
              All worksheet names are prefixxed with "sheet" name, when provided.
    overwritesheet: Overwrite worksheets flag, default True
              = True,  existing worksheets are overwritten
              = False, existing worksheets are copied and their names
                appended with (#), where # is next sequence number.
    show    : Show or Hide Excel Spreadsheet flag, default True
              = True,  show Excel Spreadsheet
              = False, do not show Excel Spreadsheet (it will be just created/opened, saved and closed)
                When calling in a loop and writing to the same file, you must set show=False.
    """
    ierr, nbuses = psspy.abuscount(-1, 2)
    if not nbuses:
        print '\n No working case in memory. ierr=%d' % ierr
        print ' Open Saved case in PSS/E and then run this function.'
        return ''
    savfile, snapfile = psspy.sfiles()
    if not xlsfile:
        p, n, x = _get_file_path_name_ext(savfile)
        xlsfile = os.path.join(p, n)
    sid = -1
    flag = 4
    ierr, genbus = psspy.amachint(sid, flag, ['NUMBER'])
    if ierr != 0:
        print 'psspy.amachint error = %d' % ierr
        return ''
    genbus = genbus[0]
    ierr, genid = psspy.amachchar(sid, flag, ['ID'])
    if ierr != 0:
        print 'psspy.amachchar error = %d' % ierr
        return ''
    genid = genid[0]
    ierr, xtran = psspy.amachcplx(sid, flag, ['XTRAN'])
    if ierr != 0:
        print 'psspy.amachchar error = %d' % ierr
        return ''
    xtran = [abs(each) for each in xtran[0]]
    ierr, qmnmx = psspy.amachreal(sid, flag, ['QMIN', 'QMAX'])
    if ierr != 0:
        print 'psspy.amachreal error = %d' % ierr
        return ''
    mctype = [1 for i in range(len(qmnmx[0]))]
    for i in range(len(qmnmx[0])):
        qmn = qmnmx[0][i]
        qmx = qmnmx[1][i]
        if abs(qmn - qmx) <= 0.01:
            mctype[i] = 3

    machines = []
    for i in range(len(genbus)):
        if xtran[i] > 0.0:
            continue
        bus = genbus[i]
        id = genid[i]
        typ = mctype[i]
        machines.append([bus, id, typ])

    del genbus
    del genid
    del mctype
    del xtran
    del qmnmx
    sid = -1
    owner = 1
    ties = 1
    flag = 2
    entry = 1
    ierr, xmer2wdg = psspy.atrnint(sid, owner, ties, flag, entry, ['FROMNUMBER', 'TONUMBER'])
    if ierr != 0:
        print 'psspy.atrnint error = %d' % ierr
        return ''
    frmbus2 = xmer2wdg[0]
    tobus2 = xmer2wdg[1]
    ierr, xmer2id = psspy.atrnchar(sid, owner, ties, flag, entry, ['ID'])
    if ierr != 0:
        print 'psspy.atrnchar error = %d' % ierr
        return ''
    xmer2id = xmer2id[0]
    ierr, xmer3wdg = psspy.atr3int(sid, owner, ties, flag, entry, [
     'WIND1NUMBER', 'WIND2NUMBER', 'WIND3NUMBER'])
    if ierr != 0:
        print 'psspy.atr3int error = %d' % ierr
        return ''
    wdg1bus = xmer3wdg[0]
    wdg2bus = xmer3wdg[1]
    wdg3bus = xmer3wdg[1]
    ierr, xmer3id = psspy.atr3char(sid, owner, ties, flag, entry, ['ID'])
    if ierr != 0:
        print 'psspy.atr3char error = %d' % ierr
        return ''
    xmer3id = xmer3id[0]
    xmers = []
    for i in range(len(frmbus2)):
        ibs = frmbus2[i]
        jbs = tobus2[i]
        kbs = 0
        id = xmer2id[i]
        xmers.append([ibs, jbs, kbs, id])

    for i in range(len(wdg1bus)):
        ibs = wdg1bus[i]
        jbs = wdg2bus[i]
        kbs = wdg3bus[i]
        id = xmer3id[i]
        xmers.append([ibs, jbs, kbs, id])

    del xmer2wdg
    del xmer2id
    del xmer3wdg
    del xmer3id
    del frmbus2
    del tobus2
    del wdg1bus
    del wdg2bus
    del wdg3bus
    iecxls, iecshts, xlsfile = _open_workbook_worksheets(_WORKSHT_SEQ_IEC_DATA_FILE, _EXPORT_QTY_IEC_DATA_FILE, _WORKSHT_SEQ_IEC_DATA_FILE, xlsfile, sheet, overwritesheet, show)
    if not iecxls:
        return ''
    row = 1
    col = 1
    txt_m = 'Note: Machine types: 1=Synhronous gen., 2=Equivalent gen., 3=Motor'
    head_m = [['BUS', 'ID', 'MCTYPE', 'UrG', 'PG', 'PFactor', 'PolePair']]
    iecxls.set_active_sheet(iecshts['machines'][0])
    iecxls.set_cell((1, 1), txt_m)
    iecxls.font_color((1, 1), 'red')
    row = row + 1
    bottomRow, rightCol = iecxls.set_range(row, col, head_m)
    iecxls.font((row, col, row, rightCol), fontStyle='Bold', fontColor='blue')
    iecxls.worksheet_top_rows2repeat((1, 2))
    row = bottomRow + 1
    bottomRow, rightCol = iecxls.set_range(row, col, machines)
    iecxls.align_columns((1, 1), alignv='right')
    iecxls.align_columns((1, 2, 1, 3), alignv='h_center')
    iecxls.align_columns((1, 4, 1, 6), alignv='right')
    iecxls.align_columns((1, 7), alignv='h_center')
    iecxls.align((1, 1), alignv='left')
    row = 1
    col = 1
    txt_t = 'Note: Generator step-up transformer types: 1=with OLTC, 2=without OLTC'
    head_t = [['GSUType', 'IBus', 'JBus', 'KBus', 'Ckt', 'PT']]
    iecxls.set_active_sheet(iecshts['transformers'][0])
    iecxls.set_cell((1, 1), txt_t)
    iecxls.font_color((1, 1), 'red')
    row = row + 1
    bottomRow, rightCol = iecxls.set_range(row, col, head_t)
    iecxls.font((row, col, row, rightCol), fontStyle='Bold', fontColor='blue')
    iecxls.worksheet_top_rows2repeat((1, 2))
    row = bottomRow + 1
    col = 2
    bottomRow, rightCol = iecxls.set_range(row, col, xmers)
    iecxls.align_columns((1, 1), alignv='h_center')
    iecxls.align_columns((1, 2, 1, 5), alignv='right')
    iecxls.align_columns((1, 6, 1, 7), alignv='h_center')
    iecxls.align((1, 1), alignv='left')
    row = 1
    col = 1
    txt = [[txt_m], [txt_t]]
    head = head_m
    head[0].extend(head_t[0])
    iecdata_shtnam = iecshts['iec data'][0]
    newnam = ''
    for each in iecdata_shtnam.split():
        if each.lower() == 'iec':
            newnam += ' IEC'
        else:
            newnam += ' ' + each

    newnam = newnam.strip()
    iecxls.set_active_sheet(iecdata_shtnam)
    iecxls.worksheet_rename(newnam, overwritesheet=True)
    bottomRow, rightCol = iecxls.set_range(row, col, txt)
    iecxls.font_color((row, col, bottomRow, rightCol), 'red')
    row = bottomRow + 2
    bottomRow, rightCol = iecxls.set_range(row, col, head)
    iecxls.font((row, col, row, rightCol), fontStyle='Bold', fontColor='blue')
    iecxls.worksheet_top_rows2repeat((row, bottomRow))
    _save_and_close(iecxls, xlsfile, 'IEC Data', msgtype=1, show=show)
    return xlsfile


def pv(pvfile='', string='', colabel='', namesplit=True, xlsfile='', sheet='', overwritesheet=True, show=True):
    """Export PV solution results to Excel Spreadsheet.
    Returns
        Excel file name (its extension will depend on Excel version installed.)
    Inputs:
    pvfile  : PV analysis output file name (.pv), no default allowed
    string  : Name or list of names indicating which results to export, no default allowed
              's' or 'summary'   - PV Solution Summary
              'm' or 'mismatch'  - Largest and Total Mismatch
              'v' or 'voltage'   - Monitored Bus Voltage
              'g' or 'generator' - Monitored Plants MW and MVAR
              'l' or 'load'      - Monitored Loads MW and MVAR
              'b' or 'branch'    - Monitored Branch Flow (MVA)
              'i' or 'interface' - Monitored Interface Flow (MW)
              Example: string='v' or string=['s','m','v','g','l','b','i']
    colabel : Contingency label or list of contingency labels whose solution is exported,
              default - all contingencies
    namesplit : Split extended bus names
                default True
              = True,  bus names split into three values: number, name and bus voltage
              = False, bus names are kept as single value string
    Output:
    xlsfile : Excel workbook name,  default Book#.xls
    sheet   : Excel worksheet name, default ''
              Depending on "string" input, worksheets created are:
              Summary            - PV Solution Summary
              Mismatch           - Largest and Total Mismatch
              Bus Voltage        - Monitored Bus Voltage
              Generator Dispatch - Monitored Plants MW and MVAR
              Bus Load           - Monitored Loads MW and MVAR
              Branch Flow        - Monitored Branch Flow (MVA)
              Interface  Flow    - Monitored Interface Flow (MW)
              All worksheet names are prefixxed with "sheet" name, when provided.
    overwritesheet: Overwrite worksheets flag, default True
              = True,  existing worksheets are overwritten
              = False, existing worksheets are copied and their names
                appended with (#), where # is next sequence number.
    show    : Show or Hide Excel Spreadsheet flag, default True
              = True,  show Excel Spreadsheet
              = False, do not show Excel Spreadsheet (it will be just created/opened, saved and closed)
                When calling in a loop and writing to the same file, you must set show=False.
    """
    if not pvfile:
        print 'PV Analysis output file (.pv) not provided.'
        return ''
    else:
        smry = pssarrays.pv_summary(pvfile)
        colabel = _validate_contingency_labels(colabel, smry.colabel)
        valid_instrlst = _validate_string_list_contingency(string, _EXPORT_QTY_PV, colabel)
        shtprefix = sheet.strip()
        pvxls, pvshts, xlsfile = _open_workbook_worksheets(valid_instrlst, _EXPORT_QTY_PV, _WORKSHT_SEQ_PV, xlsfile, sheet, overwritesheet, show)
        if not pvxls:
            return ''
        if pvshts['summary'][1]:
            _pv_summary(pvxls, pvshts['summary'][0], smry)
        proceed_to_solution = _check_to_procced_to_solution(pvshts)
        if not proceed_to_solution:
            _save_and_close(pvxls, xlsfile, 'PV Analysis Results', msgtype=1, show=show)
            return xlsfile
        mwtransfer_lbl = 'MW TRANSFER->'
        if pvshts['mismatch'][1]:
            msmlabel = [
             mwtransfer_lbl, 'LARGEST MVA MISMATCH', 'TOTAL MVA MISMATCH', 
             'CONVERGED', 'CONVERGE CONDITION']
            row_msm = 1
        if pvshts['bus voltage'][1]:
            mvbuslabel = list(smry.mvbuslabel)
            if namesplit:
                mvbuslabel = _decode_bus_list(mvbuslabel)
                mvbuslabel.insert(0, ['', '', mwtransfer_lbl])
                transpose = False
                nttlclns_vlt = 3
            else:
                mvbuslabel.insert(0, mwtransfer_lbl)
                transpose = True
                nttlclns_vlt = 1
            options_vlt = [
             namesplit, nttlclns_vlt, transpose]
            row_vlt = 1
        if pvshts['generator dispatch'][1]:
            mgenbuslabel = list(smry.mgenbus)
            if namesplit:
                mgenbuslabel = _decode_bus_list(mgenbuslabel)
                mgenbuslabel.insert(0, ['', '', mwtransfer_lbl])
                mgenbuslabel.insert(1, ['', '', ''])
                transpose = False
                nttlclns_gen = 3
            else:
                mgenbuslabel.insert(0, mwtransfer_lbl)
                mgenbuslabel.insert(1, '')
                transpose = True
                nttlclns_gen = 1
            options_gen = [
             namesplit, nttlclns_gen, transpose]
            row_gen = 1
        if pvshts['bus load'][1]:
            mloadbuslabel = list(smry.mloadbus)
            if namesplit:
                mloadbuslabel = _decode_bus_list(mloadbuslabel)
                mloadbuslabel.insert(0, ['', '', mwtransfer_lbl])
                mloadbuslabel.insert(1, ['', '', ''])
                transpose = False
                nttlclns_lod = 3
            else:
                mloadbuslabel.insert(0, mwtransfer_lbl)
                mloadbuslabel.insert(1, '')
                transpose = True
                nttlclns_lod = 1
            options_lod = [
             namesplit, nttlclns_lod, transpose]
            row_lod = 1
        if pvshts['branch flow'][1]:
            mbranchlabel = list(smry.mbranch)
            if namesplit:
                mbranchlabel = _decode_branch_list(mbranchlabel)
                mbranchlabel.insert(0, ['', '', '', '', '', '', mwtransfer_lbl])
                transpose = False
                nttlclns_brn = 7
            else:
                mbranchlabel.insert(0, mwtransfer_lbl)
                transpose = True
                nttlclns_brn = 1
            options_brn = [
             namesplit, nttlclns_brn, transpose]
            row_brn = 1
        if pvshts['interface flow'][1]:
            if namesplit:
                minterfacelabel = _decode_interface_list(smry.minterface)
                minterfacelabel.insert(0, [mwtransfer_lbl])
                transpose = False
                nttlclns_itf = 1
            else:
                minterfacelabel = [each.strip() for each in smry.minterface]
                minterfacelabel.insert(0, mwtransfer_lbl)
                transpose = True
                nttlclns_itf = 1
            options_itf = [
             namesplit, nttlclns_itf, transpose]
            row_itf = 1
        color_now = _alternate_colors()
        ret_ierr = 0
        for lbl in colabel:
            soln = pssarrays.pv_solution(pvfile, lbl)
            if soln == None:
                continue
            if soln.ierr != 0:
                ret_ierr = soln.ierr
            if pvshts['mismatch'][1]:
                disable_wsht, row_msm = _pvqv_m(pvxls, pvshts['mismatch'][0], lbl, 'Mismatch (MVA)', row_msm, msmlabel, soln.mwtransfer, soln.mvaworst, soln.mvatotal, soln.cnvflag, soln.cnvcond)
                if disable_wsht:
                    pvxls['mismatch'][1] = False
            if pvshts['bus voltage'][1]:
                disable_wsht, row_vlt = _pvqv_one(pvxls, pvshts['bus voltage'][0], lbl, 'Voltage (pu)', row_vlt, mvbuslabel, soln.mwtransfer, soln.volts, options_vlt, soln.cnvflag)
                if disable_wsht:
                    pvxls['bus voltage'][1] = False
            if pvshts['branch flow'][1]:
                disable_wsht, row_brn = _pvqv_one(pvxls, pvshts['branch flow'][0], lbl, 'Branch Flow (MVA)', row_brn, mbranchlabel, soln.mwtransfer, soln.mbrnmva, options_brn, soln.cnvflag)
                if disable_wsht:
                    pvxls['branch flow'][1] = False
            if pvshts['interface flow'][1]:
                disable_wsht, row_itf = _pvqv_one(pvxls, pvshts['interface flow'][0], lbl, 'Interface Flow (MW)', row_itf, minterfacelabel, soln.mwtransfer, soln.mitfmw, options_itf, soln.cnvflag)
                if disable_wsht:
                    pvxls['interface flow'][1] = False
            if pvshts['generator dispatch'][1]:
                disable_wsht, row_gen = _pv_two(pvxls, pvshts['generator dispatch'][0], lbl, 'Plant (MW and MVAR)', row_gen, mgenbuslabel, soln.mwtransfer, soln.mgenmw, soln.mgenmvar, options_gen, soln.cnvflag)
                if disable_wsht:
                    pvxls['generator dispatch'][1] = False
            if pvshts['bus load'][1]:
                if not soln.mloadmw:
                    continue
                disable_wsht, row_lod = _pv_two(pvxls, pvshts['bus load'][0], lbl, 'Load (MW and MVAR)', row_lod, mloadbuslabel, soln.mwtransfer, soln.mloadmw, soln.mloadmvar, options_lod, soln.cnvflag)
                if disable_wsht:
                    pvxls['bus load'][1] = False
            color_now = _alternate_colors(color_now)

        for k, v in pvshts.iteritems():
            if not v[0]:
                continue
            sheet = v[0].lower()
            shtdefnam = sheet[len(shtprefix):].strip()
            if shtdefnam == 'summary':
                continue
            elif shtdefnam == 'mismatch':
                pvxls.autofit_columns((1, 1), sheet)
            else:
                if shtdefnam == 'bus voltage':
                    nttlclns = nttlclns_vlt
                elif shtdefnam == 'branch flow':
                    nttlclns = nttlclns_brn
                elif shtdefnam == 'interface flow':
                    nttlclns = nttlclns_itf
                elif shtdefnam == 'generator dispatch':
                    nttlclns = nttlclns_gen
                elif shtdefnam == 'bus load':
                    nttlclns = nttlclns_lod
                if namesplit:
                    pvxls.autofit_columns((1, 1, 1, nttlclns), sheet)
                else:
                    pvxls.autofit_columns((1, 1), sheet)

        _save_and_close(pvxls, xlsfile, 'PV Analysis Results', msgtype=1, show=show)
        return xlsfile


def qv(qvfile='', string='', colabel='', namesplit=True, xlsfile='', sheet='', overwritesheet=True, show=True):
    """Export QV solution results to Excel Spreadsheet.
    Returns
        Excel file name (its extension will depend on Excel version installed.)
    Inputs:
    qvfile  : QV analysis output file name (.qv), no default allowed
    string  : Name or list of names indicating which results to export, no default allowed
              's' or 'summary'   - QV Solution Summary
              'm' or 'mismatch'  - Largest and Total Mismatch
              'v' or 'voltage'   - Monitored Bus Voltage
              'g' or 'generator' - Monitored Plants MW and MVAR
              Example: string='v' or string=['s','m','v','g']
    colabel : Contingency label or list of contingency labels whose solution is exported,
              default - all contingencies
    namesplit : Split extended bus names
                default True
              = True,  bus names split into three values: number, name and bus voltage
              = False, bus names are kept as single value string
    Output:
    xlsfile : Excel workbook name,  default Book#.xls
    sheet   : Excel worksheet name, default ''
              Depending on "string" input, worksheets created are:
              Summary            - QV Solution Summary
              Mismatch           - Largest and Total Mismatch
              Bus Voltage        - Monitored Bus Voltage
              Generator Dispatch - Monitored Plants MW and MVAR
              All worksheet names are prefixxed with "sheet" name, when provided.
    overwritesheet: Overwrite worksheets flag, default True
              = True,  existing worksheets are overwritten
              = False, existing worksheets are copied and their names
                appended with (#), where # is next sequence number.
    show    : Show or Hide Excel Spreadsheet flag, default True
              = True,  show Excel Spreadsheet
              = False, do not show Excel Spreadsheet (it will be just created/opened, saved and closed)
                When calling in a loop and writing to the same file, you must set show=False.
    """
    if not qvfile:
        print 'QV Analysis output file (.qv) not provided.'
        return ''
    else:
        smry = pssarrays.qv_summary(qvfile)
        colabel = _validate_contingency_labels(colabel, smry.colabel)
        valid_instrlst = _validate_string_list_contingency(string, _EXPORT_QTY_QV, colabel)
        shtprefix = sheet.strip()
        qvxls, qvshts, xlsfile = _open_workbook_worksheets(valid_instrlst, _EXPORT_QTY_QV, _WORKSHT_SEQ_QV, xlsfile, sheet, overwritesheet, show)
        if not qvxls:
            return ''
        if qvshts['summary'][1]:
            _qv_summary(qvxls, qvshts['summary'][0], smry)
        proceed_to_solution = _check_to_procced_to_solution(qvshts)
        if not proceed_to_solution:
            _save_and_close(qvxls, xlsfile, 'QV Analysis Results', msgtype=1, show=show)
            return xlsfile
        vstp_lbl = 'VOLTAGE SETPOINT->'
        if qvshts['mismatch']:
            msmlabel = [
             vstp_lbl, 'LARGEST MVA MISMATCH', 'TOTAL MVA MISMATCH', 
             'CONVERGED', 'CONVERGE CONDITION']
            row_msm = 1
        if qvshts['bus voltage']:
            mvbuslabel = list(smry.mvbuslabel)
            if namesplit:
                mvbuslabel = _decode_bus_list(mvbuslabel)
                mvbuslabel.insert(0, ['', '', vstp_lbl])
                transpose = False
                nttlclns_vlt = 3
            else:
                mvbuslabel.insert(0, vstp_lbl)
                transpose = True
                nttlclns_vlt = 1
            options_vlt = [
             namesplit, nttlclns_vlt, transpose]
            row_vlt = 1
        if qvshts['generator dispatch']:
            mgenbuslabel = list(smry.mgenbus)
            if namesplit:
                mgenbuslabel = _decode_bus_list(mgenbuslabel)
                mgenbuslabel.insert(0, ['', '', vstp_lbl])
                transpose = False
                nttlclns_gen = 3
            else:
                mgenbuslabel.insert(0, vstp_lbl)
                transpose = True
                nttlclns_gen = 1
            options_gen = [
             namesplit, nttlclns_gen, transpose]
            row_gen = 1
        color_now = _alternate_colors()
        ret_ierr = 0
        for lbl in colabel:
            soln = pssarrays.qv_solution(qvfile, lbl)
            if soln == None:
                continue
            if soln.ierr != 0:
                ret_ierr = soln.ierr
            if qvshts['mismatch'][1]:
                disable_wsht, row_msm = _pvqv_m(qvxls, qvshts['mismatch'][0], lbl, 'Mismatch (MVA)', row_msm, msmlabel, soln.vsetpoint, soln.mvaworst, soln.mvatotal, soln.cnvflag, soln.cnvcond)
                if disable_wsht:
                    pvxls['mismatch'][1] = False
            if qvshts['bus voltage'][1]:
                disable_wsht, row_vlt = _pvqv_one(qvxls, qvshts['bus voltage'][0], lbl, 'Voltage (pu)', row_vlt, mvbuslabel, soln.vsetpoint, soln.volts, options_vlt, soln.cnvflag)
                if disable_wsht:
                    qvxls['bus voltage'][1] = False
            if qvshts['generator dispatch'][1]:
                disable_wsht, row_gen = _pvqv_one(qvxls, qvshts['generator dispatch'][0], lbl, 'Plant (MVAR)', row_gen, mgenbuslabel, soln.vsetpoint, soln.mgenmvar, options_gen, soln.cnvflag)
                if disable_wsht:
                    qvxls['generator dispatch'][1] = False
            color_now = _alternate_colors(color_now)

        for k, v in qvshts.iteritems():
            if not v[0]:
                continue
            sheet = v[0].lower()
            shtdefnam = sheet[len(shtprefix):].strip()
            if shtdefnam == 'summary':
                continue
            elif shtdefnam == 'mismatch':
                qvxls.autofit_columns((1, 1), sheet)
            else:
                if shtdefnam == 'bus voltage':
                    nttlclns = nttlclns_vlt
                elif shtdefnam == 'generator dispatch':
                    nttlclns = nttlclns_gen
                if namesplit:
                    qvxls.autofit_columns((1, 1, 1, nttlclns), sheet)
                else:
                    qvxls.autofit_columns((1, 1), sheet)

        _save_and_close(qvxls, xlsfile, 'QV Analysis Results', msgtype=1, show=show)
        return xlsfile


def pvuserin():
    """Get argument values for "pssexcel.pv" function using 'psspy.userin' function.
    """
    pvfile, string, colabel, xlsfile, sheet, overwritesheet = pssexceluserin.pv()
    pv(pvfile, string, colabel, xlsfile, sheet, overwritesheet)


def qvuserin():
    """Get argument values for "pssexcel.qv" function using 'psspy.userin' function.
    """
    qvfile, string, colabel, xlsfile, sheet, overwritesheet = pssexceluserin.qv()
    qv(qvfile, string, colabel, xlsfile, sheet, overwritesheet)


if __name__ == '__main__':
    print 'Functions to Export PSSE Data/Results to Excel Spreadsheet.\nSee help(pssexcel) for details.\n    '

# okay decompiling pssexcel.pyc
