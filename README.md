## Readme for SE project UE16CS402

### This is the repository for the UI of the project.

* Install and setup git
* Clone the repository
* Create your own branch ``git checkout -b `branch_name` ``
* ## Do not work on the master branch. Always work on your own branch

### Commit and push your changes

* Once you have made all your changes in your branch, commit it.
* `git add .`
* `git commit -m "commit_message"`
* `git push origin "branch_name"`
* Once committed, create a pull request against the `staging` branch.

### Initilizing the project
* Install postgresql 11 `sudo apt-get install postgresql`
* Install redis-server `sudo apt-get install redis-server`
* Create python3 virtualenv using `python3 -m venv venv`
* `sudo passwd postgres`
* Inside postgres shell `ALTER USER postgres PASSWORD 'postgres';`

### Running the project

* `source venv/bin/activate`
* `cd npo_backend`
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py runserver`