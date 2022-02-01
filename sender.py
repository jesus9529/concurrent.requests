import asyncio
import aiohttp
# import json
# import requests
import time
import file

CONCURRENT_REQUESTS = 2
DATA = {
    'data': file.ENCODED_PDF_FILE,
    'fieldnames': [
        'retention', 'transmittercif', 'tipoiva1', 'total', 'iva0', 'tipoiva3',
        'iva3', 'invoicenumber', 'invoicedate', 'base0', 'base1', 'receptorcif',
        'iva1', 'base2', 'transmittername', 'iva2', 'concept', 'receptorname',
        'base3', 'tipoiva2']
}
URL = 'http://136.244.82.239:8999/async_predict'

async def make_post_request_to_async_predict(session):
    start_time = time.time()
    async with session.post(URL, json=DATA) as response:
        print(response)
        print(time.time() - start_time)

    # print('doing request')
    # data = {
    #     'data': file.ENCODED_PDF_FILE,
    #     'fieldnames': [
    #         'retention', 'transmittercif', 'tipoiva1', 'total', 'iva0', 'tipoiva3',
    #         'iva3', 'invoicenumber', 'invoicedate', 'base0', 'base1', 'receptorcif',
    #         'iva1', 'base2', 'transmittername', 'iva2', 'concept', 'receptorname',
    #         'base3', 'tipoiva2']
    # }
    # url = 'http://136.244.82.239:8999/async_predict'
    # headers = {
    # 'Content-Type': 'application/json'
    # }
    # # response = requests.post(url, data=data)
    # response = requests.request('POST', url, headers=headers, data=json.dumps(data))
    # print(response)


async def manage_requests_tasks():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(0, CONCURRENT_REQUESTS):
            print('adding task')
            task = asyncio.ensure_future(make_post_request_to_async_predict(session))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)

start_time = time.time()
asyncio.get_event_loop().run_until_complete(manage_requests_tasks())
duration = time.time() - start_time
print('Performing {} concurrent request in {} s'.format(CONCURRENT_REQUESTS, duration))