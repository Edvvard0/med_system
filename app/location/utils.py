import asyncio

import aiohttp

from app.location.schemas import SPersonLocations, SPersonCabinet

json_response = [
    {
        "PersonCode": "1223",
        "PersonRole": "Клиент",
        "LastSecurityPointNumber": 1,
        "LastSecurityPointDirection": "in",
        "LastSecurityPointTime": "2025-03-31T19:15:17.755Z",
    },
    {
        "PersonCode": "1223",
        "PersonRole": "Клиент",
        "LastSecurityPointNumber": 2,
        "LastSecurityPointDirection": "in",
        "LastSecurityPointTime": "2025-03-31T19:15:17.755Z",
    },
    {
        "PersonCode": "1223",
        "PersonRole": "Сотрудник",
        "LastSecurityPointNumber": 2,
        "LastSecurityPointDirection": "in",
        "LastSecurityPointTime": "2025-03-31T19:15:17.755Z",
    },
]


async def get_pearson_location():
    # async with aiohttp.ClientSession() as session:
    #     async with session.get('http://python.org') as response:
    # json = response.json()
    # json: list[SPersonLocations] = [SPersonLocations(**x) for x in json_response]

    json: list[SPersonLocations] = [SPersonLocations(**x) for x in json_response]
    rez = {}

    # print(json)
    for person in json:
        if rez.get(person.LastSecurityPointNumber) is None:
            rez[person.LastSecurityPointNumber] = SPersonCabinet(
                LastSecurityPointNumber=person.LastSecurityPointNumber
            )

        if person.LastSecurityPointDirection == "in":
            if person.PersonRole == "Клиент":
                rez[person.LastSecurityPointNumber].CountPatients += 1
            else:
                rez[person.LastSecurityPointNumber].CountDoctors += 1

    # lst = list(rez.values())
    # return lst
    print(rez[1].CountPatients)
    return rez


# asyncio.run(get_pearson_location())
