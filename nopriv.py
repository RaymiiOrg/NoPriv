#!/usr/bin/env python
import imaplib
import email
from email.header import decode_header
import time
import re
from random import choice
import os
import base64
import cgi
import sys
from quopri import decodestring

###########################
# Do not edit above here  #
###########################

IMAPSERVER = ""
IMAPLOGIN = ""
IMAPPASSWORD = ""
IMAPFOLDER = "INBOX"
ssl = True

# IMAPFOLDER = "INBOX"
# IMAPFOLDER = "[Gmail]/Alle berichten"
# IMAPFOLDER = "[Gmail]/Sent Mail"
# IMAPFOLDER = "[Gmail]/All Mail"

###########################
# Do not edit below here  #
###########################
enable_html = True
if ssl is True:
    mail = imaplib.IMAP4_SSL(IMAPSERVER)
if ssl is False:
    mail = imaplib.IMAP4(IMAPSERVER)
mail.login(IMAPLOGIN, IMAPPASSWORD)
mail.select(IMAPFOLDER)
result, data = mail.search(None, "ALL")
ids = data[0]
id_list = ids.split()
breakOut = False




def returnHeader(title, inclocation="inc", layout=1):
    if layout is 1:
        response = """
<html>
    <head>
        <title>%s</title>
        <script type="text/javascript" src="%s/js/jquery.1.7.2.min.js"></script>
        <script type="text/javascript" src="%s/js/prettify.js"></script>
        <script type="text/javascript" src="%s/js/kickstart.js"></script>
        <link rel="stylesheet" type="text/css" href="%s/css/kickstart.css" media="all" />
        <link rel="stylesheet" type="text/css" href="%s/css/style.css" media="all" />
    </head>
            <body>
                <div id="wrap" class="clearfix">
                    <div class="col_12">
                        <table class=\"striped tight\" style=\"{text-align:left;}\">
                           <thead>
                           <tr>
                               <th>#</th>
                               <th>From</th>
                               <th>To</th>
                               <th>Subject</th>
                                <th>Date</th>
                               </tr>
                           </thead>
                           <tbody>
        """ % (title, inclocation, inclocation, inclocation, inclocation, inclocation)
    elif layout is 2:
        response = """
                <html>
                <head>
                    <title>%s</title>
                    <script type="text/javascript" src="%s/js/jquery.min.js"></script>
                    <script type="text/javascript" src="%s/js/prettify.js"></script>
                    <script type="text/javascript" src="%s/js/kickstart.js"></script>
                    <link rel="stylesheet" type="text/css" href="%s/css/kickstart.css" media="all" />
                    <link rel="stylesheet" type="text/css" href="%s/css/style.css" media="all" />
            </head>
            <body>
                <div id="wrap" class="clearfix">
                    <div class="col_12">
        """ % (title, inclocation, inclocation, inclocation, inclocation, inclocation)
    return response


def returnFooter():
    response = """
                    </div>
                <div class="footer">
                <hr />
                <center>
                Email backup made by <a href="https://raymii.org/s/software/Nopriv.py.html">NoPriv.py from Raymii.org</a>
                </center>
                </div>
            </body>
        </html>
    """
    return response


def printQuote():
    quotes = ['Come on, shut off that damn alarm and I promise I\'ll never violate you again.', 'I\'ve become romantically involved with a hologram. If that\'s possible.', 'Listen to me very carefully because I\'m only going to say this once. Coffee - black.', 'Computer, prepare to eject the warp core - authorization Torres omega five nine three!', 'The procedure is quite simple. I\'ll drill an opening into your skull percisely two milimeters in diameter and then use a neuralyte probe to extract a sample of your parietal lobe weighing approximately one gram']
    return choice(quotes)
    
class DecodeError(Exception):
    pass
    
def decode_string(string):
    for charset in ("utf-8", 'latin-1', 'iso-8859-1', 'us-ascii', 'windows-1252','us-ascii'):
        try:
            return cgi.escape(unicode(string, charset)).encode('ascii', 'xmlcharrefreplace')
        except Exception:
            continue
    raise DecodeError("Could not decode string")

