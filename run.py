# Run a development server
from app import app
app.secret_key = 'super_secret_key'
app.run(host='0.0.0.0', port=8000, debug=True)
