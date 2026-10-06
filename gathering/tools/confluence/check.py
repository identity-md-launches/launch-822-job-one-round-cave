#!/usr/bin/env python3
"""Offline synthetic quote-to-bounty integration and adversarial checks."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'shared/confluence'))
from quote import quote
from bounty import replay, ZTO
import json


def check(condition, label):
    if not condition:
        raise ValueError(label)


def reject(events):
    try:
        replay(events)
    except (ValueError, KeyError):
        return
    raise ValueError('invalid events accepted')


def main():
    # Synthetic units only: a quote does not prove a swap or a deposit occurred.
    q = quote(1000, 2000, 'IMD', 100, 30)
    check(q['amount_out'] == 47, 'reverse quote')
    events = [
        dict(id='d1', token=ZTO, type='deposit', account='gathering', amount=str(q['amount_out'])),
        dict(id='o1', token=ZTO, type='open', owner='gathering', bounty='wall-review', amount='30'),
        dict(id='p1', token=ZTO, type='pay', owner='gathering', bounty='wall-review', worker='pepe-01'),
    ]
    state = replay(events)
    check(state['balances'] == {'gathering': '17', 'pepe-01': '30'}, 'payout')
    check(sum(map(int, state['balances'].values())) == 47, 'conservation')
    pending = replay(events[:2])
    check(int(pending['balances']['gathering']) + int(pending['bounties']['wall-review']['amount']) == 47, 'reserved funds')
    cancel = dict(id='c1', token=ZTO, type='cancel', owner='gathering', bounty='wall-review')
    check(replay(events[:2] + [cancel])['balances'] == {'gathering': '47'}, 'cancel')
    reject(events + [dict(events[2], id='p2')])
    reject(events[:1] + [dict(events[1], amount='48')])
    reject([events[0], events[0]])
    reject([dict(events[0], amount='1.5')])
    reject([dict(events[0], token='IMD')])
    reject(events[:2] + [dict(events[2], owner='stranger')])
    reject(events[:2] + [dict(events[1], id='o2')])
    huge = str(2**100)
    check(replay([dict(events[0], amount=huge)])['balances']['gathering'] == huge, 'large integers')
    for amount in (1, 10, 100, 10000):
        for token in ('ZTO', 'IMD'):
            q2 = quote(1000, 2000, token, amount, 30)
            check(q2['invariant_after'] >= q2['invariant_before'], 'pool invariant')
            check(0 <= q2['amount_out'] < q2['reserve_out_before'], 'output bound')
    print(json.dumps({'synthetic_quote': q, 'planning_ledger': state}, indent=2))
    print('PASS: quote-to-bounty, conservation, reservation, cancellation, seven rejection cases, large integers and quote bounds')


if __name__ == '__main__':
    main()
