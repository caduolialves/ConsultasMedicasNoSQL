from pymongo.collection import Collection
from tabulate import tabulate
from bson import ObjectId
from utils.selection_utils import selecionar_item

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

    def atualizar_medico(self):
        while True:
            try:
                # Listar médicos para o usuário selecionar
                print("\n--- Selecionar Médico para Atualização ---")
                medicos = self.listar_medicos(return_data=True)
                medico_opcoes = [(medico[0], f"{medico[1]} ({medico[2]})") for medico in medicos]
                medico_id = selecionar_item("Selecione o Médico para Atualizar", medico_opcoes)

                if not medico_id:
                    print("Nenhum médico selecionado. Tente novamente.")
                    return

                # Solicitar os campos para atualização
                updates = {}
                nome = input("Novo nome (deixe vazio para não alterar): ").strip()
                especialidade = input("Nova especialidade (deixe vazio para não alterar): ").strip()
                telefone = input("Novo telefone (deixe vazio para não alterar): ").strip()

                if nome:
                    updates["nome"] = nome
                if especialidade:
                    updates["especialidade"] = especialidade
                if telefone:
                    updates["telefone"] = telefone

                # Atualizar no banco
                self.collection.update_one({"_id": ObjectId(medico_id)}, {"$set": updates})
                print("Médico atualizado com sucesso!")

                # Perguntar se deseja atualizar outro médico
                continuar = input("Deseja atualizar outro médico? (s/n): ").strip().lower()
                if continuar != 's':
                    break

            except Exception as e:
                print(f"Erro ao atualizar médico: {e}")
                break

    
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