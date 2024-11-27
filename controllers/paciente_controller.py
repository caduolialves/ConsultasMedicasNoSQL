from pymongo.collection import Collection
from tabulate import tabulate
from bson import ObjectId
from utils.selection_utils import selecionar_item

class PacienteController:
    def __init__(self, collection: Collection, consultas_collection: Collection):
        self.collection = collection
        self.consultas_collection = consultas_collection

    def inserir_paciente(self, nome, telefone):
        try:
            self.collection.insert_one({
                "nome": nome,
                "telefone": telefone
            })
            print("Paciente inserido com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir paciente: {e}")

    def listar_pacientes(self, return_data=False):
        try:
            pacientes = list(self.collection.find())
            formatted_pacientes = []

            for paciente in pacientes:
                formatted_pacientes.append([
                    str(paciente["_id"]),  # Convertendo ObjectId para string
                    paciente["nome"],
                    paciente["telefone"]
                ])

            if return_data:
                return formatted_pacientes
            
            # Exibir os dados formatados
            headers = ["ID", "Nome", "Telefone"]
            print(tabulate(formatted_pacientes, headers=headers, tablefmt="grid"))

        except Exception as e:
            print(f"Erro ao listar pacientes: {e}")

    def atualizar_paciente(self):
        while True:
            try:
                # Listar pacientes para o usuário selecionar
                print("\n--- Selecionar Paciente para Atualização ---")
                pacientes = self.listar_pacientes(return_data=True)
                paciente_opcoes = [(paciente[0], f"{paciente[1]}") for paciente in pacientes]
                paciente_id = selecionar_item("Selecione o Paciente para Atualizar", paciente_opcoes)

                if not paciente_id:
                    print("Nenhum paciente selecionado. Tente novamente.")
                    return

                # Solicitar os campos para atualização
                updates = {}
                nome = input("Novo nome (deixe vazio para não alterar): ").strip()
                telefone = input("Novo telefone (deixe vazio para não alterar): ").strip()

                if nome:
                    updates["nome"] = nome
                if telefone:
                    updates["telefone"] = telefone

                # Atualizar no banco
                self.collection.update_one({"_id": ObjectId(paciente_id)}, {"$set": updates})
                print("Paciente atualizado com sucesso!")

                # Perguntar se deseja atualizar outro paciente
                continuar = input("Deseja atualizar outro paciente? (s/n): ").strip().lower()
                if continuar != 's':
                    break

            except Exception as e:
                print(f"Erro ao atualizar paciente: {e}")
                break

    def remover_paciente(self, paciente_id):
        try:
            resultado = self.collection.delete_one({"_id": ObjectId(paciente_id)})
            if resultado.deleted_count > 0:
                print("Paciente removido com sucesso!")

                # Remover todas as consultas associadas ao paciente
                consultas_removidas = self.consultas_collection.delete_many({"paciente_id": ObjectId(paciente_id)})
                print(f"{consultas_removidas.deleted_count} consultas associadas ao paciente foram removidas.")
            else:
                print("Nenhum paciente encontrado com o ID fornecido.")
        except Exception as e:
            print(f"Erro ao remover paciente: {e}")
