### Requirements
#### Python
This project was created using Python 3.6.5 so the application should be run using this version or higher.
#### pip
https://pip.pypa.io/en/stable/installing/
#### virtualenv
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#installing-virtualenv
#### git
https://git-scm.com/download/mac

### Data Assumptions
It is assumed that the attribute to use as the unique identifer is 'index', as this is present in both the provided companies.json and people.json files. As this is a zero based index, and Django AutoField's (across some DBs) do not accept zero values, **the initialise process will increment all index values by +1**. It is important to note this when querying the API.

If a person in people.json has a company_id attribute that does not exist in companies.json, company_id will be saved as null.

If a person in people.json has a friend which does not exist in the file, the import process will fail and no data will be imported.

### Installation
This guide assumes you are using MacOS
- Be sure your terminal is within the directory you would like to install the application to
- Clone repository `git clone https://github.com/brett-matthews/colony-friends`
- `cd colony-friends`
- Create a virtualenv for the project dependencies to install to `virtualenv venv`
- Activate virtualenv `source venv/bin/activate`
- Install dependencies `pip install -r requirements.txt`


### Data Initialisation
Following on from the above steps
- `cd colonyfriends`
- Database migrate `
