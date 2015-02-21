# limitSQLi
This is an automatic SQL injection tool which takes advantage of LIMIT clause.<br />
Version 0.1

USAGE:
<pre>python sqli.py <url> OR ./sqli.py <URL></pre>

NOTICE:<br />
1.This tool ONLY applys to LIMIT clause exploits without filtering or anti-injection measures on the server side. If there is any filtering on the server side, injection will fail with exceptions or zero bytes.<br />
To accomplish more advance features, please modify this code or wait for update.<br />

2.Wait patiently. Recently this program doesn't have multi-threading feature and it dumps the whole database, so it might take long time.
