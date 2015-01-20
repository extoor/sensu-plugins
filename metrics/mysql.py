#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shlex
from socket import gethostname
from time import time
from subprocess import Popen, PIPE


def run(cmd):
    env = {'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'}

    proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE, env=env)

    return proc.communicate()


def main(prefix=None, host=None, user=None, password=None):
    timestamp = int(time())
    tpl = '{prefix}.mysql.status.{key} {value} {timestamp}'
    cmd = 'mysql --protocol=SOCKET --batch --execute="SHOW STATUS"'

    stdout, stderr = run(cmd)

    for line in stdout.splitlines()[1:]:
        key, value = line.split()
        print(tpl.format(prefix=prefix,
                         key=key,
                         value=value,
                         timestamp=timestamp))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--scheme', default=gethostname(), help='Metric naming scheme (default: %(default)s)')
    args = parser.parse_args()
    main(prefix=args.scheme)
