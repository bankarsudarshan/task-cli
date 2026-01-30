from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str
    file_store_location: Path = Path("~/taskman").expanduser()
    tasks_filename: str = "tasks.json"
    archives_filename: str = "archived.json"

    @property
    def database_path(self) -> Path:
        path = self.file_store_location
        if self.environment == "dev":
            return path.with_name(f"{path.name}-test")
        return path


settings = Settings(environment="prod")
