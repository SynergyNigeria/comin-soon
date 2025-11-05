"""
Custom email backend that disables SSL certificate verification.
This is needed for Docker environments where SSL certificates may not be properly configured.
"""

import ssl
import socket
from smtplib import SMTP, SMTP_SSL
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend


class UnverifiedSSLEmailBackend(SMTPBackend):
    """
    Email backend that uses an unverified SSL context.
    This bypasses SSL certificate verification for SMTP connections.
    Tries multiple strategies to connect to the SMTP server.
    """

    def open(self):
        """
        Ensure we have a connection to the email server with unverified SSL context.
        Tries TLS on port 587, then SSL on port 465 if TLS fails.
        """
        if self.connection:
            return False

        # Increase timeout to 90 seconds for production environments
        timeout = self.timeout or 90
        socket.setdefaulttimeout(timeout)

        # Create an unverified SSL context
        context = ssl._create_unverified_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        # Try TLS first (port 587)
        if self.use_tls:
            try:
                print(f"Attempting TLS connection to {self.host}:{self.port}")
                self.connection = SMTP(self.host, self.port, timeout=timeout)
                self.connection.ehlo()
                self.connection.starttls(context=context)
                self.connection.ehlo()

                if self.username and self.password:
                    self.connection.login(self.username, self.password)

                print(f"TLS connection successful to {self.host}:{self.port}")
                return True
            except Exception as e:
                print(f"TLS connection failed: {str(e)}")
                self.connection = None

                # Try SSL (port 465) as fallback
                try:
                    print(f"Attempting SSL connection to {self.host}:465")
                    self.connection = SMTP_SSL(
                        self.host, 465, timeout=timeout, context=context
                    )
                    self.connection.ehlo()

                    if self.username and self.password:
                        self.connection.login(self.username, self.password)

                    print(f"SSL connection successful to {self.host}:465")
                    return True
                except Exception as e2:
                    print(f"SSL connection also failed: {str(e2)}")
                    if not self.fail_silently:
                        raise Exception(
                            f"Both TLS and SSL connections failed. TLS: {str(e)}, SSL: {str(e2)}"
                        )
        else:
            # Non-TLS connection
            try:
                print(f"Attempting non-TLS connection to {self.host}:{self.port}")
                self.connection = SMTP(self.host, self.port, timeout=timeout)

                if self.username and self.password:
                    self.connection.login(self.username, self.password)

                print(f"Non-TLS connection successful to {self.host}:{self.port}")
                return True
            except Exception as e:
                print(f"Non-TLS connection failed: {str(e)}")
                if not self.fail_silently:
                    raise

        return False
