from .base import BimbBase

class BimbCMD(BimbBase):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def _process_pdf_to_img_args(self):
    # key: (['arg_k1', 'arg_k2'], nargs, default, help, {})
    _version_info = f"{self.program} (build-{self.__build__})"
    _cli_settings = {
      "path_base": (['-b'], "*", self.OS.getcwd(), 'Provide base directory to run the process.', {}),
      "path_file": (['-f'], "*", None, 'Provide file path to process.', {}),
      "image_width": (['-iw'], "*", 11.7, 'Output image width in inches.', {}),
      "image_height": (['-ih'], "*", 8.3, 'Output image height in inches.', {}),
      "dpi": (['-d'], "*", [72, 600], 'Output image DPI.', {}),
      "pages": (['-p'], "*", None, 'Pages (comma or space separated integers) to be processed. Add negative integer to exclude the page.', {}),
      "extensions": (['-e'], "*", ["jpg"], 'Output image DPI for output quality. Most of the image extensions are allowed are recognised.', {}),
    }

    _params = self.get_cli_args(_cli_settings, version=_version_info)

    if hasattr(self, 'setattrs'):
      self.setattrs(_params)
    else:
      self.update_attributes(self, _params)

  def pdf_to_image(self):
    self._process_pdf_to_img_args()
    self.log_info("PDF => Images...")
    if not self.require('PIL.Image', 'PILImage'):
      print("Error: PIL module is not installed.")
      return

    print("Starting image conversion...")

    # Add logic based on extension

    if getattr(self, 'path_file'):
      self._convert_pdf_to_img(getattr(self, 'path_file'))
    else:
      _pdfs = self.search_files(self.get_path(), "*.pdf")
      for _pdf in _pdfs:
        self._convert_pdf_to_img(_pdf)

    print("Image conversion completed...")

  # Clip Image
  def clip_image(self):
    self.log_info("Trimming Whitespace within the Images")
    self._process_pdf_to_img_args()
    self.require('cv2', 'CV2')
    self.require('numpy', 'NP')
    self.require('PIL.Image', 'PILImage')
    _found_images = self.find_files(self.get_path(), ["jpg", "png", "jpeg"])
    for _image in _found_images:
      _out_image = self.change_ext(_image, 'clipped.png')
      self._trim_image_white_area(_image, _out_image)

  def remove_bg(self):
    ...

  def tiling(self):
    return self._tile_images_in_pptx()

  def svg_converter(self):
    return self._svg_to_meta()

  def converter(self):
    """
    1. Raster to Raster Conversion
    2. Vector to Raster Conversion
    """

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
