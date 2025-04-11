# E-Commerce Website

## Project Overview

This project is a fully functional e-commerce website built using Flask (Python) for the backend, along with HTML, CSS, and JavaScript for the frontend. The website allows users to browse products, add items to their cart, and proceed to checkout. The backend is connected to a product database to store and manage product information.

## Features

- User authentication (sign-up, login, logout)
- Product browsing and categorization
- Shopping cart functionality
- Checkout system
- Product search functionality
- Database integration for managing products and orders
- Responsive design for mobile and desktop users

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQL (e.g., SQLite, PostgreSQL, or MySQL)
- **Frameworks/Libraries**: Flask, Jinja2 (for templating), SQLAlchemy (for database ORM)

## Installation

### Prerequisites

Make sure you have Python installed on your system.

### Steps to Set Up the Project

1. Clone this repository:
   ```
   git clone https://github.com/Tervina/ecommerce-flask.git
   cd ecommerce-flask
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv myvenv
   source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate
   ```

3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   flask run
   ```

The website should now be accessible at http://127.0.0.1:5000/

## Project Structure

```
/ecommerce-flask
│── /static          # CSS, JavaScript, images
│   ├── images       # Product and UI images
│   ├── login.css    # Login page styles
│   ├── product.css  # Product page styles
│   ├── register.css # Register page styles
│   ├── styles.css   # General styles
│── /templates       # HTML templates
│   ├── add_to_cart.html  # Add to cart page
│   ├── base.html         # Base template
│   ├── cart.html         # Shopping cart
│   ├── computer.html     # Computer category
│   ├── electronics.html  # Electronics page
│   ├── forget-pass.html  # Password reset page
│   ├── home.html         # Homepage
│   ├── index.html        # Index page
│   ├── kitchen.html      # Kitchen category
│   ├── login.html        # Login page
│   ├── product.html      # Product details
│   ├── register.html     # Registration page
│── myvenv               # Virtual environment
│── requirements.txt     # Project dependencies
│── README.md            # Project documentation
```
#### Video Demo: https://www.youtube.com/watch?v=aLbALXb45qQ
## Future Improvements

- Implement an order history feature
- Add payment gateway integration
- Enhance UI/UX design
- Optimize performance and security

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

## License

This project is open-source and available under the MIT License.

---

Made with ❤️ by Tervina
