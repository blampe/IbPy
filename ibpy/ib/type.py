#!/usr/bin/env python
""" ib.type -> data types

"""
class ComboLeg(object):
    """ ComboLeg(...) -> combo leg
        
    """
    keys = dict(zip(('SAME', 'OPEN', 'CLOSE', 'UNKNOWN'),
                    range(0, 4)))

    def __init__(self,
                 con_id=0,
                 ratio=0,
                 action='',
                 exchange='',
                 open_close=0):
        setattr_mapping(self, locals())

    def __eq__(self, other):
        if self is other:
            return True
        if not other:
            return False
        syms = ('action', 'exchange', 'con_id', 'ratio', 'open_close')
        return getattrs(self, syms) == getattrs(other, syms)


class Contract(object):
    """ Contract(...) -> stock or option contract 

    """
    def __init__(self,
                 symbol='',
                 sec_type='',
                 expiry='',
                 strike=0.0,
                 right='',
                 multiplier='',
                 exchange='',
                 currency='', 
                 local_symbol='',
                 combo_legs=None,
                 primary_exchange='',
                 cusip='',
                 ratings='',
                 desc_append='',
                 bond_type='',
                 coupon_type='',
                 callable=False,
                 putable=False,
                 coupon=0.0,
                 convertible=False,
                 maturity='',
                 issue_date=''):
        if combo_legs is None:
            combo_legs = []
        setattr_mapping(self, locals())


    def __str__(self):
        return 'Contract(%s %s %s %s %s %s %s)' % \
               (self.symbol, self.sec_type, self.expiry, self.strike,
                self.right, self.exchange, self.local_symbol)


    def __eq__(self, other):
        if not other:
            return False
        if not isinstance(other, type(self)):
            return False
        if self is other:
            return True
        if len(self.combo_legs) != len(other.combo_legs):
            return False
        if self.sec_type.lower() != other.sec_type.lower():
            return False

        syms = ('symbol', 'exchange', 'primary_exchange', 'currency')
        if getattrs(self, syms) != getattrs(other, syms):
            return False

        if self.sec_type == 'BOND':
            syms = ('putable', 'callable', 'convertible', 'coupon',
                    'cuspi', 'ratings', 'desc_append', 'bond_type',
                    'coupon_type', 'maturity', 'issue_date')
            iseq = getattrs(self, syms) == getattrs(other, syms)
        else:
            syms = ('expiry', 'right', 'multiplier', 'local_symbol')
            iseq = getattrs(self, syms) == getattrs(other, syms)

        if iseq and self.combo_legs:
            for thisleg, otherleg in zip(self.combo_legs, other.combo_legs):
                if thisleg != otherleg:
                    iseq = False
        return iseq


class ContractDetails(object):
    """ ContractDetails(...) -> contract details 

    """
    def __init__(self,
                 summary=None,
                 market_name='', 
                 trading_class='', 
                 con_id=0, 
                 min_tick=0.0,
                 multiplier='',
                 order_types='', 
                 valid_exchanges=''):
        if summary is None:
            summary = Contract()
        price_magnifier = 1
        setattr_mapping(self, locals())

    def __str__(self):
        return 'Details(%s)' % (self.summary, )


class ExecutionDetails(object):
    """ ExecutionDetails(...) -> execution details 

    """
    def __init__(self, 
                 order_id=0,
                 client_id=0,
                 exec_id='',
                 time='',
                 acct_number='',
                 exchange='',
                 side='',
                 shares=0, 
                 price=0.0, 
                 perm_id=0,
                 liquidation=0):
        setattr_mapping(self, locals())


class ExecutionFilter(object):
    """ ExecutionFilter -> what's an execution filter?

    """
    def __init__(self,
                 client_id=0,
                 acct_code='',
                 time='',
                 symbol='',
                 sec_type='',
                 exchange='',
                 side=''):
        setattr_mapping(self, locals())


