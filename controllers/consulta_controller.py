from pymongo.collection import Collection
from tabulate import tabulate
from bson import ObjectId
from utils.selection_utils import selecionar_item

class ConsultaController:

    def __init__(self, collection: Collection):
        self.collection = collection

    def inserir_consulta(self, medico_id, paciente_id, data_consulta, hora_consulta, status):
        try:
            self.collection.insert_one({
                "medico_id": ObjectId(medico_id),  # Converter para ObjectId
                "paciente_id": ObjectId(paciente_id),  # Converter para ObjectId
                "data_consulta": data_consulta,
                "hora_consulta": hora_consulta,
                "status": status
            })
            print("Consulta marcada com sucesso!")
        except Exception as e:
            print(f"Erro ao marcar consulta: {e}")
            
    def listar_consultas(self, return_data=False):
        try:
            consultas = list(self.collection.find())
            formatted_consultas = []

            for consulta in consultas:
                formatted_consultas.append([
                    str(consulta["_id"]),  # Convertendo ObjectId para string
                    consulta["medico_id"],
                    consulta["paciente_id"],
                    consulta["data_consulta"],
                    consulta["hora_consulta"],
                    consulta["status"]
                ])

            if return_data:
                return formatted_consultas
            
            # Exibir os dados formatados
            headers = ["ID", "Médico ID", "Paciente ID", "Data", "Hora", "Status"]
            print(tabulate(formatted_consultas, headers=headers, tablefmt="grid"))

        except Exception as e:
            print(f"Erro ao listar consultas: {e}")

    def atualizar_consulta(self):
        while True:
            try:
                # Listar consultas para o usuário selecionar
                print("\n--- Selecionar Consulta para Atualização ---")
                consultas = self.listar_consultas(return_data=True)
                consulta_opcoes = [
                    (consulta[0], f"Médico: {consulta[1]}, Paciente: {consulta[2]}, Data: {consulta[3]}")
                    for consulta in consultas
                ]
                consulta_id = selecionar_item("Selecione a Consulta para Atualizar", consulta_opcoes)

                if not consulta_id:
                    print("Nenhuma consulta selecionada. Tente novamente.")
                    return

                # Solicitar os campos para atualização
                updates = {}
                data_consulta = input("Nova data (YYYY-MM-DD) (deixe vazio para não alterar): ").strip()
                hora_consulta = input("Nova hora (HH:MM) (deixe vazio para não alterar): ").strip()
                status = input("Novo status (deixe vazio para não alterar): ").strip()

                if data_consulta:
                    updates["data_consulta"] = data_consulta
                if hora_consulta:
                    updates["hora_consulta"] = hora_consulta
                if status:
                    updates["status"] = status

                # Atualizar no banco
                self.collection.update_one({"_id": ObjectId(consulta_id)}, {"$set": updates})
                print("Consulta atualizada com sucesso!")

                # Perguntar se deseja atualizar outra consulta
                continuar = input("Deseja atualizar outra consulta? (s/n): ").strip().lower()
                if continuar != 's':
                    break

            except Exception as e:
                print(f"Erro ao atualizar consulta: {e}")
                break


    def remover_consulta(self, consulta_id):
        try:
            resultado = self.collection.delete_one({"_id": ObjectId(consulta_id)})
            if resultado.deleted_count > 0:
                print("Consulta removida com sucesso!")
            else:
                print("Nenhuma consulta encontrada com o ID fornecido.")
        except Exception as e:
            print(f"Erro ao remover consulta: {e}")

    def consultas_por_medico(self):
        try:
            # Pipeline de agregação para contar consultas por médico com o nome do médico
            pipeline = [
                {
                    "$group": {
                        "_id": "$medico_id",  # Agrupar por ID do médico
                        "total_consultas": {"$sum": 1}  # Contar o número de consultas
                    }
                },
                {
                    "$lookup": {
                        "from": "medicos",  # Nome da coleção de médicos
                        "localField": "_id",  # Campo no agrupamento
                        "foreignField": "_id",  # Campo na coleção de médicos
                        "as": "medico_info"  # Resultado será armazenado aqui
                    }
                },
                {
                    "$unwind": "$medico_info"  # Desmembrar a lista para acessar o objeto médico
                },
                {
                    "$project": {  # Selecionar apenas os campos desejados
                        "nome_medico": "$medico_info.nome",
                        "total_consultas": 1
                    }
                }
            ]

            resultados = list(self.collection.aggregate(pipeline))

            if not resultados:
                print("Nenhuma consulta agendada encontrada.")
                return

            # Formatando os resultados para exibição
            formatted_resultados = []
            for resultado in resultados:
                formatted_resultados.append([resultado["nome_medico"], resultado["total_consultas"]])

            # Exibir relatório formatado
            headers = ["Nome do Médico", "Total de Consultas Agendadas"]
            print(tabulate(formatted_resultados, headers=headers, tablefmt="grid"))

        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")

    def consultas_por_medico_detalhadas(self):
        try:
            # Pipeline de agregação para juntar os dados de médicos e consultas
            pipeline = [
                {
                    "$lookup": {
                        "from": "medicos",  # Nome da coleção de médicos
                        "localField": "medico_id",  # Campo na coleção de consultas
                        "foreignField": "_id",  # Campo na coleção de médicos
                        "as": "medico_info"  # Resultado será armazenado aqui
                    }
                },
                {
                    "$unwind": "$medico_info"  # Desmembrar a lista para acessar o objeto médico
                },
                {
                    "$project": {  # Selecionar apenas os campos desejados
                        "medico_nome": "$medico_info.nome",
                        "paciente_id": 1,
                        "data_consulta": 1,
                        "hora_consulta": 1,
                        "status": 1
                    }
                }
            ]

            # Executar o pipeline
            resultados = list(self.collection.aggregate(pipeline))

            if not resultados:
                print("Nenhuma consulta encontrada.")
                return

            # Formatando os resultados para exibição
            formatted_resultados = []
            for resultado in resultados:
                formatted_resultados.append([
                    resultado["medico_nome"],
                    str(resultado["paciente_id"]),
                    resultado["data_consulta"],
                    resultado["hora_consulta"],
                    resultado["status"]
                ])

            # Exibir os dados formatados
            headers = ["Médico", "Paciente ID", "Data", "Hora", "Status"]
            print(tabulate(formatted_resultados, headers=headers, tablefmt="grid"))

        except Exception as e:
            print(f"Erro ao gerar relatório detalhado: {e}")