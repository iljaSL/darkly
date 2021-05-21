## Stored XXS

Knowing that the input fields are likely to be vulnerable towards XXS or SQL injections I moved to the next one, the feedback page.
It is not vulnerable against SQL injection attacks, but I found some other interesting things. First, the console displays a couple of errors:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag9/console_errors.png">
</p>

Two functions are not defined, and the one called `checkForm` sounds promising. Starting to test out some XSS, I noticed fast that `<tags>` are being filtered out by the backend, and we can post feedback without typing down a message, the undefined function `checkForm` would explain that.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag9/different_comment_input.png">
</p>

Next I tested if the filter is smart enough to filter out some hidden/nested tags. After a few tries it actually worked, and I could pass the following XXS snippet through the filter: `IMG """><SCRIPT>alert("XXS")</SCRIPT>"\>` , a so called malformed IMG tags. It uses the so-called relaxed rendering engine to create the XSS vector within an IMG tag that should be encapsulated within quotes. It is was originally meant to correct sloppy coding. Anyway here is flag number 9:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag9/flag9_and_exploit.png">
</p>

But this is not the end of the story and the title is not without a reason Stored XXS. While refreshing the page I noticed that the comment was posted again and again, after every fresh I did. A quick research reveals that this breach is not only a simple filter evasion, but also a stored XXS vulnerability. The injected script is permanently stored on the target servers for example a database. The victim then retrieves the malicious script from the server when it requests the stored information and the script is being executed with that call.

#### How to fix the vulnerability?

Again, a input validation needs to be done with regex or a trustworthy/active third party libraries, also sanitize the input.