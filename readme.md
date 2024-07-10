# Library Management System

Welcome to the Library Management System! This application allows you to manage books, customers, and loans in a library. The system includes functionalities for adding, updating, deleting, and viewing books, customers, and loans.

## Features

- Add, update, delete, and view books
- Add, update, delete, and view customers
- Add, update, delete, and view loans
- Search books and customers
- Track late loans
- File upload for book images
- Responsive web interface

## Installation

1. Clone the repository:
    ```sh
    https://github.com/Morashastern/mors_library.git
    ```

2. Create a virtual environment:
    
    python3 -m venv env
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:

    pip install -r requirements.txt
    

4. Run the application:
    py app.py

## Usage

- Navigate to `http://127.0.0.1:5000` in your web browser to access the application.
- Use the navigation links to manage books, customers, and loans.

## Database Schema

The application uses a SQLAlchemy-based SQLite database. The schema includes the following tables:

- **Book**: Stores book information (ID, Name, Author, Year Published, Type, Status, File Path).
- **Customer**: Stores customer information (ID, Name, City, Age,Status).
- **Loan**: Stores loan information (ID, Customer ID, Book ID, Loan Date, Return Date, Status).

## File Structure

library-management-system/
├── app.py                   # Main application file
                               Database module with SQLAlchemy models
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── frontend/templates/               # HTML templates
│   ├── header.html          # header templat footer
│   ├── footer.html          # footer templat 
│   ├── index.html           # Home page template
│   ├── books.html           # Manage books page template
│   ├── customers.html       # Manage customers page template
│   ├── loans.html           # Manage loans page template
│   ├── frontend/templates/load-components.js           # activate header and footer templates 
│   
            
│   ├── css/
│     ├── styles.css       # Custom styles
│  
├
└── .env                     # Environment variables (for Flask configuration)