def return_message(message_id):
    global mail
    result, data = mail.fetch(str(message_id), "(RFC822)")
    raw_email = data[0][1]
    email_message = email.message_from_string(str(raw_email))
    decoded_subject = decode_header(email_message['Subject'])[0][0]
    subject_encoding = decode_header(email_message['Subject'])[0][1]
    if subject_encoding:
        email_subject = cgi.escape(unicode(decoded_subject, subject_encoding)).encode('ascii', 'xmlcharrefreplace')
    else:
        try:
            email_subject = decode_string(decoded_subject)
        except DecodeError:
            email_subject = "Error decoding subject."
    if not email_subject:
        email_subject = "No Subject"
    
    decoded_to = decode_header(email_message['To'])[0][0]
    to_encoding = decode_header(email_message['To'])[0][1]
    if to_encoding:
        email_to = cgi.escape(unicode(decoded_to, to_encoding)).encode('ascii', 'xmlcharrefreplace')
    else:
        try:
             email_to = decode_string(decoded_to)
        except DecodeError:
            email_to = "Error decoding Receiver."
            print "Error decoding Receiver"
    if not email_to:
        email_to = "No Receiver"

    content_type = decode_header(str(email_message['Content-Transfer-Encoding']))
   

    decoded_from = decode_header(email_message['From'])[0][0]
    from_encoding = decode_header(email_message['From'])[0][1]
    if from_encoding:
        email_from = cgi.escape(unicode(decoded_from, from_encoding)).encode('ascii', 'xmlcharrefreplace')
    else:
        try:
            email_from = decode_string(decoded_from)
        except DecodeError:
            email_from = "Error decoding sender address."
            print "Error decoding sender address"
    if not email_from:
        email_from = "No sender."
    term_from = str(decoded_from[0][0])
   
    decoded_contents = ""
    response = {}
    response['attachment'] = False
    response['from'] = str(email_from)
    response['termfrom'] = term_from
    response['to'] = str(email_to)
    response['subject'] = str(email_subject)
    response['termsubject'] = decoded_subject
    try:
        response['date'] = str(time.strftime("%d-%m-%Y %H:%m", email.utils.parsedate(email_message['Date'])))
        attDate = str(time.strftime("%Y/%m/", email.utils.parsedate(email_message['Date'])))
    except TypeError:
        response['date'] = "Error in Date"
        attDate = str("2000/1/")

    response['date2'] = email.utils.parsedate(email_message['Date'])

    contentOfMail = {}
    contentOfMail['text'] = ""
    contentOfMail['html'] = ""

    att_dir = os.path.join(attDate, str(message_id))
    if not os.path.exists(att_dir):
        os.makedirs(str(att_dir))
        print("Creating directory %s for attachments.") % (att_dir)
    fpIndex = open(att_dir + "/index.html", "w")
    fpIndex.write("<html>\n<head>\n<title>Attachments for email " + str(message_id) + "</title>\n</head>\n<body>\n")
    fpIndex.write("<h1>Attachments for email " + str(message_id) + "</h1>\n")
    fpIndex.write("<ul>\n")
    fpIndex.close()

    for part in email_message.walk():
        cType = part.get_content_type()
        charset = part.get_charsets()
        if cType == 'text/plain':
            decoded_contents = part.get_payload(decode=True)
            try:
                if charset[0]:
                    contentOfMail['text'] += cgi.escape(unicode(str(decoded_contents), charset[0])).encode('ascii', 'xmlcharrefreplace')
                else:
                    contentOfMail['text'] += cgi.escape(str(decoded_contents)).encode('ascii', 'xmlcharrefreplace')
            except Exception:
                try:
                    contentOfMail['text'] +=  decode_string(decoded_contents)
                except DecodeError:
                    contentOfMail['text'] += "Error decoding mail contents."
                    print("Error decoding mail contents")
            continue
        elif cType == 'text/html':
            decoded_contents = part.get_payload(decode=True)
            try:
                if charset[0]:
                    contentOfMail['html'] += unicode(str(decoded_contents), charset[0]).encode('ascii', 'xmlcharrefreplace')
                else:
                    contentOfMail['html'] += str(decoded_contents).encode('ascii', 'xmlcharrefreplace')
            except Exception:
                try:
                    contentOfMail['html'] += decode_string(decoded_contents)
                except DecodeError:
                    contentOfMail['html'] += "Error decoding mail contents."
                    print("Error decoding mail contents")

            continue
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') == None:
            continue
        decoded_filename = decode_header(part.get_filename())
        attFileName = re.sub(r'[^.a-zA-Z0-9 :;,\.\?]', "_", str(decoded_filename[0][0]).replace(":", "").replace("/", "").replace("\\", ""))
        
        att_path = os.path.join(attDate, str(message_id), attFileName)
        att_locs = []
        fp = open(att_path, 'wb')
        try:
            fp.write(part.get_payload(decode=True))
            print("Saved attachment \"%s\".") % attFileName 
        except Exception as e:
            fp.write("Error writing attachment: " + str(e) + ".\n")
            print("Error writing attachment: " + str(e) + ".\n")
        fpIndex = open(att_dir + "/index.html", "a")
        fpIndex.write("<li><a href=\"" + str(attFileName) + "\">" + str(attFileName) + "</a></li>\n")
        fpIndex.close() 
        fp.close()
        
        response['attachment'] = True


    response['content'] = contentOfMail
    response['message_id'] = message_id
    
        
    return response

