# Washington Post Layoff Research

A python script tracking the outcomes of the 300+ Washington Post terminated employees. The script takes as input a folder of LinkedIn webpages (downloaded as .txt on a Firefox browser) and analyzes the data using RegEx to create a "Person" object for each profile. Each object includes a list of their past employment and education.

The script consists of four files:
* `person.py`—The `person` object
* `main.py`—the first file run, calls `getData` and `analyzeData`
* `getData.py`—iterates through `WaPo Profiles/`, gets the data, and formats it into a new Person object for each profile
* `analyzeData.py`—takes person objects and prints it in a readable form that can be imported into a spreadsheet.

To Do:
- [x] Scrape names, linkedin URL, employment, and education
- [x] Parse employment to mark pre-WaPo, WaPo, and post-WaPo positions
- [ ] Add comments throughout code