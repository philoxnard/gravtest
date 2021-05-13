
# TODO For the Web

This file contains things we should be aware of but may not necessarily have a home or need to be assigned an issue yet.

1) 
A cookie associated with a cross-site resource at https://www.tailwindapp.com/ was set without the `SameSite` attribute. A future release of Chrome will only deliver cookies with cross-site requests if they are set with `SameSite=None` and `Secure`. You can review cookies in developer tools under Application>Storage>Cookies and see more details at https://www.chromestatus.com/feature/5088147346030592 and https://www.chromestatus.com/feature/5633521622188032.
