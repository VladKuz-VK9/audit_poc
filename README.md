# Original ReadMe:

# Social Clone Project
This is a social clone project made following the step by step Django Courses

## Thanks
Thanks to Jose Portilla for this amazing course. 

Link to Udemy course
<https://www.udemy.com/python-and-django-full-stack-web-developer-bootcamp/>


# New ReadMe:

## Project Setup:

- Install dependencies:
```
pip install -r requirements.txt
```
- Apply migrations:
```
cd simplesocial 
python manage.py migrate
```
- Create a superuser (you need it to have access to the AuditLog Admin):
```
python manage.py createsuperuser
```
- Run the application:
```
python manage.py runserver
```

## Project Description

Enhanced original Simple Social Clone application with PoC AuditLog capabilities:
1. All requests from the authenticated users are recorded
2. DB responses also recorded if user gets a response from the DB
3. All logs available in the Admin Panel -> AuditLog
4. AuditLog records are not editable or removable
5. For each AuditLog record you can review all DB responses as formatted JSON
6. To export AuditLogs please select all or needed records and activate `Export selected to CSV` action in the Admin Panel