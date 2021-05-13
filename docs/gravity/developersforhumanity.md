
Developer Coding Instuctions and Best Practices
===============================================

This document defines the best practices to use when developing software and working with as team as this project grows over time.

This document will be contiually updated as the community works together to determine how to work together to develop this opensource project.

Be Postive, Help Others, Create Great Things
--------------------------------------------

This project is designed out of love and #unity.  By contributing to this project, you agree that you are now are part of a global community of incredible people trying to make the world a better place, you are now part of the #developersforhumanity community.  We are here to create #softwareforhumanity.

Within this community, we support each other to realize what we can create and build together.  We use open source principles to give to the world, so that we can also use this code for our own projects.


Develop as if you were on an Airplane without Wi-Fi
---------------------------------------------------

The requirements for this project are that the Gravity web server shall work without any access to the open global internet.  This means that any dependencies that are necessary for the project to run must be something that can be installed on the host operating system though the package manager.

On the client side though, this is a bit more of a challenge.  This means that any Javascript libraries will need to be checked into this code base directly.  Now it is realized that if we are running this on the global internet, you may want to pull Javascript files from CDN's.  This fine except this should be a "production" switch and should not be the default operation.  

Anything that is required for the server to run on your local machine should be self contained within this repository or other Git repositorys locally.  Do not depend on the global internet for obtaining files.

This means you should test your code too by turning off the Wi-Fi of your laptop and make sure the code still runs as you would expect.  Remember sometimes that your browser caches data, so make sure you do a full refresh or open a new browser to test.

Also make sure your code works across a local area network (LAN).  Find the IP address of the computer that is hosting the Gravity Server, type that IP address into a client on another device on your local LAN and make sure the behavior is the same across the network.

Git
---

This project uses Git as it's version control system.  The Git is repository is hosted on a public Gitlab respository.  We use Gitlab's own issue tracking system to manage interaction among developers on this project.

### Branch Management

Any development branches you are working with should be prepended by your Gitlab username. For instance, my Gitlab username is @pfarrell, therefore if I'm working on a feature of user management, my branch may be named pfarrell/user_management.

The master branch is the branch that defines the currently approved version of the code base. The master branch is maintained by the owner of the project and other developers should not be pushing or making changes to the master branch.

The "dev" branch is the official testing and development branch of all the merged code across all developers.  Once a developer feels their code is ready to be tested by the full community, they will submit their branch to the dev branch.  Once the dev branch has been validated and all code is approved, the master branch will move up to the approved version of the dev branch.

### Commit Management

The Git history within this project should remain as linear and streamlined as possible.  Any commits that will be moved into the dev or master branch should be complete commits.  This means that if you are working on a feature and the implementation of that feature on your development branch spans multiple commits, those commits should be squashed together before you actually submit the code for review or a merge request.

The requires are that once a commit is merged into the mainline, a developer should be able to check out any commit in the history and the code should work properly based on the feature set that is currently there.  There should be no commits in the mainline where the code is essentially "broken".

By keeping the history clean and having each commit be a full change where the baseline code works properly, this saves time on both the commits, the maintainer of the project, and any new individuals that wish to download the code and run it for the first time without understand it fully.

### What gets included in commits

Please do not commit any large image files or items that you don't plan to incorporate into the mainline.  This will take up space for everyone as they clone the repository.  Be mindful of what should be visible by others and what should remain on your local machine.

Project Dependencies
--------------------

This code is designed from the ground up to reduce the amount of other dependencies as much as possible.  Developers should not take opensource code from other projects and incorporate that code here unless there is good reason to do so.  All dependencies should be offical python modules that can be downloaded from the official package managers such as "pip".

Javascript is a separate issue and is addressed below as many of these files will need to be stored within this repo directly.

There will be cases where code must be included in this repository directly, as mentioned by the Javascipt case. Each dependency will be a case-by-case issue and the maintainer of the project will determine what gets included in the project.


