from app_start import *
import os

if __name__ == "__main__":
    debug = False
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)
