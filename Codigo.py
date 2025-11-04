import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Este script é apenas um exemplo. Todas as credenciais foram removidas por segurança.

def atividades_ti():
    # Configurações
    ZCRM_CLIENT_ID = "SEU_CLIENT_ID_AQUI"
    ZCRM_CLIENT_SECRET = "SEU_CLIENT_SECRET_AQUI"
    ZCRM_REFRESH_TOKEN = "SEU_REFRESH_TOKEN_AQUI"
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "SENHA_AQUI"

    MYSQL_DB = "backup"
    MYSQL_PORT = "3306"

    # Função para obter access_token a partir do refresh_token
    def get_access_token():
        url = "sua URL ZOHO token aqui"
        body = {
            'refresh_token': ZCRM_REFRESH_TOKEN,
            'client_id': ZCRM_CLIENT_ID,
            'client_secret': ZCRM_CLIENT_SECRET,
            'grant_type': 'refresh_token'
        }
        
        response = requests.post(url, data=body)
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            print("❌ Erro ao obter o access_token:", response.json())
            return None

    # Função para buscar todas as páginas de tarefas no Zoho CRM
    def get_all_tasks(access_token):
        url = "sua URL ZOHO aqui"
        headers = {"Authorization": f"Bearer {access_token}"}
        tasks = []
        more_records = True
        page = 1

        while more_records:
            params = {"page": page, "per_page": 200}  # Pega 200 registros por página
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                tasks.extend(data.get('data', []))
                more_records = data.get('info', {}).get('more_records', False)
                page += 1
            else:
                print(f"❌ Erro ao buscar dados na página {page}:", response.json())
                break
        
        return tasks

    # Função para inserir tarefas no banco de dados
    def insert_tasks(conn, tasks):
        try:
            cursor = conn.cursor()

            # Excluir todas as tarefas antes de reimportar
            cursor.execute("DELETE FROM atividades_ti")
            conn.commit()
            print("✅ Tabela limpa antes da inserção.")

            '''
            

            '''
            for task in tasks:
                # Verifique se 'Solicitante' é um dicionário e, caso contrário, defina como uma string vazia
                solicitante = task.get('Solicitante', {})
                solicitante_name = solicitante.get('name', '') if isinstance(solicitante, dict) else ''
                
                # Verifique se 'Owner' e outros campos que podem ser dicionários ou não são strings
                owner = task.get('Owner', {})
                owner_name = owner.get('name', '') if isinstance(owner, dict) else task.get('Owner', '')

                # Verifique se 'Prioridade' e 'Tipo_de_demanda' são dicionários antes de acessar valores
                prioridade = task.get('Prioridade', '')
                tipo_de_demanda = task.get('Tipo_de_demanda', '')
                setor_solicitante = task.get('Setor_da_solicita_o','')
                tecnologia_utilizada = task.get('Tecnologia','')

                # Verifique se 'Data_cria_o' está no formato adequado para ser inserido
                data_criacao = task.get('Data_cria_o', '')
                
                # Verifique o status da tarefa
                status = task.get('Status', '')

                # Agora insira os dados no banco
                cursor.execute("""
                    INSERT INTO atividades_ti (name, solicitante_name, proprietario, prioridade, tipo_de_demanda, Data_criacao, Status,setor_solicitante, tecnologia)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s , %s)
                """, (
                    task.get('Name', ''),
                    solicitante_name,
                    owner_name,
                    prioridade,
                    tipo_de_demanda,
                    data_criacao,
                    status,
                    setor_solicitante,
                    tecnologia_utilizada
                ))

            conn.commit()
            print(f"✅ {len(tasks)} tarefas inseridas com sucesso!")
            print(task.get('Solicitante'))  # Verifique o conteúdo completo
            print(f"✅ {len(tasks)} tarefas inseridas com sucesso!")
            print(task.get('Solicitante'))  # Verifique o conteúdo completo

        
        except Error as e:
            print("❌ Erro ao inserir tarefas:", e)
        
        finally:
            cursor.close()

    # Função principal
    def main():
        access_token = get_access_token()
        if not access_token:
            return

        tasks = get_all_tasks(access_token)
        if not tasks:
            print("⚠ Nenhuma tarefa encontrada.")
            return

        try:
            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DB,
                port=MYSQL_PORT
            )
            if conn.is_connected():
                print("✅ Conexão com o banco de dados bem-sucedida!")
                insert_tasks(conn, tasks)
                conn.close()
                print("🎉 Processo concluído com sucesso!")
        except Error as e:
            print("❌ Erro ao conectar ao banco de dados:", e)

    if __name__ == "__main__":
        main()



print("Rodando o código...")
atividades_ti()
print("Finalizado.")
