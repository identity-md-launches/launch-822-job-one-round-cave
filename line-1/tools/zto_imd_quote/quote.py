#!/usr/bin/env python3
"""Offline integer constant-product quotes for an explicitly supplied ZTO/IMD pool."""

import argparse
import json
import sys


def positive_int(value):
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if number <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return number


def fee_bps(value):
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if not 0 <= number < 10000:
        raise argparse.ArgumentTypeError("must be between 0 and 9999")
    return number


def nonnegative_int(value):
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if number < 0:
        raise argparse.ArgumentTypeError("must be nonnegative")
    return number


def quote(zto_reserve, imd_reserve, input_token, amount_in, fee):
    """Return the maximum integer output under x*y=k with the stated input fee."""
    if input_token == "ZTO":
        reserve_in, reserve_out, output_token = zto_reserve, imd_reserve, "IMD"
    else:
        reserve_in, reserve_out, output_token = imd_reserve, zto_reserve, "ZTO"

    discounted_input = amount_in * (10000 - fee)
    amount_out = discounted_input * reserve_out // (
        reserve_in * 10000 + discounted_input
    )
    post_in, post_out = reserve_in + amount_in, reserve_out - amount_out
    return {
        "input_token": input_token,
        "output_token": output_token,
        "amount_in": amount_in,
        "amount_out": amount_out,
        "fee_bps": fee,
        "reserve_in_before": reserve_in,
        "reserve_out_before": reserve_out,
        "reserve_in_after": post_in,
        "reserve_out_after": post_out,
        "invariant_before": reserve_in * reserve_out,
        "invariant_after": post_in * post_out,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Quote a constant-product ZTO/IMD swap from supplied base-unit reserves."
    )
    parser.add_argument("--zto-reserve", type=positive_int, required=True)
    parser.add_argument("--imd-reserve", type=positive_int, required=True)
    parser.add_argument("--input-token", choices=("ZTO", "IMD"), required=True)
    parser.add_argument("--amount-in", type=positive_int, required=True)
    parser.add_argument("--fee-bps", type=fee_bps, required=True)
    parser.add_argument("--assert-output", type=nonnegative_int)
    args = parser.parse_args()

    result = quote(
        args.zto_reserve, args.imd_reserve, args.input_token, args.amount_in,
        args.fee_bps,
    )
    print(json.dumps(result, indent=2))
    if args.assert_output is not None and result["amount_out"] != args.assert_output:
        print(
            f"expected {args.assert_output}, got {result['amount_out']}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
