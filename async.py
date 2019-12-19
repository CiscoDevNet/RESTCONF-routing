#!/usr/bin/env python
import aiohttp
import asyncio
import async_timeout
import json
import logging
import os
from config import USERNAME, PASSWORD, DEVICES


async def parse_result(response, device):
    output = []
    for table in response['ietf-routing:routing-instance']:
        #print (json.dumps(table, indent=2))
        #print(table['name'], table['type'])
        for rib in table['ribs']['rib']:
            if 'routes' in rib:
                # break by 'source-protocol'
                source_protocol =[ r['source-protocol'] for r in rib['routes']['route']]
                source_protocol = [ s.split(":")[1] for s in source_protocol]
                result = {x:source_protocol.count(x) for x in source_protocol}
                #print(rib['address-family'], rib['name'], break_down)

                result['vrf'] = table['name']
                result['table'] = rib['address-family']
                result['device'] = device
                output.append(result)
    #print(output)
    return output

async def restconf(session, device):
    url = "https://{}/restconf/data/ietf-routing:routing-state/routing-instance".format(device)

    with async_timeout.timeout(30):
        #print("before:{}".format(url))
        async with session.get(url) as response:
            #print ("after:{}".format(url))
            return await parse_result(await response.json(), device)
            #return await response.json()


async def main(loop, device):
    try:
        async with aiohttp.ClientSession(loop=loop,
                                     connector=aiohttp.TCPConnector(ssl=False),
                                     headers={"accept": "application/yang-data+json"},
                                     auth=aiohttp.BasicAuth(USERNAME, PASSWORD)) as session:
            return await restconf(session, device)
    except aiohttp.client_exceptions.ContentTypeError:
        logging.warning("Invalid response from device:{}".format(device))
        return []
    except asyncio.TimeoutError:
        logging.warning("Timeout for device:{}".format(device))
        return []

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(
                asyncio.gather(
                    *(main(loop, device) for device in DEVICES)
    )
    )
    flat = [item for sublist in result for item in sublist]
    print(json.dumps(flat))