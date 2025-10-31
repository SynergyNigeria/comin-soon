# COVU Market - Nigerian E-commerce Marketplace

COVU Market is a transparent, secure, and fair e-commerce platform designed for Nigerian fashion entrepreneurs. This project features a modern coming soon/notify page, live seller statistics, email verification, and a mobile-friendly, trust-focused landing page.

## Features

- **Coming Soon Landing Page**: Beautiful, responsive design using Tailwind CSS and Montserrat fonts.
- **Live Pre-Registered Sellers Count**: Real-time count of sellers, updated from the backend for transparency.
- **Email Notification Signup**: Users can sign up to be notified at launch, with email verification and anti-spam measures.
- **Secure Email Delivery**: Uses Zoho SMTP for reliable email notifications.
- **Progress & News Timeline**: Honest, transparent updates about platform milestones.
- **Mobile-First Design**: Fully responsive and optimized for all devices.
- **PWA Support**: Installable as a Progressive Web App.
- **Environment Variables**: Sensitive data managed securely via `.env` and `python-dotenv`.

## Tech Stack

- **Backend**: Django 5.x
- **Frontend**: Tailwind CSS, HTML, JavaScript
- **Database**: SQLite (default, can be changed)
- **Email**: Zoho SMTP
- **Other**: python-dotenv, Feather Icons, Font Awesome

## Project Structure

```
.
├── coming-soon/
│   ├── main.html           # Main landing page
│   ├── coming_soon.html    # Email template (inline styles for email safety)
│   ├── script.js           # Frontend logic (AJAX, modals, etc.)
│   ├── style.css           # Custom styles (if needed)
│   └── ...
├── covu_soon/
│   ├── settings.py         # Django settings (uses .env for secrets)
│   ├── urls.py             # Project URLs
│   └── ...
├── signup/
│   ├── models.py           # EmailSubscription model
│   ├── views.py            # Handles signup, verification, and passes live count
│   ├── urls.py             # App URLs
│   └── ...
├── db.sqlite3              # SQLite database (default)
├── .env                    # Environment variables (not tracked by git)
├── requirements.txt        # Python dependencies
├── manage.py               # Django management script
└── README.md               # Project documentation
```

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/synergynigeria/coming-soon.git
cd covumarket.com
```

### 2. Create and Activate a Virtual Environment

```sh
python3.11 -m venv .venv
.venv\Scripts\activate  # On Windows
# Or
source .venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root (see `.env.example`):

```
SECRET_KEY=your-very-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST=smtp.zoho.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
```

### 5. Run Migrations

```sh
python manage.py migrate
```

### 6. Start the Development Server

```sh
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Deployment Notes

- Set `DEBUG=False` and update `ALLOWED_HOSTS` in production.
- Use a secure, unique `SECRET_KEY`.
- Configure your production email backend and database as needed.
- Never commit your `.env` file or secrets to version control.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

## Contact

- Email: teams@covumarket.com
- Twitter: [@covumarket](https://twitter.com/covumarket)

---

Built with ❤️ for Nigerian entrepreneurs.
