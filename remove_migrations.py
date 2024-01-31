# import os
import os
import shutil

# Get the list of all files and directories
path = "/Users/apple/django-backend-projects/commdem_warriors_django"
dir_list = os.listdir(path)

print("Files and directories in '", path, "' :")

for i in range(0, len(dir_list)):
    print(dir_list[i])
    if os.path.exists(
        f"/Users/apple/django-backend-projects/commdem_warriors_django/{dir_list[i]}/migrations/"
    ):
        shutil.rmtree(
            f"/Users/apple/django-backend-projects/commdem_warriors_django/{dir_list[i]}/migrations/"
        )
