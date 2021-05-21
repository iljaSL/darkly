## Unvalidated Redirect and Forward Attack

Let's move on to another finding that we discovered during the enumeration. A fast look at browser console revealed that the redirection to different social media sites at the bottom of the website are not validated. Open redirect are not directly critical for the website itself and do not allow an attacker to steal data that belongs to the owner of the website, but are rather dangerous for the user of the website. There are mainly used for phishing attacks, the victim receives an email that looks legitimate with a link that points to a correct and expected domain. What the victim may not notice, is that in a middle of a long URL there are parameters that manipulate and change where the link will take them.

Let's test it out on the darkly website and forge the URL:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag3/open_redirection.png">
</p>

Click the social media link and there we go! Flag number 3!

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag2/flag2.png">
</p>

#### How to fix the vulnerability?

The best solution is not to use any redirects or forwards, if it's not a crucial business aspect of the website. You also could store full URLs in the database, give them identifiers and use the identifiers as request parameters. With such an approach, attackers will not be able to redirect or forward to unauthorized pages.
You can also whitelist some URLs that you think are save for a redirection. This solution is risky though, because errors in filtering may make certain attack vectors possible.