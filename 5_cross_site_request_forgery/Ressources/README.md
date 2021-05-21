## Sensitive Information in Source Code and Cross-Site Request Forgery

Let's focus on the other enumeration findings. Going through the page (of course with the console open!!!), I noticed some crazy amount of comments on the copyright  page. Most if it was in french, but there were two interesting comments in english.

```
You must cumming from : "https://www.nsa.gov/" to go to the next step
```
and
```
Let's use this browser: "ft_bornToSec".
```
After a quick google search, I could for sure say that a `ft_bornToSec` browser does not exist. My next natural step was to visit the official page of the NSA and go from there  to the darkly copyrights page, which sadly did not work. After a rather long google session, I came across a specific Cross-Site Request Forgery attack, it is a type of attack that occurs when a malicious web site, causes a users web browser to do an unwanted action on a trusted site. It's a very broad topic, I'm focusing on the manipulation and forgery of the HTTP header. Now I just need to manipulate two fields inside the header, turning on burp, intercepting the request and changing the fields `Referer` and `User-Agent` to the following:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag5/flag5_burp_header_manipulation.png">
</p>

Forwarding it...and jackpot, flag number 5 is displayed on the screen!

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag5/flag5.png">
</p>

#### How to fix the vulnerability?

Don't leave sensative comments inside the source code that you don't want to be seen by the public! Also verify server side if the origin/referer header is present and its value matches the target origin. Create a strong check for the referer and create a whitelist for the user agent.

[Click for more information (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#introduction)