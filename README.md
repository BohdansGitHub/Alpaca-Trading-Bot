# **Alpaca Trading Bot**

## Description

The Alpaca Trading Bot is a trading solution designed to showcase the power of algorithmic trading strategies, risk management, portfolio optimization with **pyportfolioopt** library, parallel computing with the Dask library and the Alpaca API. This project demonstrates the integration of quantitative research, programming skills, financial analysis, and distributed computing to create an effective trading bot for equities.

By combining a moving average crossover strategy with risk management techniques, the bot aims to make informed trading decisions. The portfolio optimization component provides insights into optimal asset allocation, helping traders achieve a balanced and diversified portfolio.

To handle large-scale data processing efficiently, the project leverages the **Dask** library for parallel and distributed computing. This allows for faster data analysis, making the trading bot well-suited for handling substantial amounts of historical and real-time financial data.

This repository is an educational resource for aspiring quantitative researchers, algorithmic traders, and finance enthusiasts. It serves as an example of how to structure and develop a trading bot that incorporates various quantitative techniques and takes advantage of parallel computing to make data-driven investment decisions.

**Note**: This project is designed for paper trading on https://paper-api.alpaca.markets. Keep in mind that in a real-world scenario, you would need to delve deeper into factors, such as risk-adjusted performance metrics, correlation analysis, scenario-based simulations, etc.

## Features

* Utilization of the **Dask** library for parallel and distributed computing to enhance data processing efficiency
* Risk management to control position sizing and protect capital
* Portfolio optimization using the **pyportfolioopt** library to determine optimal asset allocation weights
* Moving average crossover strategy implementation
* Alpaca API integration for fetching historical data and placing orders

## Setup Instructions

1. Clone the repository:
`git clone https://github.com/BohdansGitHub/Alpaca-Trading-Bot.git`
2. Change the current working directory:
`cd Alpaca-Trading-Bot`
3. Install the required packages using pip:
`pip install -r requirements.txt`
4. Obtain Alpaca API keys:
   * Sign up for an Alpaca account at https://alpaca.markets/. 
   * Create API keys with appropriate permissions.
   * Copy your API keys and save them to paste it into the **config.ini** file at Step 5.
5. Create the config.ini file:
   * Duplicate the config.ini.example file and rename it to config.ini.
   * Open the config.ini file in a text editor.
   * Replace the placeholder values with your actual API key and secret.
   * Please note that the **config.ini** file contains sensitive information and should not be shared publicly. Make sure to keep it private and secure.
6. Customize the strategy parameters and settings:
Adjust the parameters in **config.ini** file to suit your strategy. 
7. Run the bot:
`python main.py`

## Acknowledgement

I would like to express my gratitude to the following individuals, projects, and resources that have contributed to the development and success of the Alpaca Trading Bot:

- The [Alpaca](https://alpaca.markets/) team for providing the Alpaca API, which forms the foundation of our trading bot's data retrieval and order execution.
- The creators and maintainers of the [Dask](https://dask.org/) library, including [Matthew Rocklin](https://github.com/mrocklin) and [contributors](https://github.com/dask/dask/graphs/contributors), who enabled us to harness parallel and distributed computing for efficient data processing and strategy execution.
- The [pyportfolioopt](https://pyportfolioopt.readthedocs.io/) library by [Rutger van Haasteren](https://github.com/rshkv), which significantly enhanced portfolio optimization capabilities.

I am also grateful for the wider open-source community, online forums, and resources that have helped me overcome challenges and expand our knowledge.


## Contact

For inquiries, please, write an email to _kulykbo@gmail.com_ or contact me on LinkedIn https://www.linkedin.com/in/bohdan-kulyk/
