## Error Handling
Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "status_code": 400,
    "message": "Bad Request"
}
```

The API will return three error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Unprocessable Entity
500: Internal Error


## Endpoints

## Resource: Volunteer

### GET `/volunteers`
- Fetches a list of volunteers with detailed information
- Request Arguments: None
- Sample Response
```
{
    "count": 1,
    "volunteers": [
        {
            "email": "stella@me.com",
            "id": 1,
            "name": "Stella",
            "seeking_student": "True"
        }
    ]
}
```

### GET `/volunteer/<volunteer_id>`
- Fetches a volunteer information given the ID
- Request Arguments: volunteer ID
- Sample Response
```
{
    "age": 15,
    "email": "stella@me.com",
    "id": 1,
    "name": "Stella",
    "seeking_description": "Teaches Chinese, Maths, English",
    "seeking_student": "True"
}
```

### POST `/volunteer/register`
- Creates a volunteer profile.
- Sample Body
```
{
    "name": "stella",
    "age": 15,
    "gender": "Female",
    "email": "stella@me.com",
    "image_link": "https://media.licdn.com/media/AAYQAQSOAAgAAQAAAAAAABy3-hIQRcT8QpykdK6OdWi7yQ.png",
    "profile_link": "",
    "seeking_student": "Yes",
    "seeking_description": "Teaches Chinese, Maths, English"
}
```
- Success Response
```
{"success": True}
```

### PATCH `volunteer/<volunteer_id>`
- Patches a specific volunteer given its ID.
- Request Arguments: volunteer ID
- Sample Body
```
{
    "seeking_student": "No",
    "seeking_description": ""
}
```
- Success Response
```
{"success": True}
```

### DELETE `/volunteer/<volunteer_id>`
- Deletes a specific volunteer given its ID.
- Request Arguments: volunteer ID
- Success Response
```
{
    "success": True
}
```

### POST `/volunteers/search`
- Get a list of volunteers based on a search term in name or description, not case sensitive.
- Sample Body
```
{
  "searchTerm": English
}
```
- Sample Response
```
{
    "count": 1,
    "search_term": "English",
    "volunteers": [
        {
            "age": 15,
            "email": "stella@me.com",
            "id": 1,
            "name": "Stella",
            "seeking_description": "Teaches Chinese, Maths, English",
            "seeking_student": "True"
        }
    ]
}
```


## Resource: Student

### GET `/students`
- Fetches a list of students with detailed information
- Request Arguments: None
- Sample Response
```
{
    "count": 1,
    "volunteers": [
        {
            "email": "micheal@me.com",
            "id": 1,
            "name": "Micheal",
            "seeking_volunteer": "True"
        }
    ]
}
```

### GET `/student/<student_id>`
- Fetches a student information given the ID
- Request Arguments: None
- Sample Response
```
{
    "age": 9,
    "email": "micheal@me.com",
    "id": 1,
    "name": "Micheal",
    "seeking_description": "I want to practice my Chinese, and English!",
    "seeking_volunteer": "True"
}
```

### POST `/student/register`
- Creates a student profile.
- Sample Body
```
{
    "name": "Michael",
    "age": 9,
    "gender": "Male",
    "email": "michael@me.com",
    "image_link": "https://media.licdn.com/media/AAYQAQSOAAgAAQAAAAAAABy3-hIQRcT8QpykdK6OdWi7yQ.png",
    "profile_link": "",
    "seeking_volunteer": "No",
    "seeking_description": ""
}
```
- Success Response
```
{"success": True}
```

### PATCH `student/<student_id>`
- Patches a specific student given its ID.
- Request Arguments: student ID
- Sample Body
```
{
    "seeking_volunteer": "Yes",
    "seeking_description": "Teaches Chinese, Maths, English"
}
```
- Success Response
```
{"success": True}
```

### DELETE `/student/<student_id>`
- Deletes a specific student given its ID.
- Request Arguments: student ID
- Success Response
```
{
    "success": True
}
```

### POST `/students/search`
- Get a list of students based on a search term in name or description, not case sensitive.
- Sample Body
```
{
  "searchTerm": English
}
```
- Sample Response
```
{
    "count": 1,
    "search_term": "Chinese",
    "students": [
        {
            "age": 9,
            "email": "micheal@me.com",
            "id": 1,
            "name": "Micheal",
            "seeking_description": "I want to practice my Chinese, and English!",
            "seeking_volunteer": "True"
        }
    ]
}
```

## Resource: Classroom

### GET `classroom/<classroom_id>`
- Fetch one classroom given its ID
- Request Arguments: classroom ID
- Sample Response
```
{
    "description": "English practice",
    "end_date": "None",
    "id": 3,
    "start_date": "2021-02-01",
    "student_id": 1,
    "time": "09:00:00",
    "volunteer_id": 1
}
```

### GET `/volunteer/<volunteer_id>/classrooms`
- Fetches a list of classrooms owned by a given volunteer
- Request Arguments: volunteer ID
- Sample Response
```
{
    "classrooms": [
        {
            "description": "English practice",
            "end_date": "2021-03-01",
            "id": 3,
            "start_date": "2021-02-01",
            "student_id": 1,
            "student_name": "Micheal",
            "time": "08:00:00",
            "volunteer_id": 1
        }
    ],
    "count": 1,
    "volunteer_id": 1,
    "volunteer_name": "Stella"
}
```

### GET `/student/<student_id>/classrooms`
- Fetches a list of classrooms owned by a given student
- Request Arguments: student ID
- Sample Response
```
{
    "classrooms": [
        {
            "description": "English practice",
            "end_date": "2021-03-01",
            "id": 3,
            "start_date": "2021-02-01",
            "student_id": 1,
            "time": "08:00:00",
            "volunteer_id": 1,
            "volunteer_name": "Stella"
        }
    ],
    "count": 1,
    "student_id": 1,
    "student_name": "Micheal"
}
```

### PATCH `classroom/<classroom_id>`
- Patches a specific classroom given its ID.
- Request Arguments: classroom ID
- Sample Body
```
{
    "time": "09:00",
    "end_date": null
}
```
- Success Response
```
{"success": True}
```

### DELETE `/classroom/<classroom_id>`
- Deletes a specific classroom given its ID.
- Request Arguments: classroom ID
- Success Response
```
{
    "success": True
}
```

