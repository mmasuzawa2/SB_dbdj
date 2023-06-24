### Conceptual Exercise

Answer the following questions below:

- What is PostgreSQL?
a database management system

- What is the difference between SQL and PostgreSQL?
SQL is a type of language to manipulate database. PostgreSQL is a program that manages the database.

- In `psql`, how do you connect to a database?
having 'psql' command enabled, 'psql {database name}'

- What is the difference between `HAVING` and `WHERE`?
if there is a GROUP BY clause, WHERE would take place before HAVING.

- What is the difference between an `INNER` and `OUTER` join?
INNER joins are joined by reference where as OUTER joins are joined regardless of relationships.

- What is the difference between a `LEFT OUTER` and `RIGHT OUTER` join?
The LEFT JOIN includes all records from the left side and matched rows from the right table, 
whereas RIGHT JOIN returns all rows from the right side and unmatched rows from the left table

- What is an ORM? What do they do?
Like SQLAlechemy, ORM allows you to define regular Python objects and methods and translates them into low-level SQL database instructions for you.

- What are some differences between making HTTP requests using AJAX and from the server side using a library like `requests`?
  One main difference is with AJAX, request is done on user side via browser, which means they have access to communication in detail. 
  If it is handled on server side, much of the data being sent and received are not visible to user machine. 
  

- What is CSRF? What is the purpose of the CSRF token?
Cross site request forgery is type of attack where a browser is tricked into processing some kind of data. 
By using CSRF token and config 'SECERET_KEY' , integrity of data can be verified. 

- What is the purpose of `form.hidden_tag()`?
to add a hidden token to the form
