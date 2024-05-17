from pydantic_settings import BaseSettings
from pydantic import DirectoryPath


class AppConfig(BaseSettings):
    bucket_name: str = 'it.neratech.feem'
    csv_delimiter: str = ';'
    current_years: list[int] = [2025, 2030]
    delete_temporary_file: bool = False
    local_working_folder: DirectoryPath
    log_level: str = 'WARNING'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    def bucket_csv_folder(self, with_protocol: bool = True) -> str:
        s: str = f'{self.bucket_name}/OnSSET/v2'
        return 's3://' + s if with_protocol else s

    def bucket_twitter_folder(self, with_protocol: bool = True) -> str:
        s: str = f'{self.bucket_name}/OnSSET/twitter'
        return 's3://' + s if with_protocol else s
