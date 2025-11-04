import time
import copy

from enum import Enum
class OrderType(Enum):
    LIMIT = 1
    MARKET = 2
    IOC = 3

class OrderSide(Enum):
    BUY = 1
    SELL = 2


class NonPositiveQuantity(Exception):
    pass

class NonPositivePrice(Exception):
    pass

class InvalidSide(Exception):
    pass

class UndefinedOrderType(Exception):
    pass

class UndefinedOrderSide(Exception):
    pass

class NewQuantityNotSmaller(Exception):
    pass

class UndefinedTraderAction(Exception):
    pass

class UndefinedResponse(Exception):
    pass


from abc import ABC


class Order(ABC):
    """
    Abstract base class for all order types.

    An order represents a request to buy or sell a financial instrument.
    This base class contains the common attributes shared by all order types.

    Attributes:
        id (int): Unique identifier for the order
        symbol (str): Trading symbol/ticker for the instrument
        quantity (int/float): Number of units to trade (must be positive)
        side (OrderSide): BUY or SELL
        time (float): Timestamp when the order was created

    Raises:
        NonPositiveQuantity: If quantity is not positive
        InvalidSide: If side is not BUY or SELL
    """
    def __init__(self, id, symbol, quantity, side, time):
        self.id = id
        self.symbol = symbol
        if quantity > 0:
            self.quantity = quantity
        else:
            raise NonPositiveQuantity("Quantity Must Be Positive!")
        if side in [OrderSide.BUY, OrderSide.SELL]:
            self.side = side
        else:
            raise InvalidSide("Side Must Be Either \"Buy\" or \"OrderSide.SELL\"!")
        self.time = time


class LimitOrder(Order):
    """
    Limit order - executes at specified price or better.

    A limit order will only execute at the limit price or better (lower for buy,
    higher for sell). If not immediately matched, it rests in the order book
    until filled, cancelled, or expires.

    Attributes:
        price (float): The limit price at which the order should execute
        type (OrderType): Set to OrderType.LIMIT

    Raises:
        NonPositivePrice: If price is not positive
    """
    def __init__(self, id, symbol, quantity, price, side, time):
        super().__init__(id, symbol, quantity, side, time)
        if price > 0:
            self.price = price
        else:
            raise NonPositivePrice("Price Must Be Positive!")
        self.type = OrderType.LIMIT


class MarketOrder(Order):
    """
    Market order - executes immediately at best available price.

    A market order will execute immediately at the best available price in the
    order book. It does not specify a price, prioritizing speed of execution
    over price certainty.

    Attributes:
        type (OrderType): Set to OrderType.MARKET
    """
    def __init__(self, id, symbol, quantity, side, time):
        super().__init__(id, symbol, quantity, side, time)
        self.type = OrderType.MARKET


class IOCOrder(Order):
    """
    Immediate-or-Cancel (IOC) order - executes immediately or cancels.

    An IOC order attempts to execute immediately at the specified price or better.
    Any portion of the order that cannot be filled immediately is cancelled rather
    than being added to the order book.

    Attributes:
        price (float): The limit price for execution
        type (OrderType): Set to OrderType.IOC

    Raises:
        NonPositivePrice: If price is not positive
    """
    def __init__(self, id, symbol, quantity, price, side, time):
        super().__init__(id, symbol, quantity, side, time)
        if price > 0:
            self.price = price
        else:
            raise NonPositivePrice("Price Must Be Positive!")
        self.type = OrderType.IOC


class FilledOrder(Order):
    """
    Represents a completed/executed order.

    This class stores information about orders that have been successfully matched
    and executed in the market.

    Attributes:
        price (float): The execution price
        limit (bool): Whether this was originally a limit order
    """
    def __init__(self, id, symbol, quantity, price, side, time, limit = False):
        super().__init__(id, symbol, quantity, side, time)
        self.price = price
        self.limit = limit
        


