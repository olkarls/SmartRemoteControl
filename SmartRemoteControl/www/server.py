import socket
import time

from flask import *

import config


# TCP port the Yun console listens for connections on.
CONSOLE_PORT = 6571

# Create flask application.
app = Flask(__name__)

# Get activity configuration.
remotes = config.get_commands()

@app.route('/')
def root():
	return render_template('index.html', remotes=remotes)

@app.route('/<string:name>/<string:command>', methods=['POST'])
def send_command(name, command):
	code = None

	for remote in remotes['remotes']:
		if remote['name'] == name:
			for comm in remote['commands']:
				if comm['name'] == command:
					code = comm['code']

	if code is None:
		print 'code is None'
		abort(404)
	else:
		print 'code: ' + code
		console = socket.create_connection(('localhost', CONSOLE_PORT))
		console.sendall(code + '\n')
		time.sleep(0.5)
		console.shutdown(socket.SHUT_RDWR)
		console.close()
	return 'OK'


# @app.route('/activity/<int:index>', methods=['POST'])
# def activity(index):
# 	# Connect to the console socket.
# 	console = socket.create_connection(('localhost', CONSOLE_PORT))
# 	# Send all the codes in order that are associated with the activity.
# 	for code in activities[index].get('codes', []):
# 		console.sendall(code + '\n')
# 		# Wait ~500 milliseconds between codes.
# 		time.sleep(0.5)
# 	console.shutdown(socket.SHUT_RDWR)
# 	console.close()
# 	return 'OK'


if __name__ == '__main__':
	# Create a server listening for external connections on the default
	# port 5000.  Enable debug mode for better error messages and live
	# reloading of the server on changes.  Also make the server threaded
	# so multiple connections can be processed at once (very important
	# for using server sent events).
	app.run(host='0.0.0.0', debug=True, threaded=True)
