"""Source: http://blog.digital-horror.com/how-to-setup-pycharms-remote-debugger-for-docker/"""
class DebuggerClient:
    """Shell class that stores properties to be used by the debugger

    Exposes methods to be used for debugging purposes
    """

    def __init__(self, server_host, server_port):
        self.host = server_host
        self.port = int(server_port)

    def breakpoint(self):
        """Sets a breakpoint for the debug server to catch

        Will only set the breakpoint should the debugger client is set;
         this is done to ensure that in a non-development environment
         any possible lingering breakpoints don't accidentally hang
         any threads.
        """
        import pydevd
        from app.config.DevelopmentConfig import ENVIRONMENT

        if ENVIRONMENT.lower() == 'development':
            pydevd.settrace(self.host, port=self.port, stdoutToServer=True, stderrToServer=True)


class Debugger:
    """Assigns the debugger client to be used as a class variable

    Only will allow a single debugger client to be assigned at any
     given time.
    """

    debugger = None  # :class:DebuggerClient

    def __init__(self):
        pass

    @classmethod
    def set_debugger_client(cls, debugger):
        """Sets the debugger client"""
        cls.debugger = debugger