"""
What does this programme do?
 Given link to courses in BASIS such as this one:

 https://basis.uni-bonn.de/qisserver/
 rds?state=wtree&search=1&trex=step&root120151=108340|123654|123689|123672&P.vx=lang

 it will create single ICS file with all the appointments,
 which you can later import to Google Calendar, MS Outlook, Thunderbird,
 or your favourite Calendar, assuming it accepts ICS file
"""

__author__ = 'vladimir stashkov'

import urllib2
import re
import os

def get_id_courses(url):
    """
    :param url:
    :return: ID of appointments for each subject
    """
    response = urllib2.urlopen(url)
    data = response.read()      # a 'bytes' object
    text = data.decode('utf-8')  # a 'str'; this step can't be used if data is binary

    publish_ids = []
    for m in re.finditer('(?<=publishid=)[0-9]+(?=&amp;moduleCall=iCalendar)', text):
       publish_ids.append(text[m.start(): m.end()])

    publish_ids = [x.encode('utf-8') for x in publish_ids]
    return publish_ids

def get_id(url):
    """
    :param url:
    :return: 2 arrays of IDs and description of IDs for each subject
    """
    #print "downloading IDs of courses from specified URL..."
    response = urllib2.urlopen(url)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8')  # a `str`; this step can't be used if data is binary

    publish_ids = []
    description = []
    #for m in re.finditer('(?<=publishid=)[0-9]+(?=&amp)', text):
    #    print text[m.start(): m.end()]

    #find all lines that contain "publishid="
    lines = re.findall('^.*publishid=.*$', text, flags=re.MULTILINE)
    for line in lines:
        publish_ids += re.findall('(?<=publishid=)[0-9]+(?=&amp)', line)
        description += re.findall('(?<=title="Mehr Informationen zu ).*(?=")', line)


    # found some ID's which do not belong here
    #print len(publish_ids), len(description)
    while not(len(publish_ids) == len(description)):
        publish_ids.pop(0)

    publish_ids = [x.encode('utf-8') for x in publish_ids]
    description = [x.encode('utf-8') for x in description]
    description = [x.replace('/', ' ') for x in description]

    print '\n'
    print '----START LIST OF COURSE FOUND----'
    for i in range(len(publish_ids)):
        print publish_ids[i], description[i]
    print '----END LIST OF COURSE FOUND----\n'

    # no courses
    if len(publish_ids) == 0:  # found no courses
        print 'Incorrect URL. Exiting...'
        exit()

    return publish_ids, description


def get_subj_id(courses_id):
    """
    :param courses_id:
    :return: return ID's of ics appointments
    """
    subj_ids = []
    print 'Looking for appointments for each subject...'
    for item in courses_id:
        subj_url = 'https://basis.uni-bonn.de/qisserver/rds?state=verpub' \
                   'lish&status=init&vmfile=no&publishid=' + item + '&modu' \
                   'leCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung'
        subj_temp = get_id_courses(subj_url)
        subj_ids.append(subj_temp)
    subj_ids = [item for sublist in subj_ids for item in sublist]
    return subj_ids



def download_and_merge_ics(subj_ids, path):
    """
    :param subj_ids: ids of subjects
    :param path: path where to save the file
    :return: path where the file was saved
    """
    ical_ids = []

    # if the file exists delete it
    try:
        os.remove(os.path.join(path, 'TimeTable.ics'))
    except OSError:
        pass

    # create big file out of all of the ics calendars
    print 'Opening the file: ' + str(os.path.join(path, 'TimeTable.ics'))
    local_file = open(os.path.join(path, 'TimeTable.ics'), 'a')
    local_file.write('BEGIN:VCALENDAR\n')  # beginning of the calendar

    for i in subj_ids:
        ics_calendar_url = 'https://basis.uni-bonn.de/qisserver/rds?state=verpu' \
                           'blish&status=transform&vmfile=no&publishid=' + i + '&modu' \
                           'leCall=iCalendar&publishConfFile=reports&publishSubDi' \
                             'r=veranstaltung'
        f = urllib2.urlopen(ics_calendar_url)
        text = f.read()
        text = text.replace('BEGIN:VCALENDAR\n', '')
        text = text.replace('END:VCALENDAR\n', '')
        local_file.write(text)

        print 'Writing appointments to the file...' + str(subj_ids.index(i)+1) + '/' + str(len(subj_ids))

    local_file.write('END:VCALENDAR\n')  # end of the calendar
    print 'Closing the file: ' + str(os.path.join(path, 'TimeTable.ics'))
    local_file.close()  # close the file
    return path


def main():

    # example url
    # initial_url = 'https://basis.uni-bonn.de/qisserver/rds?state=wtree' \
    #               '&search=1&trex=step&root120152=125965|130651|130664&P.vx=lang'

    initial_url = raw_input('paste url with courses: ')

    # get id of courses, their descriptions and print it
    courses_ids, description = get_id(initial_url)
    # for each of the id of a course get all of the appointments
    appointment_ids = get_subj_id(courses_ids)
    # download all of the appointments and merge them in 1 file
    save_to_path = os.path.expanduser('~') + '/Downloads/'
    saved_file = download_and_merge_ics(appointment_ids, save_to_path)

    print '\nFile was saved to: ' + str(saved_file)


if __name__ == "__main__":
    main()
