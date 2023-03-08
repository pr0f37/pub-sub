import os
import sys

from api.app import create_app

if __name__ == "__main__":
    try:
        create_app()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
