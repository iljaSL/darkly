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