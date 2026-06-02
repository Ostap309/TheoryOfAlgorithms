def find_best_trade(prices, number_of_stocks):
    if len(prices) < 2:
        return None, None, 0

    min_price = max(prices)  # минимальная цена для покупки
    min_day = 0  # день покупки
    max_profit = 0  # максимальная прибыль
    buy_day = 0  # оптимальный день покупки
    sell_day = 0  # оптимальный день продажи

    for i in range(1, len(prices)):
        if prices[i] < min_price:
            min_price = prices[i]
            min_day = i

        current_profit = prices[i] - min_price

        if current_profit > max_profit:
            max_profit = current_profit
            buy_day = min_day
            sell_day = i

    if max_profit == 0:
        return None, None, 0
    else:
        return buy_day + 1, sell_day + 1, max_profit * number_of_stocks


if __name__ == "__main__":
    stocks = 1000
    stock_prices = [100, 90, 80, 110, 120, 70, 130, 1]

    buy_day, sell_day, profit = find_best_trade(stock_prices, stocks)

    if buy_day is None:
        print("Перепродажа с прибылью невозможна.")
    else:
        print(f"Покупать в день {buy_day}, продавать в день {sell_day}")
        print(f"Максимальная прибыль: {profit} рублей (при покупке {stocks} акций)")
