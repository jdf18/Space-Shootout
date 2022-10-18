from time import time

class Time:
	start_time = time()
	@staticmethod
	def time():
		return time()

def createPrintCallback(message):
	def callback(*args):
		print(message)
	return callback