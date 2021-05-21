## Session Prediction

Okay now is the time to turn the attention to the one thing that bothered me the most, the session cookie I received, `I_am_admin=68934a3e9455fa72420237eb05902327`. I googled the random generated string after the equal sign and the first result that pops out is, that this string is a MD5 hash. I confirmed it by using the same online hash cracker that I used for the very first flag and here is the result:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag7/hash_cracker_first_try.png">
</p>

It is indeed a MD5 hash which equals to `false`. It took me a very long time to get to the bottom of this, but after a while I was thinking, 'hey it looks like it's a boolean so what happens if I set the value to true?'. So I set the session cookie to `I_am_admin=true`, forwarded the request (using burp of course!) and... nothing happened. After another very long time, I came finally to the conclusion that I need to hash the value `true` back into a MD5 hash. So I did:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag7/md5_encryption_true.png">
</p>

Again, forwarding the request with burp... and it worked! Now it was very obvious to me, but getting that flag took me a very long time! Nevertheless, here is flag number 7.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag7/flag7.png">
</p>

#### How to fix the vulnerability?

Don't store cookies with key values and descriptions to what exactly the session cookie belongs, you will just make it easier for the hacker to analyze and understand the session ID generation process. Consider using JWT and do not use MD5 hashes at all, they are unsecure and very easy to crack.

[Click for more information (OWASP)](https://owasp.org/www-community/attacks/Session_Prediction)