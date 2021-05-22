## Web Crawling For Sensitive Information

This was a rather tricky flag to get. During the path traversal attack process of getting the second flag, I mentioned that the many directories always include a README file with a comment in French inside it and I marked it as not important information. Well translating a couple of those text in different README files, I noticed that they included clues (but why are those comments in french 42!!!) in pointing out that one of the README is having the flag. Going through the many directories manual would take at least a day, so it was pretty clear that I need to use a web crawler for that task. I coded a small script for this task and got after a minute the following output with the flag number 14:

<p align="center">
  <img src="https://github.com/iljaSL/darkly/blob/main/assets/images/flag14/flag14_script_output.png">
</p>

#### How to fix the vulnerability?

Search engines, like Google, use bots or web crawlers and apply search algorithm to gather data, so relevant links are provided in response to search queries. It helps in generating a list of web pages or search engine results and improving the SEO. A simple rule is to make some of your web pages/directories not discoverable that you do not want to be discovered by the public.
