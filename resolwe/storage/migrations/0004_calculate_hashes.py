# Generated by Django 2.2.10 on 2020-05-12 08:44
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from django.db import migrations


from resolwe.storage.connectors import connectors


def process_storage_location(file_storage, best_storage_location):
    connector = connectors[best_storage_location.connector_name].duplicate()
    base_url = Path(best_storage_location.url)
    for referenced_path in file_storage.files.exclude(path__endswith="/"):
        url = base_url / referenced_path.path
        hashes = connector.get_hashes(url, ["md5", "crc32c", "awss3etag"])
        referenced_path.md5 = hashes["md5"]
        referenced_path.crc32c = hashes["crc32c"]
        referenced_path.awss3etag = hashes["awss3etag"]
        referenced_path.save()


def calculate_hashes(apps, schema_editor):
    """Calculate hashes for existing ReferencedPaths."""
    FileStorage = apps.get_model("storage", "FileStorage")

    with ThreadPoolExecutor(max_workers=50) as executor:
        for file_storage in FileStorage.objects.all():
            storage_locations = file_storage.storage_locations.filter(status="OK")
            # Do not calculate hash when no location with status OK exists.
            if storage_locations.count() == 0:
                continue
            best_storage_location = storage_locations.first()
            best_priority = connectors[best_storage_location.connector_name].priority
            for storage_location in storage_locations:
                priority = connectors[storage_location.connector_name].priority
                if priority < best_priority:
                    best_storage_location = storage_location
                    best_priority = priority
            storage_location = best_storage_location
            executor.submit(
                process_storage_location, file_storage, best_storage_location
            )


class Migration(migrations.Migration):
    dependencies = [
        ("storage", "0003_add_hash_fields_to_referenced_path"),
    ]

    operations = [
        migrations.RunPython(calculate_hashes),
    ]
