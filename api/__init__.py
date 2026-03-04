from .app import app


def create_app():
    """Flask application factory compatibility wrapper."""
    return app


__all__ = ["app", "create_app"]
