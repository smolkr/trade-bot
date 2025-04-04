import subprocess
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Primeiro commit"])
subprocess.run(["git", "branch", "-M", "main"])
subprocess.run(["git", "remote", "add", "origin", "https://github.com/smolkr/trade-bot.git"])
subprocess.run(["git", "push", "-u", "origin", "main"])
import pandas as pd
import time
import threading
import queue
STOP_LOSS_PERCENT = 0.005  # 0.5%
TAKE_PROFIT_PERCENT = 0.01  # 1%
open_position = None
entry_price = None
trade_history = []
running = False
bot_thread = None
trade_interval = 1
thread_lock = threading.Lock()
trade_queue = queue.Queue()
def fetch_news_sentiment():
    return np.random.uniform(-1, 1)
def generate_mock_data():
    assets = ['WIN', 'PETR4', 'VALE3', 'ITUB4']
    market_data = {}
    for asset in assets:
        prices = np.random.randn(100).cumsum() + np.random.randint(20, 120) * 1000
        volumes = np.random.randint(100, 10000, 100)
        market_data[asset] = pd.DataFrame({'close': prices, 'volume': volumes})
    return market_data
def calculate_indicators(df):
    df['SMA_9'] = df['close'].rolling(window=9).mean()
    df['SMA_21'] = df['close'].rolling(window=21).mean()
    df['RSI'] = 100 - (100 / (1 + df['close'].pct_change().rolling(14).mean()))
    df['Volume_MA'] = df['volume'].rolling(window=10).mean()
    return df
def choose_best_asset(market_data):
    best_asset = None
    best_score = -np.inf
    sentiment_score = fetch_news_sentiment()    
    for asset, df in market_data.items():
        df = calculate_indicators(df)
        if df['SMA_9'].iloc[-1] > df['SMA_21'].iloc[-1] and df['RSI'].iloc[-1] < 70 and df['volume'].iloc[-1] > df['Volume_MA'].iloc[-1]:
            score = (df['SMA_9'].iloc[-1] - df['SMA_21'].iloc[-1]) + sentiment_score
            if score > best_score:
                best_score = score
                best_asset = asset
    return best_asset, market_data.get(best_asset)
def trade_signal(df):
    global open_position, entry_price
    last_price = df['close'].iloc[-1] 
    if open_position == 'BUY':
        if last_price <= entry_price * (1 - STOP_LOSS_PERCENT) or last_price >= entry_price * (1 + TAKE_PROFIT_PERCENT):
            open_position = None
            trade_history.append({'action': 'SELL', 'price': last_price})
            return 'SELL'
    elif open_position == 'SELL':
        if last_price >= entry_price * (1 + STOP_LOSS_PERCENT) or last_price <= entry_price * (1 - TAKE_PROFIT_PERCENT):
            open_position = None
            trade_history.append({'action': 'BUY', 'price': last_price})
            return 'BUY'
    else:
        if df['SMA_9'].iloc[-1] > df['SMA_21'].iloc[-1] and df['RSI'].iloc[-1] < 70:
            open_position = 'BUY'
            entry_price = last_price
            trade_history.append({'action': 'BUY', 'price': last_price})
            return 'BUY'
        elif df['SMA_9'].iloc[-1] < df['SMA_21'].iloc[-1] and df['RSI'].iloc[-1] > 30:
            open_position = 'SELL'
            entry_price = last_price
            trade_history.append({'action': 'SELL', 'price': last_price})
            return 'SELL'
    return 'HOLD'
def generate_trade_report():
    df = pd.DataFrame(trade_history)
    if df.empty:
        return "Nenhuma operação foi realizada."
    total_trades = len(df)
    buys = df[df['action'] == 'BUY']
    sells = df[df['action'] == 'SELL']
    total_profit = sells['price'].sum() - buys['price'].sum()
    avg_profit_per_trade = total_profit / total_trades if total_trades > 0 else 0
    report = f"\n===== RELATÓRIO DE DESEMPENHO =====\n"
    report += f"Total de Trades: {total_trades}\n"
    report += f"Lucro Total: {total_profit:.2f}\n"
    report += f"Média de Lucro por Trade: {avg_profit_per_trade:.2f}\n"
    report += "================================="
    return report
def process_trades():
    while running:
        try:
            df = trade_queue.get(timeout=trade_interval)
            best_asset, _ = choose_best_asset({"asset": df})
            if df is not None:
                signal = trade_signal(df)
                print(f"Ativo escolhido: {best_asset} | Trade Signal: {signal}")
        except queue.Empty:
            continue
def start_bot():
    global running, bot_thread
    with thread_lock:
        if bot_thread and bot_thread.is_alive():
            print("O bot já está em execução.")
            return
        running = True
        bot_thread = threading.Thread(target=process_trades, daemon=True)
        bot_thread.start()
def stop_bot():
    global running, bot_thread
    with thread_lock:
        running = False
        if bot_thread and bot_thread.is_alive():
            bot_thread.join(timeout=5)
            bot_thread = None
            print("O bot foi interrompido com sucesso.")
def enqueue_trade():
    market_data = generate_mock_data()
    for _, df in market_data.items():
        trade_queue.put(df)
if __name__ == "__main__":
    print("Robô de Trading Iniciado! Para iniciar, chame start_bot(). Para parar, chame stop_bot(). Para adicionar operações à fila, chame enqueue_trade().")
    start_bot()
    enqueue_trade()
    time.sleep(5)
    stop_bot()
    print("Execução encerrada.")
    import subprocess
subprocess.run(["git", "init"])