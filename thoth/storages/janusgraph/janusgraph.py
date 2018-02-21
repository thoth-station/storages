"""A Gremlin server adapter communicating via a web socket."""

from selinon import DataStorage


class JanusGraphDatabase(DataStorage):
    """A Gremlin server adapter communicating via a web socket."""

    def __init__(self, host, port):
        """Initialize Gremlin server database adapter."""
        super().__init__()
        self.host = host
        self.port = port

    def is_connected(self):
        """Check if we are connected to a remote Gremlin server."""
        return True

    def connect(self):
        """Connect to a graph database via a websocket, use GraphSONSerializersV2d0."""
        # TODO: implement

    def store_pypi_package(self, package_name: str, package_version: str, dependencies: list) -> None:
        """Store the given PyPI package into the graph database and construct dependency graph based on dependencies."""
        # TODO: implement

    def store_pypi_solver_result(self, solver_result):
        """Store results of Thoth's PyPI dependency solver."""
        # TODO: implement

