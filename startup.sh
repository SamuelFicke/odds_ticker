echo "changing dirs"

cd /home/pi/Projects/odds_ticker

echo "running git pull"

python3 /home/pi/Projects/ticker_pull.py

echo "starting GUI"

python3 /home/pi/Projects/odds_ticker/ticker_top.py
