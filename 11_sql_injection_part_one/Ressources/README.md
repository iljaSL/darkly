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