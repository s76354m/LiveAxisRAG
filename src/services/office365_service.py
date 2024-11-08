class Office365Integration:
    def __init__(self, credentials):
        self.account = Account(credentials)
        self.mailbox = self.account.mailbox()
        
    def send_notification(self, template_name: str, context: dict):
        template = self.get_email_template(template_name)
        message = self.mailbox.new_message()
        message.subject = template.render_subject(context)
        message.body = template.render_body(context)
        return message.send() 