from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from plykos import PageNotFound

router = APIRouter()



@router.get('/{device}/{buildid}')
async def get_firmware_keys(
    request: Request, device: str, buildid: str
) -> dict:
    try:
        firm = await request.state.client.get_key_data(device, buildid)
    except PageNotFound:
        raise HTTPException(status_code=404, detail='Firmware not found')


    response = {
        'identifier': firm.identifier,
        'buildid': firm.buildid,
        'codename': firm.codename,
        'restoreramdiskexists': any(
            c.name == 'RestoreRamdisk' for c in firm.components
        ),
        'updateramdiskexists': any(c.name == 'UpdateRamdisk' for c in firm.components),
        'keys': [],
    }

    for comp in firm.components:
        image = {
            'image': comp.name,
            'filename': comp.filename,
            'date': datetime.now().isoformat(),
            'key': comp.key.hex(),
        }

        if any(comp.name == x for x in ('RootFS', 'RestoreRamdisk', 'UpdateRamdisk')):
            image['filename'] += '.dmg'

        if comp.iv is not None:
            image['iv'] = comp.iv.hex()
            image['kbag'] = image['iv'] + image['key']

        response['keys'].append(image)

    return response


@router.get('/{device}/{boardconfig}/{buildid}')
async def get_board_firmware_keys(
    request: Request, device: str, boardconfig: str, buildid: str
) -> dict:
    try:
        firm = await request.state.client.get_key_data(device, buildid)
    except PageNotFound:
        raise HTTPException(status_code=404, detail='Firmware not found')

    response = {
        'identifier': firm.identifier,
        'buildid': firm.buildid,
        'codename': firm.codename,
        'restoreramdiskexists': any(
            c.name == 'RestoreRamdisk' for c in firm.components
        ),
        'updateramdiskexists': any(c.name == 'UpdateRamdisk' for c in firm.components),
        'keys': [],
    }

    for comp in firm.components:
        if (comp.model is not None) and (
            comp.model.casefold() != boardconfig.casefold()
        ):
            continue

        image = {
            'image': comp.name,
            'filename': comp.filename,
            'date': datetime.now().isoformat(),
            'key': comp.key.hex(),
        }

        if any(comp.name == x for x in ('RootFS', 'RestoreRamdisk', 'UpdateRamdisk')):
            image['filename'] += '.dmg'

        if comp.iv is not None:
            image['iv'] = comp.iv.hex()
            image['kbag'] = image['iv'] + image['key']

        response['keys'].append(image)

    return response
