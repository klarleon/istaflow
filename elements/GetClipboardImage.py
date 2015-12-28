# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
import clipboard

class GetClipboardImage(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = None
		self.setup_params()
	
	def setup_params(self):
		pass
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return None
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'image'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = []):
		self.params = params
		
	def get_description(self):
		 return 'This gets the an image from the system clipboard"'
	
	def get_title(self):
		return 'Get Clipboard Image'
		
	def get_icon(self):
		return 'iob:image_32'
		
	def get_category(self):
		return 'Image'
	
	def run(self):
		self.status = 'complete'
		img = clipboard.get_image()
		ev = ElementValue(type=self.get_output_type(),value=img)
		return ev