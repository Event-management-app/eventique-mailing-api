'''
                                                                                                                                                                                 
 _|_|_|_|                                    _|      _|                                  _|      _|            _|  _|  _|                              _|_|    _|_|_|    _|_|_|  
 _|        _|      _|    _|_|    _|_|_|    _|_|_|_|        _|_|_|  _|    _|    _|_|      _|_|  _|_|    _|_|_|      _|      _|_|_|      _|_|_|        _|    _|  _|    _|    _|    
 _|_|_|    _|      _|  _|_|_|_|  _|    _|    _|      _|  _|    _|  _|    _|  _|_|_|_|    _|  _|  _|  _|    _|  _|  _|  _|  _|    _|  _|    _|        _|_|_|_|  _|_|_|      _|    
 _|          _|  _|    _|        _|    _|    _|      _|  _|    _|  _|    _|  _|          _|      _|  _|    _|  _|  _|  _|  _|    _|  _|    _|        _|    _|  _|          _|    
 _|_|_|_|      _|        _|_|_|  _|    _|      _|_|  _|    _|_|_|    _|_|_|    _|_|_|    _|      _|    _|_|_|  _|  _|  _|  _|    _|    _|_|_|        _|    _|  _|        _|_|_|  
                                                               _|                                                                          _|                                    
                                                               _|                  _|_|_|_|_|                                          _|_|    _|_|_|_|_|                        
Mailing API for Eventique (api.eventique.intellx.co.in)
BY AADITYA RENGARAJAN
CREATION TIMESTAMP : 11:44 11/23/21 23 11 2021
'''
#==============IMPORTING MODULES======================================================
#/- see 'requirements.txt' to install extra modules via pip
from flask import redirect, render_template, Flask, request, url_for, send_file, abort
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl, smtplib

#==============DEFINING BASIC FUNCTIONS======================================================

def sendmail(from_mail,to_mail,thesmtp,pwd,content,html,subject):
    # creating the MIME as plain text and HTML
    sender_email = from_mail
    receiver_email = to_mail
    password = pwd
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    part1 = MIMEText(content, 'plain')
    part2 = MIMEText(html, 'html')
    message.attach(part1)
    message.attach(part2)
    # starting an SSL context to send an e-mail
    try:
      context = ssl.create_default_context()
      with smtplib.SMTP_SSL(thesmtp, 465, context=context) as server:
          server.login(sender_email, password)
          server.sendmail(
              sender_email, receiver_email, message.as_string()
          )
      return 'Succesfuly Sent'
    except Exception as e:
        print(f"tried sending [{receiver} , {subject} , {text}]; failed due to error : {e}.")


app = Flask(__name__)

#==============ROUTES======================================================

#/- routes are defined by @app.route decorator

@app.route('/favicon.ico')
def favicon():
    return send_file("thumb.png")

