#!/usr/bin/env python
import unittest
import ib.type


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
        self.c0 = ib.type.ComboLeg()
        self.c00 = ib.type.ComboLeg()
        self.c1 = ib.type.ComboLeg(1, 2, 'SMART', 1)
        self.c10 = ib.type.ComboLeg(1, 2, 'SMART', 1)
        self.c2 = ib.type.ComboLeg(1, 2, 'SMART', 0)
        self.c20 = ib.type.ComboLeg(2, 3, 'ANY', 0)        


class Contract_Test(unittest.TestCase, TypeTestMixin):
    def setUp(self):
        self.c0 = ib.type.Contract()
        self.c00 = ib.type.Contract()

        syms = dict(symbol='GOOG', sec_type='STK', exchange='SMART',
                    primary_exchange='SMART', currency='USD')
        self.c1 = ib.type.Contract(**syms)
        self.c10 = ib.type.Contract(**syms)

        syms = dict(symbol='GOOG', sec_type='STK', exchange='SMART',
                    primary_exchange='SMART', currency='EUR')
        self.c2 = ib.type.Contract(syms)
        self.c20 = ib.type.Contract(symbol='GOOG')
    
    
if __name__ == '__main__':
    unittest.main()
