# Online Shop

This is an online shop project built with Django. It supports various features such as multi-upload, filtering, and REST
API functionalities.

## Dependencies

This project uses the following dependencies:

- django-multiupload
- Django
- pillow
- django-filter
- django-crispy-forms
- crispy-tailwind
- asgiref
- celery
- redis
- django-celery-beat
- python-decouple
- django-jazzmin
- djangorestframework
- django-taggit
- poetry
- pre-commit

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/online-shop.git
    cd online-shop
    ```

2. Install the dependencies using Poetry:
    ```sh
    poetry install
    ```

3. Set up environment variables:
   Create a `.env` file in the root directory of the project and add your environment variables there. Refer
   to `.env.example` for the required variables.

4. Apply migrations:
    ```sh
    poetry run python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    poetry run python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    poetry run python manage.py runserver
    ```

## Usage

- Access the admin interface at `http://127.0.0.1:8000/admin/`.
- The REST API endpoints are available under the `/api/` URL path.
- Upload and manage products using the multi-upload feature.
- Use filtering options to search and sort products.

## Running Celery

Start the Celery worker and beat scheduler with the following commands:

```sh
poetry run celery -A your_project_name worker --loglevel=info
poetry run celery -A your_project_name beat --loglevel=info