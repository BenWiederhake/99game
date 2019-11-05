#!/usr/bin/env python3

#K, V = 8, 4
K, V = 32, 4

B = 6  # Hard-coded, can't change
#B = 14
PTR_SIZE = 8  # Usually fixed

leaf_size = (PTR_SIZE + 2 + 2 + (K + V) * (2 * B - 1))
internal_size = leaf_size + PTR_SIZE * (2 * B)

asymp_min_bytes_per_entry = (leaf_size * 1 + internal_size * 1 / (B - 1)) / (2 * B - 1)
asymp_max_bytes_per_entry = (leaf_size * 1 + internal_size * 1 / (B - 1)) / (B - 1)
max_overhead = (asymp_max_bytes_per_entry - K - V) / (K + V)
min_overhead = (asymp_min_bytes_per_entry - K - V) / (K + V)

print('Parameters: K={}, V={}, B={}, P={}'.format(K, V, B, PTR_SIZE))
print('Node sizes are {} and {}.'.format(leaf_size, internal_size))
print('Need asymptotically {:.2f} to {:.2f} bytes per entry.  ({} for the data itself.)'.format(asymp_min_bytes_per_entry, asymp_max_bytes_per_entry, K + V))
print('That is an overhead of {:.2f}% to {:.2f}%.'.format(100 * min_overhead, 100 * max_overhead))
