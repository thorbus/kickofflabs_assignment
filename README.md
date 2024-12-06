
# Event Calendar App

This repository contains a simple yet functional personal calendar application that enables users to create, view, edit, and delete events/meetings. The project is built with Django for the backend and ReactJS for the frontend, incorporating user authentication to ensure data privacy and security.






## Run Locally

Clone the project

```bash
  git clone https://github.com/thorbus/kickofflabs_assignment.git
```

Go to the project directory

```bash
  cd event_calendar_backend
```

Install dependencies

```bash
  pip install -r requirements.txt

```

Run Database Migration
```bash
  python manage.py migrate

```

Start the server

```bash
  python manage.py runserver

```


## Environment Variables



## Features


User Authentication: Secure user login and registration system. 

Event Management:
Create new events/meetings with details such as title, description, date, and time.  
     View all events in a user-friendly calendar interface. 
    
Edit existing events to update details.

 Delete events no longer needed.

UI: Intuitive user interface built with ReactJS.

API Integration: RESTful APIs for seamless communication between the frontend and backend
