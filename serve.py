import os
from jbrowse_jupyter import serve


if __name__ == "__main__":
    # Enter a PORT number
    PORT = input("ENTER A PORT: ")
    if not PORT:
        PORT = 8080
    else:
        PORT = int(PORT)
    # Enter a host
    HOST = input("ENTER A HOST: ")
    if not HOST:
        HOST = "localhost"
    # Enter the path to your local data
    DIRECTORY = input("ENTER PATH TO YOUR LOCAL DATA: ")
    if not DIRECTORY:
        DIRECTORY = os.getcwd()
    serve(DIRECTORY, port=PORT, host=HOST)
    print("\n You are now running a development server. \n"
          "This is not inteded for production")
