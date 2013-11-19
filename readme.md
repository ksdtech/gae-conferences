Parent Teacher Conferences
==========================

A web app built with the Ferris Framework.

Ferris code cloned from develop branch on Bitbucket:
 
    From b4e00ee3745a30bc73568ea09cfdca6aedcffee1 Mon Sep 17 00:00:00 2001
    From: Jon Wayne Parrott <jjramone13@gmail.com>
    Date: Wed, 13 Nov 2013 13:49:40 -0500
    Subject: [PATCH] decode_key now checks if the parameter is already a key
    
    
Using This App With PowerSchool
-------------------------------

For enrollments, use DDE on CC records and select these fields:

SchoolID
[01]Student_Number
[05]TeacherNumber
Course_Number
SectionID
[03]Expression


TODO
----

Having trouble using webapp2\_extras auth module. Perhaps we're 
saving to a different session store? Log shows:

    WARNING  2013-11-17 09:29:51,441 securecookie.py:77] Invalid cookie signature 

User authentication (for students/guardians) based on this skeleton project:

    https://github.com/abahgat/webapp2-user-accounts


The Ferris Framework
--------------------

Ferris is a web framework written in Python for App Engine, inspired by: Ruby on Rails, CakePHP, Django, and Flask. Unlike most other frameworks, Ferris is designed specifically for App Engine.

For information and documentation:

    http://ferrisframework.org/

For help and questions: 

    https://groups.google.com/forum/?fromgroups#!forum/ferris-framework


Starting a new project
----------------------

Checkout a copy of Ferris using git:

    git clone git@bitbucket.org:cloudsherpas/ferris-framework.git
    cd ferris-framework

Use git to export ferris to your project directory (trailing slash is important!):

    git checkout-index -a -f --prefix=/project-directory/

You're ready to go, just open your project directory and  run the app engine server.


License
-------

Ferris is licensed under the Apache License, Version 2.

Third-party libraries that are in the packages directory have varying licenses. Please check the license file that's with each package.

WTForms: BSD
ProtoPigeon: Apache License v2
PyTZ: MIT
GData Client Library: Apache License v2
Google API Python Client Library: Apache License v2
OAuth2 Client: Apache License v2