@app.route('/')
def index():
  email_type = str(request.args.get("email_type")).upper()
  if "C" in email_type.upper():
    email_type = "CNT"
    print(email_type,"detected.")
    if request.args["send"]!="true":
      if request.args.get("image"):
        image = request.args["image"].lower()
      else:
        image = 0
      return render_template("CNT_mail.html",
                             name = request.args["name"],
                             color = request.args["color"].lower(),
                             subject = request.args["subject"],
                             image = image,
                             content = request.args["content"],
                             confid = request.args["confid"].lower()
                             )
    elif request.args["send"]=="true":
      if request.args.get("image"):
        image = request.args["image"].lower()
      else:
        image = 0
      the_email = render_template("CNT_mail.html",
                                   name = request.args["name"],
                                   color = request.args["color"].lower(),
                                   subject = request.args["subject"],
                                   image = image,
                                   content = request.args["content"],
                                   confid = request.args["confid"].lower()
                                   )
      return app.response_class(
                  response=sendmail(request.args["sender"],
                                    request.args["recepient"],
                                    request.args["smtp"],
                                    request.args["pwd"],
                                    request.args["content"],
                                    the_email,
                                    request.args["subject"]),
                  mimetype='text/plain'
                )
  elif ("C" not in email_type.upper()) and email_type.upper()!="NONE":
    email_type = "PLN"
    if request.args["send"]!="true":
      if request.args.get("image"):
        image = request.args["image"].lower()
      else:
        image = 0
      return render_template("PLN_mail.html",
                             to = request.args["recepient"].lower(),
                             from_mail = request.args["sender"].lower(),
                             subject = request.args["subject"],
                             image = image,
                             content = request.args["content"],
                             name = request.args["name"],
                             confid = request.args["confid"].lower()
                             )
    elif request.args["send"]=="true":
      if request.args.get("image"):
        image = request.args["image"].lower()
      else:
        image = 0
      the_email = render_template("PLN_mail.html",
                                   to = request.args["recepient"].lower(),
                                   from_mail = request.args["sender"].lower(),
                                   subject = request.args["subject"],
                                   image = image,
                                   content = request.args["content"],
                                   name = request.args["name"],
                                   confid = request.args["confid"].lower()
                                   )
      return app.response_class(
                  response=sendmail(request.args["sender"],
                                    request.args["recepient"],
                                    request.args["smtp"],
                                    request.args["pwd"],
                                    request.args["content"],
                                    the_email,
                                    request.args["subject"]),
                  mimetype='text/plain'
                )
  return app.response_class(
        response='''HTML E-Mail Dispatch `Documentation
- There are 2 types of E-Mails, "CNT" and "PLN", to be mentioned in query string 'email_type'.
- For CNT :
  - Name of Sender is to be included under query string 'name'.
  - Primary Color of E-Mail is to be included under query string 'color'.
  - Subject of E-Mail is to be included under query string 'subject'.
  - Any Image is to be included under query string 'image' (OPTIONAL).
  - Content of the E-Mail is to be included under query string 'content' as HTML format.
- For PLN :
  - The Recepient (To) of the E-Mail is to be included under query string 'recepient' as an e-mail address.
  - The Sender (From) of the E-Mail is to be included under query string 'sender' as an e-mail address.
  - Subject of E-Mail is to be included under query string 'subject'.
  - Any Image is to be included under query string 'image' (OPTIONAL).
  - Content of the E-Mail is to be included under query string 'content' as HTML format.
  - Name of Sender is to be included under query string 'name'.
- Include Query String 'confid', 'true' if e-mail is confidential, 'false' if else.
- If the e-mail is to be sent :
  - Mention it by including query string 'send' and giving it a value as 'true'.
  - The Sender (From) of the E-Mail is to be inclued under query string 'sender' as an e-mail address.
  - The Recepient (To) of the E-Mail is to be inclued under query string 'recepient' as an e-mail address.
  - The SMTP Server (eg : smtp.gmail.com) is to be inclued under query string 'smtp'.
  - The Sender's E-Mail Password is to be inclued under query string 'pwd'.
  - Content of the E-Mail is to be inclued under query string 'content'.
This HTML E-Mail Dispatching System has been developed by Aaditya Rengarajan for Eventique by PSGCT.
''',
        mimetype='text/plain'
      )

#==============ERROR HANDLING======================================================

#/- custom error handling using custom template to get fancy ;)

@app.errorhandler(404)
def page_not_found(e):
    return str((render_template('error.html',
                code="404",
                type="Not Found",
                content="Sorry, this page was not found!"))), 404

@app.errorhandler(500)
def internal_server_error(e):
    return str((render_template('error.html',
                code="500",
                type="Internal Server Error",
                content=f"Oh No! Something Went Wrong!<br/>{e}"))), 500

@app.errorhandler(410)
def gone(e):
    return str((render_template('error.html',
                code="410",type="Gone",
                content="Sorry, this page is has mysteriously vanished!"))), 410

@app.errorhandler(403)
def forbidden(e):
    return str((render_template('error.html',
                code="403",
                type="Forbidden",
                content="Sorry, you are not allowed to access this page!"))), 403

@app.errorhandler(401)
def unauthorized(e):
    return str((render_template('error.html',
                code="401",
                type="Unauthorized",
                content="Sorry, you are not authorized to access this page!"))), 401

#==============PROGRAM RUN======================================================

if __name__=="__main__":
    #/- note : remove debuggers and change port respectively
    #/- on production deployment.
    app.run(
        debug=True,
        use_reloader=True,
        use_debugger=True,
        port=8025,
        host="0.0.0.0",
        use_evalex=True,
        threaded=True,
        passthrough_errors=False
        )

#==============END OF WEBAPP======================================================