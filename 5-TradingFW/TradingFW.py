
import os
import csv
import matplotlib.pyplot as plt



import ctypes

class TradingFW(object):
    def __init__(self):
        super(TradingFW).__init__()

        self.c_lib = None
        self._init_cpp_code()
        self.header = []

    def _init_cpp_code(self):
        dll = os.path.join(os.path.dirname(os.path.realpath(__file__)),"cbinding","TradingFW.dll")
        self.c_lib = ctypes.CDLL(dll)
        self.c_lib.NewTradingFW.restype = ctypes.c_void_p
        self.c_lib.get_value.restype = ctypes.c_char_p
        self.c_lib.get_value.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
        self.c_lib.get_csv_name.restype = ctypes.c_char_p
        self.c_lib.get_csv_name.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.c_lib.rows.restype = ctypes.c_int
        self.c_lib.rows.argtypes = [ctypes.c_void_p]
        self.c_lib.cols.restype = ctypes.c_int
        self.c_lib.cols.argtypes = [ctypes.c_void_p]
        self.c_lib.add_value.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_char_p]
        self.c_lib.read_csv.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
        self._cpp_obj = ctypes.c_void_p(self.c_lib.NewTradingFW())

    def _csv_n_cols(self):
        self._cvs_max_column = self.c_lib.cols(self._cpp_obj)
        return self._cvs_max_column

    def _csv_n_rows(self):
        self._cvs_max_rows = self.c_lib.rows(self._cpp_obj)
        return self._cvs_max_rows

    def _get_value(self,row,col):
        if col > self._cvs_max_column:
            return None
        if row > self._cvs_max_rows:
            return None
        empty_string = ctypes.create_string_buffer(100)
        value = self.c_lib.get_value(self._cpp_obj,empty_string,row,col).decode("utf-8")
        if value == "None":
            return None

        if row == 0:
            return str(value)
        else:
            key = self.header[col]
            if key == "keySymbol":
                return str(value)
            elif key == "timestampNano":
                return int(value)
            elif key == "lastQty":
                return int(value)
            elif key.endswith("q"):
                return int(value)
            else:
                return float(value)

    def _csv_add_col(self,key,values):
        if key not in self.header:
            self.header.append(key)
            col = self.header.index(key)
            buff = self._to_c_str(key)
            self.c_lib.add_value(self._cpp_obj, 0, col, buff)
        else:
            col = self.header.index(key)

        self._cvs_max_column += 1

        for i in range(len(values)):
            buff = self._to_c_str(str(values[i]))
            self.c_lib.add_value(self._cpp_obj,i+1,col,buff)
        return

    @staticmethod
    def _to_c_str(s):
        return ctypes.create_string_buffer(s.encode("utf-8"),100)

    def _csv_keys(self):
        cols = self._csv_n_cols()
        keys = []
        for i in range(cols):
            key = self._get_value(0,i)
            keys.append(key)
        return keys

    def read_csv(self, path, max_lines=0):
        print("Reading csv...")
        self.name = os.path.basename(path).split(".")[0].upper()

        self.c_lib.read_csv(self._cpp_obj,self._to_c_str(path),max_lines)

        print("Read " + str(self._csv_n_cols()) + " columns")
        print("     " + str(self._csv_n_rows()) + " rows")
        self.header = self._csv_keys()

        # empty_string = ctypes.create_string_buffer(100)
        # header = self.c_lib.get_value(self._cpp_obj, empty_string,0,0)
        # csv_name = self.c_lib.get_csv_name(self._cpp_obj,empty_string)

        # with open(path) as csvfile:
        #     data = csv.reader(csvfile, delimiter=',')
        #     self.data = []
        #     for i, l in enumerate(data):
        #         if i == 0:
        #             keys = l[:]
        #         else:
        #             if max_lines != 0 and i > max_lines:
        #                 break
        #             v = OrderedDict()
        #             for j, key in enumerate(keys):
        #                 if key == "keySymbol":
        #                     v[key] = str(l[j])
        #                 elif key == "timestampNano":
        #                     v[key] = int(l[j])
        #                 elif key == "lastQty":
        #                     v[key] = int(l[j])
        #                 elif key.endswith("q"):
        #                     v[key] = int(l[j])
        #                 else:
        #                     v[key] = float(l[j])
        #             self.data.append(v)
        # return self.data

    def _csv_row(self,row):
        n_cols = self._csv_n_cols()
        ret_row = []
        for i in range(n_cols):
            ret_row.append(self._get_value(row,i))
        return ret_row

    def _csv_rows(self):
        n_rows = self._csv_n_rows()
        ret_rows = []
        for i in range(n_rows):
            ret_rows.append(self._csv_row(i))
        return ret_rows

    def to_csv(self, path=None):
        if path == None:
            path = self.name + ".csv"

        with open(path, 'w') as csvfile:
            if len(self._csv_n_rows()) > 0:
                keys = self._csv_keys()
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                writer.writeheader()
                for i_row in range(self._csv_n_rows()):
                    row = self._csv_row(i_row)
                    writer.writerow(row)

    def __str__(self):
        return self.describe()

    def __iter__(self):
        return iter(self.data)

    def head(self,keys):
        ret = ""
        ret += self._str_header(keys)
        for i in range(10):
            if i > 0 and i < self._csv_n_rows():
                ret += "\n" + self._str_row(i, keys)
        return ret

    def tail(self,keys=None):
        ret = ""
        ret += self._str_header(keys)
        for i in range(self._csv_n_rows()-10,self._csv_n_rows()):
            if i > 0 and i < self._csv_n_rows():
                ret += "\n" + self._str_row(i,keys)
        return ret

    def _str_header(self,keys=None):
        ret = ""
        if self._csv_n_rows() > 0:
            header = self.header[:]

            if keys != None:
                header = [h for h in header if h in keys]

            if "timestampNano" in header:
                ret += " " * 4

            ret += " ".join(["{:<8}".format(h) for h in header])
        return ret

    def _str_row(self,index,keys=None):
        ret = ""
        if self._csv_n_rows() > 0:
            header_keys = self.header[:]

            if keys != None:
                header_keys = [h for h in header_keys if h in keys]

            row = self._csv_row(index)
            values = []
            for key in header_keys:
                col = self.header.index(key)
                values.append(str(row[col]))
                values = ["{:<8}".format(v) for v in values]
            ret = " ".join(values)
        return ret

    def add(self, key, value):
        #print("adding "+key+"...")
        if isinstance(value,list):
            self._csv_add_col(key,value)
        else:
            all_values = []
            for i in range(1,self._csv_n_rows()):
                row = self._csv_row(i)
                all_values.append(value(row))
            self._csv_add_col(key, all_values)

    # def filter(self, filter_lambda):
    #     print("filtering...")
    #     tf = TradingFW()
    #     ret = []
    #     rows = self._csv_rows()[1:]
    #     ret.append(rows[0])
    #     for row in rows[1:]:
    #         if filter_lambda(row):
    #             ret.append(row)
    #     tf.data = ret
    #     return tf

    def describe(self,keys=None):
        ret = self._str_header(keys)
        for i in range(10):
            if i > 0 and i < self._csv_n_rows():
                ret += "\n" + self._str_row(i, keys)

        ret += "\n..."
        for i in range(self._csv_n_rows() - 10, self._csv_n_rows()):
            if i > 0 and i < self._csv_n_rows():
                ret += "\n" + self._str_row(i, keys)
        return ret

    def show(self):
        plt.show()

    # def daily_close(self):
    #     return self.data[['Adj Close']]

    # def returns(self):
    #     dc = self.daily_close()
    #     return np.log(dc / dc.shift(1))

    # def pct_change_pandas(self):
    #     daily_pct_change = self.daily_close().pct_change()
    #     daily_pct_change.fillna(0, inplace=True)
    #     return daily_pct_change

    # def pct_change(self):
    #     daily_close = self.daily_close()
    #     daily_pct_change = np.log(daily_close / daily_close.shift(1))
    #     return daily_pct_change
    #
    # def daily_log_returns(self):
    #     return np.log(self.daily_close().pct_change() + 1)
    #
    # def cumulative_daily_return(self):
    #     return (1 + self.pct_change()).cumprod()

    # # Ordinary Least-Squares Regression
    # def OLS(self, cmp_data):
    #
    #     # Calculate the returns
    #     returns0 = self.returns()
    #     returns1 = cmp_data.returns()
    #
    #     # Build up a new DataFrame with AAPL and MSFT returns
    #     returns_data = pandas.concat([returns0, returns1], axis=1)[1:]
    #     returns_data.columns = [self.name, cmp_data.name]
    #
    #     # Add a constant
    #     X = sm.add_constant(returns_data[self.name])
    #
    #     # Construct the model
    #     model = sm.OLS(returns_data[cmp_data.name], X).fit()
    #
    #     # Print the summary
    #     print(model.summary())
    #
    #     return model

    def diff(self,key):
        ret = []
        ret.append(None)
        col = self.header.index(key)
        for i in range(2, self._csv_n_rows()):
            val1 = self._get_value(i,col)
            val2 = self._get_value(i-1,col)
            if val1 != None and val2 != None:
                v = val1 - val2
            else:
                v = None
            ret.append(v)

        return ret

    def window(self,window,key):
        ret = []
        ret.append(None)
        col_key = self.header.index(key)

        rows = self._csv_rows()[1:]
        for i in range(1,self._csv_n_rows()-1):
            window_data = rows[max(i-window,0):i]

            if len(window_data) > 0:
                _data = float(sum([d[col_key] for d in window_data]))/len(window_data)
                ret.append(_data)
            else:
                ret.append(None)

        return ret


    # Simple Moving Average
    def SMA_signals(self, short_window=100, long_window=1000):
        # SMA
        self.prediction = "SMA"

        def low_ask(v):
            m = None
            for i in range(1,6):
                col = self.header.index("ask"+str(i)+"q")
                if v[col] > 0:
                    col2 = self.header.index("ask"+str(i)+"p")
                    if m == None:
                        m = v[col2]
                    else:
                        m = min(m,v[col2])
            return m
        def max_bid(v):
            m = None
            for i in range(1,6):
                col = self.header.index("bid"+str(i)+"q")
                if v[col] > 0:
                    col2 = self.header.index("bid"+str(i)+"p")
                    if m == None:
                        m = v[col2]
                    else:
                        m = max(m,v[col2])
            return m

        print("Calculate best bid/ask")
        self.add("best_bid",low_ask)
        self.add("best_ask",max_bid)

        print("Calculate moving windows")
        short_ma_ask = self.window(window=short_window,key="best_ask")
        long_ma_ask = self.window(window=long_window,key="best_ask")
        # short_ma_bid = self.get("best_bid").rolling(window=short_window)
        # long_ma_bid = self.get("best_bid").rolling(window=long_window)

        self.add("short_ma_ask", short_ma_ask)
        self.add("long_ma_ask", long_ma_ask)

        signals = []
        for i in range(self._csv_n_rows()-1):
            signal = None

            # buy
            if short_ma_ask[i] != None and long_ma_ask[i] != None:
                if short_ma_ask[i] > long_ma_ask[i]:
                    signal = 1
                elif short_ma_ask[i] <= long_ma_ask[i]:
                    signal = 0
            # # sell
            # if short_ma_bid[i] != None and long_ma_bid[i] != None:
            #     if short_ma_bid[i]["best_bid"] > long_ma_bid[i]["best_bid"]:
            #         signal = 0

            signals.append(signal)


        self.add("signal",signals)
        positions = self.diff(key='signal')
        self.add("positions", positions)

        return self

    def plot_SMA(self):
        # plot
        fig = plt.figure()
        fig.add_subplot(111, ylabel='Price')

        if self.prediction == "SMA":

            rows = self._csv_rows()[1:]
            col_best_ask = self.header.index("best_ask")
            col_long_ma_ask = self.header.index("long_ma_ask")
            col_short_ma_ask = self.header.index("short_ma_ask")
            col_nano = self.header.index('timestampNano')
            col_positions = self.header.index('positions')

            # Selling price:
            x1 = [p[col_nano] for p in rows if p[col_best_ask] != None]
            y1 = [p[col_best_ask] for p in rows if p[col_best_ask] != None]
            plt.plot(x1,y1, color='r', lw=2.)

            # Moving Averages
            x2 = [p[col_nano] for p in rows if p[col_long_ma_ask] != None]
            y2 = [p[col_long_ma_ask] for p in rows if p[col_long_ma_ask] != None]
            plt.plot(x2, y2, lw=2.)

            x3 = [p[col_nano] for p in rows if p[col_short_ma_ask] != None]
            y3 = [p[col_short_ma_ask] for p in rows if p[col_short_ma_ask] != None]
            plt.plot(x3, y3, lw=2.)

            # Buy sell points
            x4 = [p[col_nano] for p in rows if p[col_best_ask] != None and p[col_positions] == 1]
            y4 = [p[col_best_ask] for p in rows if p[col_best_ask] != None and p[col_positions] == 1]
            plt.plot(x4, y4, '^',markersize=10, color='m')

            x5 = [p[col_nano] for p in rows if p[col_best_ask] != None and p[col_positions] == -1]
            y5 = [p[col_best_ask] for p in rows if p[col_best_ask] != None and p[col_positions] == -1]
            plt.plot(x5, y5, 'v',markersize=10, color='k')

            plt.show()

    def calculate_portfolio(self,initial_capital=100000,order_qty=100):

        cash = initial_capital
        holdings = 0
        col_positions = self.header.index('positions')
        col_best_ask = self.header.index("best_ask")
        col_best_bid = self.header.index("best_bid")

        self.results = []
        rows = self._csv_rows()[1:]
        for i, d in enumerate(rows):

            res = {}
            qty = 0
            price = 0
            if d[col_positions] != None:
                if d[col_positions] > 0:
                    price = d[col_best_ask]
                    qty = min(order_qty,int(cash/price))
                    holdings += qty
                elif d[col_positions] < 0:
                    price = d[col_best_bid]
                    qty = min(order_qty, holdings)
                    holdings -= qty

                cash -= qty * d[col_positions] * price

            res['cash'] = cash
            res['holdings'] = holdings * d[col_best_bid]
            res['total'] = cash + holdings
            if i > 0:
                prev_row = self.results[-1]
                res['returns'] = float(res['total'] - prev_row['total'])/max(res['total'],prev_row['total'])
            else:
                res['returns'] = None
            self.results.append(res)

        return

    def plot_portfolio(self):
        fig = plt.figure()

        ax1 = fig.add_subplot(111, ylabel='Portfolio')


        # Plot the equity curve in dollars
        col_nano = self.header.index('timestampNano')
        col_positions = self.header.index('positions')

        rows = self._csv_rows()[1:]

        x1 = [p[col_nano] for p in rows if p != None]
        y1 = [p["total"] for p in self.results if p != None]
        plt.plot(x1, y1, lw=2.)

        if self.prediction == "SMA":
            x4 = [p[col_nano] for p in rows if p != None and p[col_positions] == 1]
            y4 = [r["total"] for r,p in zip(self.results,rows) if p[col_positions] == 1]
            plt.plot(x4, y4, '^',markersize=10, color='m')

            x5 = [p[col_nano] for p in rows if p != None and p[col_positions] == -1]
            y5 = [r["total"] for r, p in zip(self.results, rows) if p[col_positions] == -1]
            plt.plot(x5, y5, 'v',markersize=10, color='k')

        # Show the plot
        plt.show()
