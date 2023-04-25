#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import logging
import yaml
import pytoml as toml
import datetime
import re

default_logging_level = logging.WARNING
default_timezome_offset = +datetime.timedelta(hours=8)


class Logger(object):
    def __init__(self, name):
        logformat = 'Hexo2hugo (%(name)s): [%(levelname)s] %(message)s'

        self.logger = logging.getLogger(name or __name__)
        self.logger.setLevel(default_logging_level)
        myhandler = logging.StreamHandler()
        myhandler.setFormatter(logging.Formatter(logformat))
        self.logger.addHandler(myhandler)


class Hexo2Hugo(object):
    def __init__(self, src, dest, remove_date):
        self.root_path = os.path.expanduser(src)
        self.dest_path = os.path.expanduser(dest)
        self.remove_date = remove_date
        self.logger = Logger("Hexo").logger

        self._find_all_files()

    def go(self):
        for post in self._process_files():
            name = post['name']
            meta = post['meta']
            body = post['body']

            if self.remove_date:
                name = self._remove_date(name)

            with open(os.path.join(self.dest_path, name), 'w+') as fp:
                self.logger.info("Write to {}, meta: {}".format(name, meta))
                fp.writelines("+++\n{}+++\n\n{}".format(meta, body))

    def _remove_date(self, name):
        new_name = re.sub('^\d+-\d+-\d+-(.*)', r'\1', name)
        if new_name:
            return new_name
        return name

    def _find_all_files(self):
        self.files = []
        for file in os.listdir(self.root_path):
            if os.path.isfile(os.path.join(self.root_path, file)):
                self.files.append(file)
        self.logger.info("Total {} files found".format(len(self.files)))

    def _extract_date_from_filename(self, filename):
        m = re.match('^(\d+-\d+-\d+)-.*$', filename)
        if m:
            return m.group(1)

    def _process_files(self):
        for hexo_file in self.files:
            date_from_filename = self._extract_date_from_filename(hexo_file)
            with open(os.path.join(self.root_path, hexo_file), 'r') as fp:
                meta_yaml = ''
                body = ''
                is_meta = True
                is_first_line = True
                is_in_pre = False
                for line in fp:
                    if is_first_line:
                        is_first_line = False
                        if line == '---\n':
                            continue

                    if is_meta:
                        if line == '---\n':
                            is_meta = False
                        else:
                            meta_yaml += line
                    else:
                        if re.search(r'.html$', hexo_file):
                            if re.search(r'^<pre', line):
                                is_in_pre = True

                            if re.search(r'^</pre', line):
                                is_in_pre = False

                            if not is_in_pre and not re.match(r'^$', line) and not re.search(r'<br */>$', line):
                                body += line[:-1] + "<br />\n"
                            else:
                                body += line
                        else:
                            body += line
                meta = yaml.full_load(meta_yaml)

                self.logger.info("Process {} now, meta: {}, body length: {}".format(hexo_file, meta, len(body)))

                if 'date' in meta:
                    no_tz_date = meta['date']
                    if type(no_tz_date) == str:
                        no_tz_date = datetime.datetime.strptime(no_tz_date, '%Y-%m-%d %H:%M')

                    meta['date'] = no_tz_date.replace(tzinfo=datetime.timezone(default_timezome_offset)).isoformat('T')
                else:
                    meta['date'] = date_from_filename

                meta['description'] = ''
                if 'permalink' in meta:
                    meta['slug'] = meta['permalink']
                    del meta['permalink']

                if 'layout' in meta:
                    del meta['layout']

                if 'tags' in meta and type(meta['tags']) == str:
                    meta['tags'] = meta['tags'].split(',')

                meta_toml = toml.dumps(meta)
                yield({'name': hexo_file, 'meta': meta_toml, 'body': body})


def main(args):
    hexo = Hexo2Hugo(args.src, args.dest, args.remove_date_from_name)
    hexo.go()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', help='Hexo posts directory')
    parser.add_argument('--dest', help='Destination directory')
    parser.add_argument('--remove-date-from-name', help='Remove date from file name', action='store_true')
    parser.add_argument('--verbose', help='Output level', action='store_true')

    args = parser.parse_args()

    if args.verbose:
        default_logging_level = logging.DEBUG

    main(args)
