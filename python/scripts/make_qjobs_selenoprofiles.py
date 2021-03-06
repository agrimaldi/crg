#!/usr/bin/env python2.6

import sys
import os
import random
import time
import socket
import optparse
from AGBio.Utilities import *

SELENOPROFILES = 'python /users/rg/mmariotti/Scripts/selenoprofiles.py'

def main():

    parser = optparse.OptionParser()

    parser.add_option( '-g', '--genomes_folder',
                       dest='genomesfolder',
                       help='path to the genome folder.',
                       metavar='DIR' )

    parser.add_option( '-G', '--genomes_list',
                       dest='genomeslist',
                       help='file containing the names of the genomes.',
                       metavar='FILE' )

    parser.add_option( '-p', '--profiles_folder',
                       dest='profilesfolder',
                       help='folder containing the profiles.',
                       metavar='DIR' )

    parser.add_option( '-P', '--profiles_list',
                       dest='profileslist',
                       help='file containing the names of the profiles.',
                       metavar='FILE' )

    parser.add_option( '-d', '--output_folder',
                       dest='outputfolder',
                       help='root folder for the output.',
                       metavar='DIR' )

    parser.add_option( '-t', '--temp_folder',
                       dest='tempfolder',
                       help='folder to use for temporary files storage.',
                       metavar='DIR' )

    parser.add_option( '-n', '--job_base_name',
                       dest='jobbasename',
                       help='base name of the qsub jobs. the name of each genome is appended.',
                       metavar='NAME' )

    parser.add_option( '-q', '--q_param',
                       dest='qparam',
                       help='`q` parametter of the cluster. supposedly the quantity of ram for each job.',
                       metavar='NAME' )

    parser.add_option( '-M', '--jobs_folder',
                       dest='jobsfolder',
                       help='folder in which all the `jobs scripts` are to be stored.',
                       metavar='DIR' )

    parser.add_option( '-S', '--selenoprofiles_path',
                       dest='sppath',
                       help='path to selenoprofiles.',
                       metavar='FILE' )

    parser.add_option( '-r', '--args',
                       dest='sp_args',
                       help='additional args (coma separated) to pass to\
                       selenoprofiles. For instance, steps to perform go there.\
                       Default : -S',
                       metavar='OPTS')
    
    
    parser.set_defaults( outputfolder = '_'.join([str(t) for t in time.localtime(time.time())[:3]]),
                         tempfolder = os.path.abspath('/tmp'),
                         jobbasename = 'SP_',
                         qparam = 'mem_4',
                         jobsfolder = os.getcwd(),
                         sppath = '/users/rg/mmariotti/Scripts/selenoprofiles.py',
                         sp_args = 'S',
                         profileslist = None,
                         profilesfolder = None)

    (options, args) = parser.parse_args()

    opt_profileslist = ''
    opt_profilesfolder = ''
    if options.profileslist:
        opt_profileslist = ' '.join(['-i',
                                     os.path.abspath(options.profileslist)])
    if options.profilesfolder:
        opt_profilesfolder = ' '.join(['-profiles',
                                       os.path.abspath(options.profilesfolder)])

    if not os.path.isdir(options.outputfolder):
        os.makedirs(options.outputfolder)
        
    logs_dir = os.path.abspath(os.path.join(os.path.split(options.outputfolder)[0], 'logs'))
    if not os.path.isdir(logs_dir):
        os.makedirs(logs_dir)

    if not os.path.isdir(options.jobsfolder):
        os.makedirs(options.jobsfolder)

    with open(options.genomeslist, 'r') as gl:
        genomeslist = [g.strip() for g in gl.readlines()]

    for genome in genomeslist:
        tmpfold = genTempfilename(options.tempfolder)
        jobfilename = os.path.join(options.jobsfolder,
                                   options.jobbasename \
                                   + genome + '.sh')

        with open(jobfilename, 'w') as tjf:
            tjf.write('#!/bin/bash\n')
            tjf.write('#$ -e ' + os.path.join(logs_dir, genome + '.err.log') + '\n')
            tjf.write('#$ -o ' + os.path.join(logs_dir, genome + '.out.log') + '\n')
            tjf.write('#$ -q ' + options.qparam + '\n')
            tjf.write('#$ -N ' + options.jobbasename + genome + '\n')
            tjf.write('. /etc/profile\n')
            tjf.write('PATH=$PATH:/users/rg/agrimaldi/usr/bin:/users/rg/agrimaldi/Code/python/python/scripts:/users/rg/mmariotti/bin\n')
            tjf.write('echo "host : $HOSTNAME"\n')
            tjf.write('mkdir ' + tmpfold + '\n')
            tjf.write(' '.join(( 'python', options.sppath,
                                 os.path.abspath(options.outputfolder),
                                 ' '.join(['-'+o for o in options.sp_args.split(',')]),
                                 '-genomes_folder', os.path.abspath(options.genomesfolder),
                                 '-genome', genome,
                                 opt_profilesfolder, opt_profileslist,
                                 '-temp', tmpfold,
                                 '>>', os.path.join(logs_dir, genome + '.out.log'),
                                 '2>>', os.path.join(logs_dir, genome + '.err.log'),
                                 '\n')))
            tjf.write('rm -r ' + tmpfold + '\n')

if __name__ == '__main__':

    main()
