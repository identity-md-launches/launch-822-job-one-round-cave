import assert from 'node:assert/strict';

export const ZTO = '0xd782bdea4ef02a0bd391eb9089470c8080f0a68e';
// Pure, offline accounting: integer base units, never floating-point prices.
export function replay(events) {
  const balances = new Map();
  const ids = new Set();
  const bounties = new Map();
  const amount = x => {
    if (typeof x !== 'string' || !/^[1-9][0-9]*$/.test(x)) throw Error('positive integer amount required');
    return BigInt(x);
  };
  const name = x => {
    if (typeof x !== 'string' || !/^[a-zA-Z0-9_-]{1,64}$/.test(x)) throw Error('invalid identifier');
    return x;
  };
  const debit = (who, n) => {
    if ((balances.get(who) ?? 0n) < n) throw Error('insufficient balance');
    balances.set(who, balances.get(who) - n);
  };
  const credit = (who, n) => balances.set(who, (balances.get(who) ?? 0n) + n);
  for (const e of events) {
    name(e.id);
    if (ids.has(e.id)) throw Error('duplicate event');
    ids.add(e.id);
    if (e.token !== ZTO) throw Error('ZTO token required');
    if (e.type === 'deposit') credit(name(e.account), amount(e.amount));
    else if (e.type === 'open') {
      const owner = name(e.owner), key = name(e.bounty), n = amount(e.amount);
      if (bounties.has(key)) throw Error('duplicate bounty');
      debit(owner, n);
      bounties.set(key, { owner, amount: n, status: 'open' });
    } else if (e.type === 'pay' || e.type === 'cancel') {
      const b = bounties.get(name(e.bounty));
      if (!b || b.status !== 'open') throw Error('bounty is not open');
      if (e.owner !== b.owner) throw Error('owner mismatch');
      credit(e.type === 'pay' ? name(e.worker) : b.owner, b.amount);
      b.status = e.type === 'pay' ? 'paid' : 'cancelled';
    } else throw Error('unknown event type');
  }
  return {
    token: ZTO,
    balances: Object.fromEntries([...balances].map(([k, v]) => [k, String(v)])),
    bounties: Object.fromEntries([...bounties].map(([k, v]) => [k, { ...v, amount: String(v.amount) }]))
  };
}

if (process.argv[1]?.endsWith('/ledger.mjs')) {
  const events = [
    { id: 'd1', token: ZTO, type: 'deposit', account: 'gathering', amount: '100' },
    { id: 'o1', token: ZTO, type: 'open', owner: 'gathering', bounty: 'wall-check', amount: '30' },
    { id: 'p1', token: ZTO, type: 'pay', owner: 'gathering', bounty: 'wall-check', worker: 'pepe-01' }
  ];
  const result = replay(events);
  assert.equal(result.balances.gathering, '70');
  assert.equal(result.balances['pepe-01'], '30');
  assert.throws(() => replay([...events, { ...events[2], id: 'p2' }]), /not open/);
  assert.throws(() => replay([events[0], { ...events[1], amount: '101' }]), /insufficient/);
  assert.throws(() => replay([events[0], events[0]]), /duplicate/);
  assert.throws(() => replay([{ ...events[0], amount: '1.5' }]), /integer/);
  const cancelled = replay([events[0], events[1], { id: 'c1', token: ZTO, type: 'cancel', owner: 'gathering', bounty: 'wall-check' }]);
  assert.equal(cancelled.balances.gathering, '100');
  console.log(JSON.stringify(result, null, 2));
  console.log('PASS: payout, cancellation, overdraft, duplicate and double-payment checks');
}
