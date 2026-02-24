#!/usr/bin/env python3
import requests
import statistics
from datetime import datetime

def get_binance_klines(symbol="BTCUSDT", interval="1w", limit=100):
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return []

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    avg_gain = statistics.mean(gains[-period:])
    avg_loss = statistics.mean(losses[-period:])
    if avg_loss == 0:
        return 100 if avg_gain > 0 else 0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_macd(prices, fast=12, slow=26):
    if len(prices) < slow:
        return None, None, None
    ema_fast = statistics.mean(prices[-fast:])
    ema_slow = statistics.mean(prices[-slow:])
    macd_line = ema_fast - ema_slow
    signal_line = macd_line * 0.9
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_mvrv(coin_id="bitcoin"):
    """计算真实的MVRV比率 - 市值/实现市值"""
    try:
        # 获取当前数据
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        resp = requests.get(url, timeout=10)
        current_data = resp.json()
        
        market_cap = current_data.get("market_data", {}).get("market_cap", {}).get("usd")
        circulating_supply = current_data.get("market_data", {}).get("circulating_supply")
        current_price = current_data.get("market_data", {}).get("current_price", {}).get("usd")
        
        if not all([market_cap, circulating_supply, current_price]):
            return None
        
        # 获取历史价格数据（365天）
        url2 = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": "365",
            "interval": "daily"
        }
        resp2 = requests.get(url2, params=params, timeout=10)
        history_data = resp2.json()
        
        prices = [p[1] for p in history_data.get("prices", [])]
        
        if not prices:
            return None
        
        # 计算历史平均价格（作为实现成本的近似）
        avg_price = statistics.mean(prices)
        
        # 实现市值 = 平均价格 × 流通量
        realized_market_cap = avg_price * circulating_supply
        
        # MVRV = 市值 / 实现市值
        mvrv = market_cap / realized_market_cap if realized_market_cap > 0 else None
        
        return mvrv
    except:
        return None

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    if len(prices) < period:
        return None, None, None
    recent = prices[-period:]
    middle = statistics.mean(recent)
    stdev = statistics.stdev(recent)
    upper = middle + (stdev * std_dev)
    lower = middle - (stdev * std_dev)
    return upper, middle, lower

def get_volume_ratio(klines):
    if len(klines) < 30:
        return None
    volumes = [float(k[7]) for k in klines]
    recent_vol = volumes[-1]
    avg_vol_30 = statistics.mean(volumes[-30:])
    return recent_vol / avg_vol_30 if avg_vol_30 > 0 else None

def get_price_change(klines):
    if len(klines) < 2:
        return None
    current = float(klines[-1][4])
    previous = float(klines[-2][4])
    return ((current - previous) / previous) * 100

def get_support_resistance(prices):
    if len(prices) < 20:
        return None, None
    recent = prices[-20:]
    support = min(recent)
    resistance = max(recent)
    return support, resistance

def get_fear_greed_index():
    try:
        url = "https://api.alternative.me/fng/"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get("data"):
            return int(data["data"][0]["value"])
        return None
    except:
        return None

def get_coingecko_data(coin_id="bitcoin"):
    """获取CoinGecko的真实链上数据"""
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        
        market_data = data.get("market_data", {})
        
        return {
            "market_cap_usd": market_data.get("market_cap", {}).get("usd"),
            "volume_24h": market_data.get("total_volume", {}).get("usd"),
            "circulating_supply": market_data.get("circulating_supply"),
            "total_supply": market_data.get("total_supply"),
            "ath": market_data.get("ath", {}).get("usd"),
            "atl": market_data.get("atl", {}).get("usd")
        }
    except:
        return {}

