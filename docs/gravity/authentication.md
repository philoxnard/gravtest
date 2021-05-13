
Gravity Authentication System and Procedure
-------------------------------------------

### Registration

When the user wishes to register themselves into the system, they must go to the registration page and submit a request to the server to create an account.  The cient side code to submit the registration currently lives in the public/js/login.js file.

The registration goes through the API and takes a JSON object with a user_info object to do the registration.

When the registration is complete, a user object will appear in the config/users.json file.

### User Login

When a user wishes to login to the system, they must already have registered and a user object must be present in
the users.json file.  Future implemenations of this system will also include a database instead of the users.json file.

To login to the system, a user must sent a JSON login message to the server with a message that matches the message schema.

When the login is successful, the client will receive a message back that containns a JSON Web token. We typically just refer to this as a token in this documentation and throughout the code.  For any future request that requires a login page, the user must submit this token in the header.

On the server-side, the tokens are stored in a file called tokens.json.  This file contains a dictionary of the tokkens and the username (or email addresss) that the token is associated with.

### User Logout

A user remains logged into the system as long as their token is valid (it remains in the token.json file). When the user wishes to logout, they must submit a request to the server and the server must find their token in the token.json file and remove it.

After the token has been removed from the tokens.json file, their token is now invalid and they must login again to receive a new token to continue interacting with the system.