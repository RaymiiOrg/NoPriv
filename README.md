# NoPriv.py - HTML5 IMAP email backup

NoPriv.py is a python script to backup any IMAP capable email account to a HTML archive, nicely browsable, instead of weird folders (Maildir), one huge file (mbox), only needing a web browser to view (thunderbird) and no propritary code, so you can make sure I won't steal your password.

### Demo

[Click here for a demo](http://sparklingnetwork.nl/nopriv/index.html)

### Screenshots

#### Running the program
<a href = "http://i.imgur.com/8Uvrk.png"><img src="http://i.imgur.com/8Uvrk.png" width=400 height=400 /></a>

#### Index page
<a href = 'http://i.imgur.com/jFLX7.png'><img src="http://i.imgur.com/jFLX7.png" width=400 height=400 /></a>

#### Folder Overview page 
<a href = "http://i.imgur.com/BKHln.jpg"><img src="http://i.imgur.com/BKHln.jpg" width=400 height=400 /></a>

#### Email itself
<a href = "http://imgur.com/W18fR"><img src="http://i.imgur.com/W18fR.png" width=400 height=400 /></a>

#### Attachments
<a href="http://i.imgur.com/YA4wZ.jpg"><img src="http://i.imgur.com/YA4wZ.jpg" width=400 height=400 /></a>

#### Command Line Client (links2):
<a href="http://i.imgur.com/gt9nH.png"><img src="http://i.imgur.com/gt9nH.png" width=400 height=400 /></a>

### Features

- Works with any IMAP/IMAPS account
- Supports multiple IMAP folders
- Supports HTML email
- Supports TEXT email
- Supports MULTIPART email
- Saves attachments
- Backups to HTML files for easy browsing
- Small HTML files can be backed up to external medium more easily, and can be sent over the internet more easily.

### Changelog

New in version 2:

- Support for multiple IMAP folders
- Index page is generated
- Pages have menu now.
- On running it shows all available IMAP folders.

### Usage

1. Clone the repository:

    git clone git://github.com/RaymiiOrg/NoPriv.git

2. Set up your login details, imap server and ssl:

Open `nopriv.py` in a text editor and edit the following variables (example filled in for gmail):

    IMAPSERVER = "imap.gmail.com"
    IMAPLOGIN = "janeway@gmail.com"
    IMAPPASSWORD = "Voyager1"
    IMAPFOLDER = ["[Gmail]/Sent Mail", "INBOX", "[Gmail]/Starred", "Captains_Log", "Important"]
    ssl = True

(Mind the capital on ssl, `True`/`False`, not `true`/`false`). 

If you use gmail and want to backup all your email, use the "[Gmail]/All Mail" folder. It might be named different if you use another locale, for me with a Dutch gmail account it is named "[Gmail]/Alle Berichten".

If you only want to backup one folder, use something like this: `IMAPFOLDER = ["Folder"]`. 

3. Execute the script:

    python ./nopriv.py

4. Browse the generated backup:

Open the file `index.html` in your browser. There are all your folders and emails.

If you only have a console, it works just fine in Links2 (see above screenshot):
    
    links2 ./index.html


### Requirements

Python 2.7

Running debian 6 which has python 2.6.6? Execute the following steps to install python 2.7:

    sudo apt-get install python-pip

    sudo pip install pythonbrew

    pythonbrew_install

    source "$HOME/.pythonbrew/etc/bashrc"

    pythonbrew install 2.7.3

    pythonbrew use 2.7.3

### Known issues

- Does not work with python3 (Feel free to port/fix it.)
- Does not handle all charsets. Works best with utf-8 and ascii.
- Might create an extra index file (example: you have 46 pages, there are 47 in the folder).
- Some non-rfc compliant emails will look weird, or have weird subjects etc. 
- No search function.
- Not able to change default sorting (latest first).

### More Info:

[https://raymii.org/s/software/Nopriv.py.html](https://raymii.org/s/software/Nopriv.py.html)  
[https://github.com/RaymiiOrg/NoPriv](https://github.com/RaymiiOrg/NoPriv)