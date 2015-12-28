# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
import photos

class SaveImagetoCameraRoll(ElementBase):
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
		return 'image'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return None
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = []):
		self.params = params
		
	def get_description(self):
		return 'Saves input image to Camera Roll'
	
	def get_title(self):
		return 'Save Image to Camera Roll'
		
	def get_icon(self):
		return 'iob:camera_32'
		
	def get_category(self):
		return 'Image'

	def run(self, input):
		photos.save_image(input)
		self.status = 'complete'