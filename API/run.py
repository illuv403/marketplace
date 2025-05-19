from API.app import create_app

if __name__ == '__main__':
    """
    Entry point for running the Flask application in development mode.
    """

    # Create the Flask app instance using the factory method
    app = create_app()

    # Run the app in debug mode for development
    app.run()
