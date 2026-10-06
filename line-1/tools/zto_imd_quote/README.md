# ZTO/IMD offline quote

This tool calculates an integer constant-product swap quote from reserve values supplied on the command line. It supports ZTO to IMD and IMD to ZTO. It uses base units, floors the output as a pool contract normally would, and prints the reserves and invariant before and after the swap. `--assert-output` makes an unexpected quote fail with a nonzero exit code.

Run this demonstration from the repository root:

```sh
python3 line-1/tools/zto_imd_quote/quote.py --zto-reserve 1000 --imd-reserve 2000 --input-token ZTO --amount-in 100 --fee-bps 30 --assert-output 181
```

The command prints an output of 181 IMD base units and exits successfully. In the local trial, the reverse direction and a wrong expected output were also checked; the latter exited nonzero. No install, network access, wallet, key, environment variable, or input file is needed. Reserve values and the fee must come from a trusted snapshot before this can represent an actual pool. The tool does not discover or attest to a live pool, and it does not account for transfer-tax tokens or other nonstandard pool rules.
