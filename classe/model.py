import pandas as pd
import joblib

class ModelTitanic():
    def __init__(self, values: dict):
        self.df = self.get_data(values)

    def predict(self):
        self.replace_values()
        data = self.create_dummies(self.df)
        # print(data)
        data = self.get_scaler().transform(data)

        res = self.get_model().predict(data)

        return True if res[0] == 1 else False
    
    def get_model(self):
        return joblib.load('./classe/model/model.sav')

    def get_scaler(self):
        return joblib.load('./classe/model/scaler.sav')

    def get_data(self, values):
        v_ = {
            'idade': [values['idade_passageiro']],
            'sexo': [values['sexo_passageiro']],
            'classe_navio': [values['class_navio']],
            'valor_passagem': [values['valor_passagem']],
            'n_irmaos_conjuge': [values['qtd_irmaos_conjuge']] if values['qtd_irmaos_conjuge'] != None else [0],
            'n_pais_filhos': [values['qtd_pais_filhos']] if values['qtd_pais_filhos'] != None else [0],
            'porto_de_embarque': [values['porto_embarque']]
            }

        return pd.DataFrame(data = v_)

    def replace_values(self):
        mapper_sexo = {
            'Masculino': 'M',
            'Feminino': 'F'
        }

        self.df['sexo'] = self.df['sexo'].replace(mapper_sexo)

        mapper_classe_navio = {
            '1ª': 1,
            '2ª': 2,
            '3ª': 3
        }

        self.df['classe_navio'] = self.df['classe_navio'].replace(mapper_classe_navio)

    def create_dummies(self, df):
        """
        Método responsável por criar as variáveis dummies das variável categóricas.
        """
        cols = ['classe_navio', 'sexo', 'porto_de_embarque']
        
        df.loc[:, 'classe_navio_1'] = 1 if df[cols[0]][0] == 1 else 0
        df.loc[:, 'classe_navio_2'] = 1 if df[cols[0]][0] == 2 else 0
        df.loc[:, 'classe_navio_3'] = 1 if df[cols[0]][0] == 3 else 0

        df.loc[:, 'sexo_F'] = 1 if df[cols[1]][0] == 'F' else 0

        df.loc[:, 'porto_de_embarque_Cherbourg'] = 1 if df[cols[2]][0] == 'Cherbourg' else 0
        df.loc[:, 'porto_de_embarque_Queenstown'] = 1 if df[cols[2]][0] == 'Queenstown' else 0
        df.loc[:, 'porto_de_embarque_Southampton'] = 1 if df[cols[2]][0] == 'Southampton' else 0

        df.drop(cols, axis = 1, inplace = True)

        return df
