"""Python adapter for line 4's offline ZTO planning event format; no payments."""
import re

ZTO = '0xd782bdea4ef02a0bd391eb9089470c8080f0a68e'


def replay(events):
    balances, bounties, ids = {}, {}, set()

    def name(value):
        if not isinstance(value, str) or not re.fullmatch(r'[a-zA-Z0-9_-]{1,64}', value):
            raise ValueError('invalid identifier')
        return value

    for e in events:
        identifier = name(e['id'])
        if identifier in ids:
            raise ValueError('duplicate event')
        ids.add(identifier)
        if e['token'] != ZTO:
            raise ValueError('ZTO token required')
        kind = e['type']
        if kind in ('deposit', 'open'):
            value = e['amount']
            if not isinstance(value, str) or not re.fullmatch(r'[1-9][0-9]*', value):
                raise ValueError('positive integer amount required')
            amount = int(value)
        if kind == 'deposit':
            who = name(e['account'])
            balances[who] = balances.get(who, 0) + amount
        elif kind == 'open':
            owner, key = name(e['owner']), name(e['bounty'])
            if key in bounties:
                raise ValueError('duplicate bounty')
            if balances.get(owner, 0) < amount:
                raise ValueError('insufficient balance')
            balances[owner] -= amount
            bounties[key] = dict(owner=owner, amount=amount, status='open')
        elif kind in ('pay', 'cancel'):
            b = bounties.get(name(e['bounty']))
            if b is None or b['status'] != 'open':
                raise ValueError('bounty is not open')
            if e['owner'] != b['owner']:
                raise ValueError('owner mismatch')
            who = name(e['worker']) if kind == 'pay' else b['owner']
            balances[who] = balances.get(who, 0) + b['amount']
            b['status'] = 'paid' if kind == 'pay' else 'cancelled'
        else:
            raise ValueError('unknown event type')
    return dict(token=ZTO, balances={k: str(v) for k, v in balances.items()},
                bounties={k: dict(v, amount=str(v['amount'])) for k, v in bounties.items()})
