import uuid, os
import sys
from io import BytesIO
from PIL import Image
import xml.etree.cElementTree as et

from django.core.exceptions import ValidationError
from django.db.models import ImageField as DjangoImageField
from django.utils import six


def get_image_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	return os.path.join(instance._meta.db_table, filename)
