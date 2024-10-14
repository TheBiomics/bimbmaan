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
