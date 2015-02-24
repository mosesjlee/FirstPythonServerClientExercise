"""
Simple Client side app. 
"""

import sys, socket

#create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect the socket to the server port
server_address = ('localhost', 8000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
	#on the server side it will look for a file named
	#moses.json

	#check for response

	while True:
		message = raw_input('Type in the name of file or 0 to exit: ')

		#exit if user wants to
		if message == '0':
			break

		print >>sys.stderr, 'Looking for %s...' % message

		sock.sendall(message)

		#receiving flag status
		data = sock.recv(16)
		if data == '0':
			print >>sys.stderr, 'File "%s".json does not exist' % message
			continue
		else:
			while True:

				#check to see if field is valid
				field = raw_input('Type in the field to view or edit or 0 to view a different file: ')

				#sending the field to look for
				print >>sys.stderr, 'Looking for field...'
				sock.sendall(field)
				if field == '0':
					break

				#waiting for server to validate field
				isValid = sock.recv(16)
				if isValid == '0':
					print >>sys.stderr, 'Field "%s" is not a valid field' % field
					continue

				#To see if a the user wants to query information or write information
				#1 to read 0 to write
				print('Enter r to read or w to write')
				readOrWrite = raw_input('Anything Else to exit ')
				if readOrWrite == 'r':
					sock.sendall('r')
					msg = sock.recv(64)
					print >>sys.stderr, '%s is' % field 
					print >>sys.stderr, '%s' % msg
					continue;
					
				elif readOrWrite == 'w':
					sock.sendall('w')
					print 'Type in the value to put in the field'
					value = raw_input('Just hitting return is equivalent to deleting the field: ')
					sock.sendall(value)
					continue
				else:
					sock.sendall(readOrWrite)
					print 'Good Bye'
					break;

finally:
	print >>sys.stderr , 'closing socket'
	sock.close()
