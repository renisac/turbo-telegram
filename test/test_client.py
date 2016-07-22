from ri_registry.client import Client


def test_client():
    cli = Client('https://localhost:3000', 12345)
    assert cli.remote == 'https://localhost:3000'
