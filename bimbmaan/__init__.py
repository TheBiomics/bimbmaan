from .manager import BimbManager

def bimbpdf():
  _m = BimbManager()
  _m.pdf_to_image()

def bimbsvg():
  _m = BimbManager()
  _m._svg_to_meta()

def bimbtile():
  _m = BimbManager()
  _m.tiling()

def bimbconv():
  _m = BimbManager()
  _m.converter()

def bimbclip():
  _m = BimbManager()
  _m.clip_image()

def bimbrbg():
  _m = BimbManager()
  _m.remove_bg()
