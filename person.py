class Person:
    
    def __init__(self, firstname, lastname, url, jobs, education):
        self.firstname = firstname
        self.lastname = lastname
        self.url = url
        self.jobs = jobs
        self.education = education

    def asdict(self):
        return {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'url': self.url,
            'email': '',
            'phone': '',
            'jobs': self.jobs,
            'education': self.education
        }