# 77file.com Simple Downloader

## Installation

### Install project locally

1. Clone repository

   ```shell
   git clone https://github.com/bayy420-999/ssf-downloader.git
   ```

2. Install required python dependencies

   ```shell
   pip install -r requirements.txt
   ```

3. Install project

   ```shell
   pip install .
   ```

### Install project from pip

```shell
pip install 77file-downloader
```

## Usage

### As a library

1. Importing library

   ```python3
   # This library is asynchrounus library
   # so you need to import asyncio
   import asyncio
   # Import SSFClient
   from ssf_downloader.client import SSFClient
   ```

2. Initialize SSFClient

   You can initialize SSFClient within async context manager

   ```python3
   async def main():
       # You can pass username and password directly
       # or leave it blank, and pass username and password when login()
       async with SSFClient() as client: 
           # Do stuff
   ```

   Or you initilize the client manually (dont forget to close the session)

   ```python3
   async def main():
       # You can pass username and password directly
       # or leave it blank, and pass username and password when login()
       client = SSFClient()
       # Do stuff
   
       # Close session
       await client.close()
   ```

3. Login

   ```python3
   # Username and password is optional
   # but if you didn't pass it during client intialization
   # you need to pass it during login
   await client.login(username, password)
   ```

4. Register (Optional)

   If you don't have 77file.com account, you can register it by calling client.register() method, and pass your registration details

   ```python3
   await client.register(username, email, password)
   ```

5. Get file details (filename, download_link, etc)

   ```python3
   # Pass 77file.com file url
   file_details = await client.get_file_details(url)
   filename = file_details.file_name
   file_size = file_details.file_size
   download_link = file_details.link
   print(f'{filename=}\n{file_size=}\n{download_link=}')
   ```

The final result would be like in `main.py` file

### As CLI Tools

Once you register/login, your login session will be saved

1. Register

   ```shell
   ssf_downloader register --username='your_username' --email='your_email@example.com' --password='your_password'
   ```

2. Login 

   ```shell
   ssf_downloader login --username='your_username' --password='your_password'
   ```

3. Get file details

   ```shell
   ssf_downloader get_file --url='77file.com url' | jq
   ```