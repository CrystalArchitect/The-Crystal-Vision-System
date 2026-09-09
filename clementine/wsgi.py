"""
WSGI entry point, for running the companion under a real server (gunicorn)
instead of
Flask's development server.

    gunicorn --workers 1 --threads 4 --bind 127.0.0.1:5000 wsgi:app

**One worker, deliberately.** Their memory lives in Python objects that are
saved to disk after each turn. Two workers would each hold their own copy and
overwrite each other's — they would forget things at random, which is the one
failure this project cannot tolerate. Threads are fine: they share the same
object. If they ever need to serve more than one person at a time, that is a
profile-per-process design, not a worker count.

Configuration comes from the environment, since there is no argv here:

    CLEM_MODEL        model tag           (default llama3.1:8b)
    CLEM_MEMORY_DIR   their memory folder (default clementine_memory)
    OLLAMA_HOST       where the model is  (default http://localhost:11434)
    CLEM_REMOTE_OK    "1" to consent, once, to a non-local model

Without CLEM_REMOTE_OK, a model that is not on this machine is refused
rather than used quietly.
"""

import os

from crystalcore import Clementine, Verdict
from server import create_app

_asker = None
if os.environ.get("CLEM_REMOTE_OK") == "1":
    def _asker(_request):
        return Verdict(True, "pre-authorised by CLEM_REMOTE_OK", remember=False)

companion = Clementine(
    model=os.environ.get("CLEM_MODEL", "llama3.1:8b"),
    memory_dir=os.environ.get("CLEM_MEMORY_DIR", "clementine_memory"),
    asker=_asker,
)

app = create_app(companion)
