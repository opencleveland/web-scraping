Quick and Dirty Scraping
========================

This document describes the process of rapidly creating the prototype web
scraping program called clb-scraper.py, as seen in the examples directory of
this repo.  For a more thorough discussion of web scraping, please read the
document called web-scraping-at-the-poverty-center.md.


First, inspect the target
-------------------------
In this case, our target is a site that has around 8,000 records that a user
can browse through 15 at a time.  To analyze this process, we make two 
comparisons.  First, we compare the load of the first page of records with the
load of the second page of records.  This tells us how to initialize our process
and how to take a step forward in the record set.  Using the Chrome developer
tools, I can see the source code and network action of the step to the next
page.  Our target site advances to the next page using  an HTML form to do an 
HTTP POST action.  Next, we compare the code of the second to last page with
the code of the last page -- this tells us how to terminate our process.  Our
target site deactivates the "next page" button on the last page by changing the
name attribute of the button element.

Now that we know how the record browsing process works, we need to figure out
how to extract the data from the page.  Looking at the HTML source of each
page we see that the data we want is always in a table with a unique name
attribute and with the same set of columns on every page -- this is very 
convenient, because we can write a scraper to extract this table element from
each page convert the rows of the table to rows of output data.

Second, pick a tool
-------------------
I would usually use Java and HtmlUnit for a scraping task, but setting up those
tools would require much more explanation than is necessary for the task at
hand.  So, I will pick a tool with less infrastructure required but which still
has great libraries available that will let me ignore a lot of technical
details: Python.

I have never used Python for web scraping before, so I start by searching the
Internet for "web scraping python" -- instantly I find several StackOverflow
questions and answers that give me options for accomplishing my task.  I see an
approach using Qt, which I vaguely know is used for creating user interfaces,
and I see a magic word in the example using Qt: webkit.  Webkit is a browser
engine, which will be ideal for almost any scraping task because it will load
web pages and parse HTML.

Third, make it work
-------------------
Using example code, we initialize the browsing process by reading a URL from
the command line and loading the page at that URL.  Then we write the code that
locates the table on the page and converts the rows to tab-delimited lines of
data.  Finally, we write the code that determines whether we are on the last
page and if so to quit and if not to load the next page of records.  We also
include a delay in between page loads so as not to over load the server.

How did we do?
--------------
This task was easy because the interface being scraped did not have any
complicated features such as search, login, or asynchronous content loading.
We were able to get the data we wanted quickly and in a format we can convert
easily with command-line tools like tr, sed, and grep.  We did not build in
error handling but the whole run takes less than 20 minutes, so the waste of
resources and time in the event of a crash is small.  Making the scraper was
quick, and it works, and we are aware of the dirty details of situations that
could make it fail, but for now our work is done.



