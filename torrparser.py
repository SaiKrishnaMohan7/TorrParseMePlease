#! usr/bin/env python
from datetime import datetime
from glob import glob
import os
import sys
import string

from wrap_torr import WrapTorr

class TorrParseMePlease(object):
  
  # Dict identifying start and end of DS
  IDENTIFIERS = {
    'int': 'i',
    'string_sep': ':',
    'dict': 'd',
    'dict_kv_sep': ': ',
    'list': 'l',
    'list_sep': ', ',
    'common_end': 'e'
  }

  # Silent exceptions/error toggle
  silence = False

  def __init__(self, file_path, silence=False):

    self.silence = silence

    if not file_path or not os.path.exists(file_path):
      raise IOError('No File at location %r' % (file_path,))

    with open(file_path) as torrent_file:
      file_content = torrent_file.read()
      self.torr_str = WrapTorr(file_content, silence)
    
    self.parsed_content = self._parse_torr_file()

  def get_tracking_url(self):
    return self.parsed_content.get('announce')
    
  def get_creation_date(self, time_format='iso'): 
    time_stamp = self.parsed_content.get('creation date')

    if time_stamp:
      time_stamp = datetime.utcfromtimestamp(time_stamp)

    if time_format == 'iso':
      return time_stamp.isoformat()
    else:
      return time_stamp
    
  def get_client(self):
    return self.parsed_content.get('created by')
    
  def get_file_details(self):
    parsed_files_info = {}

    # 'info' should be present in all torrent files.
    files_info = self.parsed_content.get('info', {})

    # multiple-file torrent
    multiple_files_info = files_info.get('files', [])

    parsed_files_info.update(
      { os.path.sep.join(multifile_info.get('path')):
        multifile_info.get('length')
        for multifile_info in multiple_files_info })

    # single file torrent
    if not parsed_files_info:
      name = files_info.get('name')
      if name:
        parsed_files_info[name] = files_info.get('length')
    
      # some single-file torrents (incorrectly) have their details
      # in the parsed_content scope (eg. uTorrent/3200)
      # only use this if no other fields have been present
    if not parsed_files_info:
      name = self.parsed_content.get('name')
      if name:
        parsed_files_info[name] = self.parsed_content.get('length')

    parsed_files_info_lst = [ (k, v) for k, v in parsed_files_info.items() ]

    return parsed_files_info_lst
    
  def _parse_torr_file(self):
    parsed_char = self.torr_str.current()

    if not parsed_char:
      return
    
    if parsed_char == self.IDENTIFIERS['common_end']:
      return
    
    elif parsed_char == self.IDENTIFIERS['int']:
      return self.torr_str.parse_int()
    
    elif parsed_char in string.digits:
      self.torr_str.move()
      return self.torr_str.parse_str()
    
    elif parsed_char == self.IDENTIFIERS['dict']:
      parsed_dict = {}
      while True:
        dict_key = self._parse_torr_file()
        if not dict_key:
            break
        dict_value = self._parse_torr_file()
        parsed_dict.setdefault(dict_key, dict_value)

      return parsed_dict

    elif parsed_char == self.IDENTIFIERS['list']:
      parsed_list=[]
      while True:
        list_item = self._parse_torr_file()
        if not list_item:
          break
        parsed_list.append(list_item)

      return parsed_list
  

if __name__ == '__main__':
    
  if len(sys.argv) > 1:
    torrent_files = sys.argv[1:]
    for torrent_file in torrent_files:
        if os.path.exists(torrent_file):
          print 'Parsing file {}'.format(torrent_file)
        else:
          sys.exit('Unable to find file {}'.format(torrent_file))

  for torrent_file in torrent_files:
    tp = TorrParseMePlease(torrent_file)
    print
    print 'File Name: ' + torrent_file
    print 'Tracker URL: ' + tp.get_tracking_url()
    print 'Created Date: ' + tp.get_creation_date()
    print 'Client Name: ' + tp.get_client()
    print 'File Details: ' + str(tp.get_file_details()) + '\n'