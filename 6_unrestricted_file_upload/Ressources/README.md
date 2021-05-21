## Unrestricted File Upload

Having done some rooms on try hack me that were specialized on unrestricted file uploads, I got really interested in the upload picture site on darkly. First things first, I tried to intercept the request with burpsuite  by uploading a normal JPEG picture, and I was able to capture some interesting specs:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag6/enumeration_first_upload.png">
</p>

That looks like the parameters might be not checked by the server. But first I tried if the file upload is properly checked on the backend. Files without an `.jpeg` extensions got filtered out, `webshell.php` or `webshell.py` were not allowed to upload. But one thing was not considered by the backend check, a double extension. I uploaded the following file containing a reverse webshell script, `test.php%00.jpg`. The `.jpg` gets truncated and `.php` becomes the new extension, and it worked!

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag6/enumeration_bonus_breach.png">
</p>

But unfortunately, I did not get any flag for that vulnerability. I guess it's a bonus point. <br>
Knowing that the server does have some filter problems and highly likely  a flag, I focused again on the burpsuite results. This time I upload a plain `webshell.php` file, intercept it with burp and change the `Content-Type` to `image/jpeg`.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag6/exploit_flag6.png">
</p>

Once again I forward it and it actually worked! The file has been upload, and I received flag number 6.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag6/flag6.png">
</p>

#### How to fix the vulnerability?

Files should be thoroughly scanned and validated before being uploaded. All the control characters, special characters and Unicode ones should be removed from the filenames and their extensions without any exception.