Preface:
Sorry about the code. I tried to comment as best as possible to help follow my logic. This is my first time experience on python server/client based applications and json objects. I learned everything on the go. It does what the challenge asks: you can manipulate, delete, and read data from the json file by querying the server for various information.

ASSUMPTIONS:
-simple json objects i.e. no tuples or lists within json objects
-message being passed over network is less than 64 characters
-user cannot delete fields but can only modify the values and put in empty values
-this will only work over an adhoc network. NOT to be used over a actual server/client
-demonstrates simple message passing with only one value at a time at user request to manipulate json fields on the server
-the file already exists on server, the server app will open, extract, and modify if needed
-runs 1 client instance at a time

USAGE:
Always start the server first. The server will create the socket and the local address for the client to connect to.

Right now because this is a simple application you can only edit one field at a time. For example here are the inputs that the app expects from the client side:

-Type in the name of file or 0 to exit: (user input for a file name that may exist in the server)

-Type in the field to view or edit or 0 to view a different file: (user input of the field the user wants to query information about or modify)

-Type in the value to put in the field
Just hitting return is equivalent to deleting the field: (user input to change or delete the value of the field)

There will be various messages that deal with file not found, field not found, and other invalid operations.


So in this instance there is a file named “moses.json” which contains the json object. The script will prompt user to type in name and will relay the message to server and the server will check to see if the file exists. If it exists it will open and retrieve the json objects and prompts the client to enter the field that they would like to modify. The user then will enter in the field to modify. If the field exists it will ask to enter in the value to modify the field with. 

IMPLEMENTATION:

server:
-has access to .json files
-has methods to alter and modify .json files
-checks for file existence, field validity, and permissible operations

client:
-has no access to .json files
-has methods to query and requests to modify fields in the .json files on the server
-has methods to listen to the server to check if user inputs are valid

INFRASTRUCTURE:
server:
-all json files live here
-sets up a local host

client:
-only client relevant code reside here

ALGORITHM:
server:
1. start up sockets
2. create unique server address
3. bind the address to the network
4. While: Wait and listen forever for any client connections
5. Once established connection with client:
	a. receive file name and check for file existence
	b. if file exists open file and ask which field to view or edit
	c. check to see if it is a valid field, if field not valid exit
		and ask for another file name
	d. if valid field ask if to read or write to that field
	e. if read, send the value of the field to client, else if write
		wait for user input value, else exit and ask for the
		next file name
6. Keyboard interrupt to exit the server application

client:
1. start up sockets
2. look for the server address
3. Attempt to make connection
4. once connection is made ask for file to query and edit
	a. input file name, server will let us know if file exists or not
		if the user inputs 0 exit client
	b. if file exists, ask for the field to view or edit, 
		if not ask for another filename.
	c. if field exists ask to read or write or to exit
		i. if read, wait for server to send the value of
		   the respective field
		ii. if write, send the server the value to replace
		   the current value
		iii. else exit and ask for the next file to view/edit



NOT IMPLEMENTED:

-sending over lists
-sending over tuples
-content error checking i.e. is name in valid form, is address in valid form
-Strings longer than 64 characters
-more complex json objects
-smooth way to exit the client
-allowing multiple client connections
 