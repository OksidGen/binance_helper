import asyncio


async def main():
    from binance_helper import server
    await server.Server().start()

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    asyncio.run(main())
