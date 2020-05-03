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

#### Assumption
  It is expected that init_companies will always be run first before init_people.

#### Steps
Following on from the Installation Steps
Set settings file, migrate the database, initialise companies and initialise people 
```
  export DJANGO_SETTINGS_MODULE=colonyfriends.settings
```
```
  python manage.py migrate
```
```
  python manage.py init_companies
```
```
  python manage.py init_people
```

#### Other files?
The init_companies and init_people commands can accept an optional parameter to use a different path, example shown below.
```
  python manage.py init_people '/Users/johnsmith/repos/colony-friends/assets/companies.json'
```
#### Reset
If using SQLite, it is possible to clear all the initialised data using this command.
```
  python manage.py reset_sqlite_app_data
```

### Unit Tests
```
  python manage.py test
```
### Running
```
  python manage.py runserver
```
### API Spec
1. Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.
  
http://localhost:8000/api/company/1/employees/
 
 2. Given 2 people, provides their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive. Where 1 and 2 are indexes of people as specified in source data. **note please see index in Data Assumption section**
 
http://localhost:8000/api/people/common-friends/?id=1,2,3&eye_colour=brown&has_died=0

3. Given 1 person, provides a list of fruits and vegetables they like. This endpoint respects this interface for the output:
 {"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}

http://localhost:8000/api/people/1/
 
