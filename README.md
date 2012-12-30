### NoPriv.py - HTML5 IMAP email backup

NoPriv.py is a python script to backup any IMAP capable email account to a HTML archive, nicely browsable, instead of weird folders (Maildir), one huge file (mbox), only needing a web browser to view (thunderbird) and no propritary code, so you can make sure I won't steal your password.

### Demo

[Click here for a demo](http://sparklingnetwork.nl/nopriv/email-report-1.html)

### Screenshots

#### Running the program
<a href="http://i.imgur.com/iH330.png"><img src="http://i.imgur.com/iH330.png" width=400 height=400 /></a>

#### Overview page 
<a href="http://i.imgur.com/5TvtU.jpg"><img src="http://i.imgur.com/5TvtU.jpg" width=400 height=400 /></a>

#### Email itself
<a href = "http://i.imgur.com/enrnBh.png"><img src="http://i.imgur.com/enrnBh.png" width=400 height=400 /></a>

#### Attachments
<a href="http://i.imgur.com/YA4wZ.jpg"><img src="http://i.imgur.com/YA4wZ.jpg" width=400 height=400 /></a>

#### Command Line Client (links2):
<a href="http://i.imgur.com/gt9nH.png"><img src="http://i.imgur.com/gt9nH.png" width=400 height=400 /></a>

### Features

- Works with any IMAP/IMAPS account
- Supports HTML email
- Supports TEXT email
- Supports MULTIPART email
- Saves attachments
- Backups to HTML files for easy browsing
- Small HTML files can be backed up to external medium more easily, and can be sent over the internet more easily.

### Usage

1. Clone the repository:

    git clone git://github.com/RaymiiOrg/NoPriv.git

2. Set up your login details, imap server and ssl:

Open the file in a text editor and edit the following variables (example filled in for gmail):

    IMAPSERVER = "imap.gmail.com"
    IMAPLOGIN = "janeway@gmail.com"
    IMAPPASSWORD = "voyager1"
    IMAPFOLDER = "[Gmail]/All Mail"
    ssl = True

(Mind the capital on ssl, `True`/`False`, not `true`/`false`). 

Some example IMAP folders:

    IMAPFOLDER = "INBOX"
    IMAPFOLDER = "[Gmail]/Alle berichten"
    IMAPFOLDER = "[Gmail]/Sent Mail"
    IMAPFOLDER = "My_OWN_Folder"

3. Execute the script:

    python ./nopriv.py

4. Browse the generated backup:

Open the file `email-report-1.html` in your browser. There is all your email.

If you only have a console, it works just fine in Links2 (see above screenshot):
    
    links2 ./email-report-1.html


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