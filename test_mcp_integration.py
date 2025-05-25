# test_mcp_integration.py

import pytest
from mcp_integration import get_proxy_auth, create_session

def test_get_proxy_auth():
    username = "test_user"
    password = "test_pass"
    expected = {
        "http": f"http://{username}:{password}@zproxy.lum-superproxy.io:22225",
        "https": f"http://{username}:{password}@zproxy.lum-superproxy.io:22225"
    }
    result = get_proxy_auth(username, password)
    assert result == expected

@pytest.mark.asyncio
async def test_create_session():
    session = await create_session("test_user", "test_pass")
    assert session is not None
    assert hasattr(session, "get")
    await session.aclose()
