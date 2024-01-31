import base64

from rest_framework.decorators import api_view, authentication_classes

from commdem_warriors_backend.authenticators import ApiKeyAuthentication


# Create your views here.
@api_view(["POST"])
@authentication_classes(
    [
        ApiKeyAuthentication,
    ]
)
def add_group_chat_file(request):
    """Function to add group chat file data"""
    data = request.data
    imgdata = base64.b64decode(str(data["key"]))
    filename = data["fileName"]  # I assume you have a way of picking unique filenames
    with open("static/" + filename, "wb") as f:
        f.write(imgdata)
