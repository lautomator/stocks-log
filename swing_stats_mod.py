#!/usr/local/bin/python3

import datetime
from collections import Counter


metrics = {
    'trading period': 0, # months
    'total number of trades': 0,
    'avg trades per month': 0,
    'avg trades per week': 0,
    'avg trade length': 0, # days
    'total profits': 0,
    'total losses': 0,
    'avg monthly profits': 0,
    'avg monthly losses': 0,
    'final pnl': 0,
    'avg roi': 0,
    'long trades': 0,
    'short trades': 0,
    'avg entry price': 0,
    'avg risk amount': 0,
    'most traded': []
}


def total_trades(data):
    return len(data)


def trading_period(data):
    entry_months = []
    entry_month = 0

    for row in data:
        entry_month = datetime.datetime.strptime(
            row['entry date'], '%m/%d/%Y').month
        entry_months.append(entry_month)

    max_month = max(entry_months)
    min_month = min(entry_months)
    period = max_month - min_month + 1
    return period


def avg_no_of_trades(total_trades, period):
    weeks = period * 4
    monthly = round(total_trades / period)
    weekly = round(total_trades / weeks)
    avg_no_trades = {
        'monthly': monthly,
        'weekly': weekly
    }
    return avg_no_trades


def avg_trade_length(data):
    avg_trade_len = 0
    trade_lengths = []
    start = None
    stop = None
    trade_length = None

    for row in data:
        start = datetime.datetime.strptime(row['entry date'], '%m/%d/%Y')
        stop = datetime.datetime.strptime(row['sell date'], '%m/%d/%Y')
        trade_length = (stop - start).days + 1
        trade_lengths.append(trade_length)

    avg_trade_len = round(sum(trade_lengths) / len(trade_lengths))
    return avg_trade_len


def profit_and_loss(period, data):
    pnl = {
        'total profits': 0,
        'monthly profits': 0,
        'total losses': 0,
        'monthly losses': 0,
        'pnl': 0
    }

    tp = 0
    mp = 0
    tl = 0
    ml = 0

    for row in data:
        if float(row['pnl']) > 0:
            tp += float(row['pnl'])
        else:
            tl += float(row['pnl'])

    mp = tp / period
    ml = tl / period

    pnl['total profits'] = round(tp, 2)
    pnl['monthly profits'] = round(mp, 2)
    pnl['total losses'] = round(tl, 2)
    pnl['monthly losses'] = round(ml, 2)
    pnl['pnl'] = tp + tl
    return pnl


def return_of_investment(net_return, data):
    roi = 0
    ent_p = 0 # entry price
    ext_p = 0 # exit price
    shares = 0
    profit = 0
    all_rois = []
    avg_roi = 0 # expressed as a percentage

    # (((entry price - exit price) * no of shares) /
    # (exit price * no of shares)) * 100
    # ref: https://www.investopedia.com/articles/basics/10/guide-to-calculating-roi.asp

    for row in data:
        ent_p = float(row['entry price'])
        ext_p = float(row['exit price'])
        shares = int(row['shares'])
        profit = (ext_p - ent_p) * shares

        roi = round((profit / (ent_p * shares)) * 100, 2)
        all_rois.append(roi)

    avg_roi = round(sum(all_rois) / len(all_rois))
    return avg_roi


def trade_type_amts(data):
    trade_types = {
        'long': 0,
        'short': 0
    }

    tlong = 0
    tshort = 0

    for row in data:
        if int(row['shares']) > 0:
            tlong += 1
        else:
            tshort += 1

    trade_types['long'] = tlong
    trade_types['short'] = tshort
    return trade_types


def price_averager(data, col_name):
    total_entries = 0
    total_entries_amt = 0
    avg_entry = 0

    for row in data:
        total_entries_amt += float(row[col_name])
        total_entries += 1

    avg_entry = round(total_entries_amt / total_entries, 2)
    return avg_entry


def get_most_traded_equity(data):
    all_symbols = []
    the_winner = []

    for row in data:
        all_symbols.append(row['investment'])

    occurence_count = Counter(all_symbols)

    the_winner.append(occurence_count.most_common(1)[0][0])
    the_winner.append(occurence_count.most_common(1)[0][1])
    return the_winner
