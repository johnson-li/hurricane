Introduction
===

There are so much technology in today's web server development, most of them are beneficial for the web server performance. But to a company, it's important to make out the technology's tradeoff before applying it. This Project aims to measure these tradeoff.

A modern RESTful web sever can be separated into several layers:
 
- present layer (www)
- business logic layer (webrpc)
- persistent storage layer (db)
 
Generally, a web server's performance is determined by the implementation of each layer, and the efficiency of their communication.



Architecture
===
As a benchmark system, this project can be seperated into two parts in design

- persistent parts
	- `api` each layer should provide a consistent outer interface to provide a fair contest environment
- configurable parts
	- `implementation` db provider, etc
	- `communication` different protocols, sync vs async
	- `cache` cache can exist between any 2 layers, but the efficiency and difficulty varies a lot
	
The core of this project is to make use of various configurable parts and compare their performance variance.


Configurable parts
===
The following lists all kinds of configurable parts that the project supports or will support.

- db vendor
    - [x] sqlite3
    - [ ] mysql
    - [ ] mongodb
- www server
    - [x] flask default
    - [ ] flask with gevent
    - [ ] flask with gevent and gunicorn
- webrpc server
    - [x] local call
    - [ ] flask default
    - [ ] flask with gevent
    - [ ] flask with gevent and gunicorn
- network protocol between www and webrpc
    - [x] HTTP/1.x
    - [ ] HTTP/2
    - [ ] TCP
- data expression
    - [x] original data
    - [ ] msgpack
    - [ ] protobuf
- db layer cache
    - [x] no cache
    - [ ] redis