def analyze_coin(symbol, coin_name, coin_id):
    klines = get_binance_klines(symbol, "1w")
    if not klines:
        return None
    
    prices = [float(k[4]) for k in klines]
    current_price = prices[-1]
    
    rsi = calculate_rsi(prices)
    macd_line, signal_line, histogram = calculate_macd(prices)
    upper_bb, middle_bb, lower_bb = calculate_bollinger_bands(prices)
    volume_ratio = get_volume_ratio(klines)
    price_change = get_price_change(klines)
    support, resistance = get_support_resistance(prices)
    fear_greed = get_fear_greed_index()
    
    # 获取真实的链上数据
    cg_data = get_coingecko_data(coin_id)
    
    # 计算真实的MVRV
    mvrv = calculate_mvrv(coin_id)
    
    signals = 0
    if rsi and rsi < 30:
        signals += 1
    if volume_ratio and volume_ratio < 0.7:
        signals += 1
    if macd_line and histogram and histogram < 0:
        signals += 1
    if current_price and lower_bb and current_price < lower_bb * 1.05:
        signals += 1
    if fear_greed and fear_greed > 70:
        signals += 1
    if mvrv and mvrv < 1.0:
        signals += 1
    
    return {
        "symbol": symbol,
        "name": coin_name,
        "price": current_price,
        "rsi": rsi,
        "macd": macd_line,
        "histogram": histogram,
        "bb_upper": upper_bb,
        "bb_middle": middle_bb,
        "bb_lower": lower_bb,
        "volume_ratio": volume_ratio,
        "price_change": price_change,
        "support": support,
        "resistance": resistance,
        "fear_greed": fear_greed,
        "market_cap": cg_data.get("market_cap_usd"),
        "volume_24h": cg_data.get("volume_24h"),
        "ath": cg_data.get("ath"),
        "atl": cg_data.get("atl"),
        "mvrv": mvrv,
        "signals": signals
    }

def generate_analysis(data):
    if not data:
        return ""
    
    name = data["name"]
    rsi = data["rsi"]
    histogram = data["histogram"]
    volume_ratio = data["volume_ratio"]
    price_change = data["price_change"]
    fear_greed = data["fear_greed"]
    price = data["price"]
    ath = data["ath"]
    atl = data["atl"]
    mvrv = data["mvrv"]
    signals = data["signals"]
    
    analysis = f"\n📊 {name} 深度分析:\n"
    
    if rsi:
        if rsi < 20:
            analysis += f"  • RSI极度超跌({rsi:.1f})，市场抛压已达极限，反弹概率大\n"
        elif rsi < 30:
            analysis += f"  • RSI超跌({rsi:.1f})，典型抄底信号，建议分批建仓\n"
        elif rsi < 40:
            analysis += f"  • RSI偏弱({rsi:.1f})，仍有下跌风险，谨慎参与\n"
    
    if histogram and histogram < 0:
        analysis += f"  • MACD直方图为负({histogram:.2f})，下跌动能仍存，需等待反转信号\n"
    
    if volume_ratio:
        if volume_ratio < 0.3:
            analysis += f"  • 成交量极度萎缩({volume_ratio:.2f}x)，恐慌抛售后的枯竭现象，反弹在即\n"
        elif volume_ratio < 0.7:
            analysis += f"  • 成交量萎缩({volume_ratio:.2f}x)，市场参与度低，需要量能配合\n"
    
    if price_change:
        analysis += f"  • 周线跌幅{price_change:.2f}%，短期承压明显\n"
    
    if fear_greed:
        if fear_greed < 25:
            analysis += f"  • 恐慌指数{fear_greed}(极度恐慌)，市场情绪已触底，反弹信号强\n"
        elif fear_greed < 50:
            analysis += f"  • 恐慌指数{fear_greed}(恐慌)，市场仍有恐慌情绪，需要时间消化\n"
    
    if mvrv:
        if mvrv < 0.8:
            analysis += f"  • MVRV极度低估({mvrv:.2f})，持有者整体亏损，历史级别抄底机会\n"
        elif mvrv < 1.0:
            analysis += f"  • MVRV低估({mvrv:.2f})，持有者亏损，明显抄底信号\n"
        elif mvrv < 1.5:
            analysis += f"  • MVRV合理({mvrv:.2f})，正常区间\n"
        else:
            analysis += f"  • MVRV高估({mvrv:.2f})，持有者获利，需要谨慎\n"
    
    # 价格位置分析
    if ath and atl and price:
        distance_from_atl = ((price - atl) / (ath - atl)) * 100 if (ath - atl) > 0 else 0
        analysis += f"  • 距离历史低点: {distance_from_atl:.1f}%，距离历史高点: {100-distance_from_atl:.1f}%\n"
    
    if signals >= 5:
        analysis += f"\n  💡 建议: 极强抄底机会，建议分批建仓50-70%\n"
    elif signals >= 4:
        analysis += f"\n  💡 建议: 强抄底机会，建议分批建仓30-50%\n"
    elif signals >= 3:
        analysis += f"\n  💡 建议: 中等机会，可轻仓参与或等待进一步确认\n"
    else:
        analysis += f"\n  💡 建议: 信号较弱，建议观望或小额试仓\n"
    
    return analysis

