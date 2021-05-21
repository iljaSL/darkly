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
