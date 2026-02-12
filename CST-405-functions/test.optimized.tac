Optimized Three-Address Code (TAC)
===================================
With function support and control flow

  1: DECL globalA
  2: DECL globalB
  3: DECL globalC
  4: ARRAY_DECL sharedArray[10]
  5: FUNC_BEGIN fillNumbers
  6: PARAM output
  7: output[0] = 100
  8: output[1] = 200
  9: output[2] = 300
 10: RETURN 3
 11: FUNC_END fillNumbers
 12: FUNC_BEGIN readArray
 13: PARAM input
 14: DECL val
 15: t0 = input[0]
 16: val = t0
 17: RETURN val
 18: FUNC_END readArray
 19: FUNC_BEGIN sumFive
 20: PARAM a
 21: PARAM b
 22: PARAM c
 23: PARAM d
 24: PARAM e
 25: DECL x
 26: DECL y
 27: DECL result
 28: t0 = a + b
 29: t1 = t0 + c
 30: x = t1
 31: t1 = d + e
 32: y = t1
 33: t1 = x + y
 34: result = t1
 35: RETURN result
 36: FUNC_END sumFive
 37: FUNC_BEGIN square
 38: PARAM n
 39: DECL result
 40: t1 = n * n
 41: result = t1
 42: RETURN result
 43: FUNC_END square
 44: FUNC_BEGIN cube
 45: PARAM n
 46: DECL sq
 47: DECL result
 48: ARG n
 49: t1 = CALL square, 1
 50: sq = t1
 51: t1 = sq * n
 52: result = t1
 53: RETURN result
 54: FUNC_END cube
 55: FUNC_BEGIN main
 56: ARRAY_DECL localArray[8]
 57: ARRAY_DECL resultArray[5]
 58: DECL a
 59: DECL b
 60: DECL c
 61: DECL d
 62: DECL e
 63: DECL result
 64: PRINT 111
 65: localArray[0] = 10
 66: localArray[1] = 20
 67: localArray[2] = 30
 68: localArray[3] = 40
 69: localArray[4] = 50
 70: t1 = localArray[0]
 71: PRINT t1
 72: t1 = localArray[2]
 73: PRINT t1
 74: t1 = localArray[4]
 75: PRINT t1
 76: PRINT 222
 77: t1 = 3
 78: t0 = t1 + 3
 79: t1 = t0 + 4
 80: t0 = t1 + 5
 81: result = t0
 82: PRINT result
 83: PRINT 333
 84: a = 10
 85: b = 20
 86: c = 30
 87: d = 40
 88: e = 50
 89: ARG a
 90: ARG b
 91: ARG c
 92: ARG d
 93: ARG e
 94: t0 = CALL sumFive, 5
 95: result = t0
 96: PRINT result
 97: PRINT 444
 98: ARG resultArray
 99: t0 = CALL fillNumbers, 1
100: t1 = resultArray[0]
101: PRINT t1
102: t1 = resultArray[1]
103: PRINT t1
104: t1 = resultArray[2]
105: PRINT t1
106: PRINT 555
107: ARG localArray
108: t1 = CALL readArray, 1
109: result = t1
110: PRINT result
111: PRINT 666
112: ARG 5
113: t1 = CALL square, 1
114: a = t1
115: PRINT a
116: ARG 3
117: t1 = CALL cube, 1
118: b = t1
119: PRINT b
120: RETURN 0
121: FUNC_END main
