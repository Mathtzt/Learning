import pandas as pd
import joblib

class ModelTitanic():
    """
    Classe criada para aplicação destinada a prever se o usuário, dado as características inseridas, sobreviveria ao naufrágio do Titanic ou não. 
    Para tal, a classe utiliza-se de um modelo de ML treinado previamente para esse fim.
    """
    def __init__(self, values: dict):
        self.df = self.get_data(values)

    def predict(self):
        """Método responsável por realizar os processos necessários e a predição utilizando o modelo, com base na entrada de dados do usuário.

        Returns:
            bool: Retorna True se o usuário sobreviveria ou False se o usuário morreria no Titanic.
        """
        self.replace_values()
        data = self.create_dummies(self.df)
        # print(data)
        data = self.get_scaler().transform(data)

        res = self.get_model().predict(data)

        return True if res[0] == 1 else False
    
    def get_model(self):
        """Método responsável por carregar o modelo treinado previamente.

        Returns:
            model: Retorna o modelo.
        """
        return joblib.load('./classe/model/model.sav')

    def get_scaler(self):
        """Método responsável por carregar o scaler utilizado no treinamento do modelo.

        Returns:
            scaler: Retorna o scaler.
        """
        return joblib.load('./classe/model/scaler.sav')

    def get_data(self, values: dict):
        """Método responsável por criar um DataFrame com base nos valores recebidos pela aplicação.

        Args:
            values (dict): Dicionário com os valores coletados pela entrada de dados do usuário.

        Returns:
            DataFrame: Retorna um dataframe com os respectivos valores.
        """
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
        """
        Método responsável por realizar a substituição dos valores das variáveis sexo e classe navio, a fim de respeitar suas características e o modo como foram utilizadas no modelo.
        """
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

    def create_dummies(self, df: pd.DataFrame):
        """Método responsável por criar as variáveis dummies manualmente.
        Dado o fato de a entrada para teste/predição ser única, as variáveis dummies precisam ser criadas respeitando a lógica preestabelecida.

        Args:
            df (DataFrame): DataFrame Python com os dados.

        Returns:
            DataFrame: retorna um dataframe com as variáveis criadas e sem as variáveis originais.
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
