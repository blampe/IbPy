#!/usr/bin/env python
""" ib.client.message -> Interactive Brokers client socket reader.

These types provide the logic of reading encoded TWS data and turning
that data into Message objects.  The types inherit the dispatch
method, which they use to send the Message objects to registered
listeners.
"""
import ib.lib
import ib.types


logger = ib.lib.logger()


class SocketReader(object):
    """ SocketReader() -> dispatching socket reader

    Subtypes encapsulate the logic of reading values from a socket
    object encoded by the TWS application.  After instances read data,
    they generate Message objects and send them to registered
    listeners via the dispatch method.
    """
    def __init__(self, listeners=None):
        if listeners is None:
            listeners = []
        self.listeners = listeners


    def __str__(self):
        return self.__class__.__name__


    def dispatch(self, **kwds):
        """ dispatch(**kwds) -> send a new Message instance to listeners

        """
        for listener in self.listeners:
            try:
                msg = self.detail(**kwds)
                if isinstance(msg, Error.detail):
                    log = logger.warning
                else:
                    log = logger.info
                log('%s%s' % ('    ', msg, ))
                listener(msg)
            except (Exception, ), ex:
                logger.error(str(ex))


class Message(object):
    """ Message(**kwds) -> parent type for detail classes.

    Subtypes must specify __slots__ for instances to have attributes.
    The keywords specified in the constructor must be present in the
    __slots__ tuple.
    """
    __slots__ = ()

    def __init__(self, **kwds):
        for name, value in kwds.items():
            setattr(self, name, value)


    def __str__(self):
        args = ['%s=%s' % (atr, getattr(self, atr)) for atr in self.__slots__]
        return str.join(' ', args)


class Account(SocketReader):
    """ Account() -> parent type for account-related readers

    Using a parent class enables the client to specify a single
    listener for multiple but related readers.
    """
    class detail(Message):
        __slots__ = ('key', 'value', 'currency', 'account_name', )


class AccountValue(Account):
    """ AccountValue() -> reads account value messages

    Generated detail instance:

    msg.key - name of the account update field
    msg.value - value of the update
    msg.currency - currency type
    msg.account_name - guess!
    """
    def read(self, read_int, read_float, read_str):
        """ read(...) -> read an account value message

        """
        version = read_int()
        key = read_str()
        value = read_str()
        currency = read_str()

        account_name = ''
        if version >= 2:
            account_name = read_str()

        ## suppress empty strings but not 0.0 or 0
        ## this odd behavior is new, and needs to be checked
        ## against current ib client sources
        #if value == '':
        #    return
        ## otherwise just dispatch the message normally

        self.dispatch(key=key,
                      value=value,
                      currency=currency,
                      account_name=account_name)


class AccountTime(Account):
    """ AccountTime() -> reads account time stamp messages

    Generated detail instance:

    msg.key - 'TimeStamp'
    msg.value - time the broker updated the account
    msg.currency - ""
    """
    def read(self, read_int, read_float, read_str):
        """ read(...) -> read an account update time message

        """
        version = read_int()
        time_stamp = read_str()
        self.dispatch(key='TimeStamp',
                      value=time_stamp,
                      currency='',
                      account_name='')


class ContractDetails(SocketReader):
    """ ContractDetails() -> reads contract detail messages

    Generated detail instance:

    msg.details - full description of a contract
    """
    class detail(Message):
        __slots__ = ('details', )


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read a contract details message

        """
        details = ib.types.ContractDetails()

        version = read_int()
        details.summary.symbol = read_str()
        details.summary.secType = read_str()
        details.summary.expiry = read_str()
        details.summary.strike = read_float()
        details.summary.right = read_str()
        details.summary.exchange = read_str()
        details.summary.currency = read_str()
        details.summary.localSymbol = read_str()
        details.marketName = read_str()
        details.tradingClass = read_str()
        details.conId = read_int()
        details.minTick = read_float()
        details.multiplier = read_str()
        details.orderTypes = read_str()
        details.validExchanges = read_str()
        if version >= 2:
            details.price_magnifier = read_int()            
        self.dispatch(details=details)


class Error(SocketReader):
    """ Error() -> reads error messages

    Generated detail instance:

    msg.error_id - order id or ticker id that generated the error
    msg.error_code - error codes are documented by IB
    msg.error_msg - textual description of the error, documented by IB
    """
    class detail(Message):
        __slots__ = ('error_id', 'error_code', 'error_msg', )


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read an error message

        """
        version = read_int()

        if version < 2:
            error_id = error_code = None
            error_msg = read_str()
        else:
            error_id = read_int()
            error_code = read_int()
            error_msg = read_str()

        self.dispatch(error_id=error_id, 
                      error_code=error_code, 
                      error_msg=error_msg)


