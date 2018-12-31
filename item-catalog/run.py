# JETBRAINS DEBUGGING CODE ==================================================================:
import sys
sys.path.append("pycharm-debug-py3k.egg")

import pydevd
pydevd.settrace('10.57.211.83', port=4444, stdoutToServer=True, stderrToServer=True)
#===========================================================================================
# Run a development server
from app import app

def run():
    print('run called...')
    app.secret_key = 'super_secret_key'
    # app.run(host='0.0.0.0', port=8000, debug=True)
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
    # pydevd.settrace(self.host, port=self.port, stdoutToServer=True, stderrToServer=True)

    import pydevd
    pydevd.settrace('10.57.211.83', port=4444, stdoutToServer=True, stderrToServer=True)

if __name__ == '__main__':
    run()