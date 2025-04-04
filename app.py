from flask import Flask, render_template, jsonify
import boottrade

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start')
def start_bot():
    boottrade.start_bot()
    return jsonify({'message': 'Bot iniciado!'})

@app.route('/stop')
def stop_bot():
    boottrade.stop_bot()
    return jsonify({'message': 'Bot parado!'})

@app.route('/enqueue')
def enqueue_trade():
    boottrade.enqueue_trade()
    return jsonify({'message': 'Trade adicionado à fila!'})

@app.route('/report')
def trade_report():
    report = boottrade.generate_trade_report()
    return jsonify({'report': report})

if __name__ == '__main__':
    app.run(debug=True)