class Execution(SocketReader):
    """ Execution() -> reads execution detail messages

    Generated detail instance:

    msg.orderId - order id specified in the call to place order
    msg.contract - description of the executed contract 
    msg.details - addition order execution details
    """
    class detail(Message):
        __slots__ = ('orderId', 'contract', 'details', )


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read an execution details message

        """
        contract = ib.types.Contract()
        details = ib.types.Execution()

        version = read_int()
        orderId = read_int()

        contract.symbol = read_str()
        contract.secType = read_str()
        contract.expiry = read_str()
        contract.strike = read_float()
        contract.right = read_str()
        contract.exchange = read_str()
        contract.currency = read_str()
        contract.localSymbol = read_str()

        details.orderId = orderId
        details.exec_id = read_str()
        details.time = read_str()
        details.acct_number = read_str()
        details.exchange = read_str()
        details.side = read_str()
        details.shares = read_int()
        details.price = read_float()

        if version >= 2:
            details.permId = read_int()

        if version >= 3:
            details.clientId = read_int()

        if version >= 4:
            details.liquidation = read_int()

        self.dispatch(orderId=orderId,
                      contract=contract,
                      details=details)


class ManagedAccounts(SocketReader):
    """ ManagedAccounts() -> reads a list of managed account ids

    """
    class detail(Message):
        __slots__ = ('accounts', )


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read a managed accounts message

        """
        version = read_int()
        accounts = read_str()
        self.dispatch(accounts=accounts)


class MarketDepth(SocketReader):
    """ MarketDepth() -> reads market depth messages

    Generated detail instance:

    msg.ticker_id - ticker id specified the call to request_market_depth
    msg.position - specifies the row id of the order
    msg.operation - identifies how this message should be applied to the
                      market depth.  Valid values:
                      0 = insert
                      1 = update
                      2 = delete
    msg.side - side of the book to which this order belongs. Valid values:
                 0 = ask
                 1 = bid
    msg.price - order price
    msg.size - order size
    """
    class detail(Message):
        __slots__ = ('ticker_id', 'position', 'operation', 
                     'side', 'price', 'size', )


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read a market depth message

        """
        version = read_int()
        ticker_id = read_int()
        position = read_int()
        operation = read_int()
        side = read_int()
        price = read_float()
        size = read_int()

        self.dispatch(ticker_id=ticker_id,
                      position=position,
                      operation=operation,
                      side=side,
                      price=price,
                      size=size)


class MarketDepthLevel2(SocketReader):
    """ MarketDepthLevel2Reader() -> reads level 2 market depth messages

    Generated detail instance:

    msg.ticker_id - ticker id specified the call to request_market_depth
    msg.position - specifies the row id of the order
    msg.market_maker - specifies the exchange hosting this order
    msg.operation - identifies how this message should be applied to the
                      market depth.  Valid values:
                      0 = insert
                      1 = update
                      2 = delete
    msg.side - side of the book to which this order belongs. Valid values:
                 0 = ask
                 1 = bid
    msg.price - order price
    msg.size - order size
    """
    class detail(Message):
        __slots__ = ('ticker_id', 'position', 'market_maker', 'operation', 
                     'side', 'price', 'size', )


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read a market depth level 2 message

        """
        version = read_int()
        ticker_id = read_int()
        position = read_int()
        market_maker = read_str()
        operation = read_int()
        side = read_int()
        price = read_float()
        size = read_int()

        self.dispatch(ticker_id=ticker_id,
                      position=position,
                      market_maker=market_maker,
                      operation=operation, 
                      side=side,
                      price=price,
                      size=size)


