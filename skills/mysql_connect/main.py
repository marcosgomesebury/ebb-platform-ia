import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def get_env(label, default=None):
	return os.environ.get(label, default)

def testar_conexao():
	host = get_env('EBB_CONCILIACAO_MYSQL_DEV_HOST')
	user = get_env('EBB_CONCILIACAO_MYSQL_DEV_USER')
	password = get_env('EBB_CONCILIACAO_MYSQL_DEV_PASSWORD')
	database = get_env('EBB_CONCILIACAO_MYSQL_DEV_DATABASE')

	print(f"[ebb-conciliacao-mysql-dev] Testando conexão com {host}, database {database}...")
	try:
		connection = pymysql.connect(
			host=host,
			user=user,
			password=password,
			database=database
		)
		print("Conexão bem-sucedida!")
		with connection.cursor() as cursor:
			cursor.execute("SELECT VERSION()")
			db_info = cursor.fetchone()
			print("Versão do MySQL:", db_info[0])
	except Exception as e:
		print("Erro ao conectar:", e)
	finally:
		if 'connection' in locals():
			connection.close()
			print("Conexão encerrada.")

if __name__ == "__main__":
	testar_conexao()
