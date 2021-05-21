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