class NextId(SocketReader):
    """ NextId() -> reads next valid id messages

    Generated detail instance:

    msg.next_valid_id - first order id acceptable to the broker
    """
    class detail(Message):
        __slots__ = ('next_valid_id', )


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read a next order id message

        """
        version = read_int()
        next_valid_id = read_int()
        self.dispatch(next_valid_id=next_valid_id)


class OpenOrder(SocketReader):
    """ OpenOrder() -> reads open order messages

    Generated detail instance:

    msg.orderId - the order id assigned by the broker
    msg.contract - describes the contract
    msg.order - details of the open order
    """
    class detail(Message):
        __slots__ = ('orderId', 'contract', 'order', )


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read an open order message

        """
        contract = ib.types.Contract()
        order = ib.types.Order()

        version = read_int()
        order.orderId = read_int()
        
        contract.symbol = read_str()
        contract.secType = read_str()
        contract.expiry = read_str()
        contract.strike = read_float()
        contract.right = read_str()
        contract.exchange = read_str()
        contract.currency = read_str()

        if version >= 2:
            contract.localSymbol = read_str()
            
        order.action = read_str()
        order.totalQuantity = read_int()
        order.orderType = read_str()
        order.lmtPrice = read_float()
        order.auxPrice = read_float()
        order.tif = read_str()
        order.ocaGroup = read_str()
        order.account = read_str()
        order.openClose = read_str()
        order.origin = read_int()
        order.orderRef = read_str()

        if version >= 3:
            order.clientId = read_int()

        if version >= 4:
            order.permId = read_int()
            order.ignoreRth = (read_int() == 1)
            order.hidden = (read_int() == 1)
            order.discretionaryAmt = read_float()

        if version >= 5:
            order.goodAfterTime = read_str()

        if version >= 6:
            order.sharesAllocation = read_str()

        if version >= 7:
            order.faGroup = read_str()
            order.faMethod = read_str()
            order.faPercentage = read_str()
            order.faProfile = read_str()

        if version >= 8:
            order.goodTillDate = read_str()

        if version >= 9:
            order.rule80A = read_str()
            order.percentOffset = read_float()
            order.settlingFirm = read_str()
            order.shortSaleSlot = read_int()
            order.designatedLocation = read_str()
            order.auctionStrategy = read_int()
            order.startingPrice = read_float()
            order.stockRefPrice = read_float()
            order.delta = read_float()
            order.stockRangeLower = read_float()
            order.stockRangeUpper = read_float()
            order.displaySize = read_int()
            order.rthOnly = read_int()
            order.blockOrder = read_int()
            order.sweepToFill = read_int()
            order.allOrNone = read_int()
            order.minQty= read_int()
            order.ocaType = read_int()
            order.eTradeOnly = read_int()
            order.firmQuoteOnly = read_int()
            order.nbboPriceCap = read_float()

        if version >= 10:
            order.parentId = read_int()
            order.triggerMethod = read_int()

        self.dispatch(orderId=order.orderId, 
                      contract=contract, 
                      order=order)


class OrderStatus(SocketReader):
    """ OrderStatus() -> reads order status messages

    Generated detail instance:

    msg.orderId - order id specified previously 
    msg.message - order status
    msg.filled - number of shares executed
    msg.remaining - number of shares still outstanding
    msg.avg_fill_price - average price of executed shares 
    msg.permId - permanent id maintained by the broker
    msg.parentId - parent id for bracket or auto trailing stop orders
    msg.last_fill_price - price of the last shares executed
    """
    class detail(Message):
        __slots__ = ('orderId', 'message', 'filled', 'remaining',
                     'permId', 'parentId', 'last_fill_price',
                     'avg_fill_price', 'clientId')


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read an order status message

        """
        version = read_int()
        orderId = read_int()
        message = read_str()
        filled = read_int()
        remaining = read_int()
        avg_fill_price = read_float()

        permId = 0
        if version >= 2:
            permId = read_int()

        parentId = 0
        if version >= 3:
            parentId = read_int()

        last_fill_price = 0
        if version >= 4:
            last_fill_price = read_float()

        clientId = 0
        if version >= 5:
            clientId = read_int()

        self.dispatch(orderId=orderId,
                      message=message,
                      filled=filled,
                      remaining=remaining,
                      avg_fill_price=avg_fill_price,
                      permId=permId,
                      parentId=parentId,
                      last_fill_price=last_fill_price,
                      clientId=clientId)


class Portfolio(SocketReader):
    """ Portfolio() -> reads portfolio update messages 

    Generated detail instance:

    msg.contract - description of the contract
    msg.position - indicates the position on the contract
    msg.market_price - unit price of the instrument
    msg.market_value - total market value of the instrument
    """
    class detail(Message):
        __slots__ = ('contract', 'position', 'market_price', 'market_value', 
                     'average_cost', 'unrealized_pnl', 'realized_pnl',
                     'account_name', )


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read a portfolio update message

        """
        contract = ib.types.Contract()

        version = read_int()
        contract.symbol = read_str()
        contract.secType = read_str()
        contract.expiry = read_str()
        contract.strike = read_float()
        contract.right = read_str()
        contract.currency = read_str()

        if version >= 2:
            contract.localSymbol = read_str()
            
        position = read_int()
        market_price = read_float()
        market_value = read_float()

        average_cost = unrealized_pnl = realized_pnl = 0.0
        if version >= 3:
            average_cost = read_float()
            unrealized_pnl = read_float()
            realized_pnl = read_float()

        account_name = ''
        if version >= 4:
            account_name = read_str()

        self.dispatch(contract=contract,
                      position=position,
                      market_price=market_price,
                      market_value=market_value,
                      average_cost=average_cost,
                      unrealized_pnl=unrealized_pnl,
                      realized_pnl=realized_pnl,
                      account_name=account_name)


