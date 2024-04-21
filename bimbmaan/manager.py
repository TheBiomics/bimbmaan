from UtilityLib import ProjectManager

from PIL import Image

class BimbManager(ProjectManager):
  program = "BimbMaan"
  build = 20240410

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def process_args(self):
    # key: (['arg_k1', 'arg_k2'], nargs, default, help, {})
    _version_info = f"{self.program} (build-{self.build})"
    _cli_settings = {
      "path_base": (['-b'], "*", self.OS.getcwd(), 'Provide base directory to run the process.', {}),
      "path_file": (['-f'], "*", None, 'Provide file path to process.', {}),
      "image_width": (['-iw'], "*", 11.7, 'Output image width in inches.', {}),
      "image_height": (['-ih'], "*", 8.3, 'Output image height in inches.', {}),
      "dpi": (['-d'], "*", [72, 600], 'Output image DPI.', {}),
      "extensions": (['-e'], "*", ["jpg"], 'Output image DPI for output quality. Most of the image extensions are allowed are recognised.', {}),
    }

    _params = self.get_cli_args(_cli_settings, version=_version_info)

    if hasattr(self, 'setattrs'):
      self.setattrs(_params)
    else:
      self.update_attributes(self, _params)

  def _pdf_to_img(self, _pdf_path):
    _i_width = getattr(self, 'image_width')
    _i_height = getattr(self, 'image_height')

    _dpis = getattr(self, 'dpi')
    _exts = getattr(self, 'extensions')

    _write_file_path = _pdf_path

    if not self.require('fitz', "PyFPDF"):
      print("Error: Please install `pip install fitz` and `pip install PyMuPDF` to continue.")
      return

    _pdf_pages = self.PyFPDF.open(_pdf_path)

    _allowed_extensions = Image.registered_extensions()
    
    for _pi, page in self.PB(enumerate(_pdf_pages)):
      _pix = page.get_pixmap()
      _pix = self.PyFPDF.Pixmap(_pix, 0)

      _im = Image.frombytes("RGB", [_pix.width, _pix.height], _pix.samples)

      for _dpi in _dpis:
        _dpi = float(_dpi)
        _im.info['dpi'] = (_dpi, _dpi)
        _image_dimension = int(_i_width*_dpi), int(_i_height*_dpi)
        _im = _im.resize(_image_dimension, Image.LANCZOS)
        for _ext in _exts:
          if not f".{_ext.lower()}" in _allowed_extensions:
            continue
          _type = _allowed_extensions.get(f".{_ext.lower()}")
          # Slide number using PDF file name when there are multiple PDF files 
          # Or create a directory with the PDF file name and generate images there
          _img_path = self.change_ext(_write_file_path, f"S{_pi+1}.dpi{_dpi:.0f}.{_ext}")
          _im.save(_img_path, _type, quality=100, dpi=(_dpi, _dpi))

  def pdf_to_image(self):
    self.process_args()
    print("Starting image conversion...")

    # Add logic based on extension

    if getattr(self, 'path_file'):
      self._pdf_to_img(getattr(self, 'path_file'))
    else:
      _pdfs = self.search_files(self.get_path(), "*.pdf")
      for _pdf in _pdfs:
        self._pdf_to_img(_pdf)
    print("Image conversion completed...")

  def _tile_to_pptx(self):
    """Title images to powerpoint slides for quick viewing"""

  def tiling(self):
    ...

  def _svg_to_meta(self):
    """Convert SVG to metafile (wmf/emf)"""

    if self.is_windows:
      # Inkscape windows command
      ...
    
    else:
      # Inkscape linux command
      ...

  def converter(self):
    """
    1. Raster to Raster Conversion
    2. Vector to Raster Conversion
    """
    ...
