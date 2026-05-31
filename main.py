from lib.config import Config
from lib.whitelisted_client import WhitelistedClient

config = Config()

client = WhitelistedClient(config.url, config.token)

def main():
    pass

if __name__ == '__main__':
    main()
