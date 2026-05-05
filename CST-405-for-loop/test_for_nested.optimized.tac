Optimized Three-Address Code (TAC)
===================================
With function support and control flow

  1: FUNC_BEGIN main
  2: DECL i
  3: DECL j
  4: DECL product
  5: i = 1
  6: L0:
  7: t0 = i <= 3
  8: IF_FALSE t0 GOTO L2
  9: j = 1
 10: L3:
 11: t0 = j <= 3
 12: IF_FALSE t0 GOTO L5
 13: t0 = i * j
 14: product = t0
 15: PRINT product
 16: L4:
 17: t0 = j + 1
 18: j = t0
 19: GOTO L3
 20: L5:
 21: L1:
 22: t0 = i + 1
 23: i = t0
 24: GOTO L0
 25: L2:
 26: FUNC_END main
