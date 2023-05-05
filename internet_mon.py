# Internet monitoru in python
from datetime import datetime
import asyncio
import aiohttp
from time import sleep


#COSTANTS
SITES = ["www.google.com" , "www.facebook.com" , "www.amazon.com"]
LOG_FILE = "connection.log"

def update_log(logMsg) :
    with open(LOG_FILE , "+a") as logFile :
        logFile.write(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} {logMsg} \n")


async def check_conn(session, url):
    try :
        async with session.get(url) as response :
            #response.raise_for_status()
            html = await response.text()
            return True
    except :
        return False

async def connection_tasks():
    urls = ["".join([r"https://", s]) for s in SITES]
    my_timeout = aiohttp.ClientTimeout(total=2)
    async with aiohttp.ClientSession(timeout=my_timeout) as session:
        tasks = []
        for u in urls:
            task = asyncio.ensure_future(check_conn(session, u))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses

def main() :
    update_log("Script is starting now ... ")
    connectionStatus = True
    stopTime = 0
    while True :
        sleep(1)
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(connection_tasks())
        #print("results" , results)
        if connectionStatus == True :
            if True in results : continue
            else : 
                connectionStatus = False
                stopTime = datetime.now()
                update_log("Connection went down!")
                #print("conn down")
        if connectionStatus == False :
            if True in results :
                connectionStatus = True
                downInterval = (datetime.now() - stopTime).total_seconds()
                update_log(f"Connection is again up after {downInterval} seconds")
                #print("conn up after" , downInterval)
            else : continue

if __name__ == '__main__':
    main()