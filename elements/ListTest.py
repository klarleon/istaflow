# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

class ListTest(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = None
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		pass
	
	def setup_params(self):
		pass
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return None
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'string'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return ''
	
	def get_title(self):
		return 'List Test'
		
	def get_icon(self):
		return 'iob:alert_32'
		
	def get_category(self):
		return 'Test'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		return ElementValue(type='string', value=['test','234','qwerty'])