class Order(object):
    """ Order(...) -> an order 

    """
    origin_customer = 0
    origin_firm = 1

    def __init__(self,

                 # main order fields
                 order_id=0,
                 client_id=0,
                 perm_id=0,
                 action='BUY',
                 quantity=0, 
                 order_type='LMT', 
                 limit_price=0, 
                 aux_price=0, 
                 shares_allocation='',

                 # extended order fields
                 tif='DAY', 
                 oca_group='',
                 account='', 
                 open_close='O',
                 origin=origin_customer,
                 order_ref='',
                 transmit=1, 
                 parent_id=0,
                 block_order=0,
                 sweep_to_fill=0,
                 display_size=0,
                 trigger_method=1,
                 ignore_rth=0,
                 hidden=0,
                 discretionary_amount=0,
                 good_after_time='',
                 good_till_date='',

                 fa_group='',
                 fa_profile='',
                 fa_method='',
                 fa_percentage='',
                 primary_exchange='',
                 shortSaleSlot=0,
                 designatedLocation='',

                 ocaType=0,    
                 rthOnly=0,
                 overridePercentageConstraints=0,                 
                 rule80A='',
                 settlingFirm='',
                 allOrNone=0,
                 minQty='',
                 percentOffset='',
                 eTradeOnly=1,
                 firmQuoteOnly=1,
                 nbboPriceCap='',

                 # box orders
                 auctionStrategy='',   
                 startingPrice='',
                 stockRefPrice='',
                 delta='',
                 stockRangeLower='',
                 stockRangeUpper='',

                 # volatility orders
                 volatility=0.0,
                 volatilityType=0, # 1=daily, 2=annual
                 continuousUpdate=0,
                 referencePriceType=0, # 1=average, 2=bidorask
                 deltaNeutralOrderType='',
                 deltaNeutralAuxPrice=0.0,
                 ):
        setattr_mapping(self, locals())

    def __eq__(self, other):
        if self is other:
            return True
        if not other:
            return False
        if self.perm_id == other.perm_id:
            return True
        syms = ('order_id', 'client_id', 'quantity', 'limit_price',
                'aux_price', 'origin', 'transmit', 'parent_id',
                'block_order', 'sweep_to_fill', 'display_size',
                'trigger_method', 'ignore_rth', 'hidden',
                'discretionary_amount', 'shortSaleSlot',
                'designatedLocation', 'ocaType', 'rthOnly',
                'allOrNone', 'minQty', 'percentOffset',
                'eTradeOnly', 'firmQuoteOnly', 'nbboPriceCap',
                'auctionStrategy', 'startingPrice', 'stockRefPrice',
                'delta', 'stockRangeLower', 'stockRangeUpper', 
                'volatility', 'volatilityType', 'deltaNeutralAuxPrice',
                'continuousUpdate', 'referencePriceType')
        if getattrs(self, syms) != getattrs(other, syms):
            return False

        syms = ('order_type', 'tif', 'oca_group', 'account',
                'open_close', 'order_ref', 'good_after_time',
                'good_till_date', 'primary_exchange', 'rule80A',
                'settlingFirm', 'detalNeutralOrderType')
        return getattrs(self, syms) == getattrs(other, syms)


class ScannerSubscription(object):
    """ ScannerSubscription(...) -> scanner subscription parameters 

    """
    dblmax= ''
    intmax = ''
    def __init__(self,
                 numberOfRows=-1,
                 instrument='',
                 locationCode='',
                 scanCode='',
                 abovePrice=dblmax,
                 belowPrice=dblmax,
                 aboveVolume=intmax,
                 averageOptionVolumeAbove=intmax,
                 marketCapAbove=dblmax,
                 marketCapBelow=dblmax,                 
                 moodyRatingAbove='',
                 moodyRatingBelow='',
                 spRatingAbove='',
                 spRatingBelow='',
                 maturityDateAbove='',
                 maturityDateBelow='',
                 couponRateAbove=dblmax,
                 couponRateBelow=dblmax,
                 excludeConvertible=0,
                 scannerSettingPairs='',
                 stockTypeFilter=''):
        setattr_mapping(self, locals())


class TickType(object):
    """ TickType(...) -> ticker tick type


    """
    (BID_SIZE, BID_PRICE,
     ASK_PRICE, ASK_SIZE,
     LAST_PRICE, LAST_SIZE,
     HIGH, LOW, VOLUME, CLOSE,
     BID_OPTION, ASK_OPTION, LAST_OPTION) = range(0, 13)


    def __getitem__(self, index):
        """ t[i] -> type string at i

        Return strings do not match the IB implementation
        """
        try:
            mapping = dict([(v,k) for k, v in self.__class__.__dict__.items()])
            friendly = mapping[index]            
        except (KeyError, ):
            friendly = 'unknown'
        else:
            friendly = friendly.lower().replace('_', '')
            friendly = friendly.replace('option', 'OptComp')
        return friendly


class Error(object):
    """ Error(...) -> client error type

    """
    def __init__(self, code=0, msg=''):
        setattr_mapping(locals())


def getattrs(obj, seq):
    values = [getattr(obj, k) for k in seq]
    try:
        return [v.lower() for v in values]
    except (AttributeError, ):
        return values


def setattr_mapping(obj, mapping):
    """ setattr_mapping(object, mapping) -> add attributes from mapping to obj

    """
    del(mapping['self'])
    obj.__dict__.update(mapping)
