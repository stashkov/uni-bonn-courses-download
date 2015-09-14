# uni-bonn-courses-download
download info from BASIS about date	ime of the courses and create single .ics Calendar file

###input: url link


###output: TimeTable.ics file

What does this programme do?
Given link to courses in BASIS such as this one:

 https://basis.uni-bonn.de/qisserver/rds?state=wtree&search=1&trex=step&root120151=108340|123654|123689|123672&P.vx=lang

the programme will create single ICS file with all the appointments,
which you can later import to Google Calendar, MS Outlook, Thunderbird,
or your favourite Calendar, assuming it accepts .ics file



### USAGE EXAMPLE
vladimir@Yoga-2 ~/PycharmProjects/basis_timetable $ python TimeTable.py 
paste url with courses: https://basis.uni-bonn.de/qisserver/rds?state=wtree&search=1&trex=step&root120151=108340|123654|123689|123672&P.vx=lang


----START LIST OF COURSE FOUND----
97259 V4C2   MA-INF 1201 - Approximation Algorithms
...OMITTED LINES...
96981 MA-INF 1315 - Lab Computational Geometry
----END LIST OF COURSE FOUND----

Looking for appointments for each subject...
Opening the file: /home/vladimir/Downloads/TimeTable/TimeTable.ics
Writing appointments to the file...1/36
...OMITTED LINES...
Writing appointments to the file...36/36
Closing the file: /home/vladimir/Downloads/TimeTable/TimeTable.ics

File was saved to: /home/vladimir/Downloads/TimeTable/
