# -*- coding: utf-8 -*-
"""
Created on Sun Nov 01 19:28:44 2015

@author: Alexis
"""

import pandas as pd

from anonymizer.anonymity import get_k, less_anonym_groups
from anonymizer.diversity import (get_l, get_diversities, diversity_distribution,
                       less_diverse_groups)


class AnonymDataFrame(object):

    def __init__(self, df, var_identifiantes, var_sensibles):
        assert isinstance(df, pd.DataFrame)
        self.df = df

        columns = df.columns
        for var in [var_identifiantes]:
            assert isinstance(var, list)
        assert isinstance(var_sensibles, str)
        if not all([x in columns for x in var_identifiantes]):
            not_in_columns = [x for x in var_identifiantes if x not in columns]
            raise Exception(not_in_columns, ' not in df.columns')
        assert var_sensibles in columns
        assert var_sensibles not in var_identifiantes
        self.identifiant = var_identifiantes
        self.sensible = var_sensibles

    def list_valeurs_identifiantes(self):
        for var in self.identifiant:
            print(self.df[var].unique())

    def get_k(self):
        return get_k(self.df, self.identifiant)

    def less_anonym_groups(self):
        return less_anonym_groups(self.df, self.identifiant)

    def get_l(self):
        return get_l(self.df, self.identifiant, self.sensible)

    def get_diversities(self):
        return get_diversities(self.df, self.identifiant, self.sensible)

    def diversity_distribution(self):
        return diversity_distribution(self.df, self.identifiant, self.sensible)

    def less_diverse_groups(self):
        return less_diverse_groups(self.df, self.identifiant, self.sensible)


    def transform(self, transformation):
        ''' return a new AnonymDataFrame with
            transformation is a dict where:
                keys are columns of self.df
                values are transformations to operate on var
        '''
        assert isinstance(transformation, dict)
        assert all([x in self.df.columns for x in transformation])
        df = self.df.copy()
        for colname, transfo in transformation.iteritems():
            df[colname] = transfo(self.df[colname])
        return AnonymDataFrame(df, self.identifiant, self.sensible)
