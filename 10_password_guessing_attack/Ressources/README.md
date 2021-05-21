## Password Guessing Attack

During my first enumeration attempt, I noticed that the login page is using a GET request for sending the login credentials to the server.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag10/get_request.png">
</p>

The first problem is, that nobody should use a GET request for posting sensitive data to the server. GET request are sent in plain text, this means that a hacker could SNiFF (capture) a network traffic and see the login credentials in plain text. This would also store the login link with the visible password and username in the browser history. After returning to the login page and experimenting with the page bit, I also noticed that the request is sent to and proccesed by the server without an username. The form also did not have a limit on how many requests I can send to the server with the same IP address. This is a great start for a brute force attack. So once again I intercepted the request and sent it to burps intruder in order to perform the brute force attack. I create two payloads, for the username the most common names for example admin, root etc. and the second payload is the password, for which I used the `rockyou.txt` word list. It's not the most graceful attack, but an effective one if you have the computing power and the website is not properly protected against it. Luckily after over 10 minutes I received a match!

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag10/password_found.png">
</p>

In our case, the response length is different. Trying to log in with the credentials also worked and flag number 10 is being displayed!

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag10/flag10.png">
</p>

#### How to fix the vulnerability?

The most obvious way to block brute-force attacks is to simply lock out accounts after a defined number of incorrect password attempts. You may also consider locking out authentication attempts from known and unknown browsers or devices separately.
After one or two failed login attempts, you may want to prompt the user not only for the username and password but also to answer a secret question. This not only causes problems with automated attacks, it prevents an attacker from gaining access, even if they do get the username and password correct.
Also do not use a GET request to sent sensitive information to the server and always check the form for invalid inputs for example empty inputs.

[Click for more information (OWASP)](https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks)