# Library Management System

This is a web-based Library Management System developed using Flask for the backend, Jinja2 templates with Bootstrap for the frontend, and SQLite for data storage. The system allows both a librarian and general users (students) to manage and access e-books, with functionalities for issuing, returning, and managing sections and books.

## Features

### Core Functionality
- **Multi-User Support**: 
  - **Librarian**: Admin role responsible for managing e-books, sections, and user access.
  - **General Users**: Students can request, read, and return e-books.
  
- **Section Management**:
  - Create, view, edit, and delete sections.
  - Assign books to specific sections.
  
- **Book Management**:
  - Add, view, edit, and delete e-books.
  - Manage book content, author details, and assign to sections.
  
- **Book Issuing & Returning**:
  - Users can request a maximum of 5 e-books at a time.
  - Books are issued for a specific period, after which access is automatically revoked.
  - Users can return books before the due date.
  
- **Search Functionality**:
  - Search for sections or e-books based on various criteria like section, author, etc.

### User Interface
- **Librarian's Dashboard**: 
  - Overview of all sections and books.
  - Monitor book status and user access.
  
- **User Profile**:
  - View available sections and e-books.
  - Request and return e-books.
  
- **Responsive Design**:
  - Built with Bootstrap to ensure compatibility across devices.
  
### Technology Stack
- **Backend**: Flask (Python)
- **Frontend**: Jinja2 templates, HTML, CSS, Bootstrap
- **Database**: SQLite

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/library-management-system.git
    ```
   
2. **Navigate to the Project Directory**:
    ```bash
    cd library-management-system
    ```

3. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    ```

4. **Activate the Virtual Environment**:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

5. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

6. **Run the Application**:
    ```bash
    flask run
    ```

7. **Access the Application**:
    - Open your web browser and navigate to `http://127.0.0.1:5000`.


### Presentation Video

For a detailed walkthrough of the project, you can view the presentation video [here](https://drive.google.com/file/d/1EEa24ay6VOimy4v8iw61IE2VeE362Rc9/view?usp=sharing).

