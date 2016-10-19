#!/usr/bin/env python
import logging
import optparse
import re
import sys


usage = 'usage: %prog filename [options]'
version = '%prog 0.1'
log_format_default = '%(asctime)s ' + logging.BASIC_FORMAT
log_level_names = logging._levelNames
log_level_default = log_level_names[logging.CRITICAL]


log_level_map = {
    'SYS' : logging.critical,
    'ERR' : logging.error,
    'WARN' : logging.warning,
    'INFO' : logging.info,
    'DET' : logging.debug,
    }


log_pat = (r'(?P<lang>\w+)\s+(?P<time>.*?)\s+(?P<servermsg>.*?\:\s+)'
            '\[(?P<clientid>.*?)\:(?P<clientver>.*?)\:(?P<serverver>.*?)'
            '\:(?P<clienttype>.*?)\:(?P<request>.*?)\:(?P<response>.*?)'
            '\:(?P<version>.*?)\:(?P<loglevel>.*?)\]\s+(?P<msg>.*)')


def log_filter(fd):
    log_re = re.compile(log_pat)
    for line in fd:
        match = re.match(log_re, line)
        if match:
            yield match.groupdict()


def get_options(argv):
    parser = optparse.OptionParser(usage=usage, version=version)
    parser.add_option('-f', '--format', dest='logformat',
                      help='output log format [default: %default]',
                      default=log_format_default)
    parser.add_option('-m', '--msgformat', dest='msgformat',
                      help='output message format [default %default]',
                      default='client:%(clientid)s req:%(request)s res:%(response)s msg:%(msg)s')
    parser.add_option('-l', '--level', dest='loglevel',
                      help='output log level [default: %default]',
                      default=log_level_default)
    return (parser, ) + parser.parse_args()


class IbLogFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        try:
            return record.__dict__['args']['time']
        except (KeyError, ):
            return logging.Formatter.formatTime(self, record)


def main(args=None):
    parser, opts, args = get_options(args if args is not None else sys.argv)
    if not args:
        parser.print_usage()
        return

    fn = args[0]
    fh = sys.stdin if fn == '-' else open(fn)

    def badlevel():
        print >> sys.stderr, 'Unknown log level %s' % opts.loglevel

    try:
        opts.loglevel = log_level_names[int(opts.loglevel)]
    except (ValueError, ):
        pass
    except (KeyError, ):
        badlevel()
        return

    try:
        level = log_level_names[opts.loglevel]
    except (KeyError, ):
        badlevel()
        return

    logging.basicConfig(level=level)
    logging.root.handlers[0].setFormatter(IbLogFormatter(fmt=opts.logformat))

    for data in log_filter(fh):
        call = log_level_map.get(data.get('loglevel', None), None)
        if call:
            call(opts.msgformat, data)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, ):
        pass



