from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel, Field


class Resource(BaseModel):
    """
    Represents an MCP Resource.
    Resources are read-only data exposed via a URI.
    """

    uri: str = Field(..., description="Unique URI for the resource")
    name: str = Field(..., description="Human-readable name")
    description: Optional[str] = Field(None, description="Description of the resource")
    mime_type: Optional[str] = Field(None, description="MIME type of the content")
    text: Optional[str] = Field(None, description="Text content of the resource")
    blob: Optional[str] = Field(None, description="Base64 encoded blob content")


class ResourceProvider(ABC):
    """
    Abstract base class for resource providers.
    A provider is responsible for handling a specific set of resources,
    usually identified by URI scheme or pattern.
    """

    @abstractmethod
    def get_resource(self, uri: str) -> Optional[Resource]:
        """
        Retrieve a resource by its URI.
        Returns None if the URI is not handled by this provider or not found.
        """
        pass

    @abstractmethod
    def list_resources(self) -> List[Resource]:
        """
        List all resources available from this provider.
        Note: For dynamic resources (like those based on DB IDs),
        this might return a representative list or templates.
        """
        pass