class ReaderStart(SocketReader):
    """ ReaderStart() -> pseudo message for reader start notification

    Instances do not have a 'read' method, but messages are sent with with
    the 'send' method just the same.  The message layout is:

    msg - unadorned
    """
    class detail(Message):
        __slots__ = ()


class ReaderStop(SocketReader):
    """ ReaderStart() -> pseudo message for reader stop notification

    Instances do not have a 'read' method, but messages are sent with with
    the 'send' method just the same.  The message layout is:

    msg.exception - string of the exception that stopped the reader
    """
    class detail(Message):
        __slots__ = ('exception', )


class Ticker(SocketReader):
    """ Ticker() -> parent type for ticker-related readers

    Using a parent class enables the client to specify a single listener 
    for multiple but related readers.
    """
    class detail(Message):
        """ Message type tweaked for ticker updates

        Ticker updates are the most frequent message sent by TWS.  This type
        is slightly faster than the Message base class.
        """
        __slots__ = ('ticker_id', 'field', 'value', 'can_auto_exec', )

        def __init__(self, ticker_id, field, value, can_auto_exec=0):
            self.ticker_id = ticker_id
            self.field = field
            self.value = value
            self.can_auto_exec = can_auto_exec


class TickerPrice(Ticker):
    """ TickerPrice() -> reads ticker price messages

    Generated detail instance:

    msg.ticker_id - ticker id previously specified
    msg.field - type of price (ask, bid, last, etc)
    msg.value - price of indicated field
    msg.can_auto_exec - some type of flag
    """
    sizer = None
    
    def read(self, read_int, read_float, read_str):
        """ read(...) -> read a ticker price message

        """
        version = read_int()
        ticker_id = read_int()
        price_type = read_int()
        price = read_float()

        size = 0
        if version >= 2:
            size = read_int()

        can_auto_exec = 0
        if version >= 3:
            can_auto_exec = read_int()

        self.dispatch(ticker_id=ticker_id,
                      field=price_type,
                      value=price,
                      can_auto_exec=can_auto_exec)

        return
        version = read_int()
        ticker_id = read_int()    
        price_type = read_int()
        price = read_float()
        
        if version >= 2:
            size_tick_type = None
            types = ib.types

            ## this is better expressed as a dictionary lookup,
            ## but for now i'm more interested in tracking this
            ## as close as possible to ib code

            ticktype = types.Tick
            if price_type == ticktype.BID_PRICE:
                size_tick_type = ticktype.BID_SIZE
            elif price_type == ticktype.ASK_PRICE:
                size_tick_type = ticktype.ASK_SIZE
            elif price_type == ticktype.LAST_PRICE:
                size_tick_type = ticktype.LAST_SIZE

            if size_tick_type is not None:
                self.sizer.dispatch(ticker_id=ticker_id,
                                    field=size_tick_type,
                                    value=size)


