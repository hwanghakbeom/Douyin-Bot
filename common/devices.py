from ppadb.client import Client as AdbClient

class auto_device(device_id):
	def __init__(self):
		try:
			client = AdbClient(host="127.0.0.1", port=5037)
			device = client.device(device_id)
		except OSError:
			exit(1)

	def get_screen(self):
		return self.device.screencap()


	def swipe(self):
		self.device.run("shell swippe ~")
		return