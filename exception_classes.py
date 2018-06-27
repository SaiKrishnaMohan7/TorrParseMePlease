#! usr/bin/env python

class TorrParsingException(Exception):
  """Custom exception class raised or thrown when there's an error with parsing .torrent files"""

  def __init__(self, err):
    Exception.__init__(self)
    self.err = err
  
  def __str__(self):
    return self.err