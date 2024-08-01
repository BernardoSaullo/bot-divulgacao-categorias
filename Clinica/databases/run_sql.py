import mysql.connector
from mysql.connector import Error
from dataclasses import fields

class DatabaseManager:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = "root"
        self.password = "1234"
        self.database = 'clinica_psicologica'
        self.connection = None
        self.cursor = None

    def conectar(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Conexão bem-sucedida")
        except Error as error:
            print(f"Erro ao conectar: {error}")

    def desconectar(self):
        if self.connection is not None:
            self.connection.close()
            print("Conexão fechada")

    # def criar_tabela(self, cls):
    #     table_name = cls.__name__
    #     sql_fields = []
    #     for field in fields(cls):
    #         if field.name == 'id':
    #             sql_fields.append(f"{field.name} INT AUTO_INCREMENT PRIMARY KEY")
    #         else:
    #             field_type = "VARCHAR(255)" if field.type == str else "TEXT"
    #             sql_fields.append(f"{field.name} {field_type}")
    #     sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(sql_fields)});"
    #     try:
    #         self.cursor.execute(sql)
    #         self.connection.commit()
    #         print(f"Tabela {table_name} criada com sucesso")
    #     except Error as error:
    #         print(f"Erro ao criar tabela: {error}")

    def inserir(self, obj):
        table_name = obj.__class__.__name__
        fields_names = [field.name for field in fields(obj) if field.name != 'id']
        fields_values = [getattr(obj, field) for field in fields_names]
        placeholders = ", ".join(["%s"] * len(fields_names))
        sql = f"INSERT INTO {table_name} ({', '.join(fields_names)}) VALUES ({placeholders})"
        print(fields_names)
        print(fields_values)
        print(sql)
        
        try:
            self.cursor.execute(sql, fields_values)
            self.connection.commit()
            obj.id = self.cursor.lastrowid
            print(f"{table_name} inserido com sucesso")
        except Error as error:
            print(f"Erro ao inserir {table_name}: {error}")


    def autenticar_usuario(self,cls, username, password):
            table_name = cls.__name__

            sql = f"SELECT * FROM {table_name} WHERE email = %s AND senha = %s"
            try:
                self.cursor.execute(sql, (username, password))
                user = self.cursor.fetchone()
                if user:
                    print("Autenticação bem-sucedida")
                    return True
                else:
                    print("Falha na autenticação")
                    return False
            except Error as error:
                print(f"Erro ao autenticar usuário: {error}")
                return False


    def ler_por_id(self, cls, obj_id):
        table_name = cls.__name__
        sql = f"SELECT * FROM {table_name} WHERE id = %s"
        try:
            self.cursor.execute(sql, (obj_id,))
            row = self.cursor.fetchone()
            return row
          
        except Error as error:
            print(f"Erro ao ler {table_name}: {error}")


    def atualizar(self, obj):
        table_name = obj.__class__.__name__
        fields_names = [field.name for field in fields(obj) if field.name != 'id']
        fields_values = [getattr(obj, field) for field in fields_names]
        fields_updates = ", ".join([f"{field} = %s" for field in fields_names])
        sql = f"UPDATE {table_name} SET {fields_updates} WHERE id = %s"
        try:
            self.cursor.execute(sql, fields_values + [obj.id])
            self.connection.commit()
            print(f"{table_name} atualizado com sucesso")
        except Error as error:
            print(f"Erro ao atualizar {table_name}: {error}")


    def deletar(self, cls, obj_id):
        table_name = cls.__name__
        sql = f"DELETE FROM {table_name} WHERE id = %s"
        try:
            self.cursor.execute(sql, (obj_id,))
            self.connection.commit()
            print(f"{table_name} deletado com sucesso")
        except Error as error:
            print(f"Erro ao deletar {table_name}: {error}")



