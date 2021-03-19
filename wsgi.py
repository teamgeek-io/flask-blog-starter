import os
import sys

sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "src")
)

from flask_blog import *  # noqa: E402 F403

app = create_app()  # noqa: F405
