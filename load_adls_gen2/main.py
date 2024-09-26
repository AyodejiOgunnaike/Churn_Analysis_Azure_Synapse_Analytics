import os


from azure.storage.filedatalake import (
    DataLakeServiceClient,
    DataLakeDirectoryClient,
    FileSystemClient,
    DataLakeFileClient
)


from azure.identity import DefaultAzureCredential

local_path = os.getcwd()

sas_token : str = "sp=racwdlmeop&st=2024-09-24T07:30:55Z&se=2024-09-24T15:30:55Z&spr=https&sv=2022-11-02&sr=c&sig=AjPvfi2Z%2FIhsG7gR3toFB5IqucHqwvHNo1VoHevyp3U%3D"

# Define a function that gets the data lake service client
def get_service_client_sas(account_name: str, sas_token: str) -> DataLakeServiceClient:
    account_url = f"https://{account_name}.dfs.core.windows.net"

    # The SAS token string can be passed in as credential param or appended to the account URL
    service_client = DataLakeServiceClient(account_url, credential=sas_token)

    return service_client


try:
    print("about to connect to the storage account")
    service_client : DataLakeServiceClient = get_service_client_sas("churnstg2", sas_token=sas_token)
except:
    print("error connecting to the service account")
    pass


# create file system and connect to container with file system
def create_file_system(service_client: DataLakeServiceClient, file_system_name: str) -> FileSystemClient:
    
    file_system_client = service_client.create_file_system(file_system = file_system_name)

    return file_system_client

try:
    print("about to create the container")
    file_system_client : FileSystemClient = create_file_system(service_client=service_client, file_system_name="churncontstg")
    print("done creating the container")
except:
    print("container already exist")
    pass



# create datalake directory client
def create_directory(file_system_client: FileSystemClient, directory_name: str) -> DataLakeDirectoryClient:
    directory_client = file_system_client.create_directory(directory_name)

    return directory_client

# Organize files into a folder like raw_churn/
try:
    print("about to create the directory")
    directory_client : DataLakeDirectoryClient = create_directory(file_system_client=file_system_client, directory_name="raw_churn")
    print("raw_churn directory created successfully.")
except:
    print("directory already exist")


# upload data to the created directory
def upload_file_to_directory( directory_client: DataLakeDirectoryClient, local_path: str, file_name: str):
    file_client = directory_client.get_file_client(file_name)

    with open(file=os.path.join(local_path, file_name), mode="rb") as data:
        file_client.upload_data(data, overwrite=True)


# upload_file_to_directory(directory_client=directory_client, local_path=local_path, file_name="annual-enterprise-survey-2023-financial-year-provisional.csv")

# file = DataLakeFileClient.from_connection_string()
# service_client.get_directory_client()
dir_client = service_client.get_directory_client("churncontstg","raw_churn")

file_client = dir_client.get_file_client("Churn_Modelling.csv")
with open(file=os.path.join(local_path, "Churn_Modelling.csv"), mode="rb") as data:
        file_client.upload_data(data, overwrite=True)


