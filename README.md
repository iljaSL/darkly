# darkly

## The project is incomplete 🚧 The flag hunt is still ongoing! 🏁 :) 

## Table of content

- [Introduction](#introduction)
- [Enumeration](#enumeration)
- [Flags](#flags)
  - [1: Brute Force Directories and File names](#1)
  - [2: Path Traversal Attack](#2)
  - [3: Unvalidated Redirect and Forward Attack](#3)

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

## Flags

## 1: Brute Force Directories and File names

The first interesting lead I investigated are the files and directories that resulted from the nmap and gobuster scans. I checked out all the folders gobuster found, which were not accessible duo the lack of permission, expect `/whatever`, in which I found the file `htpasswd` and was able to download it. 

```
kali@kali:~/Downloads$ cat htpasswd 
root:8621ffdbc5698829397d97767ac13db3
```

The file included the name root and what looked like a md5 hash. I confirmed it with an online hash cracker and also the cracked the hash which resulted in the following string `dragon`.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/hash_identification.png">
</p>

It looks like I found some credentials! Now I need to find out where exactly I can use them. I first started to get access to the server via SSH, which unfortunetly did not work and would be pretty funny if it would. 

```
SSH connection with root:dragon FAILED
sudo ssh -p 4242 root@192.168.1.210 Permission denied, please try again.
```

Next, I tried to log in on the website. Which failed again. <br>
While I was checking the gobuster results, I came across the following route `/admin`, which also had a log in form. I tried to log in... and there it was! The first flag.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag1.png">
</p>

#### How to fix the vulnerability?

Don't store files or directories with any sensitive information included! Especially log in credentials for admin/root accounts. Use tools like gobuster, dirbuster or burp on your web applciation to see what kind of files or dir's are visible for the public, moves those that youd don't want to be visiable to the public eye.

## 2: Path Traversal Attack

The other folder that was found through nmap contained tirvial named directories and a REEADME file (which did not included anything useful). By clicking through the directories, I noticed that I was moving through the file system on the web server and that could mean that the website might be vulnerable to Path Traversal attacks.

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/hidden_folder.png">
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
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag3.png">
</p>

#### How to fix the vulnerability?

There is a great article on the official OWASP site about the Path Traversal attack and how you can protect yourself against it! <br>
[Path Traversal Attack OWASP](https://owasp.org/www-community/attacks/Path_Traversal)

## 3: Unvalidated Redirect and Forward Attack

Let's move on to another finding that we discovered during the enumeration. A fast look at browser console revealed that the redirection to different social media sites at the bottom of the website are not validated. Open redirect are not directly critical for the website itself and do not allow an attacker to steal data that belongs to the owner of the website, but are rather dangerous for the user of the website. There are mainly used for phishing attacks, the victim receives an email that looks legitimate with a link that points to a correct and expected domain. What the victim may not notice, is that in a middle of a long URL there are parameters that manipulate and change where the link will take them.

Let's test it out on the darkly website and forge the URL:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/open_redirection.png">
</p>

Click the social media link and there we go! Flag number 3!

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag2.png">
</p>

#### How to fix the vulnerability?

The best solution is not to use any redirects or forwards, if it's not a crucial business aspect of the website. You also could store full URLs in the database, give them identifiers and use the identifiers as request parameters. With such an approach, attackers will not be able to redirect or forward to unauthorized pages.
You can also whitelist some URLs that you think are save for a redirection. This solution is risky though, because errors in filtering may make certain attack vectors possible.
