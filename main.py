import asyncio
from ssf_downloader.client import SSFClient

async def main():
    username = ''
    email = ''
    password = ''

    async with SSFClient() as client:
        #Register and login
        await client.register(username, email, password)
        await client.login(username, password)

        #After login, your user_info will be updated
        user_info = client.get_user_info()
        print(user_info)

        #And then you can get FileDetails object that contains
        #filename, download link, etc
        url = '' #77file.com url
        file_details = await client.get_file_details(url)

        #Extract file details
        filename = file_details.file_name
        file_size = file_details.file_size
        download_link = file_details.link
        
        print(f'{filename=}\n{file_size=}\n{download_link=}')

if __name__ == '__main__':
    asyncio.run(main())