from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


class Resource(BaseModel):
    """
    Represents an MCP Resource.
    Resources are read-only data exposed via a URI.
    """

    uri: str = Field(..., description="Unique URI for the resource")
    name: str = Field(..., description="Human-readable name")
    description: str | None = Field(None, description="Description of the resource")
    mime_type: str | None = Field(None, description="MIME type of the content")
    text: str | None = Field(None, description="Text content of the resource")
    blob: str | None = Field(None, description="Base64 encoded blob content")


class ResourceProvider(ABC):
    """
    Abstract base class for resource providers.
    A provider is responsible for handling a specific set of resources,
    usually identified by URI scheme or pattern.
    """

    @abstractmethod
    def get_resource(self, uri: str) -> Resource | None:
        """
        Retrieve a resource by its URI.
        Returns None if the URI is not handled by this provider or not found.
        """
        pass

    @abstractmethod
    def list_resources(self) -> list[Resource]:
        """
        List all resources available from this provider.
        Note: For dynamic resources (like those based on DB IDs),
        this might return a representative list or templates.
        """
        pass
