#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
from AGBio.UtilityWrappers2 import *

BLAST_BIN_DIR = '/usr/local/ncbi/blast/bin/'


class BlastBaseWrapper(BaseUtilityWrapper, HasOutFile):
    """Base class for the NCBI blast tools.
    """
    def __init__(self, utilitypath='', outfile=None):
        '''
        '''
        BaseUtilityWrapper.__init__(self, utilitypath)
        HasOutFile.__init__(self, '-out ', outfile)


class BaseCmdWrapper(BlastBaseWrapper):
    '''
    '''
    def __init__(self, utilitypath=None, entry=None,info=False,
                 db='nr', target_only=True, outfile=None):
        '''
        '''
        BlastBaseWrapper.__init__(self, utilitypath, outfile)
        ## if entry:
        ##     self['entry'] = ['', ','.join(entry)]
        ## if info:
        ##     self['info'] = ['', '']
        ## if db:
        ##     self['db'] = ['', db]
        ## if target_only:
        ##     self['target_only'] = ['', '']
            
    @prop
    def entry():
        def fget(self):
            return self['entry']
        return locals()

    def setentry(self, opt, value):
        if value:
            self['entry'] = [opt, ','.join(value)]
        elif 'entry' in self.keys():
            del self['entry']
        self.updateCline()
        
    @prop
    def info():
        def fget(self):
            return self['info']
        return locals()
   
    def setinfo(self, opt, value):
        if value:
            self['info'] = [opt, '']
        elif 'info' in self.keys():
            del self['info']
        self.updateCline()
        
    @prop
    def db():
        def fget(self):
            return self['db']
        return locals()
    
    def setdb(self, opt, value):
        if value:
            self['db'] = [opt, value]
        elif 'db' in self.keys():
            del self['db']
        self.updateCline()

    @prop
    def target_only():
        def fget(self):
            return self['target_only']
        return locals()
   
    def settarget_only(self, opt, value):
        if value:
            self['target_only'] = [opt, '']
        elif 'target_only' in self.keys():
            del self['target_only']
        self.updateCline()

        
class FastaCmdWrapper(BaseCmdWrapper, HasOutFile):
    '''fastacmd wrapper.
    '''
    def __init__(self, entry=None, info=False, db='nr', target_only=True,
                 outfile=None):
        '''
        '''
        BaseCmdWrapper.__init__(self, 'fastacmd', entry, info, db, target_only,
                                outfile)
        HasOutFile.__init__(self, '-o ', outfile)
        if entry:
            self.entry = entry
        if info:
            self.info = ' '
        if db:
            self.db = db
        if target_only:
            self.target_only = ' '
        self.updateCline()

    @prop
    def entry():
        def fget(self):
            return self['entry']
        def fset(self, value):
            BaseCmdWrapper.setentry(self, '-s ', value)
            self.updateCline()
        return locals()

    @prop
    def info():
        def fget(self):
            return self['info']
        def fset(self, value):
            BaseCmdWrapper.setinfo(self, '-I ', value)
            self.updateCline()
        return locals()

    @prop
    def db():
        def fget(self):
            return self['db']
        def fset(self, value):
            BaseCmdWrapper.setdb(self, '-d ', value)
            self.updateCline()
        return locals()

    @prop
    def target_only():
        def fget(self):
            return self['target_only']
        def fset(self, value):
            BaseCmdWrapper.settarget_only(self, '-t ', value)
            self.updateCline()
        return locals()


class BlastDbCmdWrapper(BlastBaseWrapper):
    '''blastdbcmd wrapper.
    '''
    def __init__(self, entry=None, info=False, db='nr', target_only=True,
                 outfile=None, version='plus'):
        '''
        '''
        BlastBaseWrapper.__init__(self, BLAST_BIN_DIR + 'blastdbcmd', outfile)
        if entry:
            self['entry'] = ['-entry ', ','.join(entry)]
        if info:
            self['info'] = ['-info', '']
        if db:
            self['db'] = ['-db ', db]
        if target_only:
            self['target_only'] = ['-target_only', '']
        if version == 'legacy':
            self._changeCmdOptLegacy()
        self.updateCline()

    @prop
    def entry():
        def fget(self):
            return self['entry']
        def fset(self, value):
            BaseCmdWrapper.settarget_only(self, '-entry ', value)
            self.updateCline()
        return locals()
        
    @prop
    def info():
        def fget(self):
            return self['info']
        def fset(self, value):
            BaseCmdWrapper.settarget_only(self, '-info ', value)
            self.updateCline()
        return locals()
        
    @prop
    def db():
        def fget(self):
            return self['db']
        def fset(self, value):
            BaseCmdWrapper.settarget_only(self, '-db ', value)
            self.updateCline()
        return locals()

    @prop
    def target_only():
        def fget(self):
            return self['target_only']
        def fset(self, value):
            BaseCmdWrapper.settarget_only(self, '-target_only ', value)
            self.updateCline()
        return locals()


class BlastAllWrapper(BaseUtilityWrapper, HasInFile, HasOutFile):
    def __init__(self, infile, outfile, exe='blastall', flavour='blastp',
                 db='nr', format='xml', lcomplexfilt=False, gis=False,
                 ncore=1, evalue=10):
        BaseUtilityWrapper.__init__(self, exe)
        HasInFile.__init__(self, '-i ', infile)
        HasOutFile.__init__(self, '-o ', outfile)
        self.exe = exe
        self.flavour = flavour
        self.db = db
        self.format = format
        self.lcomplexfilt = lcomplexfilt
        self.gis = gis
        self.ncore = ncore
        self.evalue = evalue

    @prop
    def flavour():
        def fget(self):
            return self['flavour']
        def fset(self, value):
            if value not in ('blastp', 'blastn', 'tblastn'):
                raise 'Unknown flavour.'
            self['flavour'] = ['-p ', value]
            self.updateCline()
        return locals()

    @prop
    def db():
        def fget(self):
            return self['db']
        def fset(self, value):
            self['db'] = ['-d ', value]
            self.updateCline()
        return locals()

    @prop
    def format():
        def fget(self):
            return self['format']
        def fset(self, value):
            dd = {'plain_text':'0',
                  'xml':'7'}
            self['format'] = ['-m ', dd[value]]
            self.updateCline()
        return locals()

    @prop
    def lcomplexfilt():
        def fget(self):
            return self['lcomplexfilt']
        def fset(self, value):
            if value: vv = 'T'
            else: vv = 'F'
            self['lcomplexfilt'] = ['-F ', vv]
            self.updateCline()
        return locals()

    @prop
    def gis():
        def fget(self):
            return self['gis']
        def fset(self, value):
            if value:
                self['gis'] = ['-I', '']
            elif 'gis' in self.keys():
                del self['gis']
            self.updateCline()
        return locals()

    @prop
    def ncore():
        def fget(self):
            return self['ncore']
        def fset(self, value):
            self['ncore'] = ['-a ', str(value)]
            self.updateCline()
        return locals()
    
    @prop
    def evalue():
        def fget(self):
            return self['evalue']
        def fset(self, value):
            self['evalue'] = ['-e ', str(value)]
            self.updateCline()
        return locals()
