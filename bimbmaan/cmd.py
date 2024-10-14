from .base import BimbBase

class BimbCMD(BimbBase):
  parsed_cli_args = {}
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def _process_cli_args(self):
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

    self.parsed_cli_args = self.get_cli_args(_cli_settings, version=_version_info)
    return self.parsed_cli_args

  def pdf_to_image(self):
    self._process_cli_args()
    self.log_info("PDF => Images...")
    print("Starting image conversion...")

    # Add logic based on extension

    from .helper.image import BimbImgProcessor
    _bimp = BimbImgProcessor(path_base=self.path_base)

    # Pass all arguments???
    if getattr(self, 'path_file'):
      _bimp._convert_pdf_to_img(**self.parsed_cli_args)
    else:
      _pdfs = self.search_files(self.get_path(), "*.pdf")
      for _pdf in _pdfs:
        _bimp._convert_pdf_to_img(path_file=_pdf)

    print("Image conversion completed...")

  # Clip Image
  def clip_image(self):
    self.log_info("Trimming Whitespace within the Images")
    self._process_cli_args()

    from .helper.image import BimbImgProcessor
    _bimp = BimbImgProcessor(path_base=self.path_base)

    _found_images = self.find_files(self.get_path(), ["jpg", "png", "jpeg"])
    for _image in _found_images:
      _out_image = self.change_ext(_image, 'clipped.png')
      _bimp.remove_image_bg(_image, _out_image)

  def remove_bg(self):
    ...

  def tiling(self):
    return self._tile_images_in_pptx()

  def svg_converter(self):
    from .helper.image import BimbImgProcessor
    _bimp = BimbImgProcessor(path_base=self.path_base)
    return _bimp._svg_to_meta()
