import sys
import traceback

try:
    from main import app
    print("Import successful")
except Exception:
    traceback.print_exc()
