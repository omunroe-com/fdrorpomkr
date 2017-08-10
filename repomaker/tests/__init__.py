import datetime
import os
from shutil import copyfile

from django.conf import settings
from fdroidserver import update

TEST_FILES_DIR = os.path.join(settings.BASE_DIR, 'tests')

TEST_DIR = os.path.join(settings.BASE_DIR, 'test_dir')
TEST_MEDIA_DIR = os.path.join(TEST_DIR, 'media')
TEST_PRIVATE_DIR = os.path.join(TEST_DIR, 'private_repo')
TEST_STATIC_DIR = os.path.join(TEST_DIR, 'static')


def datetime_is_recent(dt, seconds=10 * 60):
    now = datetime.datetime.utcnow().timestamp()
    return now - seconds < dt.timestamp() < now


def fake_repo_create(repo):
    if settings.PRIVATE_REPO_ROOT != TEST_PRIVATE_DIR:
        raise RuntimeError('Do not write into non-test directories')

    # copy existing keystore
    src = os.path.join(TEST_FILES_DIR, 'keystore.jks')
    dest = os.path.join(repo.get_private_path(), 'keystore.jks')
    if not os.path.isdir(repo.get_private_path()):
        os.makedirs(repo.get_private_path())
    copyfile(src, dest)
    repo.key_store_pass = 'uGrqvkPLiGptUScrAHsVAyNSQqyJq4OQJSiN1YZWxes='
    repo.key_pass = 'uGrqvkPLiGptUScrAHsVAyNSQqyJq4OQJSiN1YZWxes='

    # make sure that icon directories exist
    for icon_dir in update.get_all_icon_dirs(repo.get_repo_path()):
        if not os.path.exists(icon_dir):
            os.makedirs(icon_dir)