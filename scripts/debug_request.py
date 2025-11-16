import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

app = create_app()
app.config['TESTING'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

with app.test_client() as c:
    try:
        r = c.get('/')
        print('status:', r.status_code)
        print('body:', r.data.decode('utf-8', errors='ignore'))
    except Exception as e:
        import traceback
        traceback.print_exc()