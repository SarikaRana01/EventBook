# EventBook

**EventBook** is a Django-based web application designed to make **event management simple and efficient**. It allows both **organizers** and **attendees** to manage and participate in events seamlessly.

---

## Features

- **Organize events** and manage registrations  
- **View upcoming events** in a clean dashboard  
- **Track attendance** easily  
- User-friendly interface with secure authentication

---

## Tech Stack

- **Backend:** Django  
- **Authentication:** User login & registration  
- **Date & Time Management:** Timezone, datetime handling  
- **Database:** SQLite (default for Django projects)  

---

## Screenshots

![EventBook Screenshot](screenshot.png)  
*Replace `screenshot.png` with your actual screenshot file*

---

## Installation

1. Clone the repository:
```bash
git clone <your-repo-link>
```

2. Navigate to the project directory:
```bash
cd EventBook
```
3. Create a virtual environment:
```bash
python -m venv env
```
4. Activate the virtual environment:
```bash
Windows: env\Scripts\activate

Mac/Linux: source env/bin/activate
```

5. Install dependencies
```bash
pip install -r requirements.txt
```

6. Apply migrations:
```bash
python manage.py migrate
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Open your browser and go to:
```bash
http://127.0.0.1:8000/
```
## Usage

Organizers: Create events, manage registration

Attendees: View events, register for events

## GitHub Repository


Check out the project code here: GitHub Link

## License

This project is licensed under the MIT License.
