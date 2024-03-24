# uncompyle6 version 3.9.1
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  4 2019, 01:37:19) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: .\pssarrays.py
# Compiled at: 2016-05-19 21:00:09
"""
    Python Module:
    (1) To retrieve PSS(R)E Solution Results in Python Lists.
        Returned Python Lists are accessed as attributes of a list object.
        The attribute name is the name of the List.
    (2) To get reports based on the retrieved arrays.
"""
import sys, os, tempfile, math, time, traceback, shutil, collections, re, psspy, pssaccss
_PFLOW_SOLVED_STATE = {0: 'Met convergence tolerance', 
   1: 'Iteration limit exceeded', 
   2: 'Blown up (only when non-divergent option disabled)', 
   3: 'Terminated by non-divergent option', 
   4: 'Terminated by console interrupt', 
   5: 'Singular Jacobean matrix or (0.,0.) voltage', 
   6: 'Inertial load flow dispatch error (INLF)', 
   7: 'OPF solution met convergence tolerance (NOPF)', 
   9: 'Solution not attempted'}
_ALLOW_PLT_MSG = ''
try:
    import matplotlib as mpl
    _ok_mpl = True
except:
    _ok_mpl = False
    _ALLOW_PLT_MSG += " Error executing 'import matplotlib', check if matplotlib is installed\n"

try:
    import matplotlib.pyplot as plt
    _ok_plt = True
except:
    _ok_plt = False
    _ALLOW_PLT_MSG += " Error executing 'import matplotlib.pyplot', check matplotlib installation\n"

try:
    import matplotlib.patches as patches
    _ok_patches = True
except:
    _ok_patches = False
    _ALLOW_PLT_MSG += " Error executing 'import matplotlib.patches', check matplotlib installation\n"

try:
    import matplotlib.transforms as mtransforms
    _ok_transforms = True
except:
    _ok_transforms = False
    _ALLOW_PLT_MSG += " Error executing 'import matplotlib.transforms', check matplotlib installation\n"

if _ok_mpl and _ok_plt and _ok_patches and _ok_transforms:
    _OK_MATPLOTLIB = True
else:
    _OK_MATPLOTLIB = False
try:
    import numpy as np
    _OK_NUMPY = True
except:
    _OK_NUMPY = False
    _ALLOW_PLT_MSG += " Error executing 'import numpy', check if numpy is installed\n"

try:
    from mpl_toolkits.basemap import Basemap
    _OK_BASEMAP = True
except:
    _OK_BASEMAP = False
    _ALLOW_PLT_MSG += " Error executing 'mpl_toolkits.basemap', check if matplotlib toolkit Basemap is installed\n"

if _OK_MATPLOTLIB and _OK_NUMPY and _OK_BASEMAP:
    pass
else:
    _ALLOW_PLT_MSG += '\n Download and install required Python module(s). Refer:\n'
    _ALLOW_PLT_MSG += "      PSSE User Support Web Page and follow link 'Python Modules used by PSSE Python Utilities'\n"
_LEGENDS_FLOW_DIR = {'in': {'color': 'blue', 'linewidth': 1.5, 'marker': 'o'}, 'out': {'color': 'red', 'linewidth': 1.5, 'marker': 'D'}}
_LEGENDS_FLOW_DIR_SEQ = [
 'in', 'out']
_TMP_GICPY_FNAM = 'tmpjnkgic.py'
_TMP_GICPYC_FNAM = 'tmpjnkgic.pyc'
_MAP_LONLAT_DELTA = 4.0
_DISTANCE_THRESHOLD_FACTOR = 0.05
_IERR_NO = 0
_IERR_YES = 1
_BIGINT = psspy.psspyc.getdefaultint()
_BIGREL = psspy.psspyc.getdefaultreal()
_ERR_CODE_NAM = 'ierr'
_SHRT_TITLE_NAM = (
 'line1',
 'line2')
_RATING_NAM = (
 'a',
 'b',
 'c')
_DFAX_SIZE_NAM = (
 'size',
 (
  'nmline',
  'ninter',
  'ncase'))
_DFAX_FILE_NAM = (
 'sav',
 'dfx',
 'sub',
 'mon',
 'con')
_OTDF_FACTORS_NAM = (
 (
  'casetitle', _SHRT_TITLE_NAM),
 (
  'file', _DFAX_FILE_NAM),
 'melement',
 'colabel',
 'codesc',
 'factor')
_DFAX_SUMMARY_NAM = (
 (
  'casetitle', _SHRT_TITLE_NAM),
 (
  'file', _DFAX_FILE_NAM),
 'melement',
 'colabel',
 'codesc')
_ACCC_SOLUTION_TYPES = (
 (
  'contingency',
  'con'),
 (
  'tripping',
  'trp'),
 (
  'caction',
  'corrective action',
  'cor'))
_ACCC_SIZE_NAM = (
 'nmline',
 'ninter',
 'ncase',
 'nmvbus',
 'nmvrec',
 'nmvbusrec',
 'nbus',
 'vernum',
 'ncntlshed',
 'ntrplshed',
 'ncactlshed',
 'ncactgdisp',
 'ncactphsftr',
 'nameout',
 'filetype',
 'nareas',
 'nzones',
 'nowners',
 'nvltlevels')
_ACCC_FILE_NAM = (
 'acc',
 'sav',
 'dfx',
 'sub',
 'mon',
 'con',
 'thr',
 'inl',
 'trp')
_ACCC_SUMMARY_NAM = (
 'acccsize',
 'casetitle',
 'file',
 'melement',
 'rating',
 'mvbuslabel',
 'mvreclabel',
 'mvrecmax',
 'mvrecmin',
 'mvrectype',
 'colabel',
 'busname',
 'addcnt',
 'addtrp',
 'addcor',
 'mvrec_ivb')
_ACCC_SOLUTION_NAM = (
 'codesc',
 'cnvflag',
 'cnvcond',
 'island',
 'mvaworst',
 'mvatotal',
 'volts',
 'mvaflow',
 'ampflow',
 'lshedbus',
 'loadshed',
 'gdispbus',
 'gendisp',
 'phsftr',
 'phsftrang')
_ACCC_BRNFLOW_UNITS_NAM = (
 'xfrcur',
 'nxfrcr')
_FLT_BUS_NUM = 'fltbus'
_SHORT_CIRCUIT_UNIT = 'scunit'
_SHORT_CIRCUIT_COORDINATES = 'scfmt'
_THEVZ_NAM = (
 'thevz',
 'thevzpu')
_THEVZ_NAM_SEQUENCE = (
 'z1',
 'z2',
 'z0')
_SEQUENCE_CURRENTS_NAM = (
 'ia1',
 'ia2',
 'ia0')
_PHASE_CURRENTS_NAM = (
 'ia',
 'ib',
 'ic')
_SC_FAULT_CURRENTS_NAM = (
 'ia1',
 'ia2',
 'ia0',
 'ia',
 'ib',
 'ic')
_SC_FAULT_NAM = (
 'flt3ph',
 'fltlg',
 'fltllg',
 'fltll',
 'linout',
 'linend')
_SC_FAULT_MAX_I = 'maxflt'
_SC_FAULT_MAX_I_DSC = 'maxfltdsc'
_IECS_CURRENTS_NAM = list(_SC_FAULT_CURRENTS_NAM)
_IECS_CURRENTS_NAM.extend([
 'ipb', 
 'ipc', 
 'idc', 
 'ibsym', 
 'ibuns'])
_IECS_CURRENTS_NAM = tuple(_IECS_CURRENTS_NAM)
_PV_SIZE_NAM = (
 'ncase',
 'vernum',
 'nmline',
 'ninter',
 'nmvbus',
 'nmvrec',
 'nmgnbus',
 'nmxtrns',
 'nmldbus',
 'noptns',
 'nvals',
 'nfiles',
 'nsslbls')
_PV_FILE_NAM = (
 'pv',
 'sav',
 'ecd',
 'thr',
 'dfx',
 'sub',
 'mon',
 'con',
 'inl',
 'zip')
_PV_SUMMARY_NAM = (
 'pvsize',
 'options',
 'brnflowunits',
 'values',
 'casetitle',
 'file',
 'srcsink',
 'mbranch',
 'mbrnrating',
 'minterface',
 'mitfrating',
 'mgenbus',
 'mloadbus',
 'mvbuslabel',
 'mvreclabel',
 'mvrecmax',
 'mvrecmin',
 'mvrectype',
 'mvrec_ivb',
 'colabel',
 'codesc',
 'maxmw',
 'minmw',
 'cntadr',
 'cntntrns',
 'cntnegi')
_PV_SOLUTION_NAM = (
 'island',
 'mwtransfer',
 'cnvflag',
 'cnvcond',
 'mvaworst',
 'mvatotal',
 'volts',
 'mgenmw',
 'mgenmvar',
 'mloadmw',
 'mloadmvar',
 'mbrnmva',
 'mbrnamp',
 'mitfmw')
_PV_INT_OPTIONS_NAMES = (
 'base case tap adjustment',
 'base case area interchange adjustment',
 'base case phase shift adjustment',
 'base case dc tap adjustment',
 'base case switched shunt adjustment',
 'base case induction motor treatment (when motor fails to solve due to low terminal voltage)',
 'non-divergent solution',
 'solution method',
 'var limit code for the contingency case power flow solution',
 'var limit code for base case transfer increment solutions',
 'rating set',
 'study (source) sytem transfer dispatch method',
 'opposing (sink) system transfer dispatch method',
 'generation plant limits for transfer methods 1, 3, 5, 6 and 7',
 'positive load for transfer methods 2, 3 and 4',
 'check for low voltage at any monitored bus',
 'check for excessive loading on any monitored branch',
 'dispatch mode for power unbalances resulting from the application of contingencies',
 'ZIP archive',
 'contingency case tap adjustment',
 'contingency case area interchange adjustment',
 'contingency case phase shift adjustment',
 'contingency case dc tap adjustment',
 'contingency case switched shunt adjustment',
 'contingency case induction motor treatment (when motor fails to solve due to low terminal voltage)')
_PV_INT_OPTIONS_LIST = (
 [
  'disable',
  'enable stepping adjustment',
  'enable direct adjustment'],
 [
  'disable',
  'enable using tie flows only in calculating area interchange',
  'enable using tie flows and loads in calculating interchange'],
 [
  'disable',
  'enable'],
 [
  'disable',
  'enable'],
 [
  'disable',
  'enable',
  'enable continuous mode, disable discrete mode'],
 [
  'stall',
  'trip'],
 [
  'disable',
  'enable'],
 [
  'FDNS',
  'FNSL',
  'optimized FDNS'],
 [
  'apply immediately',
  'initially ignore, then apply automatically'],
 [
  'apply immediately',
  'initially ignore, then apply automatically'],
 [
  '', 'rate A',
  'rate B',
  'rate C'],
 [
  '', 
  'buses & factors from dfax file for buses with positive MW machines', 
  'buses & factors from dfax file for buses with positive MW constant MVA load', 
  'buses & factors from dfax file for buses with either positive mw machines or positive MW constant MVA load', 
  'subsystem buses with positive MW constant MVA load in proportion to their MW load', 
  'subsystem buses with positive MW machines in proportion to their MW output', 
  'subsystem buses with positive MW machines in proportion to their MBASEs', 
  'subsystem buses with positive MW machines in proportion to their reserves (pmaxmc - pgenmc)', 
  'subsystem buses with positive MW machines via ECDI with with unit commitment disabled', 
  'subsystem buses with positive MW machines via ECDI with with unit commitment enabled'],
 [
  '', 
  'buses & factors from dfax file for buses with positive MW machines', 
  'buses & factors from dfax file for buses with positive MW constant MVA load', 
  'buses & factors from dfax file for buses with either positive MW machines or positive MW constant MVA load', 
  'subsystem buses with positive MW constant MVA load in proportion to their MW load', 
  'subsystem buses with positive MW machines in proportion to their MW output', 
  'subsystem buses with positive MW machines in proportion to their MBASEs', 
  'subsystem buses with positive MW machines in proportion to their reserves (pgenmc - pminmc)', 
  'subsystem buses with positive MW machines via ECDI with with unit commitment disabled', 
  'subsystem buses with positive MW machines via ECDI with with unit commitment enabled'],
 [
  'no limits',
  'honor machine active power limits'],
 [
  'no limits',
  'enforce non-negative net active power constant MVA load'],
 [
  'disable check', 
  'enable check using the threshold specified', 
  'enable check using the normal lower voltage limits for base and contingency case solutions', 
  'enable check using the normal lower voltage limits for base case solutions and the emergency lower voltage limits for contingency case solutions', 
  'enable check using the emergency lower voltage limits for base and contingency case solutions'],
 [
  'disable check',
  'enable check'],
 [
  'disable', 
  'in-service subsystem machines using reserve', 
  'in-service subsystem machines using pmax', 
  'in-service subsystem machines using inertia', 
  'in-service subsystem machines using governor droop'],
 [
  'No ZIP Archive file',
  'Write ZIP Archive file ZIPFILE; preserve each system condition at its largest solved incremental transfer level',
  'Write ZIP Archive file ZIPFILE; preserve each system condition at all of its solved incremental transfer levels'],
 [
  'disable',
  'enable stepping adjustment',
  'enable direct adjustment'],
 [
  'disable',
  'enable using tie flows only in calculating area interchange',
  'enable using tie flows and loads in calculating area interchange'],
 [
  'disable',
  'enable'],
 [
  'disable',
  'enable'],
 [
  'disable',
  'enable',
  'enable continuous mode, disable discrete mode'],
 [
  'stall',
  'trip'])
_PV_REAL_VALUES_NAMES = (
 'mismatch tolerance in MW and MVAR',
 'initial transfer increment in MW',
 'transfer increment tolerance in MW',
 'maximum incremental transfer in MW',
 'low voltage threshold in pu in the low voltage check',
 'percent of rating in the excessive branch loading check',
 'minimum incremental transfer in MW',
 'power factor for load increases in dispatch methods 2, 3 and 4')
_QV_SIZE_NAM = (
 'ncase',
 'vernum',
 'notapp1',
 'notapp2',
 'nmvbus',
 'nmvrec',
 'nmgnbus',
 'nmxvstp',
 'notapp3',
 'noptns',
 'nvals',
 'nfiles',
 'nsslbls')
_QV_FILE_NAM = (
 'qv',
 'sav',
 'thr',
 'dfx',
 'sub',
 'mon',
 'con',
 'inl',
 'zip')
_QV_SUMMARY_NAM = (
 'qvbus',
 'qvsize',
 'options',
 'values',
 'casetitle',
 'file',
 'mgenbus',
 'mvbuslabel',
 'mvreclabel',
 'mvrecmax',
 'mvrecmin',
 'mvrectype',
 'mvrec_ivb',
 'colabel',
 'codesc',
 'minvstp',
 'maxvstp',
 'minmvar',
 'maxmvar',
 'maxmsm',
 'cntadr',
 'cntnvstp',
 'dispatchss')
_QV_SOLUTION_NAM = (
 'island',
 'vsetpoint',
 'cnvflag',
 'cnvcond',
 'mvaworst',
 'mvatotal',
 'volts',
 'mgenmvar')
_QV_INT_OPTIONS_NAMES = (
 'tap adjustment',
 'area interchange adjustment',
 'phase shift adjustment',
 'dc tap adjustment',
 'switched shunt adjustment',
 'induction motor treatment (when motor fails to solve due to low terminal voltage)',
 'non-divergent solution',
 'solution method',
 'var limit code for the vhi power flow solution',
 'var limit code for the subsequent voltage decrement cases',
 'study bus number',
 'dispatch mode for power unbalances resulting from the application of contingencies',
 'ZIP archive')
_QV_INT_OPTIONS_LIST = (
 [
  'disable',
  'enable stepping adjustment',
  'enable direct adjustment'],
 [
  'disable',
  'enable using tie flows only in calculating area interchange',
  'enable using tie flows and loads in calculating interchange'],
 [
  'disable',
  'enable'],
 [
  'disable',
  'enable'],
 [
  'disable',
  'enable',
  'enable continuous, disable discrete'],
 [
  'stall',
  'trip'],
 [
  'disable',
  'enable'],
 [
  'FDNS',
  'FNSL',
  'optimized FDNS'],
 [
  'apply immediately',
  'initially ignore, then apply automatically'],
 [
  'apply immediately',
  'initially ignore, then apply automatically'],
 [
  ''],
 [
  'disable', 
  'in-service subsystem machines using reserve', 
  'in-service subsystem machines using pmax', 
  'in-service subsystem machines using inertia', 
  'in-service subsystem machines using governor droop'],
 [
  'No ZIP Archive file',
  'Write ZIP Archive file ZIPFILE; preserve each system condition at its largest solved incremental transfer level',
  'Write ZIP Archive file ZIPFILE; preserve each system condition at all of its solved incremental transfer levels'])
_QV_INT_OPTIONS_STUDY_BUS_INDEX = 11
_QV_REAL_VALUES_NAMES = (
 'mismatch tolerance in MW and MVAR',
 'initial (maximum) p.u. voltage setpoint at the study bus (VHI)',
 'minimum p.u. voltage setpoint at the study bus (VLO)',
 'p.u. voltage setpoint decrement (positive) at the study bus (DLTAV)')
_INPUTERROR = 'InputError'
_SCUNIT = ['pu', 'physical']
_SCFMT = ['rectangular', 'polar']
_a3c_accfnam = None
_a3c_size = None
_a3c_summary = None
_a3c_accfnam_size = None
_a3c_accfnam_mtime = None
_otdf_dfxfnam = None
_otdf_dfxfnam_size = None
_otdf_dfxfnam_mtime = None
_otdf_ftrs_size = None
_otdf_ftrs = None
_ppv_pvfnam = None
_ppv_size = None
_ppv_summary = None
_ppv_pvfnam_size = None
_ppv_pvfnam_mtime = None
_qqv_qvfnam = None
_qqv_size = None
_qqv_summary = None
_qqv_qvfnam_size = None
_qqv_qvfnam_mtime = None
_do_pv_after_qv = True
_do_qv_after_pv = True

def check_psse_run_mode():
    """from_psse_gui = check_psse_run_mode()
    Check if PSSE is run from inside or outside of PSSE GUI
    Returns:
    from_psse_gui = True, when PSSE is run from inside PSSE GUI
                  = False, when PSSE is run from outside of PSSE GUI
    """
    _exepn = sys.executable
    _p, _exename = os.path.split(_exepn)
    _exename = _exename.lower()
    if _exename.find('psse') < 0:
        from_psse_gui = False
    else:
        from_psse_gui = True
    return from_psse_gui


_FROM_PSSE_GUI = check_psse_run_mode()

def _show_message(msg):
    if not msg:
        return
    if _FROM_PSSE_GUI:
        psspy.progress(msg)
    else:
        sys.stdout.write(msg)


def _ShowError(nam, errtxt):
    psspy.progress('\n')
    errmsg = ' %s --> %s' % (nam, errtxt)
    raise RuntimeError(errmsg)


def _ShowError_NoExec(nam, errtxt):
    psspy.progress('\n')
    errmsg = ' %s --> %s' % (nam, errtxt)


def start_timer():
    """Start timer and return time in seconds since the Epoch.
start_time = start_timer()
"""
    start_time = time.time()
    return start_time


def finish_timer(start_time):
    """Finish timer and return elapsed time as string.
timstr = finish_timer(start_time)
where start_time is value returned by start_timer().
"""
    finish_time = time.time()
    elapsed_sec = finish_time - start_time
    hr, mn1 = divmod(elapsed_sec, 3600)
    mn, sc = divmod(mn1, 60)
    timstr = ' Elapsed time: Hours = %d , Minutes = %d, Seconds = %g\n' % (hr, mn, sc)
    return timstr


def filename_with_allowed_chars(fnam, substr='_'):
    r"""Characters \/:*?"<>| are not allowed in filename. Get filename by replacing these
characters with 'substr' value provided.
    fnam = filename_with_allowed_chars(fnam, substr='_')
where:
    fnam   = Input file name (just file name, without its path)
    substr = Not allowed characters in file name are replaced by this string, '_' by default
"""
    fnam = re.sub('[!\\\\/:*?"<>|]', '_', fnam)
    return fnam


def _get_date_time_str():
    return time.strftime('%a, %b %d %Y  %H:%M:%S', time.localtime()).upper()


def _get_product_name():
    name, major, minor, modlvl, date, stat = psspy.psseversion()
    return ('{0:s}-{1:d}.{2:d}.{3:d}').format(name.strip(), major, minor, modlvl)


class _CaseLessAttributeList(list):

    def __init__(self, lstnames=None, inlist=None):
        list.__init__(self, inlist)
        for i in range(len(inlist)):
            if isinstance(inlist[i], type([])):
                v = inlist[i]
                for j in range(len(v)):
                    if isinstance(v[j], type([])):
                        v[j] = tuple(v[j])

                exec 'self.%s = tuple(v)' % lstnames[i]
            else:
                exec 'self.%s = inlist[i]' % lstnames[i]

    def __getattr__(self, name):
        """To implement caseless attributes."""
        return object.__getattribute__(self, name.lower())


class _Dict_caseless_bunch(dict):
    """
    Access dictionary items as caseless attributes or caseless dictionary items.
    """

    def __init__(self, mydict=None):
        dict.__init__(self, mydict)

    def __getitem__(self, key):
        """To implement caseless keys."""
        if key == None:
            raise KeyError(key)
        key = key.lower()
        try:
            return dict.__getitem__(self, key)
        except:
            raise

        return

    def __getattr__(self, name):
        """To implement caseless attributes."""
        try:
            return self[name.lower()]
        except KeyError:
            raise AttributeError("'%s' does not exist in Argument List." % name)
        except:
            raise

    def __setitem__(self, name, value):
        dict.__setitem__(self, name.lower(), value)

    def __setattr__(self, name, value):
        dict.__setitem__(self, name.lower(), value)


def _list_name_values_to_dict(namlist, vallist):
    retvdict = collections.OrderedDict()
    for k, v in zip(namlist, vallist):
        if type(k) in [tuple, list]:
            k1 = k[0]
        else:
            k1 = k
        retvdict[k1] = v

    return retvdict


def _get_report_object(rptfile):
    if rptfile:
        fpath, fext = os.path.splitext(rptfile)
        if not fext:
            rptfile = fpath + '.txt'
        rptfile_h = open(rptfile, 'w')
        report = rptfile_h.write
    else:
        rptfile_h = None
        if _FROM_PSSE_GUI:
            psspy.beginreport()
            report = psspy.report
        else:
            report = sys.stdout.write
    return (
     rptfile, rptfile_h, report)


def _report_done_message_str(rptfile, rptfile_h, rptdesc=u''):
    if rptfile:
        if rptdesc:
            msg = ("\n {0} report created in '{1}' file.\n").format(rptdesc, rptfile)
        else:
            msg = ("\n Report created in '{0}' file.\n").format(rptfile)
        rptfile_h.close()
    elif _FROM_PSSE_GUI:
        if rptdesc:
            msg = ('\n {0} report created in PSSE report window.\n').format(rptdesc)
        else:
            msg = '\n Report created in PSSE report window.\n'
    else:
        msg = ''
    return msg


def _remove_extra_spaces_string(instr):
    """Remove in between extra spaces from input string"""
    instr = instr.strip()
    while True:
        if instr.find('  ') < 0:
            break
        instr = instr.replace('  ', ' ')

    return instr


def _remove_extra_spaces(instr):
    """Remove in between extra spaces from input string list"""
    if isinstance(instr, type(())):
        ret_tuple = []
        for each in instr:
            each = _remove_extra_spaces_string(each)
            ret_tuple.append(each)

        return tuple(ret_tuple)
    else:
        if isinstance(instr, type([])):
            ret_list = []
            for each in instr:
                each = _remove_extra_spaces_string(each)
                ret_list.append(each)

            return ret_list
        ret_str = _remove_extra_spaces_string(instr)
        return ret_str


def _transpose_list(inlst):
    """
    oulst=[]
    rlst1=[]
    for i in range(len(inlst[0])):
        rlst1=[]
        for j in range(len(inlst)):
            rlst1.append(inlst[j][i])
        oulst.append(tuple(rlst1))
    del rlst1
    """
    if type(inlst[0]) in [list, tuple]:
        oulst = zip(*inlst)
    elif type(inlst) in [list, tuple]:
        oulst = []
        for each in inlst:
            v = [
             each]
            oulst.append(tuple(v))

    else:
        oulst = []
    return tuple(oulst)


def _check_int_type(var, varnam):
    """Check if argument input is integer."""
    if var == None:
        lerr = False
        var = _BIGINT
    else:
        if type(var) == int:
            lerr = False
        elif type(var) == float:
            lerr = False
            var = int(var)
        elif type(var) == str:
            try:
                var = int(var)
                lerr = False
            except:
                lerr = True

        else:
            lerr = True
        if lerr:
            psspy.progress(' %s = %s, should be integer value.' % (varnam, str(var)))
            var = _BIGINT
    return (
     lerr, var)


def _check_float_type(var, varnam):
    """Check if argument input is float."""
    if var == None:
        lerr = False
        var = _BIGREL
    else:
        if type(var) in [float, int]:
            lerr = False
        elif type(var) == str:
            try:
                var = float(var)
                lerr = False
            except:
                lerr = True

        else:
            lerr = True
        if lerr:
            psspy.progress(' %s = %s, should be float value.' % (varnam, str(var)))
            var = _BIGREL
    return (
     lerr, var)


def _check_str_type(var, varnam):
    """Check if argument input is string."""
    if var == None:
        lerr = False
        var = ''
    else:
        if type(var) == str:
            lerr = False
        else:
            lerr = True
        if lerr:
            psspy.progress(' %s = %s, should be string value.' % (varnam, str(var)))
            var = ''
    return (
     lerr, var)


def _check_int_input(var, varnam, minval, maxval, defval):
    """Validate integer input value."""
    try:
        if isinstance(var, int):
            if var < minval or var > maxval:
                psspy.progress(' Invalid %s value of %d.\n' % (varnam.upper(), var))
                psspy.progress('     Set to default=%d' % defval)
                var = defval
        else:
            psspy.progress(' %s value %s not recognized.\n' % (varnam.upper(), var))
            psspy.progress('     Set to default=%d' % defval)
            var = defval
    except:
        var = defval

    return var


def _check_float_input(var, varnam, minval, maxval, defval):
    """Validate float input value."""
    try:
        if isinstance(var, float) or isinstance(var, int):
            if var < minval or var > maxval:
                psspy.progress(' Invalid %s value of %g.\n' % (varnam.upper(), var))
                psspy.progress('     Set to default=%g' % defval)
                var = defval
        else:
            psspy.progress(' %s value %s not recognized.\n' % (varnam.upper(), var))
            psspy.progress('     Set to default=%g' % defval)
            var = defval
    except:
        var = defval

    return var


def _check_string_input(var, varnam, allowlst, defval):
    """Validate string input value."""
    try:
        if isinstance(var, str):
            var = var.lower()
            if var not in allowlst:
                psspy.progress(' Invalid %s input of %s.\n' % (varnam, var))
                psspy.progress('     Set to default=%s' % defval)
                var = defval
        else:
            psspy.progress(' %s value %s not recognized.\n' % (varnam, var))
            psspy.progress('     Set to default=%s' % defval)
            var = defval
    except:
        var = defval

    return var


def _remove_extra_spaces_string(instr):
    """Remove in between extra spaces from input string"""
    instr = instr.strip()
    while True:
        if instr.find('  ') < 0:
            break
        instr = instr.replace('  ', ' ')

    return instr


def _remove_extra_spaces(instr):
    """Remove in between extra spaces from input string list"""
    if isinstance(instr, type(())):
        ret_tuple = []
        for each in instr:
            each = _remove_extra_spaces_string(each)
            ret_tuple.append(each)

        return tuple(ret_tuple)
    else:
        if isinstance(instr, type([])):
            ret_list = []
            for each in instr:
                each = _remove_extra_spaces_string(each)
                ret_list.append(each)

            return ret_list
        ret_str = _remove_extra_spaces_string(instr)
        return ret_str


def _check_file(name=None, ext=None, desc=None, type=None):
    """check if file to read exists."""
    if name:
        fpath, fext = os.path.splitext(name)
        if not fext and ext:
            if ext[0] == '.':
                name = fpath + ext
            else:
                name = fpath + '.' + ext
        if type.lower() == 'read' and not os.path.exists(name):
            if desc:
                errtxt = ' %s file %s does not exist.' % (desc, name)
                _ShowError(_INPUTERROR, errtxt)
            else:
                errtxt = ' File %s does not exist.' % name
                _ShowError(_INPUTERROR, errtxt)
    elif desc:
        errtxt = ' %s file not provided.' % desc
        _ShowError(_INPUTERROR, errtxt)
    else:
        errtxt = ' File not provided.'
        _ShowError(_INPUTERROR, errtxt)
    return name


def _check_file_no_exec(name=None, ext=None, desc=None, type=None):
    """check if file to read exists."""
    if name:
        fpath, fext = os.path.splitext(name)
        if not fext and ext:
            if ext[0] == '.':
                name = fpath + ext
            else:
                name = fpath + '.' + ext
        if type.lower() == 'read' and not os.path.exists(name):
            if desc:
                errtxt = ' %s file %s does not exist.' % (desc, name)
                _ShowError_NoExec(_INPUTERROR, errtxt)
            else:
                errtxt = ' File %s does not exist.' % name
                _ShowError_NoExec(_INPUTERROR, errtxt)
    elif desc:
        errtxt = ' %s file not provided.' % desc
        _ShowError_NoExec(_INPUTERROR, errtxt)
    else:
        errtxt = ' File not provided.'
        _ShowError_NoExec(_INPUTERROR, errtxt)
    return name


def _get_report_file_object(rptfile=None, process='open', rptdesc=None):
    """open and close file/report objects"""
    global rptfile_h
    if process.lower() == 'open':
        if rptfile:
            fpath, fext = os.path.splitext(rptfile)
            if not fext:
                rptfile = fpath + '.txt'
            rptfile_h = open(rptfile, 'w')
            report = rptfile_h.write
        else:
            psspy.beginreport()
            report = psspy.report
        return report
    if not rptdesc:
        rptdesc = ''
    if rptfile:
        psspy.progress("\n %s report created in '%s' file.\n" % (rptdesc, rptfile))
        rptfile_h.close()
    else:
        psspy.progress('\n %s report created in PSS(R)E report window.\n' % rptdesc)
    return
    return


def _samefileACC(newfile):
    """
    NOT used
    check if _a3c_accfnam and newfile are same.
    Returns true if both arguments refer to the same file.
    os.path.samefile() does not exist on Windows.
    File name, size and modification time compared.
    """
    global _a3c_accfnam
    global _a3c_accfnam_mtime
    global _a3c_accfnam_size
    if _a3c_accfnam == newfile:
        if _a3c_accfnam_size == os.path.getsize(newfile):
            if _a3c_accfnam_mtime == os.path.getmtime(newfile):
                return True
            else:
                return False

        else:
            return False
    else:
        return False


def _samefile(oldfile, oldfile_size, oldfile_mtime, newfile):
    """
    check if file for which size and summary exists and newfile are same.
    Returns true if both arguments refer to the same file.
    os.path.samefile() does not exist on Windows.
    File name, size and modification time compared.
    """
    if oldfile == newfile:
        if oldfile_size == os.path.getsize(newfile):
            if oldfile_mtime == os.path.getmtime(newfile):
                retv = True
            else:
                retv = False
        else:
            retv = False
    else:
        retv = False
    return retv


def _validate_previous_results(size, *summary):
    """
    Validate previous solution results.
    Requires this check, so that previous error (=None) is not returned.
    """
    try:
        if size:
            if summary:
                smry = summary[0]
                if smry.ierr == 0:
                    retv = True
                else:
                    retv = True
            else:
                retv = True
        else:
            retv = False
    except:
        retv = False

    return retv


def _check_contingency_label(colabel, caselabels, caseaddress):
    """check for valid contingency label and return its address."""
    if colabel:
        colabel = colabel.upper()
        if colabel in caselabels:
            idx = list(caselabels).index(colabel)
            coaddress = caseaddress[idx]
        else:
            coaddress = None
            psspy.progress('\n Contingency "%12s" does not exist. Ignored.. \n' % colabel)
    else:
        coaddress = None
        psspy.progress('\n Contingency Label not provided.\n')
    return coaddress


def _check_rate(rating, ratingabc):
    """check for valid rating string."""
    if rating:
        if rating.isalpha():
            rating = rating.lower()
        if rating not in _RATING_NAM:
            psspy.progress(' Rating %s not recognized.\n' % rating.upper())
            psspy.progress('   Default Rating %s considered.\n' % _RATING_NAM[0].upper())
            rating = _RATING_NAM[0]
            ratename = 'A'
    else:
        rating = _RATING_NAM[0]
        ratename = 'A'
    if rating == _RATING_NAM[1]:
        rate = ratingabc.b
        ratename = 'B'
    elif rating == _RATING_NAM[2]:
        rate = ratingabc.c
        ratename = 'C'
    else:
        rate = ratingabc.a
        ratename = 'A'
    return (ratename, rate)


def _check_flowlimit(flowlimit=None):
    """check for valid flow limit."""
    if flowlimit:
        if not (isinstance(flowlimit, float) or isinstance(flowlimit, int)):
            idx = flowlimit.find('%')
            if idx != -1:
                flowlimit = flowlimit[:idx]
            if flowlimit:
                flowlimit = float(flowlimit)
            else:
                flowlimit = 100.0
    else:
        flowlimit = 100.0
    return flowlimit


def _check_accc_solution_type(stype):
    """check for valid ACCC solution type."""
    if stype:
        if isinstance(stype, str):
            stype1 = stype.lower().strip()
        else:
            stype1 = 'junk'
    else:
        stype1 = _ACCC_SOLUTION_TYPES[0][0]
    alltypes = []
    for each in _ACCC_SOLUTION_TYPES:
        alltypes.extend(each)

    if stype1 not in alltypes:
        stype1 = _ACCC_SOLUTION_TYPES[0][0]
        txt = " Warning.. Solution type '%s' not available.\n" % stype
        txt += "           Defaulted to 'contingency' solution.\n"
        psspy.progress(txt)
    if stype1 in _ACCC_SOLUTION_TYPES[1]:
        getwhat = 2
        getwhatname = 'TRIPPING'
        stype = _ACCC_SOLUTION_TYPES[1][0]
    elif stype1 in _ACCC_SOLUTION_TYPES[2]:
        getwhat = 3
        getwhatname = 'CORRECTIVE ACTION'
        stype = _ACCC_SOLUTION_TYPES[2][0]
    else:
        getwhat = 1
        getwhatname = 'POST-CONTINGENCY'
        stype = _ACCC_SOLUTION_TYPES[0][0]
    return (getwhat, getwhatname, stype)


def _transfer_voltages_nmvbus_to_nmvbusrec(nmvbus, nmvrec, ncnt, mvrec_ivb, volts):
    """
    Chnaged inline code to this function on 04/04/2007. Not tested and used.
    """
    if not nmvbus:
        return None
    else:
        mv_vmag = []
        for n in range(ncnt):
            mv_vmag_rec = []
            for i in range(nmvrec):
                for j in range(nmvbus):
                    k = mvrec_ivb[i][j]
                    if k == 0:
                        break
                    if k < 0:
                        continue
                    mv_vmag_rec.append(volts[n][k - 1])

            mv_vmag.append(mv_vmag_rec)

        return mv_vmag


def _accc_size(accfile=None):
    """
    rlst = _accc_size(accfile)
    Returns ACCC solution array sizes.
    Inputs:
        accfile          = ACCC output file name (.acc)
    Returned object 'rlst' contains the following attributes:
        rlst.ierr        = error code (0=no error)
        rlst.nmline      = number of monitored branches
        rlst.ninter      = number of monitored interfaces
        rlst.ncase       = number of contingencies + 1 (for base case)
        rlst.nmvbus      = number of voltage monitored buses
        rlst.nmvrec      = number of voltage monitored records
        rlst.nmvbusrec   = number of voltage monitored bus records
        rlst.nbus        = number of buses in the case
        rlst.vernum      = .acc file version number
        rlst.ncntlshed   = number of load sheds due to dispatch and contingency
        rlst.ntrplshed   = number of load sheds due to tripping
        rlst.ncactlshed  = number of load sheds due to corrective actions
        rlst.ncactgdisp  = number of generation dispached due to corrective actions
        rlst.ncactphsftr = number of phase shifter changed due to corrective actions
        rlst.nameout     = name out, 0 for number, 1 for name, -1 for undecided
        rlst.filetype    = file type, 0 for accc, 1 for N-1-1
        rlst.nareas      = number of areas
        rlst.nzones      = number of zones
        rlst.nowners     = number of owners
        rlst.nvltlevels  = number of voltage levels
    """
    global _a3c_accfnam
    global _a3c_accfnam_mtime
    global _a3c_accfnam_size
    global _a3c_size
    if accfile:
        accfile = _check_file(name=accfile, ext='acc', desc='ACCC output', type='read')
    if not _samefile(_a3c_accfnam, _a3c_accfnam_size, _a3c_accfnam_mtime, accfile):
        _a3c_accfnam = accfile
        _a3c_accfnam_size = os.path.getsize(_a3c_accfnam)
        _a3c_accfnam_mtime = os.path.getmtime(_a3c_accfnam)
        rlst = pssaccss.accc_size(accfile)
        if not rlst[0]:
            names = list(_ACCC_SIZE_NAM)
            _a3c_size = rlst[1]
            return _a3c_size
        errtxt = ' ERROR=%d Refer PSS(R)E API manual for error description.' % rlst[0]
        _ShowError('accc_size', errtxt)
    else:
        return _a3c_size


def accc_summary(accfile=None):
    """
    rlst = accc_summary(accfile)
    Returns ACCC solution summary.
    Inputs:
        accfile = ACCC output file name (.acc)
    Returned object 'rlst' contains the following attributes:
        rlst.ierr                 = error code (0=no error)
        rlst.acccsize.nmline      = number of monitored branches
        rlst.acccsize.ninter      = number of monitored interfaces
        rlst.acccsize.ncase       = number of contingencies + 1 (for base case)
        rlst.acccsize.nmvbus      = number of voltage monitored buses
        rlst.acccsize.nmvrec      = number of voltage monitored records
        rlst.acccsize.nmvbusrec   = number of voltage monitored bus records
        rlst.acccsize.nbus        = number of buses in the case
        rlst.acccsize.ncntlshed   = number of load sheds due to dispatch and contingency
        rlst.acccsize.ntrplshed   = number of load sheds due to tripping
        rlst.acccsize.ncactlshed  = number of load sheds due to corrective actions
        rlst.acccsize.ncactgdisp  = number of generation dispached due to corrective actions
        rlst.acccsize.ncactphsftr = number of phase shifter changed due to corrective actions
        rlst.acccsize.nameout     = name out, 0 for number, 1 for name, -1 for undecided
        rlst.acccsize.filetype    = file type, 0 for accc, 1 for N-1-1
        rlst.acccsize.nareas      = number of areas
        rlst.acccsize.nzones      = number of zones
        rlst.acccsize.nowners     = number of owners
        rlst.acccsize.nvltlevels  = number of voltage levels
        rlst.casetitle.line1      = short title line 1
        rlst.casetitle.line2      = short title line 2
        rlst.file.acc             = contingency output (.acc) file name
        rlst.file.sav             = saved case (.sav) file name
        rlst.file.dfx             = distribution factor data (.dfx) file name
        rlst.file.sub             = subsystem definition data (.sub) file name
        rlst.file.mon             = monitored element data (.mon) file name
        rlst.file.con             = contingency description data (.con) file name
        rlst.file.thr             = load throwover data (.thr) file name
        rlst.file.inl             = unit inertia and governor data (.inl) file name
        rlst.file.trp             = tripping element data (.trp) file name
        rlst.melement             = monitored branch and interface names
        rlst.rating.a             = rating A
        rlst.rating.b             = rating B
        rlst.rating.c             = rating C
        rlst.mvbuslabel           = monitored voltage bus label
        rlst.mvreclabel           = monitored voltage record label
        rlst.mvrecmax             = monitored bus voltage upper bound (range) or rise (deviation)
        rlst.mvrecmin             = monitored bus voltage lower bound (range) or drop (deviation)
        rlst.mvrectype            = monitored voltage record type (range/deviation)
        rlst.colabel              = contingency labels
        rlst.busname              = extended names of buses in the case
    """
    global _a3c_summary
    if not _samefile(_a3c_accfnam, _a3c_accfnam_size, _a3c_accfnam_mtime, accfile):
        acccsize = _accc_size(accfile)
        rlst = pssaccss.accc_summary(accfile, acccsize)
        if not rlst[0]:
            names = list(_ACCC_SUMMARY_NAM)
            names.insert(0, _ERR_CODE_NAM)
            rlst = list(rlst)
            rlst.insert(1, acccsize)
            rlst = _CaseLessAttributeList(lstnames=names, inlist=rlst)
            acccsize = _CaseLessAttributeList(lstnames=_ACCC_SIZE_NAM, inlist=rlst.acccsize)
            casetitle = _CaseLessAttributeList(lstnames=_SHRT_TITLE_NAM, inlist=rlst.casetitle)
            filemap = _CaseLessAttributeList(lstnames=_ACCC_FILE_NAM, inlist=rlst.file)
            rating = _CaseLessAttributeList(lstnames=_RATING_NAM, inlist=rlst.rating)
            rlst.acccsize = acccsize
            rlst.casetitle = casetitle
            rlst.file = filemap
            rlst.rating = rating
            _a3c_summary = rlst
            return _a3c_summary
        errtxt = ' ERROR=%d Refer PSS(R)E API manual for error description.' % rlst[0]
        _ShowError('accc_summary', errtxt)
    else:
        return _a3c_summary


def accc_solution(accfile=None, colabel=None, stype='contingency', busmsm=0.5, sysmsm=5.0):
    """
    rlst = accc_solution(accfile,colabel,stype,busmsm,sysmsm)
    ACCC solution monitored flows and bus voltages for one contingency.
    Inputs:
        accfile  = ACCC output file name (.acc)
        colabel  = contingency label (to get ACCC solution for)
                   only one contingency label allowed
        stype    = solution type
                   default "contingency"
                   allowed values are: "contingency", "con", "tripping", "trp",
                   "caction", "contingency action" or "cor"
        busmsm   = Bus mismatch tolerance
                   default 0.5 MVA
        sysmsm   = System mismatch tolerance
                   default 5.0 MVA
    Returned object 'rlst' contains the following attributes:
        rlst.ierr      = error code(0=no error)
        rlst.codesc    = contingency description
        rlst.cnvflag   = convergence flag (True when converged)
        rlst.cnvcond   = convergence condition
        rlst.island    = number of islands
        rlst.mvaworst  = worst MVA mismatch
        rlst.mvatotal  = total MVA mismatch
        rlst.volts     = monitored bus voltage (pu)
        rlst.mvaflow   = monitored branch MVA and interface MW flow
                         -> When MVAFLOW>0, it is measured at FROM bus
                         -> When MVAFLOW<0, it is measured at TO bus
                         These FROM and TO bus designations come from monitored element specification,
                         and not from RAW/SAV data.
        rlst.ampflow   = monitored branch ampere flow expressed in MVA for non-transformer branches, and
                         MVA flow for transformer branches. Use this to calculate current loading
                         of non-transformer branches and MVA loading of transformer branches
                         -> ampflow = mvaflow/pu bus volts (bus at which MVAFLOW is measured)
        rlst.lshedbus  = name of the load shed bus
        rlst.loadshed  = load shed (MW), for contingency and tripping solution
                       = rlst.loadshed[0], init load MW for corrective action solution
                       = rlst.loadshed[1], load shed MW for corrective action solution
            Following are available for corrective action solution only.
        rlst.gdispbus  = name of the generation dispatch bus
        rlst.gendisp   = rlst.gendisp[0], initial generation (MW)
                       = rlst.gendisp[1], generation dispatch (MW)
        rlst.phsftr    = name of the phase shifter (from bus - to bus - ckt id)
        rlst.phsftrang = rlst.phsftrang[0], initial phase shifter angle (degrees)
                       = rlst.phsftrang[1], new phase shifter angle (degrees)
    """
    if isinstance(colabel, type([])):
        errtxt = ' One contingency label expected. List provided.'
        _ShowError(_INPUTERROR, errtxt)
    sumry = accc_summary(accfile)
    getwhat, getwhatname, stype = _check_accc_solution_type(stype)
    if getwhat == 1:
        caseaddress = sumry.addcnt
    elif getwhat == 2:
        caseaddress = sumry.addtrp
    else:
        caseaddress = sumry.addcor
    coaddress = _check_contingency_label(colabel, sumry.colabel, caseaddress)
    acccsizelst = [
     sumry.acccsize.nmline,
     sumry.acccsize.ninter,
     sumry.acccsize.ncase,
     sumry.acccsize.nmvbus,
     sumry.acccsize.nmvrec,
     sumry.acccsize.nmvbusrec,
     sumry.acccsize.nbus,
     sumry.acccsize.vernum,
     sumry.acccsize.ncntlshed,
     sumry.acccsize.ntrplshed,
     sumry.acccsize.ncactlshed,
     sumry.acccsize.ncactgdisp,
     sumry.acccsize.ncactphsftr,
     sumry.acccsize.nameout,
     sumry.acccsize.filetype,
     sumry.acccsize.nareas,
     sumry.acccsize.nzones,
     sumry.acccsize.nowners,
     sumry.acccsize.nvltlevels]
    if coaddress:
        rlst = pssaccss.accc_solution(accfile, getwhat, coaddress, busmsm, sysmsm, acccsizelst)
        if not rlst[0]:
            if getwhat == 3:
                names = list(_ACCC_SOLUTION_NAM)
            else:
                names = list(_ACCC_SOLUTION_NAM[:-4])
            names.insert(0, _ERR_CODE_NAM)
            rlst = _CaseLessAttributeList(lstnames=names, inlist=rlst)
            if sumry.acccsize.nmvbus:
                mv_vmag = []
                for i in range(sumry.acccsize.nmvrec):
                    for j in range(sumry.acccsize.nmvbus):
                        k = sumry.mvrec_ivb[i][j]
                        if k == 0:
                            break
                        if k < 0:
                            continue
                        mv_vmag.append(rlst.volts[k - 1])

                rlst.volts = mv_vmag
            if len(rlst.lshedbus):
                lshedbus_nam = [sumry.busname[x - 1] for x in rlst.lshedbus]
                rlst.lshedbus = lshedbus_nam
            if getwhat == 3 and len(rlst.gdispbus):
                gdispbus_nam = [sumry.busname[x - 1] for x in rlst.gdispbus]
                rlst.gdispbus = gdispbus_nam
            return rlst
        errtxt = ' ERROR=%d Refer PSS(R)E API manual for error description.' % rlst[0]
        _ShowError('accc_solution', errtxt)
    else:
        return
    return


def accc_summary_report(accfile=None, rptfile=None):
    """
    ierr = accc_summary_report(accfile,rptfile)
    ACCC solution summary text report.
    Inputs:
        accfile = ACCC output file name (.acc)
        rptfile = report text file name (to write summary report)
                  default "PSS(R)E Report"
    Returns ierr.
        ierr    = 0, no error
    """
    rlst = accc_summary(accfile)
    report = _get_report_file_object(rptfile, process='open')
    ttl_hline = '*' + 55 * ' *' + '\n\n'
    ttl = 30 * ' ' + 'ACCC SOLUTION SUMMARY ' + 40 * ' ' + '\n'
    ttl_file = 30 * ' ' + rlst.file.acc + '\n'
    ttl_time = 30 * ' ' + time.ctime() + '\n\n'
    report(ttl_hline)
    report(ttl)
    report(ttl_file)
    report(ttl_time)
    report(ttl_hline)
    report('%s\n' % rlst.casetitle.line1)
    report('%s\n' % rlst.casetitle.line2)
    report('\n')
    report('ACCC output file             = %s\n' % rlst.file.acc)
    report('Saved Case file              = %s\n' % rlst.file.sav)
    report('DFAX file                    = %s\n' % rlst.file.dfx)
    report('Subsystem file               = %s\n' % rlst.file.sub)
    report('Monitored Element file       = %s\n' % rlst.file.mon)
    report('Contingency Description file = %s\n' % rlst.file.con)
    report('\n')
    report('Number of Monitored Branches                              = %d\n' % rlst.acccsize.nmline)
    report('Number of Monitored Interfaces                            = %d\n' % rlst.acccsize.ninter)
    report('Number of Contingencies+Base Case                         = %d\n' % rlst.acccsize.ncase)
    report('Number of Voltage Monitored Buses                         = %d\n' % rlst.acccsize.nmvbus)
    report('Number of Voltage Monitored Records                       = %d\n' % rlst.acccsize.nmvrec)
    report('Number of Voltage Monitored Bus Records                   = %d\n' % rlst.acccsize.nmvbusrec)
    if rlst.acccsize.nbus:
        report('Number of Buses in the case                               = %d\n' % rlst.acccsize.nbus)
    if rlst.acccsize.ncntlshed:
        report('Number of Loads shed due to post contingency              = %d\n' % rlst.acccsize.ncntlshed)
    if rlst.acccsize.ntrplshed:
        report('Number of Loads shed due to tripping                      = %d\n' % rlst.acccsize.ntrplshed)
    if rlst.acccsize.ncactlshed:
        report('Number of Loads shed due to corrective actions            = %d\n' % rlst.acccsize.ncactlshed)
    if rlst.acccsize.ncactgdisp:
        report('Number of Generations dispached due to corrective actions = %d\n' % rlst.acccsize.ncactgdisp)
    if rlst.acccsize.ncactphsftr:
        report('Number of Phase Shifters changed due to corrective actions= %d\n' % rlst.acccsize.ncactphsftr)
    if rlst.acccsize.nameout in (-1, 0, 1):
        if rlst.acccsize.nameout == -1:
            report("ACCC Results stored in the file are in 'unknown' form\n")
        elif rlst.acccsize.nameout == 1:
            report("ACCC Results stored in the file are in 'Bus Name Output' form\n")
        else:
            report("ACCC Results stored in the file are in 'Bus Number Output' form\n")
    if rlst.acccsize.filetype in (0, 1):
        if rlst.acccsize.filetype == 0:
            report('ACCC Results stored in the file are from ACCC analysis\n')
        else:
            report('ACCC Results stored in the file are from N-1-1 analysis\n')
    if rlst.acccsize.nareas:
        report('Number of Areas for which ACCC results are stored         = %d\n' % rlst.acccsize.nareas)
    if rlst.acccsize.nzones:
        report('Number of Zones for which ACCC results are stored         = %d\n' % rlst.acccsize.nzones)
    if rlst.acccsize.nowners:
        report('Number of Owners for which ACCC results are stored        = %d\n' % rlst.acccsize.nowners)
    if rlst.acccsize.nvltlevels:
        report('Number of Voltage levels for which ACCC results are stored= %d\n' % rlst.acccsize.nvltlevels)
    report('\n')
    if rlst.acccsize.nmline:
        report('Monitored Lines\n')
        spc = len(rlst.melement[0])
        monelm = 'MONITORED ELEMENT'
        monelm = (spc - len(monelm)) / 2 * '-' + monelm
        monelm = monelm + (spc - len(monelm)) * '-'
        txtstr = 27 * ' ' + ' ' + monelm + '   ' + '-RATE A-' + ' ' + '-RATE B-' + ' ' + '-RATE C-\n'
        report(txtstr)
        for i in range(rlst.acccsize.nmline):
            report('  Monitored  Branch   %4d: %s   %8.1f %8.1f %8.1f\n' % (i + 1, rlst.melement[i],
             rlst.rating.a[i], rlst.rating.b[i], rlst.rating.c[i]))

    report('\n')
    if rlst.acccsize.ninter:
        report('Monitored Interfaces\n')
        spc = len(rlst.melement[rlst.acccsize.nmline])
        txtstr = 27 * ' ' + ' ' + spc * ' ' + '   ' + '-RATE A-' + ' ' + '-RATE B-' + ' ' + '-RATE C-\n'
        report(txtstr)
        for i in range(rlst.acccsize.nmline, rlst.acccsize.nmline + rlst.acccsize.ninter):
            report('  Monitored Interface %4d: %s   %8.1f %8.1f %8.1f\n' % (i + 1 - rlst.acccsize.nmline,
             rlst.melement[i], rlst.rating.a[i], rlst.rating.b[i], rlst.rating.c[i]))

    report('\n')
    if rlst.acccsize.nmvbusrec:
        mxlen_mvreclabel = max([len(rlst.mvreclabel[i]) for i in range(rlst.acccsize.nmvbusrec)])
        mxlen_mvbuslabel = max([len(rlst.mvbuslabel[i]) for i in range(rlst.acccsize.nmvbusrec)])
        report('Monitored Buses\n')
        reclbl = '-RECORD-'
        len_reclbl = len(reclbl)
        if len_reclbl < mxlen_mvreclabel:
            l1 = int((mxlen_mvreclabel - len_reclbl) * 0.5)
            l2 = mxlen_mvreclabel - len_reclbl - l1
            reclbl = l1 * '-' + reclbl + l2 * '-'
            len_reclbl = len(reclbl)
        buslbl = '-----BUS-----'
        len_buslbl = len(buslbl)
        if len_buslbl < mxlen_mvbuslabel:
            l1 = int((mxlen_mvbuslabel - len_buslbl) * 0.5)
            l2 = mxlen_mvbuslabel - len_buslbl - l1
            buslbl = l1 * '-' + buslbl + l2 * '-'
            len_buslbl = len(buslbl)
        txtstr = '  ' + '          ' + ' ' + reclbl + ' ' + buslbl + ' ' + '--TYPE---' + ' ' + '-MINIMUM-' + ' ' + '-MAXIMUM-\n'
        report(txtstr)
        for i in range(rlst.acccsize.nmvbusrec):
            spc_mvreclabel = abs(len_reclbl - len(rlst.mvreclabel[i])) * ' '
            spc_mvbuslabel = abs(len_buslbl - len(rlst.mvbuslabel[i])) * ' '
            elmt = 'VMON %4d:' % (i + 1)
            elmt = elmt + (10 - len(elmt)) * ' '
            if rlst.mvrecmin[i] == 0:
                mvrecmin = '         '
            else:
                mvrecmin = '%9.5f' % rlst.mvrecmin[i]
            if rlst.mvrectype[i] == 'RANGE':
                if rlst.mvrecmax[i] == 0 or rlst.mvrecmax[i] <= rlst.mvrecmin[i]:
                    mvrecmax = '         '
                else:
                    mvrecmax = '%9.5f' % rlst.mvrecmax[i]
            else:
                mvrecmax = '%9.5f' % rlst.mvrecmax[i]
            report('  %s %s%s %s%s %9s %s %s\n' % (elmt, rlst.mvreclabel[i], spc_mvreclabel,
             rlst.mvbuslabel[i], spc_mvbuslabel,
             rlst.mvrectype[i], mvrecmin, mvrecmax))

    report('\n')
    if rlst.acccsize.ncase:
        report('ACCC Contingency Labels:\n')
        report("    Note: Contingency labels appended with '+T'  have 'Tripping' solutions.\n")
        report("          Contingency labels appended with '+CA' have 'Corrective Action' solutions.\n")
        j = 1
        if len(rlst.colabel) > 1:
            mxlen_lbl = max([len(x.strip()) for x in rlst.colabel[1:]]) + 5
            if mxlen_lbl < 9:
                mxlen_lbl = 9
        else:
            mxlen_lbl = 9
        for i in range(rlst.acccsize.ncase):
            lbl = '%s' % rlst.colabel[i]
            if rlst.addtrp[i] != 0:
                lbl += '+T'
            if rlst.addcor[i] != 0:
                lbl += '+CA'
            lbl = (mxlen_lbl - len(lbl)) * ' ' + lbl
            report('%s, ' % lbl)
            if j == 7:
                report('\n')
                j = 1
            else:
                j += 1

    else:
        report('No Contingencies..')
    report('\n\n')
    _get_report_file_object(rptfile, process='close', rptdesc='ACCC Summary')
    return rlst.ierr


def accc_solution_report(accfile=None, colabels=None, stype='contingency', busmsm=0.5, sysmsm=5.0, rating='a', rptfile=None):
    """
    ierr = accc_solution_report(accfile,colabels,stype,busmsm,sysmsm,rating,rptfile)
    ACCC solution monitored flows and bus voltages text report.
    Inputs:
        accfile  = ACCC output file name (.acc)
        colabels = contingency labels (to get ACCC solution)
                   default "all contingencies"
                   for more than one contingency, provide as a list or tuple
        stype    = solution type
                   default "contingency"
                   allowed values are: "contingency" or "tripping" or "caction",
        busmsm   = Bus mismatch tolerance
                   default 0.5 MVA
        sysmsm   = System mismatch tolerance
                   default 5.0 MVA
        rating   = rating to calculate percent loading
                   default rating "a"
                   allowed values are: "a" or "b" or "c"
        rptfile  = report text file name (to write solution report)
                   default "PSS(R)E Report"

    Returns ierr.
        ierr     = 0, no error
    """
    sumry = accc_summary(accfile)
    if colabels:
        if isinstance(colabels, type(())):
            colabels = list(colabels)
        if not isinstance(colabels, type([])):
            colabels = [
             colabels]
    else:
        colabels = sumry.colabel
        psspy.progress(' \n     Contingency Labels not provided. All contingencies considered.\n')
    ratename, rate = _check_rate(rating, sumry.rating)
    getwhat, getwhatname, stype = _check_accc_solution_type(stype)
    report = _get_report_file_object(rptfile, process='open')
    tfile_events = tempfile.TemporaryFile()
    tfile_flow = tempfile.TemporaryFile()
    tfile_volts = tempfile.TemporaryFile()
    tfile_lshed = tempfile.TemporaryFile()
    if getwhat == 3:
        tfile_gdisp = tempfile.TemporaryFile()
        tfile_phsftr = tempfile.TemporaryFile()
    ncons = len(colabels)
    counter = 0
    ret_ierr = 0
    for lbl in colabels:
        rlst = accc_solution(accfile, lbl, stype, busmsm, sysmsm)
        if rlst == None:
            continue
        if rlst.ierr != 0:
            ret_ierr = rlst.ierr
        cnvflag = rlst.cnvflag
        cnvcond = rlst.cnvcond
        island = ('%d' % rlst.island).center(7)
        mvaworst = rlst.mvaworst
        mvatotal = rlst.mvatotal
        for jj in range(len(rlst.codesc)):
            desc = rlst.codesc[jj]
            if jj == 0:
                tfile_events.write('%(lbl)s@%(desc)s@%(cnvflag)s@%(cnvcond)s@%(island)s@%(mvaworst)11.4f@%(mvatotal)11.4f\n' % vars())
            else:
                tmp = ' '
                tfile_events.write('%(tmp)s@%(desc)s\n' % vars())

        if cnvflag:
            txtstr = ''
            for jj in range(sumry.acccsize.nmline + sumry.acccsize.ninter):
                mvaflow = '%9.2f' % rlst.mvaflow[jj]
                if jj < sumry.acccsize.nmline:
                    ampflow = '%9.2f' % rlst.ampflow[jj]
                    pctflow = abs(rlst.ampflow[jj])
                else:
                    ampflow = '         '
                    pctflow = abs(rlst.mvaflow[jj])
                if rate[jj]:
                    pctflow = '%6.2f' % (pctflow * 100.0 / rate[jj])
                else:
                    pctflow = '      '
                txtstr += '@%(mvaflow)s@%(ampflow)s@%(pctflow)s ' % vars()

            if txtstr:
                tfile_flow.write('%(lbl)-12s%(txtstr)s\n' % vars())
            if sumry.acccsize.nmvbus:
                txtstr = ''
                for eachv in rlst.volts:
                    txtstr += '@%8.5f' % eachv

                if txtstr:
                    tfile_volts.write('%(lbl)-12s%(txtstr)s\n' % vars())
            if len(rlst.lshedbus):
                for jj in range(len(rlst.lshedbus)):
                    if getwhat == 1 or getwhat == 2:
                        tfile_lshed.write('%25s %10.2f %12s\n' % (rlst.lshedbus[jj], rlst.loadshed[jj], lbl))
                    else:
                        tfile_lshed.write('%25s %10.2f %10.2f %12s\n' % (rlst.lshedbus[jj], rlst.loadshed[0][jj],
                         rlst.loadshed[1][jj], lbl))

            if getwhat == 3 and len(rlst.gdispbus):
                for jj in range(len(rlst.gdispbus)):
                    tfile_gdisp.write('%25s %11.2f %11.2f %12s\n' % (rlst.gdispbus[jj], rlst.gendisp[0][jj],
                     rlst.gendisp[1][jj], lbl))

            if getwhat == 3 and len(rlst.phsftr):
                for jj in range(len(rlst.phsftr)):
                    tfile_phsftr.write('%54s %12.2f %11.2f %12s\n' % (rlst.phsftr[jj], rlst.phsftrang[0][jj],
                     rlst.phsftrang[1][jj], lbl))

        counter += 1
        fract, intgr = math.modf(counter / 10000.0)
        if counter == ncons and ncons > 1000:
            psspy.progress('    Processed last contingency: %d\n' % counter)
        elif not fract:
            psspy.progress('    Processed contingency     : %d\n' % counter)

    cln_lbl = []
    cln_desc = []
    cln_cnvcond = []
    tfile_events.seek(0)
    lines = tfile_events.readlines()
    for line in lines:
        columns = line.split('@')
        cln_lbl.append(columns[0])
        cln_desc.append(columns[1])
        try:
            cln_cnvcond.append(columns[3])
        except IndexError:
            pass

    if cln_lbl:
        mxlen_desc = max([len(x) for x in cln_desc])
        mxlen_cnvcond = max([len(x) for x in cln_cnvcond])
        lbl = '---LABEL----'
        desc = 'EVENTS'
        len_desc = len(desc)
        if len_desc < mxlen_desc:
            l1 = int((mxlen_desc - len_desc) * 0.5)
            l2 = mxlen_desc - len_desc - l1
            desc = l1 * '-' + desc + l2 * '-'
            len_desc = len(desc)
        cnvflag = 'CNVGD'
        cnvcond = 'CONVERGENCE STATE'
        len_cnvcond = len(cnvcond)
        if len_cnvcond < mxlen_cnvcond:
            l1 = int((mxlen_cnvcond - len_cnvcond) * 0.5)
            l2 = mxlen_cnvcond - len_cnvcond - l1
            cnvcond = l1 * '-' + cnvcond + l2 * '-'
            len_cnvcond = len(cnvcond)
        island = 'ISLANDS'
        mvaworst = '-MVAWORST--'
        mvatotal = '-MVATOTAL--'
        header = '%(lbl)s %(desc)s %(cnvflag)s %(cnvcond)s %(island)s %(mvaworst)s %(mvatotal)s\n' % vars()
    else:
        header = 80 * ' '
    ttl_hline = '*' + int(len(header) * 0.5) * ' *' + '\n\n'
    ttl = 30 * ' ' + 'ACCC ' + getwhatname + ' SOLUTION\n'
    ttl_file = 30 * ' ' + sumry.file.acc + '\n'
    ttl_time = 30 * ' ' + time.ctime() + '\n\n'
    report(ttl_hline)
    report(ttl)
    report(ttl_file)
    report(ttl_time)
    report(ttl_hline)
    if not cln_lbl:
        report('    No solutions found\n')
        return
    else:
        report(header)
        for line in lines:
            columns = line.split('@')
            lbl = columns[0]
            desc = columns[1]
            desc_aspc = (len_desc - len(desc)) * ' '
            try:
                cnvflag = columns[2]
                cnvcond = columns[3]
                island = columns[4]
                mvaworst = columns[5]
                mvatotal = columns[6].strip()
                cnvcond_aspc = (len_cnvcond - len(cnvcond)) * ' '
                txtstr = '\n%(lbl)12s %(desc)s%(desc_aspc)s %(cnvflag)-5s %(cnvcond)s%(cnvcond_aspc)s %(island)7s %(mvaworst)11s %(mvatotal)11s\n' % vars()
            except IndexError:
                desc = desc.strip()
                txtstr = '%(lbl)12s %(desc)s%(desc_aspc)s\n' % vars()

            report(txtstr)

        report('\n\n')
        num_mon = sumry.acccsize.nmline + sumry.acccsize.ninter
        num_mon_grp = 4
        txtstr = 48 * '=' + ' MONITORED FLOWS REPORT ' + 48 * '=' + '\n\n'
        report(txtstr)
        for i in range(0, num_mon, num_mon_grp):
            spc = '            '
            txtstr = ''
            for ii in range(num_mon_grp):
                if i + ii + 1 <= num_mon:
                    if i + ii + 1 <= sumry.acccsize.nmline:
                        elmt = '--MONITORED BRANCH ' + str(i + ii + 1)
                    else:
                        elmt = '--INTERFACE ' + str(i + ii + 1 - sumry.acccsize.nmline)
                    txtstr += elmt + (26 - len(elmt)) * '-' + ' '

            txtstr = '%s %s\n' % (spc, txtstr)
            report(txtstr)
            txtstr = ''
            for ii in range(num_mon_grp):
                if i + ii < num_mon:
                    r = '%6.1f' % rate[i + ii]
                    elmt = '-----RATING ' + str(r)
                    txtstr += elmt + (26 - len(elmt)) * '-' + ' '

            txtstr = '%s %s\n' % ('CONTINGENCY-', txtstr)
            report(txtstr)
            lbl = '---LABEL----'
            mvaflow = '-MVAFLOW-'
            ampflow = '-AMPFLOW-'
            pctflow = '--%---'
            txtstr = ''
            for ii in range(num_mon_grp):
                if i + ii + 1 <= num_mon:
                    txtstr += '%(mvaflow)s %(ampflow)s %(pctflow)s ' % vars()

            txtstr = '%(lbl)s %(txtstr)s\n' % vars()
            report(txtstr)
            if i == 0:
                jstrt = 1
            else:
                jstrt = jstp
            jstp = jstrt + num_mon_grp * 3
            if jstp > num_mon * 3 + 1:
                jstp = num_mon * 3 + 1
            tfile_flow.seek(0)
            line = tfile_flow.readline()
            while line:
                columns = line.split('@')
                lbl = '%12s' % columns[0]
                txtstr = ''
                for j in range(jstrt, jstp, 3):
                    if j + 2 == num_mon * 3:
                        txtstr += '%9s %9s %6s' % (columns[j], columns[j + 1], columns[j + 2].strip())
                    else:
                        txtstr += '%9s %9s %6s' % (columns[j], columns[j + 1], columns[j + 2])

                txtstr = '%(lbl)s %(txtstr)s\n' % vars()
                report(txtstr)
                line = tfile_flow.readline()

            report('\n')

        if sumry.acccsize.nmvbus:
            txtstr = 47 * '=' + ' MONITORED VOLTAGE REPORT ' + 47 * '=' + '\n\n'
            report(txtstr)
            num_vmon_grp = 9
            for i in range(0, sumry.acccsize.nmvbusrec, num_vmon_grp):
                lbl = '---LABEL----'
                txtstr = ''
                for ii in range(num_vmon_grp):
                    if i + ii + 1 <= sumry.acccsize.nmvbusrec:
                        elmt = '-VMON ' + str(i + ii + 1)
                        txtstr += elmt + (11 - len(elmt)) * '-' + ' '

                txtstr = '%s %s\n' % (lbl, txtstr)
                report(txtstr)
                if i == 0:
                    jstrt = 1
                else:
                    jstrt = jstp
                jstp = jstrt + num_vmon_grp
                if jstp > sumry.acccsize.nmvbusrec + 1:
                    jstp = sumry.acccsize.nmvbusrec + 1
                tfile_volts.seek(0)
                line = tfile_volts.readline()
                while line:
                    columns = line.split('@')
                    lbl = '%12s' % columns[0]
                    txtstr = ''
                    for j in range(jstrt, jstp):
                        if j == sumry.acccsize.nmvbusrec:
                            txtstr += '%11s ' % columns[j].strip()
                        else:
                            txtstr += '%11s ' % columns[j]

                    txtstr = '%(lbl)s %(txtstr)s\n' % vars()
                    report(txtstr)
                    line = tfile_volts.readline()

                report('\n')

        txtstr = '==============' + ' LOAD SHEDDING REPORT ' + '===============' + '\n\n'
        report(txtstr)
        tfile_lshed.seek(0)
        line = tfile_lshed.readline()
        if line:
            if getwhat == 1 or getwhat == 2:
                report('-----------BUS----------- LDSHED(MW) ---LABEL----\n')
            else:
                report('-----------BUS----------- INITLD(MW) LDSHED(MW) ---LABEL----\n')
        else:
            report('    None\n')
        while line:
            report(line)
            line = tfile_lshed.readline()

        report('\n')
        if getwhat == 3:
            txtstr = '================' + ' GENERATION DISPATCH REPORT ' + '==================' + '\n\n'
            report(txtstr)
            tfile_gdisp.seek(0)
            line = tfile_gdisp.readline()
            if line:
                report('-----------BUS----------- INITGEN(MW) GENDISP(MW) ---LABEL----\n')
            else:
                report('    None\n')
            while line:
                report(line)
                line = tfile_gdisp.readline()

            report('\n')
            txtstr = 32 * '=' + ' PHASE SHIFTER ANGLE REPORT ' + 32 * '=' + '\n\n'
            report(txtstr)
            tfile_phsftr.seek(0)
            line = tfile_phsftr.readline()
            if line:
                report('--------FROM BUS------------------TO BUS------------ID INITANG(deg) NEWANG(deg) ---LABEL----\n')
            else:
                report('    None\n')
            while line:
                report(line)
                line = tfile_phsftr.readline()

            report('\n')
        _get_report_file_object(rptfile, process='close', rptdesc='ACCC ' + getwhatname + ' solution')
        return ret_ierr


def _accc_flow_violations(summary, cnvgrd_labels, mvaflow, ampflow, report, rating='a', flowlimit=100.0):
    ratename, rate = _check_rate(rating, summary.rating)
    flowlimit = _check_flowlimit(flowlimit)
    fviolations = []
    for c in range(len(mvaflow)):
        fvioLst = []
        for f in range(len(mvaflow[0])):
            if f < summary.acccsize.nmline:
                pctflow = abs(ampflow[c][f])
            else:
                pctflow = abs(mvaflow[c][f])
            if rate[f]:
                pctflow = pctflow * 100.0 / rate[f]
            else:
                pctflow = 0
            if pctflow > flowlimit:
                fvio = pctflow
            else:
                fvio = 0
            fvioLst.append(fvio)

        fviolations.append(fvioLst)

    overload_exist = False
    report('Flow Violations > %g%% of rating %s\n' % (flowlimit, rating.upper()))
    if not len(fviolations):
        report('    None\n\n')
        return
    for f in range(len(fviolations[0])):
        cntfvio = [x[f] for x in fviolations]
        nno_fvio = cntfvio.count(0)
        if nno_fvio == len(cntfvio):
            continue
        if not overload_exist:
            overload_exist = True
            report('-------------------MONITORED ELEMENT------------------ -RATING- -MVAFLOW-- -AMPFLOW-- -NVIO- -AVERAGE%- --WORST%-- -WORST CNT--\n')
        melmtlabel = summary.melement[f]
        melmtrate = rate[f]
        worst_oload = max(cntfvio)
        nfvio = len(cntfvio) - nno_fvio
        avg_oload = sum(cntfvio) / nfvio
        idx = cntfvio.index(worst_oload)
        cntworst_oload = cnvgrd_labels[idx]
        melmtmva = abs(mvaflow[idx][f])
        if f < summary.acccsize.nmline:
            melmtamp = abs(ampflow[idx][f])
            melmtamp_str = '%10.1f' % melmtamp
        else:
            melmtamp = 0
            melmtamp_str = '          '
        report('%(melmtlabel)54s %(melmtrate)8.1f %(melmtmva)10.1f %(melmtamp_str)s %(nfvio)6d %(avg_oload)10.1f %(worst_oload)10.1f %(cntworst_oload)12s\n' % vars())

    if not overload_exist:
        report('    None\n')
    report('\n')


def _accc_voltage_violations(summary, cnvgrd_labels, busrecvolt, report):
    """
    print 'busrecvolt'
    for c in range(len(busrecvolt)):
        txtstr = ''
        for r in range(len(busrecvolt[0])):
            txtstr += "%f " % busrecvolt[c][r]
        print txtstr
    """
    vviolations = []
    for c in range(1, len(busrecvolt)):
        vvioLst = []
        for r in range(len(busrecvolt[0])):
            if busrecvolt[c][r] == 0.0:
                vvio = 0
            elif summary.mvrectype[r] == 'RANGE':
                if summary.mvrecmin[r] and busrecvolt[c][r] < summary.mvrecmin[r]:
                    vvio = busrecvolt[c][r] - summary.mvrecmin[r]
                elif summary.mvrecmax[r] and busrecvolt[c][r] > summary.mvrecmax[r]:
                    vvio = busrecvolt[c][r] - summary.mvrecmax[r]
                else:
                    vvio = 0
            else:
                delta = busrecvolt[c][r] - busrecvolt[0][r]
                if delta < 0:
                    if summary.mvrecmin[r] and abs(delta) > summary.mvrecmin[r]:
                        vvio = delta + summary.mvrecmin[r]
                    else:
                        vvio = 0
                elif summary.mvrecmax[r] and delta > summary.mvrecmax[r]:
                    vvio = delta - summary.mvrecmax[r]
                else:
                    vvio = 0
            vvioLst.append(vvio)

        vviolations.append(vvioLst)

    if not len(vviolations):
        report('Voltage Violations\n')
        report('    None\n\n')
        return
    tfile_min_rng_vvio = tempfile.TemporaryFile()
    tfile_min_dev_vvio = tempfile.TemporaryFile()
    tfile_max_rng_vvio = tempfile.TemporaryFile()
    tfile_max_dev_vvio = tempfile.TemporaryFile()
    for r in range(len(vviolations[0])):
        cntvvio = [x[r] for x in vviolations]
        nno_vvio = cntvvio.count(0)
        if nno_vvio == len(cntvvio):
            continue
        mvbuslabel = summary.mvbuslabel[r]
        mvreclabel = summary.mvreclabel[r]
        mvrectype = summary.mvrectype[r]
        if summary.mvrecmin[r]:
            mvrecmin = '%8.5f' % summary.mvrecmin[r]
        else:
            mvrecmin = '   --   '
        if summary.mvrecmax[r]:
            mvrecmax = '%8.5f' % summary.mvrecmax[r]
        else:
            mvrecmax = '   --   '
        mvrecvolts_init = busrecvolt[0][r]
        nminlimit_vvio = len(filter((lambda x: x < 0), cntvvio))
        nmaxlimit_vvio = len(cntvvio) - nminlimit_vvio - nno_vvio
        if nminlimit_vvio:
            worstmin_vvio = min(cntvvio)
            idxmin = cntvvio.index(worstmin_vvio) + 1
            worstmin_vvio = abs(min(cntvvio))
            mvrecvolts = busrecvolt[idxmin][r]
            cntworstmin_vvio = cnvgrd_labels[idxmin]
            minavg_vvio = abs(sum(filter((lambda x: x < 0), cntvvio))) / nminlimit_vvio
            if mvrectype == 'RANGE':
                tfile_min = tfile_min_rng_vvio.write
            else:
                tfile_min = tfile_min_dev_vvio.write
            tfile_min('%(mvbuslabel)25s %(mvreclabel)20s %(mvrectype)9s %(mvrecmin)s %(mvrecvolts_init)8.5f %(mvrecvolts)8.5f %(nminlimit_vvio)6d %(minavg_vvio)8.5f %(worstmin_vvio)8.5f %(cntworstmin_vvio)12s\n' % vars())
        if nmaxlimit_vvio:
            worstmax_vvio = max(cntvvio)
            idxmax = cntvvio.index(worstmax_vvio) + 1
            mvrecvolts = busrecvolt[idxmax][r]
            cntworstmax_vvio = cnvgrd_labels[idxmax]
            maxavg_vvio = abs(sum(filter((lambda x: x > 0), cntvvio))) / nmaxlimit_vvio
            if mvrectype == 'RANGE':
                tfile_max = tfile_max_rng_vvio.write
            else:
                tfile_max = tfile_max_dev_vvio.write
            tfile_max('%(mvbuslabel)25s %(mvreclabel)20s %(mvrectype)9s %(mvrecmax)s %(mvrecvolts_init)8.5f %(mvrecvolts)8.5f %(nmaxlimit_vvio)6d %(maxavg_vvio)8.5f %(worstmax_vvio)8.5f %(cntworstmax_vvio)12s\n' % vars())

    tfile_min_rng_vvio.seek(0)
    report('Low Voltage Range Violations\n')
    line = tfile_min_rng_vvio.readline()
    if not line:
        report('    None\n')
    else:
        report('------MONITORED BUS------ ---MONITOR LABEL---- ---TYPE-- -V MIN-- -V INIT- -V LOW-- -NVIO- AVERAGE- -WORST-- -WORST CNT--\n')
        while line:
            report(line)
            line = tfile_min_rng_vvio.readline()

    report('\n')
    tfile_min_dev_vvio.seek(0)
    report('Low Voltage Deviation Violations\n')
    line = tfile_min_dev_vvio.readline()
    if not line:
        report('    None\n')
    else:
        report('------MONITORED BUS------ ---MONITOR LABEL---- ---TYPE-- -V MIN-- -V INIT- -V LOW-- -NVIO- AVERAGE- -WORST-- -WORST CNT--\n')
        while line:
            report(line)
            line = tfile_min_dev_vvio.readline()

    report('\n')
    tfile_max_rng_vvio.seek(0)
    report('High Voltage Range Violations\n')
    line = tfile_max_rng_vvio.readline()
    if not line:
        report('    None\n')
    else:
        report('------MONITORED BUS------ ---MONITOR LABEL---- ---TYPE-- -V MAX-- -V INIT- -V HIGH- -NVIO- AVERAGE- -WORST-- -WORST CNT--\n')
        while line:
            report(line)
            line = tfile_max_rng_vvio.readline()

    report('\n')
    tfile_max_dev_vvio.seek(0)
    report('High Voltage Deviation Violations\n')
    line = tfile_max_dev_vvio.readline()
    if not line:
        report('    None\n')
    else:
        report('------MONITORED BUS------ ---MONITOR LABEL---- ---TYPE-- -V MAX-- -V INIT- -V HIGH- -NVIO- AVERAGE- -WORST-- -WORST CNT--\n')
        while line:
            report(line)
            line = tfile_max_dev_vvio.readline()

    report('\n')


def _accc_load_curtailment(summary, getwhat, cnvgrd_labels, lshedbus, loadshed, report):
    report('Load Curtailments\n')
    load_curtailment_exists = False
    if not len(lshedbus):
        report('    None\n\n')
        return
    for c in range(len(lshedbus)):
        if load_curtailment_exists:
            break
        for n in range(len(lshedbus[c])):
            if lshedbus[c][n]:
                if getwhat == 1 or getwhat == 2:
                    report('-----------BUS----------- LDSHED(MW)  ---LABEL----\n')
                else:
                    report('-----------BUS----------- INITLD(MW)  LDSHED(MW)  ---LABEL----\n')
                load_curtailment_exists = True
                break

    if not load_curtailment_exists:
        report('    None\n\n')
        return
    spc = '  '
    for c in range(len(lshedbus)):
        for n in range(len(lshedbus[c])):
            lbl = cnvgrd_labels[c]
            if getwhat == 1 or getwhat == 2:
                report('%25s %8.1f %s %12s\n' % (lshedbus[c][n], loadshed[c][n], spc, lbl))
            else:
                report('%25s %8.1f %s %8.1f %s %12s\n' % (lshedbus[c][n], loadshed[c][0][n], spc,
                 loadshed[c][1][n], spc, lbl))

    report('\n')


def _accc_generation_dispatch(summary, getwhat, cnvgrd_labels, gdispbus, gendisp, report):
    if getwhat < 3:
        return
    report('Generation Dispatch\n')
    gen_dispatch_exists = False
    if not len(gdispbus):
        report('    None\n\n')
        return
    for c in range(len(gdispbus)):
        if gen_dispatch_exists:
            break
        for n in range(len(gdispbus[c])):
            if gdispbus[c][n]:
                gen_dispatch_exists = True
                report('-----------BUS----------- INITGEN(MW) GENDISP(MW) ---LABEL----\n')
                break

    if not gen_dispatch_exists:
        report('    None\n\n')
        return
    spc = '  '
    for c in range(len(gdispbus)):
        for n in range(len(gdispbus[c])):
            lbl = cnvgrd_labels[c]
            report('%25s %8.1f %s %8.1f %s %12s\n' % (gdispbus[c][n], gendisp[c][0][n], spc,
             gendisp[c][1][n], spc, lbl))

    report('\n')


def _accc_phase_shifter_angles(summary, getwhat, cnvgrd_labels, phsftr, phsftrang, report):
    if getwhat < 3:
        return
    report('Phase Shifter Angle Adjustements\n')
    phsftrang_exists = False
    if not len(phsftr):
        report('    None\n\n')
        return
    for c in range(len(phsftr)):
        if phsftrang_exists:
            break
        for n in range(len(phsftr[c])):
            if phsftr[c][n]:
                phsftrang_exists = True
                report('--------FROM BUS------------------TO BUS------------ID INITANG(deg) NEWANG(deg) ---LABEL----\n')
                break

    if not phsftrang_exists:
        report('    None\n\n')
        return
    spc = '  '
    for c in range(len(phsftr)):
        for n in range(len(phsftr[c])):
            lbl = cnvgrd_labels[c]
            report('%54s %8.1f %s  %8.1f %s %12s\n' % (phsftr[c][n], phsftrang[c][0][n], spc,
             phsftrang[c][1][0], spc, lbl))

    report('\n')


def accc_violations_report(accfile=None, stype='contingency', busmsm=0.5, sysmsm=5.0, rating='a', flowlimit=100.0, rptfile=None):
    """
    ierr = accc_violations_report(accfile,stype,busmsm,sysmsm,rating,flowlimit,rptfile)
    ACCC solution monitored flows and bus voltages violations text report.
    Inputs:
        accfile  = ACCC output file name (.acc)
        stype    = solution type
                   default "contingency"
                   allowed values are: "contingency", "con", "tripping", "trp"
                   "caction", "contingency action" or "cor"
        busmsm   = Bus mismatch tolerance
                   default 0.5 MVA
        sysmsm   = System mismatch tolerance
                   default 5.0 MVA
        rating   = rating to calculate percent loading
                   default rating "a"
                   allowed values are: "a" or "b" or "c"
        flowlimit= percent of flow rating
                   default 100
        rptfile  = report text file name (to write violations report)
                   default "PSS(R)E Report"

    Returns ierr.
        ierr     = 0, no error
    """
    getwhat, getwhatname, stype = _check_accc_solution_type(stype)
    report = _get_report_file_object(rptfile, process='open')
    summary = accc_summary(accfile)
    cnvgrd_labels, busrecvolt, mvaflow, ampflow, lshedbus, loadshed = ([], [], [], [], [], [])
    if getwhat == 3:
        gdispbus, gendisp, phsftr, phsftrang = ([], [], [], [])
    if getwhat == 1:
        colabels = summary.colabel
    elif len(summary.colabel) == 1:
        t1 = '    ACCC ' + getwhatname + ' VIOLATIONS NOT AVAILABLE FOR BASE CASE.\n'
        report(t1)
        return
    colabels = summary.colabel[1:]
    ret_ierr = 0
    for lbl in colabels:
        rlst = accc_solution(accfile, lbl, stype, busmsm, sysmsm)
        if rlst == None:
            continue
        if rlst.ierr != 0:
            ret_ierr = rlst.ierr
        if rlst.cnvflag:
            cnvgrd_labels.append(lbl)
            busrecvolt.append(rlst.volts)
            mvaflow.append(rlst.mvaflow)
            ampflow.append(rlst.ampflow)
            lshedbus.append(rlst.lshedbus)
            loadshed.append(rlst.loadshed)
            if getwhat == 3:
                gdispbus.append(rlst.gdispbus)
                gendisp.append(rlst.gendisp)
                phsftr.append(rlst.phsftr)
                phsftrang.append(rlst.phsftrang)

    ttl_hline = '*' + 63 * ' *' + '\n\n'
    ttl = 30 * ' ' + 'ACCC ' + getwhatname + ' VIOLATIONS\n'
    ttl_file = 30 * ' ' + summary.file.acc + '\n'
    ttl_time = 30 * ' ' + time.ctime() + '\n\n'
    report(ttl_hline)
    report(ttl)
    report(ttl_file)
    report(ttl_time)
    report(ttl_hline)
    if not len(cnvgrd_labels):
        report('    No converged solutions found\n')
        return
    else:
        _accc_flow_violations(summary, cnvgrd_labels, mvaflow, ampflow, report, rating, flowlimit)
        _accc_voltage_violations(summary, cnvgrd_labels, busrecvolt, report)
        _accc_load_curtailment(summary, getwhat, cnvgrd_labels, lshedbus, loadshed, report)
        if getwhat == 3:
            _accc_generation_dispatch(summary, getwhat, cnvgrd_labels, gdispbus, gendisp, report)
            _accc_phase_shifter_angles(summary, getwhat, cnvgrd_labels, phsftr, phsftrang, report)
        _get_report_file_object(rptfile, process='close', rptdesc='ACCC ' + getwhatname + ' violations')
        return ret_ierr


def ascc_currents(sid=0, all=1, flt3ph=0, fltlg=0, fltllg=0, fltll=0, linout=0, linend=0, voltop=0, genxop=0, tpunty=0, dcload=0, zcorec=1, lnchrg=0, shntop=0, loadop=0, machpq=0, volts=1.0, relfile='', fcdfile='', scfile='nooutput', rprtyp=-1, rprlvl=0):
    """ASCC short circuit currents in three-phase a.c. systems.

robj = ascc_currents(sid,all,flt3ph,fltlg,fltllg,fltll,linout,linend,
                     voltop,genxop,tpunty,dcload,zcorec,lnchrg,shntop,
                     loadop,machpq,volts,relfile,fcdfile,scfile,rprtyp,rprlvl)
Inputs:
    sid     : Valid subsystem identifier
              Range from 0 to 3, must have been previously defined
              = 0 (default)
    all     : Consider "all" buses or selected subsystem
              = 1, process all buses (default)
              = 0, process only buses in subsystem SID
    flt3ph  : Get 3 phase fault currents
              = 1, apply 3 phase faults
              = 0, do not apply 3 phase faults (default)
    fltlg   : Get LG (line to ground) fault currents
              = 1, apply LG faults
              = 0, do not apply LG faults (default)
    fltllg  : Get LLG (two lines to ground) fault currents
              = 1, apply LLG faults
              = 0, do not apply LLG faults (default)
    fltll   : Get LL (line to line) fault currents
              = 1, apply LL faults
              = 0, do not apply LL faults (default)
    linout  : Consider LINE OUT faults
              = 1, apply LINOUT faults
              = 0, do not apply LINOUT faults (default)
    linend  : Consider LINE END faults
              = 1, apply LINEND faults
              = 0, do not apply LINEND faults (default)
    voltop  : Bus Voltage option
              = 0, use bus voltages from power flow solution (default)
              = 1, set all bus voltages at specified value and at 0 deg
              = 2, set faulted bus voltage at specified value and at 0 deg
    genxop  : Synchronous Machine Reactance selection option
              = 0, subtransient (default)
              = 1, transient
              = 2, synchronous
    tpunty  : Transformer Tap Ratios and Phase Shift Angles option
              = 0, leave tap ratios and phase shift angles unchanged (default)
              = 1, set tap ratios to 1.0 pu and phase shift angles to 0 deg.
              = 2, set tap ratios to 1.0 pu and phase shift angles unchanged.
              = 3, set tap ratios unchanged and phase shift angles to 0 deg.
    dcload  : DC Lines and FACTS Devices option
              = 0, block (default)
              = 1, represent as load
    zcorec  : Transformer zero sequence impedance correction option
              = 0, ignore
              = 1, apply (default)
    lnchrg  : Line Charging option
              = 0, leave unchanged (default)
              = 1, set to 0.0 in the positive and negative sequences
              = 2, set to 0.0 in all sequences
    shntop  : Line shunts, Fixed shunts, Switched shunts and
              Transformer Magnetizing Admittance option
              = 0, leave unchanged (default)
              = 1, set to 0.0 in the positive and negative sequences
              = 2, set to 0.0 in all sequences
    loadop  : Load option
              = 0, leave unchanged (default)
              = 1, set to 0.0 in the positive and negative sequences
              = 2, set to 0.0 in all sequences
    machpq  : Synchronous and Asynchronous machines power output option
              = 0, use real and reactive power outputs from power flow solution  (default)
              = 1, set real and reactive power outputs to 0.0
    volts   : User specified bus voltage value in pu. (default = 1.0 pu)
              This is used only when voltop = 1 or 2.
    relfile : Relay output data data file (.iec) (default blank)
    fcdfile : Fault control input data file (.fcd) (default blank)
    scfile  : ASCC results file (.sc) (default='nooutput')
              ='nooutput' to not create SC file 
    rprtyp  : Report option
              =-1, no report (default)
              = 0, fault current summary table
              = 1, total fault currents with Thevenin impedance
              = 2, fault contributions to "N" levels away
              = 3, total fault currents and fault contributions to "N" levels away
    rprlvl  : Number of levels back for contributions report (>=0) (0 by default)
              Used when rprtyp = 2 or 3

Returns 'robj' object. It is a special caseless dictionary object, which can be accessed
     either by dictionary keys or attributes.

    Currents and Impedances returned are complex values.
    I''k is initial symmetrical short circuit current (r.m.s.).
    Index i is the ith fault bus.

    robj.ierr    = error code (0=no error)
    robj.scunit  = Units of returned fault currents
                 = 'pu' or 'physical'
    robj.scfmt   = Co-ordinates of returned fault currents
                 = 'rectangular' or 'polar'
    robj.fltbus  = list of faulted bus numbers

    robj.flt3ph[i].ia1   = three phase fault, Positive Sequence Current = I''k
    robj.flt3ph[i].ia2   = three phase fault, Negative Sequence Current
    robj.flt3ph[i].ia0   = three phase fault, Zero Sequence Current
    robj.flt3ph[i].ia    = three phase fault, Phase A current
    robj.flt3ph[i].ib    = three phase fault, Phase B current
    robj.flt3ph[i].ic    = three phase fault, Phase C current

    robj.fltlg[i].ia1    = line to ground fault, Positive Sequence Current
    robj.fltlg[i].ia2    = line to ground fault, Negative Sequence Current
    robj.fltlg[i].ia0    = line to ground fault, Zero Sequence Current = I''k/3
    robj.fltlg[i].ia     = line to ground fault, Phase A current
    robj.fltlg[i].ib     = line to ground fault, Phase B current
    robj.fltlg[i].ic     = line to ground fault, Phase C current

    robj.fltllg[i].ia1   = line line to ground fault, Positive Sequence Current
    robj.fltllg[i].ia2   = line line to ground fault, Negative Sequence Current
    robj.fltllg[i].ia0   = line line to ground fault, Zero Sequence Current = I''k/3
    robj.fltllg[i].ia    = line line to ground fault, Phase A current
    robj.fltllg[i].ib    = line line to ground fault, Phase B current
    robj.fltllg[i].ic    = line line to ground fault, Phase C current

    robj.fltll[i].ia1    = line to line fault, Positive Sequence Current
    robj.fltll[i].ia2    = line to line fault, Negative Sequence Current
    robj.fltll[i].ia0    = line to line fault, Zero Sequence Current
    robj.fltll[i].ia     = line to line fault, Phase A current
    robj.fltll[i].ib     = line to line fault, Phase B current = I''k
    robj.fltll[i].ic     = line to line fault, Phase C current = -I''k

    robj.thevz[i].z1     = Thevenin impedance, positive sequence, in PU or OHM as set by SCUNIT
    robj.thevz[i].z2     = Thevenin impedance, negative sequence, in PU or OHM as set by SCUNIT
    robj.thevz[i].z0     = Thevenin impedance, zero sequence, in PU or OHM as set by SCUNIT

    robj.thevzpu[i].z1   = PU Thevenin impedance, positive sequence
    robj.thevzpu[i].z2   = PU Thevenin impedance, negative sequence
    robj.thevzpu[i].z0   = PU Thevenin impedance, zero sequence

    robj.maxflt[i].ia1   = Maximum fault current, Positive Sequence Current
    robj.maxflt[i].ia2   = Maximum fault current, Negative Sequence Current
    robj.maxflt[i].ia0   = Maximum fault current, Zero Sequence Current
    robj.maxflt[i].ia    = Maximum fault current, Phase A current
    robj.maxflt[i].ib    = Maximum fault current, Phase B current
    robj.maxflt[i].ic    = Maximum fault current, Phase C current

    robj.maxfltdsc[i]    = Description of fault condition for Maximum fault current

Note 1: Maximum fault current is the largest fault current among analyzed faults at a bus.

Note 2: Any item from robj can be accessed with case insensitive attribute or dictionary key.
So following examples for accessing 'fltbus' are allowed.
    robj.fltbus, robj.fltBus, robj['fltbus'], robj['FLTBUS']
"""
    sid = _check_int_input(sid, 'sid', 0, 11, 3)
    all = _check_int_input(all, 'all', 0, 1, 1)
    flt3ph = _check_int_input(flt3ph, 'flt3ph', 0, 1, 0)
    fltlg = _check_int_input(fltlg, 'fltlg', 0, 1, 0)
    fltllg = _check_int_input(fltllg, 'fltllg', 0, 1, 0)
    fltll = _check_int_input(fltll, 'fltll', 0, 1, 0)
    linout = _check_int_input(linout, 'linout', 0, 1, 0)
    linend = _check_int_input(linend, 'linend', 0, 1, 0)
    voltop = _check_int_input(voltop, 'voltop', 0, 2, 0)
    genxop = _check_int_input(genxop, 'genxop', 0, 2, 0)
    tpunty = _check_int_input(tpunty, 'tpunty', 0, 3, 0)
    dcload = _check_int_input(dcload, 'dcload', 0, 1, 0)
    zcorec = _check_int_input(zcorec, 'zcorec', 0, 1, 1)
    lnchrg = _check_int_input(lnchrg, 'lnchrg', 0, 2, 0)
    shntop = _check_int_input(shntop, 'shntop', 0, 2, 0)
    loadop = _check_int_input(loadop, 'loadop', 0, 2, 0)
    machpq = _check_int_input(machpq, 'machpq', 0, 1, 0)
    rprtyp = _check_int_input(rprtyp, 'rprtyp', -1, 3, -1)
    rprlvl = _check_int_input(rprlvl, 'rprlvl', 0, 99, 0)
    if not (flt3ph or fltlg or fltllg or fltll):
        errtxt = ' Returning .. No faults specified.'
        _ShowError('ascc_currents', errtxt)
    if voltop in (1, 2):
        if type(volts) not in [int, float]:
            errtxt = ' Specified bus voltage is of %s. It must be a value.' % str(type(volts))
            _ShowError('ascc_currents', errtxt)
        if volts <= 0.0:
            errtxt = ' Specified bus voltages to set = %s. It must be greater than zero.' % str(volts)
            _ShowError('ascc_currents', errtxt)
    if fcdfile:
        fcdfile = _check_file(name=fcdfile, ext='fcd', desc='Fault control input data data', type='read')
    ierr, nfbus = pssaccss.ascc_size(sid, all)
    if ierr:
        errtxt = ' ERROR=%d Refer PSS(R)E API manual for error description.' % ierr
        _ShowError('ascc_size', errtxt)
    ierr, ivalunit = psspy.short_circuit_units()
    if ierr:
        errtxt = ' ERROR=%d in psspy.short_circuit_units()' % ierr
        _ShowError('ascc_currents', errtxt)
    ierr, ivalfmt = psspy.short_circuit_coordinates()
    if ierr:
        errtxt = ' ERROR=%d in psspy.short_circuit_coordinates()' % ierr
        _ShowError('ascc_currents', errtxt)
    ierr, fltbus, rlst, rlst_z, rlst_zpu, rlst_max, rlst_maxdsc = pssaccss.ascc_currents(sid, all, flt3ph, fltlg, fltllg, fltll, linout, linend, voltop, genxop, tpunty, dcload, zcorec, lnchrg, shntop, loadop, machpq, volts, relfile, fcdfile, scfile, nfbus, rprtyp, rprlvl)
    if ierr:
        errtxt = ' ERROR=%d Refer PSS(R)E API manual for error description.' % ierr
        _ShowError('ascc_currents', errtxt)
    rlst = _transpose_list(rlst)
    ik3 = []
    ik1 = []
    ik2 = []
    ik2L = []
    for each in rlst:
        cln_bgn = 0
        cln_end = 0
        if flt3ph:
            cln_end += 6
            ik3.append(each[cln_bgn:cln_end])
            cln_bgn += 6
        if fltlg:
            cln_end += 6
            ik1.append(each[cln_bgn:cln_end])
            cln_bgn += 6
        if fltllg:
            cln_end += 6
            ik2.append(each[cln_bgn:cln_end])
            cln_bgn += 6
        if fltll:
            cln_end += 6
            ik2L.append(each[cln_bgn:cln_end])
            cln_bgn += 6

    rlst_z = _transpose_list(rlst_z)
    rlst_zpu = _transpose_list(rlst_zpu)
    rlst_max = _transpose_list(rlst_max)
    del rlst
    rdctobj = _Dict_caseless_bunch({_ERR_CODE_NAM: ierr, _SHORT_CIRCUIT_UNIT: (_SCUNIT[ivalunit]), 
       _SHORT_CIRCUIT_COORDINATES: (_SCFMT[ivalfmt]), 
       _FLT_BUS_NUM: fltbus, 
       (_SC_FAULT_NAM[0]): {}, (_SC_FAULT_NAM[1]): {}, (_SC_FAULT_NAM[2]): {}, (_SC_FAULT_NAM[3]): {}, (_THEVZ_NAM[0]): {}, (_THEVZ_NAM[1]): {}, _SC_FAULT_MAX_I: {}, _SC_FAULT_MAX_I_DSC: {}})
    for flt_exists, fltnam, fltvals in zip([flt3ph, fltlg, fltllg, fltll], _SC_FAULT_NAM[:4], [
     ik3, ik1, ik2, ik2L]):
        if not flt_exists:
            continue
        for i, each in enumerate(fltvals):
            tdct = {}
            for nam, val in zip(_SC_FAULT_CURRENTS_NAM, each):
                tdct[nam] = val

            rdctobj[fltnam][i] = _Dict_caseless_bunch(tdct)

    for znam, zvals in zip(_THEVZ_NAM, [rlst_z, rlst_zpu]):
        for i, each in enumerate(zvals):
            tdct = {}
            for nam, val in zip(_THEVZ_NAM_SEQUENCE, each):
                tdct[nam] = val

            rdctobj[znam][i] = _Dict_caseless_bunch(tdct)

    for i, each in enumerate(rlst_max):
        tdct = {}
        for nam, val in zip(_SC_FAULT_CURRENTS_NAM, each):
            tdct[nam] = val

        rdctobj[_SC_FAULT_MAX_I][i] = _Dict_caseless_bunch(tdct)

    for i, each in enumerate(rlst_maxdsc):
        rdctobj[_SC_FAULT_MAX_I_DSC][i] = each

    try:
        del fltvals
        del zvals
        del each
    except:
        pass

    return rdctobj


def iecs_currents(sid=0, all=1, flt3ph=0, fltlg=0, fltllg=0, fltll=0, fltloc=0, linout=0, linend=0, tpunty=0, lnchrg=1, shntop=1, dcload=0, zcorec=0, optnftrc=0, loadop=1, genxop=0, brktime=0.1, vfactorc=1.1, iecfile='', fcdfile='', scfile='nooutput', rprtyp=-1, rprlvl=0):
    """IEC-60909 short circuit currents in three-phase a.c. systems.

robj = iecs_currents(sid,all,flt3ph,fltlg,fltllg,fltll,fltloc,linout,linend,tpunty,
                     lnchrg,shntop,dcload,zcorec,optnftrc,loadop,genxop,
                     brktime,vfactorc,iecfile,fcdfile,scfile,rprtyp,rprlvl)
Inputs:
    sid     : Valid subsystem identifier
              Range from 0 to 11, must have been previously defined
              = 0 (default)
    all     : Consider "all" buses or selected subsystem
              = 0, process only buses in subsystem SID
              = 1, process all buses (default)
    flt3ph  : Get 3 phase fault currents
              = 0, do not apply 3 phase faults (default)
              = 1, apply 3 phase faults
    fltlg   : Get LG (line to ground) fault currents
              = 0, do not apply LG faults (default)
              = 1, apply LG faults
    fltllg  : Get LLG (two lines to ground) fault currents
              = 0, do not apply LLG faults (default)
              = 1, apply LLG faults
    fltll   : Get LL (line to line) fault currents
              = 0, do not apply LL faults (default)
              = 1, apply LL faults
    fltloc  : Fault location
              = 0, fault at Network bus (default)
              = 1, fault at LV bus of Power Station Unit (PSU)
              = 2, fault at Auxiliary Transformer (connected to PSU) LV Bus
    linout  : Consider LINE OUT faults
              = 0, do not apply LINOUT faults (default)
              = 1, apply LINOUT faults
    linend  : Consider LINE END faults
              = 0, do not apply LINEND faults (default)
              = 1, apply LINEND faults
    tpunty  : Transformer Tap Ratios and Phase Shift Angles option
              = 0, leave tap ratios and phase shift angles unchanged (default)
              = 1, set tap ratios to 1.0 pu and phase shift angles to 0 deg.
              = 2, set tap ratios to 1.0 pu and leave phase shift angles unchanged.
              = 3, leave tap ratios unchanged and set phase shift angles to 0 deg.
    lnchrg  : Line Charging option
              = 0, leave unchanged
              = 1, set to 0.0 in the positive and negative sequences (default)
              = 2, set to 0.0 in all sequences
    shntop  : Line shunts, Fixed shunts, Switched shunts and
              Transformer Magnetizing Admittance option
              = 0, leave unchanged
              = 1, set to 0.0 in the positive and negative sequences (default)
              = 2, set to 0.0 in all sequences
    dcload  : DC Lines and FACTS Devices option
              = 0, block (default)
              = 1, represent as load
    zcorec  : Transformer zero sequence impedance correction option
              = 0, ignore (default)
              = 1, apply
    optnftrc: Voltage Factor C option
              = 0, Voltage Factor C for maximum fault currents (default)
              = 1, Voltage Factor C for minimum fault currents
              = 2, Voltage Factor C as specified by 'vfactorc' value
    loadop  : Load option
              = 0, leave unchanged
              = 1, set to 0.0 in the positive and negative sequences (default)
              = 2, set to 0.0 in all sequences
    genxop   : Synchronous Machine Reactance selection option
              = 0, subtransient (default)
              = 1, transient
              = 2, synchronous
    brktime : Breaker opening time in Seconds
              = 5/BaseFrequency (default)
    vfactorc: User specified Voltage Factor C, no default allowed
              This is used only when optnftrc=2.
    iecfile : IEC input data file (.iec) (default blank)
    fcdfile : Fault control input data file (.fcd) (default blank)
    scfile  : IECS results file (.sc) (default='nooutput')
              ='nooutput' to not create SC file
    rprtyp  : Report Type
              =-1, no report (default)
              = 0, fault current summary table
              = 1, total fault currents with Thevenin impedance
              = 2, fault contributions to "N" levels away
              = 3, total fault currents and fault contributions to "N" levels away
    rprlvl  : Number of levels back for contributions report (>=0) (0 by default)
              Used when rprtyp = 2 or 3

Returns 'robj' object. It is a special caseless dictionary object, which can be accessed
     either by dictionary keys or attributes.

    Currents and Impedances returned are complex values.
    I''k is initial symmetrical short circuit current (r.m.s.).
    Index i is the ith fault bus.

    robj.ierr    = error code (0=no error)
    robj.scunit  = Units of returned fault currents
                 = 'pu' or 'physical'
    robj.scfmt   = Co-ordinates of returned fault currents
                 = 'rectangular' or 'polar'
    robj.fltbus  = list of faulted bus numbers

    robj.flt3ph[i].ia1   = three phase fault, Positive Sequence Current = I''k
    robj.flt3ph[i].ia2   = three phase fault, Negative Sequence Current
    robj.flt3ph[i].ia0   = three phase fault, Zero Sequence Current
    robj.flt3ph[i].ia    = three phase fault, Phase A current
    robj.flt3ph[i].ib    = three phase fault, Phase B current
    robj.flt3ph[i].ic    = three phase fault, Phase C current
    robj.flt3ph[i].ipb   = three phase fault, peak Current - Method B, ip(B)
    robj.flt3ph[i].ipc   = three phase fault, peak Current - Method C, ip(C)
    robj.flt3ph[i].idc   = three phase fault, DC component of asymmetrical breaking current, idc
    robj.flt3ph[i].ibsym = three phase fault, symmetrical breaking current (r.m.s.), ib(sym)
    robj.flt3ph[i].ibuns = three phase fault, asymmetrical breaking current (r.m.s.), ib(uns)

    robj.fltlg[i].ia1    = line to ground fault, Positive Sequence Current
    robj.fltlg[i].ia2    = line to ground fault, Negative Sequence Current
    robj.fltlg[i].ia0    = line to ground fault, Zero Sequence Current = I''k/3
    robj.fltlg[i].ia     = line to ground fault, Phase A current
    robj.fltlg[i].ib     = line to ground fault, Phase B current
    robj.fltlg[i].ic     = line to ground fault, Phase C current
    robj.fltlg[i].ipb    = line to ground fault, peak Current - Method B, ip(B)
    robj.fltlg[i].ipc    = line to ground fault, peak Current - Method C, ip(C)
    robj.fltlg[i].idc    = line to ground fault, DC component of asymmetrical breaking current, idc
    robj.fltlg[i].ibsym  = line to ground fault, symmetrical breaking current (r.m.s.), ib(sym)
    robj.fltlg[i].ibuns  = line to ground fault, asymmetrical breaking current (r.m.s.), ib(uns)

    robj.fltllg[i].ia1   = line line to ground fault, Positive Sequence Current
    robj.fltllg[i].ia2   = line line to ground fault, Negative Sequence Current
    robj.fltllg[i].ia0   = line line to ground fault, Zero Sequence Current = I''k/3
    robj.fltllg[i].ia    = line line to ground fault, Phase A current
    robj.fltllg[i].ib    = line line to ground fault, Phase B current
    robj.fltllg[i].ic    = line line to ground fault, Phase C current
    robj.fltllg[i].ipb   = line line to ground fault, peak Current - Method B, ip(B)
    robj.fltllg[i].ipc   = line line to ground fault, peak Current - Method C, ip(C)
    robj.fltllg[i].idc   = line line to ground fault, DC component of asymmetrical breaking current, idc
    robj.fltllg[i].ibsym = line line to ground fault, symmetrical breaking current (r.m.s.), ib(sym)
    robj.fltllg[i].ibuns = line line to ground fault, asymmetrical breaking current (r.m.s.), ib(uns)

    robj.fltll[i].ia1    = line to line fault, Positive Sequence Current
    robj.fltll[i].ia2    = line to line fault, Negative Sequence Current
    robj.fltll[i].ia0    = line to line fault, Zero Sequence Current
    robj.fltll[i].ia     = line to line fault, Phase A current
    robj.fltll[i].ib     = line to line fault, Phase B current = I''k
    robj.fltll[i].ic     = line to line fault, Phase C current = -I''k
    robj.fltll[i].ipb    = line to line fault, peak Current - Method B, ip(B)
    robj.fltll[i].ipc    = line to line fault, peak Current - Method C, ip(C)
    robj.fltll[i].idc    = line to line fault, DC component of asymmetrical breaking current, idc
    robj.fltll[i].ibsym  = line to line fault, symmetrical breaking current (r.m.s.), ib(sym)
    robj.fltll[i].ibuns  = line to line fault, asymmetrical breaking current (r.m.s.), ib(uns)

    robj.thevz[i].z1     = Thevenin impedance, positive sequence, in PU or OHM as set by SCUNIT
    robj.thevz[i].z2     = Thevenin impedance, negative sequence, in PU or OHM as set by SCUNIT
    robj.thevz[i].z0     = Thevenin impedance, zero sequence, in PU or OHM as set by SCUNIT

    robj.thevzpu[i].z1   = PU Thevenin impedance, positive sequence
    robj.thevzpu[i].z2   = PU Thevenin impedance, negative sequence
    robj.thevzpu[i].z0   = PU Thevenin impedance, zero sequence

    robj.maxflt[i].ia1   = Maximum fault current, Positive Sequence Current
    robj.maxflt[i].ia2   = Maximum fault current, Negative Sequence Current
    robj.maxflt[i].ia0   = Maximum fault current, Zero Sequence Current
    robj.maxflt[i].ia    = Maximum fault current, Phase A current
    robj.maxflt[i].ib    = Maximum fault current, Phase B current
    robj.maxflt[i].ic    = Maximum fault current, Phase C current

    robj.maxfltdsc[i]    = Description of fault condition for Maximum fault current

Note 1: Maximum fault current is the largest fault current among analyzed faults at a bus.

Note 2: Any item from robj can be accessed with case insensitive attribute or dictionary key.
So following examples for accessing 'fltbus' are allowed.
    robj.fltbus, robj.fltBus, robj['fltbus'], robj['FLTBUS']
"""
    sid = _check_int_input(sid, 'sid', 0, 11, 0)
    all = _check_int_input(all, 'all', 0, 1, 1)
    flt3ph = _check_int_input(flt3ph, 'flt3ph', 0, 1, 0)
    fltlg = _check_int_input(fltlg, 'fltlg', 0, 1, 0)
    fltllg = _check_int_input(fltllg, 'fltllg', 0, 1, 0)
    fltll = _check_int_input(fltll, 'fltll', 0, 1, 0)
    fltloc = _check_int_input(fltloc, 'fltloc', 0, 2, 0)
    linout = _check_int_input(linout, 'linout', 0, 1, 0)
    linend = _check_int_input(linend, 'linend', 0, 1, 0)
    tpunty = _check_int_input(tpunty, 'tpunty', 0, 3, 0)
    lnchrg = _check_int_input(lnchrg, 'lnchrg', 0, 2, 1)
    shntop = _check_int_input(shntop, 'shntop', 0, 2, 1)
    dcload = _check_int_input(dcload, 'dcload', 0, 1, 0)
    zcorec = _check_int_input(zcorec, 'zcorec', 0, 1, 0)
    optnftrc = _check_int_input(optnftrc, 'optnftrc', 0, 2, 0)
    loadop = _check_int_input(loadop, 'loadop', 0, 2, 1)
    genxop = _check_int_input(genxop, 'genxop', 0, 2, 0)
    rprtyp = _check_int_input(rprtyp, 'rprtyp', -1, 3, -1)
    rprlvl = _check_int_input(rprlvl, 'rprlvl', 0, 99, 0)
    if not (flt3ph or fltlg or fltllg or fltll):
        errtxt = ' Returning .. No faults specified.'
        _ShowError('iecs_currents', errtxt)
    try:
        ierr, basefq = psspy.base_frequency()
        if ierr == 0:
            defbrktim = 5.0 / basefq
        else:
            defbrktim = 0.1
    except:
        defbrktim = 0.1

    brktime = _check_float_input(brktime, 'brktime', 0.0, 1.0, defbrktim)
    if optnftrc == 2:
        if type(vfactorc) not in [int, float]:
            errtxt = ' Specified Voltage Factor C is of %s. It must be a value.' % str(type(vfactorc))
            _ShowError('iecs_currents', errtxt)
        if vfactorc <= 0.0:
            errtxt = ' Specified Voltage Factor C = %s. It must be greater than zero.' % str(vfactorc)
            _ShowError('iecs_currents', errtxt)
    if iecfile:
        iecfile = _check_file(name=iecfile, ext='iec', desc='IEC input data', type='read')
    if fcdfile:
        fcdfile = _check_file(name=fcdfile, ext='fcd', desc='Fault control input data data', type='read')
    ierr, nfbus = pssaccss.iecs_size(sid, all)
    if ierr:
        errtxt = ' ERROR=%d Refer PSS(R)E API manual for error description.' % ierr
        _ShowError('iecs_size', errtxt)
    ierr, ivalunit = psspy.short_circuit_units()
    if ierr:
        errtxt = ' ERROR=%d in psspy.short_circuit_units()' % ierr
        _ShowError('iecs_currents', errtxt)
    ierr, ivalfmt = psspy.short_circuit_coordinates()
    if ierr:
        errtxt = ' ERROR=%d in psspy.short_circuit_coordinates()' % ierr
        _ShowError('iecs_currents', errtxt)
    ierr, fltbus, rlst, rlst_z, rlst_zpu, rlst_max, rlst_maxdsc = pssaccss.iecs_currents(sid, all, flt3ph, fltlg, fltllg, fltll, fltloc, linout, linend, tpunty, lnchrg, shntop, dcload, zcorec, optnftrc, loadop, genxop, brktime, vfactorc, iecfile, fcdfile, scfile, nfbus, rprtyp, rprlvl)
    if ierr:
        errtxt = ' ERROR=%d Refer PSS(R)E API manual for error description.' % ierr
        _ShowError('iecs_currents', errtxt)
    rlst = _transpose_list(rlst)
    ik3 = []
    ik1 = []
    ik2 = []
    ik2L = []
    for each in rlst:
        cln_bgn = 0
        cln_end = 0
        if flt3ph:
            cln_end += 11
            ik3.append(each[cln_bgn:cln_end])
            cln_bgn += 11
        if fltlg:
            cln_end += 11
            ik1.append(each[cln_bgn:cln_end])
            cln_bgn += 11
        if fltllg:
            cln_end += 11
            ik2.append(each[cln_bgn:cln_end])
            cln_bgn += 11
        if fltll:
            cln_end += 11
            ik2L.append(each[cln_bgn:cln_end])
            cln_bgn += 11

    rlst_z = _transpose_list(rlst_z)
    rlst_zpu = _transpose_list(rlst_zpu)
    rlst_max = _transpose_list(rlst_max)
    del rlst
    rdctobj = _Dict_caseless_bunch({_ERR_CODE_NAM: ierr, _SHORT_CIRCUIT_UNIT: (_SCUNIT[ivalunit]), 
       _SHORT_CIRCUIT_COORDINATES: (_SCFMT[ivalfmt]), 
       _FLT_BUS_NUM: fltbus, 
       (_SC_FAULT_NAM[0]): {}, (_SC_FAULT_NAM[1]): {}, (_SC_FAULT_NAM[2]): {}, (_SC_FAULT_NAM[3]): {}, (_THEVZ_NAM[0]): {}, (_THEVZ_NAM[1]): {}, _SC_FAULT_MAX_I: {}, _SC_FAULT_MAX_I_DSC: {}})
    for flt_exists, fltnam, fltvals in zip([flt3ph, fltlg, fltllg, fltll], _SC_FAULT_NAM[:4], [
     ik3, ik1, ik2, ik2L]):
        if not flt_exists:
            continue
        for i, each in enumerate(fltvals):
            tdct = {}
            for nam, val in zip(_IECS_CURRENTS_NAM, each):
                tdct[nam] = val

            rdctobj[fltnam][i] = _Dict_caseless_bunch(tdct)

    for znam, zvals in zip(_THEVZ_NAM, [rlst_z, rlst_zpu]):
        for i, each in enumerate(zvals):
            tdct = {}
            for nam, val in zip(_THEVZ_NAM_SEQUENCE, each):
                tdct[nam] = val

            rdctobj[znam][i] = _Dict_caseless_bunch(tdct)

    for i, each in enumerate(rlst_max):
        tdct = {}
        for nam, val in zip(_SC_FAULT_CURRENTS_NAM, each):
            tdct[nam] = val

        rdctobj[_SC_FAULT_MAX_I][i] = _Dict_caseless_bunch(tdct)

    for i, each in enumerate(rlst_maxdsc):
        rdctobj[_SC_FAULT_MAX_I_DSC][i] = each

    try:
        del fltvals
        del zvals
        del each
    except:
        pass

    return rdctobj


def otdf_factors(dfxfile=None):
    """This function is obsolete. Replaced by DFAX_PP object.
    Get help as:
        help(pssarrays.DFAX_PP)
    Create dfx object and get otdf factors as below:
        dfxobj = pssarrays.DFAX_PP(dfxfile)
        otdfobj = dfxobj.otdf_factors()
    """
    msg = 'otdf_factors(..) function is obsolete. Replaced by DFAX_PP object.\n    Get help as:\n        help(pssarrays.DFAX_PP)\n    Create dfx object and get otdf factors as below:\n        dfxobj = pssarrays.DFAX_PP(dfxfile)\n        otdfobj = dfxobj.otdf_factors()\n'
    print msg


def _pv_size(pvfile=None):
    """
    rlst = pv_size(pvfile)
    Returns PV analysis array sizes.
    Inputs:
        pvfile  = PV output file name (.pv)
    Returned object 'rlst' contains the following attributes:
        See pv_summary for returned values.
    """
    global _ppv_pvfnam
    global _ppv_pvfnam_mtime
    global _ppv_pvfnam_size
    global _ppv_size
    if pvfile:
        pvfile = _check_file(name=pvfile, ext='pv', desc='PV output', type='read')
    _ppv_pvfnam = pvfile
    _ppv_pvfnam_size = os.path.getsize(_ppv_pvfnam)
    _ppv_pvfnam_mtime = os.path.getmtime(_ppv_pvfnam)
    rlst = pssaccss.pv_size(pvfile)
    if rlst[0]:
        _ppv_size = None
        errtxt = ' ERROR=%d Refer PSS(R)E API manual for error description.' % rlst[0]
        _ShowError('pv_size', errtxt)
    _ppv_size = []
    _ppv_size.append(rlst[1])
    _ppv_size.append(rlst[2])
    _ppv_size.append(rlst[3])
    _ppv_size.append(rlst[4])
    _ppv_size.append(rlst[5])
    _ppv_size.append(rlst[6])
    _ppv_size.append(rlst[7])
    _ppv_size.append(rlst[8])
    return _ppv_size


def pv_summary(pvfile=None):
    """
    rlst = pv_summary(pvfile)
    Returns PV analysis summary.
    Inputs:
        pvfile = PV output file name (.pv)
    Returned object 'rlst' contains the following attributes:
        rlst.ierr                = error code (0=no error)
        rlst.pvsize.ncase        = number of contingencies + 1 (for base case)
        rlst.pvsize.nmline       = number of monitored branches
        rlst.pvsize.ninter       = number of monitored interfaces
        rlst.pvsize.nmvbus       = number of voltage monitored buses
        rlst.pvsize.nmvrec       = number of voltage monitored records
        rlst.pvsize.nmgnbus      = number of monitored plant (generator) buses
        rlst.pvsize.nmldbus      = number of monitored load buses
        rlst.pvsize.nmxtrns      = maximum number of MW transfer changes
        rlst.options             = PV solution options (same as in API manual)
        rlst.values              = PV solution values (same as in API manual)
        rlst.brnflowunits.xfrcur = PV solution transformer branch flow units ('mbrnamp' in pv_solution return list)
        rlst.brnflowunits.nxfrcr = PV solution non-transformer branch flow units ('mbrnamp' in pv_solution return list)
        rlst.casetitle.line1     = short title line 1
        rlst.casetitle.line2     = short title line 2
        rlst.file.pv             = contingency output (.acc) file name
        rlst.file.sav            = saved case (.sav) file name
        rlst.file.ecd            = economic dispatch data (.ecd) file name
        rlst.file.thr            = load throwover data (.thr) file name
        rlst.file.dfx            = distribution factor data (.dfx) file name
        rlst.file.sub            = subsystem definition data (.sub) file name
        rlst.file.mon            = monitored element data (.mon) file name
        rlst.file.con            = contingency description data (.con) file name
        rlst.file.inl            = inertia and governor response data (.inl) file name
        rlst.file.zip            = incremental Save case archive (.zip) file name
        rlst.srcsink             = source and sink subsystem names
        rlst.mbranch             = monitored branch names
        rlst.mbrnrating.a        = rating A
        rlst.mbrnrating.b        = rating B
        rlst.mbrnrating.c        = rating C
        rlst.minterface          = monitored interface names
        rlst.mitfrating          = selected rating of monitored interface
        rlst.mgenbus             = monitored plant (generator) bus label
        rlst.mloadbus            = monitored load bus label
        rlst.mvbuslabel          = monitored voltage bus label
        rlst.mvreclabel          = monitored voltage record label
        rlst.mvrecmax            = monitored voltage bus maximum
        rlst.mvrecmin            = monitored voltage bus minimum
        rlst.mvrectype           = monitored voltage record type (range/deviation)
        rlst.colabel             = contingency labels
        rlst.codesc              = contingency description
        rlst.maxmw               = maximum MW transfer
        rlst.minmw               = minimum MW transfer
    """
    global _do_pv_after_qv
    global _do_qv_after_pv
    global _ppv_summary
    if _samefile(_ppv_pvfnam, _ppv_pvfnam_size, _ppv_pvfnam_mtime, pvfile) and not _do_pv_after_qv:
        if _validate_previous_results(_ppv_size, _ppv_summary):
            return _ppv_summary
    _do_pv_after_qv = False
    _do_qv_after_pv = True
    pvsize_rlst = _pv_size(pvfile)
    pvsize = pvsize_rlst[0]
    pvcntlbl = pvsize_rlst[1]
    pvcntdsc = pvsize_rlst[2]
    pvmaxmw = pvsize_rlst[3]
    pvminmw = pvsize_rlst[4]
    pvcntadr = pvsize_rlst[5]
    pvcntntrns = pvsize_rlst[6]
    pvcntnegi = pvsize_rlst[7]
    rlst = pssaccss.pv_summary(pvfile, pvsize)
    if rlst[0]:
        _ppv_summary = None
        errtxt = ' ERROR=%d Refer PSS(R)E API manual for error description.' % rlst[0]
        _ShowError('pv_summary', errtxt)
    rlst = list(rlst)
    bflow_tmp = rlst.pop(2)
    brnflowunits = []
    for each in bflow_tmp:
        if each == 1:
            brnflowunits.append('AMP')
        else:
            brnflowunits.append('MVA')

    rlst.insert(2, brnflowunits)
    rlst.insert(1, pvsize)
    names = list(_PV_SUMMARY_NAM)
    names.insert(0, _ERR_CODE_NAM)
    rlst.append(pvcntlbl)
    rlst.append(pvcntdsc)
    rlst.append(pvmaxmw)
    rlst.append(pvminmw)
    rlst.append(pvcntadr)
    rlst.append(pvcntntrns)
    rlst.append(pvcntnegi)
    rlst = _CaseLessAttributeList(lstnames=names, inlist=rlst)
    pvsize = _CaseLessAttributeList(lstnames=_PV_SIZE_NAM, inlist=rlst.pvsize)
    brnflowunits = _CaseLessAttributeList(lstnames=_ACCC_BRNFLOW_UNITS_NAM, inlist=rlst.brnflowunits)
    casetitle = _CaseLessAttributeList(lstnames=_SHRT_TITLE_NAM, inlist=rlst.casetitle)
    filemap = _CaseLessAttributeList(lstnames=_PV_FILE_NAM, inlist=rlst.file)
    mbrnrating = _CaseLessAttributeList(lstnames=_RATING_NAM, inlist=rlst.mbrnrating)
    mitfrating = _CaseLessAttributeList(lstnames=_RATING_NAM, inlist=rlst.mitfrating)
    rlst.pvsize = pvsize
    rlst.brnflowunits = brnflowunits
    rlst.casetitle = casetitle
    rlst.file = filemap
    rlst.mbrnrating = mbrnrating
    rlst.mitfrating = mitfrating
    codesc = []
    for i in range(pvsize.ncase):
        dsc = _remove_extra_spaces(rlst.codesc[i])
        codesc.append(dsc)

    rlst.codesc = codesc
    _ppv_summary = rlst
    return _ppv_summary


def pv_solution(pvfile=None, colabel=None):
    """
    rlst = pv_solution(pvfile,colabel)
    PV analysis monitored flows and bus voltages for one contingency.
    Inputs:
        pvfile  = PV output file name (.pv)
        colabel = contingency label (to get PV solution for)
                  only one contingency label allowed
    Returned object 'rlst' contains the following attributes:
        rlst.ierr       = error code(0=no error)
        rlst.island     = number of islands, integer
        rlst.mwtransfer = MW transactions, float of length [ntrans]
        rlst.cnvflag    = convergence flag (True when converged), logical of length [ntrans]
        rlst.cnvcond    = convergence condition
        rlst.mvaworst   = larget bus MVA mismatch, float of length [ntrans]
        rlst.mvatotal   = total system MVA mismatch, float of length [ntrans]
        rlst.volts      = monitored bus voltage (pu), float of length [nmvbus][ntrans]
        rlst.mgenmw     = monitored plant MW, float of length [nmgnbus][ntrans]
        rlst.mgenmvar   = monitored plant MVAR, float of length [nmgnbus][ntrans]
        rlst.mloadmw    = monitored load MW, float of length [nmldbus][ntrans]
        rlst.mloadmvar  = monitored load MVAR, float of length [nmldbus][ntrans]
        rlst.mbrnmva    = monitored branch MVA flow (MVA), float of length [nmline][ntrans]
        rlst.mbrnamp    = monitored branch flow, AMPS expressed in MVA or MVA, float of length [nmline][ntrans]
                          The "brnflowunits" variable in pv_summary determine the units.
                          Use this value to calculate branch loadings.
         rlst.mitfmw   = monitored interface MW flow (MW), float of length [ninter][ntrans]

        where
        ntrans  = number of MW transfer changes
        nmvbus  = number of voltage monitored buses
        nmgnbus = number of monitored plant (generator) buses
        nmldbus = number of monitored load buses
        nmline  = number of monitored branches
        ninter  = number of monitored interfaces
    """
    if isinstance(colabel, type([])):
        errtxt = ' One contingency label expected. List provided.'
        _ShowError(_INPUTERROR, errtxt)
    sumry = pv_summary(pvfile)
    coaddress = _check_contingency_label(colabel, sumry.colabel, sumry.cntadr)
    if not coaddress:
        return
    else:
        pvsizelst = []
        for nam in _PV_SIZE_NAM:
            pvsizelst.append(getattr(sumry.pvsize, nam))

        idx = list(sumry.cntadr).index(coaddress)
        pvntrns = sumry.cntntrns[idx]
        pvnegi = sumry.cntnegi[idx]
        rlst = pssaccss.pv_solution(pvfile, pvsizelst, coaddress, pvntrns, pvnegi)
        if rlst[0]:
            errtxt = ' ERROR=%d Refer PSS(R)E API manual for error description.' % rlst[0]
            _ShowError('pv_solution', errtxt)
        names = list(_PV_SOLUTION_NAM)
        names.insert(0, _ERR_CODE_NAM)
        rlst = _CaseLessAttributeList(lstnames=names, inlist=rlst)
        if sumry.pvsize.vernum <= 0:
            rlst.mloadmw = None
            rlst.mloadmvar = None
        return rlst


def pv_summary_report(pvfile=None, rptfile=None):
    """
    ierr = pv_summary_report(pvfile,rptfile)
    PV analysis summary text report.
    Inputs:
        pvfile  = PV output file name (.pv)
        rptfile = report text file name (to write summary report)
                  default "PSS(R)E Report"
    Returns ierr.
        ierr    = 0, no error
    """
    smry = pv_summary(pvfile)
    report = _get_report_file_object(rptfile, process='open')
    ttl_hline = '*' + 46 * ' *' + '\n\n'
    ttl = 30 * ' ' + 'PV SOLUTION SUMMARY ' + '\n'
    ttl_file = 30 * ' ' + smry.file.pv + '\n'
    ttl_time = 30 * ' ' + time.ctime() + '\n\n'
    report(ttl_hline)
    report(ttl)
    report(ttl_file)
    report(ttl_time)
    report(ttl_hline)
    report('%s\n' % smry.casetitle.line1)
    report('%s\n' % smry.casetitle.line2)
    report('\n')
    report('PV output file                     = %s\n' % smry.file.pv)
    report('Saved Case file                    = %s\n' % smry.file.sav)
    if smry.file.ecd:
        report('Economic dispatch file             = %s\n' % smry.file.ecd)
    if smry.file.thr:
        report('Load throwover file                = %s\n' % smry.file.thr)
    report('DFAX file                          = %s\n' % smry.file.dfx)
    report('Subsystem file                     = %s\n' % smry.file.sub)
    report('Monitored Element file             = %s\n' % smry.file.mon)
    report('Contingency Description file       = %s\n' % smry.file.con)
    if smry.file.inl:
        report('Inertia and Governor Response file = %s\n' % smry.file.inl)
    if smry.file.zip:
        report('Incremental Save Case Archive file = %s\n' % smry.file.zip)
    report('\n')
    report('PV Solution Options:\n')
    for i in range(len(smry.options)):
        j = smry.options[i]
        ti = str(i + 1).rjust(2)
        tj = str(j)
        t1 = _PV_INT_OPTIONS_NAMES[i]
        try:
            t2 = _PV_INT_OPTIONS_LIST[i][j]
        except:
            t2 = 'value undefined at i=%d, j=%d' % (i + 1, j + 1)

        report('option(%(ti)s): %(t1)s =%(tj)s =%(t2)s\n' % vars())

    report('\n')
    report('PV Solution Values:\n')
    for i in range(len(smry.values)):
        ti = str(i + 1)
        tn = _PV_REAL_VALUES_NAMES[i]
        tv = '%g' % smry.values[i]
        report('value(%(ti)s): %(tn)s =%(tv)s\n' % vars())

    report('\n')
    report('Study    (source) subsystem = %s\n' % smry.srcsink[0])
    report('Opposing (sink)   subsystem = %s\n' % smry.srcsink[1])
    if smry.srcsink[2]:
        report('Dispatch          subsystem = %s\n' % smry.srcsink[2])
    else:
        report('Dispatch          subsystem = %s\n' % 'None')
    report('\n')
    report('Number of Contingencies+Base Case     = %d\n' % smry.pvsize.ncase)
    report('Number of Monitored Branches          = %d\n' % smry.pvsize.nmline)
    report('Number of Monitored Interfaces        = %d\n' % smry.pvsize.ninter)
    report('Number of Monitored Generators(Plants)= %d\n' % smry.pvsize.nmgnbus)
    report('Number of Monitored Loads             = %d\n' % smry.pvsize.nmldbus)
    report('Number of Voltage Monitored Buses     = %d\n' % smry.pvsize.nmvbus)
    report('Number of Voltage Monitored Records   = %d\n' % smry.pvsize.nmvrec)
    report('\n')
    if smry.pvsize.nmline:
        w_column1 = len(str(smry.pvsize.nmline)) + 1
        w_column2 = max([len(each) for each in smry.mbranch])
        w_rat = 8
        report('Monitored Branches\n')
        srnum = ' ' * w_column1
        nam = ('NAME').center(w_column2)
        rata = ('RATING A').rjust(w_rat)
        ratb = ('RATING B').rjust(w_rat)
        ratc = ('RATING C').rjust(w_rat)
        report('%(srnum)s %(nam)s %(rata)s %(ratb)s %(ratc)s\n' % vars())
        for i in range(smry.pvsize.nmline):
            srnum = (str(i + 1) + ':').rjust(w_column1)
            nam = smry.mbranch[i].ljust(w_column2)
            rata = '%8.2f' % smry.mbrnrating.a[i]
            ratb = '%8.2f' % smry.mbrnrating.b[i]
            ratc = '%8.2f' % smry.mbrnrating.c[i]
            report('%(srnum)s %(nam)s %(rata)s %(ratb)s %(ratc)s\n' % vars())

        report('\n')
    if smry.pvsize.ninter:
        w_column1 = len(str(smry.pvsize.ninter)) + 1
        w_column2 = max([len(each) for each in smry.minterface])
        w_rat = 8
        report('Monitored Interfaces\n')
        srnum = ' ' * w_column1
        nam = ('NAME').center(w_column2)
        rata = ('RATING A').rjust(w_rat)
        ratb = ('RATING B').rjust(w_rat)
        ratc = ('RATING C').rjust(w_rat)
        report('%(srnum)s %(nam)s %(rata)s %(ratb)s %(ratc)s\n' % vars())
        for i in range(smry.pvsize.ninter):
            srnum = (str(i + 1) + ':').rjust(w_column1)
            nam = smry.minterface[i].ljust(w_column2)
            rata = '%8.2f' % smry.mitfrating.a[i]
            ratb = '%8.2f' % smry.mitfrating.b[i]
            ratc = '%8.2f' % smry.mitfrating.c[i]
            report('%(srnum)s %(nam)s %(rata)s %(ratb)s %(ratc)s\n' % vars())

        report('\n')
    if smry.pvsize.nmgnbus:
        w_column1 = len(str(smry.pvsize.nmgnbus)) + 1
        w_column2 = max([len(each) for each in smry.mgenbus])
        report('Monitored Plants (Generators)\n')
        for i in range(smry.pvsize.nmgnbus):
            srnum = (str(i + 1) + ':').rjust(w_column1)
            nam = smry.mgenbus[i].ljust(w_column2)
            report('%(srnum)s %(nam)s\n' % vars())

        report('\n')
    if smry.pvsize.nmldbus:
        w_column1 = len(str(smry.pvsize.nmldbus)) + 1
        w_column2 = max([len(each) for each in smry.mloadbus])
        report('Monitored Loads\n')
        for i in range(smry.pvsize.nmldbus):
            srnum = (str(i + 1) + ':').rjust(w_column1)
            nam = smry.mloadbus[i].ljust(w_column2)
            report('%(srnum)s %(nam)s\n' % vars())

        report('\n')
    if smry.pvsize.nmvbus:
        w_column1 = len(str(smry.pvsize.nmvbus)) + 1
        w_column2 = max([len(each) for each in smry.mvbuslabel])
        report('Monitored Buses\n')
        for i in range(smry.pvsize.nmvbus):
            srnum = (str(i + 1) + ':').rjust(w_column1)
            nam = smry.mvbuslabel[i].ljust(w_column2)
            report('%(srnum)s %(nam)s\n' % vars())

        report('\n')
    if smry.pvsize.ncase:
        w_column1 = len(str(smry.pvsize.ncase)) + 1
        w_column2 = max([len(each) for each in smry.colabel])
        w_mxmw = 8
        if w_column2 < 5:
            w_column2 = 5
        report('PV Contingencies\n')
        srnum = ' ' * w_column1
        nam = ('LABEL').ljust(w_column2)
        mxmw = ('MaxMW').rjust(w_mxmw)
        dsc = 'DESCRIPTION'
        report('%(srnum)s %(nam)s %(mxmw)s %(dsc)s\n' % vars())
        for i in range(smry.pvsize.ncase):
            if i == 0:
                srnum = ' ' * w_column1
            else:
                srnum = str(i).rjust(w_column1)
            nam = smry.colabel[i].ljust(w_column2)
            mxmw = ('%8.2f' % smry.maxmw[i]).rjust(w_mxmw)
            for j in range(len(smry.codesc[i])):
                dsc = smry.codesc[i][j]
                if j == 0:
                    report('%(srnum)s %(nam)s %(mxmw)s %(dsc)s\n' % vars())
                else:
                    spc = ' ' * (w_column1 + 1 + w_column2 + 1 + w_mxmw)
                    report('%(spc)s %(dsc)s\n' % vars())

    else:
        report('No Contingencies..')
    _get_report_file_object(rptfile, process='close', rptdesc='PV Summary')
    return smry.ierr


def _pv_report_one_contingency(cntlbl, soln, report):
    smry = _ppv_summary
    ntrans = len(soln.mwtransfer)
    nmvbus = len(soln.volts[0])
    nmgnbus = len(soln.mgenmw[0])
    nmline = len(soln.mbrnmva[0])
    ninter = len(soln.mitfmw[0])
    if smry.pvsize.vernum >= 1:
        nmldbus = len(soln.mloadmw[0])
    else:
        nmldbus = 0
    mwtrns_ttl = 'MW TRANSFER-->'
    mwtransfer = ''
    for i in range(ntrans):
        mw = '%9g' % soln.mwtransfer[i]
        mwtransfer += ' %9s' % mw

    w_mwtransfer = len(mwtransfer)
    w_columneach = 10
    cntlbl = 'CONTINGENCY: ' + cntlbl.strip()
    w_cntlbl = len(cntlbl)
    w_hline = max(w_mwtransfer, 80)
    w_hlspc = int(0.5 * (w_hline - w_cntlbl))
    hline = '=' * w_hlspc + cntlbl + '=' * w_hlspc
    report('\n%(hline)s\n' % vars())
    report('Solution Mismatch\n')
    mvaworst = 'MVA MISMATCH'
    mvatotal = 'TOTAL MVA MISMATCH'
    cnvstate = 'CONVERGED'
    cnvcondn = 'CONVERGE CONDITION'
    w_column1 = max(len(mvaworst), len(mvatotal), len(mwtrns_ttl), len(cnvstate), len(cnvcondn))
    column1 = mwtrns_ttl.rjust(w_column1)
    mvaworst = mvaworst.rjust(w_column1)
    mvatotal = mvatotal.rjust(w_column1)
    cnvstate = cnvstate.rjust(w_column1)
    cnvcondn = cnvcondn.rjust(w_column1)
    report('%(column1)s%(mwtransfer)s\n' % vars())
    for i in range(ntrans):
        mvaworst += ('%9.5f' % soln.mvaworst[i]).rjust(w_columneach)
        mvatotal += ('%9.5f' % soln.mvatotal[i]).rjust(w_columneach)
        if soln.cnvflag[i]:
            st = 'YES'
        else:
            st = 'NO'
        cnvstate += ('%s' % st).rjust(w_columneach)
        cnvcondn += ('%s' % soln.cnvcond[i][:9]).rjust(w_columneach)

    report('%(mvaworst)s\n' % vars())
    report('%(mvatotal)s\n' % vars())
    report('%(cnvstate)s\n' % vars())
    report('%(cnvcondn)s\n' % vars())
    report('\n')
    if nmvbus:
        w_column1 = max([len(each) for each in smry.mvbuslabel])
        report('Monitored Bus Voltages (pu)\n')
        column1 = mwtrns_ttl.rjust(w_column1)
        report('%(column1)s%(mwtransfer)s\n' % vars())
        for i in range(nmvbus):
            volt = smry.mvbuslabel[i].rjust(w_column1)
            for j in range(ntrans):
                volt += ('%9.5f' % soln.volts[j][i]).rjust(w_columneach)

            report('%(volt)s\n' % vars())

        report('\n')
    if nmgnbus:
        w_column1 = max([len(each) for each in smry.mgenbus])
        w_unit = 4
        report('Monitored Plants (MW and MVAR)\n')
        column1 = mwtrns_ttl.rjust(w_column1)
        unit = ' ' * w_unit
        report('%(column1)s %(unit)s%(mwtransfer)s\n' % vars())
        for i in range(nmgnbus):
            mw = smry.mgenbus[i].rjust(w_column1)
            unit = ('MW').rjust(w_unit)
            mw = '%(mw)s %(unit)s' % vars()
            mvar = ' ' * w_column1
            unit = ('MVAR').rjust(w_unit)
            mvar = '%(mvar)s %(unit)s' % vars()
            for j in range(ntrans):
                mw += ('%9.2f' % soln.mgenmw[j][i]).rjust(w_columneach)
                mvar += ('%9.2f' % soln.mgenmvar[j][i]).rjust(w_columneach)

            report('%(mw)s\n' % vars())
            report('%(mvar)s\n' % vars())

        report('\n')
    if nmldbus:
        w_column1 = max([len(each) for each in smry.mloadbus])
        w_unit = 4
        report('Monitored Loads (MW and MVAR)\n')
        column1 = mwtrns_ttl.rjust(w_column1)
        unit = ' ' * w_unit
        report('%(column1)s %(unit)s%(mwtransfer)s\n' % vars())
        for i in range(nmldbus):
            mw = smry.mloadbus[i].rjust(w_column1)
            unit = ('MW').rjust(w_unit)
            mw = '%(mw)s %(unit)s' % vars()
            mvar = ' ' * w_column1
            unit = ('MVAR').rjust(w_unit)
            mvar = '%(mvar)s %(unit)s' % vars()
            for j in range(ntrans):
                mw += ('%9.2f' % soln.mloadmw[j][i]).rjust(w_columneach)
                mvar += ('%9.2f' % soln.mloadmvar[j][i]).rjust(w_columneach)

            report('%(mw)s\n' % vars())
            report('%(mvar)s\n' % vars())

        report('\n')
    if nmline:
        w_column1 = max([len(each) for each in smry.mbranch])
        w_unit = 3
        report('Monitored Branches Flow\n')
        column1 = mwtrns_ttl.rjust(w_column1)
        unit = ' ' * w_unit
        report('%(column1)s %(unit)s%(mwtransfer)s\n' % vars())
        for i in range(nmline):
            mva = smry.mbranch[i].rjust(w_column1)
            unit = ('MVA').rjust(w_unit)
            mva = '%(mva)s %(unit)s' % vars()
            unit = ('AMP').rjust(w_unit)
            for j in range(ntrans):
                mva += ('%9.2f' % soln.mbrnmva[j][i]).rjust(w_columneach)

            report('%(mva)s\n' % vars())

        report('\n')
    if ninter:
        w_column1 = max([len(each) for each in smry.minterface])
        w_unit = 2
        report('Monitored Interfaces (MW)\n')
        column1 = mwtrns_ttl.rjust(w_column1)
        unit = ' ' * w_unit
        report('%(column1)s %(unit)s%(mwtransfer)s\n' % vars())
        for i in range(ninter):
            mw = smry.minterface[i].rjust(w_column1)
            unit = ('MW').rjust(w_unit)
            mw = '%(mw)s %(unit)s' % vars()
            for j in range(ntrans):
                mw += ('%9.2f' % soln.mitfmw[j][i]).rjust(w_columneach)

            report('%(mw)s\n' % vars())


def pv_solution_report(pvfile=None, colabels=None, rptfile=None):
    """
    ierr = pv_solution_report(pvfile,colabels,rptfile)
    PV analysis solution text report.
    Inputs:
        pvfile   = PV output file name (.pv)
        colabels = contingency labels (to get PV solution)
                   default "all contingencies"
                   for more than one contingency, provide as a list or tuple
        rptfile  = report text file name (to write solution report)
                   default "PSS(R)E Report"
    Returns ierr.
        ierr     = 0, no error
    """
    smry = pv_summary(pvfile)
    if colabels:
        if isinstance(colabels, type(())):
            colabels = list(colabels)
        if not isinstance(colabels, type([])):
            colabels = [
             colabels]
    else:
        colabels = smry.colabel
        psspy.progress(' \n     Contingency Labels not provided. All contingencies considered.\n')
    report = _get_report_file_object(rptfile, process='open')
    ttl_hline = '*' + 46 * ' *' + '\n\n'
    ttl = 30 * ' ' + 'PV SOLUTION' + '\n'
    ttl_file = 30 * ' ' + smry.file.pv + '\n'
    ttl_time = 30 * ' ' + time.ctime() + '\n\n'
    report(ttl_hline)
    report(ttl)
    report(ttl_file)
    report(ttl_time)
    report(ttl_hline)
    ret_ierr = 0
    for lbl in colabels:
        rlst = pv_solution(pvfile, lbl)
        if rlst == None:
            continue
        if rlst.ierr != 0:
            ret_ierr = rlst.ierr
        _pv_report_one_contingency(lbl, rlst, report)

    _get_report_file_object(rptfile, process='close', rptdesc='PV solution')
    return ret_ierr


def _qv_size(qvfile=None):
    """
    rlst = qv_size(qvfile)
    Returns QV analysis array sizes.
    Inputs:
        qvfile  = QV output file name (.qv)
    Returned object 'rlst' contains the following attributes:
        See qv_summary for returned values.
    """
    global _qqv_qvfnam
    global _qqv_qvfnam_mtime
    global _qqv_qvfnam_size
    global _qqv_size
    if qvfile:
        qvfile = _check_file(name=qvfile, ext='pv', desc='QV output', type='read')
    _qqv_qvfnam = qvfile
    _qqv_qvfnam_size = os.path.getsize(_qqv_qvfnam)
    _qqv_qvfnam_mtime = os.path.getmtime(_qqv_qvfnam)
    rlst = pssaccss.qv_size(qvfile)
    if rlst[0]:
        _qqv_size = None
        errtxt = ' ERROR=%d Refer PSS(R)E API manual for error description.' % rlst[0]
        _ShowError('qv_size', errtxt)
    _qqv_size = []
    _qqv_size.append(rlst[1])
    _qqv_size.append(rlst[2])
    _qqv_size.append(rlst[3])
    _qqv_size.append(rlst[4])
    _qqv_size.append(rlst[5])
    _qqv_size.append(rlst[6])
    _qqv_size.append(rlst[7])
    _qqv_size.append(rlst[8])
    _qqv_size.append(rlst[9])
    _qqv_size.append(rlst[10])
    return _qqv_size


def qv_summary(qvfile=None):
    """
    rlst = qv_summary(qvfile)
    Returns QV analysis summary.
    Inputs:
        qvfile = QV output file name (.qv)
    Returned object 'rlst' contains the following attributes:
        rlst.ierr             = error code (0=no error)
        rlst.qvbus            = QV analysis bus name
        rlst.qvsize.ncase     = number of contingencies + 1 (for base case)
        rlst.qvsize.nmvbus    = number of voltage monitored buses
        rlst.qvsize.nmvrec    = number of voltage monitored records
        rlst.qvsize.nmgnbus   = number of monitored plant (generator) buses
        rlst.qvsize.nmxvstp   = maximum number of voltage setpoint changes
        rlst.options          = QV solution options (same as in API manual)
        rlst.values           = QV solution values (same as in API manual)
        rlst.casetitle.line1  = short title line 1
        rlst.casetitle.line2  = short title line 2
        rlst.file.qv          = contingency output (.acc) file name
        rlst.file.sav         = saved case (.sav) file name
        rlst.file.thr         = load throwover data (.thr) file name
        rlst.file.dfx         = distribution factor data (.dfx) file name
        rlst.file.sub         = subsystem definition data (.sub) file name
        rlst.file.mon         = monitored element data (.mon) file name
        rlst.file.con         = contingency description data (.con) file name
        rlst.file.inl         = inertia and governor response data (.inl) file name
        rlst.file.zip         = incremental Save case archive (.zip) file name
        rlst.dispatchss       = dispatch subsystem name
        rlst.mgenbus          = monitored plant (generator) bus label
        rlst.mvbuslabel       = monitored voltage bus label
        rlst.mvreclabel       = monitored voltage record label
        rlst.mvrecmax         = monitored voltage bus maximum
        rlst.mvrecmin         = monitored voltage bus minimum
        rlst.mvrectype        = monitored voltage record type (range/deviation)
        rlst.colabel          = contingency labels
        rlst.codesc           = contingency description
        rlst.minvstp          = minimum voltage setpoint
        rlst.maxvstp          = maximum voltage setpoint
        rlst.minmvar          = minimum MVAR change
        rlst.maxmvar          = maximum MVAR change
        rlst.maxmsm           = maximum MVAR mismatch
    """
    global _do_pv_after_qv
    global _do_qv_after_pv
    global _qqv_summary
    if _samefile(_qqv_qvfnam, _qqv_qvfnam_size, _qqv_qvfnam_mtime, qvfile) and not _do_qv_after_pv:
        if _validate_previous_results(_qqv_size, _qqv_summary):
            return _qqv_summary
    _do_pv_after_qv = True
    _do_qv_after_pv = False
    qvsize_rlst = _qv_size(qvfile)
    qvsize = qvsize_rlst[0]
    qvcntlbl = qvsize_rlst[1]
    qvcntdsc = qvsize_rlst[2]
    qvminvstp = qvsize_rlst[3]
    qvmaxvstp = qvsize_rlst[4]
    qvminmvar = qvsize_rlst[5]
    qvmaxmvar = qvsize_rlst[6]
    qvmaxmsm = qvsize_rlst[7]
    qvcntadr = qvsize_rlst[8]
    qvcntnvstp = qvsize_rlst[9]
    rlst = pssaccss.qv_summary(qvfile, qvsize)
    if rlst[0]:
        _qqv_summary = None
        errtxt = ' ERROR=%d Refer PSS(R)E API manual for error description.' % rlst[0]
        _ShowError('qv_summary', errtxt)
    names = list(_QV_SUMMARY_NAM)
    names.insert(0, _ERR_CODE_NAM)
    rlst = list(rlst)
    dispatchss = rlst.pop(-1)
    dispatchss = dispatchss[0]
    qvbus = rlst[1][_QV_INT_OPTIONS_STUDY_BUS_INDEX - 1]
    try:
        tmp_bsnums = [int(each.split()[0]) for each in rlst[5]]
    except ValueError:
        tmp_bsnums = [int(each.split()[2]) for each in rlst[5]]

    idx = tmp_bsnums.index(qvbus)
    qvbus = rlst[5][idx]
    rlst.insert(1, qvbus)
    rlst.insert(2, qvsize)
    rlst.append(qvcntlbl)
    rlst.append(qvcntdsc)
    rlst.append(qvminvstp)
    rlst.append(qvmaxvstp)
    rlst.append(qvminmvar)
    rlst.append(qvmaxmvar)
    rlst.append(qvmaxmsm)
    rlst.append(qvcntadr)
    rlst.append(qvcntnvstp)
    rlst.append(dispatchss)
    rlst = _CaseLessAttributeList(lstnames=names, inlist=rlst)
    qvsize = _CaseLessAttributeList(lstnames=_QV_SIZE_NAM, inlist=rlst.qvsize)
    casetitle = _CaseLessAttributeList(lstnames=_SHRT_TITLE_NAM, inlist=rlst.casetitle)
    filemap = _CaseLessAttributeList(lstnames=_QV_FILE_NAM, inlist=rlst.file)
    rlst.qvsize = qvsize
    rlst.casetitle = casetitle
    rlst.file = filemap
    codesc = []
    for i in range(qvsize.ncase):
        dsc = _remove_extra_spaces(rlst.codesc[i])
        codesc.append(dsc)

    rlst.codesc = codesc
    _qqv_summary = rlst
    return _qqv_summary


def qv_solution(qvfile=None, colabel=None):
    """
    rlst = qv_solution(qvfile,colabel)
    QV analysis monitored flows and bus voltages for one contingency.
    Inputs:
        qvfile  = QV output file name (.qv)
        colabel = contingency label (to get QV solution for)
                  only one contingency label allowed
    Returned object 'rlst' contains the following attributes:
        rlst.ierr       = error code(0=no error)
        rlst.island     = number of islands, integer
        rlst.vsetpoint  = voltage setpoints, float of length [nvstp]
        rlst.cnvflag    = convergence flag (True when converged), logical of length [nvstp]
        rlst.cnvcond    = convergence condition
        rlst.mvaworst   = larget bus MVA mismatch, float of length [nvstp]
        rlst.mvatotal   = total system MVA mismatch, float of length [nvstp]
        rlst.volts      = monitored bus voltage (pu), float of length [nmvbus][nvstp]
        rlst.mgenmvar   = monitored plant Mvar, float of length [nmgnbus][nvstp]

        where
        nvstp   = number of voltage setpoint changes
        nmvbus  = number of voltage monitored buses
        nmgnbus = number of monitored plant (generator) buses
    """
    if isinstance(colabel, type([])):
        errtxt = ' One contingency label expected. List provided.'
        _ShowError(_INPUTERROR, errtxt)
    sumry = qv_summary(qvfile)
    coaddress = _check_contingency_label(colabel, sumry.colabel, sumry.cntadr)
    if not coaddress:
        return None
    else:
        qvsizelst = []
        for nam in _QV_SIZE_NAM:
            qvsizelst.append(getattr(sumry.qvsize, nam))

        idx = list(sumry.cntadr).index(coaddress)
        qvnvstp = sumry.cntnvstp[idx]
        rlst = pssaccss.qv_solution(qvfile, qvsizelst, coaddress, qvnvstp)
        if rlst[0]:
            errtxt = ' ERROR=%d Refer PSS(R)E API manual for error description.' % rlst[0]
            _ShowError('qv_solution', errtxt)
        names = list(_QV_SOLUTION_NAM)
        names.insert(0, _ERR_CODE_NAM)
        rlst = _CaseLessAttributeList(lstnames=names, inlist=rlst)
        return rlst


def qv_summary_report(qvfile=None, rptfile=None):
    """
    ierr = qv_summary_report(qvfile,rptfile)
    QV analysis summary text report.
    Inputs:
        qvfile  = QV output file name (.qv)
        rptfile = report text file name (to write summary report)
                  default "PSS(R)E Report"
    Returns ierr.
        ierr    = 0, no error
    """
    smry = qv_summary(qvfile)
    report = _get_report_file_object(rptfile, process='open')
    ttl_hline = '*' + 46 * ' *' + '\n\n'
    ttl = 30 * ' ' + 'QV SOLUTION SUMMARY ' + '\n'
    ttl_file = 30 * ' ' + smry.file.qv + '\n'
    ttl_time = 30 * ' ' + time.ctime() + '\n\n'
    qvbus_line = 30 * ' ' + 'QV Analysis Bus = %s\n\n' % smry.qvbus
    report(ttl_hline)
    report(ttl)
    report(ttl_file)
    report(ttl_time)
    report(qvbus_line)
    report(ttl_hline)
    report('%s\n' % smry.casetitle.line1)
    report('%s\n' % smry.casetitle.line2)
    report('\n')
    report('QV output file               = %s\n' % smry.file.qv)
    report('Saved Case file              = %s\n' % smry.file.sav)
    if smry.file.thr:
        report('Load throwover file          = %s\n' % smry.file.thr)
    report('DFAX file                    = %s\n' % smry.file.dfx)
    report('Subsystem file               = %s\n' % smry.file.sub)
    report('Monitored Element file       = %s\n' % smry.file.mon)
    report('Contingency Description file = %s\n' % smry.file.con)
    if smry.file.inl:
        report('Inertia and Governor Response file = %s\n' % smry.file.inl)
    if smry.file.zip:
        report('Incremental Save Case Archive file = %s\n' % smry.file.zip)
    report('\n')
    report('QV Solution Options:\n')
    for i in range(len(smry.options)):
        j = smry.options[i]
        ti = str(i + 1).rjust(2)
        tj = str(j)
        t1 = _QV_INT_OPTIONS_NAMES[i]
        if i == _QV_INT_OPTIONS_STUDY_BUS_INDEX - 1:
            report('option(%(ti)s): %(t1)s =%(tj)s\n' % vars())
        else:
            t2 = _QV_INT_OPTIONS_LIST[i][j]
            report('option(%(ti)s): %(t1)s =%(tj)s =%(t2)s\n' % vars())

    report('\n')
    report('QV Solution Values:\n')
    for i in range(len(smry.values)):
        ti = str(i + 1)
        tn = _QV_REAL_VALUES_NAMES[i]
        tv = '%g' % smry.values[i]
        report('value(%(ti)s): %(tn)s =%(tv)s\n' % vars())

    report('\n')
    if smry.dispatchss:
        report('Dispatch subsystem = %s\n' % smry.dispatchss)
        report('\n')
    report('Number of Contingencies+Base Case          = %d\n' % smry.qvsize.ncase)
    report('Number of Monitored Generators(Plants)     = %d\n' % smry.qvsize.nmgnbus)
    report('Number of Voltage Monitored Buses          = %d\n' % smry.qvsize.nmvbus)
    report('Number of Voltage Monitored Records        = %d\n' % smry.qvsize.nmvrec)
    report('Number of maximum voltage setpoint changes = %d\n' % smry.qvsize.nmxvstp)
    report('\n')
    if smry.qvsize.nmgnbus:
        w_column1 = len(str(smry.qvsize.nmgnbus)) + 1
        w_column2 = max([len(each) for each in smry.mgenbus])
        report('Monitored Plants (Generators)\n')
        for i in range(smry.qvsize.nmgnbus):
            srnum = (str(i + 1) + ':').rjust(w_column1)
            nam = smry.mgenbus[i].ljust(w_column2)
            report('%(srnum)s %(nam)s\n' % vars())

        report('\n')
    if smry.qvsize.nmvbus:
        w_column1 = len(str(smry.qvsize.nmvbus)) + 1
        w_column2 = max([len(each) for each in smry.mvbuslabel])
        report('Monitored Buses\n')
        for i in range(smry.qvsize.nmvbus):
            srnum = (str(i + 1) + ':').rjust(w_column1)
            nam = smry.mvbuslabel[i].ljust(w_column2)
            report('%(srnum)s %(nam)s\n' % vars())

        report('\n')
    if smry.qvsize.ncase:
        w_column1 = len(str(smry.qvsize.ncase)) + 1
        w_column2 = max([len(each) for each in smry.colabel])
        w_mxmnvstp = 7
        w_mxmnmvar = 8
        w_mxmsm = 9
        if w_column2 < 5:
            w_column2 = 5
        report('QV Contingencies\n')
        srnum = ' ' * w_column1
        nam = ('LABEL').ljust(w_column2)
        minvstp = ('MinVstp').rjust(w_mxmnvstp)
        maxvstp = ('MaxVstp').rjust(w_mxmnvstp)
        minmvar = ('MinMVAR').rjust(w_mxmnmvar)
        maxmvar = ('MaxMVAR').rjust(w_mxmnmvar)
        maxmsm = ('MaxMSM').rjust(w_mxmsm)
        dsc = 'DESCRIPTION'
        report('%(srnum)s %(nam)s %(minvstp)s %(maxvstp)s %(minmvar)s %(maxmvar)s %(maxmsm)s %(dsc)s\n' % vars())
        for i in range(smry.qvsize.ncase):
            if i == 0:
                srnum = (' ').rjust(w_column1)
            else:
                srnum = str(i).rjust(w_column1)
            nam = smry.colabel[i].ljust(w_column2)
            minvstp = ('%4.2f' % smry.minvstp[i]).rjust(w_mxmnvstp)
            maxvstp = ('%4.2f' % smry.maxvstp[i]).rjust(w_mxmnvstp)
            minmvar = ('%8.2f' % smry.minmvar[i]).rjust(w_mxmnmvar)
            maxmvar = ('%8.2f' % smry.maxmvar[i]).rjust(w_mxmnmvar)
            maxmsm = ('%9.4f' % smry.maxmsm[i]).rjust(w_mxmsm)
            for j in range(len(smry.codesc[i])):
                dsc = smry.codesc[i][j]
                if j == 0:
                    report('%(srnum)s %(nam)s %(minvstp)s %(maxvstp)s %(minmvar)s %(maxmvar)s %(maxmsm)s %(dsc)s\n' % vars())
                else:
                    spc = ' ' * (w_column1 + 1 + w_column2 + 1 + 2 * (w_mxmnvstp + 1) + 2 * (w_mxmnmvar + 1) + w_mxmsm)
                    report('%(spc)s %(dsc)s\n' % vars())

    else:
        report('No Contingencies..')
    _get_report_file_object(rptfile, process='close', rptdesc='QV Summary')
    return smry.ierr


def _qv_report_one_contingency(cntlbl, soln, report):
    smry = _qqv_summary
    nvstp = len(soln.vsetpoint)
    nmvbus = len(soln.volts[0])
    nmgnbus = len(soln.mgenmvar[0])
    vstp_ttl = 'Voltage Setpoint-->'
    vsetpoint = ''
    for i in range(nvstp):
        vst = '%g' % soln.vsetpoint[i]
        vsetpoint += ' %9s' % vst

    w_vsetpoint = len(vsetpoint)
    w_columneach = 10
    cntlbl = 'CONTINGENCY: ' + cntlbl.strip()
    w_cntlbl = len(cntlbl)
    w_hline = max(w_vsetpoint, 80)
    w_hlspc = int(0.5 * (w_hline - w_cntlbl))
    hline = '=' * w_hlspc + cntlbl + '=' * w_hlspc
    report('\n%(hline)s\n' % vars())
    report('Solution Mismatch\n')
    mvaworst = 'MVA MISMATCH'
    mvatotal = 'TOTAL MVA MISMATCH'
    cnvstate = 'CONVERGED'
    cnvcondn = 'CONVERGE CONDITION'
    w_column1 = max(len(mvaworst), len(mvatotal), len(vstp_ttl), len(cnvstate), len(cnvcondn))
    column1 = vstp_ttl.rjust(w_column1)
    mvaworst = mvaworst.rjust(w_column1)
    mvatotal = mvatotal.rjust(w_column1)
    cnvstate = cnvstate.rjust(w_column1)
    cnvcondn = cnvcondn.rjust(w_column1)
    report('%(column1)s%(vsetpoint)s\n' % vars())
    for i in range(nvstp):
        mvaworst += ('%9.5f' % soln.mvaworst[i]).rjust(w_columneach)
        mvatotal += ('%9.5f' % soln.mvatotal[i]).rjust(w_columneach)
        if soln.cnvflag[i]:
            st = 'YES'
        else:
            st = 'NO'
        cnvstate += ('%s' % st).rjust(w_columneach)
        cnvcondn += ('%s' % soln.cnvcond[i][:9]).rjust(w_columneach)

    report('%(mvaworst)s\n' % vars())
    report('%(mvatotal)s\n' % vars())
    report('%(cnvstate)s\n' % vars())
    report('%(cnvcondn)s\n' % vars())
    report('\n')
    if nmvbus:
        w_column1 = max([len(each) for each in smry.mvbuslabel])
        report('Monitored Bus Voltages (pu)\n')
        column1 = vstp_ttl.rjust(w_column1)
        report('%(column1)s%(vsetpoint)s\n' % vars())
        for i in range(nmvbus):
            volt = smry.mvbuslabel[i].rjust(w_column1)
            for j in range(nvstp):
                volt += ('%9.5f' % soln.volts[j][i]).rjust(w_columneach)

            report('%(volt)s\n' % vars())

    report('\n')
    if nmgnbus:
        w_column1 = max([len(each) for each in smry.mgenbus])
        w_unit = 4
        report('Monitored Plants (MVAR)\n')
        column1 = vstp_ttl.rjust(w_column1)
        unit = ' ' * w_unit
        report('%(column1)s %(unit)s%(vsetpoint)s\n' % vars())
        for i in range(nmgnbus):
            mvar = smry.mgenbus[i].rjust(w_column1)
            unit = ('MVAR').rjust(w_unit)
            mvar = '%(mvar)s %(unit)s' % vars()
            for j in range(nvstp):
                mvar += ('%9.2f' % soln.mgenmvar[j][i]).rjust(w_columneach)

            report('%(mvar)s\n' % vars())

    report('\n')


def qv_solution_report(qvfile=None, colabels=None, rptfile=None):
    """
    ierr = qv_solution_report(qvfile,colabels,rptfile)
    QV analysis solution text report.
    Inputs:
        qvfile   = QV output file name (.qv)
        colabels = contingency labels (to get QV solution)
                   default "all contingencies"
                   for more than one contingency, provide as a list or tuple
        rptfile  = report text file name (to write solution report)
                   default "PSS(R)E Report"
    Returns ierr.
        ierr     = 0, no error
    """
    smry = qv_summary(qvfile)
    if colabels:
        if isinstance(colabels, type(())):
            colabels = list(colabels)
        if not isinstance(colabels, type([])):
            colabels = [
             colabels]
    else:
        colabels = smry.colabel
        psspy.progress(' \n     Contingency Labels not provided. All contingencies considered.\n')
    report = _get_report_file_object(rptfile, process='open')
    ttl_hline = '*' + 46 * ' *' + '\n\n'
    ttl = 30 * ' ' + 'QV SOLUTION' + '\n'
    ttl_file = 30 * ' ' + smry.file.qv + '\n'
    ttl_time = 30 * ' ' + time.ctime() + '\n\n'
    qvbus_line = 30 * ' ' + 'QV Analysis Bus = %s\n\n' % smry.qvbus
    report(ttl_hline)
    report(ttl)
    report(ttl_file)
    report(ttl_time)
    report(qvbus_line)
    report(ttl_hline)
    ret_ierr = 0
    for lbl in colabels:
        rlst = qv_solution(qvfile, lbl)
        if rlst == None:
            continue
        if rlst.ierr != 0:
            ret_ierr = rlst.ierr
        _qv_report_one_contingency(lbl, rlst, report)

    _get_report_file_object(rptfile, process='close', rptdesc='QV solution')
    return ret_ierr


def _validate_args_sensitivity_flow_to_mw(ibus, jbus, mainsys, dfxfile, kbus, ckt, netmod, brnflowtyp, transfertyp, oppsystyp, dispmod, toln, oppsys):
    if psspy.totbus() <= 0:
        errtxt = ' Returning .. no network data in memory. Open PSSE power flow case.'
        _ShowError('sensitivity_flow_to_mw', errtxt)
    errlst = []
    lerr, ibus = _check_int_type(ibus, 'ibus')
    errlst.append(lerr)
    lerr, jbus = _check_int_type(jbus, 'jbus')
    errlst.append(lerr)
    lerr, kbus = _check_int_type(kbus, 'kbus')
    errlst.append(lerr)
    lerr, ckt = _check_str_type(ckt, 'ckt')
    errlst.append(lerr)
    lerr, mainsys = _check_str_type(mainsys, 'mainsys')
    errlst.append(lerr)
    dfxfile = _check_file(name=dfxfile, ext='dfx', desc='DFAX file', type='read')
    lerr, toln = _check_float_type(toln, 'toln')
    errlst.append(lerr)
    lerr, oppsys = _check_str_type(oppsys, 'oppsys')
    errlst.append(lerr)
    netmod = _check_string_input(netmod, 'netmod', allowlst=['dc', 'ac'], defval='dc')
    brnflowtyp = _check_string_input(brnflowtyp, 'brnflowtyp', allowlst=['mw', 'mvar', 'mva', 'amps'], defval='mw')
    transfertyp = _check_string_input(transfertyp, 'transfertyp', allowlst=['import', 'export'], defval='import')
    oppsystyp = _check_string_input(oppsystyp, 'oppsystyp', allowlst=[
     'slack', 'slack bus', 'single bus', 'single', 'subsystem', 'system'], defval='slack')
    if oppsystyp in ('subsystem', 'system'):
        dispmod = _check_int_input(dispmod, 'dispmod', minval=1, maxval=7, defval=1)
    ierr = any(errlst)
    return (
     ierr, ibus, jbus, mainsys, dfxfile, kbus, ckt, netmod, brnflowtyp, transfertyp, oppsystyp, dispmod, toln, oppsys)


def _do_sensitivity_flow_to_mw(ibus, jbus, mainsys, dfxfile, kbus, ckt, netmod, brnflowtyp, transfertyp, oppsystyp, dispmod, toln, oppsys):
    opt = []
    opt.append(ibus)
    opt.append(jbus)
    opt.append(kbus)
    if netmod == 'dc':
        opt.append(0)
    else:
        opt.append(1)
    if brnflowtyp == 'mw':
        opt.append(0)
    elif brnflowtyp == 'mvar':
        opt.append(1)
    elif brnflowtyp == 'mva':
        opt.append(2)
    else:
        opt.append(3)
    if transfertyp == 'import':
        opt.append(0)
    else:
        opt.append(1)
    if oppsystyp in ('slack', 'slack bus'):
        opt.append(0)
    elif oppsystyp in ('single bus', 'single'):
        opt.append(1)
    else:
        opt.append(2)
    opt.append(dispmod)
    ierr, genbus, genval, lodbus, lodval = pssaccss.sensitivity_ftomw(opt, toln, ckt, [mainsys, oppsys], dfxfile)
    if ierr:
        errtxt = ' ERROR=%d Refer PSS(R)E API manual for error description.' % ierr
        _ShowError('sensitivity_flow_to_mw', errtxt)
    rdctobj = _Dict_caseless_bunch({_ERR_CODE_NAM: ierr, 'ngenbuses': (len(genbus[0])), 
       'nloadbuses': (len(lodbus[0])), 
       'genvalues': {}, 'loadvalues': {}})
    for bus, pgen, pmax, pmin, sftr in zip(genbus[0], genval[0], genval[1], genval[2], genval[3]):
        rdctobj['genvalues'][bus] = _Dict_caseless_bunch({'pgen': pgen, 'pmax': pmax, 'pmin': pmin, 'factor': sftr})

    for bus, pload, sftr in zip(lodbus[0], lodval[0], lodval[1]):
        rdctobj['loadvalues'][bus] = _Dict_caseless_bunch({'pload': pload, 'factor': sftr})

    return rdctobj


def sensitivity_flow_to_mw(ibus, jbus, mainsys, dfxfile, kbus=0, ckt='1', netmod='dc', brnflowtyp='mw', transfertyp='import', oppsystyp='slack bus', dispmod=1, toln=None, oppsys=''):
    """Calculate Sensitity Factors of a branch flow to MW power at generator and load buses.

robj = sensitivity_flow_to_mw(ibus,jbus,mainsys,dfxfile,kbus=0,ckt='1',netmod='dc',brnflowtyp='mw',
            transfertyp='import',oppsystyp='slack bus',dispmod=1,toln=TOLN,oppsys=None)
Inputs:
    ibus,jbus,kbus,ckt = study branch identification
                         from bus, to bus, third bus (if branch is part of three winding
                         transformer) and circuit id.
                         kbus = 0 by default
                         ckt  = '1' by default
    mainsys     = label of the subsystem containing components to which the sensitivity factors
                  of the branch flow are calculated
    dfxfile     = distribution factors file name (.dfx)
    netmod      = network model name on which sensitivity analysis is based,
                = 'dc' for DC network model (default)
                = 'ac' for AC network model
    brnflowtyp  = branch flow type to which the sensitivity factors are calculated
                  When using DC network model
                = 'mw' for MW flow (default)
                  When using AC network model
                = 'mw' for MW flow (default)
                = 'mvar' for MVAR flow
                = 'mva' for MVA flow
                = 'amps' for ampere flow
    transfertyp = flag to specify the transfer from the components to which sensitivity
                  factors of the branch flow are calculated to the opposing subsystem
                = 'import' for the positive transfer is from components to opposing subsystem (default)
                = 'export' for the positive transfer is from opposing subsystem to components
    oppsystyp   = opposing subsystem type
                = 'slack bus' or 'slack' (default)
                = 'single bus' or 'single'
                = 'subsystem' or 'subsys'
    dispmod     = 1 for buses and participating factors from DFAX file for buses with
                    positive MW machines (default)
                = 2 for buses and participating factors from DFAX file for buses with
                    positive MW constant MVA load
                = 3 for Buses & participating factors from DFAX file for buses with
                    either positive MW machines or positive MW constant MVA load
                = 4 for Subsystem buses with positive MW constant MVA load in proportion
                    to their MW load
                = 5 for Subsystem buses with positive MW machines in proportion to
                    their MW output
                = 6 for Subsystem buses with positive MW machines in proportion to their MBASE
                = 7 for Subsystem buses with positive MW machines in proportion to their
                    reserves (Pmaxmc-Pgenmc)
    toln        = mismatch tolerance for continuing sensitivity analysis in AC mode,
                  ignored in DC mode (TOLN by default)
    oppsys      = label of the opposing subsystem when the opposing subsystem type is a subsystem

Returns 'robj' object. It is a special caseless dictionary object, which can be accessed either
    by dictionary keys or attributes.

    robj.ierr       = error code (0=no error)
    robj.ngenbuses  = number of generator buses to which sensitivity factors are calculated
    robj.nloadbuses = number of load buses to which sensitivity factors are calculated

    robj.genvalues[bus].pgen   = generator real power output, MW
    robj.genvalues[bus].pmax   = generator maximum power output, MW
    robj.genvalues[bus].pmin   = generator minimum power output, MW
    robj.genvalues[bus].factor = generator sensitivity factor
        where bus is generator bus extented names to which sensitivity factors are calculated

    robj.loadvalues[bus].pload  = load real power, MW
    robj.loadvalues[bus].factor = load sensitivity factor
        where bus is load bus extented names to which sensitivity factors are calculated

Note:
Any item from robj can be accessed with case insensitive attribute or dictionary key.
So following examples for accessing 'ngenbuses' are allowed.
        robj.ngenbuses, robj.ngenBuses, robj['ngenbuses'], robj['NGENbuses']
"""
    ierr, ibus, jbus, mainsys, dfxfile, kbus, ckt, netmod, brnflowtyp, transfertyp, oppsystyp, dispmod, toln, oppsys = _validate_args_sensitivity_flow_to_mw(ibus, jbus, mainsys, dfxfile, kbus, ckt, netmod, brnflowtyp, transfertyp, oppsystyp, dispmod, toln, oppsys)
    if ierr:
        return {}
    rdctobj = _do_sensitivity_flow_to_mw(ibus, jbus, mainsys, dfxfile, kbus, ckt, netmod, brnflowtyp, transfertyp, oppsystyp, dispmod, toln, oppsys)
    return rdctobj


def sensitivity_flow_to_mw_report(ibus, jbus, mainsys, dfxfile, kbus=0, ckt='1', netmod='dc', brnflowtyp='mw', transfertyp='import', oppsystyp='slack bus', dispmod=1, toln=None, oppsys='', rptfile=None):
    """Calculate Sensitity Factors of a branch flow to MW power at generator and load buses.

ierr = sensitivity_flow_to_mw_report(ibus,jbus,mainsys,dfxfile,kbus=0,ckt='1',netmod='dc',brnflowtyp='mw',
        transfertyp='import',oppsystyp='slack bus',dispmod=1,toln=TOLN,oppsys=None,rptfile='')

Inputs:
    rptfile  = report text file name (to write solution report)
               default "PSS(R)E Report"
    For other inputs refer help(sensitivity_flow_to_mw).

Returns ierr.
    ierr     = 0, no error
"""
    ierr, ibus, jbus, mainsys, dfxfile, kbus, ckt, netmod, brnflowtyp, transfertyp, oppsystyp, dispmod, toln, oppsys = _validate_args_sensitivity_flow_to_mw(ibus, jbus, mainsys, dfxfile, kbus, ckt, netmod, brnflowtyp, transfertyp, oppsystyp, dispmod, toln, oppsys)
    if ierr:
        return []
    rlst = _do_sensitivity_flow_to_mw(ibus, jbus, mainsys, dfxfile, kbus, ckt, netmod, brnflowtyp, transfertyp, oppsystyp, dispmod, toln, oppsys)
    report = _get_report_file_object(rptfile, process='open')
    ttl_hline = '*' + 36 * ' *' + '\n\n'
    ttl = '                    ' + 'SENSITIVITY FACTORS: BRANCH FLOW TO MW  ' + '\n'
    ttl_time = '                    ' + time.ctime() + '\n\n'
    report(ttl_hline)
    report(ttl)
    report(ttl_time)
    report(ttl_hline)
    ierr, inam = psspy.notona(ibus)
    inam = _remove_extra_spaces_string(inam)
    ierr, jnam = psspy.notona(jbus)
    jnam = _remove_extra_spaces_string(jnam)
    if kbus == 0:
        report('Study BRANCH: from bus %d (%s), to bus %d (%s), ckt %s\n' % (ibus, inam, jbus, jnam, ckt))
    else:
        ierr, knam = psspy.notona(kbus)
        knam = _remove_extra_spaces_string(knam)
        report('Study BRANCH: from bus %d (%s), to bus %d (%s), to bus %d (%s), ckt %s\n' % (ibus, inam, jbus, jnam, kbus, knam, ckt))
    report('\n')
    report('SAV file                = %s\n' % psspy.sfiles()[0])
    report('DFAX file               = %s\n' % dfxfile)
    report('Network Model           = %s\n' % netmod.upper())
    report('Branch Flow Type        = %s\n' % brnflowtyp.upper())
    report('Transfer Flag           = %s\n' % transfertyp.upper())
    report('Opposing subsystem Type = %s\n' % oppsystyp.upper())
    if type(dispmod) == int:
        report('Dispatch Mode           = %d\n' % dispmod)
    else:
        report('Dispatch Mode           = %s\n' % str(dispmod))
    if toln >= _BIGREL:
        report('Tolerance               = TOLN\n')
    else:
        report('Tolerance               = %g\n' % toln)
    report('Main subsystem          = %s, i.e. sensitivity factors are calculated for components in this subsystem\n' % mainsys)
    if oppsystyp in ('subsystem', 'subsys'):
        report('Opposing subsystem      = %s\n' % oppsys.upper())
    report('\n')
    report('------GENERATOR BUS------  --PMAX--  --PMIN--  --PGEN--  -FACTOR--\n')
    for nam, each in rlst.genvalues.items():
        pmax = each.pmax
        pmin = each.pmin
        pgen = each.pgen
        sftr = each.factor
        txt = '%(nam)s  %(pmax)8.2f  %(pmin)8.2f  %(pgen)8.2f   %(sftr)8.5f\n' % vars()
        report(txt)

    report('\n')
    report('--------LOAD BUS---------  --PLOAD-  -FACTOR--\n')
    for nam, each in rlst.loadvalues.items():
        plod = each.pload
        sftr = each.factor
        txt = '%(nam)s  %(plod)8.2f   %(sftr)8.5f\n' % vars()
        report(txt)

    return rlst.ierr


class GIC():
    """Create GIC object as below, get GIC solution results in Python objects and
    apply various methods defined here.

gicobj = pssarrays.GIC(savfile, gicfile, efield_mag, efield_deg,
    tielevels=0, study_year=0, thermal_ana_optn=0,
    substation_r=0.1, branch_xbyr=30.0, transformer_xbyr=30.0, efield_mag_local=0.0, efield_deg_local=0.0,
    efield_type='uniform', efield_unit='v/km', addfile_optn='rdch', gic2mvar_optn='kfactors',
    earth_model_name='', scan_storm_event='', power_flow_optn='',
    ejet_million_amps=0.0, ejet_halfwidth_km=0.0, ejet_period_min=0.0, ejet_height_km=0.0, ejet_center_deg=0.0,
    addfile='', purgfile='', rnwkfile='', pygicfile='nooutput',
    basekv=[], areas=[], buses=[], owners=[], zones=[],
    basekv_local=[], areas_local=[], buses_local=[], owners_local=[], zones_local=[],
    pf_itmxn=_i, pf_toln=_f, pf_tap=_i, pf_area=_i, pf_phshft=_i, pf_dctap=_i, pf_swsh=_i,
    pf_flat=_i, pf_varlmt=_i, pf_nondiv=_i
    )

where:
savfile          : PSSE power flow data file (.sav) name, no default allowed (Base Case)
                   (If power flow is to be solved after GIC calculations, ensure case is solved.)
gicfile          : GIC data file (.gic) name, no default allowed

efield_mag       : Geomagnetic storm electric field magnitude in units defined by 'efield_unit',
                   must be >0.0, no default allowed
                   For efield_type='benchmark',
                     - when specified as 0.0, it will be set to 8.0 v/km (default benchmark event strength)
                     - when specifed >0.0, used as specified
                   For efield_type='nonuniform', it will be not used.
efield_deg       : Geomagnetic storm electric field direction in degrees
                   When efield_type='uniform',    it must be 0.0 <= efield_deg <= 180.0 (no default allowed)
                   When efield_type='benchmark',  it must be 0.0 <= efield_deg <= 180.0 (no default allowed)
                   When efield_type='nonuniform', it will not be used.

tielevels        : Number of levels of inter-tie buses to add to subsystem (0 by default)
                   = 0 consider only subsystem buses, no buses from inter-ties
                   > 0 consider subsystem buses + these many levels of inter-tie buses
study_year       : Year number to scale benchmark event GMD storm (0 by default)
                   Default value 0 means current year. This is used when efield_type='benchmark'.
                   These scaling factors account in the influence of geomagnetic latitude and earth model on
                   the estimated geoelectric field magnitude and are provided in NERC TPL-007-1.
thermal_ana_optn : Option for Transformer Thermal Analysis (0 by default)
                   = -1, perform on all transformers
                   =  0, do not perform
                   >  0, perform on these many top transformers ordered by effective GIC flow

substation_r     : substation grounding dc resistance (0.1 ohm by default)
branch_xbyr      : transmission line X/R ratio, used to calculate branch DC resistance if R=0.0 in
                   in network data (30.0 by default)
transformer_xbyr : transformers X/R ratio, used to calculate winding DC resistance if R=0.0 in
                   network data (30.0 by default)
efield_mag_local : Local GMD hot spots electric field magnitude in units defined by efield_unit.
                   When efield_type='uniform',    it must be > 0.0    (default=efield_mag)
                   When efield_type='benchmark',  it must be > 0.0    (default=efield_mag)
                   When efield_type='nonuniform', it will be not used.
efield_deg_local : Local GMD hot spots electric field direction in degrees, 0.0 <= v <= 180.0
                   When efield_type='uniform',    it must be 0.0 <= deg <= 180.0    (default=efield_deg)
                   When efield_type='benchmark',  it must be 0.0 <= deg <= 180.0    (default=efield_deg)
                   When efield_type='nonuniform', it will be not used.

efield_type      : Electric Field Type ('uniform' by default)
                   = 'uniform' for Uniform
                   = 'benchmark' for benchmark event electric field
                   = 'nonuniform' for Non-uniform
efield_unit      : Geomagnetic storm electric field magnitude unit ('v/km' by default)
                   = 'v/km' for volts per km
                   = 'v/mi' for volts per mile
addfile_optn     : Option to add GIC updates to base case  ('rdch' by default)
                   = 'sav' to add updates to Saved Case
                   = 'rdch' to create RDCH file for GIC updates
gic2mvar_optn    : Option to select method for GIC to Mvar Calculation  ('kfactors' by default)
                   = 'kfactors' for GIC to Mvar scaling factors from GIC data file when provided,
                      otherwise default scaling factors
                   = 'capchar' for GIC to Mvar scaling factors from GIC data file when provided,
                     otherwise scaling factors from default transformer Mvar and GIC characteristics
earth_model_name : Earth Model Name ('' by default)
                   Either Standard or User defined model name must be provided if:
                   - Benchmark Event Electric Field is to be modeled
                   - Non-uniform Electric Field is to be modeled
                   - Transformer Thermal Analysis is to be performed
scan_storm_event : Option to scan storm event scenarios ('' by default)
                   (used when efield_type='uniform' or 'benchmark')
                   = ' '       , no storm orientation scan
                   = 'scan_deg', perform storm orientation scan that give maximum Var losses
                   Note: Degree Scan Steps
                   a) deg scan is performed in 10 deg steps initially.
                   b) find orientation for maximum var losses
                   c) in steps of 1 deg from orienttaion in (b), calculate VAR losses till losses
                      are less than max losses

power_flow_optn  : Option to solve Power Flow with GIC losses added to the base case  ('' by default)
                   = ' '   , do not perform power flow solution
                   = 'fdns', use fixed slope decoupled Newton-Raphson method
                   = 'fnsl', use Full Newton-Raphson method
                   = 'nsol', use Decoupled Newton-Raphson method
                      When scan_storm_event='scan_deg', power flow solved for one
                      orientation angle that give maximum Var losses

Electrojet Characteristics options used only if efield_type='nonuniform'
ejet_million_amps: Eletrojet current in million amperes, must be >0, no default allowed
ejet_halfwidth_km: Cauchy distribution half-width in km, must be >0, no default allowed
ejet_period_min  : Eletrojet period of variation in minutes, must be >0, no default allowed
ejet_height_km   : Eletrojet height of current in km, must be >0, no default allowed
ejet_center_deg  : Latitude of center of electrojet in degrees, no default allowed

addfile          : GIC updates to Base Case file name ('addfile_optn' determines type of
                   file created) (blank by default, no file created)
purgfile         : RDCH file to remove GIC updates from GIC updated case in working memory to set
                   it back to Base Case network condition (blank by default, no file created)
rnwkfile         : GIC resistive network raw file. This represents the network used to calculate
                   GIC flow (blank by default, no file created)
pygicfile        : GIC Results map data file for given Efield magnitude and degrees OR given Efield magnitude
                   and degrees which give maximum Var losses if degree scan is performed.
                   This is used by GICMAPS to plot GIC results on network map.
                   =nooutput, by default, no file created.

Following arguments used to define GIC study subsystem.
basekv           : list of two elements ([] by default)
                   = basekv[0] is the minimum base kV limit.
                   = basekv[1] is the maximum base kV limit.
areas            : list of areas to consider in subsystem  ([] by default)
buses            : list of buses to consider in subsystem  ([] by default)
owners           : list of owners to consider in subsystem ([] by default)
zones            : list of zones to consider in subsystem  ([] by default)

Following arguments used to define local GMD hot spots subsystem.
basekv_local     : list of two elements ([] by default)
                   = basekv[0] is the minimum base kV limit.
                   = basekv[1] is the maximum base kV limit.
areas_local      : list of areas to consider in subsystem  ([] by default)
buses_local      : list of buses to consider in subsystem  ([] by default)
owners_local     : list of owners to consider in subsystem ([] by default)
zones_local      : list of zones to consider in subsystem  ([] by default)

Following arguments used to solve power flow after adding GIC reactive power loads to base case.
(Note: Ensure that the base case used in GIC calculations is a converged power flow solution case.)
pf_itmxn   : Newton solution iteration limit, allowed >=0, default=program Newton solution iterations
pf_toln    : Newton solution tolerance (largest MW and MVAR mismatch), allowed>=0,
             default=program Newton solution tolerance
pf_tap     : tap adjustment flag, default=program tap adjustment option
             0 Lock taps; 1 enable stepping adjustment; 2 enable direct adjustment
pf_area    : area interchange adjustment flag, default=program area interchange adjustment option
             0 disable, 1 enable using tie line flows only; 2 enable using tie line flows and loads
pf_phshft  : phase shift adjustment flag, default=program phase shift adjustment option
             0 disable, 1 enable
pf_dctap   : dc tap adjustment flag, default=program dc tap adjustment option
             0 disable, 1 enable
pf_swsh    : switched shunt adjustment flag, default=program switched shunt adjustment option
             0 disable, 1 enable, 2 enable continuous mode, disable discrete mode
pf_flat    : flat start flag, default=0
             0 do not flat start, 1 flat start
pf_varlmt  : var limit flag, default=99
             0 apply var limits immediately
             >0 apply var limits on iteration n (or sooner if mismatch gets small)
             -1 ignore var limits
pf_nondiv  : non-divergent solution flag, default=program non-divergent solution option
             0 disable, 1 enable

Results of the GIC calculations are stored in following Python objects:
Following shows how to access results when calculations are done for only one 'efield_deg' angle.
See Note 2 below, on how to access results when calculations are done for more than one angles.

gicobj.ierr  -> =0 for no error, else error occurred

gicobj.misc.efield_mag         -> Electric field magnitude
gicobj.misc.efield_deg         -> Electric field direction
gicobj.misc.efield_mag_local   -> Electric field magnitude of local GMD hot spots
gicobj.misc.efield_deg_local   -> Electric field direction of local GMD hot spots
gicobj.misc.tielevels          -> Subsystem tie levels
gicobj.misc.study_year         -> Benchmark Event study year
gicobj.misc.efield_unit        -> Electric field magnitude unit
                                  ('v/km' or 'v/mi')
gicobj.misc.efield_type        -> Electric field type
                                  ('uniform' or 'benchmark' or 'nonuniform')
gicobj.misc.gic2mvar_optn      -> Electric field type
                                  ('kfactors')
gicobj.misc.earth_model_name   -> Earth model name
gicobj.misc.scan_storm_event   -> Scan storm event scenarios option
                                  ('' or 'scan_deg')
gicobj.misc.power_flow_optn    -> Solve Power Flow with GIC losses added to the base case option
                                  ('' or 'fdns' or'fnsl' or 'nsol')
gicobj.misc.power_flow_optn    -> Solve Power Flow with GIC losses added to the base case option
gicobj.misc.ejet_million_amps  -> Eletrojet current in million amperes
gicobj.misc.ejet_halfwidth_km  -> Eletrojet Cauchy distribution half-width in km
gicobj.misc.ejet_period_min    -> Eletrojet period of variation in minutes
gicobj.misc.ejet_height_km     -> Eletrojet height of current in km
gicobj.misc.ejet_center_deg    -> Latitude of center of electrojet in degrees
gicobj.misc.nbus_study         -> Numbers of buses in study subsystem
gicobj.misc.nsubstation_study  -> Numbers of substations in study subsystem
gicobj.misc.nbranch_study      -> Numbers of non-transformer branches in study subsystem
gicobj.misc.ntransformer_study -> Numbers of transformers in study subsystem
gicobj.misc.longitude_min      -> Minimum longitude among all substations
gicobj.misc.longitude_max      -> Maximum longitude among all substations
gicobj.misc.latitude_min       -> Minimum latitude  among all substations
gicobj.misc.latitude_max       -> Maximum latitude  among all substations
gicobj.misc.distance_min       -> Minimum (non zero) distance among all branches
gicobj.misc.distance_max       -> Maximum distance among all branches

gicobj.bus[eachbus].substation -> Substation number of bus
gicobj.bus[eachbus].dcvolts    -> Bus DC voltage in Volts
                                 (real value for Uniform and Benchmark, complex value for Nonuniform)
gicobj.bus[eachbus].basekv     -> Bus Base voltage in kV
gicobj.bus[eachbus].vpu_base   -> Base case bus voltage in pu (initial solved working case bus voltages)
gicobj.bus[eachbus].vpu_gic    -> Working case + GIC Loads,  power flow solution bus voltages in pu
    eachbus is a bus number in study subsystem

gicobj.substation[eachss].name      -> Substation name (from GIC data file)
gicobj.substation[eachss].latitude  -> Substation latitude in degrees (from GIC data file)
gicobj.substation[eachss].longitude -> Substation longitude in degrees (from GIC data file)
gicobj.substation[eachss].dcvolts   -> Substation DC voltage in Volts
                                      (real value for Uniform and Benchmark, complex value for Nonuniform)
gicobj.substation[eachss].gic       -> GIC flows in substation in Amps, flowing from Bus to Ground
                                      (real value for Uniform and Benchmark, complex value for Nonuniform)
gicobj.substation[eachss].mvar      -> Sum of reactive power losses for all transformers
                                       connected at this substation
    eachss is a substation number in study subsystem

gicobj.branch[eachbrn].distance -> Non-transformer branch distance.
                                   If efield_unit is V/km, distance is in kilometers.
                                   If efield_unit is V/mi, distance is in miles.
gicobj.branch[eachbrn].gic      -> GIC flows in branch in Amps/Phase, flowing from 'From Bus' to 'To Bus'
                                   (real value for Uniform and Benchmark, complex value for Nonuniform)
    eachbrn = (fromBus,Tobus,ckt) is a tuple identifying non-transformer branch in study subsystem

gicobj.fixedshunt[eachfxsh].gic -> GIC flows in bus fixed shunt in Amps/Phase, flowing from Bus to Ground
                                   (real value for Uniform and Benchmark, complex value for Nonuniform)
    eachfxsh = (Bus,ckt) is a tuple identifying fixed shunt in study subsystem

gicobj.transformer[eachtrn].wdg1_auto    -> Identifying if winding 1 is part of auto-transformer
                                            =0 for not auto transformer winding
                                            =1 for auto transformer common winding
                                            =2 for auto transformer series winding
gicobj.transformer[eachtrn].wdg2_auto    -> Same as wdg1_auto, but for winding 2
gicobj.transformer[eachtrn].wdg3_auto    -> Same as wdg1_auto, but for winding 3
    When wdg1_auto = wdg2_auto = wdg3_auto = 0, transformer is a not an auto transformer.
gicobj.transformer[eachtrn].wdg1_gic     -> GIC flows in winding 1 in Amps/Phase, flowing from Bus to Neutral
                                            (real value for Uniform and Benchmark, complex value for Nonuniform)
gicobj.transformer[eachtrn].wdg2_gic     -> GIC flows in winding 2 in Amps/Phase, flowing from Bus to Neutral
                                            (real value for Uniform and Benchmark, complex value for Nonuniform)
gicobj.transformer[eachtrn].wdg3_gic     -> GIC flows in winding 3 in Amps/Phase, flowing from Bus to Neutral
                                            (real value for Uniform and Benchmark, complex value for Nonuniform)
gicobj.transformer[eachtrn].eff_gic      -> Effective GIC flow in transformer in Amps/Phase
gicobj.transformer[eachtrn].kfactor      -> Transformer GIC to Mvar conversion Kfactor
gicobj.transformer[eachtrn].kfactor_type -> Kfactor type
                                            =0 for 'default'
                                            =1 for 'user' specfied in GIC data file
gicobj.transformer[eachtrn].qloss        -> Transformer Mvar losses
    eachtrn = (wdg1bus, wdg2bus, wdg3bus, ckt) is a tuple identifying transformer in study subsystem
    wdg3bus = 0 for two winding transformers

gicobj.qtotal.wdg2_normal -> Total Mvar losses for all two winding non-auto transformers in study subsystem
gicobj.qtotal.wdg2_auto   -> Total Mvar losses for all two winding auto transformers in study subsystem
gicobj.qtotal.wdg3_normal -> Total Mvar losses for all three winding non-auto transformers in study subsystem
gicobj.qtotal.wdg3_auto   -> Total Mvar losses for all three winding auto transformers in study subsystem
gicobj.qtotal.total       -> Total Mvar losses for all transformers in study subsystem

gicobj.pf_solved.flag -> Power flow solution convergence flag
gicobj.pf_solved.cond -> Power flow solution convergence description
      When scan_storm_event = 'scan_deg', then pf_solved.flag and pf_solved.cond are for
      storm direction corresponding to maximum reactive power losses.

gicobj.maxq                        -> Maximum Total Mvar losses from all studied Electric field directions
                                      (=None when efield_type='nonuniform')
gicobj.efield_deg_for_maxq         -> Electric field directions for maximum Total Mvar losses
                                      This could be one angle or list of angles.
                                      (=None when efield_type='nonuniform')
gicobj.ordered_efield_deg_per_maxq -> Electric field directions in descending order of Maximum Total Mvar losses
                                      This could be one angle or list of angles.
                                      (=[] when efield_type='nonuniform')

When storm orientation scan is performed, for each storm orientation, total Mvar losses are accessed as below.
(gicobj.deg_scan_qtotal={} when efield_type='nonuniform')
gicobj.deg_scan_qtotal[deg].wdg2_normal -> Losses for all two winding non-auto transformers at orientation angle 'deg'
gicobj.deg_scan_qtotal[deg].wdg2_auto   -> Losses for all two winding auto transformers at orientation angle 'deg'
gicobj.deg_scan_qtotal[deg].wdg3_normal -> Losses for all three winding non-auto transformers at orientation angle 'deg'
gicobj.deg_scan_qtotal[deg].wdg3_auto   -> Losses for all three winding auto transformers at orientation angle 'deg'
gicobj.deg_scan_qtotal[deg].total       -> Total transformer losses at orientation angle 'deg'

Note 1:
Any of these Python objects can be accessed with case insensitive attributes or as dictionary keys.
So following examples for accessing bus results are allowed.
    gicobj.bus[eachbus].dcvolts     or  gicobj.bus[eachbus]['dcvolts']
    gicobj.bus[eachbus].DCvolts     or  gicobj.bus[eachbus]['DCvolts']
    gicobj.bus[eachbus].substation  or  gicobj.bus[eachbus]['substation']
    gicobj.bus[eachbus].suBSTation  or  gicobj.bus[eachbus]['suBSTation']
In case of nonuniform efield calculations, real and imaginary of dcvolts is accessed as:
    gicobj.bus[eachbus].dcvolts.real  or  gicobj.bus[eachbus]['dcvolts'].real
    gicobj.bus[eachbus].dcvolts.imag  or  gicobj.bus[eachbus]['dcvolts'].imag
"""

    def __init__(self, savfile, gicfile, efield_mag, efield_deg, **kwds):
        """"""
        self.ierr = True
        savfile = _check_file_no_exec(savfile, ext='.sav', desc='PSSE Saved Case', type='read')
        if not savfile:
            return
        else:
            self.savfile = savfile
            gicfile = _check_file_no_exec(gicfile, ext='.gic', desc='PSSE GIC Data', type='read')
            if not gicfile:
                return
            self.gicfile = gicfile
            kwdslower = {}
            for k, v in kwds.items():
                klow = k.lower()
                kwdslower[klow] = v

            _allowed_kwds_dict = {'tielevels': 0, 
               'study_year': 0, 'thermal_ana_optn': 0, 'substation_r': 0.1, 
               'branch_xbyr': 30.0, 'transformer_xbyr': 30.0, 'efield_mag_local': 0.0, 'efield_deg_local': 0.0, 'efield_type': 'uniform', 
               'efield_unit': 'v/km', 'addfile_optn': 'rdch', 'gic2mvar_optn': 'kfactors', 'earth_model_name': '', 
               'scan_storm_event': '', 'power_flow_optn': '', 'ejet_million_amps': 0.0, 
               'ejet_halfwidth_km': 0.0, 'ejet_period_min': 0.0, 'ejet_height_km': 0.0, 'ejet_center_deg': 0.0, 'addfile': '', 
               'purgfile': '', 'rnwkfile': '', 'pygicfile': 'nooutput', 'basekv': [], 'areas': [], 'buses': [], 'owners': [], 'zones': [], 'basekv_local': [], 'areas_local': [], 'buses_local': [], 'owners_local': [], 'zones_local': [], 'pf_itmxn': _BIGINT, 
               'pf_toln': _BIGREL, 'pf_tap': _BIGINT, 'pf_area': _BIGINT, 'pf_phshft': _BIGINT, 'pf_dctap': _BIGINT, 'pf_swsh': _BIGINT, 
               'pf_flat': _BIGINT, 'pf_varlmt': _BIGINT, 'pf_nondiv': _BIGINT}
            for key, val in _allowed_kwds_dict.items():
                if key in kwdslower:
                    vin = kwdslower[key]
                    if type(vin) in [int, float, list, tuple]:
                        v = vin
                    else:
                        try:
                            v = vin.lower()
                        except:
                            v = vin

                    setattr(self, key, v)
                else:
                    setattr(self, key, val)

            del kwdslower
            self.efield_mag = efield_mag
            self.efield_deg = efield_deg
            self.bus = {}
            self.substation = {}
            self.branch = {}
            self.fixedshunt = {}
            self.transformer = {}
            self.qtotal = None
            self.ncasebus = None
            self.ierr, rdct = self._run_pssaccss_gic()
            if not self.ierr:
                self._arrange_as_casless_dict(rdct)
            return

    def _run_pssaccss_gic(self):
        ierr = psspy.case(self.savfile)
        if ierr:
            return (ierr, None)
        else:
            if not self.ncasebus:
                ierr, self.ncasebus, self.ncasebrn, self.ncasetrn = pssaccss.gic_size()
                if ierr:
                    return (ierr, None)
            if self.basekv or self.areas or self.buses or self.owners or self.zones:
                sidarg = 3
                allarg = 0
                usekv = 0
                if self.basekv:
                    usekv = 1
                numarea, numbus, numowner, numzone = (
                 len(self.areas), len(self.buses), len(self.owners), len(self.zones))
                ierr = psspy.bsys(sidarg, usekv, self.basekv, numarea, self.areas, numbus, self.buses, numowner, self.owners, numzone, self.zones)
            else:
                sidarg = 0
                allarg = 1
            if self.basekv_local or self.areas_local or self.buses_local or self.owners_local or self.zones_local:
                sid_local = 11
                usekv = 0
                if self.basekv:
                    usekv = 1
                numarea, numbus, numowner, numzone = (
                 len(self.areas_local), len(self.buses_local), len(self.owners_local), len(self.zones_local))
                ierr = psspy.bsys(sid_local, usekv, self.basekv_local, numarea, self.areas_local, numbus, self.buses_local, numowner, self.owners_local, numzone, self.zones_local)
            else:
                sid_local = 0
            if self.addfile_optn == 'sav':
                add_fextn = '.sav'
            else:
                add_fextn = '.raw'
            addfile = self._fname_add_suffix_deg_check_extn(self.addfile, extn=add_fextn)
            purgfile = self._fname_add_suffix_deg_check_extn(self.purgfile, extn='.raw')
            rnwkfile = self._fname_add_suffix_deg_check_extn(self.rnwkfile, extn='.raw')
            intgoptns = [
             self.tielevels, self.study_year, sid_local, self.thermal_ana_optn]
            realoptns = [self.efield_mag, self.efield_deg, self.substation_r, self.branch_xbyr, self.transformer_xbyr, self.efield_mag_local, self.efield_deg_local]
            charoptns = [self.efield_type, self.efield_unit, self.addfile_optn, self.gic2mvar_optn, self.earth_model_name, self.scan_storm_event, self.power_flow_optn]
            ejetoptns = [self.ejet_million_amps, self.ejet_halfwidth_km, self.ejet_period_min, self.ejet_height_km, self.ejet_center_deg]
            fileoptns = [self.gicfile, addfile, purgfile, rnwkfile, self.pygicfile]
            if self.pf_itmxn < _BIGINT or self.pf_toln < _BIGREL:
                intgar = [_BIGINT for i in range(5)]
                realar = [_BIGREL for i in range(19)]
                if self.pf_itmxn < _BIGINT:
                    intgar[1] = self.pf_itmxn
                if self.pf_toln < _BIGREL:
                    realar[5] = self.pf_toln
                psspy.solution_parameters_4(intgar, realar)
            if self.pf_tap < _BIGINT:
                psspy.tap_adjustment(self.pf_tap)
            if self.pf_area < _BIGINT:
                psspy.control_area_interchange(self.pf_area)
            if self.pf_phshft < _BIGINT:
                psspy.phase_shift_adjustment(self.pf_phshft)
            if self.pf_dctap < _BIGINT:
                psspy.dc_tap_adjustment(self.pf_dctap)
            if self.pf_swsh < _BIGINT:
                psspy.switched_shunt_adjustment(self.pf_swsh)
            if self.pf_nondiv < _BIGINT:
                psspy.non_divergent(self.pf_nondiv)
            rdct = pssaccss.gic(sidarg, allarg, intgoptns, realoptns, charoptns, ejetoptns, fileoptns, self.ncasebus, self.ncasebrn, self.ncasetrn)
            psspy.bsysdef(sidarg, 0)
            psspy.bsysdef(sid_local, 0)
            return (
             False, rdct)

    def _arrange_as_casless_dict(self, rdct):
        self.ierr = rdct['ierr']
        if self.ierr:
            return
        misc = {'efield_mag': (rdct['realoptns'][0]), 'efield_deg': (rdct['realoptns'][1]), 'efield_mag_local': (rdct['realoptns'][5]), 
           'efield_deg_local': (rdct['realoptns'][6]), 
           'tielevels': (rdct['intgoptns'][0]), 
           'study_year': (rdct['intgoptns'][1]), 
           'efield_type': (rdct['charoptns'][0].strip()), 
           'efield_unit': (rdct['charoptns'][1].strip()), 
           'gic2mvar_optn': (rdct['charoptns'][3].strip()), 
           'earth_model_name': (rdct['charoptns'][4].strip()), 
           'scan_storm_event': (rdct['charoptns'][5].strip()), 
           'power_flow_optn': (rdct['charoptns'][6].strip()), 
           'ejet_million_amps': (rdct['ejetoptns'][0]), 
           'ejet_halfwidth_km': (rdct['ejetoptns'][1]), 
           'ejet_period_min': (rdct['ejetoptns'][2]), 
           'ejet_height_km': (rdct['ejetoptns'][3]), 
           'ejet_center_deg': (rdct['ejetoptns'][4]), 
           'nbus_study': (rdct['nbus']), 
           'nsubstation_study': (rdct['nsubstn']), 
           'nbranch_study': (rdct['nbrn']), 
           'ntransformer_study': (rdct['ntrn'])}
        efld_typ = misc['efield_type']
        bus = {}
        for eachbus, ss, bkv, dcv, vpu_base, vpu_gic in zip(rdct['bus_intg'][0], rdct['bus_intg'][1], rdct['bus_real'][0], rdct['bus_cplx'][0], rdct['bus_cplx'][1], rdct['bus_cplx'][2]):
            if efld_typ == 'nonuniform':
                vlt = dcv
            else:
                vlt = dcv.real
            bus[eachbus] = {'substation': ss, 'dcvolts': vlt, 
               'basekv': bkv, 
               'vpu_base': vpu_base, 
               'vpu_gic': vpu_gic}

        temp_lon = {}
        temp_lat = {}
        substation = {}
        for ss, nam, lat, lon, dcv, amp, erthmdl in zip(rdct['substn_intg'], rdct['substn_nam'], rdct['substn_real'][0], rdct['substn_real'][1], rdct['substn_cplx'][0], rdct['substn_cplx'][1], rdct['substn_earthmdl']):
            if lon not in temp_lon:
                temp_lon[lon] = 1
            if lat not in temp_lat:
                temp_lat[lat] = 1
            if efld_typ == 'nonuniform':
                vlt = dcv
                cur = amp
            else:
                vlt = dcv.real
                cur = amp.real
            substation[ss] = {'name': nam, 'latitude': lat, 
               'longitude': lon, 
               'dcvolts': vlt, 
               'gic': cur, 
               'mvar': 0.0, 
               'earth_mdl': erthmdl}

        lon_list = temp_lon.keys()
        lat_list = temp_lat.keys()
        lon_list.sort()
        lat_list.sort()
        misc['longitude_min'] = math.floor(lon_list[0])
        misc['longitude_max'] = math.ceil(lon_list[-1])
        misc['latitude_min'] = math.floor(lat_list[0])
        misc['latitude_max'] = math.ceil(lat_list[-1])
        del temp_lon
        del temp_lat
        del lon_list
        del lat_list
        temp_dist = {}
        branch = {}
        for i, j, ckt, dist, indv, ejetEe, amp in zip(rdct['brn_intg'][0], rdct['brn_intg'][1], rdct['brn_ckt'], rdct['brn_real'][0], rdct['brn_cplx'][0], rdct['brn_cplx'][1], rdct['brn_cplx'][2]):
            if dist not in temp_dist:
                temp_dist[dist] = 1
            if efld_typ == 'nonuniform':
                vlt = indv
                ee = ejetEe
                cur = amp
            else:
                vlt = indv.real
                ee = ejetEe.real
                cur = amp.real
            branch[(i, j, ckt)] = {'distance': dist, 'induced_voltage': vlt, 
               'ejet_ee': ee, 
               'gic': cur}

        dist_list = temp_dist.keys()
        dist_list.sort()
        for dist in dist_list:
            dist_min = dist
            if dist_min:
                break

        misc['distance_min'] = dist_min
        misc['distance_max'] = dist_list[-1]
        del temp_dist
        del dist_list
        transformer = {}
        for i, j, k, ckt, iauto, jauto, kauto, kftr_typ, iamp, jamp, kamp, effamps, kftr, qloss in zip(rdct['trn_intg'][0], rdct['trn_intg'][1], rdct['trn_intg'][2], rdct['trn_ckt'], rdct['trn_intg'][3], rdct['trn_intg'][4], rdct['trn_intg'][5], rdct['trn_intg'][6], rdct['trn_cplx'][0], rdct['trn_cplx'][1], rdct['trn_cplx'][2], rdct['trn_real'][0], rdct['trn_real'][1], rdct['trn_real'][2]):
            if efld_typ == 'nonuniform':
                cur_i = iamp
                cur_j = jamp
                cur_k = kamp
            else:
                cur_i = iamp.real
                cur_j = jamp.real
                cur_k = kamp.real
            transformer[(i, j, k, ckt)] = {'wdg1_auto': iauto, 'wdg2_auto': jauto, 
               'wdg3_auto': kauto, 
               'wdg1_gic': cur_i, 
               'wdg2_gic': cur_j, 
               'wdg3_gic': cur_k, 
               'eff_gic': effamps, 
               'kfactor': kftr, 
               'kfactor_type': kftr_typ, 
               'qloss': qloss}
            ss = 0
            if i in bus:
                ss = bus[i]['substation']
            if not ss:
                if j in bus:
                    ss = bus[j]['substation']
            if not ss and k:
                if k in bus:
                    ss = bus[k]['substation']
            if ss:
                substation[ss]['mvar'] += qloss

        fixedshunt = {}
        for i, ckt, amp in zip(rdct['fxsh_intg'], rdct['fxsh_ckt'], rdct['fxsh_cplx'][0]):
            if efld_typ == 'nonuniform':
                cur = amp
            else:
                cur = amp.real
            fixedshunt[(i, ckt)] = {'gic': cur}

        qtotal = {'wdg2_normal': (rdct['qtotal'][0]), 'wdg2_auto': (rdct['qtotal'][1]), 
           'wdg3_normal': (rdct['qtotal'][2]), 
           'wdg3_auto': (rdct['qtotal'][3]), 
           'total': (rdct['qtotal'][4])}
        self.misc = _Dict_caseless_bunch(misc)
        for k, vdict in bus.items():
            self.bus[k] = _Dict_caseless_bunch(vdict)

        for k, vdict in substation.items():
            self.substation[k] = _Dict_caseless_bunch(vdict)

        for k, vdict in branch.items():
            self.branch[k] = _Dict_caseless_bunch(vdict)

        for k, vdict in transformer.items():
            self.transformer[k] = _Dict_caseless_bunch(vdict)

        for k, vdict in fixedshunt.items():
            self.fixedshunt[k] = _Dict_caseless_bunch(vdict)

        self.qtotal = _Dict_caseless_bunch(qtotal)
        self.pf_solved = _Dict_caseless_bunch({'flag': (rdct['solved_icnvrg']), 'cond': (rdct['solved_cond'].strip())})
        self.deg_scan_qtotal = {}
        if efld_typ == 'nonuniform':
            self.ordered_efield_deg_per_maxq = []
            self.maxq = None
            self.efield_deg_for_maxq = None
        else:
            tmp_qtotal = {}
            for i in range(rdct['deg_scan_ndeg']):
                deg = rdct['deg_scan_qloss'][0][i]
                q_2nrml = rdct['deg_scan_qloss'][1][i]
                q_2auto = rdct['deg_scan_qloss'][2][i]
                q_3nrml = rdct['deg_scan_qloss'][3][i]
                q_3auto = rdct['deg_scan_qloss'][4][i]
                qt = rdct['deg_scan_qloss'][5][i]
                qtotal = {'wdg2_normal': q_2nrml, 'wdg2_auto': q_2auto, 
                   'wdg3_normal': q_3nrml, 
                   'wdg3_auto': q_3auto, 
                   'total': qt}
                if qt in tmp_qtotal:
                    jnk = tmp_qtotal[qt]
                    if type(jnk) == list:
                        tmp_qtotal[qt].append(deg)
                    else:
                        tmp_qtotal[qt] = [
                         jnk, deg]
                else:
                    tmp_qtotal[qt] = deg
                self.deg_scan_qtotal[deg] = _Dict_caseless_bunch(qtotal)

            qlist = list(tmp_qtotal.keys())
            qlist.sort()
            qlist.reverse()
            degord = []
            for q in qlist:
                d = tmp_qtotal[q]
                if type(d) == list:
                    degord.extend(d)
                else:
                    degord.append(d)

            self.ordered_efield_deg_per_maxq = degord[:]
            self.maxq = qlist[0]
            self.efield_deg_for_maxq = degord[0]
            del degord
        del misc
        del bus
        del substation
        del branch
        del transformer
        del qtotal
        return

    def _fname_add_suffix_deg_check_extn(self, fnam, extn=''):
        if not fnam:
            retv = fnam
        else:
            pn, x = os.path.splitext(fnam)
            if extn:
                x = extn
            retv = pn + x
        return retv

    def _get_formatted_real_value(self, vin):
        if vin < _BIGREL:
            rstr = '%12.5f' % vin
        else:
            rstr = '            '
        return rstr

    def _get_formatted_real_value1(self, vin):
        if vin < _BIGREL:
            rstr = '%12.5f' % vin
        else:
            rstr = '     0.00000'
        return rstr

    def _get_kfactor_type(self, vin):
        if vin == 1:
            rstr = '   User'
        else:
            rstr = 'Default'
        return rstr

    def _get_valid_real_value(self, vin):
        if vin < _BIGREL:
            vout = vin
        else:
            vout = ''
        return vout

    def _text_report(self, rptfile):
        if self.ierr:
            return
        else:
            misc = self.misc
            bus = self.bus
            substation = self.substation
            branch = self.branch
            fixedshunt = self.fixedshunt
            transformer = self.transformer
            qtotal = self.qtotal
            if rptfile:
                rptfile = self._fname_add_suffix_deg_check_extn(rptfile, extn='.txt')
                rptfobj = open(rptfile, 'w')
                report = rptfobj.write
            else:
                report = sys.stdout.write
            txt = self._report_hdr()
            report(txt)
            efield_type = misc.efield_type
            txt = ''
            if self.basekv or self.areas or self.buses or self.owners or self.zones:
                txt += '\n Subsystem used for GIC studiies is defined as:\n'
                if self.basekv:
                    txt += '     Voltage = %s\n' % str(self.basekv)
                if self.areas:
                    txt += '     Areas   = %s\n' % str(self.areas)
                if self.buses:
                    txt += '     Buses   = %s\n' % str(self.buses)
                if self.owners:
                    txt += '     Owners  = %s\n' % str(self.owners)
                if self.zones:
                    txt += '     Zones   = %s\n' % str(self.zones)
                txt += '     Subsystem Inter tie Levels = %d\n' % self.tielevels
            else:
                txt += '\n Subsystem used for GIC studiies comprises entire network.\n'
            txt += '\n Number of buses in study subsystem        = %d\n' % misc.nbus_study
            txt += ' Number of substations in study subsystem  = %d\n' % misc.nsubstation_study
            txt += ' Number of branches in study subsystem     = %d\n' % misc.nbranch_study
            txt += ' Number of transformers in study subsystem = %d\n' % misc.ntransformer_study
            report(txt)
            buslist = bus.keys()
            buslist.sort()
            if self.pf_solved.flag == 0:
                txt = '\n Bus GIC Calculation DC and Power Flow Solution AC Voltages\n'
                txt += '     Base case voltages are initial solved working case bus voltages.\n'
                txt += '     GIC case voltages are base case + GIC loads power flow solution bus voltages.\n'
                if efield_type == 'nonuniform':
                    txt += '                    |------DC Voltage-------|  |-Base Case AC Voltage--|  |--GIC Case AC Voltage--|\n'
                    txt += '    Bus Substation  |---Re(V)--| |--Im(V)---|  |-Mag(pu)--| |Angle(deg)|  |-Mag(pu)--| |Angle(deg)|\n'
                else:
                    txt += '                    |--GIC DC--|  |-Base Case AC Voltage--|  |--GIC Case AC Voltage--|\n'
                    txt += '    Bus Substation   Voltage (V)  |-Mag(pu)--| |Angle(deg)|  |-Mag(pu)--| |Angle(deg)|\n'
                report(txt)
                if efield_type == 'nonuniform':
                    for eachbus in buslist:
                        v = bus[eachbus].vpu_base
                        vpu_base_mag = abs(v)
                        vpu_base_ang = math.degrees(math.atan(v.imag / v.real))
                        v = bus[eachbus].vpu_gic
                        vpu_gic_mag = abs(v)
                        vpu_gic_ang = math.degrees(math.atan(v.imag / v.real))
                        txt = ' %6d     %6d  %12.5f %12.5f      %8.5f    %9.4f      %8.5f    %9.4f\n' % (
                         eachbus, bus[eachbus].substation, bus[eachbus].dcvolts.real, bus[eachbus].dcvolts.imag,
                         vpu_base_mag, vpu_base_ang, vpu_gic_mag, vpu_gic_ang)
                        report(txt)

                else:
                    for eachbus in buslist:
                        v = bus[eachbus].vpu_base
                        vpu_base_mag = abs(v)
                        vpu_base_ang = math.degrees(math.atan(v.imag / v.real))
                        v = bus[eachbus].vpu_gic
                        vpu_gic_mag = abs(v)
                        vpu_gic_ang = math.degrees(math.atan(v.imag / v.real))
                        txt = ' %6d     %6d  %12.5f      %8.5f    %9.4f      %8.5f    %9.4f\n' % (
                         eachbus, bus[eachbus].substation, bus[eachbus].dcvolts,
                         vpu_base_mag, vpu_base_ang, vpu_gic_mag, vpu_gic_ang)
                        report(txt)

            else:
                txt = '\n Bus DC Voltages\n'
                if efield_type == 'nonuniform':
                    txt += '    Bus Substation  |---Re(V)--| |--Im(V)---|\n'
                else:
                    txt += '    Bus Substation   Voltage (V)\n'
                report(txt)
                if efield_type == 'nonuniform':
                    for eachbus in buslist:
                        txt = ' %6d     %6d  %12.5f %12.5f\n' % (eachbus, bus[eachbus].substation, bus[eachbus].dcvolts.real, bus[eachbus].dcvolts.imag)
                        report(txt)

                else:
                    for eachbus in buslist:
                        txt = ' %6d     %6d  %12.5f\n' % (eachbus, bus[eachbus].substation, bus[eachbus].dcvolts)
                        report(txt)

            txt = '\n Substations DC Voltages and GIC Flows, flowing from Bus to Substation Ground\n'
            if efield_type == 'nonuniform':
                txt += ' Substation Name                                     Latitude(deg) Longitude(deg)  |---Re(V)--| |--Im(V)---| |---Re(A)--| |--Im(A)---|\n'
            else:
                txt += ' Substation Name                                     Latitude(deg) Longitude(deg)   Voltage (V)    GIC(Amps)\n'
            report(txt)
            sslist = substation.keys()
            sslist.sort()
            if efield_type == 'nonuniform':
                for ss in sslist:
                    txt = '     %6d %-40s  %12.6f   %12.6f  %12.5f %12.5f %12.5f %12.5f\n' % (ss, substation[ss].name,
                     substation[ss].latitude, substation[ss].longitude, substation[ss].dcvolts.real,
                     substation[ss].dcvolts.imag, substation[ss].gic.real, substation[ss].gic.imag)
                    report(txt)

            else:
                for ss in sslist:
                    txt = '     %6d %-40s  %12.6f   %12.6f  %12.5f %12.5f\n' % (ss, substation[ss].name,
                     substation[ss].latitude, substation[ss].longitude, substation[ss].dcvolts,
                     substation[ss].gic)
                    report(txt)

            if misc.efield_unit == 'v/km':
                unt = 'km'
            else:
                unt = 'mi'
            txt = '\n GIC flow in Non-Transformer Branches, flowing from From Bus to To Bus\n'
            if efield_type == 'nonuniform':
                txt += '                                  |-------Per Phase-------| |------Three Phase------|\n'
                txt += ' FromBus  ToBus Ckt  Distance(%s) |---Re(A)--| |--Im(A)---| |---Re(A)--| |--Im(A)---|\n' % unt
            else:
                txt += ' FromBus  ToBus Ckt  Distance(%s) per-Phase(A)   3-Phase(A)\n' % unt
            report(txt)
            brnlist = branch.keys()
            brnlist.sort()
            if efield_type == 'nonuniform':
                for brn in brnlist:
                    ir = branch[brn].gic.real
                    ix = branch[brn].gic.imag
                    txt = '  %6d %6d  %-2s  %12.5f %12.5f %12.5f %12.5f %12.5f\n' % (brn[0], brn[1], brn[2],
                     branch[brn].distance, ir, ix, 3 * ir, 3 * ix)
                    report(txt)

            else:
                for brn in brnlist:
                    txt = '  %6d %6d  %-2s  %12.5f %12.5f %12.5f\n' % (brn[0], brn[1], brn[2],
                     branch[brn].distance, branch[brn].gic, 3 * branch[brn].gic)
                    report(txt)

            txt = '\n GIC flow in Bus Shunts, flowing from Bus to Substation ground bus\n'
            if fixedshunt:
                if efield_type == 'nonuniform':
                    txt += '              |-------Per Phase-------| |------Three Phase------|\n'
                    txt += '     Bus Ckt  |---Re(A)--| |--Im(A)---| |---Re(A)--| |--Im(A)---|\n'
                else:
                    txt += '     Bus Ckt  per-Phase(A)   3-Phase(A)\n'
                report(txt)
                fxshlist = fixedshunt.keys()
                fxshlist.sort()
                if efield_type == 'nonuniform':
                    for fxsh in fxshlist:
                        ir = fixedshunt[fxsh].gic.real
                        ix = fixedshunt[fxsh].gic.imag
                        txt = '  %6d  %-2s  %12.5f %12.5f %12.5f %12.5f\n' % (fxsh[0], fxsh[1], ir, ix, 3 * ir, 3 * ix)
                        report(txt)

                else:
                    for fxsh in fxshlist:
                        txt = '  %6d  %-2s  %12.5f %12.5f\n' % (fxsh[0], fxsh[1], fixedshunt[fxsh].gic, 3 * fixedshunt[fxsh].gic)
                        report(txt)

            else:
                txt += '        None\n'
                report(txt)
            trnlist = transformer.keys()
            trnlist.sort()
            no_2wdg_nrml = '\n     No two winding transformers in GIC studied network.\n'
            no_2wdg_auto = '\n     No two winding auto transformers in GIC studied network.\n'
            no_3wdg_nrml = '\n     No three winding transformers in GIC studied network.\n'
            no_3wdg_auto = '\n     No three winding auto transformers in GIC studied network.\n'
            txt = '\n Two Winding Transformers: Per Phase GIC flow in windings, flowing from winding Bus to Neutral\n'
            txt += ' Reactive power loss, represented as constant current load on highest voltage bus in power flow\n'
            if efield_type == 'nonuniform':
                txt += '                    |-------Winding 1-------| |-------Winding 2-------|\n'
                txt += '   Ibus   Jbus Ckt  |---Re(A)--| |--Im(A)---| |---Re(A)--| |--Im(A)---|    Effgic(A) Kfactor KftrTyp  Qloss(Mvar)\n'
            else:
                txt += '   Ibus   Jbus Ckt       Igic(A)      Jgic(A)    Effgic(A) Kfactor KftrTyp  Qloss(Mvar)\n'
            report(txt)
            for trn in trnlist:
                kbus = trn[2]
                if kbus:
                    continue
                autoi = transformer[trn].wdg1_auto
                autoj = transformer[trn].wdg2_auto
                if autoi or autoj:
                    continue
                if efield_type == 'nonuniform':
                    ir = self._get_formatted_real_value(transformer[trn].wdg1_gic.real)
                    ix = self._get_formatted_real_value(transformer[trn].wdg1_gic.imag)
                    jr = self._get_formatted_real_value(transformer[trn].wdg2_gic.real)
                    jx = self._get_formatted_real_value(transformer[trn].wdg2_gic.imag)
                else:
                    igic = self._get_formatted_real_value(transformer[trn].wdg1_gic)
                    jgic = self._get_formatted_real_value(transformer[trn].wdg2_gic)
                effgic = self._get_formatted_real_value(transformer[trn].eff_gic)
                qloss = self._get_formatted_real_value(transformer[trn].qloss)
                kftrtyp = self._get_kfactor_type(transformer[trn].kfactor_type)
                if efield_type == 'nonuniform':
                    txt = ' %6d %6d  %-2s  %s %s %s %s %s %7.3f %s %s\n' % (trn[0], trn[1], trn[3], ir, ix, jr, jx, effgic,
                     transformer[trn].kfactor, kftrtyp, qloss)
                else:
                    txt = ' %6d %6d  %-2s  %s %s %s %7.3f %s %s\n' % (trn[0], trn[1], trn[3], igic, jgic, effgic,
                     transformer[trn].kfactor, kftrtyp, qloss)
                report(txt)
                if no_2wdg_nrml:
                    no_2wdg_nrml = ''

            if no_2wdg_nrml:
                report(no_2wdg_nrml)
            txt = '\n Two Winding Auto Transformers: Per Phase GIC flow in windings, flowing from winding Bus to Neutral\n'
            txt += ' Reactive power loss, represented as constant current load on Series Winding bus in power flow\n'
            if efield_type == 'nonuniform':
                txt += '                    |---------Common--------| |---------Series--------|\n'
                txt += ' Common Series Ckt  |---Re(A)--| |--Im(A)---| |---Re(A)--| |--Im(A)---|    Effgic(A) Kfactor KftrTyp  Qloss(Mvar)\n'
            else:
                txt += ' Common Series Ckt Common gic(A) Series gic(A)    Effgic(A) Kfactor KftrTyp  Qloss(Mvar)\n'
            report(txt)
            for trn in trnlist:
                kbus = trn[2]
                if kbus:
                    continue
                autoi = transformer[trn].wdg1_auto
                autoj = transformer[trn].wdg2_auto
                if not autoi or not autoj:
                    continue
                if autoi == 1:
                    ibus = trn[0]
                    jbus = trn[1]
                else:
                    ibus = trn[1]
                    jbus = trn[0]
                if efield_type == 'nonuniform':
                    ir = self._get_formatted_real_value(transformer[trn].wdg1_gic.real)
                    ix = self._get_formatted_real_value(transformer[trn].wdg1_gic.imag)
                    jr = self._get_formatted_real_value(transformer[trn].wdg2_gic.real)
                    jx = self._get_formatted_real_value(transformer[trn].wdg2_gic.imag)
                else:
                    igic = self._get_formatted_real_value(transformer[trn].wdg1_gic)
                    jgic = self._get_formatted_real_value(transformer[trn].wdg2_gic)
                effgic = self._get_formatted_real_value(transformer[trn].eff_gic)
                qloss = self._get_formatted_real_value(transformer[trn].qloss)
                kftrtyp = self._get_kfactor_type(transformer[trn].kfactor_type)
                if efield_type == 'nonuniform':
                    txt = ' %6d %6d  %-2s  %s %s %s %s %s %7.3f %s %s\n' % (ibus, jbus, trn[3], ir, ix, jr, jx, effgic,
                     transformer[trn].kfactor, kftrtyp, qloss)
                else:
                    txt = ' %6d %6d  %-2s  %s  %s %s %7.3f %s %s\n' % (ibus, jbus, trn[3], igic, jgic, effgic,
                     transformer[trn].kfactor, kftrtyp, qloss)
                report(txt)
                if no_2wdg_auto:
                    no_2wdg_auto = ''

            if no_2wdg_auto:
                report(no_2wdg_auto)
            txt = '\n Three Winding Transformers: Per Phase GIC flow in windings, flowing from winding Bus to Neutral\n'
            txt += ' Reactive power loss, represented as constant current load on highest voltage bus in power flow\n'
            if efield_type == 'nonuniform':
                txt += '                           |-------Winding 1-------| |-------Winding 2-------| |-------Winding 3-------|\n'
                txt += '   Ibus   Jbus   Kbus Ckt  |---Re(A)--| |--Im(A)---| |---Re(A)--| |--Im(A)---| |---Re(A)--| |--Im(A)---|    Effgic(A) Kfactor KftrTyp  Qloss(Mvar)\n'
            else:
                txt += '   Ibus   Jbus   Kbus Ckt       Igic(A)      Jgic(A)      Kgic(A)    Effgic(A) Kfactor KftrTyp  Qloss(Mvar)\n'
            report(txt)
            for trn in trnlist:
                kbus = trn[2]
                if not kbus:
                    continue
                autoi = transformer[trn].wdg1_auto
                autoj = transformer[trn].wdg2_auto
                autok = transformer[trn].wdg3_auto
                if autoi or autoj or autok:
                    continue
                if efield_type == 'nonuniform':
                    ir = self._get_formatted_real_value(transformer[trn].wdg1_gic.real)
                    ix = self._get_formatted_real_value(transformer[trn].wdg1_gic.imag)
                    jr = self._get_formatted_real_value(transformer[trn].wdg2_gic.real)
                    jx = self._get_formatted_real_value(transformer[trn].wdg2_gic.imag)
                    kr = self._get_formatted_real_value(transformer[trn].wdg3_gic.real)
                    kx = self._get_formatted_real_value(transformer[trn].wdg3_gic.imag)
                else:
                    igic = self._get_formatted_real_value(transformer[trn].wdg1_gic)
                    jgic = self._get_formatted_real_value(transformer[trn].wdg2_gic)
                    kgic = self._get_formatted_real_value(transformer[trn].wdg3_gic)
                effgic = self._get_formatted_real_value(transformer[trn].eff_gic)
                qloss = self._get_formatted_real_value(transformer[trn].qloss)
                kftrtyp = self._get_kfactor_type(transformer[trn].kfactor_type)
                if efield_type == 'nonuniform':
                    txt = ' %6d %6d %6d  %-2s  %s %s %s %s %s %s %s %7.3f %s %s\n' % (trn[0], trn[1], trn[2], trn[3],
                     ir, ix, jr, jx, kr, kx, effgic, transformer[trn].kfactor, kftrtyp, qloss)
                else:
                    txt = ' %6d %6d %6d  %-2s  %s %s %s %s %7.3f %s %s\n' % (trn[0], trn[1], trn[2], trn[3],
                     igic, jgic, kgic, effgic, transformer[trn].kfactor, kftrtyp, qloss)
                report(txt)
                if no_3wdg_nrml:
                    no_3wdg_nrml = ''

            if no_3wdg_nrml:
                report(no_3wdg_nrml)
            txt = '\n Three Winding Auto Transformers: Per Phase GIC flow in windings, flowing from winding Bus to Neutral\n'
            txt += ' Reactive power loss, represented as constant current load on highest voltage bus in power flow\n'
            if efield_type == 'nonuniform':
                txt += '                           |---------Common--------| |---------Series--------|\n'
                txt += ' Common Series   Kbus Ckt  |---Re(A)--| |--Im(A)---| |---Re(A)--| |--Im(A)---| |---Re(A)--| |--Im(A)---|    Effgic(A) Kfactor KftrTyp  Qloss(Mvar)\n'
            else:
                txt += ' Common Series   Kbus Ckt Common gic(A) Series gic(A)      Kgic(A)    Effgic(A) Kfactor KftrTyp  Qloss(Mvar)\n'
            report(txt)
            for trn in trnlist:
                kbus = trn[2]
                if not kbus:
                    continue
                autoi = transformer[trn].wdg1_auto
                autoj = transformer[trn].wdg2_auto
                if not autoi or not autoj:
                    continue
                if autoi == 1:
                    ibus = trn[0]
                    jbus = trn[1]
                else:
                    ibus = trn[1]
                    jbus = trn[0]
                if efield_type == 'nonuniform':
                    ir = self._get_formatted_real_value(transformer[trn].wdg1_gic.real)
                    ix = self._get_formatted_real_value(transformer[trn].wdg1_gic.imag)
                    jr = self._get_formatted_real_value(transformer[trn].wdg2_gic.real)
                    jx = self._get_formatted_real_value(transformer[trn].wdg2_gic.imag)
                    kr = self._get_formatted_real_value(transformer[trn].wdg3_gic.real)
                    kx = self._get_formatted_real_value(transformer[trn].wdg3_gic.imag)
                else:
                    igic = self._get_formatted_real_value(transformer[trn].wdg1_gic)
                    jgic = self._get_formatted_real_value(transformer[trn].wdg2_gic)
                    kgic = self._get_formatted_real_value(transformer[trn].wdg3_gic)
                effgic = self._get_formatted_real_value(transformer[trn].eff_gic)
                qloss = self._get_formatted_real_value(transformer[trn].qloss)
                kftrtyp = self._get_kfactor_type(transformer[trn].kfactor_type)
                if efield_type == 'nonuniform':
                    txt = ' %6d %6d %6d  %-2s  %s %s %s %s %s %s %s %7.3f %s %s\n' % (ibus, jbus, kbus, trn[3],
                     ir, ix, jr, jx, kr, kx, effgic, transformer[trn].kfactor, kftrtyp, qloss)
                else:
                    txt = ' %6d %6d %6d  %-2s  %s %s %s %s %7.3f %s %s\n' % (ibus, jbus, kbus, trn[3],
                     igic, jgic, kgic, effgic, transformer[trn].kfactor, kftrtyp, qloss)
                report(txt)
                if no_3wdg_auto:
                    no_3wdg_auto = ''

            if no_3wdg_auto:
                report(no_3wdg_auto)
            if no_2wdg_nrml:
                qwdg2_nrml = '        None'
            else:
                qwdg2_nrml = '%12.5f Mvar' % qtotal.wdg2_normal
            if no_2wdg_auto:
                qwdg2_auto = '        None'
            else:
                qwdg2_auto = '%12.5f Mvar' % qtotal.wdg2_auto
            if no_3wdg_nrml:
                qwdg3_nrml = '        None'
            else:
                qwdg3_nrml = '%12.5f Mvar' % qtotal.wdg3_normal
            if no_3wdg_auto:
                qwdg3_auto = '        None'
            else:
                qwdg3_auto = '%12.5f Mvar' % qtotal.wdg3_auto
            txt = '\n Transformer Reactive Power Loss Summary\n'
            txt += ' Two Winding Transformers        = %s\n' % qwdg2_nrml
            txt += ' Two Winding Auto Transformers   = %s\n' % qwdg2_auto
            txt += ' Three Winding Transformers      = %s\n' % qwdg3_nrml
            txt += ' Three Winding Auto Transformers = %s\n' % qwdg3_auto
            txt += '                           Total = %12.5f Mvar\n' % qtotal.total
            report(txt)
            txt = '\n Power Flow Convergence Condition after adding GIC var losses to base case:\n'
            txt += '     %s\n' % self.pf_solved.cond
            report(txt)
            if rptfile:
                rptfobj.close()
                return rptfile
            return
            return

    def _excel_export(self, shtoptns, xlfile, show, overwritesheet):
        if self.ierr:
            return
        import excelpy
        _NROW_AT_A_TIME = 100
        if not xlfile:
            xlfile, x = os.path.split(self.savfile)
        _WORKSHT_SEQ_GIC = ['event', 'bus', 'sub', 'brn', 'fxsh', 'trn', 'qloss']
        if type(shtoptns) in [list, tuple]:
            sheet_optns = shtoptns
        elif type(shtoptns) == str:
            sheet_optns = [
             shtoptns]
        else:
            sheet_optns = []
        do_sheets = []
        if sheet_optns:
            shtlw = [each.lower().strip() for each in sheet_optns]
            for each in _WORKSHT_SEQ_GIC:
                if each in shtlw:
                    do_sheets.append(each)
                    if each == 'trn':
                        do_sheets.append('trnauto')

        if not do_sheets:
            do_sheets = _WORKSHT_SEQ_GIC[:]
            do_sheets.insert(-1, 'trnauto')
        _EXPORT_QTY_GIC = {'event': 'GMD event', 
           'bus': 'bus', 
           'sub': 'substation', 
           'brn': 'branch', 
           'fxsh': 'fixed shunts', 
           'trn': 'transformer', 
           'trnauto': 'auto transformer', 
           'qloss': 'MVAR Losses'}
        if self.misc.efield_unit == 'v/km':
            s_distance = 'Distance(km)'
        else:
            s_distance = 'Distance(mi)'
        _WORKSHT_COLUMN_LABELS_GIC = {'bus': {'pfsolved': {'ub': [['', '', 'GIC DC', 'Base Case AC Voltage', 
                                      '', 
                                      'GIC Case AC Voltage', 
                                      ''],
                                     [
                                      'Bus', 
                                      'Substation', 
                                      'Voltage(V)', 
                                      'Mag(pu)', 
                                      'Angle(deg)', 
                                      'Mag(pu)', 
                                      'Angle(deg)']], 
                                'n': [
                                    [
                                     '', 
                                     '', 'DC Voltage', 
                                     '', 'Base Case AC Voltage', 
                                     '', 'GIC Case AC Voltage', 
                                     ''],
                                    [
                                     'Bus', 
                                     'Substation', 
                                     'Re(V)', 
                                     'Im(V)', 
                                     'Mag(pu)', 
                                     'Angle(deg)', 
                                     'Mag(pu)', 
                                     'Angle(deg)']]}, 
                   'pfno': {'ub': ['Bus', 'Substation', 'DC Voltage(V)'], 'n': [
                                'Bus', 'Substation', 'Re(V)', 'Im(V)']}}, 
           'sub': {'ub': ['Substation', 'Name', 'Latitude(deg)', 'Longitude(deg)', 
                        'Voltage(V)', 'GIC(Amps)'], 'n': [
                       'Substation', 
                       'Name', 'Latitude(deg)', 'Longitude(deg)', 
                       'Re(V)', 'Im(V)', 'Re(A)', 'Im(A)']}, 
           'brn': {'ub': ['FromBus', 'ToBus', 'Ckt', s_distance, 'per-Phase(A)', 
                        '3-Phase(A)'], 'n': [
                       [
                        '', '', 
                        '', '', 'Per Phase', '', 'Three Phase', 
                        ''],
                       [
                        'FromBus', 
                        'ToBus', 'Ckt', s_distance, 'Re(A)', 
                        'Im(A)', 'Re(A)', 'Im(A)']]}, 
           'fxsh': {'ub': ['Bus', 'Ckt', 'per-Phase(A)', '3-Phase(A)'], 'n': [
                        [
                         '', '', 
                         'Per Phase', '', 'Three Phase', 
                         ''],
                        [
                         'Bus', 
                         'Ckt', 'Re(A)', 'Im(A)', 'Re(A)', 
                         'Im(A)']]}, 
           'trn': {'ub': ['Ibus', 'Jbus', 'Kbus', 'Ckt', 'Igic(A)', 'Jgic(A)', 
                        'Kgic(A)', 'Effgic(A)', 'Kfactor', 
                        'KftrTyp', 'Qloss(Mvar)'], 'n': [
                       [
                        '', '', 
                        '', '', 'Winding1', '', 'Winding2', 
                        '', 'Winding3', '', '', '', 
                        '', ''],
                       [
                        'Ibus', 'Jbus', 
                        'Kbus', 'Ckt', 'Re(A)', 'Im(A)', 
                        'Re(A)', 'Im(A)', 'Re(A)', 'Im(A)', 
                        'Effgic(A)', 'Kfactor', 'KftrTyp', 
                        'Qloss(Mvar)']]}, 
           'trnauto': {'ub': ['Common', 'Series', 'Kbus', 'Ckt', 'Common gic(A)', 
                            'Series gic(A)', 'Kgic(A)', 
                            'Effgic(A)', 'Kfactor', 
                            'KftrTyp', 'Qloss(Mvar)'], 'n': [
                           [
                            '', 
                            '', '', '', 'Common Winding', 
                            '', 'Series Winding', 
                            '', 'Third Winding', '', 
                            '', '', '', ''],
                           [
                            'Common', 
                            'Series', 'Kbus', 'Ckt', 
                            'Re(A)', 'Im(A)', 'Re(A)', 
                            'Im(A)', 'Re(A)', 'Im(A)', 
                            'Effgic(A)', 'Kfactor', 
                            'KftrTyp', 'Qloss(Mvar)']]}, 
           'qloss': [
                   [
                    'Orientation', 'Two Winding Transformers', 
                    '', 'Three Winding Transformers', '', 
                    'Total'],
                   [
                    'Degrees', 'Normal(MVAR)', 
                    'Auto(MVAR)', 'Normal(MVAR)', 'Auto(MVAR)', 
                    'MVAR']]}
        _WORKSHT_INFO_TXT_GIC = {'bus': {'pfsolved': [['Bus GIC Calculation DC and Power Flow Solution AC Voltages'],
                              [
                               'Base case voltages are initial solved working case bus voltages'],
                              [
                               'GIC case voltages are base case + GIC loads power flow solution bus voltages']], 
                   'pfno': [
                          'Bus DC Voltages']}, 
           'sub': [
                 'Substations DC Voltages and GIC Flows, flowing from Bus to Substation Ground'], 
           'brn': [
                 'GIC flow in Non-Transformer Branches, flowing from From Bus to To Bus'], 
           'fxsh': [
                  'GIC flow in Bus Shunts, flowing from Bus to Substation ground bus'], 
           'trn': [
                 [
                  'Transformers: Per Phase GIC flow in windings, flowing from winding Bus to Neutral'],
                 [
                  'Reactive power loss, represented as constant current load on highest voltage bus in power flow']], 
           'trnauto': [
                     [
                      'Auto Transformers: Per Phase GIC flow in windings, flowing from winding Bus to Neutral'],
                     [
                      'Reactive power loss, represented as constant current load on Series Winding bus in power flow']], 
           'qloss': {'ub': ['Transformer Reactive Power Loss Summary for each Storm Orientation'], 'n': [
                         'Transformer Reactive Power Loss Summary']}}
        row_begin = {}
        for k, info in _WORKSHT_INFO_TXT_GIC.items():
            if type(info) == dict:
                row_begin[k] = {}
                for k1, v1 in info.items():
                    row_begin[k][k1] = len(v1) + 2

            else:
                row_begin[k] = len(info) + 2

        for i, do_key in enumerate(do_sheets):
            shtnam = _EXPORT_QTY_GIC[do_key]
            if i == 0:
                xlsobj = excelpy.workbook(xlfile, shtnam, overwritesheet=overwritesheet)
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

        efield_type = self.misc.efield_type
        _BGNROW, _BGNCLN = (1, 1)
        do_key = 'event'
        if do_key in do_sheets:
            shtnam = _EXPORT_QTY_GIC[do_key]
            txt = self._report_hdr()
            if self.basekv or self.areas or self.buses or self.owners or self.zones:
                txt += '\n Subsystem used for GIC studies is defined as:\n'
                if self.basekv:
                    txt += '     Voltage = %s\n' % str(self.basekv)
                if self.areas:
                    txt += '     Areas   = %s\n' % str(self.areas)
                if self.buses:
                    txt += '     Buses   = %s\n' % str(self.buses)
                if self.owners:
                    txt += '     Owners  = %s\n' % str(self.owners)
                if self.zones:
                    txt += '     Zones   = %s\n' % str(self.zones)
                txt += '     Subsystem Inter tie Levels = %d\n' % self.tielevels
            else:
                txt += '\n Subsystem used for GIC studies comprises entire network.\n'
            txt += '\n Number of buses in study subsystem        = %d\n' % self.misc.nbus_study
            txt += ' Number of substations in study subsystem  = %d\n' % self.misc.nsubstation_study
            txt += ' Number of branches in study subsystem     = %d\n' % self.misc.nbranch_study
            txt += ' Number of transformers in study subsystem = %d\n' % self.misc.ntransformer_study
            optntxtlist = txt.split('\n')
            xlsobj.set_active_sheet(shtnam)
            br, rc = xlsobj.set_range(_BGNROW, _BGNCLN, optntxtlist, transpose=True)
            del optntxtlist
        do_key = 'bus'
        if do_key in do_sheets:
            shtnam = _EXPORT_QTY_GIC[do_key]
            if self.pf_solved.flag == 0:
                lbltr = row_begin[do_key]['pfsolved']
                shtttl = _WORKSHT_INFO_TXT_GIC[do_key]['pfsolved']
            else:
                lbltr = row_begin[do_key]['pfno']
                shtttl = _WORKSHT_INFO_TXT_GIC[do_key]['pfno']
            xlsobj.set_active_sheet(shtnam)
            rowdata = []
            if self.pf_solved.flag == 0:
                if efield_type == 'nonuniform':
                    rowdata.extend(_WORKSHT_COLUMN_LABELS_GIC[do_key]['pfsolved']['n'])
                else:
                    rowdata.extend(_WORKSHT_COLUMN_LABELS_GIC[do_key]['pfsolved']['ub'])
            elif efield_type == 'nonuniform':
                rowdata.append(_WORKSHT_COLUMN_LABELS_GIC[do_key]['pfno']['n'])
            else:
                rowdata.append(_WORKSHT_COLUMN_LABELS_GIC[do_key]['pfno']['ub'])
            br, rc = xlsobj.set_range(lbltr, _BGNCLN, rowdata)
            lblbr = br
            buslist = list(self.bus.keys())
            buslist.sort()
            rowdata = []
            nnrow = 0
            if self.pf_solved.flag == 0:
                for eachbus in buslist:
                    nnrow += 1
                    v = self.bus[eachbus].vpu_base
                    vpu_base_mag = abs(v)
                    vpu_base_ang = math.degrees(math.atan(v.imag / v.real))
                    v = self.bus[eachbus].vpu_gic
                    vpu_gic_mag = abs(v)
                    vpu_gic_ang = math.degrees(math.atan(v.imag / v.real))
                    if efield_type == 'nonuniform':
                        tlst = [
                         eachbus, self.bus[eachbus].substation, self.bus[eachbus].dcvolts.real, self.bus[eachbus].dcvolts.imag,
                         vpu_base_mag, vpu_base_ang, vpu_gic_mag, vpu_gic_ang]
                    else:
                        tlst = [
                         eachbus, self.bus[eachbus].substation, self.bus[eachbus].dcvolts,
                         vpu_base_mag, vpu_base_ang, vpu_gic_mag, vpu_gic_ang]
                    rowdata.append(tlst)
                    if nnrow >= _NROW_AT_A_TIME:
                        br, rc = xlsobj.set_range(br + 1, _BGNCLN, rowdata)
                        rowdata = []
                        nnrow = 0

            else:
                for eachbus in buslist:
                    nnrow += 1
                    if efield_type == 'nonuniform':
                        tlst = [
                         eachbus, self.bus[eachbus].substation, self.bus[eachbus].dcvolts.real, self.bus[eachbus].dcvolts.imag]
                    else:
                        tlst = [
                         eachbus, self.bus[eachbus].substation, self.bus[eachbus].dcvolts]
                    rowdata.append(tlst)
                    if nnrow >= _NROW_AT_A_TIME:
                        br, rc = xlsobj.set_range(br + 1, _BGNCLN, rowdata)
                        rowdata = []
                        nnrow = 0

            if rowdata:
                br, rc = xlsobj.set_range(br + 1, _BGNCLN, rowdata)
            del rowdata
            xlsobj.width((_BGNROW, _BGNCLN, _BGNROW, rc), 16)
            xlsobj.font_color((lbltr, _BGNCLN, lblbr, rc), 'red')
            xlsobj.align((lbltr, 3), alignv='right')
            if self.pf_solved.flag == 0:
                if efield_type == 'nonuniform':
                    xlsobj.merge((lbltr, 3, lbltr, 4))
                    xlsobj.merge((lbltr, 5, lbltr, 6))
                    xlsobj.merge((lbltr, 7, lbltr, 8))
                    xlsobj.align((lbltr, 3), alignv='h_center')
                    xlsobj.align((lbltr, 5), alignv='h_center')
                    xlsobj.align((lbltr, 7), alignv='h_center')
                else:
                    xlsobj.merge((lbltr, 4, lbltr, 5))
                    xlsobj.merge((lbltr, 6, lbltr, 7))
                    xlsobj.align((lbltr, 4), alignv='h_center')
                    xlsobj.align((lbltr, 6), alignv='h_center')
            xlsobj.align_rows((lblbr, _BGNCLN), alignv='right')
            if len(shtttl) == 1:
                xlsobj.set_cell((_BGNROW, _BGNCLN), shtttl, fontStyle='bold', fontSize=12, fontColor='blue')
            else:
                xlsobj.set_range(_BGNROW, _BGNCLN, shtttl, fontStyle='bold', fontSize=12, fontColor='blue')
            xlsobj.freezepanes((lblbr + 1, 1))
        do_key = 'sub'
        if do_key in do_sheets:
            shtnam = _EXPORT_QTY_GIC[do_key]
            lbltr = row_begin[do_key]
            shtttl = _WORKSHT_INFO_TXT_GIC[do_key]
            xlsobj.set_active_sheet(shtnam)
            rowdata = []
            if efield_type == 'nonuniform':
                rowdata.append(_WORKSHT_COLUMN_LABELS_GIC[do_key]['n'])
            else:
                rowdata.append(_WORKSHT_COLUMN_LABELS_GIC[do_key]['ub'])
            br, rc = xlsobj.set_range(lbltr, _BGNCLN, rowdata)
            lblbr = br
            sslist = list(self.substation.keys())
            sslist.sort()
            rowdata = []
            nnrow = 0
            for ss in sslist:
                nnrow += 1
                if efield_type == 'nonuniform':
                    tlst = [
                     ss, self.substation[ss].name, self.substation[ss].latitude, self.substation[ss].longitude,
                     self.substation[ss].dcvolts.real, self.substation[ss].dcvolts.imag,
                     self.substation[ss].gic.real, self.substation[ss].gic.imag]
                else:
                    tlst = [
                     ss, self.substation[ss].name, self.substation[ss].latitude, self.substation[ss].longitude,
                     self.substation[ss].dcvolts, self.substation[ss].gic]
                rowdata.append(tlst)
                if nnrow >= _NROW_AT_A_TIME:
                    br, rc = xlsobj.set_range(br + 1, _BGNCLN, rowdata)
                    rowdata = []
                    nnrow = 0

            if rowdata:
                br, rc = xlsobj.set_range(br + 1, _BGNCLN, rowdata)
            del rowdata
            xlsobj.width((_BGNROW, _BGNCLN, _BGNROW, rc), 16)
            xlsobj.font_color((lbltr, _BGNCLN, lblbr, rc), 'red')
            xlsobj.align_rows((lblbr, _BGNCLN), alignv='right')
            xlsobj.align((lblbr, 2), alignv='left')
            xlsobj.set_cell((_BGNROW, _BGNCLN), shtttl, fontStyle='bold', fontSize=12, fontColor='blue')
            xlsobj.freezepanes((lblbr + 1, 1))
        do_key = 'brn'
        if do_key in do_sheets:
            shtnam = _EXPORT_QTY_GIC[do_key]
            lbltr = row_begin[do_key]
            shtttl = _WORKSHT_INFO_TXT_GIC[do_key]
            xlsobj.set_active_sheet(shtnam)
            rowdata = []
            if efield_type == 'nonuniform':
                rowdata.extend(_WORKSHT_COLUMN_LABELS_GIC[do_key]['n'])
            else:
                rowdata.append(_WORKSHT_COLUMN_LABELS_GIC[do_key]['ub'])
            br, rc = xlsobj.set_range(lbltr, _BGNCLN, rowdata)
            lblbr = br
            brnlist = list(self.branch.keys())
            brnlist.sort()
            rowdata = []
            nnrow = 0
            for brn in brnlist:
                nnrow += 1
                if efield_type == 'nonuniform':
                    ir = self.branch[brn].gic.real
                    ix = self.branch[brn].gic.imag
                    tlst = [brn[0], brn[1], brn[2], self.branch[brn].distance, ir, ix, 3 * ir, 3 * ix]
                else:
                    igic = self.branch[brn].gic
                    tlst = [brn[0], brn[1], brn[2], self.branch[brn].distance, igic, 3 * igic]
                rowdata.append(tlst)
                if nnrow >= _NROW_AT_A_TIME:
                    br, rc = xlsobj.set_range(br + 1, _BGNCLN, rowdata)
                    rowdata = []
                    nnrow = 0

            if rowdata:
                br, rc = xlsobj.set_range(br + 1, _BGNCLN, rowdata)
            del rowdata
            xlsobj.width((_BGNROW, _BGNCLN, _BGNROW, rc), 16)
            xlsobj.font_color((lbltr, _BGNCLN, lblbr, rc), 'red')
            xlsobj.align_rows((lblbr, _BGNCLN), alignv='right')
            xlsobj.align_columns((lblbr, _BGNCLN + 2), alignv='right')
            xlsobj.width((_BGNROW, _BGNCLN + 2), 8)
            if efield_type == 'nonuniform':
                xlsobj.merge((lbltr, 5, lbltr, 6))
                xlsobj.merge((lbltr, 7, lbltr, 8))
                xlsobj.align((lbltr, 5), alignv='h_center')
                xlsobj.align((lbltr, 7), alignv='h_center')
            xlsobj.set_cell((_BGNROW, _BGNCLN), shtttl, fontStyle='bold', fontSize=12, fontColor='blue')
            xlsobj.freezepanes((lblbr + 1, 1))
        do_key = 'fxsh'
        if do_key in do_sheets:
            shtnam = _EXPORT_QTY_GIC[do_key]
            lbltr = row_begin[do_key]
            shtttl = _WORKSHT_INFO_TXT_GIC[do_key]
            xlsobj.set_active_sheet(shtnam)
            rowdata = []
            if efield_type == 'nonuniform':
                rowdata.extend(_WORKSHT_COLUMN_LABELS_GIC[do_key]['n'])
            else:
                rowdata.append(_WORKSHT_COLUMN_LABELS_GIC[do_key]['ub'])
            br, rc = xlsobj.set_range(lbltr, _BGNCLN, rowdata)
            lblbr = br
            fxshlist = list(self.fixedshunt.keys())
            fxshlist.sort()
            rowdata = []
            nnrow = 0
            for fxsh in fxshlist:
                nnrow += 1
                if efield_type == 'nonuniform':
                    ir = self.fixedshunt[fxsh].gic.real
                    ix = self.fixedshunt[fxsh].gic.imag
                    tlst = [fxsh[0], fxsh[1], ir, ix, 3 * ir, 3 * ix]
                else:
                    igic = self.fixedshunt[fxsh].gic
                    tlst = [fxsh[0], fxsh[1], igic, 3 * igic]
                rowdata.append(tlst)
                if nnrow >= _NROW_AT_A_TIME:
                    br, rc = xlsobj.set_range(br + 1, _BGNCLN, rowdata)
                    rowdata = []
                    nnrow = 0

            if rowdata:
                br, rc = xlsobj.set_range(br + 1, _BGNCLN, rowdata)
            del rowdata
            xlsobj.width((_BGNROW, _BGNCLN, _BGNROW, rc), 16)
            xlsobj.font_color((lbltr, _BGNCLN, lblbr, rc), 'red')
            xlsobj.align_rows((lblbr, _BGNCLN), alignv='right')
            xlsobj.align_columns((lblbr, _BGNCLN + 1), alignv='right')
            xlsobj.width((_BGNROW, _BGNCLN + 1), 8)
            if efield_type == 'nonuniform':
                xlsobj.merge((lbltr, 3, lbltr, 4))
                xlsobj.merge((lbltr, 5, lbltr, 6))
                xlsobj.align((lbltr, 3), alignv='h_center')
                xlsobj.align((lbltr, 5), alignv='h_center')
            xlsobj.set_cell((_BGNROW, _BGNCLN), shtttl, fontStyle='bold', fontSize=12, fontColor='blue')
            xlsobj.freezepanes((lblbr + 1, 1))
        for do_key in ['trn', 'trnauto']:
            if do_key in do_sheets:
                shtnam = _EXPORT_QTY_GIC[do_key]
                lbltr = row_begin[do_key]
                shtttl = _WORKSHT_INFO_TXT_GIC[do_key]
                xlsobj.set_active_sheet(shtnam)
                rowdata = []
                if efield_type == 'nonuniform':
                    rowdata.extend(_WORKSHT_COLUMN_LABELS_GIC[do_key]['n'])
                else:
                    rowdata.append(_WORKSHT_COLUMN_LABELS_GIC[do_key]['ub'])
                br, rc = xlsobj.set_range(lbltr, _BGNCLN, rowdata)
                lblbr = br
                trnlist = list(self.transformer.keys())
                trnlist.sort()
                rowdata = []
                nnrow = 0
                for trn in trnlist:
                    kbus = trn[2]
                    autoi = self.transformer[trn].wdg1_auto
                    autoj = self.transformer[trn].wdg2_auto
                    if not kbus:
                        isauto = autoi or autoj
                    else:
                        autok = self.transformer[trn].wdg3_auto
                        isauto = autoi or autoj or autok
                    if do_key == 'trn' and isauto:
                        continue
                    if do_key == 'trnauto' and not isauto:
                        continue
                    ibus = trn[0]
                    jbus = trn[1]
                    ckt = trn[3]
                    nnrow += 1
                    kr, kx = ('', '')
                    if efield_type == 'nonuniform':
                        ir = self._get_valid_real_value(self.transformer[trn].wdg1_gic.real)
                        ix = self._get_valid_real_value(self.transformer[trn].wdg1_gic.imag)
                        jr = self._get_valid_real_value(self.transformer[trn].wdg2_gic.real)
                        jx = self._get_valid_real_value(self.transformer[trn].wdg2_gic.imag)
                        if kbus:
                            kr = self._get_valid_real_value(self.transformer[trn].wdg3_gic.real)
                            kx = self._get_valid_real_value(self.transformer[trn].wdg3_gic.imag)
                    else:
                        ir = self._get_valid_real_value(self.transformer[trn].wdg1_gic)
                        ix = self._get_valid_real_value(self.transformer[trn].wdg1_gic)
                        jr = self._get_valid_real_value(self.transformer[trn].wdg2_gic)
                        jx = self._get_valid_real_value(self.transformer[trn].wdg2_gic)
                        if kbus:
                            kr = self._get_valid_real_value(self.transformer[trn].wdg3_gic)
                            kx = self._get_valid_real_value(self.transformer[trn].wdg3_gic)
                    eff_gic = self._get_valid_real_value(self.transformer[trn].eff_gic)
                    qloss = self._get_valid_real_value(self.transformer[trn].qloss)
                    kftrtyp = self._get_kfactor_type(self.transformer[trn].kfactor_type)
                    if efield_type == 'nonuniform':
                        tlst = [
                         trn[0], trn[1], trn[2], trn[3], ir, ix, jr, jx, kr, kx, eff_gic,
                         self.transformer[trn].kfactor, kftrtyp, qloss]
                    else:
                        tlst = [
                         trn[0], trn[1], trn[2], trn[3], ir, jr, kr, eff_gic,
                         self.transformer[trn].kfactor, kftrtyp, qloss]
                    rowdata.append(tlst)
                    if nnrow >= _NROW_AT_A_TIME:
                        br, rc = xlsobj.set_range(br + 1, _BGNCLN, rowdata)
                        rowdata = []
                        nnrow = 0

                if rowdata:
                    br, rc = xlsobj.set_range(br + 1, _BGNCLN, rowdata)
                del rowdata
                xlsobj.width((_BGNROW, _BGNCLN, _BGNROW, rc), 16)
                xlsobj.font_color((lbltr, _BGNCLN, lblbr, rc), 'red')
                xlsobj.align_rows((lblbr, _BGNCLN), alignv='right')
                xlsobj.align_columns((lblbr, _BGNCLN + 3), alignv='right')
                xlsobj.align_columns((lblbr, rc - 1), alignv='right')
                xlsobj.width((_BGNROW, _BGNCLN + 3), 8)
                if efield_type == 'nonuniform':
                    xlsobj.merge((lbltr, 5, lbltr, 6))
                    xlsobj.merge((lbltr, 7, lbltr, 8))
                    xlsobj.merge((lbltr, 9, lbltr, 10))
                    xlsobj.align((lbltr, 5), alignv='h_center')
                    xlsobj.align((lbltr, 7), alignv='h_center')
                    xlsobj.align((lbltr, 9), alignv='h_center')
                xlsobj.set_range(_BGNROW, _BGNCLN, shtttl, fontStyle='bold', fontSize=12, fontColor='blue')
                xlsobj.freezepanes((lblbr + 1, 1))

        do_key = 'qloss'
        if do_key in do_sheets:
            shtnam = _EXPORT_QTY_GIC[do_key]
            if efield_type == 'nonuniform':
                lbltr = row_begin[do_key]['n']
                shtttl = _WORKSHT_INFO_TXT_GIC[do_key]['n']
            else:
                lbltr = row_begin[do_key]['ub']
                shtttl = _WORKSHT_INFO_TXT_GIC[do_key]['ub']
            xlsobj.set_active_sheet(shtnam)
            rowdata = []
            rowdata.extend(_WORKSHT_COLUMN_LABELS_GIC[do_key])
            br, rc = xlsobj.set_range(lbltr, _BGNCLN, rowdata)
            lblbr = br
            rowdata = []
            nnrow = 0
            if efield_type == 'nonuniform':
                nnrow += 1
                r_2nrml = self.qtotal.wdg2_normal
                r_2auto = self.qtotal.wdg2_auto
                r_3nrml = self.qtotal.wdg3_normal
                r_3auto = self.qtotal.wdg3_auto
                r_qtotal = self.qtotal.total
                tlst = ['', r_2nrml, r_2auto, r_3nrml, r_3auto, r_qtotal]
                rowdata.append(tlst)
                br, rc = xlsobj.set_range(br + 1, _BGNCLN, rowdata)
            else:
                for deg in self.ordered_efield_deg_per_maxq:
                    nnrow += 1
                    r_2nrml = self.deg_scan_qtotal[deg].wdg2_normal
                    r_2auto = self.deg_scan_qtotal[deg].wdg2_auto
                    r_3nrml = self.deg_scan_qtotal[deg].wdg3_normal
                    r_3auto = self.deg_scan_qtotal[deg].wdg3_auto
                    r_qtotal = self.deg_scan_qtotal[deg].total
                    tlst = [deg, r_2nrml, r_2auto, r_3nrml, r_3auto, r_qtotal]
                    rowdata.append(tlst)

                br, rc = xlsobj.set_range(br + 1, _BGNCLN, rowdata)
            del rowdata
            xlsobj.width((_BGNROW, _BGNCLN, _BGNROW, rc), 16)
            xlsobj.font_color((lbltr, _BGNCLN, lblbr, rc), 'red')
            xlsobj.align_rows((lblbr, _BGNCLN), alignv='right')
            xlsobj.align((lbltr, rc), alignv='right')
            xlsobj.align((lbltr, 1), alignv='right')
            xlsobj.merge((lbltr, 2, lbltr, 3))
            xlsobj.align((lbltr, 2), alignv='h_center')
            xlsobj.merge((lbltr, 4, lbltr, 5))
            xlsobj.align((lbltr, 4), alignv='h_center')
            xlsobj.set_cell((_BGNROW, _BGNCLN), shtttl, fontStyle='bold', fontSize=12, fontColor='blue')
            xlsobj.freezepanes((lblbr + 1, 1))
            if efield_type == 'nonuniform':
                txt = ('Power Flow Solution: {0:s}').format(self.pf_solved.cond)
            else:
                s_ef = '%10.2f' % self.misc.efield_mag
                s_ef = s_ef.strip()
                s_deg = '%8.2f' % self.misc.efield_deg
                s_deg = s_deg.strip()
                txt = ('Power Flow Solution for Efield of {0:s} {1:s} at {2:s} degrees: {3:s}').format(s_ef, self.misc.efield_unit, s_deg, self.pf_solved.cond)
            xlsobj.set_cell((br + 2, _BGNCLN), txt, fontStyle='bold', fontSize=10, fontColor='blue')
        savfnam = xlsobj.save(xlfile)
        if not show:
            xlsobj.close()
        elif 'event' in do_sheets:
            shtnam = _EXPORT_QTY_GIC['event']
            xlsobj.set_active_sheet(shtnam)
        return savfnam

    def _pyout_for_maps(self, pyoutfile):
        if self.ierr:
            return
        else:
            misc = self.misc
            bus = self.bus
            substation = self.substation
            branch = self.branch
            fixedshunt = self.fixedshunt
            transformer = self.transformer
            qtotal = self.qtotal
            pyoutfile = self._fname_add_suffix_deg_check_extn(pyoutfile, extn='.py')
            rptfobj = open(pyoutfile, 'w')
            report = rptfobj.write
            txt = 'elecfld_mag = %g\n' % misc.efield_mag
            report(txt)
            txt = "elecfld_unit = '%s'\n" % misc.efield_unit
            report(txt)
            txt = 'elecfld_deg = %g\n' % misc.efield_deg
            report(txt)
            txt = 'efield_mag_local = %g\n' % misc.efield_mag_local
            report(txt)
            txt = 'efield_deg_local = %g\n' % misc.efield_deg_local
            report(txt)
            txt = "efield_type = '%s'\n" % misc.efield_type
            report(txt)
            txt = "gic2mvar_optn = '%s'\n" % misc.gic2mvar_optn
            report(txt)
            txt = "earth_model_name = '%s'\n" % misc.earth_model_name
            report(txt)
            txt = "power_flow_optn = '%s'\n" % misc.power_flow_optn
            report(txt)
            txt = 'power_flow_solution_flag = %d\n' % self.pf_solved.flag
            report(txt)
            txt = "power_flow_solution_cond = '%s'\n" % self.pf_solved.cond
            report(txt)
            if self.tielevels:
                txt = 'tielevels = %s\n' % str(self.tielevels)
            else:
                txt = 'tielevels = None\n'
            report(txt)
            efield_type = misc.efield_type
            if efield_type == 'benchmark':
                txt = 'study_year = %d\n' % misc.study_year
                report(txt)
            elif efield_type == 'nonuniform':
                txt = 'ejet_million_amps = %g\n' % misc.ejet_million_amps
                report(txt)
                txt = 'ejet_halfwidth_km = %g\n' % misc.ejet_halfwidth_km
                report(txt)
                txt = 'ejet_period_min = %g\n' % misc.ejet_period_min
                report(txt)
                txt = 'ejet_height_km = %g\n' % misc.ejet_height_km
                report(txt)
                txt = 'ejet_center_deg = %g\n' % misc.ejet_center_deg
                report(txt)
            txt = "savfile= r'%s'\n" % self.savfile
            report(txt)
            txt = "gicfile= r'%s'\n" % self.gicfile
            report(txt)
            txt = ''
            if self.basekv:
                txt += 'basekv = %s\n' % str(self.basekv)
            else:
                txt += 'basekv = []\n'
            if self.areas:
                txt += 'areas = %s\n' % str(self.areas)
            else:
                txt += 'areas = []\n'
            if self.buses:
                txt += 'buses = %s\n' % str(self.buses)
            else:
                txt += 'buses = []\n'
            if self.owners:
                txt += 'owners = %s\n' % str(self.owners)
            else:
                txt += 'owners = []\n'
            if self.zones:
                txt += 'zones = %s\n' % str(self.zones)
            else:
                txt += 'zones = []\n'
            report(txt)
            txt = ''
            if self.basekv_local:
                txt += 'basekv_local = %s\n' % str(self.basekv_local)
            else:
                txt += 'basekv_local = []\n'
            if self.areas_local:
                txt += 'areas_local = %s\n' % str(self.areas_local)
            else:
                txt += 'areas_local = []\n'
            if self.buses_local:
                txt += 'buses_local = %s\n' % str(self.buses_local)
            else:
                txt += 'buses_local = []\n'
            if self.owners_local:
                txt += 'owners_local = %s\n' % str(self.owners_local)
            else:
                txt += 'owners_local = []\n'
            if self.zones_local:
                txt += 'zones_local = %s\n' % str(self.zones_local)
            else:
                txt += 'zones_local = []\n'
            report(txt)
            sslist = substation.keys()
            sslist.sort()
            temp_lon = {}
            temp_lat = {}
            txt = 'substation = {\n'
            report(txt)
            for ss in sslist:
                lon = substation[ss].longitude
                lat = substation[ss].latitude
                if lon not in temp_lon:
                    temp_lon[lon] = 1
                if lat not in temp_lat:
                    temp_lat[lat] = 1
                dcv = substation[ss].dcvolts
                gic = substation[ss].gic
                if efield_type == 'nonuniform':
                    dcv = abs(dcv)
                    gic = abs(gic)
                mvar = substation[ss].mvar
                txt = "    %d:{'longitude':%g, 'latitude':%g, 'dcvolts':%g, 'gic':%g, 'mvar':%g},\n" % (ss, lon, lat, dcv, gic, mvar)
                report(txt)

            report('    }\n\n')
            lon_list = temp_lon.keys()
            lat_list = temp_lat.keys()
            lon_list.sort()
            lat_list.sort()
            txt = 'longitude_min = %g\n' % lon_list[0]
            txt += 'longitude_max = %g\n' % lon_list[-1]
            txt += 'latitude_min  = %g\n' % lat_list[0]
            txt += 'latitude_max  = %g\n\n' % lat_list[-1]
            report(txt)
            del temp_lon
            del temp_lat
            del lon_list
            del lat_list
            buslist = bus.keys()
            buslist.sort()
            txt = 'bus = {\n'
            report(txt)
            for b in buslist:
                ss = bus[b].substation
                dcv = bus[b].dcvolts
                if efield_type == 'nonuniform':
                    dcv = abs(dcv)
                kv = bus[b].basekv
                vpu_base = bus[b].vpu_base
                vpu_gic = bus[b].vpu_gic
                if vpu_gic.real == -1.0 and vpu_gic.imag == -1.0:
                    s_vpu_gic = None
                else:
                    s_vpu_gic = '%g' % abs(vpu_gic)
                txt = "    %d:{'substation':%d, 'dcvolts':%g, 'basekv':%g, 'vpu_base':%g, 'vpu_gic':%s},\n" % (b, ss, dcv, kv, abs(vpu_base), s_vpu_gic)
                report(txt)

            report('    }\n\n')
            brnlist = branch.keys()
            brnlist.sort()
            distance_dict = {}
            txt = 'branch = {\n'
            report(txt)
            for ii, brn in enumerate(brnlist):
                dst = branch[brn].distance
                gic = branch[brn].gic
                if efield_type == 'nonuniform':
                    gic = abs(gic)
                if dst not in distance_dict:
                    distance_dict[dst] = 1
                txt = "    (%d,%d,'%-2s'):{'distance':%g, 'gic':%g},\n" % (brn[0], brn[1], brn[2], dst, gic)
                report(txt)

            report('    }\n\n')
            distance_list = distance_dict.keys()
            distance_list.sort()
            distance_max = distance_list[-1]
            ii = 0
            while True:
                if distance_list[ii] >= 0.1 * distance_max:
                    distance_min = distance_list[ii]
                    break
                else:
                    ii += 1

            txt = 'distance_min = %g\n' % distance_min
            txt += 'distance_max = %g\n\n' % distance_max
            report(txt)
            fxshlist = fixedshunt.keys()
            fxshlist.sort()
            txt = 'fixedshunt = {\n'
            report(txt)
            for ii, fxsh in enumerate(fxshlist):
                gic = fixedshunt[fxsh].gic
                if efield_type == 'nonuniform':
                    gic = abs(gic)
                txt = "    (%d,'%-2s'):{'gic':%g},\n" % (fxsh[0], fxsh[1], gic)
                report(txt)

            report('    }\n\n')
            trnlist = transformer.keys()
            trnlist.sort()
            txt = 'transformer = {\n'
            report(txt)
            for trn in trnlist:
                igic = transformer[trn].wdg1_gic
                jgic = transformer[trn].wdg2_gic
                kgic = transformer[trn].wdg3_gic
                if efield_type == 'nonuniform':
                    igic = abs(igic)
                    jgic = abs(jgic)
                    kgic = abs(kgic)
                igic = self._get_formatted_real_value1(igic)
                jgic = self._get_formatted_real_value1(jgic)
                kgic = self._get_formatted_real_value1(kgic)
                effgic = self._get_formatted_real_value1(transformer[trn].eff_gic)
                qloss = self._get_formatted_real_value1(transformer[trn].qloss)
                kftrtyp = transformer[trn].kfactor_type
                kftr = transformer[trn].kfactor
                autoi = transformer[trn].wdg1_auto
                autoj = transformer[trn].wdg2_auto
                autok = transformer[trn].wdg3_auto
                if autoi or autoj:
                    auto = 1
                else:
                    auto = 0
                ibus = trn[0]
                jbus = trn[1]
                if autoj == 1:
                    ibus = trn[1]
                    jbus = trn[0]
                kbus = trn[2]
                ckt = trn[3]
                txt = "    (%d,%d,%d,'%-2s'):{'wdg1_gic':%s, 'wdg2_gic':%s, 'wdg3_gic':%s, 'eff_gic':%s, 'qloss':%s, 'kfactor_type':%d, 'kfactor':%g, 'auto':%d},\n" % (
                 ibus, jbus, kbus, ckt, igic, jgic, kgic, effgic, qloss, kftrtyp, kftr, auto)
                report(txt)

            report('    }\n\n')
            txt = 'qtotal = {\n'
            txt += "    '2wdg_normal':%g, '2wdg_auto':%g, '3wdg_normal':%g, '3wdg_auto':%g, 'total':%g\n" % (
             qtotal.wdg2_normal, qtotal.wdg2_auto, qtotal.wdg3_normal, qtotal.wdg3_auto, qtotal.total)
            txt += '    }\n\n'
            report(txt)
            txt = 'qtotal_all = {\n'
            report(txt)
            tmplist = list(self.deg_scan_qtotal.keys())
            tmplist.sort()
            for deg in tmplist:
                txt = '    %g:%g,\n' % (deg, self.deg_scan_qtotal[deg].total)
                report(txt)

            report('    }\n\n')
            del tmplist
            rptfobj.close()
            return

    def _report_hdr(self):
        if self.misc.efield_type == 'nonuniform':
            crnt = ('%10.2f' % self.misc.ejet_million_amps).strip()
            ha = ('%10.2f' % self.misc.ejet_halfwidth_km).strip()
            fq = ('%10.2f' % self.misc.ejet_period_min).strip()
            ht = ('%10.2f' % self.misc.ejet_height_km).strip()
            lat = ('%10.2f' % self.misc.ejet_center_deg).strip()
            txt = ' GMD Event: Non Uniform Geoelectric Field with Electrojet Source Current characteristics -\n    Electrojet Current Amplitude = %s million Amps\n    Electrojet Current Density Cauchy Distribution half-width = %s km\n    Electrojet Period of Variation = %s minutes\n    Electrojet Height of Current = %s km\n    Latitude of Electrojet Center = %s degrees' % (crnt, ha, fq, ht, lat)
            txt += '\n'
        else:
            elecfld_mag = '%10.2f' % self.misc.efield_mag
            elecfld_mag = elecfld_mag.strip()
            elecfld_unt = self.misc.efield_unit
            elecfld_unt = elecfld_unt[0].upper() + elecfld_unt[1:]
            elecfld_deg = '%10.2f' % self.misc.efield_deg
            elecfld_deg = elecfld_deg.strip()
            txt = ' GMD Event: %s Electric Field = %s %s, %s deg\n' % (self.misc.efield_type.title(), elecfld_mag, elecfld_unt, elecfld_deg)
        if self.misc.efield_type == 'benchmark':
            txt += '\n Study year: %d\n' % self.misc.study_year
        txt += '\n Power flow data file: %s\n' % self.savfile
        txt += ' GIC data file: %s\n' % self.gicfile
        return txt

    def qtotal_report(self, rptfile=''):
        """When GIC calculations are done for many storm directions (efield_deg), this report provides
total reactive power for all storm directions.
"""
        if self.ierr:
            return
        if self.misc.efield_type == 'nonuniform':
            return
        if rptfile:
            rptfile = self._fname_add_suffix_deg_check_extn(rptfile, extn='.txt')
            rptfobj = open(rptfile, 'w')
            report = rptfobj.write
        else:
            report = sys.stdout.write
        txt = self._report_hdr()
        report(txt)
        txt = '\n Storm Orientation Scan: Transformer Reactive Power Loss Summary\n\n'
        report(txt)
        txt = ' Orientation  |--Two Winding Transformers--|  |--Three Winding Transformers--|  |---Total---|\n'
        report(txt)
        txt = '     Degrees     Normal(MVAR)    Auto(MVAR)      Normal(MVAR)    Auto(MVAR)          MVAR\n'
        report(txt)
        for deg in self.ordered_efield_deg_per_maxq:
            r_2nrml = self.deg_scan_qtotal[deg].wdg2_normal
            r_2auto = self.deg_scan_qtotal[deg].wdg2_auto
            r_3nrml = self.deg_scan_qtotal[deg].wdg3_normal
            r_3auto = self.deg_scan_qtotal[deg].wdg3_auto
            r_qtotal = self.deg_scan_qtotal[deg].total
            txt = ('{0:6s}{1:6.2f}{0:4s}{2:12.5f}{0:2s}{3:12.5f}{0:6s}{4:12.5f}{0:2s}{5:12.5f}{0:5s}{6:12.5f}\n').format(' ', deg, r_2nrml, r_2auto, r_3nrml, r_3auto, r_qtotal)
            report(txt)

        s_ef = '%10.2f' % self.misc.efield_mag
        s_ef = s_ef.strip()
        s_deg = '%8.2f' % self.misc.efield_deg
        s_deg = s_deg.strip()
        txt = ('\n Power Flow Solution for Efield of {0:s} {1:s} at {2:s} degrees: {3:s}\n').format(s_ef, self.misc.efield_unit, s_deg, self.pf_solved.cond)
        report(txt)
        if rptfile:
            rptfobj.close()

    def text_report(self, rptfile=''):
        """Text report of GIC results.
rptfile -> Output file name (.txt), default progress window
           When scan_storm_event = 'scan_deg', then report is created for
           storm direction corresponding to maximum reactive power losses.
"""
        self._text_report(rptfile)

    def excel_export(self, string='', xlfile='', show=True, overwritesheet=True):
        """Export of GIC results to Excel Spreadsheet.
string -> Name or list of names or  indicating which results to export, default export all results
          'event' - GMD event for which results are calculated
          'bus'   - Bus DC voltages, Base Case and GIC Case AC voltages if power flow is solved
          'sub'   - Substation GPS data, DC voltages and GICs Flow
          'brn'   - Non transformer branch GICs Flow
          'fxsh'  - Fixed Shunt GICs Flow
          'trn'   - Transformer GICs Flow and Reactive Power Losses
          'qloss' - Total Reactive Power losses for every storm angle scanned
          Example: string='bus' or string=['event','bus','sub','brn','fxsh','trn','qloss']
xlfile -> Output Excel file name (extension based on Excel version added)
          When scan_storm_event = 'scan_deg', then Excel output is created for
          storm direction corresponding to maximum reactive power losses.
          When xlfile name not provided, .sav file name used
show   -> Show or not show Excel Workbook when being populated
          = True  - show Workbook (default)
          = False - do not show Workbook
overwritesheet -> Overwrite worksheets flag, default True
          = True,  existing worksheets are overwritten
          = False, existing worksheets are copied and their names
            appended with (#), where # is next sequence number.
"""
        xlfile = self._excel_export(string, xlfile, show, overwritesheet)
        return xlfile

    def gicoutput_for_maps(self, pyoutfile):
        """GIC results are saved in a Python File. This file is used as input file to plot
GIC results on maps using arrbox.gicmaps.GICMAPS object.
pyoutfile  -> Output file name (.py), no default allowed
              When scan_storm_event = 'scan_deg', then report is created for
              storm direction corresponding to maximum reactive power losses.
"""
        if not pyoutfile:
            msgtxt = "\n Error: Provide 'pyoutfile' file name.\n"
            psspy.progress(errmsg)
            return
        self._pyout_for_maps(pyoutfile)


class GICMAPS():
    """Create GICMAPS object as below and apply various methods defined here.

gicmapsobj = pssarrays.GICMAPS(pygicfile)

where:
pygicfile : GIC results python output (.py) file name, no default allowed
    This is the output file created using pssarrays.GIC object function gicoutput_for_maps(..).

Any variable in pygicfile can be accessed, for example, as:
    elecfld_deg = gicmapsobj.pygicobj.elecfld_deg

The various plots created here return Axes and Figure instances.
Using Axes instance and matplotlib functions/methods one could modify those plots as desired.
Then using Figure instance those can be saved to any file. For example:
    fig.savefig('test.png', dpi=300, bbox_inches='tight')
"""

    def __init__(self, pygicfile):
        """"""
        self.ierr = True
        if not os.path.exists(pygicfile):
            msg = '\n File does not exist: %s\n' % pygicfile
            print msg
            return
        else:
            if _OK_MATPLOTLIB and _OK_NUMPY and _OK_BASEMAP:
                pass
            else:
                print _ALLOW_PLT_MSG
                return
            self._fignum = 0
            self._basemap = None
            shutil.copyfile(pygicfile, _TMP_GICPY_FNAM)
            import tmpjnkgic as pygicobj
            self.pygicobj = pygicobj
            try:
                os.remove(_TMP_GICPY_FNAM)
            except:
                pass

            try:
                os.remove(_TMP_GICPYC_FNAM)
            except:
                pass

            self.set_options_base_kv_colors()
            self.set_legend_options_kv()
            self.set_legend_options_ss_gic_desc()
            self.set_legend_options_ss_gic_values()
            self.set_options_voltage_pu_colors()
            self.set_legend_options_voltage_pu_desc()
            self.set_legend_options_voltage_pu_values()
            self.set_state_boundary_options()
            self.set_longitude_options()
            self.set_latitude_options()
            self.set_xlabel_options()
            self.set_ylabel_options()
            self.set_title_options()
            self.set_xlabel_options_qtotal()
            self.set_ylabel_options_qtotal()
            self.set_title_options_qtotal()
            self._set_substation_pflow_voltages()
            self.annotate_substations(None)
            self.ierr = False
            return

    def _set_substation_pflow_voltages(self):
        self._substation_voltages = collections.OrderedDict()
        for bus, vdict in self.pygicobj.bus.items():
            ss = vdict['substation']
            vpu_base = vdict['vpu_base']
            vpu_gic = vdict['vpu_gic']
            if ss not in self._substation_voltages:
                self._substation_voltages[ss] = {'vpu_base': [], 'vpu_gic': []}
            if vpu_base not in self._substation_voltages[ss]['vpu_base']:
                self._substation_voltages[ss]['vpu_base'].append(vpu_base)
            if vpu_gic not in self._substation_voltages[ss]['vpu_gic']:
                self._substation_voltages[ss]['vpu_gic'].append(vpu_gic)

        for ss, vdict in self._substation_voltages.items():
            max_vpu_base = max(vdict['vpu_base'])
            min_vpu_base = min(vdict['vpu_base'])
            max_vpu_gic = max(vdict['vpu_gic'])
            min_vpu_gic = min(vdict['vpu_gic'])
            self._substation_voltages[ss]['max_vpu_base'] = max_vpu_base
            self._substation_voltages[ss]['min_vpu_base'] = min_vpu_base
            self._substation_voltages[ss]['max_vpu_gic'] = max_vpu_gic
            self._substation_voltages[ss]['min_vpu_gic'] = min_vpu_gic

    def _get_midpoint(self, loni, lati, lonj, latj):
        dlon = loni - lonj
        dlat = lati - latj
        if not dlon or not dlat:
            lon50 = None
            lat50 = None
        else:
            slope = dlat / dlon
            yintercept = lati - slope * loni
            lon50 = loni - dlon / 2.0
            lat50 = slope * lon50 + yintercept
        return (
         lon50, lat50)

    def _get_arrow_points(self, loni, lati, lonj, latj):
        lon50, lat50 = self._get_midpoint(loni, lati, lonj, latj)
        if not lon50:
            xall, yall = [], []
        else:
            lon25, lat25 = self._get_midpoint(loni, lati, lon50, lat50)
            if not lon25:
                lon75, lat75 = (None, None)
            else:
                lon75, lat75 = self._get_midpoint(lon50, lat50, lonj, latj)
            xall = [loni]
            yall = [lati]
            if lon25:
                xall.append(lon25)
                yall.append(lat25)
            if lon75:
                xall.append(lon75)
                yall.append(lat75)
            xall.append(lonj)
            yall.append(latj)
        return (
         xall, yall)

    def _get_quiver_data(self, xproj, yproj, gicdir='from2to'):
        if gicdir == 'from2to':
            x = [each for each in xproj[::-1]]
            y = [each for each in yproj[::-1]]
        else:
            x = xproj[:]
            y = yproj[:]
        dlon = x[0] - x[1]
        dlat = y[0] - y[1]
        u = []
        v = []
        for each in x[1:-1]:
            u.append(dlon)
            v.append(dlat)

        return (x[1:-1], y[1:-1], u, v)

    def _get_color_buspu(self, buspu):
        vpu = None
        for n in range(len(self._legends_bus_pu_seq)):
            if self._legends_bus_pu_seq[n] > buspu:
                if n == 0:
                    n1 = n
                else:
                    n1 = n - 1
                vpu = self._legends_bus_pu_seq[n1]
                break

        if not vpu:
            if buspu >= self._legends_bus_pu_seq[-1]:
                vpu = self._legends_bus_pu_seq[-1]
        color = self._legends_bus_pu[vpu]['color']
        return (
         vpu, color)

    def _get_color_linewidth_basekv(self, basekv):
        bkv = None
        for n in range(len(self._legends_base_kv_seq)):
            if self._legends_base_kv_seq[n] > basekv:
                if n == 0:
                    n1 = n
                else:
                    n1 = n - 1
                bkv = self._legends_base_kv_seq[n1]
                break

        if not bkv:
            if basekv >= self._legends_base_kv_seq[-1]:
                bkv = self._legends_base_kv_seq[-1]
        color = self._legends_base_kv[bkv]['color']
        linewidth = self._legends_base_kv[bkv]['linewidth']
        return (
         bkv, color, linewidth)

    def _get_color_linewidth_flow_dir(self, val):
        if val < 0:
            flowdir = 'in'
        else:
            flowdir = 'out'
        color = _LEGENDS_FLOW_DIR[flowdir]['color']
        linewidth = _LEGENDS_FLOW_DIR[flowdir]['linewidth']
        marker = _LEGENDS_FLOW_DIR[flowdir]['marker']
        return (
         flowdir, color, linewidth, marker)

    def _do_basemap(self):
        if not _OK_BASEMAP:
            return
        if self._basemap:
            return
        longitude_min = math.floor(self.pygicobj.longitude_min)
        latitude_min = math.floor(self.pygicobj.latitude_min)
        longitude_max = math.ceil(self.pygicobj.longitude_max)
        latitude_max = math.ceil(self.pygicobj.latitude_max)
        diff_lon = abs(abs(longitude_max) - abs(longitude_min))
        diff_lat = abs(abs(latitude_max) - abs(latitude_min))
        margin_lon = min(1.0, diff_lon)
        margin_lat = min(1.0, diff_lat)
        llcrnrlon = longitude_min - margin_lon
        urcrnrlon = longitude_max + margin_lon
        llcrnrlat = latitude_min - margin_lat
        urcrnrlat = latitude_max + margin_lat
        llcrnrlon = math.floor(llcrnrlon)
        llcrnrlat = math.floor(llcrnrlat)
        urcrnrlon = math.ceil(urcrnrlon)
        urcrnrlat = math.ceil(urcrnrlat)
        diff_lon = abs(abs(llcrnrlon) - abs(urcrnrlon))
        diff_lat = abs(abs(llcrnrlat) - abs(urcrnrlat))
        lon_0 = llcrnrlon + 0.5 * diff_lon
        lat_0 = llcrnrlat + 0.5 * diff_lat
        scale_lon = int(diff_lon / 5.0)
        if scale_lon < 1.0:
            scale_lon = 1.0
        scale_lat = int(diff_lat / 5.0)
        if scale_lat < 1.0:
            scale_lat = 1.0
        self._basemap = Basemap(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, resolution='c', projection='stere', lon_0=lon_0, lat_0=lat_0)
        self.llcrnrlon = llcrnrlon
        self.urcrnrlon = urcrnrlon
        self.llcrnrlat = llcrnrlat
        self.urcrnrlat = urcrnrlat
        self.scale_lon = scale_lon
        self.scale_lat = scale_lat

    def _plot_ss_brn_on_base_map(self, quiver=False):
        self._do_basemap()
        if not self._basemap:
            return (True, None, None, None)
        else:
            self._fignum += 1
            fig = plt.figure(num=self._fignum)
            ax = fig.add_subplot(111)
            legends_dict_limitkv = {}
            for brn, vdict in self.pygicobj.branch.items():
                i = brn[0]
                j = brn[1]
                distance = vdict['distance']
                if distance < 1.0:
                    continue
                basekv = self.pygicobj.bus[i]['basekv']
                si = self.pygicobj.bus[i]['substation']
                sj = self.pygicobj.bus[j]['substation']
                loni = self.pygicobj.substation[si]['longitude']
                lati = self.pygicobj.substation[si]['latitude']
                lonj = self.pygicobj.substation[sj]['longitude']
                latj = self.pygicobj.substation[sj]['latitude']
                x, y = self._basemap([loni, lonj], [lati, latj])
                limitkv, color, linewidth = self._get_color_linewidth_basekv(basekv)
                l, = self._basemap.plot(x, y, linewidth=linewidth, color=color)
                if limitkv not in legends_dict_limitkv:
                    legends_dict_limitkv[limitkv] = {'handle': l, 'color': color}
                if quiver:
                    gic = vdict['gic']
                    if not gic:
                        continue
                    if gic > 0:
                        gicdir = 'from2to'
                    else:
                        gicdir = 'to2from'
                    if distance > self.distance_threshold:
                        xarw, yarw = self._get_arrow_points(loni, lati, lonj, latj)
                        if len(xarw) > 2:
                            xproj, yproj = self._basemap(xarw, yarw)
                            arwscale = 4 * distance / self.distance_max
                            x, y, u, v = self._get_quiver_data(xproj, yproj, gicdir)
                            self._basemap.quiver(x, y, u, v, scale_units='xy', angles='xy', scale=arwscale, color=color, edgecolor=color, headwidth=5, headlength=7, pivot='mid')

            if self._legend_optns_kv['show']:
                for n, limitkv in enumerate(self._legends_base_kv_seq):
                    if limitkv not in legends_dict_limitkv:
                        continue
                    if n + 1 == len(self._legends_base_kv_seq):
                        txt = '>=%g kV' % self._legends_base_kv_seq[-1]
                    else:
                        txt = '%g<=kV<%g' % (self._legends_base_kv_seq[n], self._legends_base_kv_seq[n + 1])
                    legends_dict_limitkv[limitkv]['label'] = txt

                legends_dict_limitkv_ordered = {}
                n = -1
                for limitkv in self._legends_base_kv_seq:
                    if limitkv not in legends_dict_limitkv:
                        continue
                    n += 1
                    legends_dict_limitkv_ordered[n] = {'handle': (legends_dict_limitkv[limitkv]['handle']), 'label': (legends_dict_limitkv[limitkv]['label']), 
                       'color': (legends_dict_limitkv[limitkv]['color'])}

                nmlgds, hdlist, lblist = legends_dict_limitkv_ordered.keys(), [], []
                nmlgds.sort()
                for n in nmlgds:
                    hdlist.append(legends_dict_limitkv_ordered[n]['handle'])
                    lblist.append(legends_dict_limitkv_ordered[n]['label'])

                legend_limitkv = ax.legend(hdlist, lblist, loc=self._legend_optns_kv['loc'], borderpad=self._legend_optns_kv['borderpad'], labelspacing=self._legend_optns_kv['labelspacing'], handlelength=self._legend_optns_kv['handlelength'], handletextpad=self._legend_optns_kv['handletextpad'], prop={'size': (self._legend_optns_kv['fontsize'])})
                for nn, l in enumerate(legend_limitkv.get_texts()):
                    clr = legends_dict_limitkv_ordered[nn]['color']
                    l.set_color(clr)

                legend_limitkv.get_frame().set_linewidth(0)
                legend_limitkv.draggable(True)
            else:
                legend_limitkv = None
            return (False, fig, ax, legend_limitkv)

    def _plot_main_brngic(self, ttl, figfile, dpi):
        ierr, fig, ax, legend_limitkv = self._plot_ss_brn_on_base_map(quiver=True)
        if ierr:
            return (None, None)
        else:
            self._decorate_and_save(ax, fig, ttl, figfile, dpi)
            return (
             ax, fig)

    def _plot_main_ssgic(self, ttl, figfile, dpi):
        ierr, fig, ax, lgd1 = self._plot_ss_brn_on_base_map(quiver=False)
        if ierr:
            return (None, None)
        else:
            gic_in = []
            gic_out = []
            gicmax = 0.0
            for ss, vdict in self.pygicobj.substation.items():
                gic = vdict['gic']
                if abs(gic) > gicmax:
                    gicmax = abs(gic)
                if gic < 0.0:
                    if gic not in gic_in:
                        gic_in.append(gic)
                elif gic > 0.0:
                    if gic not in gic_out:
                        gic_out.append(gic)

            gic_in.sort()
            gic_out.sort()
            legends_dict_ssgic = {}
            for ss, vdict in self.pygicobj.substation.items():
                lon = vdict['longitude']
                lat = vdict['latitude']
                gic = vdict['gic']
                flowdir, color, linewidth, marker = self._get_color_linewidth_flow_dir(gic)
                msz = self._maxmarksz_ssgic * abs(gic) / gicmax
                x, y = self._basemap(lon, lat)
                l, = self._basemap.plot(x, y, marker, markersize=msz, markerfacecolor=color, markeredgecolor=color)
                if flowdir not in legends_dict_ssgic:
                    legends_dict_ssgic[flowdir] = {'handle': l, 'color': color}

            for flowdir in _LEGENDS_FLOW_DIR_SEQ:
                if flowdir not in legends_dict_ssgic:
                    continue
                if flowdir == 'in':
                    txt = 'GIC flowing into ground'
                else:
                    txt = 'GIC flowing into bus'
                legends_dict_ssgic[flowdir]['label'] = txt

            legends_dict_ssgic_ordered = {}
            n = -1
            for flowdir in _LEGENDS_FLOW_DIR_SEQ:
                if flowdir not in legends_dict_ssgic:
                    continue
                n += 1
                legends_dict_ssgic_ordered[n] = {'handle': (legends_dict_ssgic[flowdir]['handle']), 'label': (legends_dict_ssgic[flowdir]['label']), 
                   'color': (legends_dict_ssgic[flowdir]['color'])}

            if self._legend_optns_ssgic_desc['show']:
                nmlgds, hdlist, lblist = legends_dict_ssgic_ordered.keys(), [], []
                nmlgds.sort()
                for n in nmlgds:
                    hdlist.append(legends_dict_ssgic_ordered[n]['handle'])
                    lblist.append(legends_dict_ssgic_ordered[n]['label'])

                lgd2 = ax.legend(hdlist, lblist, loc=self._legend_optns_ssgic_desc['loc'], borderpad=self._legend_optns_ssgic_desc['borderpad'], labelspacing=self._legend_optns_ssgic_desc['labelspacing'], handlelength=self._legend_optns_ssgic_desc['handlelength'], handletextpad=self._legend_optns_ssgic_desc['handletextpad'], prop={'size': (self._legend_optns_ssgic_desc['fontsize'])}, numpoints=1)
            else:
                lgd2 = None
            lgd3 = None
            lgd3_in = None
            lgd3_ou = None
            if (gic_in or gic_out) and self._legend_optns_ssgic_vals['show']:
                hdlist, lgd3clrlist, lgd3giclist, lblist = ([], [], [], [])
                hdlist_in, lgd3clrlist_in, lgd3giclist_in, lblist_in = ([], [], [], [])
                hdlist_ou, lgd3clrlist_ou, lgd3giclist_ou, lblist_ou = ([], [], [], [])
                if gic_in:
                    flowdir, clr, linewidth, mkr = self._get_color_linewidth_flow_dir(gic_in[0])
                    hdl = legends_dict_ssgic[flowdir]['handle']
                    hdlist_in.append(hdl)
                    lgd3clrlist_in.append(clr)
                    lgd3giclist_in.append(gic_in[0])
                    lblist_in.append('%0.2f A' % gic_in[0])
                    if len(gic_in) > 1:
                        hdlist_in.append(hdl)
                        lgd3clrlist_in.append(clr)
                        lgd3giclist_in.append(gic_in[-1])
                        lblist_in.append('%0.2f A' % gic_in[-1])
                if gic_out:
                    flowdir, clr, linewidth, mkr = self._get_color_linewidth_flow_dir(gic_out[-1])
                    hdl = legends_dict_ssgic[flowdir]['handle']
                    hdlist_ou.append(hdl)
                    lgd3clrlist_ou.append(clr)
                    lgd3giclist_ou.append(gic_out[-1])
                    lblist_ou.append('%0.2f A' % gic_out[-1])
                    if len(gic_out) > 1:
                        hdlist_ou.append(hdl)
                        lgd3clrlist_ou.append(clr)
                        lgd3giclist_ou.append(gic_out[0])
                        lblist_ou.append('%0.2f A' % gic_out[0])
                if self._legend_optns_ssgic_vals['loc']:
                    for a, b, c, d in zip(hdlist_in, lgd3clrlist_in, lgd3giclist_in, lblist_in):
                        hdlist.append(a)
                        lgd3clrlist.append(b)
                        lgd3giclist.append(c)
                        lblist.append(d)

                    for a, b, c, d in zip(hdlist_ou, lgd3clrlist_ou, lgd3giclist_ou, lblist_ou):
                        hdlist.append(a)
                        lgd3clrlist.append(b)
                        lgd3giclist.append(c)
                        lblist.append(d)

                    lgd3 = ax.legend(hdlist, lblist, loc=self._legend_optns_ssgic_vals['loc'], borderpad=self._legend_optns_ssgic_vals['borderpad'], labelspacing=self._legend_optns_ssgic_vals['labelspacing'], handlelength=self._legend_optns_ssgic_vals['handlelength'], handletextpad=self._legend_optns_ssgic_vals['handletextpad'], prop={'size': (self._legend_optns_ssgic_vals['fontsize'])}, numpoints=1)
                    if lgd1:
                        ax.add_artist(lgd1)
                    if lgd2:
                        ax.add_artist(lgd2)
                else:
                    if lblist_in:
                        lgd3_in = ax.legend(hdlist_in, lblist_in, loc=self._legend_optns_ssgic_vals['loc_in'], borderpad=self._legend_optns_ssgic_vals['borderpad'], labelspacing=self._legend_optns_ssgic_vals['labelspacing'], handlelength=self._legend_optns_ssgic_vals['handlelength'], handletextpad=self._legend_optns_ssgic_vals['handletextpad'], prop={'size': (self._legend_optns_ssgic_vals['fontsize'])}, numpoints=1)
                    if lblist_ou:
                        lgd3_ou = ax.legend(hdlist_ou, lblist_ou, loc=self._legend_optns_ssgic_vals['loc_out'], borderpad=self._legend_optns_ssgic_vals['borderpad'], labelspacing=self._legend_optns_ssgic_vals['labelspacing'], handlelength=self._legend_optns_ssgic_vals['handlelength'], handletextpad=self._legend_optns_ssgic_vals['handletextpad'], prop={'size': (self._legend_optns_ssgic_vals['fontsize'])}, numpoints=1)
                    if lgd3_ou:
                        if lgd3_in:
                            ax.add_artist(lgd3_in)
                    if lgd1:
                        ax.add_artist(lgd1)
                    if lgd2:
                        ax.add_artist(lgd2)
            elif lgd1:
                ax.add_artist(lgd1)
            if lgd2:
                for nn, l in enumerate(lgd2.get_texts()):
                    clr = legends_dict_ssgic_ordered[nn]['color']
                    l.set_color(clr)

                for l in lgd2.get_lines():
                    l._legmarker.set_markersize(5)

                lgd2.get_frame().set_linewidth(0)
                lgd2.draggable(True)
            if lgd3:
                for nn, l in enumerate(lgd3.get_texts()):
                    clr = lgd3clrlist[nn]
                    l.set_color(clr)

                for nn, l in enumerate(lgd3.get_lines()):
                    msz = self._maxmarksz_ssgic * abs(lgd3giclist[nn]) / gicmax
                    l._legmarker.set_markersize(msz)

                lgd3.get_frame().set_linewidth(0)
                lgd3.draggable(True)
            if lgd3_in:
                for nn, l in enumerate(lgd3_in.get_texts()):
                    clr = lgd3clrlist_in[nn]
                    l.set_color(clr)

                for nn, l in enumerate(lgd3_in.get_lines()):
                    msz = self._maxmarksz_ssgic * abs(lgd3giclist_in[nn]) / gicmax
                    l._legmarker.set_markersize(msz)

                lgd3_in.get_frame().set_linewidth(0)
                lgd3_in.draggable(True)
            if lgd3_ou:
                for nn, l in enumerate(lgd3_ou.get_texts()):
                    clr = lgd3clrlist_ou[nn]
                    l.set_color(clr)

                for nn, l in enumerate(lgd3_ou.get_lines()):
                    msz = self._maxmarksz_ssgic * abs(lgd3giclist_ou[nn]) / gicmax
                    l._legmarker.set_markersize(msz)

                lgd3_ou.get_frame().set_linewidth(0)
                lgd3_ou.draggable(True)
            self._decorate_and_save(ax, fig, ttl, figfile, dpi)
            return (
             ax, fig)

    def _plot_main_ssvpu(self, ttl, figfile, dpi):
        pf_flag = self.pygicobj.power_flow_solution_flag
        if pf_flag:
            if self._ss_voltage_case == 'gic':
                msg = '\n Power flow solution condition: %s (%s)\n' % (pf_flag, self.pygicobj.power_flow_solution_cond)
                msg += '     GIC case bus voltage plot not drawn.'
                print msg
                return (None, None)
        ierr, fig, ax, lgd1 = self._plot_ss_brn_on_base_map(quiver=False)
        if ierr:
            return (None, None)
        else:
            vpulist = []
            ssvpu_dict = {}
            for ss, vdict in self._substation_voltages.items():
                if self._ss_voltage_case == 'gic':
                    if self._ss_voltage_limit == 'min':
                        vpu = vdict['min_vpu_gic']
                    else:
                        vpu = vdict['max_vpu_gic']
                elif self._ss_voltage_limit == 'min':
                    vpu = vdict['min_vpu_base']
                else:
                    vpu = vdict['max_vpu_base']
                ssvpu_dict[ss] = vpu
                if vpu not in vpulist:
                    vpulist.append(vpu)

            vpulist.sort()
            if self._ss_voltage_limit == 'max':
                vpulist.reverse()
            legends_dict_ssvpu = {}
            for ss, vdict in self._substation_voltages.items():
                lon = self.pygicobj.substation[ss]['longitude']
                lat = self.pygicobj.substation[ss]['latitude']
                vpu = ssvpu_dict[ss]
                limitpu, color = self._get_color_buspu(vpu)
                msz = self._maxmarksz_ssvpu * abs(vpu - 1.0) + 1
                x, y = self._basemap(lon, lat)
                l, = self._basemap.plot(x, y, 'o', markersize=msz, markerfacecolor=color, markeredgecolor=color)
                if limitpu not in legends_dict_ssvpu:
                    legends_dict_ssvpu[limitpu] = {'handle': l, 'color': color}

            for n, limitpu in enumerate(self._legends_bus_pu_seq):
                if limitpu not in legends_dict_ssvpu:
                    continue
                if n + 1 == len(self._legends_bus_pu_seq):
                    txt = '>=%g pu' % self._legends_bus_pu_seq[-1]
                else:
                    txt = '%g<=pu<%g' % (self._legends_bus_pu_seq[n], self._legends_bus_pu_seq[n + 1])
                legends_dict_ssvpu[limitpu]['label'] = txt

            legends_dict_ssvpu_ordered = {}
            n = -1
            for limitpu in self._legends_bus_pu_seq:
                if limitpu not in legends_dict_ssvpu:
                    continue
                n += 1
                legends_dict_ssvpu_ordered[n] = {'handle': (legends_dict_ssvpu[limitpu]['handle']), 'label': (legends_dict_ssvpu[limitpu]['label']), 
                   'color': (legends_dict_ssvpu[limitpu]['color'])}

            if self._legend_optns_vpu_desc['show']:
                nmlgds, hdlist, lblist = legends_dict_ssvpu_ordered.keys(), [], []
                nmlgds.sort()
                for n in nmlgds:
                    hdlist.append(legends_dict_ssvpu_ordered[n]['handle'])
                    lblist.append(legends_dict_ssvpu_ordered[n]['label'])

                lgd2 = ax.legend(hdlist, lblist, loc=self._legend_optns_vpu_desc['loc'], borderpad=self._legend_optns_vpu_desc['borderpad'], labelspacing=self._legend_optns_vpu_desc['labelspacing'], handlelength=self._legend_optns_vpu_desc['handlelength'], handletextpad=self._legend_optns_vpu_desc['handletextpad'], prop={'size': (self._legend_optns_vpu_desc['fontsize'])}, numpoints=1)
            else:
                lgd2 = None
            if vpulist and self._legend_optns_vpu_vals['show']:
                hdlist, lgd3clrlist, lgd3vpulist, lblist = ([], [], [], [])
                limitpu, clr = self._get_color_buspu(vpulist[0])
                hdl = legends_dict_ssvpu[limitpu]['handle']
                hdlist.append(hdl)
                lgd3clrlist.append(clr)
                lgd3vpulist.append(vpulist[0])
                lblist.append('%0.4g pu' % vpulist[0])
                if len(vpulist) > 1:
                    hdlist.append(hdl)
                    lgd3clrlist.append(clr)
                    lgd3vpulist.append(vpulist[-1])
                    lblist.append('%0.4g pu' % vpulist[-1])
                lgd3 = ax.legend(hdlist, lblist, loc=self._legend_optns_vpu_vals['loc'], borderpad=self._legend_optns_vpu_vals['borderpad'], labelspacing=self._legend_optns_vpu_vals['labelspacing'], handlelength=self._legend_optns_vpu_vals['handlelength'], handletextpad=self._legend_optns_vpu_vals['handletextpad'], prop={'size': (self._legend_optns_vpu_vals['fontsize'])}, numpoints=1)
                if lgd1:
                    ax.add_artist(lgd1)
                if lgd2:
                    ax.add_artist(lgd2)
            elif lgd1:
                ax.add_artist(lgd1)
            lgd3 = None
            if lgd2:
                for nn, l in enumerate(lgd2.get_texts()):
                    clr = legends_dict_ssvpu_ordered[nn]['color']
                    l.set_color(clr)

                for l in lgd2.get_lines():
                    l._legmarker.set_markersize(5)

                lgd2.get_frame().set_linewidth(0)
                lgd2.draggable(True)
            if lgd3:
                for nn, l in enumerate(lgd3.get_texts()):
                    clr = lgd3clrlist[nn]
                    l.set_color(clr)

                for nn, l in enumerate(lgd3.get_lines()):
                    msz = self._maxmarksz_ssvpu * abs(lgd3vpulist[nn] - 1.0) + 1
                    l._legmarker.set_markersize(msz)

                lgd3.get_frame().set_linewidth(0)
                lgd3.draggable(True)
            self._decorate_and_save(ax, fig, ttl, figfile, dpi)
            return (
             ax, fig)

    def _draw_boundaries_lat_lon(self):
        self._basemap.drawmapboundary(fill_color='white')
        if self._state_optns['show']:
            self._basemap.drawstates(linewidth=self._state_optns['linewidth'], color=self._state_optns['color'])
        if self._meridians_optns['show']:
            self._basemap.drawmeridians(np.arange(self.llcrnrlon, self.urcrnrlon, self.scale_lon), labels=[0, 0, 0, 1], linewidth=self._meridians_optns['linewidth'], color=self._meridians_optns['color'], dashes=self._meridians_optns['dashes'], fontsize=self._meridians_optns['fontsize'])
        if self._parallels_optns['show']:
            self._basemap.drawparallels(np.arange(self.llcrnrlat, self.urcrnrlat, self.scale_lat), labels=[1, 0, 0, 0], linewidth=self._parallels_optns['linewidth'], color=self._parallels_optns['color'], dashes=self._parallels_optns['dashes'], fontsize=self._parallels_optns['fontsize'])

    def _decorate_and_save(self, ax, fig, ttl, figfile, dpi):
        self._draw_boundaries_lat_lon()
        if self._xlabel_optns['label']:
            ax.set_xlabel(self._xlabel_optns['label'], labelpad=self._xlabel_optns['labelpad'], color=self._xlabel_optns['color'], fontsize=self._xlabel_optns['fontsize'])
        if self._ylabel_optns['label']:
            ax.set_ylabel(self._ylabel_optns['label'], labelpad=self._ylabel_optns['labelpad'], color=self._ylabel_optns['color'], fontsize=self._ylabel_optns['fontsize'])
        if ttl:
            ax.set_title(ttl, color=self._title_optns['color'], fontsize=self._title_optns['fontsize'])
        self._do_ss_annotation(ax)
        if figfile:
            fig.savefig(figfile, dpi=dpi, bbox_inches='tight')

    def _decorate_and_save_qtotal(self, ax, fig, figfile, dpi, title):
        if title:
            ttl = title
        else:
            ttl = self._title_optns_qtotal['label']
        if self._xlabel_optns_qtotal['label']:
            ax.set_xlabel(self._xlabel_optns_qtotal['label'], labelpad=self._xlabel_optns_qtotal['labelpad'], color=self._xlabel_optns_qtotal['color'], fontsize=self._xlabel_optns_qtotal['fontsize'])
        if self._ylabel_optns_qtotal['label']:
            ax.set_ylabel(self._ylabel_optns_qtotal['label'], labelpad=self._ylabel_optns_qtotal['labelpad'], color=self._ylabel_optns_qtotal['color'], fontsize=self._ylabel_optns_qtotal['fontsize'])
        if self._title_optns_qtotal['label']:
            ax.set_title(ttl, color=self._title_optns_qtotal['color'], fontsize=self._title_optns_qtotal['fontsize'])
        if figfile:
            fig.savefig(figfile, dpi=dpi, bbox_inches='tight')

    def _check_and_set_options(self, *args):
        tmpdict = {}
        for each in args:
            key = each[0]
            val = each[1]
            defval = each[2]
            valtyp = each[3]
            if valtyp in ('str', 'bool'):
                if type(val) == eval(valtyp):
                    if type(val) == str:
                        tmpdict[key] = val.strip()
                    else:
                        tmpdict[key] = val
                else:
                    tmpdict[key] = defval
            elif valtyp == 'float':
                if type(val) in [int, float]:
                    tmpdict[key] = val
                else:
                    tmpdict[key] = defval
            elif valtyp == 'intlist':
                if type(val) in [list, tuple]:
                    v = []
                    for e in val:
                        if type(e) == int:
                            v.append(e)

                    if v:
                        tmpdict[key] = v
                    else:
                        tmpdict[key] = defval
                else:
                    tmpdict[key] = defval

        return tmpdict

    def _validate_legend_loc_string(self, loc, defval):
        if loc:
            loc = loc.lower()
            if loc not in ('upper right', 'upper left', 'lower left', 'lower right',
                           'right', 'center left', 'center right', 'lower center',
                           'upper center', 'center'):
                loc = defval
        return loc

    def set_state_boundary_options(self, show=True, color='#CCCCCC', linewidth=0.5):
        """Set state boundary options.
    where:
    show      -> True to draw state boundaries, default=True, allowed: True and False
    color     -> Any valid matplotlib color name or valid HTML hex string, default='#CCCCCC'
    linewidth -> Line width, defaul=0.5
"""
        self._state_optns = self._check_and_set_options((
         'show', show, True, 'bool'), (
         'color', color, '#CCCCCC', 'str'), (
         'linewidth', linewidth, 0.5, 'float'))

    def set_longitude_options(self, show=True, color='#CCFFFF', linewidth=1.0, dashes=[1, 3], fontsize=10):
        """Set longitude lines (meridians) options.
    where:
    show      -> True to draw longitude lines, default=True, allowed: True and False
    color     -> Any valid matplotlib color name or valid HTML hex string, default=black' or '#CCFFFF'
    linewidth -> Line width, default=1.0
    dashes    -> dash pattern for meridians, default=[1,3], i.e. 1 pixel on, 3 pixel off
    fontsize  -> Label font size, default=10
"""
        self._meridians_optns = self._check_and_set_options((
         'show', show, True, 'bool'), (
         'color', color, '#CCFFFF', 'str'), (
         'linewidth', linewidth, 1.0, 'float'), (
         'dashes', dashes, [1, 3], 'intlist'), (
         'fontsize', fontsize, 10, 'float'))

    def set_latitude_options(self, show=True, color='#CCFFFF', linewidth=1.0, dashes=[1, 1], fontsize=10):
        """Set latitude lines (parallels) options.
    where:
    show      -> True to draw latitude lines, default=True, allowed: True and False
    color     -> Any valid matplotlib color name or valid HTML hex string, default='#CCFFFF'
    linewidth -> Line width, default=1.0
    dashes    -> dash pattern for meridians, default=[1,3], i.e. 1 pixel on, 3 pixel off
    fontsize  -> Label font size, default=10
"""
        self._parallels_optns = self._check_and_set_options((
         'show', show, True, 'bool'), (
         'color', color, '#CCFFFF', 'str'), (
         'linewidth', linewidth, 1.0, 'float'), (
         'dashes', dashes, [1, 3], 'intlist'), (
         'fontsize', fontsize, 10, 'float'))

    def set_options_base_kv_colors(self, kv_thresholds={}):
        """Set bus base kV color and linewidth to draw network on map.
    kv_thresholds is a dictionary of the format:
        kv_thresholds = { kv1: {'color':'black',   'linewidth':1.5},
                          kv2: {'color':'#00FF00', 'linewidth':2.0},
                        }
        Where:
        kv1, kv2 are bus base kV threshold levels.
        color -> Any valid matplotlib color name or valid HTML hex string, e.g., 'black' or '#000000'
        Defaults used:
            kv_thresholds = {
                0  : {'color':'#666666', 'linewidth':1.0},   # black
                169: {'color':'#00FFFF', 'linewidth':1.5},   # cyan
                230: {'color':'#FF3300', 'linewidth':2.0},   # red
                345: {'color':'#FFCC00', 'linewidth':2.5},   # golden
                500: {'color':'#00FF00', 'linewidth':3.0},   # green
        Here for   0 >= kv < 169  --> color = black
                 169 >= kv < 230  --> color = cyan
                 230 >= kv < 345  --> color = red
                 345 >= kv < 500  --> color = golden
                 500 >= kv        --> color = green
                }
"""
        input_legends = {}
        if type(kv_thresholds) == dict:
            for kv, vdict in kv_thresholds.items():
                if type(kv) not in [float, int]:
                    continue
                if 'color' in vdict:
                    clr = vdict['color']
                else:
                    clr = ''
                if 'linewidth' in vdict:
                    lwd = vdict['linewidth']
                    if type(lwd) not in [float, int]:
                        lwd = ''
                else:
                    lwd = ''
                if clr and lwd:
                    input_legends[kv] = {'color': clr, 'linewidth': lwd}

        if not input_legends:
            input_legends = {0: {'color': '#666666', 'linewidth': 1.0}, 169: {'color': '#00FFFF', 'linewidth': 1.5}, 230: {'color': '#FF3300', 'linewidth': 2.0}, 345: {'color': '#FFCC00', 'linewidth': 2.5}, 500: {'color': '#00FF00', 'linewidth': 3.0}}
        self._legends_base_kv = input_legends
        self._legends_base_kv_seq = self._legends_base_kv.keys()
        self._legends_base_kv_seq.sort()

    def set_options_voltage_pu_colors(self, pu_thresholds={}):
        """Set bus pu voltage (obtained after power flow solution) color. It is used to paint bus nodes.
    pu_thresholds is a dictionary of the format:
        pu_thresholds = { pu1: {'color':'#FF3300'},   # red
                          pu2: {'color':'#33FF00'},   # green
                          pu3: {'color':'#0033FF'},   # blue
                        }
        Where:
        pu1, pu2, pu3 are bus pu voltage levels.
        color -> Any valid matplotlib color name or valid HTML hex string, e.g., 'red' or '#FF3300'
        Defaults used:
            pu_thresholds = {
                0.0 : {'color':'#FF3300'},   # red
                0.95: {'color':'#33FF00'},   # green
                1.05: {'color':'#0033FF'},   # blue
                }
        Here for   0  >= pu < 0.95 --> color = red
                 0.95 >= pu < 1.05 --> color = green
                 1.05 >= pu        --> color = blue
"""
        input_legends = {}
        if type(pu_thresholds) == dict:
            for pu, vdict in pu_thresholds.items():
                if type(pu) not in [float, int]:
                    continue
                if 'color' in vdict:
                    clr = vdict['color']
                else:
                    clr = ''
                if clr:
                    input_legends[pu] = {'color': clr}

        if not input_legends:
            input_legends = {0.0: {'color': '#FF3300'}, 0.95: {'color': '#33FF00'}, 1.05: {'color': '#0033FF'}}
        self._legends_bus_pu = input_legends
        self._legends_bus_pu_seq = self._legends_bus_pu.keys()
        self._legends_bus_pu_seq.sort()

    def set_legend_options_kv(self, show=True, loc='upper right', borderpad=0.0, labelspacing=0.5, handlelength=1.5, handletextpad=0.5, fontsize=10):
        """Set bus base kV description legend options. The legend can be dragged to adjust its position.
    where:
    show          -> True to kV legend, default=True, allowed: True and False
    loc           -> Any valid matplotlib legend location string, default='upper right'
                     Allowed: 'upper right', 'upper left', 'lower left', 'lower right',
                     'right', 'center left', 'center right', 'lower center', 'upper center',
                     'center'
    borderpad     -> Whitespace inside the legend border, default=0.0
    labelspacing  -> Vertical space between the legend entries, default=0.5
    handlelength  -> Length of the legend handles, default=1.5
    handletextpad -> Pad between the legend handle and text, default=0.5
    fontsize      -> Font size, default=10
    Note: The pad and spacing parameters are measured in font-size units.
          A fontsize of 10 points and a handlelength=5 implies a handlelength of 50 points.
"""
        self._legend_optns_kv = self._check_and_set_options((
         'show', show, True, 'bool'), (
         'loc', loc, 'upper right', 'str'), (
         'borderpad', borderpad, 0.0, 'float'), (
         'labelspacing', labelspacing, 0.5, 'float'), (
         'handlelength', handlelength, 1.5, 'float'), (
         'handletextpad', handletextpad, 0.5, 'float'), (
         'fontsize', fontsize, 10, 'float'))
        self._legend_optns_kv['loc'] = self._validate_legend_loc_string(self._legend_optns_kv['loc'], 'upper right')

    def set_legend_options_voltage_pu_desc(self, show=True, loc='upper left', borderpad=0.0, labelspacing=0.5, handlelength=1.5, handletextpad=0.5, fontsize=10):
        """Set bus pu voltage description legend options. The legend can be dragged to adjust its position.
    where:
    show          -> True to kV legend, default=True, allowed: True and False
    loc           -> Any valid matplotlib legend location string, default='upper right'
                     Allowed: 'upper right', 'upper left', 'lower left', 'lower right',
                     'right', 'center left', 'center right', 'lower center', 'upper center',
                     'center'
    borderpad     -> Whitespace inside the legend border, default=0.0
    labelspacing  -> Vertical space between the legend entries, default=0.5
    handlelength  -> Length of the legend handles, default=1.5
    handletextpad -> Pad between the legend handle and text, default=0.5
    fontsize      -> Font size, default=10
    Note: The pad and spacing parameters are measured in font-size units.
          A fontsize of 10 points and a handlelength=5 implies a handlelength of 50 points.
"""
        self._legend_optns_vpu_desc = self._check_and_set_options((
         'show', show, True, 'bool'), (
         'loc', loc, 'upper left', 'str'), (
         'borderpad', borderpad, 0.0, 'float'), (
         'labelspacing', labelspacing, 0.5, 'float'), (
         'handlelength', handlelength, 1.5, 'float'), (
         'handletextpad', handletextpad, 0.5, 'float'), (
         'fontsize', fontsize, 10, 'float'))
        self._legend_optns_vpu_desc['loc'] = self._validate_legend_loc_string(self._legend_optns_vpu_desc['loc'], 'upper left')

    def set_legend_options_voltage_pu_values(self, show=True, loc='upper center', borderpad=0.2, labelspacing=0.5, handlelength=1.5, handletextpad=0.5, fontsize=10):
        """Set bus pu voltage values legend options. The legend can be dragged to adjust its position.
    where:
    show          -> True to kV legend, default=True, allowed: True and False
    loc           -> Any valid matplotlib legend location string, default='upper right'
                     Allowed: 'upper right', 'upper left', 'lower left', 'lower right',
                     'right', 'center left', 'center right', 'lower center', 'upper center',
                     'center'
    borderpad     -> Whitespace inside the legend border, default=0.2
    labelspacing  -> Vertical space between the legend entries, default=0.5
    handlelength  -> Length of the legend handles, default=1.5
    handletextpad -> Pad between the legend handle and text, default=0.5
    fontsize      -> Font size, default=10
    Note: The pad and spacing parameters are measured in font-size units.
          A fontsize of 10 points and a handlelength=5 implies a handlelength of 50 points.
"""
        self._legend_optns_vpu_vals = self._check_and_set_options((
         'show', show, True, 'bool'), (
         'loc', loc, 'upper center', 'str'), (
         'borderpad', borderpad, 0.2, 'float'), (
         'labelspacing', labelspacing, 0.5, 'float'), (
         'handlelength', handlelength, 1.5, 'float'), (
         'handletextpad', handletextpad, 0.5, 'float'), (
         'fontsize', fontsize, 10, 'float'))
        self._legend_optns_vpu_vals['loc'] = self._validate_legend_loc_string(self._legend_optns_vpu_vals['loc'], 'upper center')

    def set_legend_options_ss_gic_desc(self, show=True, loc='upper left', borderpad=0.0, labelspacing=0.5, handlelength=1.5, handletextpad=0.5, fontsize=10):
        """Set substation gic flow description legend options. The legend can be dragged to adjust its position.
    where:
    show          -> True to kV legend, default=True, allowed: True and False
    loc           -> Any valid matplotlib legend location string, default='upper right'
                     Allowed: 'upper right', 'upper left', 'lower left', 'lower right',
                     'right', 'center left', 'center right', 'lower center', 'upper center',
                     'center'
    borderpad     -> Whitespace inside the legend border, default=0.0
    labelspacing  -> Vertical space between the legend entries, default=0.5
    handlelength  -> Length of the legend handles, default=1.5
    handletextpad -> Pad between the legend handle and text, default=0.5
    fontsize      -> Font size, default=10
    Note: The pad and spacing parameters are measured in font-size units.
          A fontsize of 10 points and a handlelength=5 implies a handlelength of 50 points.
"""
        self._legend_optns_ssgic_desc = self._check_and_set_options((
         'show', show, True, 'bool'), (
         'loc', loc, 'upper left', 'str'), (
         'borderpad', borderpad, 0.0, 'float'), (
         'labelspacing', labelspacing, 0.5, 'float'), (
         'handlelength', handlelength, 1.5, 'float'), (
         'handletextpad', handletextpad, 0.5, 'float'), (
         'fontsize', fontsize, 10, 'float'))
        self._legend_optns_ssgic_desc['loc'] = self._validate_legend_loc_string(self._legend_optns_ssgic_desc['loc'], 'upper left')

    def set_legend_options_ss_gic_values(self, show=True, loc='upper center', loc_in='lower left', loc_out='lower right', borderpad=0.2, labelspacing=0.5, handlelength=1.5, handletextpad=0.5, fontsize=10):
        """Set substation gic flow values legend options. The legend can be dragged to adjust its position.
    Legends for GICs flowing into substation and flowing out of substation can be combined as one legend or put as
    two legends. When 'loc' is provided legends are combined and put at this location. When 'loc' is not provided
    legends are put in locations provided by 'loc_in' and 'loc_out'.
    where:
    show          -> True to kV legend, default=True, allowed: True and False
    loc           -> Any valid matplotlib legend location code for GICs flowing into and out of
                     substation, default='center'
                     When 'loc' is provided 'loc_in' and 'loc_out' are ignored.
    loc_in        -> Any valid matplotlib legend location code for GICs flowing into substation,
                     default='lower left'
    loc_out       -> Any valid matplotlib legend location code for GICs flowing out of substation,
                     default='lower right'
                     Allowed locations codes: 'upper right', 'upper left', 'lower left',
                     'lower right', 'right', 'center left', 'center right', 'lower center',
                     'upper center', 'center'
    borderpad     -> Whitespace inside the legend border, default=0.2
    labelspacing  -> Vertical space between the legend entries, default=0.5
    handlelength  -> Length of the legend handles, default=1.5
    handletextpad -> Pad between the legend handle and text, default=0.5
    fontsize      -> Font size, default=10
    Note: The pad and spacing parameters are measured in font-size units.
          A fontsize of 10 points and a handlelength=5 implies a handlelength of 50 points.
"""
        self._legend_optns_ssgic_vals = self._check_and_set_options((
         'show', show, True, 'bool'), (
         'loc', loc, 'upper center', 'str'), (
         'loc_in', loc_in, 'lower left', 'str'), (
         'loc_out', loc_out, 'lower right', 'str'), (
         'borderpad', borderpad, 0.2, 'float'), (
         'labelspacing', labelspacing, 0.5, 'float'), (
         'handlelength', handlelength, 1.5, 'float'), (
         'handletextpad', handletextpad, 0.5, 'float'), (
         'fontsize', fontsize, 10, 'float'))
        if loc:
            self._legend_optns_ssgic_vals['loc'] = self._validate_legend_loc_string(self._legend_optns_ssgic_vals['loc'], 'center')
        else:
            self._legend_optns_ssgic_vals['loc'] = None
        self._legend_optns_ssgic_vals['loc_in'] = self._validate_legend_loc_string(self._legend_optns_ssgic_vals['loc_in'], 'lower left')
        self._legend_optns_ssgic_vals['loc_out'] = self._validate_legend_loc_string(self._legend_optns_ssgic_vals['loc_out'], 'lower right')
        return

    def set_xlabel_options(self, label='Longitude (deg)', labelpad=20, color='blue', fontsize=10):
        """Set X axis label options.
    where:
    label    -> Label, default='Longitude (deg)',
                When label=None or '', label will not be added to the plot
    labelpad -> Spacing in points between the label and X-axis, default=20
    color    -> Any valid matplotlib color name or valid HTML hex string, default='blue'
    fontsize -> Font size, default=10
"""
        self._xlabel_optns = self._check_and_set_options((
         'label', label, 'Longitude (deg)', 'str'), (
         'labelpad', labelpad, 20, 'float'), (
         'color', color, 'blue', 'str'), (
         'fontsize', fontsize, 10, 'float'))

    def set_ylabel_options(self, label='Latitude (deg)', labelpad=30, color='blue', fontsize=10):
        """Set Y axis label options.
    where:
    label    -> Label, default='Latitude (deg)',
                When label=None or '', label will not be added to the plot
    labelpad -> Spacing in points between the label and Y-axis, default=30
    color    -> Any valid matplotlib color name or valid HTML hex string, default='blue'
    fontsize -> Font size, default=10
"""
        self._ylabel_optns = self._check_and_set_options((
         'label', label, 'Latitude (deg)', 'str'), (
         'labelpad', labelpad, 30, 'float'), (
         'color', color, 'blue', 'str'), (
         'fontsize', fontsize, 10, 'float'))

    def set_title_options(self, color='blue', fontsize=10):
        """Set Title options.
    where:
    color    -> Any valid matplotlib color name or valid HTML hex string, default='blue'
    fontsize -> Font size, default=10
"""
        self._title_optns = self._check_and_set_options((
         'color', color, 'blue', 'str'), (
         'fontsize', fontsize, 10, 'float'))

    def set_xlabel_options_qtotal(self, label='GMD Storm Direction (deg)', labelpad=10, color='blue', fontsize=10):
        """Set toal MVAR losses plot X axis label options.
    where:
    label    -> Label, default='GMD Storm Direction (deg)',
                When label=None or '', label will not be added to the plot
    labelpad -> Spacing in points between the label and X-axis, default=10
    color    -> Any valid matplotlib color name or valid HTML hex string, default='blue'
    fontsize -> Font size, default=10
"""
        self._xlabel_optns_qtotal = self._check_and_set_options((
         'label', label, 'GMD Storm Direction (deg)', 'str'), (
         'labelpad', labelpad, 10, 'float'), (
         'color', color, 'blue', 'str'), (
         'fontsize', fontsize, 10, 'float'))

    def set_ylabel_options_qtotal(self, label='Mvar', labelpad=10, color='blue', fontsize=10):
        """Set toal MVAR losses plot Y axis label options.
    where:
    label    -> Label, default='Mvar',
                When label=None or '', label will not be added to the plot
    labelpad -> Spacing in points between the label and Y-axis, default=10
    color    -> Any valid matplotlib color name or valid HTML hex string, default='blue'
    fontsize -> Font size, default=10
"""
        self._ylabel_optns_qtotal = self._check_and_set_options((
         'label', label, 'Mvar', 'str'), (
         'labelpad', labelpad, 10, 'float'), (
         'color', color, 'blue', 'str'), (
         'fontsize', fontsize, 10, 'float'))

    def set_title_options_qtotal(self, label='Total Transformer Mvar Losses', color='blue', fontsize=10):
        """Set toal MVAR losses plot Title options.
    where:
    label    -> Label, default='Total Transformer Mvar Losses',
                When label=None or '', label will not be added to the plot
    color    -> Any valid matplotlib color name or valid HTML hex string, default='blue'
    fontsize -> Font size, default=10
"""
        self._title_optns_qtotal = self._check_and_set_options((
         'label', label, 'Total Transformer Mvar Losses', 'str'), (
         'color', color, 'blue', 'str'), (
         'fontsize', fontsize, 10, 'float'))

    def annotate_substations(self, ss, color='black', fontsize=10):
        """Annotate map with substation numbers. These annotations can be dragged to adjust their position.
    where:
    ss    -> = list of substation numbers to be annotated on base map
             = [] or None, no substation number annotation
             = 'all', annotate all substation numbers
    color    -> Any valid matplotlib color name or valid HTML hex string, default='black'
    fontsize -> Font size, default=10
"""
        self.annotate_ss = {}
        self.annotate_ss['number'] = []
        self.annotate_ss['color'] = color
        self.annotate_ss['fontsize'] = fontsize
        if not ss:
            return
        if ss == 'all':
            self.annotate_ss['number'] = self.pygicobj.substation.keys()
        elif type(ss) == int:
            if ss in self.pygicobj.substation.keys():
                self.annotate_ss['number'].append(ss)
        elif type(ss) in [list, tuple]:
            for each in ss:
                if type(each) == int:
                    if each in self.pygicobj.substation.keys():
                        if each not in self.annotate_ss['number']:
                            self.annotate_ss['number'].append(each)

    def _do_ss_annotation(self, ax):
        for ss in self.annotate_ss['number']:
            longi = self.pygicobj.substation[ss]['longitude']
            lati = self.pygicobj.substation[ss]['latitude']
            x, y = self._basemap(longi, lati)
            ann = ax.annotate(str(ss), xy=(x, y), xytext=(x, y), color=self.annotate_ss['color'], fontsize=self.annotate_ss['fontsize'])
            ann.draggable(True)

    def annotate_text(self, s, x, y, ax, xycoords='long_lat', color='black', fontsize=10):
        """Add any text annotation at location provided by x, y. This annotation can be dragged to adjust its position.
    where:
    s        -> Text to be put on the plot
    x, y     -> x and y give co-ordinate location where text is placed.
                x => longitude
                y => latitude
    ax       -> Plot Axes instance on which text is to placed.
                (For example, plot_bus_voltages() returns ax, fig. This Axes instance is used here.)
    xycoords -> Type of data provided by x and y.
                = 'long_lat', for x and y representing longitude and latitude of a point, default
                = 'data', for x and y representing data value
    color    -> Any valid matplotlib color name or valid HTML hex string, default='black'
    fontsize -> Font size, default=10
"""
        if not s:
            return
        if type(s) != str:
            s = str(s)
        s = s.strip()
        if not s:
            return
        if xycoords.lower() == 'long_lat':
            x, y = self._basemap(x, y)
        ann = ax.annotate(s, xy=(x, y), xytext=(x, y), color=color, fontsize=fontsize)
        ann.draggable(True)

    def datapoint_xy_from_longitude_latiude(self, longitude, latiude):
        """Get a data point x and y co-ordinates on a map plot corresponding to its longitude and latitude.
    x, y = gicmapsobj.datapoint_xy_from_longitude_latiude(longitude, latiude)
where:
longitude -> A datapoint longitude on a map plot.
latiude   -> A datapoint latiude on a map plot.
Returns
x, y      -> x and y co-ordinates on a map plot corresponding to its longitude and latitude.
"""
        x, y = (None, None)
        if not longitude or not latiude:
            return (x, y)
        else:
            if type(longitude) not in [float, int]:
                return (x, y)
            if type(latiude) not in [float, int]:
                return (x, y)
            if not self._basemap:
                return (x, y)
            x, y = self._basemap(longitude, latiude)
            return (
             x, y)

    def plots_show(self):
        """Show created plots.
"""
        if self.ierr:
            return
        plt.show()

    def plots_close(self):
        """Close created plots.
"""
        if self.ierr:
            return
        plt.close('all')

    def plot_bus_voltages(self, figfile=None, case='gic', limit='min', title='Bus Voltages', dpi=300, markersize=100):
        """Plot power flow solution pu bus voltages. The voltages are plotted on substations in a map
only if power flow solution is converged.
Minimum and Maximum pu voltages from all buses terminating into substaions are found and plotted.
    ax, fig = gicmapsobj.plot_bus_voltages(figfile, case, limit, title, dpi, markersize)
figfile -> File name to save plot. File type could be any allowed by matplotlib (like png, pdf, ps, eps, svg)
case    -> 'gic'  <- PFlow solution pu bus voltages including GIC var losses
        -> 'base' <- base case PFlow solution pu bus voltages (GIC var losses not considered)
limit   -> 'min'  <- Minimum voltage from all substation buses
        -> 'max'  <- Maximum voltage from all substation buses
title   -> Plot title, default='Bus Voltages'
dpi     -> Resolution in dots per inch of saved figure, default=300
markersize -> Bus voltages are decorated with markers whose sizes are calculated as:
                  markersize*abs(vpu-1.0)+1
              where vpu is the actual bus voltages. It indicates how far away the bus voltage is from 1 pu.
              Default=100
Returns:
ax      -> the Axes instance
fig     -> the Figure instance
"""
        if self.ierr:
            return (None, None)
        else:
            self._ss_voltage_case = case
            self._ss_voltage_limit = limit
            self._maxmarksz_ssvpu = markersize
            ax, fig = self._plot_main_ssvpu(title, figfile, dpi)
            return (
             ax, fig)

    def plot_substation_gicflows(self, figfile=None, title='GIC flows in Substation ground', dpi=300, markersize=20):
        """Plot GICs flowing in substations.
    ax, fig = gicmapsobj.plot_substation_gicflows(figfile, title, dpi, markersize)
figfile -> File name to save plot. File type could be any allowed by matplotlib (like png, pdf, ps, eps, svg)
title   -> Plot title, default='GIC flows in Substation ground'
dpi     -> Resolution in dots per inch of saved figure, default=300
markersize -> GIC values are decorated with markers whose sizes are calculated as:
                    markersize*gic_actual/gic_maximum
              where gic_actual is the actual GIC amperes and gic_maximum is the maximum GIC amperes.
              Default=20
Returns:
ax      -> the Axes instance
fig     -> the Figure instance
"""
        if self.ierr:
            return (None, None)
        else:
            self._maxmarksz_ssgic = markersize
            ax, fig = self._plot_main_ssgic(title, figfile, dpi)
            return (
             ax, fig)

    def plot_branch_gicflows(self, figfile=None, title='GIC flows in Transmission Lines', dpi=300):
        """Plot GICs flowing in branches.
    ax, fig = gicmapsobj.plot_branch_gicflows(figfile, title, dpi, markersize)
figfile -> File name to save plot. File type could be any allowed by matplotlib (like png, pdf, ps, eps, svg)
title   -> Plot title, default='GIC flows in Transmission Lines'
dpi     -> Resolution in dots per inch of saved figure, default=300
Returns:
ax      -> the Axes instance
fig     -> the Figure instance
"""
        if self.ierr:
            return (None, None)
        else:
            self.distance_min = self.pygicobj.distance_min
            self.distance_max = self.pygicobj.distance_max
            self.distance_threshold = _DISTANCE_THRESHOLD_FACTOR * self.distance_max
            if self.distance_min < self.distance_threshold:
                self.distance_threshold = self.distance_min
            ax, fig = self._plot_main_brngic(title, figfile, dpi)
            return (
             ax, fig)

    def plot_qtotal_barchart(self, figfile=None, width=0.35, barcolors=['red', 'blue'], dpi=300, title=''):
        """Plot Total Reactive power losses bar chart.
    ax, fig = gicmapsobj.plot_qtotal_barchart(figfile, width, barcolors, dpi, title)
figfile   -> File name to save plot. File type could be any allowed by matplotlib (like png, pdf, ps, eps, svg)
width     -> Width of a bar
barcolors -> Two item list of bar colors, used to paint alternate bars
dpi       -> Resolution in dots per inch of saved figure, default=300
title     -> Plot title, default='Total Transformer Reactive Power Losses'
Returns:
ax      -> the Axes instance
fig     -> the Figure instance
"""
        if self.ierr:
            return (None, None)
        else:
            qtotal_all_dict = self.pygicobj.qtotal_all
            deg_list = self.pygicobj.qtotal_all.keys()
            deg_list.sort()
            qtt_list = []
            for eachdeg in deg_list:
                qtt_list.append(self.pygicobj.qtotal_all[eachdeg])

            if not qtt_list:
                return (None, None)
            x1, x2, y1, y2 = ([], [], [], [])
            for n in range(len(deg_list)):
                if not n % 2:
                    x1.append(n + 1)
                    y1.append(qtt_list[n])
                else:
                    x2.append(n + 1)
                    y2.append(qtt_list[n])

            x = [i + 1 for i in range(len(deg_list))]
            n_xticks = min(7, len(deg_list))
            step_xticks = int(len(deg_list)) / n_xticks
            xticks = []
            xlbls = []
            for n, each in enumerate(deg_list):
                if not n % step_xticks:
                    xticks.append(x[n] + width / 2.0)
                    xlbls.append(str(each))

            self._fignum += 1
            fig = plt.figure(num=self._fignum)
            ax = fig.add_subplot(111)
            ax.bar(x1, y1, width, color=barcolors[0], linewidth=0)
            ax.bar(x2, y2, width, color=barcolors[1], linewidth=0)
            nxs = int(len(x) / n_xticks)
            ax.set_xlim(right=x[-1] + 1)
            ax.set_xticks(xticks)
            ax.set_xticklabels(xlbls)
            self._decorate_and_save_qtotal(ax, fig, figfile, dpi, title)
            return (
             ax, fig)

    def plot_qtotal(self, figfile=None, color='black', linestyle='None', linewidth=1, marker='D', markersize=5, markeredgecolor='black', markeredgewidth=1, fillstyle='none', dpi=300, title=''):
        """Plot Total Reactive power losses as line plot.
    ax, fig = gicmapsobj.plot_qtotal(figfile, color, linestyle, linewidth, marker, markersize,
                    markeredgecolor, markeredgewidth, fillstyle, dpi, title)
figfile         -> File name to save plot. File type could be any allowed by matplotlib
                   (like png, pdf, ps, eps, svg)
color           -> Any valid matplotlib color name or valid HTML hex string, default='blue'
linestyle       -> Any valid matplotlib linestyle, e.g., 'solid', 'dashed', 'dash_dot', 'dotted', 'None';
                   default='None'
linewidth       -> Linewidth in points, default= 1
marker          -> Any valid matplotlib marker, e.g., 'D', 'o', 's', default='D'
markersize      -> Markersize in points, default= 5
markeredgecolor -> Markeredgecolor, any valid matplotlib color name or valid HTML hex string, default='blue'
markeredgewidth -> Markeredgewidth in points, default= 1
fillstyle       -> Any valid matplotlib marker fill style, e.g., 'full', 'left, 'right, 'bottom, 'top, 'none',
                   default='none'
dpi             -> Resolution in dots per inch of saved figure, default=300
title           -> Plot title, default='Total Transformer Reactive Power Losses'
Returns:
ax      -> the Axes instance
fig     -> the Figure instance
"""
        if self.ierr:
            return (None, None)
        else:
            qtotal_all_dict = self.pygicobj.qtotal_all
            deg_list = self.pygicobj.qtotal_all.keys()
            deg_list.sort()
            qtt_list = []
            for eachdeg in deg_list:
                qtt_list.append(self.pygicobj.qtotal_all[eachdeg])

            if not qtt_list:
                return (None, None)
            self._fignum += 1
            fig = plt.figure(num=self._fignum)
            ax = fig.add_subplot(111)
            ax.plot(deg_list, qtt_list, color=color, linestyle=linestyle, linewidth=linewidth, marker=marker, markersize=markersize, markeredgecolor=markeredgecolor, markeredgewidth=markeredgewidth, fillstyle=fillstyle)
            self._decorate_and_save_qtotal(ax, fig, figfile, dpi, title)
            return (
             ax, fig)


class FAULT_SUMMARY():

    def __init__(self, activity, sid, busall, **kwds):
        """Run Short Circuit Calculations with specified 'activity' and get total fault current results in Python objects.

Create Python object as below and apply various methods defined here.

fltobj = pssarrays.FAULT_SUMMARY(activity, sid, busall,
                                 flt3ph=0,  fltlg=0, fltllg=0,  fltll=0,   linout=0, linend=0, linopn=0,
                                 voltop=0, genxop=0, tpunty=0,  dcload=0,  zcorec=1, lnchrg=0, shntop=0,
                                 loadop=0, machpq=0, volts=1.0, nbrlnks=10,
                                 rprtyp=-1, rprlvl=0)
Pre-requisite:
    PSSE must have working case in memory, and subsystem must be defined before calling this.

Where:
activity : PSSE Short Circuit activity to run, allowed 'ASCC'
sid      : Valid subsystem identifier
           Range from 0 to 11, must have been previously defined
busall   : Consider "all" buses or selected subsystem
           = 1, process all buses
           = 0, process only buses in subsystem SID
flt3ph   : Get 3 phase fault currents
           = 1, apply 3 phase faults
           = 0, do not apply 3 phase faults (default)
fltlg    : Get LG (line to ground) fault currents
           = 1, apply LG faults
           = 0, do not apply LG faults (default)
fltllg   : Get LLG (two lines to ground) fault currents
           = 1, apply LLG faults
           = 0, do not apply LLG faults (default)
fltll    : Get LL (line to line) fault currents
           = 1, apply LL faults
           = 0, do not apply LL faults (default)
linout   : Consider LINE OUT faults
           = 1, apply LINOUT faults
           = 0, do not apply LINOUT faults (default)
linend   : Consider LINE END faults
           = 1, apply LINEND faults
           = 0, do not apply LINEND faults (default)
linopn   : Consider LINE ONE END OPEN faults (applied on non-transfromer branches only)
           = 1, apply LINOPN faults
           = 0, do not apply LINOPN faults (default)
voltop   : Bus Voltage option
           = 0, use bus voltages from power flow solution (default)
           = 1, set all bus voltages at specified value and at 0 deg
           = 2, set faulted bus voltage at specified value and at 0 deg
genxop   : Synchronous Machine Reactance selection option
           = 0, subtransient (default)
           = 1, transient
           = 2, synchronous
tpunty   : Transformer Tap Ratios and Phase Shift Angles option
           = 0, leave tap ratios and phase shift angles unchanged (default)
           = 1, set tap ratios to 1.0 pu and phase shift angles to 0 deg.
           = 2, set tap ratios to 1.0 pu and phase shift angles unchanged.
           = 3, set tap ratios unchanged and phase shift angles to 0 deg.
dcload   : DC Lines and FACTS Devices option
           = 0, block (default)
           = 1, represent as load
zcorec   : Transformer zero sequence impedance correction option
           = 0, ignore
           = 1, apply (default)
lnchrg   : Line Charging option
           = 0, leave unchanged (default)
           = 1, set to 0.0 in the positive and negative sequences
           = 2, set to 0.0 in all sequences
shntop   : Line shunts, Fixed shunts, Switched shunts and
           Transformer Magnetizing Admittance option
           = 0, leave unchanged (default)
           = 1, set to 0.0 in the positive and negative sequences
           = 2, set to 0.0 in all sequences
loadop   : Load option
           = 0, leave unchanged (default)
           = 1, set to 0.0 in the positive and negative sequences
           = 2, set to 0.0 in all sequences
machpq   : Synchronous and Asynchronous machines power output option
           = 0, use real and reactive power outputs from power flow solution  (default)
           = 1, set real and reactive power outputs to 0.0
volts    : User specified bus voltage value in pu. (default = 1.0 pu)
           This is used only when voltop = 1 or 2.
nbrlnks  : Maximum possible number of links (branches) at a bus, default=10
           Since LINOUT/LINEND/LINOPN total fault currents are saved for each branch in subsystem,
           this provides just enough temporary stoarage space. You may never need to change this.
rprtyp   : Report option
           =-1, no report (default)
           = 0, fault current summary table
           = 1, total fault currents with Thevenin impedance
           = 2, fault contributions to "N" levels away
           = 3, total fault currents and fault contributions to "N" levels away
rprlvl   : Number of levels back for contributions report (>=0) (0 by default)
           Used when rprtyp = 2 or 3

The Short Circuit calculations results are stored as Python objects. Following shows how to access them.
For network cases having series compensated branches with Metal Oxide Varistors (MOVs) enabled,
calculation results are accessed differently as shown below.

fltobj.ierr  -> =0 for no error, else error occurred

fltobj.mov   -> =0 No MOVs in the case
                >0 Number of MOVs in the case

Bus Faults
fbus is fauted bus number.
fltobj.busfault[fbus].ph3   -> three phase (3PH) fault current (ia1)
fltobj.busfault[fbus].lg    -> line to ground (LG) fault current (3*ia0)
fltobj.busfault[fbus].llg   -> line line to ground (LLG) fault current (3*ia0)
fltobj.busfault[fbus].ll    -> line to line (LL) fault current (ib)
    Network case without MOVs
fltobj.busfault[fbus].z0    -> Zero sequence Thevenin Impedance
fltobj.busfault[fbus].z1    -> Positive sequence Thevenin Impedance
fltobj.busfault[fbus].z2    -> Negative sequence Thevenin Impedance
    Network case with MOVs
fltobj.busfault[fbus].z1ph3 -> Positive sequence Thevenin Impedance
fltobj.busfault[fbus].z0lg  -> Zero sequence Thevenin Impedance
fltobj.busfault[fbus].z1lg  -> Positive sequence Thevenin Impedance
fltobj.busfault[fbus].z2lg  -> Negative sequence Thevenin Impedance
fltobj.busfault[fbus].z0llg -> Zero sequence Thevenin Impedance
fltobj.busfault[fbus].z1llg -> Positive sequence Thevenin Impedance
fltobj.busfault[fbus].z2llg -> Negative sequence Thevenin Impedance
fltobj.busfault[fbus].z0ll  -> Zero sequence Thevenin Impedance
fltobj.busfault[fbus].z1ll  -> Positive sequence Thevenin Impedance
fltobj.busfault[fbus].z2ll  -> Negative sequence Thevenin Impedance

Line OUT Faults - non transformer branches
fbus is fauted bus number and brn is tuple (bus1, bus2, ckt) of branch.
fltobj.linoutfault_brn[fbus][brn].ph3    -> three phase (3PH) fault current (ia1)
fltobj.linoutfault_brn[fbus][brn].lg     -> line to ground (LG) fault current (3*ia0)
fltobj.linoutfault_brn[fbus][brn].llg    -> line line to ground (LLG) fault current (3*ia0)
fltobj.linoutfault_brn[fbus][brn].ll     -> line to line (LL) fault current (ib)
    Network case without MOVs
fltobj.linoutfault_brn[fbus][brn].z0     -> Zero sequence Thevenin Impedance
fltobj.linoutfault_brn[fbus][brn].z1     -> Positive sequence Thevenin Impedance
fltobj.linoutfault_brn[fbus][brn].z2     -> Negative sequence Thevenin Impedance
    Network case with MOVs
fltobj.linoutfault_brn[fbus][brn].z1ph3  -> Positive sequence Thevenin Impedance
fltobj.linoutfault_brn[fbus][brn].z0lg   -> Zero sequence Thevenin Impedance
fltobj.linoutfault_brn[fbus][brn].z1lg   -> Positive sequence Thevenin Impedance
fltobj.linoutfault_brn[fbus][brn].z2lg   -> Negative sequence Thevenin Impedance
fltobj.linoutfault_brn[fbus][brn].z0llg  -> Zero sequence Thevenin Impedance
fltobj.linoutfault_brn[fbus][brn].z1llg  -> Positive sequence Thevenin Impedance
fltobj.linoutfault_brn[fbus][brn].z2llg  -> Negative sequence Thevenin Impedance
fltobj.linoutfault_brn[fbus][brn].z0ll   -> Zero sequence Thevenin Impedance
fltobj.linoutfault_brn[fbus][brn].z1ll   -> Positive sequence Thevenin Impedance
fltobj.linoutfault_brn[fbus][brn].z2ll   -> Negative sequence Thevenin Impedance

Line OUT Faults - two winding transformer branches
fbus is fauted bus number and brn is tuple (bus1, bus2, ckt) of transformer branch.
fltobj.linoutfault_2wdg[fbus][brn].ph3    -> three phase (3PH) fault current (ia1)
fltobj.linoutfault_2wdg[fbus][brn].lg     -> line to ground (LG) fault current (3*ia0)
fltobj.linoutfault_2wdg[fbus][brn].llg    -> line line to ground (LLG) fault current (3*ia0)
fltobj.linoutfault_2wdg[fbus][brn].ll     -> line to line (LL) fault current (ib)
    Network case without MOVs
fltobj.linoutfault_2wdg[fbus][brn].z0     -> Zero sequence Thevenin Impedance
fltobj.linoutfault_2wdg[fbus][brn].z1     -> Positive sequence Thevenin Impedance
fltobj.linoutfault_2wdg[fbus][brn].z2     -> Negative sequence Thevenin Impedance
    Network case with MOVs
fltobj.linoutfault_2wdg[fbus][brn].z1ph3  -> Positive sequence Thevenin Impedance
fltobj.linoutfault_2wdg[fbus][brn].z0lg   -> Zero sequence Thevenin Impedance
fltobj.linoutfault_2wdg[fbus][brn].z1lg   -> Positive sequence Thevenin Impedance
fltobj.linoutfault_2wdg[fbus][brn].z2lg   -> Negative sequence Thevenin Impedance
fltobj.linoutfault_2wdg[fbus][brn].z0llg  -> Zero sequence Thevenin Impedance
fltobj.linoutfault_2wdg[fbus][brn].z1llg  -> Positive sequence Thevenin Impedance
fltobj.linoutfault_2wdg[fbus][brn].z2llg  -> Negative sequence Thevenin Impedance
fltobj.linoutfault_2wdg[fbus][brn].z0ll   -> Zero sequence Thevenin Impedance
fltobj.linoutfault_2wdg[fbus][brn].z1ll   -> Positive sequence Thevenin Impedance
fltobj.linoutfault_2wdg[fbus][brn].z2ll   -> Negative sequence Thevenin Impedance

Line OUT Faults - three winding transformer branches
fbus is fauted bus number and brn is tuple (bus1, bus2, bus3, ckt) of transformer branch.
fltobj.linoutfault_3wdg[fbus][brn].ph3    -> three phase (3PH) fault current (ia1)
fltobj.linoutfault_3wdg[fbus][brn].lg     -> line to ground (LG) fault current (3*ia0)
fltobj.linoutfault_3wdg[fbus][brn].llg    -> line line to ground (LLG) fault current (3*ia0)
fltobj.linoutfault_3wdg[fbus][brn].ll     -> line to line (LL) fault current (ib)
    Network case without MOVs
fltobj.linoutfault_3wdg[fbus][brn].z0     -> Zero sequence Thevenin Impedance
fltobj.linoutfault_3wdg[fbus][brn].z1     -> Positive sequence Thevenin Impedance
fltobj.linoutfault_3wdg[fbus][brn].z2     -> Negative sequence Thevenin Impedance
    Network case with MOVs
fltobj.linoutfault_3wdg[fbus][brn].z1ph3  -> Positive sequence Thevenin Impedance
fltobj.linoutfault_3wdg[fbus][brn].z0lg   -> Zero sequence Thevenin Impedance
fltobj.linoutfault_3wdg[fbus][brn].z1lg   -> Positive sequence Thevenin Impedance
fltobj.linoutfault_3wdg[fbus][brn].z2lg   -> Negative sequence Thevenin Impedance
fltobj.linoutfault_3wdg[fbus][brn].z0llg  -> Zero sequence Thevenin Impedance
fltobj.linoutfault_3wdg[fbus][brn].z1llg  -> Positive sequence Thevenin Impedance
fltobj.linoutfault_3wdg[fbus][brn].z2llg  -> Negative sequence Thevenin Impedance
fltobj.linoutfault_3wdg[fbus][brn].z0ll   -> Zero sequence Thevenin Impedance
fltobj.linoutfault_3wdg[fbus][brn].z1ll   -> Positive sequence Thevenin Impedance
fltobj.linoutfault_3wdg[fbus][brn].z2ll   -> Negative sequence Thevenin Impedance

Line END Faults - non transformer branches
fbus is fauted bus number and brn is tuple (bus1, bus2, ckt) of branch.
fltobj.linendfault_brn[fbus][brn].ph3    -> three phase (3PH) fault current (ia1)
fltobj.linendfault_brn[fbus][brn].lg     -> line to ground (LG) fault current (3*ia0)
fltobj.linendfault_brn[fbus][brn].llg    -> line line to ground (LLG) fault current (3*ia0)
fltobj.linendfault_brn[fbus][brn].ll     -> line to line (LL) fault current (ib)
    Network case without MOVs
fltobj.linendfault_brn[fbus][brn].z0     -> Zero sequence Thevenin Impedance
fltobj.linendfault_brn[fbus][brn].z1     -> Positive sequence Thevenin Impedance
fltobj.linendfault_brn[fbus][brn].z2     -> Negative sequence Thevenin Impedance
    Network case with MOVs
fltobj.linendfault_brn[fbus][brn].z1ph3  -> Positive sequence Thevenin Impedance
fltobj.linendfault_brn[fbus][brn].z0lg   -> Zero sequence Thevenin Impedance
fltobj.linendfault_brn[fbus][brn].z1lg   -> Positive sequence Thevenin Impedance
fltobj.linendfault_brn[fbus][brn].z2lg   -> Negative sequence Thevenin Impedance
fltobj.linendfault_brn[fbus][brn].z0llg  -> Zero sequence Thevenin Impedance
fltobj.linendfault_brn[fbus][brn].z1llg  -> Positive sequence Thevenin Impedance
fltobj.linendfault_brn[fbus][brn].z2llg  -> Negative sequence Thevenin Impedance
fltobj.linendfault_brn[fbus][brn].z0ll   -> Zero sequence Thevenin Impedance
fltobj.linendfault_brn[fbus][brn].z1ll   -> Positive sequence Thevenin Impedance
fltobj.linendfault_brn[fbus][brn].z2ll   -> Negative sequence Thevenin Impedance

Line END Faults - two winding transformer branches
fbus is fauted bus number and brn is tuple (bus1, bus2, ckt) of transformer branch.
fltobj.linendfault_2wdg[fbus][brn].ph3    -> three phase (3PH) fault current (ia1)
fltobj.linendfault_2wdg[fbus][brn].lg     -> line to ground (LG) fault current (3*ia0)
fltobj.linendfault_2wdg[fbus][brn].llg    -> line line to ground (LLG) fault current (3*ia0)
fltobj.linendfault_2wdg[fbus][brn].ll     -> line to line (LL) fault current (ib)
    Network case without MOVs
fltobj.linendfault_2wdg[fbus][brn].z0     -> Zero sequence Thevenin Impedance
fltobj.linendfault_2wdg[fbus][brn].z1     -> Positive sequence Thevenin Impedance
fltobj.linendfault_2wdg[fbus][brn].z2     -> Negative sequence Thevenin Impedance
    Network case with MOVs
fltobj.linendfault_2wdg[fbus][brn].z1ph3  -> Positive sequence Thevenin Impedance
fltobj.linendfault_2wdg[fbus][brn].z0lg   -> Zero sequence Thevenin Impedance
fltobj.linendfault_2wdg[fbus][brn].z1lg   -> Positive sequence Thevenin Impedance
fltobj.linendfault_2wdg[fbus][brn].z2lg   -> Negative sequence Thevenin Impedance
fltobj.linendfault_2wdg[fbus][brn].z0llg  -> Zero sequence Thevenin Impedance
fltobj.linendfault_2wdg[fbus][brn].z1llg  -> Positive sequence Thevenin Impedance
fltobj.linendfault_2wdg[fbus][brn].z2llg  -> Negative sequence Thevenin Impedance
fltobj.linendfault_2wdg[fbus][brn].z0ll   -> Zero sequence Thevenin Impedance
fltobj.linendfault_2wdg[fbus][brn].z1ll   -> Positive sequence Thevenin Impedance
fltobj.linendfault_2wdg[fbus][brn].z2ll   -> Negative sequence Thevenin Impedance

Line END Faults - three winding transformer branches
fbus is fauted bus number and endbus_brn is tuple (endbus, bus1, bus2, bus3, ckt) of transformer branch.
Two line end faults are calculted for each transformer bus. For example, WDG1 bus is faulted bus,
then line end faults are applied at 1) dummy bus at WDG2 and 2)dummy bus at WDG3.
So endbus in above tuple is either WDG2 bus or WDG3 bus.
fltobj.linendfault_3wdg[fbus][endbus_brn].ph3    -> three phase (3PH) fault current (ia1)
fltobj.linendfault_3wdg[fbus][endbus_brn].lg     -> line to ground (LG) fault current (3*ia0)
fltobj.linendfault_3wdg[fbus][endbus_brn].llg    -> line line to ground (LLG) fault current (3*ia0)
fltobj.linendfault_3wdg[fbus][endbus_brn].ll     -> line to line (LL) fault current (ib)
    Network case without MOVs
fltobj.linendfault_3wdg[fbus][endbus_brn].z0     -> Zero sequence Thevenin Impedance
fltobj.linendfault_3wdg[fbus][endbus_brn].z1     -> Positive sequence Thevenin Impedance
fltobj.linendfault_3wdg[fbus][endbus_brn].z2     -> Negative sequence Thevenin Impedance
    Network case with MOVs
fltobj.linendfault_3wdg[fbus][endbus_brn].z1ph3  -> Positive sequence Thevenin Impedance
fltobj.linendfault_3wdg[fbus][endbus_brn].z0lg   -> Zero sequence Thevenin Impedance
fltobj.linendfault_3wdg[fbus][endbus_brn].z1lg   -> Positive sequence Thevenin Impedance
fltobj.linendfault_3wdg[fbus][endbus_brn].z2lg   -> Negative sequence Thevenin Impedance
fltobj.linendfault_3wdg[fbus][endbus_brn].z0llg  -> Zero sequence Thevenin Impedance
fltobj.linendfault_3wdg[fbus][endbus_brn].z1llg  -> Positive sequence Thevenin Impedance
fltobj.linendfault_3wdg[fbus][endbus_brn].z2llg  -> Negative sequence Thevenin Impedance
fltobj.linendfault_3wdg[fbus][endbus_brn].z0ll   -> Zero sequence Thevenin Impedance
fltobj.linendfault_3wdg[fbus][endbus_brn].z1ll   -> Positive sequence Thevenin Impedance
fltobj.linendfault_3wdg[fbus][endbus_brn].z2ll   -> Negative sequence Thevenin Impedance

Line one end OPEN Faults - non transformer branches
fbus is fauted bus number and brn is tuple (bus1, bus2, ckt) of branch.
fltobj.linopnfault_brn[fbus][brn].ph3    -> three phase (3PH) fault current (ia1)
fltobj.linopnfault_brn[fbus][brn].lg     -> line to ground (LG) fault current (3*ia0)
fltobj.linopnfault_brn[fbus][brn].llg    -> line line to ground (LLG) fault current (3*ia0)
fltobj.linopnfault_brn[fbus][brn].ll     -> line to line (LL) fault current (ib)
    Network case without MOVs
fltobj.linopnfault_brn[fbus][brn].z0     -> Zero sequence Thevenin Impedance
fltobj.linopnfault_brn[fbus][brn].z1     -> Positive sequence Thevenin Impedance
fltobj.linopnfault_brn[fbus][brn].z2     -> Negative sequence Thevenin Impedance
    Network case with MOVs
fltobj.linopnfault_brn[fbus][brn].z1ph3  -> Positive sequence Thevenin Impedance
fltobj.linopnfault_brn[fbus][brn].z0lg   -> Zero sequence Thevenin Impedance
fltobj.linopnfault_brn[fbus][brn].z1lg   -> Positive sequence Thevenin Impedance
fltobj.linopnfault_brn[fbus][brn].z2lg   -> Negative sequence Thevenin Impedance
fltobj.linopnfault_brn[fbus][brn].z0llg  -> Zero sequence Thevenin Impedance
fltobj.linopnfault_brn[fbus][brn].z1llg  -> Positive sequence Thevenin Impedance
fltobj.linopnfault_brn[fbus][brn].z2llg  -> Negative sequence Thevenin Impedance
fltobj.linopnfault_brn[fbus][brn].z0ll   -> Zero sequence Thevenin Impedance
fltobj.linopnfault_brn[fbus][brn].z1ll   -> Positive sequence Thevenin Impedance
fltobj.linopnfault_brn[fbus][brn].z2ll   -> Negative sequence Thevenin Impedance

Note 1:
The unit of fault currents (pu or kA) and Thevenin impedance (pu or ohms) is determmined
by PSSE option setting "short_circuit_units (scunit)". When scunit=1 (physical), currents
are in kA and impedances are in ohms.

The format (rectangular or polar) of fault currents and Thevenin impedance is determmined
by PSSE option setting "short_circuit_coordinates".

Note 2:
Any of these Python objects can be accessed with case insensitive attributes or as dictionary keys.
So following examples for accessing busfault object are allowed.
    fltobj.busfault[fbus].ph3  or  fltobj.busfault[fbus].pH3  or  fltobj.busfault[fbus]['pH3']
    fltobj.busfault[fbus].lg   or  fltobj.busfault[fbus].LL   or  fltobj.busfault[fbus]['LL']
    fltobj.busfault[fbus].llg  or  fltobj.busfault[fbus].lLg  or  fltobj.busfault[fbus]['Llg']
    fltobj.busfault[fbus].ll   or  fltobj.busfault[fbus].lL   or  fltobj.busfault[fbus]['LL']

"""
        self.ierr = True
        self.activity = activity
        self.sid = sid
        self.all = busall
        ierr, self.nfbus, self.ncasebus, self.ncasebrn, self.ncasetrn, self.ncasetrn3 = pssaccss.ascc_size_summary(self.sid, self.all)
        kwdslower = {}
        for k, v in kwds.items():
            klow = k.lower()
            kwdslower[klow] = v

        _allowed_kwds_dict = {'flt3ph': 0, 
           'fltlg': 0, 'fltllg': 0, 'fltll': 0, 'linout': 0, 'linend': 0, 'voltop': 0, 
           'genxop': 0, 'tpunty': 0, 'dcload': 0, 'zcorec': 1, 'lnchrg': 0, 'shntop': 0, 
           'loadop': 0, 'machpq': 0, 'volts': 1.0, 'nbrlnks': 10, 'linopn': 0, 'rprtyp': (-1), 
           'rprlvl': 0}
        self._optns = {}
        for key, val in _allowed_kwds_dict.items():
            if key in kwdslower:
                setattr(self, key, kwdslower[key])
                self._optns[key] = kwdslower[key]
            else:
                setattr(self, key, val)
                self._optns[key] = val

        del kwdslower
        if self.fltlg or self.fltllg or self.fltll:
            self.fltuns = True
        else:
            self.fltuns = False
        ierr_jnk, scfrmt = psspy.short_circuit_coordinates()
        if scfrmt == 1:
            self.scfrmt = 'polar'
        else:
            self.scfrmt = 'rectangular'
        ierr_jnk, scunit = psspy.short_circuit_units()
        if scunit == 1:
            self.scunit = 'kA'
        else:
            self.scunit = 'pu'
        self._rdct = pssaccss.ascc_currents_summary(self.sid, self.all, self.flt3ph, self.fltlg, self.fltllg, self.fltll, self.linout, self.linend, self.voltop, self.genxop, self.tpunty, self.dcload, self.zcorec, self.lnchrg, self.shntop, self.loadop, self.machpq, self.volts, self.nfbus, self.nbrlnks, self.linopn, self.rprtyp, self.rprlvl)
        self.ierr = self._rdct['ierr']
        self.mov = self._rdct['mov']
        _ftyp = []
        if self.flt3ph:
            _ftyp.append('ph3')
        if self.fltlg:
            _ftyp.append('lg')
        if self.fltllg:
            _ftyp.append('llg')
        if self.fltll:
            _ftyp.append('ll')
        self._ftyp_calculated = tuple(_ftyp)
        _outendopn = []
        if self.linout:
            _outendopn.append('linout')
        if self.linend:
            _outendopn.append('linend')
        if self.linopn:
            _outendopn.append('linopn')
        self._outendopn_calculated = tuple(_outendopn)
        self.busfault = collections.OrderedDict()
        if self.mov == 0:
            for i in range(len(self._rdct['faulted_bus'])):
                fbus = self._rdct['faulted_bus'][i]
                tmpdict = self._collect_fault_currents('bus', i)
                self.busfault[fbus] = _Dict_caseless_bunch(tmpdict)

        else:
            tmp_outdict = collections.OrderedDict()
            for ftyp in self._ftyp_calculated:
                for i in range(len(self._rdct['faulted_bus'])):
                    fbus = self._rdct['faulted_bus'][i]
                    tmpdict = self._collect_fault_currents('bus', i, ftyp_mov=ftyp)
                    if fbus not in tmp_outdict:
                        tmp_outdict[fbus] = collections.OrderedDict()
                    for k, v in tmpdict.items():
                        tmp_outdict[fbus][k] = v

            for fbus, vdict in tmp_outdict.items():
                if fbus not in self.busfault:
                    self.busfault[fbus] = collections.OrderedDict()
                self.busfault[fbus] = _Dict_caseless_bunch(vdict)

        for outendopn in ['linout', 'linend', 'linopn']:
            for brntyp in ['brn', '2wdg', '3wdg']:
                if outendopn == 'linopn' and brntyp == '2wdg':
                    break
                which = outendopn + '_' + brntyp
                ki = 'bus' + '_' + which
                kc = 'ckt' + '_' + which
                dnam = 'self.' + outendopn + 'fault' + '_' + brntyp
                exec dnam + '= collections.OrderedDict()'
                if outendopn not in self._outendopn_calculated:
                    continue
                if self.mov == 0:
                    if self._rdct[ki]:
                        out_fltbus = self._rdct[ki][0]
                        for i in range(len(out_fltbus)):
                            fbus = out_fltbus[i]
                            if brntyp in ['brn', '2wdg']:
                                brn = [
                                 self._rdct[ki][1][i], self._rdct[ki][2][i], self._rdct[kc][i]]
                            elif outendopn == 'linout':
                                brn = [
                                 self._rdct[ki][1][i], self._rdct[ki][2][i], self._rdct[ki][3][i], self._rdct[kc][i]]
                            else:
                                brn = [
                                 self._rdct[ki][1][i], self._rdct[ki][2][i], self._rdct[ki][3][i], self._rdct[ki][4][i], self._rdct[kc][i]]
                            brn = self._brn_id_with_ascend_buses(brn)
                            tmpdict = self._collect_fault_currents(which, i)
                            if fbus not in eval(dnam):
                                exec dnam + '[fbus] = collections.OrderedDict()'
                            exec dnam + '[fbus][brn] = _Dict_caseless_bunch(tmpdict)'

                else:
                    tmp_outdict = collections.OrderedDict()
                    for ftyp in self._ftyp_calculated:
                        kii = ki + '_' + ftyp
                        kcc = kc + '_' + ftyp
                        if self._rdct[kii]:
                            out_fltbus = self._rdct[kii][0]
                            for i in range(len(out_fltbus)):
                                fbus = out_fltbus[i]
                                if brntyp in ['brn', '2wdg']:
                                    brn = [
                                     self._rdct[kii][1][i], self._rdct[kii][2][i], self._rdct[kcc][i]]
                                elif outendopn == 'linout':
                                    brn = [
                                     self._rdct[kii][1][i], self._rdct[kii][2][i], self._rdct[kii][3][i], self._rdct[kcc][i]]
                                else:
                                    brn = [
                                     self._rdct[kii][1][i], self._rdct[kii][2][i], self._rdct[kii][3][i], self._rdct[kii][4][i], self._rdct[kcc][i]]
                                brn = self._brn_id_with_ascend_buses(brn)
                                tmpdict = self._collect_fault_currents(which, i, ftyp_mov=ftyp)
                                if fbus not in tmp_outdict:
                                    tmp_outdict[fbus] = collections.OrderedDict()
                                if brn not in tmp_outdict[fbus]:
                                    tmp_outdict[fbus][brn] = collections.OrderedDict()
                                for k, v in tmpdict.items():
                                    tmp_outdict[fbus][brn][k] = v

                    for fbus, vdict in tmp_outdict.items():
                        if fbus not in eval(dnam):
                            exec dnam + '[fbus] = collections.OrderedDict()'
                        for brn, tmpdict in vdict.items():
                            exec dnam + '[fbus][brn] = _Dict_caseless_bunch(tmpdict)'

                    del tmp_outdict

    def _collect_fault_currents(self, which, idx, ftyp_mov=None):
        tmpdict = {}
        if not ftyp_mov:
            for k in self._ftyp_calculated:
                kif = 'i' + k + '_' + which
                crnt = self._rdct[kif][0][idx]
                tmpdict[k] = self._convert_current_value(crnt)

            kz = 'thevz_' + which
            tmpdict['z1'] = self._rdct[kz][0][idx]
            tmpdict['z2'] = self._rdct[kz][1][idx]
            tmpdict['z0'] = self._rdct[kz][2][idx]
        else:
            kif = 'i' + ftyp_mov + '_' + which
            crnt = self._rdct[kif][0][idx]
            tmpdict[ftyp_mov] = self._convert_current_value(crnt)
            kz = 'thevz_' + which + '_' + ftyp_mov
            kz1 = 'z1' + ftyp_mov
            kz2 = 'z2' + ftyp_mov
            kz0 = 'z0' + ftyp_mov
            tmpdict[kz1] = self._rdct[kz][0][idx]
            tmpdict[kz2] = self._rdct[kz][1][idx]
            tmpdict[kz0] = self._rdct[kz][2][idx]
        return tmpdict

    def _convert_current_value(self, crnt):
        if self.scunit == 'pu':
            retv = crnt
        elif self.scfrmt == 'polar':
            ir = crnt.real / 1000.0
            iang = crnt.imag
            retv = complex(ir, iang)
        else:
            retv = crnt / 1000.0
        return retv

    def _brn_id_with_ascend_buses(self, brn):
        ckt = brn.pop(-1)
        if len(brn) == 4:
            endbus = brn.pop(0)
        else:
            endbus = None
        brn.sort()
        brn.append(ckt)
        if endbus:
            brn.insert(0, endbus)
        return tuple(brn)

    def _get_options_used_desc(self):
        _options_desc = collections.OrderedDict([
         (
          'voltop',
          {0: 'SET PRE-FAULT VOLTAGES AND PHASE SHIFT ANGLES TO POWER FLOW SOLUTION', 
             1: (('SET PRE-FAULT VOLTAGE ON ALL BUSES TO {0:g} PU AT 0 PHASE SHIFT ANGLE').format(self._optns['volts'])), 
             2: (('SET PRE-FAULT VOLTAGE ON FAULTED BUS TO {0:g} PU AT 0 PHASE SHIFT ANGLE').format(self._optns['volts']))}),
         (
          'machpq',
          {0: 'SET SYNCHRONOUS/ASYNCHRONOUS MACHINE POWER OUTPUTS TO POWER FLOW SOLUTION', 
             1: 'SET SYNCHRONOUS/ASYNCHRONOUS MACHINE POWER OUTPUTS TO P=0.0, Q=0.0'}),
         (
          'genxop',
          {0: 'SET GENERATOR POSITIVE SEQUENCE REACTANCES TO SUBTRANSIENT', 
             1: 'SET GENERATOR POSITIVE SEQUENCE REACTANCES TO TRANSIENT', 
             2: 'SET GENERATOR POSITIVE SEQUENCE REACTANCES TO SYNCHRONOUS'}),
         (
          'tpunty',
          {0: 'TRANSFORMER TAP RATIOS AND PHASE SHIFT ANGLES UNCHANGED', 
             1: 'SET TRANSFORMER TAP RATIOS=1.0 PU AND PHASE SHIFT ANGLES=0.0', 
             2: 'SET TRANSFORMER TAP RATIOS=1.0 PU AND PHASE SHIFT ANGLES UNCHANGED', 
             3: 'TRANSFORMER TAP RATIOS UNCHANGED AND SET PHASE SHIFT ANGLES=0.0'}),
         (
          'lnchrg',
          {0: 'LINE CHARGING REPRESENTED IN +/-/0 SEQUENCES', 
             1: 'SET LINE CHARGING=0.0 IN +/- SEQUENCES', 
             2: 'SET LINE CHARGING=0.0 IN +/-/0 SEQUENCES'}),
         (
          'shntop',
          {0: 'LINE/FIXED/SWITCHED SHUNTS AND TRANSFORMER MAGNETIZING ADMITTANCE REPRESENTED IN +/-/0 SEQUENCES', 
             1: 'SET LINE/FIXED/SWITCHED SHUNTS=0.0 AND TRANSFORMER MAGNETIZING ADMITTANCE=0.0 IN +/- SEQUENCES', 
             2: 'SET LINE/FIXED/SWITCHED SHUNTS=0.0 AND TRANSFORMER MAGNETIZING ADMITTANCE=0.0 IN +/-/0 SEQUENCES'}),
         (
          'loadop',
          {0: 'LOAD REPRESENTED IN +/-/0 SEQUENCES', 
             1: 'SET LOAD=0.0 IN +/- SEQUENCES', 
             2: 'SET LOAD=0.0 IN +/-/0 SEQUENCES'}),
         (
          'dcload',
          {0: 'DC LINES AND FACTS DEVICES BLOCKED', 
             1: 'DC LINES AND FACTS DEVICES REPRESENTED AS LOAD'}),
         (
          'zcorec',
          {0: 'IMPEDANCE CORRECTIONS NOT APPLIED TO TRANSFORMER ZERO SEQUENCE IMPEDANCES', 
             1: 'IMPEDANCE CORRECTIONS APPLIED TO TRANSFORMER ZERO SEQUENCE IMPEDANCES'})])
        optns_desc = '\n OPTIONS USED:\n'
        for k, vdict in _options_desc.items():
            op = self._optns[k]
            optns_desc += ('     - {0:s} ({1:s}={2:d})\n').format(vdict[op], k, op)

        if self.mov > 0:
            optns_desc += ('     - Number of series compensated branches with MOV enabled = {0:d}\n').format(self.mov)
        return optns_desc

    def text_report(self, rptfile=''):
        """Text report of Short Circuit Calculations.
rptfile -> Output file name (.txt), default PSSE report window
"""
        if self.ierr:
            return
        if self.scfrmt == 'polar':
            frmt_str = '(magnitude and angle of'
        else:
            frmt_str = '(real and imaginary values of'
        if self.scunit == 'kA':
            unit_str = ' currents in kA and Thevenin impedance in ohms)'
        else:
            unit_str = ' currents in pu and Thevenin impedance in pu)'
        frmt_unit_str = frmt_str + unit_str
        if rptfile:
            pn, x = os.path.splitext(rptfile)
            if not x:
                rptfile = pn + '.txt'
            rptfobj = open(rptfile, 'w')
            self.report = rptfobj.write
        else:
            self.report = psspy.report
            psspy.beginreport()
        dattim = _get_date_time_str()
        prdnam = _get_product_name()
        hdr = (' {0:s} {1:s} SHORT CIRCUIT CURRENTS      {2:s}').format(prdnam, self.activity, dattim)
        self.report(hdr + '\n')
        savfnam, snpfnam = psspy.sfiles()
        self.report(('\n {0:s}\n').format(savfnam))
        line1, line2 = psspy.titldt()
        self.report(' ' + line1 + '\n')
        self.report(' ' + line2 + '\n')
        optns_desc = self._get_options_used_desc()
        self.report(optns_desc)
        self._fault_header(('\n Bus Faults {0:s}\n FLTBUS').format(frmt_unit_str))
        for bus, vdict in self.busfault.items():
            txt = (' {0:6d} ').format(bus)
            self._fault_values(txt, vdict)

        _name_brn = {'brn': 'Non transformer branches', '2wdg': 'Two winding transformer branches', 
           '3wdg': 'Three winding transformer branches'}
        for outendopn in ['linout', 'linend', 'linopn']:
            for brntyp in ['brn', '2wdg', '3wdg']:
                if outendopn == 'linopn' and brntyp == '2wdg':
                    break
                dnam = 'self.' + outendopn + 'fault' + '_' + brntyp
                if not eval(dnam):
                    continue
                if brntyp in ('brn', '2wdg'):
                    hdr = ('\n {0:s} Faults - {1:s} {2:s}\n FLTBUS |----Branch----|').format(outendopn.upper(), _name_brn[brntyp], frmt_unit_str)
                elif outendopn in ('linout', 'linopn'):
                    hdr = ('\n {0:s} Faults - {1:s} {2:s}\n FLTBUS |--------Branch-------|').format(outendopn.upper(), _name_brn[brntyp], frmt_unit_str)
                else:
                    tstr = '    First bus in branch identifier is the bus where LINEND fault is applied'
                    hdr = ('\n {0:s} Faults - {1:s} {2:s}\n {3:s}\n FLTBUS |-----------Branch-----------|').format(outendopn.upper(), _name_brn[brntyp], frmt_unit_str, tstr)
                self._fault_header(hdr)
                fst_time = True
                dnam_items = dnam + '.items()'
                for bus, vdict1 in eval(dnam_items):
                    if fst_time:
                        fst_time = False
                    else:
                        self.report('\n')
                    if brntyp in ('brn', '2wdg'):
                        for brn, vdict in vdict1.items():
                            txt = (' {0:6d} {1:6d} {2:6d} {3:2s} ').format(bus, brn[0], brn[1], brn[2])
                            self._fault_values(txt, vdict)

                    elif outendopn in ('linout', 'linopn'):
                        for brn, vdict in vdict1.items():
                            txt = (' {0:6d} {1:6d} {2:6d} {3:6d} {4:2s} ').format(bus, brn[0], brn[1], brn[2], brn[3])
                            self._fault_values(txt, vdict)

                    else:
                        for brn, vdict in vdict1.items():
                            txt = (' {0:6d} {1:6d} {2:6d} {3:6d} {4:6d} {5:2s} ').format(bus, brn[0], brn[1], brn[2], brn[3], brn[4])
                            self._fault_values(txt, vdict)

        if rptfile:
            rptfobj.close()

    def _fault_header(self, txt):
        if self.mov == 0:
            if self.flt3ph:
                txt += ' |------Three Phase--------|'
            if self.fltlg:
                txt += ' |----Line to Ground-------|'
            if self.fltllg:
                txt += ' |---LineLine to Grd-------|'
            if self.fltll:
                txt += ' |-----Line to Line--------|'
        else:
            txt += ' Fault |-----Fault Current-------|'
        txt += ' |----Positive Thev Z------|'
        if self.fltuns:
            txt += ' |----Negative Thev Z------|'
            txt += ' |------Zero Thev Z--------|'
        txt += '\n'
        self.report(txt)

    def _fault_values(self, txt, vdct):
        if self.mov == 0:
            if self.flt3ph:
                txt += self._format_complex_value(vdct['ph3'])
            if self.fltlg:
                txt += self._format_complex_value(vdct['lg'])
            if self.fltllg:
                txt += self._format_complex_value(vdct['llg'])
            if self.fltll:
                txt += self._format_complex_value(vdct['ll'])
            txt += self._format_complex_value(vdct['z1'])
            if self.fltuns:
                txt += self._format_complex_value(vdct['z2'])
                txt += self._format_complex_value(vdct['z0'])
            txt += '\n'
        else:
            tx0 = txt
            ltx0 = len(tx0)
            txt = ''
            if self.flt3ph:
                txt += tx0 + '  3PH ' + self._format_complex_value(vdct['ph3'])
                txt += self._format_complex_value(vdct['z1ph3'])
                txt += '\n'
                tx0 = ' ' * ltx0
            if self.fltlg:
                txt += tx0 + '   LG ' + self._format_complex_value(vdct['lg'])
                txt += self._format_complex_value(vdct['z1lg'])
                txt += self._format_complex_value(vdct['z2lg'])
                txt += self._format_complex_value(vdct['z0lg'])
                txt += '\n'
                tx0 = ' ' * ltx0
            if self.fltllg:
                txt += tx0 + '  LLG ' + self._format_complex_value(vdct['llg'])
                txt += self._format_complex_value(vdct['z1llg'])
                txt += self._format_complex_value(vdct['z2llg'])
                txt += self._format_complex_value(vdct['z0llg'])
                txt += '\n'
                tx0 = ' ' * ltx0
            if self.fltll:
                txt += tx0 + '   LL ' + self._format_complex_value(vdct['ll'])
                txt += self._format_complex_value(vdct['z1ll'])
                txt += self._format_complex_value(vdct['z2ll'])
                txt += self._format_complex_value(vdct['z0ll'])
                txt += '\n'
        self.report(txt)

    def _format_complex_value(self, val):
        r = self._format_to_length(val.real)
        x = self._format_to_length(val.imag)
        rx = ('{0:>12s} {1:>12s} | ').format(r, x)
        return rx

    def _format_to_length(self, val):
        vstr = ('{0:g}').format(val)
        return vstr


class DFAX_PP():
    """Distribution factors output file (.dfx) post processing
"""

    def __init__(self, dfxfile):
        """dfxobj = pssarrays.DFAX_PP(dfxfile)
        Create 'dfxobj' for Distribution factors output file (.dfx) post-processing.
    Inputs:
        dfxfile = PSSE Distribution factors (DFAX) output file (.dfx), no default allowed.
    Returns:
        dfxobj.ierr = error code (0=no error)
    Pre-requisite:
        PSSE must have working case in memory.
"""
        self._sz_ierr = _IERR_YES
        if not os.path.exists(dfxfile):
            msg = '\n File does not exist: %s\n' % dfxfile
            print msg
            return
        self._dfxfnam_s = dfxfile
        ierr, self._nmlinexx, self._ninterxx, self._ncasexx, self._ncase_otdfxx = pssaccss.dfax_size(self._dfxfnam_s)
        self._sz_ierr = ierr
        if ierr:
            errtxt = ' Error processing file, ignored:\n'
            errtxt += '    DFAX size error=%d, for file: %s\n' % (ierr, dfxfile)
            _ShowError(_INPUTERROR, errtxt)
            return

    def summary(self):
        """smryobj = dfxobj.summary()
        Summary information from DFAX output file (.dfx).
    Returns:
        Summary information dictionaty object 'smryobj', which is accessed by its keys or attributes as below.
        smryobj.ierr             = error code (0=no error)
        smryobj.size.nmline      = number of monitored branches
        smryobj.size.ninter      = number of monitored interfaces
        smryobj.size.ncase       = number of contingencies + 1 (for base case)
        smryobj.casetitle.line1  = short title line 1
        smryobj.casetitle.line2  = short title line 2
        smryobj.file.sav         = saved case (.sav) file name
        smryobj.file.dfx         = distribution factor data (.dfx) file name
        smryobj.file.sub         = subsystem definition data (.sub) file name
        smryobj.file.mon         = monitored element data (.mon) file name
        smryobj.file.con         = contingency description data (.con) file name
        smryobj.melement         = monitored branch and interface names, [] of nmline+ninter items
        smryobj.colabel          = contingency labels, [] of ncase items
        smryobj.codesc           = contingency description,
                                   [] of ncase items with each item is [] of contingency events
        """
        self._smry_ierr = _IERR_YES
        if self._sz_ierr:
            return None
        else:
            rlst_smry = pssaccss.dfax_summary(self._dfxfnam_s, self._nmlinexx, self._ninterxx, self._ncasexx)
            if rlst_smry[0]:
                errtxt = ' Error processing file, ignored:\n'
                errtxt += '    DFAX Summary error=%d, for file: %s\n' % (rlst_smry[0], self._dfxfnam_s)
                _ShowError(_INPUTERROR, errtxt)
                return None
            self._smry_ierr = _IERR_NO
            smryobj = _Dict_caseless_bunch({_ERR_CODE_NAM: _IERR_NO})
            _tmpdict = _list_name_values_to_dict(_DFAX_SIZE_NAM[1], [self._nmlinexx, self._ninterxx, self._ncasexx])
            smryobj[_DFAX_SIZE_NAM[0]] = _Dict_caseless_bunch(_tmpdict)
            _tmpdict = _list_name_values_to_dict(_DFAX_SUMMARY_NAM, rlst_smry[1:])
            for each in _DFAX_SUMMARY_NAM:
                if type(each) in [tuple, list]:
                    k = each[0]
                    k1 = each[1]
                    _tdct1 = _list_name_values_to_dict(k1, _tmpdict[k])
                    smryobj[k] = _Dict_caseless_bunch(_tdct1)
                elif each == 'codesc':
                    codesc = []
                    for dsc in _tmpdict[each]:
                        codesc.append(_remove_extra_spaces(dsc))

                    smryobj[each] = codesc
                else:
                    smryobj[each] = _tmpdict[each]

            del rlst_smry
            del _tmpdict
            return smryobj

    def otdf_factors(self):
        """otdfobj = dfxobj.otdf_factors()
        DFAX file summary information and OTDF factors from DFAX file (.dfx).
    Returns:
        OTDF factors dictionaty object 'otdfobj', which is accessed by its keys or attributes as below.
        otdfobj.ierr             = error code (0=no error)
        otdfobj.size.nmline      = number of monitored branches
        otdfobj.size.ninter      = number of monitored interfaces
        otdfobj.size.ncase       = number of allowed contingencies in OTDF factors
                                   (Note: Multi-event contingencies are not allowed in OTDF factors.)
        otdfobj.casetitle.line1  = short title line 1
        otdfobj.casetitle.line2  = short title line 2
        otdfobj.file.sav         = saved case (.sav) file name
        otdfobj.file.dfx         = distribution factor data (.dfx) file name
        otdfobj.file.sub         = subsystem definition data (.sub) file name
        otdfobj.file.mon         = monitored element data (.mon) file name
        otdfobj.file.con         = contingency description data (.con) file name
        otdfobj.melement         = monitored branch and interface names, [] of nmline+ninter items
        otdfobj.colabel          = contingency labels, [] of ncase items
        otdfobj.codesc           = contingency description, [] of ncase items
        otdfobj.factor           = monitored branch MVA and interface MW flow,
                                   [] of ncase items with each item is [] of nmline+ninter items
        """
        self._otdf_ierr = _IERR_YES
        if self._sz_ierr:
            return None
        else:
            rlst_smry = pssaccss.otdf_factors(self._dfxfnam_s, self._nmlinexx, self._ninterxx, self._ncase_otdfxx)
            if rlst_smry[0]:
                errtxt = ' Error processing file, ignored:\n'
                errtxt += '    OTDF FACTORS error=%d, for file: %s\n' % (rlst_smry[0], self._dfxfnam_s)
                _ShowError(_INPUTERROR, errtxt)
                return None
            self._otdf_ierr = _IERR_NO
            otdfobj = _Dict_caseless_bunch({_ERR_CODE_NAM: _IERR_NO})
            _tmpdict = _list_name_values_to_dict(_DFAX_SIZE_NAM[1], [self._nmlinexx, self._ninterxx, self._ncase_otdfxx])
            otdfobj[_DFAX_SIZE_NAM[0]] = _Dict_caseless_bunch(_tmpdict)
            _tmpdict = _list_name_values_to_dict(_OTDF_FACTORS_NAM, rlst_smry[1:])
            for each in _OTDF_FACTORS_NAM:
                if type(each) in [tuple, list]:
                    k = each[0]
                    k1 = each[1]
                    _tdct1 = _list_name_values_to_dict(k1, _tmpdict[k])
                    otdfobj[k] = _Dict_caseless_bunch(_tdct1)
                elif each == 'codesc':
                    codesc = []
                    for dsc in _tmpdict[each]:
                        codesc.append(_remove_extra_spaces(dsc))

                    otdfobj[each] = codesc
                else:
                    otdfobj[each] = _tmpdict[each]

            del rlst_smry
            del _tmpdict
            return otdfobj

    def summary_report(self, rptfile=None):
        """ierr = dfxobj.summary_report(rptfile=None)
        Create DFAX summary information report.
    Inputs:
        rptfile  = report output text file name
                   default "PSSE Report" when run from PSSE or
                           Python shell when run from Python Interpreter
    Returns:
        ierr = error code ((0=no error)
        """
        ierr = self._sz_ierr
        if ierr:
            return ierr
        else:
            smryobj = self.summary()
            if smryobj == None:
                return _IERR_YES
            if smryobj.ierr != 0:
                return smryobj.ierr
            rptfile, rptfile_h, report = _get_report_object(rptfile)
            ttl_hline = '*' + 46 * ' *' + '\n\n'
            ttl = 30 * ' ' + 'DFAX Summary Report' + '\n'
            ttl_file = 30 * ' ' + smryobj.file.dfx + '\n'
            ttl_time = 30 * ' ' + time.ctime() + '\n\n'
            report(ttl_hline)
            report(ttl)
            report(ttl_file)
            report(ttl_time)
            report(ttl_hline)
            report('%s\n' % smryobj.casetitle.line1)
            report('%s\n' % smryobj.casetitle.line2)
            report('\n')
            report('Saved Case file              = %s\n' % smryobj.file.sav)
            report('DFAX file                    = %s\n' % smryobj.file.dfx)
            report('Subsystem file               = %s\n' % smryobj.file.sub)
            report('Monitored Element file       = %s\n' % smryobj.file.mon)
            report('Contingency Description file = %s\n' % smryobj.file.con)
            report('\n')
            report('*** Contingency Description ***\n')
            lblen = [len(each) for each in smryobj.colabel]
            mxlblen = max(lblen)
            for i in range(smryobj.size.ncase):
                lbl = ('{0:{align}{width}}').format(smryobj.colabel[i], align='<', width=mxlblen)
                lblspc = ' ' * mxlblen
                for j, dsc in enumerate(smryobj.codesc[i]):
                    if j == 0:
                        report('  %s  %s\n' % (lbl, dsc))
                    else:
                        report('  %s  %s\n' % (lblspc, dsc))

            msg = _report_done_message_str(rptfile, rptfile_h, rptdesc='DFAX Summary')
            if msg:
                _show_message(msg)
            return smryobj.ierr

    def otdf_factors_report(self, rptfile=None):
        """ierr = dfxobj.otdf_factors_report(rptfile=None)
        Create DFAX file summary information and OTDF factors report.
    Inputs:
        rptfile  = report output text file name
                   default "PSSE Report" when run from PSSE or
                           Python shell when run from Python Interpreter
    Returns:
        ierr = error code ((0=no error)
        """
        ierr = self._sz_ierr
        if ierr:
            return ierr
        else:
            otdfobj = self.otdf_factors()
            if otdfobj == None:
                return _IERR_YES
            if otdfobj.ierr != 0:
                return otdfobj.ierr
            rptfile, rptfile_h, report = _get_report_object(rptfile)
            ttl_hline = '*' + 46 * ' *' + '\n\n'
            ttl = 30 * ' ' + 'OTDF Factors Report' + '\n'
            ttl_file = 30 * ' ' + otdfobj.file.dfx + '\n'
            ttl_time = 30 * ' ' + time.ctime() + '\n\n'
            report(ttl_hline)
            report(ttl)
            report(ttl_file)
            report(ttl_time)
            report(ttl_hline)
            report('%s\n' % otdfobj.casetitle.line1)
            report('%s\n' % otdfobj.casetitle.line2)
            report('\n')
            report('Saved Case file              = %s\n' % otdfobj.file.sav)
            report('DFAX file                    = %s\n' % otdfobj.file.dfx)
            report('Subsystem file               = %s\n' % otdfobj.file.sub)
            report('Monitored Element file       = %s\n' % otdfobj.file.mon)
            report('Contingency Description file = %s\n' % otdfobj.file.con)
            report('\n')
            report('*** OTDF Contingency Description ***\n')
            lblen = [len(each) for each in otdfobj.colabel]
            mxlblen = max(lblen)
            for i in range(otdfobj.size.ncase):
                lbl = ('{0:{align}{width}}').format(otdfobj.colabel[i], align='<', width=mxlblen)
                desc = otdfobj.codesc[i]
                report('  %s  %s\n' % (lbl, desc))

            report('\n')
            report('*** OTDF Factors ***\n')
            report('  <---------- Monitored Branch/Interface ------------->  ')
            for each in otdfobj.colabel:
                report('%12s  ' % each.strip())

            report('\n')
            for i in range(otdfobj.size.nmline + otdfobj.size.ninter):
                report('  %52s  ' % otdfobj.melement[i].strip())
                for j in range(otdfobj.size.ncase):
                    report('%12.6f  ' % otdfobj.factor[j][i])

                report('\n')

            msg = _report_done_message_str(rptfile, rptfile_h, rptdesc='OTDF Factors')
            if msg:
                _show_message(msg)
            return otdfobj.ierr


if __name__ == '__main__':
    try:
        import pssarrays
        help(pssarrays)
    except:
        print '\n        Python Module to retrieve PSS(R)E Solution Results in Python Lists.\n        Returned Python Lists are accessed as attributes of a list object.\n        The attribute name is the name of the List.\n        Refer help(pssarrays) for details.\n        '

# okay decompiling pssarrays.pyc
