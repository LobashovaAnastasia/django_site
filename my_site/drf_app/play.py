import io
from drf_app.models import Book, Publisher, Author
from drf_app.serializers import BookSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
