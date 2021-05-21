## XXS Code Encoding

During the reconnaissance I noticed that early on that there is only one image clickable, which leads to a different route. The URL looked at the first glance already really promising `<darklyIP>/?page=media&src=nsa` and could be vulnerable to a XSS attack if there is no correct sanitizing on the server side happening. One thing that also noticed inside the source code, is that the website is using HTML object tags for the picture.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag8/object_tag_source_code.png">
</p>

Theoretically, I could craft URL's for phishing attacks and abuse it, because in this case, data inside the object tag is not checked, and I can execute script commands.
However, I did not receive a flag for that one. Moving on to the URL, lets craft one with once again the help of OWASP. A simple `<script>alert("XXS")</script>` won't work though, we need to decode it with base64 otherwise it won't work. Once again I use burp for it:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag8/exploit_payload.png">
</p>

The crafted URL is ready, forwarding the request with burp and once again the XXS attack worked, this time I also got the flag:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag8/flag8.png">
</p>

#### How to fix the vulnerability?

In order to prevent this attack, a URL validation with regex or trustworthy/active third party libraries needs to happen on the backend. Consider also to accept only predefined patterns after `src=` and of course sanitize the users input!