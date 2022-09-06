
import os, sys
from TradingFW import TradingFW



def main():

    mdfs_paths = os.listdir("MarketDataFiles")
    mdfs_paths = [os.path.join("MarketDataFiles",p) for p in mdfs_paths]
    mdfs_paths = [p for p in mdfs_paths if p.endswith("csv")]

    mdfs_data = []
    for path in mdfs_paths:
        data = TradingFW()
        data.read_csv(path)
        mdfs_data.append(data)
        print(data.describe())

        print("calculate SMA...")
        data.SMA_signals(short_window=100,long_window=1000)
        data.plot_SMA()

        print("calculate portfolio...")
        initial_investment = 100000
        data.calculate_portfolio(initial_investment)
        data.plot_portfolio()

        total = data.results[-1]["total"]
        print("result: " +str(total-initial_investment))






if __name__ == "__main__":
    main()