import badgerlib
import smtplib
from email.mime.text import MIMEText
class EmailHandler(badgerlib.Handler):

    def __init__ (self, config=None):
        badgerlib.Handler.__init__(self, config)
        if self.config:
            self.enabled = self.config.get("enable", True)
            self.from_addr = self.config.get("from", "nobody@nobody.com")
            self.to_addr = self.config.get("to", "nobody")
            self.subject = self.config.get("subject", "Badger Alert")
            self.message = self.config.get("message", "Smartcard inserted")
            self.server = self.config.get("server", "localhost")

    def on_lock(self, state):
        if not state.get_inserted() or self.config is None or not self.enabled:
            return
        msg = MIMEText(self.message)
        msg['Subject'] = self.subject
        msg['From'] = self.from_addr
        msg['To'] = self.to_addr
        try:
            s = smtplib.SMTP(self.server)
            s.sendmail(self.from_addr, [self.to_addr], msg.as_string())
            s.quit()
        except:
            print "SMTP Error"



            