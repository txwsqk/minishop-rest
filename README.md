# minishop walkthrough

### Prerequisite

```shell
pip install MySQL-python
pip install django
pip install django-suit==0.2.25
pip install djangorestframework
```

### Summary

I'm a business man selling some productions and you're customer who can buy or comment productions

*Entity*

* User
  1. business : sell productions
  2. customer: buy something from business and comment the productions
* Production
  business  (foreignkey to Userprofile)
* comment
* UserProfile
  extended from django User

*UML*

![](minishop_uml.png)



### Some useful stuff

1. init

   ```
   # create mysql DB
   CREATE DATABASE minishop DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

   # sync table
   python manage.py makemigrations
   python manage.py migrate

   # create superuser
   python manage.py createsuperuser

   # now start
   python manage.py runserver   # default linstening on   127.0.0.1:8000

   # open your browser
   http://127.0.0.1:8000/admin  # admin
   http://127.0.0.1:8000/api  # rest
   ```

   ​

2. create production

```
curl -X POST -H "Content-Type:multipart/form-data"  -H "Authorization: Token 6f26ebdaa63b6f23c69e7095a420d61a412ee297" -F "image=@/Users/quke/pear.jpeg;type=image/jpeg" -F "name=Name" -F "status=online" -F "business=5" -F "instruction=SomeInstruction" -F "recommend_times=3" http://127.0.0.1:8000/api/production/
```

