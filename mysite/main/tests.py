from main.utils import insertDirectoryPath

# Create your tests here.


DIRS_TEMP = insertDirectoryPath(["../main", "../users"], Path(__file__).resolve().parent.parent, "templates")

print(DIRS_TEMP)