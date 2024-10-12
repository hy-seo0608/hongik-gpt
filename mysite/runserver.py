import os

os.system('daphne config.asgi:application --port 8000 --bind 0.0.0.0 -v2')
