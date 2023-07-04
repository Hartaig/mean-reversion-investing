import pandas as pd
import numpy as np

class Simulator:
    def __init__(self, m_cash_flow, price_history):
        self.m_cash_flow = m_cash_flow
        self.price_history = price_history
    
    def compute_return(self, dfs: list[pd.DataFrame], period: str='Y') -> dict:
        """
        """
        # merge data
        df_final = dfs[0][['Date', 'Close']]
        s = 0
        for i in dfs:
            s = s + 1
            df_out = i[['Date', 'num_shares_bought', 'cash_to_invest']]
            df_out = df_out.rename(columns={'num_shares_bought':f"s{s}_num_shares_bought",
                                            'cash_to_invest': f"s{s}_cash_to_invest"})
            df_final = df_final.merge(df_out, on='Date', how='left')
        df_final[period] = df_final['Date'].dt.to_period(period)
        # groupby data
        g_dict = {'Close': 'last'}
        for i in [x for x in df_final.columns if x.startswith('s')]:
            if i.endswith('cash_to_invest'):
                g_dict.update({i: 'last'})
            else:
                g_dict.update({i: 'sum'})
        df_final_g = df_final.groupby(period).agg(g_dict).reset_index()
        # calculate return metrics
        d = {}
        for i in range(1, s + 1):
            df_final_g[f"s{i}_num_shares_bought_cumsum"] = np.cumsum(df_final_g[f"s{i}_num_shares_bought"])
            df_final_g[f"s{i}_value"] = df_final_g['Close']*df_final_g[f"s{i}_num_shares_bought_cumsum"] 
            df_final_g[f"s{i}_return"] = ((df_final_g[f"s{i}_value"] - df_final_g[f"s{i}_value"].shift(1))/df_final_g[f"s{i}_value"].shift(1))*100
            d.update({f"s{i}_avg_overall_return": np.mean(df_final_g[f"s{i}_return"])})
            d.update({f"s{i}_std_overall_return": np.std(df_final_g[f"s{i}_return"])})
            d.update({f"s{i}_avg_pos_return": np.mean(df_final_g[df_final_g[f"s{i}_return"]>0][f"s{i}_return"])})
            d.update({f"s{i}_avg_neg_return": np.mean(df_final_g[df_final_g[f"s{i}_return"]<0][f"s{i}_return"])})
            d.update({f"s{i}_end_val": df_final_g[f"s{i}_value"][len(df_final_g)-1]})
            d.update({f"s{i}_cagr": (((d[f"s{i}_end_val"]/self.m_cash_flow)**(1/len(df_final_g))) - 1)*100})
        return {'df_agg': df_final_g, 'return': d}


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
        return df_out

    def dca_sim(self) -> dict:
        """
        """
        df_out = self.price_history.copy()
        df_out['cash_to_invest'] = [self.m_cash_flow] * len(df_out)
        df_out['num_shares_bought'] = df_out['cash_to_invest']/df_out['Close']
        df_out['cash_to_invest'] = 0
        return df_out