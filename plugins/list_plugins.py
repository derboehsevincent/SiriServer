#!/usr/bin/python
# -*- coding: utf-8 -*-
#created by nuno12345
#edited by derboehsevincent - fixed handling for german language

import re,os
from plugin import *

config_file="plugins.conf"
pluginPath="plugins"
tline = []
tline_answer = ''

with open(config_file, "r") as fh:
    for line in fh:
        line = line.strip()
        if not line.startswith("#") and len(line) != 0:
            tline.append(line)
    for x in sorted(tline):
        tline_answer = tline_answer +'\n' + "".join(x)


class help(Plugin):

    @register("de-DE", "(Script)|(Scripts)")
    @register("en-US", "(Script)|(Scripts)")
    def st_hello(self, speech, language):
        if language == 'de-DE':
            self.say("Folgende Plugins sind auf dem Server installiert:")
            self.say(tline_answer,' ')
        else:
            self.say("Here are the plugins installed in your server:")
            self.say(tline_answer,' ')
        self.complete_request()
