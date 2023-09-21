# My Django Project Documentation
``Intlum Project by Arth Patel``

## Project Overview
This Django project is designed to create a data drive system similar to Google Drive. It allows users to perform CRUD operations on folders and files.

## Installation
Follow these steps to set up and run the project locally:

1. Clone the project repository:
``git clone https://github.com/yourusername/your-project.git`` or unzip from zip file.
2. Create a virtual environment and activate it: 
``python -m venv venv`` 
``source venv/bin/activate # On Windows, use: venv\Scripts\activate``
3. Install project dependencies:
``pip install -r requirements.txt``

4. Make Migrations:``python manage.py makemigrations``
5. Apply database migrations:``python manage.py migrate``

6. Run the development server: ``python manage.py runserver``




## Usage
### User Registration and Login
- Users can create accounts and log in to the system.
- No "forgot password" feature is available in this version.

### Folder Management
- Users can create folders of any depth (nesting).
- CRUD operations are available for folders:
- Create: Users can create new folders.
- Read: Users can view folder contents.
- Update: Users can rename folders.
- Delete: Users can delete empty folders.

### File Management
- Users can upload files to folders.
- CRUD operations are available for files:
- Create: Users can upload files.
- Read: Users can download files.
- Delete: Users can delete files.

### Frontend Side
- Frontend side is done by me.
- Used JavaScript, Jquery, Bootstrap, FontAwesome, SweetAlert and more plugins.

## Project Structure
The project is structured as follows:
- `intlum_drive_manager/` (main project directory)
- `intlum_drive/` (Django app directory)
- `venv/` (virtual environment)
- `requirements.txt` (list of dependencies)
- `manage.py` (Django management script)

## Additional Notes
- This is a basic version of the project.
- Users can organize folders and files as needed.
- Please refer to the project's GitHub repository for the complete source code.

## Contact Information
If you have any questions or need assistance, please contact us at [arthpatel.ce@gmail.com](mailto:arthpatel.ce@gmail.com), [+916355260850](tel:+916355260850).

---