class MatchingEngine():
    """
    Order matching engine implementing price-time priority algorithm.

    The MatchingEngine maintains two order books (bid and ask) and matches
    incoming orders against resting orders using price-time priority:
    - Best prices get priority (highest bid, lowest ask)
    - Among same prices, earlier orders execute first

    Attributes:
        bid_book (list): List of buy orders, sorted by (-price, time)
        ask_book (list): List of sell orders, sorted by (price, -time)

    Example:
        >>> engine = MatchingEngine()
        >>> order = LimitOrder(1, "AAPL", 100, 150.50, OrderSide.BUY, time.time())
        >>> filled = engine.handle_order(order)
    """
    def __init__(self):
        # These are the order books you are given and expected to use for matching the orders below
        self.bid_book = []
        self.ask_book = []

    def handle_order(self, order):
        """
        Route an order to the appropriate handler based on its type.

        Args:
            order (Order): The order object to process

        Raises:
            UndefinedOrderType: If order type is not recognized

        Returns:
            None for limit orders, list of FilledOrders for market/IOC orders
        """
        # Route order to appropriate handler based on order type
        if order.type == OrderType.LIMIT:
            self.handle_limit_order(order)
        elif order.type == OrderType.IOC:
            self.handle_ioc_order(order)
        elif order.type == OrderType.MARKET:
            self.handle_market_order(order)
        else:
            # Raise error if the type of order is ambiguous or undefined
            raise UndefinedOrderType("Undefined Order Type!")


    def handle_limit_order(self, order):
        """
        Process a limit order - match against opposite book, post remainder.

        Limit orders are matched against the opposite book at their limit price
        or better. Any unfilled quantity is added to the appropriate order book.

        Args:
            order (LimitOrder): The limit order to process

        Returns:
            list: List of FilledOrder objects representing executed trades

        Raises:
            UndefinedOrderSide: If order side is None or invalid
        """
        filled_orders = []
        # The orders that are filled from the market order need to be inserted into the above list

        if order.side == None:
            raise UndefinedOrderSide("Undefined Order Side!")            
            
        #Need to check if cross first 
        if order.side == OrderSide.BUY:
            temp_list = []
            while self.ask_book:
                
                book =self.ask_book.pop(0)
                
                # Order for a differnt stock goes back in the book
                if (book.symbol != order.symbol) or order.quantity == 0:
                    #print("1. Adding ID to temp_list -> ", book.id, book.quantity)
                    temp_list.append(book)
    
                # Correct stock and order price less/equal to price in book 
                elif (book.symbol == order.symbol) and (order.price <= book.price):
                    
                    #DEBUG
                    #print("Limit Buy: ID {}, Price {}, Quantity {} -> Matched Bid ID {}, Price {}, Quantity {}".format(order.id,order.price,order.quantity,book.id, book.price, book.quantity))
                    
                    # Order Quantity > Book Quantity 
                    if order.quantity > book.quantity:
                        # Partially fill order
                        order.quantity = order.quantity - book.quantity
                        # Book entry sent to filled
                        filled_orders.append(book) 
                        book.quantity = 0
                        #print("Filled Book ID: ", book.id, " | Order ID: ", order.id, " has quantity remaining of ", order.quantity)
                    
                    # Book Quantity > Order Quantity 
                    elif book.quantity > order.quantity:   
                        
                        book.quantity = (book.quantity-order.quantity)
                        mod_book_order = copy.deepcopy(book)
                       
                        #print("Book ID {} has quantity remaining of {}".format(mod_book_order.id, mod_book_order.quantity))
                        #print("B. Adding ID to temp_list -> ", mod_book_order.id, mod_book_order.quantity)
                        temp_list.append(mod_book_order)
                        
                        # Book partially filled
                        book.quantity = order.quantity
                                                
                        # Fill the order
                        filled_orders.append(order)
                        filled_orders.append(book)             
                        order.quantity = 0 
                    
                    # Order Quantity == Book Quantity                  
                    else: 
                        filled_orders.append(book) 
                        filled_orders.append(order)
                        order.quantity = 0
                        book.quantity = 0
                        
                else:
                    #print("3. Adding ID to temp_list -> ", book.id, book.quantity)
                    temp_list.append(book)    
                        
            #Send uncrossed orders back into book 
            self.ask_book = temp_list.copy() 
            
            # Any quantity not crossed inserted into book 
            if order.quantity > 0:
                self.insert_limit_order(order)
            
        if order.side == OrderSide.SELL:
            temp_list = []
            while self.bid_book:
                
                book = self.bid_book.pop(0)
                
                # Order for a differnt stock goes back in the book
                if (book.symbol != order.symbol) or order.quantity == 0:
                    #print("A. Adding ID to temp_list -> ", book.id, book.quantity)
                    temp_list.append(book)
    
                # Correct stock and order price less/equal to price in book 
                elif (book.symbol == order.symbol) and (order.price <= book.price):
                    #print("Looking at Book ID: ", book.id, ", Quantity: ", book.quantity, " | Order: ", order.id, ", Amount: ", order.quantity)
                    #DEBUG
                    #print("Limit Sell: ID {}, Price {}, Quantity {} -> Matched Bid ID {}, Price {}, Quantity {}".format(order.id,order.price,order.quantity,book.id, book.price, book.quantity))
                    
                    # Order Quantity > Book Quantity 
                    if order.quantity > book.quantity:
                        # Partially fill order
                        order.quantity = order.quantity - book.quantity
                        # Book entry sent to filled
                        filled_orders.append(book) 
                        book.quantity = 0
                        #print("Filled Book ID: ", book.id, " | Order ID: ", order.id, " has quantity remaining of ", order.quantity)
                    
                    # Book Quantity > Order Quantity 
                    elif book.quantity > order.quantity:   
                        
                        book.quantity = (book.quantity-order.quantity)
                        mod_book_order = copy.deepcopy(book)
                       
                        #print("Book ID {} has quantity remaining of {}".format(mod_book_order.id, mod_book_order.quantity))
                        #print("B. Adding ID to temp_list -> ", mod_book_order.id, mod_book_order.quantity)
                        temp_list.append(mod_book_order)
                        
                        # Book partially filled
                        book.quantity = order.quantity
                                                
                        # Fill the order
                        filled_orders.append(order)
                        filled_orders.append(book)             
                        order.quantity = 0 
                    
                    # Order Quantity == Book Quantity                  
                    else: 
                        filled_orders.append(book) 
                        filled_orders.append(order)
                        order.quantity = 0
                        book.quantity = 0
                        
                else:
                    #print("C. Adding ID to temp_list -> ", book.id, book.quantity)
                    temp_list.append(book)
            
            #print("Temp Book[0] ID | Quantity: {} | {} ".format(temp_list[0].id,temp_list[0].quantity))
                    
            #Send uncrossed orders back into book 
            self.bid_book = temp_list.copy() 
            
            # Any quantity not crossed inserted into book 
            if order.quantity > 0:
                self.insert_limit_order(order)
                
        # DEBUG
        """
        if len(filled_orders) == 3:
            
            print("Filled Order IDs -> ", end="")
            for order in filled_orders:
                print("ID: ", order.id,"Price: ", order.price, "Time: ", order.time," || ", end=" ")
            print(" ")
            
            print("Bid Book[0] ID: ", self.bid_book[0].id, " Quantity: ", self.bid_book[0].quantity, " Time: " ,self.bid_book[0].time)
        """
        return filled_orders

    def handle_market_order(self, order):
        """
        Process a market order - execute immediately at best available prices.

        Market orders consume liquidity from the order book, executing against
        the best available prices until fully filled or the book is exhausted.

        Args:
            order (MarketOrder): The market order to process

        Returns:
            list: List of FilledOrder objects representing executed trades

        Raises:
            UndefinedOrderSide: If order side is None or invalid
        """
        filled_orders = []

        if order.side == None:
            # You need to raise the following error if the side the order is for is ambiguous
            raise UndefinedOrderSide("Undefined Order Side!")            
            
        #Need to check if cross first 
        if order.side == OrderSide.BUY:
            temp_list = []
            
            while self.ask_book:
                
                book =self.ask_book.pop(0)
                
                # Order for a differnt stock goes back in the book
                if (book.symbol != order.symbol) or order.quantity == 0:
                    temp_list.append(book)
    
                # Correct stock and order price less/equal to price in book 
                elif (book.symbol == order.symbol):

                    # Order Quantity > Book Quantity 
                    if order.quantity > book.quantity:
                        # Partially fill order
                        order.quantity = order.quantity - book.quantity
                        # Book entry sent to filled
                        filled_orders.append(book) 
                        book.quantity = 0
                    
                    # Book Quantity > Order Quantity 
                    elif book.quantity > order.quantity:   
                        book.quantity = (book.quantity-order.quantity)
                        mod_book_order = copy.deepcopy(book)
                        temp_list.append(mod_book_order)
                        
                        # Book partially filled
                        book.quantity = order.quantity
                        order.price = book.price                        
                        # Fill the order
                        filled_orders.append(order)
                        filled_orders.append(book)             
                        order.quantity = 0 
                    
                    # Order Quantity == Book Quantity                  
                    else: 
                        filled_orders.append(book) 
                        filled_orders.append(order)
                        order.quantity = 0
                        book.quantity = 0
                        
                else:
                    temp_list.append(book)    
                                    
            # Any quantity not crossed inserted into book
            if order.quantity > 0:
                temp_list.append(order)

            #Send uncrossed orders back into book
            self.ask_book = temp_list.copy()
            # Sort ask book by price (lowest first), then time (earliest first)
            self.ask_book = sorted(self.ask_book, key=lambda x: (x.price, x.time))
            
        if order.side == OrderSide.SELL:
            temp_list = []
            while self.bid_book:
                
                book = self.bid_book.pop(0)
                
                # Order for a differnt stock goes back in the book
                if (book.symbol != order.symbol) or order.quantity == 0:
                    temp_list.append(book)
    
                # Correct stock and order price less/equal to price in book 
                elif (book.symbol == order.symbol):
                    #DEBUG
                    # Order Quantity > Book Quantity 
                    if order.quantity > book.quantity:
                        # Partially fill order
                        order.quantity = order.quantity - book.quantity
                        # Book entry sent to filled
                        filled_orders.append(book) 
                        book.quantity = 0
                    
                    # Book Quantity > Order Quantity 
                    elif book.quantity > order.quantity:   
                        book.quantity = (book.quantity-order.quantity)
                        mod_book_order = copy.deepcopy(book)
                        temp_list.append(mod_book_order)
                        
                        # Book partially filled
                        book.quantity = order.quantity
                        order.price = book.price                        
                        # Fill the order
                        filled_orders.append(order)
                        filled_orders.append(book)             
                        order.quantity = 0 
                    
                    # Order Quantity == Book Quantity                  
                    else: 
                        filled_orders.append(book) 
                        filled_orders.append(order)
                        order.quantity = 0
                        book.quantity = 0
                        
                else:
                    temp_list.append(book)

            # Any quantity not crossed inserted into book 
            if order.quantity > 0:
                temp_list.append(order)
 
            #Send uncrossed orders back into book 
            self.bid_book = temp_list.copy() 
            self.bid_book = sorted(self.bid_book, key=lambda x: (x.price, x.time))
            #print("The Bid Book[0]: ", self.bid_book[0].quantity, self.bid_book[0].id, "Filled Orders [0]: ID -> ", filled_orders[0].id)
          
        # The filled orders are expected to be the return variable (list)
        return filled_orders

    def handle_ioc_order(self, order):
        """
        Process an Immediate-or-Cancel (IOC) order.

        IOC orders attempt immediate execution at the limit price or better.
        Any unfilled quantity is cancelled rather than posted to the book.

        Args:
            order (IOCOrder): The IOC order to process

        Returns:
            list: List of FilledOrder objects representing executed trades

        Raises:
            UndefinedOrderSide: If order side is None or invalid
        """
        filled_orders = []

        if order.side == None:
            # You need to raise the following error if the side the order is for is ambiguous
            raise UndefinedOrderSide("Undefined Order Side!")            
            
        #Need to check if cross first 
        if order.side == OrderSide.BUY:
            temp_list = []
            
            while self.ask_book:
                
                book =self.ask_book.pop(0)
                
                # Order for a differnt stock goes back in the book
                if (book.symbol != order.symbol) or order.quantity == 0:
                    temp_list.append(book)
    
                # Correct stock and order price less/equal to price in book 
                elif (book.symbol == order.symbol) and (order.price <= book.price):

                    # Order Quantity > Book Quantity 
                    if order.quantity > book.quantity:
                        # Partially fill order
                        order.quantity = order.quantity - book.quantity
                        # Book entry sent to filled
                        filled_orders.append(book) 
                        book.quantity = 0
                    
                    # Book Quantity > Order Quantity 
                    elif book.quantity > order.quantity:   
                        book.quantity = (book.quantity-order.quantity)
                        mod_book_order = copy.deepcopy(book)
                        temp_list.append(mod_book_order)
                        
                        # Book partially filled
                        book.quantity = order.quantity
                        order.price = book.price                        
                        # Fill the order
                        filled_orders.append(order)
                        filled_orders.append(book)             
                        order.quantity = 0 
                    
                    # Order Quantity == Book Quantity                  
                    else: 
                        filled_orders.append(book) 
                        filled_orders.append(order)
                        order.quantity = 0
                        book.quantity = 0
                else:
                    temp_list.append(book)

            #Send uncrossed orders back into book
            self.ask_book = temp_list.copy()
            # Sort ask book by price (lowest first), then time (earliest first)
            self.ask_book = sorted(self.ask_book, key=lambda x: (x.price, x.time))
            
        if order.side == OrderSide.SELL:
            temp_list = []
            while self.bid_book:
                
                book = self.bid_book.pop(0)
                
                # Order for a differnt stock goes back in the book
                if (book.symbol != order.symbol) or order.quantity == 0:
                    temp_list.append(book)
    
                # Correct stock and order price less/equal to price in book 
                elif (book.symbol == order.symbol) and (order.price <= book.price):
                    #DEBUG
                    # Order Quantity > Book Quantity 
                    if order.quantity > book.quantity:
                        # Partially fill order
                        order.quantity = order.quantity - book.quantity
                        # Book entry sent to filled
                        filled_orders.append(book) 
                        book.quantity = 0
                    
                    # Book Quantity > Order Quantity 
                    elif book.quantity > order.quantity:   
                        book.quantity = (book.quantity-order.quantity)
                        mod_book_order = copy.deepcopy(book)
                        temp_list.append(mod_book_order)
                        
                        # Book partially filled
                        book.quantity = order.quantity
                        order.price = book.price                        
                        # Fill the order
                        filled_orders.append(order)
                        filled_orders.append(book)             
                        order.quantity = 0 
                    
                    # Order Quantity == Book Quantity                  
                    else: 
                        filled_orders.append(book) 
                        filled_orders.append(order)
                        order.quantity = 0
                        book.quantity = 0
                        
                else:
                    temp_list.append(book)

 
            #Send uncrossed orders back into book 
            self.bid_book = temp_list.copy() 
            self.bid_book = sorted(self.bid_book, key=lambda x: (x.price, x.time))
            #print("The Bid Book[0]: ", self.bid_book[0].quantity, self.bid_book[0].id, "Filled Orders [0]: ID -> ", filled_orders[0].id)
            
        # The filled orders are expected to be the return variable (list)
        return filled_orders


    def insert_limit_order(self, order):
        """
        Insert a limit order into the appropriate order book.

        Orders are inserted into bid or ask book and sorted by price-time priority:
        - Bid book: Sorted by highest price first, then earliest time
        - Ask book: Sorted by lowest price first, then latest time

        Args:
            order (LimitOrder): The limit order to insert

        Raises:
            AssertionError: If order type is not LIMIT
            UndefinedOrderSide: If order side is invalid
        """
        assert order.type == OrderType.LIMIT

        if order.side == OrderSide.BUY:

            if not self.bid_book:
                self.bid_book.append(order)                
            else:
                self.bid_book.append(order)
   
        elif order.side == OrderSide.SELL:
            
            if not self.ask_book:
                self.ask_book.append(order)
                
            else:
                self.ask_book.append(order)
        else:
            raise UndefinedOrderSide("Undefined Order Side!")

        self.bid_book = sorted(self.bid_book, key=lambda x: (-x.price, x.time))
        self.ask_book = sorted(self.ask_book, key=lambda x: (x.price, -x.time))
        #self.bid_book.sort(key=lambda x: x.price, reverse=True)
        #self.ask_book.sort(key=lambda x: x.price)
        """
        if order.side == OrderSide.SELL:
            print("BID BOOK AFTER SELL ORDER: ", end="")
            for order in self.bid_book:
                print(order.id, " ", end="")
        """
    def amend_quantity(self, id, quantity):
        """
        Amend the quantity of an existing order in the book.

        Only allows quantity reductions (not increases) to maintain fairness
        in the order queue. Searches both bid and ask books for the order ID.

        Args:
            id: The unique identifier of the order to amend
            quantity (int/float): The new quantity (must be less than current)

        Raises:
            NewQuantityNotSmaller: If new quantity is greater than existing quantity

        Returns:
            bool: True if amendment successful, False if order not found
        """
        # Remember that there are two order books, one on the bid side and one on the ask side
        found_order = False
        for index, bid in enumerate(self.bid_book):
            if bid.id == id:
                found_order = True
                if quantity > bid.quantity:
                    # You need to raise the following error if the user attempts to modify an order
                    # with a quantity that's greater than given in the existing order
                    raise NewQuantityNotSmaller("Amendment Must Reduce Quantity!")
                    return False
                else:
                    #print("Amending Order ID {} at Index {}: {} to {}".format(id, index,  bid.quantity, quantity))
                    self.bid_book[index].quantity = quantity

        if not found_order:
            for ask in self.ask_book:
                if ask.id == id:
                    if quantity > ask.quantity:
                        # You need to raise the following error if the user attempts to modify an order
                        # with a quantity that's greater than given in the existing order
                        raise NewQuantityNotSmaller("Amendment Must Reduce Quantity!")
                        return False
                    else:
                        ask['quantity'] = quantity
                        self.ask_book[id] = ask
        
        #print("Order quanty:", self.bid_book[0].quantity)
        
    def cancel_order(self, id):
        """
        Cancel an order by removing it from the appropriate order book.

        Args:
            id: The unique identifier of the order to cancel

        Returns:
            bool: True if order was found and cancelled, False otherwise
        """
        # Search for order in bid book
        for index, order in enumerate(self.bid_book):
            if order.id == id:
                del self.bid_book[index]
                return True

        # If not found in bid book, search ask book
        for index, order in enumerate(self.ask_book):
            if order.id == id:
                del self.ask_book[index]
                return True

        # Order not found in either book
        return False
