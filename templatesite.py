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

parser.add_option('-l', '--localpaths', dest='withlocalpaths', action='store_true',
                  default=False, help='Transform urls to local paths, useful for testing locally')

parser.add_option('-c', '--css', dest='with_css', action='store_true',
                  default=False, help='Process CSS files as templates too')


options, args = parser.parse_args()

path = os.curdir
out_path = os.path.abspath(options.output)

try:
    os.stat(out_path)
except Exception, e:
    os.mkdir(out_path)

print "Loading Environment"
print "Input Path:", path
print "Output Path:", out_path

file_types = ['.html']

if options.with_css:
    file_types.append('.css')

env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))

def url(u):
    if options.withlocalpaths:
        if u[0] == '/':
            u = u[1:]
        final_url = 'file:///' + os.path.join(out_path, u).replace(os.path.sep, '/')
    else:
        final_url = u
    return final_url

env_vars = dict(url=url)
def parse_folder(folder_path, base_path):
    print "\tParsing folder [%s]" % base_path
    for filename in os.listdir(folder_path):
        if filter(lambda x: x in filename, file_types) and filename != options.master_template:
            t_path = os.path.join(base_path, filename)
            t_name = t_path.replace('\\', '/')
            print "\tRendering template:", t_name
            template = env.get_template(t_name)
            output = os.path.join(out_path, t_path)
            fd = file(output, 'w')
            fd.write(template.render(**env_vars).encode('utf-8'))
            fd.close()
        elif os.path.isdir(os.path.join(folder_path, filename)):
            print "\tDescending into folder:", filename
            output = os.path.join(out_path, base_path, filename)
            try:
                os.stat(output)
            except Exception, e:
                os.mkdir(output)
            parse_folder(os.path.join(folder_path, filename), os.path.join(base_path, filename))

if options.output:
    print "Parsing files"
    parse_folder(path, '')
