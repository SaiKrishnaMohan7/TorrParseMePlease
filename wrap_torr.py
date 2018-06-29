from StringIO import StringIO
from custom_exceptions import TorrParsingException
import string


class WrapTorr(object):
  delim = {
    'int': 'i',
    'string_sep': ':',
    'common_end': 'e'
    }
  silence = False
  
  def __init__(self, torr, silence=False):
    self.torr = StringIO(torr)
    self.curr = None
    self.silence = silence

  def current(self):
    self.curr = self.torr.read(1)
    return self.torr.read(1)
    
  def move(self, pos=-1, mode=1):
    self.torr.seek(pos, mode)
    
  def parse_str(self):
    length = self._parse_num(delim=self.delim['string_sep'])

    if not length:
        if self.silence:
            return ''
        raise TorrParsingException('Empty String at %d' % self.torr.pos)

    return self.torr.read(length)
  
  def parse_int(self):
    self.move()
    if self.current() != self.delim['int']:
      raise TorrParsingException('Parsing for int but found %s at %d, expected - %s' % (self.current(), self.torr.pos, self.delim['int']))

    return self._parse_num(delim=self.delim['common_end']) 
  
  def _parse_num(self, delim): 
    parsed_int = ''
    while True:
        parsed_int_char = self.current()
        if parsed_int_char not in string.digits:
            if parsed_int_char != delim:
                raise TorrParsingException('Invalid character %s found after parsing an integer (%s expected) at position %d.' %
                          (parsed_int_char, delim, self.torr.pos))
            else:
                break
        parsed_int += parsed_int_char

    return int(parsed_int)