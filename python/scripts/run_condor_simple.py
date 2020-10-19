#!/usr/bin/env python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--batchname'   , default = ''      , type = str, help = 'name to display')
parser.add_argument('--script'      , required = True   , type = str, help = 'name of the script to launch')
parser.add_argument('--veto'        , default = ''      , type = str, help = 'list of vetoed machines (separated by a comma)')
time_group = parser.add_mutually_exclusive_group()
time_group.add_argument('--runtime' , default = 3000    , type = int, help = 'runtime in minutes')
time_group.add_argument('--flavour' , default = ''      , type = str, help = 'job flavour')
args = parser.parse_args()

import os
import htcondor

schedd = htcondor.Schedd()
submit = htcondor.Submit()

submit['Universe']          = 'Vanilla'
submit['Executable']        = args.script
submit['use_x509userproxy'] = 'true'
submit['Log']               = 'condor_job.log'
submit['Output']            = 'condor_job.out'
submit['Error']             = 'condor_job.err'
submit['getenv']            = 'true'
submit['environment']       = "LS_SUBCWD={}".format(os.environ['PWD'])
submit['request_memory']    = 2000

if not args.veto is '':
    submit['+Requirements'] = ' && '.join(['(machine != "{}")'.format(mac.strip(' ')) for mac in args.veto.split(',')])

if not args.flavour is '': 
    submit['+JobFlavour'] = args.flavour
else:
    submit['+MaxRuntime'] = str(args.runtime*60)

if not args.batchname is '':
    submit['JobBatchName'] = args.batchname

with schedd.transaction() as txn:
  submit.queue(txn)
