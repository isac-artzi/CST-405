Unoptimized Three-Address Code (TAC)
=====================================
Intermediate representation with functions

  1: FUNC_BEGIN main
  2: DECL i
  3: DECL sum
  4: PRINT 1111
  5: sum = 0
  6: i = 1
  7: L0:
  8: t0 = i <= 5
  9: IF_FALSE t0 GOTO L1
 10: t0 = sum + i
 11: sum = t0
 12: t0 = i + 1
 13: i = t0
 14: GOTO L0
 15: L1:
 16: PRINT sum
 17: RETURN 0
 18: FUNC_END main
