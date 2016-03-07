#encoding: utf-8

from lib.utils.FileUtils import FileUtils

class PassParser(object):
	"""docstring for PassParser"""
	def __init__(self, dicfile):
		super(PassParser, self).__init__()
		self.dicfile = dicfile

	def parser(self):
		tmp_dict = []
		for line in FileUtils.getLines(self.dicfile):
			#line的格式为admin:admin
			tmp_dict.append(line)
		return tmp_dict
