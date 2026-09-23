import os
from person import Person
from dateutil import parser
import re
import csv

people = [] # this is going to be our final result

def processDate(d):
    if d:
        if d == "Present":
            return "Present"
        else:
            return parser.parse(d).strftime("%m-%d-%Y")
    else: return None

def analyzeExp(exp): ## we are going to return a list of dictionaries

    jobList = []

    pattern = r'((?:-{72}|Experience)((?:\n\n(?:.*)\n\n)(?:(?:(?P<url>.*)\n\n(?P<employer>.*))|(?P<_url>.*www.linkedin.com.*)\n\n(?P<role>.*)\n\n(?P<_employer>.*)|(.*))\n\n(?:(?P<start>(?:\w{3}\s)?\d{4})\s(-|–)\s(?P<end>(?:\w{3}\s)?\d{4}|Present)|.*(?:(?:yrs|mos)).*)))'
    matches = re.finditer(pattern, exp)

    ## flatten dictionary into a nice one
    for match in matches:
        newDict = {}
        match = match.groupdict()
        if match['url']:
            if match['employer']:
                match['employer'] = match['employer'].split(" · ")[0]
            newDict.update({
                'url': match['url'],
                'employer': match['employer'],
                'role': None,
                'start': processDate(match['start']),
                'end': processDate(match['end'])
            })
        else:
            if match['_employer']:
                match['_employer'] = match['_employer'].split(" · ")[0]
            newDict.update({
                'url': match['_url'],
                'employer': match['_employer'],
                'role': match['role'],
                'start': processDate(match['start']),
                'end': processDate(match['end'])
            })
        jobList.append(newDict)

    return jobList


def analyzeEdu(exp):

    eduList = []

    pattern = r'((?:-{72}|Education)(?:\n\n(?:.*)\n\n)(?:(?:(?P<url>.*)\n\n(?P<school>.*))|(?P<_url>.*www.linkedin.com\/school.*)\n\n(?P<_school>.*)\n\n(?P<degree>.*)|(.*))\n\n(?:(?P<start>(?:\w{3}\s)?\d{4})\s(-|–)\s(?P<end>(?:\w{3}\s)?\d{4}|Present)|.*(?:(?:yrs|mos)).*))'
    matches = re.finditer(pattern, exp)

    ## flatten dictionary into a nice one
    for match in matches:
        newDict = {}
        match = match.groupdict()
        if match['url']:
            newDict.update({
                'url': match['url'],
                'school': match['school'],
                'degree': None,
                'start': processDate(match['start']),
                'end': processDate(match['end'])
            })
        else:
            newDict.update({
                'url': match['_url'],
                'school': match['_school'],
                'degree': match['degree'],
                'start': processDate(match['start']),
                'end': processDate(match['end'])
            })
        eduList.append(newDict)

    return eduList

def parsePerson(person):
    mexp = re.search(r'((Experience)(?=(?:\n\n(?:.*)\n\n)(?:(?:(?P<url>.*)\n\n(?P<employer>.*))|(?P<_url>.*www.linkedin.com.*)\n\n(?P<role>.*)\n\n(?P<_employer>.*)|(.*))\n\n(?:(?P<start>(?:\w{3}\s)?\d{4})\s(-|–)\s(?P<end>(?:\w{3}\s)?\d{4}|Present)|.*(?:(?:yrs|mos)).*)))', person)
    medu = re.search(r'((Education)(?=(?:\n\n(?:.*)\n\n)(?:(?:(?P<url>.*)\n\n(?P<employer>.*))|(?P<_url>.*www.linkedin.com.*)\n\n(?P<role>.*)\n\n(?P<_employer>.*)|(.*))\n\n(?:(?P<start>(?:\w{3}\s)?\d{4})\s(-|–)\s(?P<end>(?:\w{3}\s)?\d{4}|Present)|.*(?:(?:yrs|mos)).*)))', person)
    if mexp == None and medu == None:
        return None, None
    if mexp == None:
        edustart = medu.start()
        EDU_STR = medu.string[edustart:]
        return None, EDU_STR
    if medu == None:
        expstart = mexp.start()
        EXP_STR = mexp.string[expstart:]
        return  EXP_STR, None
    else:
        expstart = mexp.start()
        edustart = medu.start()
        
        EXP_STR = mexp.string[expstart:edustart]
        EDU_STR = mexp.string[edustart:]

        return EXP_STR, EDU_STR


def getNameAndURL(person):
    person = person.split('\n')
    person = list(filter(None, person))
    person = list(map(str.strip, person))
    if "Skip to aside" in person: ## get rid of an element that sometimes appears and messes up the order
        person.remove("Skip to aside")

    name = person[22].split()
    firstname = ' '.join(name[:-1])
    lastname = name[-1]
    url = person[24].strip('<').strip('>')
    return firstname, lastname, url

def analyzePerson(person):

    ## get split file
    EXP_STR, EDU_STR = parsePerson(person)

    ## get results from other funcs
    if EXP_STR:
        jobs = analyzeExp(EXP_STR)
    else: jobs = None
    if EDU_STR:
        education = analyzeEdu(EDU_STR)
    else: education = None
    
    firstname, lastname, url = getNameAndURL(person)

    return firstname, lastname, url, jobs, education

def assemble(person, personIndex):
    
    ## get all the data
    firstname, lastname, url, jobs, education = analyzePerson(person)

    ## assemble data
    if firstname:
        newPerson = Person(firstname, lastname, url, jobs, education)
        people.append(newPerson)

def main():
    # iterate over 'WaPo Profiles' folder and start analysis
    directory = 'All Profiles'

    index = 0

    print("Iterating through directory \"" + directory + "\"")
    for entry in os.scandir(directory):
        # if index == 1: # temporarily limit amount
        #     break
        index = index + 1
        if entry.is_file():  # check if it's a file
            if 'Experience'in entry.path:
                continue
            else:
                with open(entry.path) as f:
                    person = f.read()
                    assemble(person, index) # send string with data

    return people