class TickerSize(Ticker):
    """ TickerSize() -> reads ticker size messages

    Generated detail instance:

    msg.ticker_id - ticker id previously specified
    msg.field - type of size (ask, bid, last, etc)
    msg.value - size of indicated field
    """
    def read(self, read_int, read_float, read_str):
        """ read(...) -> read a ticker size message

        """
        version = read_int()
        ticker_id = read_int()
        size_type = read_int()
        size = read_int()

        self.dispatch(ticker_id=ticker_id,
                      field=size_type,
                      value=size)


class NewsBulletin(SocketReader):
    """ NewsBulletin() -> reads news bulletin messages

    """
    class detail(Message):
        __slots__ = ('news_id', 'news_type', 'news_message', 'news_exchange')


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read a news bulletin message

        """
        version = read_int()
        news_id = read_int()
        news_type = read_int()
        news_message = read_str()
        news_exchange = read_str()

        self.dispatch(news_id=news_id,
                      news_type=news_type,
                      news_message=news_message,
                      news_exchange=news_exchange)


class ReceiveFa(SocketReader):
    """ ReceiveFa() -> reads some type of message

    """
    class detail(Message):
        __slots__ = ('data_type', 'xml', )


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read a type of message

        """
        version = read_int()
        data_type = read_int()
        xml = read_str()
        
        self.dispatch(data_type=data_type,
                      xml=xml)


class HistoricalData(SocketReader):
    """ HistoricalData() -> reads some type of message

    """
    class detail(Message):
        __slots__ = ('version', 'ticker_id', 'rows' )


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read a type of message

        """
        version = read_int()
        ticker_id = read_int()
        nitems = read_int()
        rows = []
        for i in range(nitems):
            #read date,open,high,low,close,volume,wap,hasgaps
            row=[read_str(), read_float(), read_float(), read_float(), read_float(),
                 read_int(), read_float(), read_str().lower()=='true']
            rows.append(row)
        self.dispatch(version=version, ticker_id=ticker_id, rows=rows)


class BondContractData(SocketReader):
    """ BondContractData() -> reads some type of message

    """
    class detail(Message):
        __slots__ = ('details', )


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read a type of message

        """
        details = ib.types.ContractDetails()
        readBoolFromInt = read_int
        readDouble = read_float
        readstr = read_str

        version = read_int()
        details.summary.symbol = readStr()
        details.summary.secType = readStr()
        details.summary.cusip = readStr()
        details.summary.coupon = readDouble()
        details.summary.maturity = readStr()
        details.summary.issueDate  = readStr()
        details.summary.ratings = readStr()
        details.summary.bondType = readStr()
        details.summary.couponType = readStr()
        details.summary.convertible = readBoolFromInt()
        details.summary.callable = readBoolFromInt()
        details.summary.putable = readBoolFromInt()
        details.summary.descAppend = readStr()
        details.summary.exchange = readStr()
        details.summary.currency = readStr()
        details.marketName = readStr()
        details.tradingClass = readStr()
        details.conId = readInt()
        details.minTick = readDouble()
        details.orderTypes = readStr()
        details.validExchanges = readStr()
        self.dispatch(details=details)


class ScannerParameters(SocketReader):
    """ ScannerParameters() -> reads some type of message

    """
    class detail(Message):
        __slots__ = ('xml', )


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read a type of message

        """
        version = read_int()
        xml = read_str()
        self.dispatch(xml=xml)


class ScannerData(SocketReader):
    """ ReceiveFa() -> reads some type of message

    """
    class detail(Message):
        __slots__ = ('ticker_id', 'rows', )


    def read(self, read_int, read_float, read_str):
        """ read(...) -> read a type of message

        """
        version = read_int()
        ticker_id = read_int()
        nelements = read_int()
        rows = []

        for i in range(nelements):
            rank = read_int()
            contract = ib.types.ContractDetails()
            contract.summary.symbol = read_str()
            contract.summary.secType = read_str()
            contract.summary.expiry = read_str()
            contract.summary.strike = read_float()
            contract.summary.right = read_str()
            contract.summary.exchange = read_str()
            contract.summary.currency = read_str()
            contract.summary.localSymbol = read_str()
            contract.marketName = read_str()
            contract.tradingClass = read_str()
            distance = read_str()
            benchmark = read_str()
            projection = read_str()
            rows.append(dict(rank=rank, contract=contract, distance=distance,
                             benchmark=benchmark, projection=projection))

        self.dispatch(ticker_id=ticker_id, rows=rows)
