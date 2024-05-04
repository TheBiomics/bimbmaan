from .cmd import BimbCMD as CMD
from .manager import BimbManager as BimbMan

def bimbpdf():
  _m = CMD()
  _m.pdf_to_image()

def bimbsvg():
  _m = CMD()
  _m._svg_to_meta()

def bimbtile():
  _m = CMD()
  _m.tiling()

def bimbconv():
  _m = CMD()
  _m.converter()

def bimbclip():
  _m = CMD()
  _m.clip_image()

def bimbrbg():
  _m = CMD()
  _m.remove_bg()
