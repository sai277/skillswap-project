from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet
# print(Fernet.generate_key())
# import base64

# Store this key securely (e.g., environment variable in production)
SECRET_KEY = b'Dv9Ks8w6kSElBcQqGhkX6hvgfpO9sXEeQ6j331pQ6kg='

fernet = Fernet(SECRET_KEY)

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    encrypted_content = models.BinaryField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save_encrypted_message(self, content):
        self.encrypted_content = fernet.encrypt(content.encode('utf-8'))
        self.save()

    def get_decrypted_message(self):
        return fernet.decrypt(self.encrypted_content).decode('utf-8')

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp}"
