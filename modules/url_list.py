import logging

class UrlList(object):
  def __init__(self, urls):
    self.__urls = urls
    self.__decorated_classes = []
  def build_url_list(self):
    def inject_urls(cls):
      if cls in self.__decorated_classes:
        return
      self.__decorated_classes.append(cls)
      old_init = cls.__init__
      def __init__(s):
        old_init(s)
        s.set_template_value('urls', self)
      cls.__init__ = __init__

    return_list = []
    for section_key in self.__urls:
      section = self.__urls[section_key]
      base_url = section['base_url'][0]
      if section['base_url'][1] is not None:
        inject_urls(section['base_url'][1])
        return_list.append(section['base_url'])
      for subsection in ['pages', 'right-pages', 'actions']:
        for page in section[subsection]:
          inject_urls(page[2])
          return_list.append((base_url + page[1], page[2]))
    return return_list
  
  def get_section_name(self, path):
    for section_key in self.__urls:
      section = self.__urls[section_key]
      base_url = section['base_url'][0]
      if path == base_url:
        return ''
      for subsection in ['pages', 'right-pages', 'actions']:
        for page in section[subsection]:
          if path == base_url + page[1]:
            return section_key
    return None
    
  def make_links(self, section, subsections):
    base_url = section['base_url'][0]
    return_list = []
    for subsection in subsections:
      for page in section[subsection]:
        return_list.append({'path':base_url + page[1], 'name':page[0]})
    
    return return_list


  def get_links(self, section):
    if section not in self.__urls:
      return []
    
    return self.make_links(self.__urls[section], ['pages', 'right-pages'])


  def get_left_links(self, section):
    if section not in self.__urls:
      return []
    
    return self.make_links(self.__urls[section], ['pages'])

  def get_right_links(self, section):
    if section not in self.__urls:
      return []
    
    return self.make_links(self.__urls[section], ['right-pages'])
