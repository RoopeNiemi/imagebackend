from app import app
import os


if __name__ == '__main__':
    if 'PORT' in  os.environ:
        port = os.environ['PORT']
    else:
        port=5000
    app.run(debug=True, host='0.0.0.0', port=port)