from API.app import create_app
from API.services.main_page_service import PageService

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)