import sublime
import sublime_plugin

import subprocess
import threading
import os

class AgkBuildCommand(sublime_plugin.WindowCommand):
    ###########################################################################################################################################################
    ###########################################################################################################################################################
    BuildCancelled = False
    OutputPanel = None
    OutputPanelLock = threading.Lock()
    BuildProcess = None
    Encoding = 'utf-8'

    ###########################################################################################################################################################
    ###########################################################################################################################################################
    def is_enabled(self, CancelBuild=False):
        # The Cancel build option should only be available when the process is still running.
        if CancelBuild:
            return self.BuildProcess is not None and self.BuildProcess.poll() is None
        return True


    ###########################################################################################################################################################
    ###########################################################################################################################################################
    def run(self, CompileAndBroadcast=False, CompileAndDebug=False, CompileAndRun=False, CancelBuild=False):
        #=============================================================================================================================
        if CancelBuild:
            if self.BuildProcess:
                self.BuildProcess.terminate()
                self.BuildCancelled = True
            return

        #=============================================================================================================================
        BuildSetupErrorStr = "AppGameKit.py ERROR: "
        BuildSetupError    = False
        BuildVariables     = self.window.extract_variables()
        BuildSettings      = sublime.load_settings("AppGameKit.sublime-settings")

        #=============================================================================================================================
        # Find "AGKCompiler.exe".
        Use64bitInterpreter = BuildSettings.get("Use64bitInterpreter", False)
        #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if CompileAndRun:
            RunMe = BuildSettings.get("AGKCompiler", "")
            if not os.path.exists(RunMe):
                self.queue_write(BuildSetupErrorStr+"'"+RunMe+"' does not exist.\n"+" "*len(BuildSetupErrorStr)+"Also, try restarting SublimeText.\n")
                BuildSetupError = True
            else:
                if Use64bitInterpreter: RunMe = RunMe + " -run -64 main.agc"
                else                  : RunMe = RunMe + " -run main.agc"
        #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        elif CompileAndBroadcast:
            RunMe = BuildSettings.get("AGKBroadcaster", "")
            if not os.path.exists(RunMe):
                self.queue_write(BuildSetupErrorStr+"'"+RunMe+"' does not exist.\n"+" "*len(BuildSetupErrorStr)+"Also, try restarting SublimeText.\n")
                BuildSetupError = True
            else:
                if Use64bitInterpreter: RunMe = RunMe + " ??? -64 todo.agc"
                else                  : RunMe = RunMe + " ??? todo.agc"
        #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        elif CompileAndDebug:
            RunMe = BuildSettings.get("AGKBroadcaster", "")
            if not os.path.exists(RunMe):
                self.queue_write(BuildSetupErrorStr+"'"+RunMe+"' does not exist.\n"+" "*len(BuildSetupErrorStr)+"Also, try restarting SublimeText.\n")
                BuildSetupError = True
            else:
                if Use64bitInterpreter: RunMe = RunMe + " ??? -64 todo.agc"
                else                  : RunMe = RunMe + " ??? todo.agc"
        #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        else:
            RunMe = BuildSettings.get("AGKCompiler", "")
            if not os.path.exists(RunMe):
                self.queue_write(BuildSetupErrorStr+"'"+RunMe+"' does not exist.\n"+" "*len(BuildSetupErrorStr)+"Also, try restarting SublimeText.\n")
                BuildSetupError = True
            else:
                if Use64bitInterpreter: RunMe = RunMe + " -agk -64 main.agc"
                else                  : RunMe = RunMe + " -agk main.agc"
        #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #=============================================================================================================================
        # Find "main.agc".
        WorkingDir = BuildVariables["file_path"]
        BackSlashCount = WorkingDir.count("\\")-1

        SearchDepth = BuildSettings.get("FindMainAgcDepth", 0)
        SearchDepth = max(SearchDepth,              0) # Not less-than 0.
        SearchDepth = min(SearchDepth, BackSlashCount) # Not greater-than number of parent dirs.

        MainFound = False
        for iLook in range(0, SearchDepth+1):
            if os.path.isfile(WorkingDir+"\\main.agc"):
                MainFound = True
                break
            elif iLook == SearchDepth:
                self.queue_write(BuildSetupErrorStr+"Unable to find 'main.agc'.  MainAgcLookDepth = "+str(SearchDepth)+"\n")
                BuildSetupError = True
            elif MainFound == False:
                WorkingDir = WorkingDir[0:WorkingDir.rfind("\\", 0, len(WorkingDir)-1)]

        #=============================================================================================================================
        # A lock is used to ensure only one thread is touching the output panel at a time.
        with self.OutputPanelLock:
            # Creating the panel implicitly clears any previous contents.
            self.OutputPanel = self.window.create_output_panel('exec')

            # OutputPanel result navigation.  Double-click message to goto error File & LineNumber.
            OutputPanelSettings = self.OutputPanel.settings()
            OutputPanelSettings.set('result_file_regex', r'^\s{2}\K(.+\.agc):(\d+):' )
            OutputPanelSettings.set('result_line_regex',                  r':(\d+):' )
            OutputPanelSettings.set('result_base_dir', WorkingDir )

        #=============================================================================================================================
        # Run build.
        if self.BuildProcess is not None:
            self.BuildProcess.terminate()
            self.BuildProcess = None

        if BuildSetupError:
            self.BuildCancelled = True
        else:
            if   CompileAndRun      : self.queue_write("AppGameKit Compile & Run: "      +RunMe+"\n")
            elif CompileAndBroadcast: self.queue_write("AppGameKit Compile & Broadcast: "+RunMe+"\n")
            elif CompileAndDebug    : self.queue_write("AppGameKit Compile & Debug: "    +RunMe+"\n")
            else                    : self.queue_write("AppGameKit Compile: "            +RunMe+"\n")

            self.BuildProcess = subprocess.Popen( RunMe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=WorkingDir )
            self.BuildCancelled = False
            threading.Thread( target=self.read_handle, args=(self.BuildProcess.stdout,) ).start()


    ###########################################################################################################################################################
    ###########################################################################################################################################################
    def read_handle(self, handle):
        chunk_size = 2 ** 13
        out = b''
        while True:
            try:
                data = os.read(handle.fileno(), chunk_size)
                # If exactly the requested number of bytes was
                # read, there may be more data, and the current
                # data may contain part of a multibyte char
                out += data
                if len(data) == chunk_size:
                    continue
                if data == b'' and out == b'':
                    raise IOError('EOF')

                # We pass out to a function to ensure the
                # timeout gets the value of out right now,
                # rather than a future (mutated) version
                self.queue_write("  " + out.decode(self.Encoding).replace("\r\n", "\n  ").replace("\r", "\n  "))

                if data == b'':
                    raise IOError('EOF')
                out = b''
            except (UnicodeDecodeError) as e:
                msg = 'Error decoding output using %s - %s'
                self.queue_write(msg  % (self.Encoding, str(e)))
                break
            except (IOError):
                if self.BuildCancelled: msg = 'Cancelled'
                else                  : msg = 'Finished'
                self.queue_write('\n[%s]' % msg)
                break


    ###########################################################################################################################################################
    ###########################################################################################################################################################
    def queue_write(self, text):
        sublime.set_timeout(lambda: self.do_write(text), 1)

    def do_write(self, text):
        with self.OutputPanelLock:
            self.OutputPanel.run_command('append', {'characters': text})

