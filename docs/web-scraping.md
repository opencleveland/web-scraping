Web Scraping
============

This is a technical note describing approaches to web scraping based on the 
experiences of the software development team at the Center on Urban Poverty
and Community Development at Case Western Reserve University.  It is meant as
an anecdotal history of our efforts and an informal introduction to the subject
of web scraping.

TL;DR for best results use a browser simulator.  We like HtmlUnit.


Bad, Ugly, and Necessary
------------------------
Web scraping refers to the process of extracting bulk data from web sites that
have a human-readable interface but no machine-readable interface.  For
instance, many web sites operated by governmental organizations are full of
public records but have interfaces designed to provide access to small sets of
records in human-readable documents.  Researchers and software developers 
interested in accessing the complete data set can use web scraping to extract
data from these interfaces and format the data in a manner suited to analysis.

Ideally, data would be easily 
available, yet it is unrealistic for every organization to build an interface
that fits the needs of every user.  At the same time, web scraping should be
seen as a bad but practical solution to a hard problem.  The primary weakness
of web scraping is that a scraper encodes a method for extracting data for an
existing interface, and the scraper will cease to work when the interface
changes.  The ugly reality is that detecting a change in the interface that
invalidates the assumptions of the scraper design may be difficult or
impossible.  Even with these fundamental problems, web scraping remains a
necessity for those interested in retrieval of data hidden behind limited 
interfaces.




Habits of a Well-Behaved Scraper
--------------------------------
Scraping is
often explicitly disallowed by the terms of use of web sites for a variety of
reasons:

1. Site operators may not want all of the data available in their site to 
   be readily accessible.
2. Scraping may place more load on a web site than the operator is prepared to
   serve.  In the worst case, this can degrade service for all users,
   effectively executing a denial-of-service attack on the site.
3. Scraping creates redundant data which may suffer from quality problems not
   present in the original source.  For instance, scraped data will become
   stale (out of date) when the source data changes.

In response to these concerns, developers of a well-behaved scraper should 
follow these guidelines:

1. Do not violate the terms of use for the site or the data.  Work with the
   site owners and operators to agree upon a special exemption to the terms if
   necessary.
2. Work with the site owners and operators to understand the load they are
   capable of absorbing.  Alternatively, do not scrape data faster than a
   person would browse the site.
3. Always include the data source, time of access, and version number of the
   scraper program in the resulting data set.



Characteristics of Web Scraping Tasks
-------------------------------------
The wide variety of techniques available for building web interfaces, combined
with the wide variety of data available in source systems makes it difficult to
generalize about scraping tasks.  Here we describe some common features of 
tasks we have encountered that demonstrate the difficulties in web scraping
as opposed to web crawling, aka link following.

1. Login / initial form: some sites require use of an initial form which has 
   the effect of changing the state of the session.  The typical result is that
   some data identifying the session is sent to the client and the client must
   send this identifier back to the server with every subsequent request,
   whether as a cookie or request data.
2. Search: some sites require users to search for records rather than offering
   the ability to browse.  Search criteria may include date ranges, record
   identifiers, or any other fields in the data.  Successfully automating a
   search process involves constructing an input file that yields searches that
   return record sets that are distinct (no duplicates across searches) and
   complete (no records left out because too many results were returned).
3. Browse: paging through record sets requires establishing a loop with entry
   conditions, actions to take at each step, and termination conditions.
4. Table and document parsing: once a scraper has managed to search or browse
   to the desired data, the next step is extracting the data from the HTML and
   writing the data to an output file.  Extraction can be performed by various
   means including pattern matching, converting tags to delimiters, and HTML
   parsing.  A browser simulating HTML parser can provide good results because
   some browsers can compensate for irregularities in the HTML.
5. Writing multiple outputs: it is often advantageous to write separate outputs
   for various components of a record set, for instance, the summary results
   from a search in one file and the detailed results for an individual record
   in another.
6. Skipping dead records: in the event that some records are known to be
   historical then a scraper can save time and resources by not fetching this
   data again after it has been fetched once.
7. Job failure and recovery: web requests made by a scraper may fail for any
   number of reasons, and the scraper must be able to recover from errors.
   Without error recovery, scrapers risk wasting time and risk executing 
   redundant requests.


A History of our Approaches
---------------------------
Our first web scraper used Watir, a Ruby web automation framework, to control
a browser running in a separate process.  With this approach while the scraper
is running the browser is open on-screen and the input action of the scraper
is visible, which is comforting but unnecessary.  In our experience, this
approach was effective but suffered from significant drawbacks:

1. Rendering each web page (converting the HTML and images to a layout) creates
   an unnecessary delay in scraping.
2. Browsing action was slow, and the machine running the scraper had CPU
   utilization of 100%, probably due to inefficient interprocess communication
   between the browser and the scraper program.

Our second generation of web scrapers were written in Ruby without any
third-party frameworks.  We built these scrapers by looking at the cookie data
and form data used in the source web sites and creating sequences of HTTP
requests to mimic the requests generated by the browser without needing to
involve a web browser.  This approach was by far the fastest and most efficient
of any we have tried, since we were able to fetch data using one third the
number of HTTP requests as a user would generate using the browser interface.
However, this approach was unable to cope with later needs, specifically
scraping data from JavaScript-driven interfaces.

Our current generation of web scrapers combine lessons learned from the earlier
generations, as enabled by a third-party Java component: a browser simulator called
HtmlUnit.  HtmlUnit is avoids the interprocess communication and rendering
issues encountered by our early scrapers and is also able to interpret
JavaScript-driven interfaces, making it more useful that our second generation
scrapers.  We use a wrapper over the base HtmlUnit functionality that improves
error recovery and simplifies interactions with the current document for
common tasks such as typing into a field and clicking an element.  Also useful
is that HtmlUnit includes HTML parsing capabilities, which decreases the
effort of extracting data from documents. 


Final Notes
-----------
Our experience is not comprehensive of all the situations one may encouter
when web scraping, but it is likely similar to many basic scraping tasks.  The
techniques we discuss here will address a wide range of scenarios in basic web
scraping, yet not all aspects of our approach will be necessary for every task.
Due to fundamental issues, scraping will never be perfect solution to data
access, but with careful consideration scraping can be a practical means to 
increase availability of data for research.



