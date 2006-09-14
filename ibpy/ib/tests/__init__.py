#!/usr/bin/env python
import unittest
import ib.types


class TypeTestMixin:
    def test_null_notequal(self):
        self.assertNotEqual(self.c0, None)
        self.assertNotEqual(self.c0, [])
        self.assertNotEqual(self.c0, '')
        
    def test_identity_equal(self):
        self.assertEqual(self.c0, self.c0)
        self.assertEqual(self.c00, self.c00)
        self.assertEqual(self.c1, self.c10)
        self.assertEqual(self.c2, self.c2)
        
    def test_value_equal(self):
        self.assertEqual(self.c0, self.c00)
        self.assertEqual(self.c1, self.c10)

    def test_specific_notequal(self):
        self.assertNotEqual(self.c1, self.c2)
        self.assertNotEqual(self.c1, self.c20)        


class ComboLeg_Test(unittest.TestCase, TypeTestMixin):
    def setUp(self):
        self.c0 = ib.types.ComboLeg()
        self.c00 = ib.types.ComboLeg()
        self.c1 = ib.types.ComboLeg(1, 2, 'SMART', 1)
        self.c10 = ib.types.ComboLeg(1, 2, 'SMART', 1)
        self.c2 = ib.types.ComboLeg(1, 2, 'SMART', 0)
        self.c20 = ib.types.ComboLeg(2, 3, 'ANY', 0)        


class Contract_Test(unittest.TestCase, TypeTestMixin):
    def setUp(self):
        self.c0 = ib.types.Contract()
        self.c00 = ib.types.Contract()

        syms = dict(symbol='GOOG', secType='STK', exchange='SMART',
                    primaryExch='SMART', currency='USD')
        self.c1 = ib.types.Contract(**syms)
        self.c10 = ib.types.Contract(**syms)

        syms = dict(symbol='GOOG', secType='STK', exchange='SMART',
                    primaryExch='SMART', currency='EUR')
        self.c2 = ib.types.Contract(syms)
        self.c20 = ib.types.Contract(symbol='GOOG')

class ScannerSubscription_Test(unittest.TestCase):
    def setUp(self):
        self.scansub = ib.types.ScannerSubscription()

    def test_empty(self):
        scansub = self.scansub
        self.failUnlessEqual(scansub.numberOfRows, -1)


class Tick_Test(unittest.TestCase):
    def setUp(self):
        self.tick = ib.types.Tick()

    def test_friendly_strings(self):
        tick = self.tick
        self.failUnlessEqual(tick[tick.BID_SIZE], 'bidSize')
        self.failUnlessEqual(tick[tick.BID], 'bidPrice')
        self.failUnlessEqual(tick[tick.ASK], 'askPrice')
        self.failUnlessEqual(tick[tick.ASK_SIZE], 'askSize')
        self.failUnlessEqual(tick[tick.LAST], 'lastPrice')
        self.failUnlessEqual(tick[tick.LAST_SIZE], 'lastSize')
        self.failUnlessEqual(tick[tick.HIGH], 'high')
        self.failUnlessEqual(tick[tick.LOW], 'low')
        self.failUnlessEqual(tick[tick.VOLUME], 'volume')
        self.failUnlessEqual(tick[tick.CLOSE], 'close')
        self.failUnlessEqual(tick[tick.BID_OPTION], 'bidOptComp')
        self.failUnlessEqual(tick[tick.ASK_OPTION], 'askOptComp')
        self.failUnlessEqual(tick[tick.LAST_OPTION], 'lastOptComp')
        self.failUnlessEqual(tick[None], 'unknown')
        self.failUnlessEqual(tick[-1], 'unknown')        
        
    
if __name__ == '__main__':
    unittest.main()
