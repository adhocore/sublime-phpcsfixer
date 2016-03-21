import os
import sublime
import subprocess
import sublime_plugin

conf = sublime.load_settings('phpcsfixer.sublime-settings')

def phpcsfix(view):
    path = view.file_name()

    # The command line params
    cmd = [
        conf.get('phpcsfixer_php_path'),
        conf.get('phpcsfixer_phar_path'),
        "fix",
        path
    ]

    # Append extra options if any
    for key, value in conf.get('phpcsfixer_options').items():
        arg = key
        if value != "":
            arg += "=" + value
        cmd.append(arg)

    # Info for winOS
    info = None
    if os.name == 'nt':
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=info)
    if proc.stdout:
        data = proc.communicate()[0]

    return True

class PhpcsfixerCommand(sublime_plugin.TextCommand):
    """A minimal PHP cs fixer plugin for sublime - by Jitendra Adhikari"""
    def run(self, edit):
        return phpcsfix(self.view)

    def is_enabled(self):
        ext  = os.path.splitext(self.view.file_name())[1]
        conf = sublime.load_settings('phpcsfixer.sublime-settings')

        return ext[1:] in conf.get('phpcsfixer_file_extensions')

class RunFixerOnSave(sublime_plugin.EventListener):
    def on_post_save(self, view):
        if conf.get('phpcsfixer_fix_on_save'):
            return phpcsfix(view)
