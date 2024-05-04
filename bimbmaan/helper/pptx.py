
from UtilityLib.base import BaseUtility
from pptx import Presentation
from pptx.util import Inches, Pt

# Remove clip_remove_bg against bimbmaan that clips images and removes extra white area

class BimbPPTX():
  def __init__(self, *args, **kwargs):
    self.PPTX_Obj = Presentation()
    self.layout = self.PPTX_Obj.slide_masters[0].slide_layouts[0]
    self.slide = self.PPTX_Obj.slides.add_slide(self.layout)

    self.__defaults = {
      "PPTX_Obj": None,
      "image_per_col": 4,
      "image_per_row": 4,

      "image_spacing": 0.25,

      "image_width": Inches(3),
      "image_height": Inches(2),

      "row_index": 0,
      "col_index": 0,

      "layout": self.layout,
      "slide": self.slide,
    }

    BaseUtility.update_attributes(self, kwargs, self.__defaults)

    self.image_width = Inches((self.PPTX_Obj.slide_width.inches / self.image_per_col) - self.image_spacing)
    self.image_height = Inches((self.PPTX_Obj.slide_height.inches / self.image_per_row) - self.image_spacing)

  def set_images(self, _image_list):
    for _idx, _img in enumerate(_image_list):
      _left = (self.image_width * self.col_index)  + Inches(self.image_spacing)
      _top = (self.image_height * self.row_index) + Inches(self.image_spacing)
      # _pic_ph = self.slide.shapes.add_picture(_img, _left, _top, self.image_width, self.image_height)
      _pic_ph = self.slide.shapes.add_picture(_img, _left, _top, None, self.image_height) # preserve aspect ratio

      if self.col_index < self.image_per_col -1:
        self.col_index += 1
      else:
        self.row_index += 1
        self.col_index = 0

      if self.row_index < self.image_per_row:
        ...
      else:
        self.slide = self.PPTX_Obj.slides.add_slide(self.layout)
        self.row_index = 0

  def save(self, path):
    self.PPTX_Obj.save(path)
