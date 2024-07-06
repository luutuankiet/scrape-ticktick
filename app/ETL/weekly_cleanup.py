#%%

import os,sys; sys.path.append(os.path.dirname(__file__))
from datetime import datetime,timezone

from loader import *
from loader import _delete_tasks

from dagster import op,job,Definitions


#%%

@op
def cleanup():
    TickTickClient._login = new_login
    auth_client = OAuth2(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        cache_path=cache_path
                        )
    client = TickTickClient(username, password, auth_client)
    today = datetime.now(timezone.utc)
    cutoff_date = today - timedelta(days=7)
    # cutoff_date = datetime(2022, 7, 24, tzinfo=timezone.utc)
    # _delete_tasks(end=cutoff_date,client=client)

#%%
@job
def weekly_cleanup():
    cleanup()

import requests

def logout_sessions():
    url = "https://api.ticktick.com/api/v2/user/sessions/others"
    
    headers = {
        "Host": "api.ticktick.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://ticktick.com/",
        "X-Device": '{"platform":"web","os":"macOS 10.15","device":"Firefox 127.0","name":"","version":6003,"id":"66666db22ee6d03d8bb8def7","channel":"website","campaign":"","websocket":"668926ea2ee6d00eaf84b485"}',
        "hl": "en_US",
        "x-tz": "Asia/Ho_Chi_Minh",
        "X-Csrftoken": "HCbSn4vWcB3b7H9Dog9_qcigK2irm60WRPTld3mzCs-1720264431",
        "traceid": "668927422ee6d00eaf84b698",
        "Origin": "https://ticktick.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Connection": "keep-alive",
        "Cookie": "oai=BF857A58CEB4255014A4A8CD86BEABBD72C27262B4099533C7F08651C0AC58BB34CEA7A507E4CD149DA4F308AE280DED446CC66A73DF6834E22B1CB2D760BE262562A9849D460D22C831B1AD1D504EA90C8465438B7D7041657A963817E98413D3056E5F14F48270FF5A558241904A8C1A604A0C2264EFC68F06951BDE44D338F7FC8F1FB633EED091E3CC362DFFF95BB903F85E837AF7F56A03362067985D12; t=0CAB80045A64122B46B09A77BCF00F8272C319C5CD3473130F4A53C351789F86CD1D4B6D1A436199A5072FA070ECB039A48D4358697D80A335CF715A74DAF7CB6D1B271CA435DBA539F54CC9712B9DC2CD01F5A71C143E885BC0C132D417A9285A26F727D16F3BD5C2DD30DAD771BAEE711F9CAEDB90785807E606E0D11DADF25A26F727D16F3BD509D097AD848956646F07136087B1B3F14F442891F6E1DE9061CD5A7B16FB9B794CAF2AB2F9925BD37353686E6CEE8A83; AWSALB=b1H5z0L8InsQDxbDBqKWKJ2Tu+V+7HTFg8snTy7/1zdbrrYOfdwv1kKZaKioBTJMEySuszahKnj1pf31D98QOb0BjddK3OJXbgTnjdC8nQ/JBEiuFcAok+xcBqrGhFTveEc0YHmKOpVn3hDAi67Q/wXw7YsDA2dkHt/u1VD7ALs82pTZhQYDwdMTm5Voeg==; AWSALBCORS=b1H5z0L8InsQDxbDBqKWKJ2Tu+V+7HTFg8snTy7/1zdbrrYOfdwv1kKZaKioBTJMEySuszahKnj1pf31D98QOb0BjddK3OJXbgTnjdC8nQ/JBEiuFcAok+xcBqrGhFTveEc0YHmKOpVn3hDAi67Q/wXw7YsDA2dkHt/u1VD7ALs82pTZhQYDwdMTm5Voeg==; _csrf_token=HCbSn4vWcB3b7H9Dog9_qcigK2irm60WRPTld3mzCs-1720264431",
        "Priority": "u=1",
        "TE": "trailers"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        print("Successfully logged out of all sessions.")
    else:
        print(f"Failed to log out of all sessions. Status code: {response.status_code}")
        print(response.text)

# TODO: Call the function to execute the request. last time ended at client.http_delete(url="https://api.ticktick.com/api/v2/user/sessions/others")
# but very dangerous there ran into a bug it constantly logs me out.
# logout_sessions()







defs =  Definitions(jobs=[weekly_cleanup])

#%%





