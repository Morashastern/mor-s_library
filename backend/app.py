from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy,session
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

from datetime import datetime,timedelta

app = Flask(__name__)
CORS(app)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Define the path to the 'media' directory
app.config['UPLOAD_FOLDER'] = 'media'


# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Define models
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bookName = db.Column(db.String(100), nullable=False)
    Author = db.Column(db.String(100), nullable=False)
    YearPublished = db.Column(db.Integer, nullable=False)
    BookType = db.Column(db.String(50), nullable=False)
    BookStatus = db.Column(db.Boolean, nullable=True)
    filePath = db.Column(db.String(255), nullable=True)  


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customerName = db.Column(db.String(100), nullable=False)
    City = db.Column(db.String(100), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    customerstatus = db.Column(db.Integer, nullable=False)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustID = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    BookID = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    LoanDate = db.Column(db.Date, nullable=False, default=datetime.now)
    ReturnDate = db.Column(db.Date, nullable=True)
    LoanStatus = db.Column(db.String(50), nullable=False, default='Active')

# Create the database tables


@app.route('/')
def hello():
    
    return 'Hello, World!'

@app.route("/new_book", methods=["POST"])
def add_book():
    try:
        data = request.form  # Use form data instead of JSON
        file = request.files.get('file')

        if not file or file.filename == '':
            return jsonify({"error": "No file selected for uploading"}), 400

        # Save the file to the 'media' directory
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(file_path)
        file.save(file_path)

        new_book = Book(
            bookName=data.get("bookName"),
            Author=data.get("author"),
            YearPublished=data.get("yearPublished"),
            BookType=data.get("bookType"),
            BookStatus=bool(int(data.get("bookStatus"))),
            filePath=file_path  # Save the file path in the database
        )
        print(new_book)
                       
        db.session.add(new_book)
        db.session.commit()

        return jsonify({"message": f"New book added: {data}"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/media/<filename>')
def media(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/get_books')
def get_books():
    books = Book.query.all()
    books_list = [
        {"id": book.id, "bookName": book.bookName, "Author": book.Author, "YearPublished": book.YearPublished, "BookType": book.BookType, "BookStatus": book.BookStatus,"filePath": book.filePath}
        for book in books
    ]
    return jsonify(books_list)


@app.route('/del_book/<int:book_id>', methods=["delete"])
def del_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        print(book)
        return jsonify({"error": "Book not found"}), 404
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}), 200

@app.route('/upt_books/<int:book_id>', methods=["PUT"])
def update_book(book_id):
    try:
        data = request.form  
        file = request.files.get('file')
        print (data)

        if not file or file.filename == '':
            return jsonify({"error": "No file selected for uploading"}), 400

        # Save the file to the 'media' directory
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(file_path)
        file.save(file_path)
        book = Book.query.get(book_id)
        if not book:
            return jsonify({"error": "Book not found"}), 404

        book.bookName = data.get("bookName", book.bookName)
        book.Author = data.get("author", book.Author)
        book.YearPublished = data.get("yearPublished", book.YearPublished)
        book.BookType = data.get("bookType", book.BookType)
        book_status = data.get("bookStatus")

        if book_status is not None:
            book.BookStatus = bool(int(book_status))

        
        book.filePath=file_path 
        print(book.bookName,book.Author,book.YearPublished,book.BookType,book.BookStatus)
        db.session.commit()
        return jsonify({"message": f"Book with ID {book_id} updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/search_books/<string:name>', methods=['GET'])
def search_books(name):
    books = Book.query.filter(Book.bookName.like(f"%{name}%")).all()
    books_list = [{"id": book.id, "bookName": book.bookName} for book in books]
    return jsonify(books_list)

   
@app.route("/new_customer", methods=["POST"])
def add_customer():
    try:
        data = request.get_json()
        new_customer = Customer(
            customerName=data.get("customerName"),
            City=data.get("City"),
            Age=data.get("Age"),
            customerstatus=data.get("customerstatus")
        )
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({"message": f"New customer added: {data}"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_customers')
def get_customers():
    customers = Customer.query.all()
    customers_list = [
        {"id": customer.id, "customerName": customer.customerName, "City": customer.City, "Age": customer.Age, "customerstatus": customer.customerstatus}
        for customer in customers
    ]
    return jsonify(customers_list)

@app.route('/del_customer/<int:customer_id>', methods=["PUT"])
def del_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    customer.customerstatus =0
    db.session.commit()
    return jsonify({"message": "Customer IS INACTTIVE"}), 200


@app.route('/upt_customer/<int:customer_id>', methods=["PUT"])
def update_customer(customer_id):
    try:
        data = request.get_json()
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        customer.customerName = data.get("customerName", customer.customerName)
        customer.City = data.get("City", customer.City)
        customer.Age = data.get("Age", customer.Age)
        customer.customerstatus = data.get("customerstatus", customer.customerstatus)

        db.session.commit()
        return jsonify({"message": f"Customer with ID {customer_id} updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@app.route('/search_customers/<string:name>', methods=['GET'])
def search_customers(name):
    customers = Customer.query.filter(Customer.customerName.like(f"%{name}%")).all()
    customers_list = [{"id": customer.id, "customerName": customer.customerName} for customer in customers]
    return jsonify(customers_list)
@app.route("/new_loan", methods=["POST"])
def add_loan():
    try:
        data = request.get_json()
        
        # Fetch the book to determine the return date based on its type
        book = Book.query.get(data.get("BookID"))
        if not book:
            return jsonify({"error": "Book not found"}), 404
        
        if book.BookStatus == False:
            return jsonify({"error": "Book isn't available"}), 400

        if book.BookType == "1":
            return_date = datetime.now() + timedelta(days=10)
        elif book.BookType == "2":
            return_date = datetime.now() + timedelta(days=15)
        elif book.BookType == "3":
            return_date = datetime.now() + timedelta(days=20)
        else:
            return jsonify({"error": "Invalid BookType"}), 400
        
        new_loan = Loan(
            CustID=data.get("CustID"),
            BookID=data.get("BookID"),
            LoanDate=datetime.utcnow(),
            ReturnDate=return_date
        )
        db.session.add(new_loan)
           # Change the book status to False
        book.BookStatus = False
        db.session.commit()


        return jsonify({"message": f"New loan added: {data}"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_loans')
def get_loans():
    loans = Loan.query.all()
    loans_list = [
        {"id": loan.id, "CustID": loan.CustID, "BookID": loan.BookID, "LoanDate": loan.LoanDate, "ReturnDate": loan.ReturnDate}
        for loan in loans
    ]
    return jsonify(loans_list)

@app.route('/del_loan/<int:loan_id>', methods=["DELETE"])
def del_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404
    
    db.session.delete(loan)
    db.session.commit()
    return jsonify({"message": "Loan deleted"}), 200

@app.route('/upt_loan/<int:loan_id>', methods=["PUT"])
def update_loan(loan_id):
    try:
        data = request.get_json()
        loan = Loan.query.get(loan_id)
        if not loan:
            return jsonify({"error": "Loan not found"}), 404

        loan.CustID = data.get("CustID", loan.CustID)
        loan.BookID = data.get("BookID", loan.BookID)
        loan.LoanDate = data.get("LoanDate", loan.LoanDate)
        loan.ReturnDate = data.get("ReturnDate", loan.ReturnDate)
        loan.LoanStatus = data.get("LoanStatus",loan.LoanStatus)

        db.session.commit()
        return jsonify({"message": f"Loan with ID {loan_id} updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/get_loans_details')
def get_loans_details():
    loans = Loan.query.join(Customer, Loan.CustID == Customer.id).join(Book, Loan.BookID == Book.id).add_columns(
        Loan.id, Customer.customerName, Book.bookName, Loan.LoanDate, Loan.ReturnDate, Loan.LoanStatus).all()
    
    loans_details = [
        {"id": loan.id, "customerName": loan.customerName, "bookName": loan.bookName, "LoanDate": loan.LoanDate, "ReturnDate": loan.ReturnDate,"LoanStatus":loan.LoanStatus}
        for loan in loans
    ]
    return jsonify(loans_details)

@app.route('/return_loan/<int:loan_id>', methods=["PUT"])
def return_loan(loan_id):
    try:
        loan = Loan.query.get(loan_id)
        if not loan:
            return jsonify({"error": "Loan not found"}), 404
        
        if loan.LoanStatus != 'Active':
            return jsonify({"error": "Loan is already returned"}), 400
        
        # Fetch the book to update its status
        book = Book.query.get(loan.BookID)
        if not book:
            return jsonify({"error": "Book not found"}), 404

        # Update loan status and book status
        loan.LoanStatus = 'Returned'
        book.BookStatus = 1
        
        db.session.commit()
        return jsonify({"message": "Loan returned successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@app.route('/late_loans_details')
def get_late_loans_details():

    try:
        loans = db.session.query(Loan, Customer.customerName, Book.bookName).join(Customer, Loan.CustID == Customer.id).join(Book, Loan.BookID == Book.id).filter(Loan.ReturnDate < datetime.utcnow()).all()
        
        late_loans_details = [
            {
                "id": loan.Loan.id,
                "customerName": loan.customerName,
                "bookName": loan.bookName,
                "LoanDate": loan.Loan.LoanDate,
                "ReturnDate": loan.Loan.ReturnDate,
                "LoanStatus": loan.Loan.LoanStatus
            }
            for loan in loans
        ]
        return jsonify(late_loans_details), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    with app.app_context():
       db.create_all()
    app.run(debug=True )