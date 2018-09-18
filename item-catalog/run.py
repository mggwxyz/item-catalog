# Setup debugger
# from mydebugger import Debugger, DebuggerClient
# from config import REMOTE_DEBUG_SERVER_HOST, REMOTE_DEBUG_SERVER_PORT
# Debugger.set_debugger_client(DebuggerClient(REMOTE_DEBUG_SERVER_HOST, REMOTE_DEBUG_SERVER_PORT))

# Run a development server
from app import app

def run():
    print('run called...')
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=8000, debug=True, ssl_context='adhoc')

if __name__ == '__main__':
    run()