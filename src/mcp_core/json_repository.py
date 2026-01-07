import fcntl
import json
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel

from .repository import Repository

T = TypeVar("T", bound=BaseModel)

class JsonFileRepository(Repository[T]):
    """
    A file-based repository implementation using JSON.
    Supports basic CRUD operations and optimistic locking.
    """

    def __init__(self, model_class: type[T], file_path: str):
        self.model_class = model_class
        self.file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def _read_data(self) -> dict[str, Any]:
        with open(self.file_path) as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            try:
                content = f.read()
                return json.loads(content) if content else {}
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    def _write_data(self, data: dict[str, Any]):
        with open(self.file_path, 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                json.dump(data, f, indent=2, default=str)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    def get(self, id: str) -> T | None:
        data = self._read_data()
        item_data = data.get(id)
        if item_data:
            # We trust that item_data matches the model structure
            return self.model_class.model_validate(item_data)  # type: ignore
        return None

    def list(self) -> list[T]:
        data = self._read_data()
        # We trust that item matches the model structure
        return [self.model_class.model_validate(item) for item in data.values()]  # type: ignore

    def save(self, entity: T) -> T:
        # Use a read-modify-write cycle with file locking to ensure atomicity
        # For simplicity in this file-based approach, we lock the file during the whole operation
        # This implementation is slightly different from _read_data/_write_data split to avoid race conditions

        with open(self.file_path, 'r+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                content = f.read()
                data = json.loads(content) if content else {}

                # Check for optimistic locking if updating existing entity
                if hasattr(entity, 'id') and hasattr(entity, 'version'):
                    entity_id = entity.id
                    current_version = entity.version

                    if entity_id in data:
                        existing_data = data[entity_id]
                        stored_version = existing_data.get('version', 0)
                        if stored_version > current_version:
                            raise ValueError(f"Optimistic locking failure: Stored version {stored_version} is newer than {current_version}")

                        # Increment version for update
                        entity.version = current_version + 1
                    else:
                        # New entity, ensure version starts at 1
                         entity.version = 1

                # Update data
                entity_dict = entity.model_dump(mode='json')
                data[str(entity.id)] = entity_dict

                # Write back
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=2, default=str)

                return entity
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    def delete(self, id: str) -> bool:
        with open(self.file_path, 'r+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                content = f.read()
                data = json.loads(content) if content else {}

                if id in data:
                    del data[id]
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=2)
                    return True
                return False
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
