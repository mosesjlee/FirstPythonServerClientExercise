"""
this script cannot be run a true server client system
this is only to demonstrate the basic functionality
of client and server side application interaction

This script does not allow message sizes beyond 64 for 
some of the messages being passed through
"""

import socket
import sys
import json

"""
Define some helper methods to open, modify and close the json file
"""
#opens the json file
#returns the json data if file is found
#returns empty list if not
def openJSONFile(fileName):
	jsonData = []
	try:
		jsonFile = open(fileName, 'rw')
		jsonData = json.load(jsonFile)
		return jsonData
	except IOError as e:
		return [] 

#writes the new json information back to the json file
def writeAndCloseJSONFile(fileName, data):
	print >>sys.stderr, 'File name to close %s' % fileName
	print data
	with open(fileName, 'wb') as outfile:
		json.dump(data, outfile)
	outfile.close()

#check to see if field exists
def checkValidField(json_fields, key):
	if key in json_fields:
		return True
	else:
		return False

"""
Actually Starting the server
"""

#create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind the socket
server_address = ('localhost', 8000)
print >>sys.stderr, 'starting up simple server/client on %s on port %s' % server_address
sock.bind(server_address)

#listen for any connection
sock.listen(1)

#sort of global variables
jsonInfo = []
fileName = ""

#listen forever
while True:
	print 'waiting for connection'
	connection, client_address = sock.accept()

	try:
		print 'connection from', client_address

		while True:
			print 'Waiting for client to respond'
			print 'Waiting for the file name'
			data = connection.recv(64)
		
			#client shuts down program, the server will now go back into
			#forever listening
			if data == '0':
				break

			if data:
				fileName = data
				print >>sys.stderr, 'Looking for %s' % fileName
				jsonInfo = openJSONFile(fileName)

				#if jsonInfo length 0 the file does not exist
				if len(jsonInfo) == 0:
					print 'File Does not exist'
					connection.sendall('0')
					continue
				else:
					#informing that the file is found
					connection.sendall('1')
					print 'Found file'
					
					#listen for client inputs
					while True:
						key = connection.recv(64)

						#client initiated exit
						if key == '0':
							break

						print >>sys.stderr, 'Looking for the %s field' % key
						field = key
						
						#check to see if field is valid
						isValid = checkValidField(jsonInfo, field)

						if isValid != True:
							print >>sys.stderr, 'Field not found!'
							connection.sendall('0')
							continue

						#informing that the field is found
						print >>sys.stderr, '%s field is found' % field
						connection.sendall('1')

						#checking to see if user wants to read or write to file
						#r to read w to write
						print 'Checking to see if user wants to read or write or to exit'
						readOrWrite = connection.recv(16)

						if readOrWrite == 'r':
							print 'Chose to read'
							connection.sendall(jsonInfo[field])
							continue
						elif readOrWrite == 'w':
							print 'Chose to Write'
							value = connection.recv(64)
							print >>sys.stderr, 'Changing the field value with %s' % value
							jsonInfo[field] = value
							if len(jsonInfo) > 0:
								writeAndCloseJSONFile(fileName, jsonInfo)
							continue
						else:
							print 'Chose to do break out'
							break
			else:
				print >>sys.stderr, 'no mare data from', client_address
				break

	except TypeError as e:
			print 'closing connection due to client quitting'
			connection.close()

	finally:
		connection.close()