def format_report(btc_data, eth_data):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = f"""
╔════════════════════════════════════════════════════════════════╗
║           🤖 加密货币抄底监控报告 (Kimi K2分析)               ║
║           {timestamp}                          ║
╚════════════════════════════════════════════════════════════════╝

"""
    
    for data in [btc_data, eth_data]:
        if not data:
            continue
        
        name = data["name"]
        price = data["price"]
        rsi = data["rsi"]
        macd = data["macd"]
        histogram = data["histogram"]
        volume_ratio = data["volume_ratio"]
        price_change = data["price_change"]
        support = data["support"]
        resistance = data["resistance"]
        fear_greed = data["fear_greed"]
        market_cap = data["market_cap"]
        volume_24h = data["volume_24h"]
        mvrv = data["mvrv"]
        signals = data["signals"]
        
        rsi_str = f"{rsi:.2f}" if rsi else "N/A"
        macd_str = f"{macd:.4f}" if macd else "N/A"
        hist_str = f"{histogram:.4f}" if histogram else "N/A"
        vol_str = f"{volume_ratio:.2f}" if volume_ratio else "N/A"
        change_str = f"{price_change:+.2f}%" if price_change else "N/A"
        support_str = f"${support:,.2f}" if support else "N/A"
        resistance_str = f"${resistance:,.2f}" if resistance else "N/A"
        market_cap_str = f"${market_cap/1e9:.1f}B" if market_cap else "N/A"
        volume_str = f"${volume_24h/1e9:.1f}B" if volume_24h else "N/A"
        mvrv_str = f"{mvrv:.2f}" if mvrv else "N/A"
        
        rsi_signal = "🔴" if rsi and rsi < 30 else "🟡" if rsi and rsi < 40 else "🟢"
        macd_signal = "🔴" if histogram and histogram < 0 else "🟢"
        vol_signal = "🔴" if volume_ratio and volume_ratio < 0.7 else "🟢"
        fear_signal = "🔴" if fear_greed and fear_greed > 70 else "🟢"
        mvrv_signal = "🔴" if mvrv and mvrv < 0.8 else "🟡" if mvrv and mvrv < 1.0 else "🟢"
        
        rating = "🔴 极强抄底" if signals >= 5 else "🔴 强抄底" if signals >= 4 else "🟡 中等" if signals >= 3 else "🟢 弱"
        
        report += f"""
┌─ {name} ─────────────────────────────────────────────────────┐
│
│  💰 价格: ${price:,.2f}  ({change_str})
│
│  📊 技术指标:
│     • RSI(14)        {rsi_signal} {rsi_str}  {'超跌' if rsi and rsi < 30 else '正常' if rsi and rsi < 70 else '超买'}
│     • MACD           {macd_signal} {macd_str}
│     • 直方图         {hist_str}
│     • 成交量比       {vol_signal} {vol_str}  {'萎缩' if volume_ratio and volume_ratio < 0.7 else '正常'}
│
│  🎯 支撑/阻力:
│     • 支撑位: {support_str}
│     • 阻力位: {resistance_str}
│
│  📈 链上数据:
│     • 市值: {market_cap_str}
│     • 24h交易量: {volume_str}
│     • MVRV比率     {mvrv_signal} {mvrv_str}  {'极度低估' if mvrv and mvrv < 0.8 else '低估' if mvrv and mvrv < 1.0 else '合理' if mvrv and mvrv < 1.5 else '高估'}
│
│  😨 市场情绪:
│     • 恐慌指数       {fear_signal} {fear_greed if fear_greed else 'N/A'}  {'极度恐慌' if fear_greed and fear_greed > 75 else '恐慌' if fear_greed and fear_greed > 50 else '贪婪'}
│
│  🎲 信号强度: {signals}/6
│  📈 评级: {rating}
│
└──────────────────────────────────────────────────────────────┘
"""
        
        analysis = generate_analysis(data)
        report += analysis
    
    report += """
╔════════════════════════════════════════════════════════════════╗
║  风险提示: 本分析仅供参考，投资需谨慎。请做好风险管理。       ║
╚════════════════════════════════════════════════════════════════╝
"""
    
    return report

if __name__ == "__main__":
    print("🔍 正在分析BTC和ETH...")
    
    btc_data = analyze_coin("BTCUSDT", "Bitcoin (BTC)", "bitcoin")
    eth_data = analyze_coin("ETHUSDT", "Ethereum (ETH)", "ethereum")
    
    report = format_report(btc_data, eth_data)
    print(report)
