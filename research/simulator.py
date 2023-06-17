import pandas as pd

class Simulator:
    def __init__(self, m_cash_flow, price_history):
        self.m_cash_flow = m_cash_flow
        self.price_history = price_history

    def compute_return(self, df: pd.DataFrame) -> dict:
        """
        """
        beginning_acc_balance = self.m_cash_flow
        final_acc_balance = (sum(df['num_shares_bought']) * df.iloc[len(df)-1]['Close']) + df.iloc[len(df)-1]['cash_to_invest']
        num_years = len(df)/12
        cagr = (((final_acc_balance/beginning_acc_balance)**(1/num_years)) - 1)*100
        return {'final_acc_balance': final_acc_balance, 'CAGR': f"{cagr} %"}

    def strategy_sim(self, threshold: float) -> dict:
        """
        """
        df_out = self.price_history.copy()
        cash_to_invest = [self.m_cash_flow]
        num_shares_bought = []
        for i in range(len(df_out)):
            #print(self.m_cash_flow)
            diff = (df_out.iloc[i]['Close'] - df_out.iloc[i]['lb'])/df_out.iloc[i]['lb']
            # buy signal
            if diff <= threshold:
                num_shares_bought.append(cash_to_invest[i]/df_out.iloc[i]['Close'])
                cash_to_invest[i] = 0
            else:
                num_shares_bought.append(0)
            cash_to_invest.append(cash_to_invest[i] + self.m_cash_flow)
        df_out['num_shares_bought'] = num_shares_bought
        df_out['cash_to_invest'] = cash_to_invest[0:len(cash_to_invest)-1]
        return {'sim_results': df_out, 'return': self.compute_return(df_out)}

    def dca_sim(self) -> dict:
        """
        """
        df_out = self.price_history.copy()
        df_out['cash_to_invest'] = [self.m_cash_flow] * len(df_out)
        df_out['num_shares_bought'] = df_out['cash_to_invest']/df_out['Close']
        return {'sim_results': df_out, 'return': self.compute_return(df_out)}