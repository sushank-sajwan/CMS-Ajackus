# CMS-Ajackus - Python/Django Assignment
<br />

# Install python3.7
sudo add-apt-repository ppa:deadsnakes/ppa
<br />
sudo apt install python3.7

# Install PIP
sudo apt install python3-pip


# Install and Create virtualenv
sudo apt install virtualenv
</br>
virtualenv -p python3.7 venv


# Activate the virtualenv
source venv/bin/activate


# install requirement.txt
pip install -r requirements.txt


# Run Migrations
python manage.py makemigrations
<br />
python manage.py migrate


# Create SuperUser
python manage.py createsuperuser --username Ajackus
<br />
Fill up the details for superuser access


# runserver
python manage.py runserver


# API GuideLines:

- auth/login/: Login User (Accepts Username and Email Logins)
- auth/user_import_template/: Download template for creating admin users by seeding.
- auth/seed_admin/: Upload the filled template in proper format to create the admin users.
- auth/register/: Register Author.
- content/fetch/: Fetch the Content. Admin must provide authors list in query_params for which he want data.
- content/create/: Author Can Add Records in CMS, Admin Does not have permission to do it.
- content/edit/<int:pk>/: Users can edit the CMS Records using this API.
- content/delete/<int:pk>/: Users can delete the CMS Records using this API.
- content/search/: Users can use this API to search the desired content - Combination is also supported.
