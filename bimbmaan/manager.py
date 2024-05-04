from .base import BimbBase

class BimbManager(BimbBase):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
