__all__ = ["main"]
__version__ = "1.0.1"


def main():
    # Lazy import to avoid pulling MCP runtime in unit tests.
    from .server import main as _main
    return _main()
