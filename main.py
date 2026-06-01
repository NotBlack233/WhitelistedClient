from lib.config import load_config
from lib.whitelisted_client import WhitelistedClient

config = load_config()

client = WhitelistedClient(config.url, config.token)

def main():
    pass

if __name__ == '__main__':
    main()
