from pymongo.collection import Collection
from tabulate import tabulate
from bson import ObjectId


class MedicoController:
    def __init__(self, collection: Collection, consultas_collection: Collection):
        self.collection = collection
        self.consultas_collection = consultas_collection

    def inserir_medico(self, nome, especialidade, telefone):
        try:
            self.collection.insert_one({
                "nome": nome,
                "especialidade": especialidade,
                "telefone": telefone
            })
            print("Médico inserido com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir médico: {e}")

    def listar_medicos(self, return_data=False):
        try:
            medicos = list(self.collection.find())
            formatted_medicos = []

            for medico in medicos:
                formatted_medicos.append([
                    str(medico["_id"]),  # Convertendo ObjectId para string
                    medico["nome"],
                    medico["especialidade"],
                    medico["telefone"]
                ])

            if return_data:
                return formatted_medicos
            
            # Exibir os dados formatados
            headers = ["ID", "Nome", "Especialidade", "Telefone"]
            print(tabulate(formatted_medicos, headers=headers, tablefmt="grid"))

        except Exception as e:
            print(f"Erro ao listar médicos: {e}")

    def atualizar_medico(self, medico_id, **updates):
        try:
            self.collection.update_one({"_id": medico_id}, {"$set": updates})
            print("Médico atualizado com sucesso!")
        except Exception as e:
            print(f"Erro ao atualizar médico: {e}")
    
    def remover_medico(self, medico_id):
        try:
            resultado = self.collection.delete_one({"_id": ObjectId(medico_id)})
            if resultado.deleted_count > 0:
                print("Médico removido com sucesso!")

                # Remover todas as consultas associadas ao médico
                consultas_removidas = self.consultas_collection.delete_many({"medico_id": ObjectId(medico_id)})
                print(f"{consultas_removidas.deleted_count} consultas associadas ao médico foram removidas.")
            else:
                print("Nenhum médico encontrado com o ID fornecido.")
        except Exception as e:
            print(f"Erro ao remover médico: {e}")