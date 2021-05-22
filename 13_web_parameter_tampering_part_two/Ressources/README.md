## Web Parameter Tampering Part Two

After landing again on the login page, I noticed the forgot password mechanism. Inspecting it a bit closer in the console, I noticed that an email value is hard-coded to the HTML input tag, to which presumably the reset email will be sent.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag13/flag13_html_form_tags.png">
</p>

The type `hidden` of the HTML tag input is in this case used as a security measure. It is true that the email will be not displayed to the user in the page's content, BUT it is still visible. It can be edited using any browser's developer tools or "View Source" functionality. Do not rely on hidden inputs as a form of security.
This can be also abused for phishing attack, by building a reset page and sending the malicious site to a user with the hackers email instead.
Manipulating the email and click the reset button results in getting also the flag number 13!

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag13/flag_13.png">
</p>

#### How to fix the vulnerability?

Don't use the type `hidden` of the input tag for a sensitive task as resetting an email. Instead, do it in the backend to prevent a web parameter tampering.
