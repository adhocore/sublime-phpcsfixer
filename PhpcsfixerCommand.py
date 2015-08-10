import os
import subprocess
import sublime_plugin

class PhpcsfixerCommand(sublime_plugin.TextCommand):
    """A minimal PHP cs fixer plugin for sublime - by Jitendra Adhikari"""
    def run(self, edit):
        path = self.view.file_name()
        ext  = os.path.splitext(path)[1]
        conf = sublime.load_settings('phpcsfixer.sublime-settings')

        # Validate file type
        if ext[1:] not in conf.get('phpcsfixer_file_extensions'):
            return False

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
