# bittrex-notify
Short and simple script to notify you via Pushbullet whenever one of your open orders on Bittrex completes (or gets cancelled).

## Usage
Create a `secret.py` file in the same folder and declare three variables:

```python
PUSHBULLET_KEY = 'pushbullet api key here'
BITTREX_KEY = 'bittrex api key here'
BITTREX_SECRET = 'bittrex secret key here'

```

Run the script with `python notifications.py`.
