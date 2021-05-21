# darkly

## The project is incomplete 🚧 The flag hunt is still ongoing! 🏁 :)

## Table of content

- [Introduction](#introduction)
- [Enumeration](#enumeration)
- [Flags](#flags)
  - [Brute Force Directories and File names](#brute-force-directories-and-file-names)
  - [Path Traversal Attack](#path-traversal-attack)
  - [Unvalidated Redirect and Forward Attack](#unvalidated-redirect-and-forward-attack)
  - [Web Parameter Tampering](#web-parameter-tampering)
  - [Sensitive Information in Source Code and Cross-Site Request Forgery](#sensitive-information-in-source-code-and-cross-site-request-forgery)
  - [Unrestricted File Upload](#unrestricted-file-upload)
  - [Session Prediction](#session-prediction)
  - [XXS Code Encoding](#xxs-code-encoding)
  - [Stored XXS](#stored-xxs)
  - [Password Guessing Attack](#password-guessing-attack)
  - [SQL Injection Union Attack Part One](#sql-injection-union-attack-part-one)
  - [SQL Injection Union Attack Part Two](#sql-injection-union-attack-part-two)

## Introduction

This Hive Helsinki Project is about finding 14 flags on a self hosted website, that I run via VirtualBox (iso file is inside the assets), through 14 different breaches.
That's it with the clues! More information about how the project is gonna be evaluated is found in the subject file.

The `darkly_enumeration.ctb` file contains my detailed enumeration process and can be opened with any note taking application. <br>
My favorite one is [CherryTree](https://www.giuspen.com/cherrytree/), which is free and open source.

## Enumeration

Enumeration is a continuous ongoing operation. Usually when I'm completely stuck on one specific problem, I'm always returning to the start and begin to search for new clues. This means that the Enumeration section will be dynamic and changing over time. It always starts with a basic nmap scan. (The IP address is provided to the student as soon as the darkly web server is started with VirtualBox)

```
nmap -sC -sV <IP>
```

`-sC (Script scan, very noisy, should be only performed with permission)` <br>
`-sV (Version detection)`

The result:
```
Nmap scan report for 192.168.1.210
Host is up (0.0030s latency).
Not shown: 998 filtered ports
PORT     STATE SERVICE VERSION
80/tcp   open  http    nginx 1.8.0
| http-robots.txt: 2 disallowed entries
|_/whatever /.hidden
|_http-server-header: nginx/1.8.0
|_http-title: BornToSec - Web Section
4242/tcp open  ssh     OpenSSH 5.9p1 Debian 5ubuntu1.7 (Ubuntu Linux; protocol 2.0)
|_dicom-ping:
| ssh-hostkey:
|   1024 c1:03:76:40:29:e8:ab:f6:8a:9f:1c:71:6e:23:e0:58 (DSA)
|   2048 89:95:1a:c3:7c:1b:fc:3c:34:1d:76:d5:c9:fa:86:03 (RSA)
|_  256 09:86:1a:be:13:a5:a1:0c:7f:f7:55:50:ac:7a:c7:1a (ECDSA)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
Now we are absolutely sure that darkly is an web server running with nginx on port 80, it allows to establish an SSH connection on port 4242 and we know the version numbers.
A big plus, nmap even detected the `robots.txt` file, which is a very common file, but unfortunately too many times the developers try to hide files or directories with sensitive information from the web crawlers.

I also like to run `gobuster` or `dirbuster` to draw a folder structures map of the website and find with a little luck more hidden folders or files that weren't meant for the public.

```
gobuster dir -u http://192.168.1.210 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

The result:

```
/images               (Status: 301) [Size: 184] [--> http://192.168.1.210/images/]
/admin                (Status: 301) [Size: 184] [--> http://192.168.1.210/admin/]
/audio                (Status: 301) [Size: 184] [--> http://192.168.1.210/audio/]
/css                  (Status: 301) [Size: 184] [--> http://192.168.1.210/css/]
/includes             (Status: 301) [Size: 184] [--> http://192.168.1.210/includes/]
/js                   (Status: 301) [Size: 184] [--> http://192.168.1.210/js/]
/fonts                (Status: 301) [Size: 184] [--> http://192.168.1.210/fonts/]
/errors               (Status: 301) [Size: 184] [--> http://192.168.1.210/errors/]
/whatever             (Status: 301) [Size: 184] [--> http://192.168.1.210/whatever/]
```

Now let's move on and visit finally the website itself. It's hard to describe the websites theme, it's a bit of everything...You can search for things, you can upload pictures, you can leave a feedback, you can log and sing in. Checking the website in detail, I discovered a couple of things.

- A `GET` request is used for sending user crediantials while trying to log in to the server
- An open redirection is used for redirecting the user to different kind of social media
- An interesting cookie is given to the user `Cookie: I_am_admin=68934a3e9455fa72420237eb05902327`
- Typing `'` into the search field results in the following error message `You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '\'' at line 1`, SQL queries are not sanitized and we know now that MySQL is used as a DB
- NSA picture on landing page redirects to a different route and is an object tag
- Copryright page contains interesting comments in source code
- Console log errors on the survey page, some validation functions do not work

## Flags

## Brute Force Directories and File names

The first interesting lead I investigated are the files and directories that resulted from the nmap and gobuster scans. I checked out all the folders gobuster found, which were not accessible duo the lack of permission, expect `/whatever`, in which I found the file `htpasswd` and was able to download it.

```
kali@kali:~/Downloads$ cat htpasswd
root:8621ffdbc5698829397d97767ac13db3
```

The file included the name root and what looked like a md5 hash. I confirmed it with an online hash cracker and also the cracked the hash which resulted in the following string `dragon`.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag1/hash_identification.png">
</p>

It looks like I found some credentials! Now I need to find out where exactly I can use them. I first started to get access to the server via SSH, which unfortunetly did not work and would be pretty funny if it would.

```
SSH connection with root:dragon FAILED
sudo ssh -p 4242 root@192.168.1.210 Permission denied, please try again.
```

Next, I tried to log in on the website. Which failed again. <br>
While I was checking the gobuster results, I came across the following route `/admin`, which also had a log in form. I tried to log in... and there it was! The first flag.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag1/flag1.png">
</p>

#### How to fix the vulnerability?

Don't store files or directories with any sensitive information included! Especially log in credentials for admin/root accounts. Use tools like gobuster, dirbuster or burp on your web applciation to see what kind of files or dir's are visible for the public, moves those that youd don't want to be visiable to the public eye.

## Path Traversal Attack

The other folder that was found through nmap contained tirvial named directories and a REEADME file (which did not included anything useful). By clicking through the directories, I noticed that I was moving through the file system on the web server and that could mean that the website might be vulnerable to Path Traversal attacks.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag2/hidden_folder.png">
</p>

With the help of the OWASP guide, I tried out different methods which did not work at first, but after focusing on the `Search Member` form and inserting to the url the following path:

```
192.168.1.210/?page=../../../../etc/shadow
```
I finally got a prompt popping out with the message `Almost`, which at first I labeled out as a 42 trolling attempt.
But I still tried to move further back in the file system, which also did not work either. So I have tried it with `/etc/passwd` (stores user account information) and after a few attempts and finally got a prompt popping out with the flag inside it!

```
192.168.1.210/?page=../../../../../../../etc/passwd
```

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag3/flag3.png">
</p>

#### How to fix the vulnerability?

There is a great article on the official OWASP site about the Path Traversal attack and how you can protect yourself against it! <br>
[Path Traversal Attack OWASP](https://owasp.org/www-community/attacks/Path_Traversal)

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

## Web Parameter Tampering

While checking out the website for more vulnerabilities, I came across the survey page and detected in the network tab inside the console that a request payload is sent to the server, which is of course totatlly normal, but what happens if I manipulate the parameters that are exchanged between client and server?

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag4/web_parameter_tampering_1.png">
</p>

Once again we intercept the post request with burp, manipulate the parameters and forward it.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag4/web_parameter_tampering_burp_2.png">
</p>

There we go! The tampering was a success and we got flag number 4!

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag4/flag4.png">
</p>

Parameter tampering results on integrity and logic validation mechanism errors, here is an example for what it can be used.
Lets assume we have the following tag `<input type=”hidden” id=”1008” name=”cost” value=”70.00”>`
In this example, an attacker can modify the “value” information of a specific item, thus lowering its cost.

[Click for more information (OWASP)](https://owasp.org/www-community/attacks/Web_Parameter_Tampering) <br>
[Click for more information (imperva blog post)](https://www.imperva.com/learn/application-security/parameter-tampering/)

#### How to fix the vulnerability?

Using regex to limit or validate data can help to limit this vulnerability or by avoiding to including parameters into the query string.
Also use a server-side validation to compare the data with all inputs.

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

## SQL Injection Union Attack Part One

First things first, I did not have too much hands-on experience with SQL injection. I was aware of the most basic stuff, but I had really trouble to exploit the next two flags during the first try. I decided to learn more about SQL injection attacks. Luckily I found the amazing learning series by port swigger -> https://portswigger.net/web-security/sql-injection, which basically helped me to get those two flags and at the same time expended my knowledge around SQL injections in an enormous way!
After doing some basic testing, I quickly found out that the search section inside the `find members` page, is vulnerable against Union attacks. I also noticed that the search form was very forgiving and basically let me input the SQL injection queries without any fancy `'` `--` commenting out stuff. Just a simple `1 OR 1=1` was already enough to trigger the queries. I will not get in too much detail about the Union Attack, the link that I previously posted, covers the topic in a great detail. In order for a Union query to work, we need tow key requirements.

- The individual queries must return the same number of columns
- The data types in each column must be compatible between the individual queries

So, first we need to find out

- How many columns are being returned from the original query?
- Which columns returned from the original query are of a suitable data type to hold the results from the injected query?

To determine how many columns are being returned, we simply need to start with the following query `1 OR 1=1 UNION SELECT NULL--` and increment the null if an error is returned. The DB behind darkly returns two columns:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag11/how_many_columns.png">
</p>

I took only a screenshot of the most interesting column, the actual query output was much larger.
Now we can move forward and check out the tables inside the DB, we know that darkly is using MySQL with the help of the enumeration. Different DB's have different type of commands, thus we always need to find out with what kind of DB we are working with. Moving on to the tables:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag11/db_information_schema.png">
</p>

It's a search form for finding site members, so we have a clue that the `users` table is probably our main target of all the tables.
Now we need more information about the users table, for example about the columns.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag11/db_user_column_information.png">
</p>

Awesome! Now I can check out what is exactly inside the users table, with the SQL function `CONCAT()`, I can simply add many expressions (in our case columns) together and return the data inside the users table:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag11/decrypted_flag.png">
</p>

Again the output is large, I only took a screenshot of the most important one.
We get a detailed step to step guide in how to retrieve the flag. Let's decrypt the MD5 (of course) hash, it results in `fortytwo` and encrypted it again into a sha256 hash.
The result is flag number 11:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag11/sha256_encoding.png">
</p>

#### How to fix the vulnerability?

Use Prepared Statements. Prepared statements ensure that an attacker is not able to change the intent of a query, even if SQL commands are inserted by an attacker.
Use Stored procedures. They require the developer to just build SQL statements with parameters which are automatically parameterized unless the developer does something largely out of the norm. The difference between prepared statements and stored procedures is that the SQL code for a stored procedure is defined and stored in the database itself, and then called from the application. Both of these techniques have the same effectiveness in preventing SQL injection so your organization should choose which approach makes the most sense for you.

[Click for more information about SQL Injection Attacks (OWASP)](https://portswigger.net/web-security/sql-injection/union-attacks)
[Click for more information about SQL Injection Preventions (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

## SQL Injection Union Attack Part Two

Same vulnerability as the previous flag [SQL Injection Union Attack Part One](#sql-injection-union-attack-part-one), this time we are searching for images. I'm not gonna go into detail and only post the screenshots regarding the attack.

First we test if the search form is vulnerable against SQL injection attacks:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag11/sha256_encoding.png">
</p>

How many columns are being returned?

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag12/column_test.png">
</p>

Let's find the most interesting column, this time it's not `users`, but something with images.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag12/images_column_names.png">
</p>

Now let's check out the data inside the `images_list`, with again the help of `CONCAT()`:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag12/union_attack_success.png">
</p>

Let's follow again the 'guide' step by step:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag12/md5_hash_decoded.png">
</p>

And flag number 12 is:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag12/flag12.png">
</p>

#### How to fix the vulnerability?

Use Prepared Statements. Prepared statements ensure that an attacker is not able to change the intent of a query, even if SQL commands are inserted by an attacker.
Use Stored procedures. They require the developer to just build SQL statements with parameters which are automatically parameterized unless the developer does something largely out of the norm. The difference between prepared statements and stored procedures is that the SQL code for a stored procedure is defined and stored in the database itself, and then called from the application. Both of these techniques have the same effectiveness in preventing SQL injection so your organization should choose which approach makes the most sense for you.

[Click for more information about SQL Injection Attacks (OWASP)](https://portswigger.net/web-security/sql-injection/union-attacks)
[Click for more information about SQL Injection Preventions (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
