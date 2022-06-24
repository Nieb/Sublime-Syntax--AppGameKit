import sublime
import sublime_plugin

import os

from Default.exec import ExecCommand

class AgkBuildCommand(ExecCommand):
    def run(self, **kwargs):
        variables = self.window.extract_variables()

        WhereAreWe = variables["file_path"]

        if "src"    in WhereAreWe: WhereAreWe = WhereAreWe[0:len(WhereAreWe)-4]
        if "source" in WhereAreWe: WhereAreWe = WhereAreWe[0:len(WhereAreWe)-7]
        if "shader" in WhereAreWe: WhereAreWe = WhereAreWe[0:len(WhereAreWe)-7]

        variables["LocationOfMain"] = WhereAreWe

        kwargs = sublime.expand_variables(kwargs, variables)
        super().run(**kwargs)
