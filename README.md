# Build-a-Simplified-Trading-Bot-Binance-Futures-Testnet-
This project is a Python-based Simplified Trading Bot built for Binance Futures Testnet (USDT-M). Its main purpose is to place Market and Limit orders using the Binance Testnet API in a secure, structured, and reusable way.

The bot supports both BUY and SELL orders and allows users to interact through a Command Line Interface (CLI). Users can provide inputs such as symbol (e.g., BTCUSDT), side (BUY/SELL), order type (MARKET/LIMIT), quantity, and price (required for LIMIT orders). Input validation is included to ensure correct values and prevent invalid order submissions.

The project follows a modular structure by separating the API client, order handling logic, input validation, and logging configuration into different files. This makes the code clean, easy to maintain, and suitable for future improvements.

A logging system is implemented to store API requests, responses, successful orders, and errors in log files. This helps with debugging and tracking system behavior. Proper exception handling is also included to manage issues like invalid input, API errors, authentication failures, and network problems without crashing the application.

For security, Binance API credentials are stored using environment variables in a .env file instead of hardcoding them into the source code.

This project demonstrates important backend development concepts such as API integration, command-line tools, clean code practices, logging, and error handling. It is designed to be professional, interview-ready, and suitable for internship assignments, technical assessments, and portfolio projects.
