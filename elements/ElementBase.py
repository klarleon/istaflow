# coding: utf-8
class ElementBase (object):

	def get_input(self):
		raise NotImplementedError("Class %s doesn't implement get_input()" % (self.__class__.__name__))

	def get_output(self):
		raise NotImplementedError("Class %s doesn't implement get_output()" % (self.__class__.__name__))

	def get_params(self):
		raise NotImplementedError("Class %s doesn't implement get_params()" % (self.__class__.__name__))
		
	def set_params(self):
		raise NotImplementedError("Class %s doesn't implement set_params()" % (self.__class__.__name__))
	
	def run(self):
		raise NotImplementedError("Class %s doesn't implement run()" % (self.__class__.__name__))