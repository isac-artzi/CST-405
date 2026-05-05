Optimized Three-Address Code (TAC)
===================================
With function support and control flow

  1: FUNC_BEGIN main
  2: DECL i
  3: DECL sum
  4: sum = 0
  5: i = 1
  6: L0:
  7: t0 = i <= 5
  8: IF_FALSE t0 GOTO L2
  9: t0 = sum + i
 10: sum = t0
 11: L1:
 12: t0 = i + 1
 13: i = t0
 14: GOTO L0
 15: L2:
 16: PRINT sum
 17: FUNC_END main
