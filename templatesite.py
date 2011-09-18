#!/usr/bin/env python
#
#    TemplateSite: Static site generator from Jinja2 templates
#    Copyright (C) 2011  Carlos Daniel Ruvalcaba Valenzuela
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.#
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import jinja2
from optparse import OptionParser

parser = OptionParser()

parser.add_option('-o', '--output', dest='output',
                  help='Output directory')

parser.add_option('-m', '--master', dest='master_template',
                  default='master.html', help='Master template')

parser.add_option('-r', '--recursive', dest='recursive', action='store_true',
                  default=True, help='Recursive parsing')

options, args = parser.parse_args()

path = os.curdir
out_path = os.path.abspath(options.output)

try:
    os.path.dirname(out_path)
except Exception, e:
    os.mkdir(out_path)

env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))

def parse_folder(folder_path, base_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.html') and filename != options.master_template:
            t_path = os.path.join(base_path, filename)
            template = env.get_template(t_path)
            output = os.path.join(out_path, t_path)
            template.render(output)
        elif os.path.isdir(os.path.join(folder_path, filename)) and filename != 'media':
            output = os.path.join(out_path, filename)
            try:
                os.path.dirname(output)
            except Exception, e:
                os.mkdir(output)
                parse_folder(os.path.join(folder_path, filename), os.path.join(base_path, filename))

if options.output:
    parse_folder(path)
