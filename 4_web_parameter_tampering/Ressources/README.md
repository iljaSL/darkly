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