indexCounter = 0
fileCounter = 1
print("##############################################")
print("# NoPriv.py IMAP Email Backup by Raymii.org. #")
print("# https://raymii.org - NoPriv.py is GPLv3    #")
print("##############################################")
print("")
print("Runtime Information:")
print(sys.version)
print("")
print(printQuote())
print("")
for y in range(indexCounter, len(id_list)):
    if len(id_list) < 50:
        lastnum = int(id_list[-1])
        firstnum = int(id_list[-1]) - (len(id_list) - 1)
    else:
        lastnum = int(id_list[-1])
        firstnum = int(id_list[-1]) - 50
    reportFileName = "email-report-" + str(fileCounter) + ".html"
    if breakOut is True:
        indexCounter += 1
        counter += 1
        breakOut = False
        break
    with open(reportFileName, "w") as emailReportFile:
        emailReportFile.write(returnHeader("Email Report " + str(fileCounter)))
        counter = 1
        maxItems = 50
        maxList = (len(id_list) - 50)
        if indexCounter >= maxList:
            maxItems = len(id_list) - indexCounter
        if indexCounter == len(id_list):
            break
        for z in range(int(indexCounter), int(indexCounter + maxItems)):
            x = (int(len(id_list)) - int(indexCounter))
            try:
                tableitem = return_message(x)
            except AttributeError as a:
                print("Error in Message %s: %s") % (z, a)
                breakOut = True
                indexCounter += 1
                counter += 1
            if breakOut == True:
                break
            try:
                yeardir = str(tableitem['date2'][0])
            except TypeError:
                yeardir = "unknown"
            try:
                monthdir = str(tableitem['date2'][1])
                if len(monthdir) == 1:
                    monthdir = str(0) + monthdir
            except TypeError:
                monthdir = "01"
            itemname = str(tableitem['message_id']) + ".html"
            emailLink = yeardir + '/' + monthdir + '/' + itemname
            print("Processing email %s from %s with subject: %s.\n") % (str(indexCounter), str(tableitem['termfrom']), str(tableitem['termsubject']))
            
            htmlSubject = cgi.escape(unicode(tableitem['subject'], 'utf-8')).encode('ascii', 'xmlcharrefreplace')
            htmlFrom = cgi.escape(unicode(tableitem['from'], 'utf-8')).encode('ascii', 'xmlcharrefreplace')
            emailReportFile.write("<tr>\n")
            emailReportFile.write("<td>\n")
            emailReportFile.write(str(indexCounter + 1))
            emailReportFile.write("</td>\n")
            emailReportFile.write("<td width=\"20%\">\n")
            emailReportFile.write(str(tableitem['from']))
            emailReportFile.write("</td>\n")
            emailReportFile.write("<td width=\"20%\">\n")
            emailReportFile.write(str(tableitem['to']))
            emailReportFile.write("</td>\n")
            emailReportFile.write("<td width=\"40%\">\n")
            emailReportFile.write("<a href=\"" + emailLink + "\">")
            emailReportFile.write(str(tableitem['subject']))
            emailReportFile.write("</a>\n")
            emailReportFile.write("</td>\n")
            emailReportFile.write("<td width=\"20%\">")
            emailReportFile.write(str(tableitem['date']))
            emailReportFile.write("</td>\n")
            emailReportFile.write("</tr>\n")
            if not os.path.exists(str(yeardir)):
                os.makedirs(str(yeardir))
            if not os.path.exists(str(yeardir) + '/' + str(monthdir)):
                os.makedirs(str(yeardir) + '/' + str(monthdir))
            with open(yeardir + '/' + monthdir + '/' + itemname, "w") as emailFile:
                emailFile.write(returnHeader("Email " + str(tableitem['subject']), "../../inc", 2))
                emailFile.write("<h1>Headers</h1>\n")
                emailFile.write("<strong>From:</strong> \"" + str(tableitem['from']) + "\"\n")
                emailFile.write("<br />\n")
                emailFile.write("<strong>To: </strong>\"" + str(tableitem['to']) + "\"\n")
                emailFile.write("<br />\n")
                emailFile.write("<strong>Subject:</strong> \"" + str(tableitem['subject']) + "\"\n")
                emailFile.write("<br />\n")
                emailFile.write("<strong>Date:</strong> \"" + str(tableitem['date']) + "\"\n")
                try:
                    if tableitem['attachment'] is True:
                        emailFile.write("<br />\n")
                        emailFile.write("<a href=\"" + str(tableitem['message_id']) + "/index.html\">")
                        emailFile.write("Click here to see the attachments of this email.")
                        emailFile.write("</a>\n")
                        attFolder = yeardir + '/' + monthdir + '/' + str(tableitem['message_id'])
                        if not os.path.exists(attFolder):
                            os.makedirs(attFolder)
                            print("Creating attachment folder %s from outer loop.") % attFolder
                        try:
                            fp = open(yeardir + '/' + monthdir + '/' + str(tableitem['message_id']) + '/index.html', 'a')
                            fp.write("</ul>\n<br />\n")
                            fp.write(returnFooter())
                            fp.close()
                        except IOError as e:
                            print("IOError in writing attachment: "), str(e)
                except IndexError:
                    emailFile.write("<br />\n")
                    emailFile.write("This email has no attachments.")

                emailFile.write("<br />\n")
                emailFile.write("<a href=\"javascript:history.go(-1)\">Go back</a>\n")
                emailFile.write("<hr />\n")
                if tableitem['content']['text']:
                    emailFile.write("<h1>Email Content (text)</h1>\n")
                    emailFile.write("<table>\n<tr>\n")
                    emailFile.write("<td width=\"100%\">\n<pre id=\"nonhtml\">\n")
                    emailFile.write(decodestring(str(tableitem['content']['text'])))
                    emailFile.write("</pre>\n</td>\n</tr>\n</table>\n")
                emailFile.write("<hr />\n")
                if tableitem['content']['html']:
                    emailFile.write("<h1>Email Content (HTML)</h1>\n")
                    emailFile.write("<table style=\"{text-align:left;}\">\n<tr>\n<td width=\"100%\" id=\"withhtml\">\n")
                    removedHeader = re.sub(r"(?i)<html>.*?<head>.*?</head>.*?<body>", "", str(tableitem['content']['html']), flags=re.DOTALL)
                    removedHeader = re.sub(r"(?i)</body>.*?</html>", "", removedHeader, flags=re.DOTALL)
                    removedHeader = re.sub(r"(?i)<!DOCTYPE.*?>", "", removedHeader, flags=re.DOTALL)
                    removedHeader = re.sub(r"(?i)POSITION: absolute;", "", removedHeader, flags=re.DOTALL)
                    removedHeader = re.sub(r"(?i)TOP: .*?;", "", removedHeader, flags=re.DOTALL)
                    emailFile.write(decodestring(removedHeader.replace("<html>", "")))
                    emailFile.write("</td>\n</tr>\n</table>\n")
                emailFile.write("<a href=\"javascript:history.go(-1)\">Go back</a>\n")
                emailFile.write(returnFooter())
                emailFile.close()
            indexCounter += 1
            counter += 1
        print("Finishing index file %s") % reportFileName
        emailReportFile.write("<tr>\n<td colspan=\"6\"><center> \n<br />\n&nbsp;<br /> \n<br /></center>\n</td>\n</tr>\n")
        emailReportFile.write("<tr>\n<td colspan=\"6\">Total Items in INBOX: %s .</td>\n</tr>\n" % str(len(id_list) - 1))
        if fileCounter == 1 and len(id_list) > 50:
            nextLink = "email-report-2.html"
            endingString = "<tr>\n<td colspan=\"2\">Page 1</td>\n<td colspan=\"3\"><a href=\"%s\">Next page.</a></td>\n</tr>\n" % nextLink
            emailReportFile.write(endingString)
            
        elif fileCounter == 1 and len(id_list) <= 50:
            endingString = "<tr>\n<td colspan=\"2\">Page 1</td>\n<td colspan=\"3\">No more pages.</td>\n</tr>"
            emailReportFile.write(endingString)
        elif fileCounter == (len(id_list) / 50):
            prevLink = "email-report-" + str(fileCounter - 1) + ".html"
            endingString = "<tr>\n<td colspan=\"2\">Page %s.</td>\n<td colspan=\"3\">\n<a href=\"%s\">Previous page.</a>\n</td>\n</tr>" % (str(fileCounter), prevLink)
            emailReportFile.write(endingString)
            
        else:
            prevLink = "email-report-" + str(fileCounter - 1) + ".html"
            nextLink = "email-report-" + str(fileCounter + 1) + ".html"
            pageNumber = str(fileCounter)
            endingString = "<tr>\n<td colspan=\"2\">Page %s.</td><td colspan=\"2\"><a href=\"%s\">Previous page.</a>\n</td>\n" % (pageNumber, prevLink)
            endingString2 = "<td colspan=\"2\"><a href=\"%s\">Next page.</a>\n</td>\n</tr>" % nextLink
            emailReportFile.write(endingString)
            emailReportFile.write(endingString2)
            
        emailReportFile.write("    </tbody>\n")
        emailReportFile.write("</table>\n")
        emailReportFile.write(returnFooter())
        emailReportFile.close()
        fileCounter += 1

