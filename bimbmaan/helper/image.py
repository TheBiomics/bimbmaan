from ..base import BimbBase

class BimbImgProcessor(BimbBase):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    if not all([self.require('PIL.Image', 'PILImage'), self.require('cv2', 'CV2'), self.require('numpy', 'NP')]):
      self.log_error("Error: Either PIL module/CV2/NP are not installed.")

  def _convert_pdf_to_img(self, *args, **kwargs):
    _path_pdf = kwargs('path_file', args[0] if len(args) > 0 else None)
    _i_width = kwargs('image_width', args[1] if len(args) > 1 else 11.7)
    _i_height = kwargs('image_height', args[2] if len(args) > 2 else 8.3)
    _dpis = kwargs('dpi', args[3] if len(args) > 3 else [72])
    _exts = kwargs('extensions', args[4] if len(args) > 4 else ['jpg'])

    if not self.require('fitz', "PyFPDF"):
      print("Error: Required packages are not installed. Please install/reinstall using `pip install PyMuPDF --force-reinstall` and `pip install fitz` to continue.")
      return

    _pdf_pages = self.PyFPDF.open(_path_pdf)

    _storage_dir = self.validate_dir(self.file_name(_path_pdf, with_dir=True, with_ext=False))

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

  def remove_image_bg(self, *args, **kwargs):
    _image_source = kwargs('input', args[0] if len(args) > 0 else None)
    _image_destination = kwargs('output', args[1] if len(args) > 1 else None)

    _img_obj = self.PILImage.open(_image_source)

    # PIL image -> OpenCV image; see https://stackoverflow.com/q/14134892/2202732
    _img = self.CV2.cvtColor(self.NP.array(_img_obj), self.CV2.COLOR_RGB2BGR)

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
    _img = _img[y:y+h, x:x+w]

    if _image_destination:
      self.CV2.imwrite(_image_destination, _img)

    return _img

  clip_remove_bg = remove_image_bg
  _trim_image_white_area = remove_image_bg

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

  svg_converter = _svg_to_meta

  def equalise_height_width():
    ...

  def equalise_height():
    ...

  def equalise_width():
    ...

  def _clip_white_space(self):
    """Clip whitespace of images"""

  def _remove_image_bg(self):
    """Bulk remove background from images"""

  def _add_image_border(self):
    """Bulk add border to images"""

  def _convert_to_grayscale(self):
    """Bulk convert images to grayscale"""

  def _image_to_video(self):
    """Bulk create video from images"""

  def _image_stiching(self):
    """Stiches images like panorama"""

  def converter(self):
    """
    1. Raster to Raster Conversion
    2. Vector to Raster Conversion
    """
