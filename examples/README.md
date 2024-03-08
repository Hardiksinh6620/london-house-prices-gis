> Reconstructed archive, assembled 2026-09-29. March 2024 author dates are assigned for this edition, not recovered original work timestamps.

# Aggregate consistency check

Run `python examples/audit_summary.py` from the repository root. It uses only Python's standard library and the transcribed aggregate table. Count is treated as the number of non-null observations; that interpretation must be confirmed against the original data.

Expected result: the reported mean matches sum/count to one decimal place and falls between the reported minimum and maximum. The tool deliberately reports that neither the standard deviation nor raw data were verified. It is an arithmetic consistency check, not a statistical model or a reproduction of the maps.
