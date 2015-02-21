# limitSQLi
This is an automatic SQL injection tool which takes advantage of LIMIT clause.
Version 0.1

USAGE:
python sqli.py <url> OR ./sqli.py <URL>

NOTICE:
1.This tool ONLY applys to LIMIT clause exploits without filtering(e.g: something like $value=intval($_GET['num']); on the server side).
  If there is any filtering on the server side, injection will fail with exceptions or zero bytes.
  To accomplish more advance features, please modify this code or wait for update.
2.Wait patiently. Recently this program doesn't have multi-threading feature and it dumps the whole database, so it might take long time.
