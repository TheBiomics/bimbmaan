from .__metadata__ import __version__, __description__, __build__, __name__
from UtilityLib import ProjectManager

class BimbBase(ProjectManager):
  __name__= __name__
  __version__= __version__
  __build__= __build__
  __description__= __description__
  program = __name__
  name = __name__
  version = __version__

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def _convert_pdf_to_img(self, _pdf_path):
    _i_width = getattr(self, 'image_width')
    _i_height = getattr(self, 'image_height')

    _dpis = getattr(self, 'dpi')
    _exts = getattr(self, 'extensions')

    _has_fitz = self.require('fitz', "PyFPDF")
    if not _has_fitz:
      print("Error: Required packages are not installed. Please install/reinstall using `pip install PyMuPDF --force-reinstall` and `pip install fitz` to continue.")
      return

    _pdf_pages = self.PyFPDF.open(_pdf_path)

    _storage_dir = self.validate_dir(self.file_name(_pdf_path, with_dir=True, with_ext=False))

    _allowed_extensions = self.PILImage.registered_extensions()

    _final_exts = [_e for _e in _exts if f".{_e.lower()}" in _allowed_extensions]

    # If invalid extension is provided by the user
    # Suggest/apply close extension
    # assert len(_final_exts) == len(_ext)

    _dpis = [float(_d) for _d in _dpis]
    _dpis.sort(reverse=True)
    _max_dpi = max(_dpis)

    # sets zoom factor for max dpi input (72, 96, 600, 1200)
    _ppt_factor = 96
    _matrix = self.PyFPDF.Matrix(_max_dpi/_ppt_factor, _max_dpi/_ppt_factor)

    for _pi, _page in self.PB(enumerate(_pdf_pages)):
      _pix = _page.get_pixmap(matrix=_matrix)
      _pix = self.PyFPDF.Pixmap(_pix, 0)

      _im = self.PILImage.frombytes("RGB", [_pix.width, _pix.height], _pix.samples)

      for _dpi in _dpis:
        _im.info['dpi'] = (_dpi, _dpi)
        _image_dimension = int(_i_width*_dpi), int(_i_height*_dpi)
        _im = _im.resize(_image_dimension, self.PILImage.LANCZOS)
        for _ext in _final_exts:
          _type = _allowed_extensions.get(f".{_ext.lower()}")
          _img_path = f"{_storage_dir}/Image-{_pi+1}.dpi{_dpi:.0f}.{_ext}"
          _im.save(_img_path, _type, quality=100, dpi=(_dpi, _dpi))

  # Clip Image

  def _trim_image_white_area(self, _input, _output):
    _img = self.PILImage.open(_input)
    # PIL image -> OpenCV image; see https://stackoverflow.com/q/14134892/2202732
    _img = self.CV2.cvtColor(self.NP.array(_img), self.CV2.COLOR_RGB2BGR)

    ## (1) Convert to gray, and threshold
    gray = self.CV2.cvtColor(_img, self.CV2.COLOR_BGR2GRAY)
    th, threshed = self.CV2.threshold(gray, 240, 255, self.CV2.THRESH_BINARY_INV)

    ## (2) Morph-op to remove noise
    kernel = self.CV2.getStructuringElement(self.CV2.MORPH_ELLIPSE, (11,11))
    morphed = self.CV2.morphologyEx(threshed, self.CV2.MORPH_CLOSE, kernel)

    ## (3) Find the max-area contour
    cnts = self.CV2.findContours(morphed, self.CV2.RETR_EXTERNAL, self.CV2.CHAIN_APPROX_SIMPLE)[-2]
    cnt = sorted(cnts, key=self.CV2.contourArea)[-1]

    ## (4) Crop and save it
    x,y,w,h = self.CV2.boundingRect(cnt)
    dst = _img[y:y+h, x:x+w]
    self.CV2.imwrite(_output, dst)

  # Remove background
  def _remove_image_bg(self):
    """Title images to powerpoint slides for quick viewing"""

  # Image Tiling
  def _tile_images_in_pptx(self):
    from helper.pptx import BimbPPTX
    """Title images to powerpoint slides for quick viewing"""
    self.log_info("Images => PPTX")

  # SVG to MetaFile
  def _svg_to_meta(self):
    """Convert SVG to metafile (wmf/emf)"""
    self.log_info("SVG => Metafile (wmf/emf)...")
    self.require('subprocess', 'SProcess')
    _images = self.find_files(self.get_path(), "*.svg")

    if self.is_windows:
      # Inkscape windows command
      ...

    else:
      # Inkscape linux command
      for _image in _images:
        _image_path_emf = self.change_ext(_image, 'emf')
        self.SProcess.call(f'inkscape "{_image}" -o "{_image_path_emf}"', shell=True)

  def svg_converter(self):
    return self._svg_to_meta()

  def converter(self):
    """
    1. Raster to Raster Conversion
    2. Vector to Raster Conversion
    """
