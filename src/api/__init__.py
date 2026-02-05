import os
import sys

sys.path.append(os.path.abspath(".."))


__all__ = ("router",)


from .routes import router
