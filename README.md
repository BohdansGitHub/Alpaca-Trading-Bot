# **Alpaca Trading Bot**

## Description

The Alpaca Trading Bot is a project that demonstrates a trading strategy using the Alpaca API. The bot combines a moving average crossover strategy with risk management and portfolio optimization techniques to make informed buy and sell decisions in the financial markets. This repository serves as a showcase for quantitative research and programming skills, particularly in the context of hedge funds and investment banks.

## Features

* Moving average crossover strategy implementation
* Risk management to control position sizing and protect capital
* Portfolio optimization to determine optimal asset allocation weights
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

## Contact

For inquiries, please, write an email to _kulykbo@gmail.com_ or contact me on LinkedIn https://www.linkedin.com/in/bohdan-kulyk/
