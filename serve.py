import os
from jbrowse_jupyter import serve


if __name__ == "__main__":
    # Enter a PORT number
    PORT = input("Enter a PORT: [default:8080] > ")
    if not PORT:
        PORT = 8080
    else:
        PORT = int(PORT)
    print(PORT)
    # Enter a host
    HOST = input("ENTER A HOST:  [default:localhost] > ")
    if not HOST:
        HOST = "localhost"
    print(HOST)
    # Enter the path to your local data
    DIRECTORY = input("ENTER PATH TO YOUR LOCAL DATA: [default:(pwd)] > ")
    if not DIRECTORY:
        DIRECTORY = os.getcwd()
    print(DIRECTORY)
    print("\n")
    serve(DIRECTORY, port=PORT, host=HOST)
