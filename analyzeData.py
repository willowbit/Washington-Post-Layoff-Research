def simplePrint(person):
    x = "" ## the final result we are going to build

    p = person.asdict()
    preWP, WP, postWP = analyzeJobs(p['jobs'])
    x = x + f"{p['firstname']};{p['lastname']};{p['url']};;;"
    if preWP: x = x + f"{preWP['employer']};{preWP['role']};;{preWP['start']};{preWP['end']};;"
    else: x = x + "None;None;;None;None;;"
    if WP: x = x + f"{WP['employer']};{WP['role']};{WP['start']};{WP['end']};;"
    else: x = x + "None;None;None;None;;"
    if postWP: x = x + f"{postWP['employer']};{postWP['role']};;{postWP['start']};{postWP['end']};;"
    else: x = x + "None;None;;None;None;;"
    try:
        ed = p['education'][0]
        x = x + f"{ed['school']};{ed['degree']};{ed['start']};{ed['end']}"
    except: x = x + "None;None;None;None"
    x = x + "\n"
    return x

def analyzeJobs(jobs):
    preWP = None
    WP = None
    postWP = None
    if jobs:
        for job in jobs:
            if job['employer'] == "The Washington Post":
                WP = jobs.index(job)
                try: preWP = jobs[WP + 1] ## get it
                except: pass
                try: postWP = jobs[WP - 1]
                except: pass
                return preWP, jobs[WP], postWP
        return None, None, None
    else:
        return None, None, None

def analyze(people):
    print("Writing data to file...")
    open('result.txt', 'w')
    with open('result.txt', 'a') as f:
        for person in people:
            x = simplePrint(person)
            f.write(x)