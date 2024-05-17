from glob import iglob
from libs.config import AppConfig
from libs.core import get_statistics, merge_csv_filenames
from libs.models import OnSSetFilename
from s3fs import S3FileSystem
import click
import logging
import os
import pandas as pd
import re

logger = logging.getLogger(__name__)

app_config: AppConfig = AppConfig()


@click.group()
def cli():
    pass


def download_csv():
    s3: S3FileSystem = S3FileSystem()
    for idx, filename in enumerate(s3.ls(path=app_config.bucket_csv_folder(with_protocol=False))):
        logger.debug(f'{idx}) {filename}')
        h: bytes = s3.head(path=filename, size=2048)
        lines = h.decode(encoding='utf-8').split('\r\n')
        for line in lines:
            logger.debug(line.split(','))
            break
        break


@cli.command('parse-csv-files')
def parse_csv_files() -> int:
    res: int = 0
    _pattern: str = os.path.join(app_config.local_working_folder, '*.csv')
    logger.debug(f'regex pattern: {_pattern}')

    output_folder: str = os.path.join(os.path.dirname(app_config.local_working_folder), 'output')
    os.makedirs(output_folder, exist_ok=True)

    _delimiter: str = app_config.csv_delimiter

    for filename in sorted(iglob(pathname=_pattern)):
        logger.info(f'parsing filename: {os.path.basename(filename)}...')

        try:
            info: OnSSetFilename = OnSSetFilename.parse(filename=os.path.basename(filename))

            df: pd.DataFrame = pd.read_csv(filename)
            df_sum: pd.DataFrame = get_statistics(df=df, years=app_config.current_years, scenario=info.scenario)

            csv_filename, _ext = os.path.splitext(os.path.basename(filename))
            csv_filename = os.path.join(output_folder, csv_filename + '_sum' + _ext)

            df_sum.to_csv(csv_filename, sep=_delimiter, index=False)
            logger.info(f'file {csv_filename} generated successfully')

            res += 0

        except Exception as ex:
            logger.error(ex)
            res = 1

    if res == 0:
        res += merge_csv_filenames(input_folder=output_folder,
                                   delimiter=_delimiter,
                                   delete_csv=app_config.delete_temporary_file)

    return res



if __name__ == '__main__':
    logging.basicConfig(level=app_config.log_level)
    for m in ('aiobotocore', 'asyncio', 'botocore', 'fsspec', 's3fs'):
        logging.getLogger(m).setLevel(level=logging.WARNING)
    cli()
