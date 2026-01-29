Optimized Three-Address Code (TAC)
===================================
With function support and control flow

  1: FUNC_BEGIN add
  2: PARAM a
  3: PARAM b
  4: DECL result
  5: t0 = a + b
  6: result = t0
  7: RETURN result
  8: FUNC_END add
  9: FUNC_BEGIN computeConstants
 10: DECL x
 11: DECL y
 12: DECL z
 13: t0 = 8
 14: x = t0
 15: t0 = 20
 16: y = t0
 17: t0 = x + y
 18: z = t0
 19: RETURN z
 20: FUNC_END computeConstants
 21: FUNC_BEGIN complexCalculation
 22: PARAM n
 23: DECL a
 24: DECL b
 25: DECL c
 26: DECL result
 27: t0 = n + 0
 28: a = t0
 29: t0 = 6
 30: b = t0
 31: t0 = a + b
 32: c = t0
 33: t0 = c * 1
 34: result = t0
 35: RETURN result
 36: FUNC_END complexCalculation
 37: FUNC_BEGIN main
 38: DECL x
 39: DECL y
 40: DECL z
 41: DECL w
 42: DECL result1
 43: DECL result2
 44: t0 = 15
 45: x = t0
 46: t0 = 12
 47: y = t0
 48: ARG x
 49: ARG y
 50: t0 = CALL add, 2
 51: z = t0
 52: t0 = 12
 53: w = t0
 54: t0 = CALL computeConstants, 0
 55: result1 = t0
 56: ARG z
 57: t0 = CALL complexCalculation, 1
 58: result2 = t0
 59: PRINT z
 60: PRINT result1
 61: PRINT result2
 62: RETURN 0
 63: FUNC_END main
