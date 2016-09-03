import os
import json
import yaml

import boto.rds
from fabric.api import local, task

VAULT_PASSWD_FILE = os.path.join(os.environ['HOME'], '.ansible_vault_passwd')
VERBOSE_LEVEL = int(os.environ.get('ANSIBLE_VERBOSE_LEVEL', 0))

with open('vars/aws.yml') as f:
    aws_vars = yaml.load(f)

def ansible_playbook(playbook, inventory, tags=None, limit=None, extra_vars=None, var_file=None, require_vault=False):
    command = 'ansible-playbook'
    args = [
        '-i {}'.format(inventory),
    ]

    if VERBOSE_LEVEL:
        args.append('-' + 'v' * VERBOSE_LEVEL)

    if limit:
        args.append('--limit {}'.format(limit))

    if require_vault:
        if os.path.exists(VAULT_PASSWD_FILE):
            args.append('--vault-password-file={}'.format(VAULT_PASSWD_FILE))
        else:
            args.append('--ask-vault-pass')

    if extra_vars:
        args.append("--extra-vars='{}'".format(json.dumps(extra_vars)))

    if var_file:
        args.append("--extra-vars='@{}'".format(var_file))

    if tags:
        args.append('--tags={}'.format(tags))

    command = 'ansible-playbook {args} {playbook}'.format(
            args = ' '.join(args),
            playbook = playbook
    )
    return local(command)

def _bool(val):
    if isinstance(val, basestring) and val.lower() in ['no', 'false']:
        val = False
    return bool(val)

@task
def provision(limit=None, tags=None, dev=False, **extra_vars):
    '''Provision instances, including installing libraries and softwares and configure them properly

    Args:
        limit: limit provision to specific hosts (comma-separated)
        tags: only execute tasks matching specific tags (comma-separated)
        extra_vars: passed in as extra_vars
    '''
    ansible_playbook('provision-pre.yml', 'inventory/perf-dev.yml' if dev else 'inventory/perf.yml',
                        tags=tags, limit=limit, extra_vars=extra_vars)
    ansible_playbook('provision.yml', 'inventory/perf-dev.yml' if dev else 'inventory/perf.yml',
                        tags=tags, limit=limit, extra_vars=extra_vars)

@task
def aws_setup(tags=None, rds=True):
    '''Setup infrastructure on AWS including secruity group, ec2 instances etc.

    Args:
        tags: only execute tasks matching specific tags (comma-separated)
        rds: whether changing rds from db.t2.micro to specific instance class
    '''
    ansible_playbook('aws_setup.yml', 'localhost,',tags=tags)
    if _bool(rds):
        rds_conn = boto.rds.connect_to_region(aws_vars['region'])
        for rds in aws_vars['rds_instances']:
            print 'RDS: {} upgraded to {}'.format(rds['name'], rds['instance_class'])
            rds_conn.modify_dbinstance(rds['name'],
                                    instance_class=rds['instance_class'],
                                    apply_immediately=True)

@task
def aws_teardown(tags=None):
    '''Teardown resources on AWS

    Args:
        tags: only execute tasks matching specific tags (comma-separated)
    '''
    ansible_playbook('aws_teardown.yml', 'localhost,',tags=tags)
    domain = '.glow-dev.com'
    local('grep {} inventory/*.yml | xargs -n1 ssh-keygen -R '
          .format(domain))
    rds_conn = boto.rds.connect_to_region(aws_vars['region'])
    for rds in aws_vars['rds_instances']:
        print 'RDS: {} degraded to db.t2.micro'.format(rds['name'])
        rds_conn.modify_dbinstance(rds['name'],
                                   instance_class='db.t2.micro',
                                   apply_immediately=True)
