﻿# -*- coding:utf-8 -*-
# Create On 20161222
# Auth: wang.yijian
# desc: 交易日历

import sys;sys.path.append("../")
import datetime
import utils.dateTime as dateTime


class CTradingCalendar(object):
    __dictTc = {}       # strExchange, set<int>

    def Empty(self):
        if (len(self.__dictTc) == 0):
            return True
        else:
            return False

    # Set && Get
    def Add(self, strExchange, setTc):
        self.__dictTc[strExchange] = sorted(setTc)

    def GetAll(self):
        return self.__dictTc

    def Get(self, strExchange):
        if (strExchange in self.__dictTc):
            return self.__dictTc[strExchange]
        else:
            return None

    def IsTradingDay(self, strExchange, tradingDay):
        if (strExchange in self.__dictTc == False):
            return False
        nTradingDay = tradingDay
        if (isinstance(tradingDay, str)):
            strTd = dateTime.ToIso(tradingDay)
            if (strTd == None):
                return False
            nTradingDay = int(strTd)
        return nTradingDay in self.__dictTc[strExchange]
    
    def GetPreTradingDay(self, strExchange, tradingDay):
        dtTradingDay = dateTime.ToDateTime(tradingDay)
        nTradingDay = int(dateTime.ToIso(tradingDay))
        if nTradingday <= self.__dictTc[strExchange][0]:
            return False, 0

        while True:
            dtTradingDay = Yestoday(dtTradingDay)
            nTradingDay = int(dateTime.ToIso(dtTradingDay))
            if self.IsTradingDay(nTradingDay) == True:
                return True, nTradingDay                


    def GetNextTradingDay(self, strExchange, tradingDay):
        nTradingDay = tradingDay           
        if (isinstance(tradingDay, str) or isinstance(tradingDay, datetime.datetime)):
            strTd = dateTime.ToIso(tradingDay)
            if (strTd == None):
                return False, 0
            nTradingDay = int(strTd)
        
        if (self.IsTradingDay(strExchange, tradingDay) == True):
            tdIndex = self.__dictTc[strExchange].index(nTradingDay) + 1
            if (tdIndex >= len(self.__dictTc[strExchange])):
                return False, 0
            return True, self.__dictTc[strExchange][tdIndex]
        else:
            if (strExchange in self.__dictTc == False):
                return False, 0
            if (len(self.__dictTc[strExchange]) <= 0):
                return False, 0
            n1st = self.__dictTc[strExchange][0]
            nLast = self.__dictTc[strExchange][len(self.__dictTc[strExchange])-1]
            # 比第一天还早，则返回第一天
            if (nTradingDay < n1st):
                return True, n1st
            # 比最后一天还晚，则返回错误
            elif (nTradingDay > nLast):
                return False, 0

            for nDay in self.__dictTc[strExchange]:
                if nTradingDay < nDay:
                    return True, nDay
            return False, 0

    def GetTradingDayList(self, strExchange, dtFrom, dtTo, bDateTime = False):
        listRtn = []
        nTradingDay = int(dateTime.ToIso(dtFrom))
        nTdTo = int(dateTime.ToIso(dtTo))
        if self.IsTradingDay(strExchange, nTradingDay) == True:
            if bDateTime == True:
                listRtn.append(dateTime.ToDateTime(dtFrom))
            else:
                listRtn.append(nTradingDay)
        while True:
            bSuccess, nTradingDay = self.GetNextTradingDay(strExchange, nTradingDay)
            if bSuccess == False or nTradingDay > nTdTo:
                break
            if bDateTime == True:
                dtTradingDay = dateTime.ToDateTime(nTradingDay)
                listRtn.append(dtTradingDay)
            else:
                listRtn.append(nTradingDay)
        return listRtn
    
    def GetTradingDayCount(self, strExchange, tdFrom, tdTo):
        if (self.IsTradingDay(strExchange, tdFrom) == False or self.IsTradingDay(strExchange, tdTo) == False):
            return False, 0

        nFrom = tdFrom
        nTo = tdTo
        if (isinstance(nFrom, str)):
            strTd = dateTime.ToIso(nFrom)
            if (strTd == False, -1):
                return False, -1
            nFrom = int(strTd)
        if (isinstance(nTo, str)):
            strTd = dateTime.ToIso(nTo)
            if (strTd == False, -1):
                return False, -1
            nTo = int(strTd)

        tdIndexFrom = self.__dictTc[strExchange].index(nFrom)
        tdIndexTo = self.__dictTc[strExchange].index(nTo)
        return True, tdIndexTo - tdIndexFrom


    # [04.01.YYYY   ~ 05.01.YYYY)   -> 12.31.YYYY-1
    # [05.01.YYYY   ~ 09.01.YYYY)   -> 03.31.YYYY
    # [09.01.YYYY   ~ 11.01.YYYY)   -> 06.30.YYYY
    # [11.01.YYYY   ~ 04.01.YYYY+1) -> 09.30.YYYY
    @staticmethod
    def GetStockReportPeriod(inputTradingDay):
        dtTd = dateTime.ToDateTime(inputTradingDay)
        dtInput = dtTd.date()
        nYearInput = dtInput.year

        dt0 = datetime.date(nYearInput - 1, 11, 1)
        dt1 = datetime.date(nYearInput, 4, 1);
        dt2 = datetime.date(nYearInput, 5, 1);
        dt3 = datetime.date(nYearInput, 9, 1);
        dt4 = datetime.date(nYearInput, 11, 1);
        dt5 = datetime.date(nYearInput + 1, 4, 1);

        dtRtn = None
        if (dtInput >= dt0 and dtInput < dt1):
            dtRtn = datetime.date(nYearInput - 1, 9, 30)
        elif (dtInput >= dt1 and dtInput < dt2):
            dtRtn = datetime.date(nYearInput - 1, 12, 31)
        elif (dtInput >= dt2 and dtInput < dt3):
            dtRtn = datetime.date(nYearInput, 3, 31)
        elif (dtInput >= dt3 and dtInput < dt4):
            dtRtn = datetime.date(nYearInput, 6, 30)
        elif (dtInput >= dt4 and dtInput < dt5):
            dtRtn = datetime.date(nYearInput, 9, 30)
        return dtRtn


    def Print(self):
        for key in self.__dictTc.keys():
            print('----- ', key, ' -----')
            print(self.__dictTc[key])



