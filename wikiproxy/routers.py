import aiohttp
from fastapi import APIRouter

from .wiki import get_key_page, parse_page

router = APIRouter()


@router.get('/{identifier}/{buildid}')
async def get_firmware_keys(identifier: str, buildid: str) -> dict:
    async with aiohttp.ClientSession() as session:
        page = await get_key_page(session, identifier, buildid)

    return parse_page(page, identifier)


@router.get('/{identifier}/{boardconfig}/{buildid}')
async def get_board_firmware_keys(
    identifier: str, boardconfig: str, buildid: str
) -> dict:
    async with aiohttp.ClientSession() as session:
        page = await get_key_page(session, identifier, buildid)

    return parse_page(page, identifier, boardconfig)
