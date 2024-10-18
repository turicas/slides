import csv

import rows
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from tqdm import tqdm


def convert_row(row):
    return {key: value or None for key, value in row.items()}


class Command(BaseCommand):
    help = "Import data to model"

    def add_arguments(self, parser):
        parser.add_argument("--batch-size", type=int, default=1000)
        parser.add_argument("method", choices=["single", "bulk", "copy"])
        parser.add_argument("model_name")
        parser.add_argument("csv_filename", help="Could be compressed (.gz, .bz2 or .xz)")

    def handle(self, *args, **kwargs):
        batch_size = int(kwargs["batch_size"])
        method = kwargs["method"]
        model_name = kwargs["model_name"]
        csv_filename = kwargs["csv_filename"]
        Model = apps.get_model("dataset", model_name)

        with connection.cursor() as cursor:
            cursor.execute(f"""TRUNCATE TABLE "{Model._meta.db_table}" RESTART IDENTITY""")

        if method == "single":
            with rows.utils.open_compressed(csv_filename) as fobj:
                reader = csv.DictReader(fobj)
                for row in tqdm(reader):
                    Model.objects.create(**convert_row(row))

        elif method == "bulk":
            with rows.utils.open_compressed(csv_filename) as fobj:
                reader = tqdm(csv.DictReader(fobj))
                for batch in rows.plugins.utils.ipartition(reader, batch_size):
                    Model.objects.bulk_create([Model(**convert_row(row)) for row in batch])

        elif method == "copy":
            progress_bar = rows.utils.ProgressBar(
                prefix="Importing data", pre_prefix="Detecting file size", unit="bytes"
            )
            import_meta = rows.plugins.postgresql.pgimport(
                csv_filename,
                settings.DATABASE_URL,
                Model._meta.db_table,
                encoding="utf-8",
                dialect="excel",
                schema=None,
                has_header=True,
                skip_rows=0,
                create_table=False,
                callback=progress_bar.update,
            )
            progress_bar.description = "{} rows imported".format(import_meta["rows_imported"])
            progress_bar.close()
