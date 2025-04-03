# Trip Planner

A comprehensive travel planning web application built with Django that allows users to create, manage, and share detailed trip plans.

## Features

- **User Authentication**: Sign up, login, and profile management with profile photos
- **Trip Management**: Create, view, edit, and delete trip plans
- **Itinerary Planning**: Add activities with dates and times
- **Budget Tracking**: Monitor expenses by category (transportation, accommodation, food, etc.)
- **Photo Sharing**: Upload and caption photos for your trips
- **Social Features**: Comment on trips and photos
- **Reactions System**: React to trips, photos, and comments with six different reaction types
- **PDF Download**: Generate printable versions of trip details
- **Exploration**: Browse and discover other users' trip plans

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **CSS Framework**: Bootstrap 5
- **Database**: SQLite (development)
- **Image Handling**: Pillow
- **Icons**: Font Awesome

## Installation

1. Clone the repository
```bash
git clone https://github.com/your-username/trip-planner.git
cd trip-planner
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Apply migrations
```bash
python manage.py migrate
```

5. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```

7. Visit http://127.0.0.1:8000/ in your browser

## Usage

- Register a new account or log in
- Create a new trip from your profile
- Add itinerary items, budget entries, and photos to your trip
- Explore other users' trips for inspiration
- Comment and react to trips you like
- Download trip details as PDF for offline reference

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Django
- UI designed with Bootstrap
- Icons from Font Awesome
