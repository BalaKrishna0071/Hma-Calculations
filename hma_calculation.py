import numpy as np
import pandas as pd

class Calc:
    def __init__(self, arr:int):
        self.arr = arr
        self.df=pd.DataFrame(arr, columns=['close'])

    # change column calculation
    def change(self):
        self.df['change']=self.df['close']-self.df['close'].shift()
        return self.df['change']

    # gain column calculation
    def gain(self):

        self.df['gain'] = self.df['change'].apply(lambda x: x if x>0 else 0)

    # loss column calculation
    def loss(self):

        self.df['loss']= self.df['change'].apply(lambda x: x*-1 if x<0 else 0)

    # avg_gain column calculation
    def avg_gain(self):

         self.df['step1']=self.df['gain'].rolling(window=14).sum()/14
         self.df['step2'] = self.df['step1'].shift(1)

         self.df['avg_gain']=self.df.apply(lambda x: ((x['step2']*13) + x['gain'])/14,axis=1)

    # avg_loss column calculation
    def avg_loss(self):
        self.df['stepone']=self.df['loss'].rolling(window=14).sum()/14
        self.df['steptwo']=self.df['stepone'].shift(1)

        self.df['avg_loss']=self.df.apply(lambda x: ((x['steptwo']*13) + x['loss'])/14,axis=1)

    # hm column calculation
    def hm(self):
        self.df['hm']=self.df['avg_gain']/self.df['avg_loss']

        return self.df

    # hma column calculation
    def hma(self):
        self.df['hma']=self.df.apply(lambda x: 100 if x['avg_gain'] == 0 else 100-(100/(1+x['hm'])), axis=1)


    # main function for calling all other function
    def calculatehma(self):
        self.change()
        self.gain()
        self.loss()
        self.avg_gain()
        self.avg_loss()
        self.hm()
        self.hma()
        self.df = self.df.drop(columns =['step1','step2','stepone','steptwo'])
        self.df = self.df.replace(np.nan, 0)
        return self.df

