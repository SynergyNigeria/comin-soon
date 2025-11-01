"""
Custom email backend that disables SSL certificate verification.
This is needed for Docker environments where SSL certificates may not be properly configured.
"""

import ssl
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend


class UnverifiedSSLEmailBackend(SMTPBackend):
    """
    Email backend that uses an unverified SSL context.
    This bypasses SSL certificate verification for SMTP connections.
    """

    def open(self):
        """
        Ensure we have a connection to the email server with unverified SSL context.
        """
        if self.connection:
            return False

        connection_params = {"timeout": self.timeout} if self.timeout else {}

        try:
            self.connection = self.connection_class(
                self.host, self.port, **connection_params
            )

            # Set debuglevel if needed
            if self.use_tls:
                # Create an unverified SSL context
                context = ssl._create_unverified_context()
                self.connection.starttls(context=context)

            if self.username and self.password:
                self.connection.login(self.username, self.password)

            return True
        except Exception:
            if not self.fail_silently:
                raise
