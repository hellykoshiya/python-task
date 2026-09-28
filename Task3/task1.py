import asyncio
import httpx


DEFAULT_USD_INR_RATE = 90.0


async def get_exchange_rate():

    url = "https://api.frankfurter.dev/v2/rate/usd/inr"

    for attempt in range(3):

        try:
            async with httpx.AsyncClient(timeout=5) as client:

                response = await client.get(url)

                response.raise_for_status()

                data = response.json()

                print("Using live exchange rate.")

                return data["rate"]

        except (httpx.RequestError, httpx.HTTPStatusError) as error:

            print(f"Attempt {attempt + 1} failed: {error}")

            if attempt < 2:

                delay = 2 ** attempt

                print(f"Retrying in {delay} seconds...")

                await asyncio.sleep(delay)

            else:

                print("External currency service is unavailable.")
                print("Using local default exchange rate.")

                return DEFAULT_USD_INR_RATE


async def quickcart_price():

    product = "Wireless Headphones"
    base_price_usd = 50
    demand = "high"

    # Get exchange rate
    exchange_rate = await get_exchange_rate()

    # Dynamic pricing
    if demand == "high":
        dynamic_price_usd = base_price_usd * 1.20

    elif demand == "medium":
        dynamic_price_usd = base_price_usd * 1.10

    else:
        dynamic_price_usd = base_price_usd

    # Convert USD to INR
    dynamic_price_inr = dynamic_price_usd * exchange_rate

    print("\n----- QuickCart -----")
    print(f"Product: {product}")
    print(f"Demand: {demand}")
    print(f"Base Price: ${base_price_usd:.2f}")
    print(f"Dynamic Price: ${dynamic_price_usd:.2f}")
    print(f"Exchange Rate: 1 USD = ₹{exchange_rate:.2f}")
    print(f"Dynamic Price in INR: ₹{dynamic_price_inr:.2f}")


asyncio.run(quickcart_price())