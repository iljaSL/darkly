# darkly

## The project is incomplete 🚧 The flag hunt is still ongoing! 🏁 :) 

## Table of content

- [Introduction](#introduction)
- [Enumeration](#enumeration)

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
