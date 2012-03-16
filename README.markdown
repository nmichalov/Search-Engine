HS Search Engine
================


Overview
--------

HS Search Engine consists of three distinct parts:
*Crawl*: takes a set of starting URLs, which should point to the main/index/root page of the target site.  The crawler will then
recursively crawls all pages within each of those sites, storing the text content of each page, and returning all the external links that it finds.

*Index*: uses the simserver package created by Radim Rahurek to generate a semantic representation of each of the pages found.
Specifically, a latent semantic vector space which utilizes latent semantic indexing (for more info see: http://en.wikipedia.org/wiki/Latent_semantic_indexing).

*Query*: queries the semantic model(s) and returns a list of URLs which point to potentially relevant matches (ranked from most to least likely). 
The results are obtained by transforming the user's query into a vector, which is then projected into the existent semantic space(s).  The area around 
the user query vector is then searched, and all those pages whose vector representations fall within some minimum distance are returned as possible 
matches, which are put into a list and sorted from with the nearest neighbor first (the distance between vector representations correlates positively 
with semantic distance between the text content of those pages).



Using HS Search Engine
----------------------

HS Search engine is designed to be run as concurrently on a cluster of machines.  This is accomplished by integrating the Pyro4 python remote objects module 
and the threading/Queue modules in the python standard library.  HS Search Engine can be run on a single machine, but multiple terminals must be used 
to mimic the setup of a multi-machine cluster.  

I intend to develop this section in much greater detail, but for now the theoretical implementation of HS Search Engine can be briefly described as follows:

(Note that the below assumes you are somewhat familiar with Pyro4, an assumption I intend to abandon in subsequent README files.  For now however, 
the documentation for Pyro4 can be found here: http://packages.python.org/Pyro4/)


*prep*
All three portions of HS Search Engine operate largely autonomously.  A more user friendly, high-level, control script is planned, but has not 
yet been created.  Utilizing HS Search Engine therefore requires explicit implementation of each of the three major portions of the code.

Each of the three portions of HS Search Engine require the following setup operations.

1 All the nodes within the cluster which will be used should have the HS Search Engine package and its dependencies installed.  If only a single machine is being used,
multiple terminals must be used.

2 Three or more distinct terminals must be used.  The distribution of the operations is flexible, but each of the following must have a dedicated terminal.
- A nameserver.  This is an optional element in Pyro4, but is currently required in HS Search Engine.  The nameserver indexes remote object URIs with simplified 
names.  When started, the nameserver host's IP address will be requested.  This is the IP address of the machine on which the nameserver is running, and 
must be provided. 
- The remote objects charged with the tasks should then be implemented, with one on each of the dedicated nodes being utilized by the cluster.  For crawling 
this is the DistCrawler, for Indexing this is the SearchServer, and for Querying this is the QueryIndex (the next update will ensure that 
more consistent naming is used.  Each remote object will request the IP address of its host (the machine on which it's running) and a unique identifier.  
Remote objects **must** be identified by numeric index, i.e. each remote object of a specific type should have a unique identifier corresponding to a value 
between 0 and n-1, where n is the number of remote objects of that type.  So, for example, if three remote instances of DistCrawler are going to be used, then the first 
DistCrawler instance should be given the identifier 0, the second should be given the identifier 1, and the third should be given the identifier 2.
- After the nameserver and each of the remote objects has been instantiated, the corresponding Director object should be created (it is assumed that the Director 
will be run on what is essentially the client machine, but this isn't a necessity.  Only one instance of the Director should be used. The purpose of the Director is to 
delegate tasks to, and integrate data received from, each of the remote objects.  Upon instantiation, the Director will request the IP address of the machine serving as the 
host of the nameserver, and the number of corresponding remote objects that exist. 



*crawl*
The first task is to crawl for the desired content.  A set of seed URLs should be put in a text file called URLlist (no extension) with one URL per line, and saved in the directory from which 
CrawlDirector will be called.  The crawling process is acomplished by first starting a nameserver, and then starting the desired number of DistCrawler remote objects which will be used.  
After the nameserver and all the DistCrawler instances are running, CrawlDirector should be called.  It will delegate the URLs in URLlist to each of the remote crawlers.  Successive iterations
of CrawlDirector should result in it appending new URLs returned by the remote DistCrawlers to its 'target\_urls' list, and passing these onto the remote DistCrawlers for crawling.

(note, the Crawl package included in HS Search Engine utilizes a queue of target URLs in CrawlDirector which passes a single URL to each DistCrawler object as it becomes available.  During testing 
however, a single machine implementation of the Crawl portion of HS Search Engine resulted in a high number page return errors.  I've been unable to ascertain exactly why this happens, but a bit 
of research on StackOverflow suggests that it may be that despite the fact that each DistCrawler object crawls a different set of pages, and paces out its own page requests, multiple such 
objects might request different pages from the same from the same host or DNS server at a higher than expected rate, and if all the requests originate from the same IP, the requests might be denied. 
If this occurs, the DistCrawler package at github.com/nmichalov.com/DistIndexer can be used instead, as rather than delegate URLs one at a time from a central queue, it divides the list of target urls 
into a set of smaller lists, each of which is given to a remote DistCrawler object, and results in a slower paced crawl of the target sites).

Page content (that is, the text of each crawled page) is stored remotely on the DistCrawler instance's host machine.



*Index*
Indexing the collected page content requires setup similar to that needed for Crawl.  First a nameserver is created, then each of the remote object instances should be instantiated on those nodes which 
served as DistCrawler hosts.  These remote SearchServer.py objects should be called from the same directory that as the one used to call the DistCrawler objects.  This is to insure that the SearchServer 
remote objects have access to the page content gathered during the crawl.

After the nameserver and remote SearchServer objects are running, IndexDirector should be run.  This will automatically call the necessary methods on each remote SearchServer object.




*Query*
Querying the collected data is accomplished by first starting a nameserver, and then running an instance of QueryIndex on each of the nodes hosting a document index.

After the nameserver and all the required QueryIndex objects are running, running an instance of the QueryDirector object on the client machine will prompt the user to enter a query.  The user input is then 
passed to each of the remote QueryIndex objects, which searches the document index stored there, and returns all the possible matches.  These results are returned to the client machine, which sorts them into 
an ordered list, and displays them via stdout.









Misc
----

As it stands, HS Search Engine is functional, but it's rather fragile, and somewhat cumbersome to use.  The code is also in desperate need of refactoring.  I intend to address these issues, as well as several 
others (mostly aimed at improving the storage of the document indexes, their ability to share data, and hopefully converting to a topic model, rather than a semantic space model).  For the moment however, I plan 
on taking a break to focus on some other projects I've been putting off.  If you've somehow stumbled upon HS Search Engine and are interested in it, feel free to use it, or any part of it, as you see fit.  
