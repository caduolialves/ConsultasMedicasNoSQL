from controllers.medico_controller import MedicoController
from controllers.paciente_controller import PacienteController
from controllers.consulta_controller import ConsultaController
from config.database import get_database
from tabulate import tabulate
from utils.selection_utils import selecionar_item
from bson import ObjectId


def main():
    # Conectar ao banco de dados MongoDB
    db = get_database()

    # Inicializando os controladores com as coleções do MongoDB
    medico_controller = MedicoController(db.get_collection("medicos"), db.get_collection("consultas"))
    paciente_controller = PacienteController(db.get_collection("pacientes"), db.get_collection("consultas"))
    consulta_controller = ConsultaController(db.get_collection("consultas"))

    while True:
        print("\n----- Sistema de Controle de Consultas Médicas -----")
        print("1. Relatórios")
        print("2. Inserir registros")
        print("3. Remover registros")
        print("4. Atualizar registros")
        print("5. Listar registros")
        print("6. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            gerar_relatorios(consulta_controller)
        elif choice == '2':
            inserir_registros(medico_controller, paciente_controller, consulta_controller)
        elif choice == '3':
            remover_registros(medico_controller, paciente_controller, consulta_controller)
        elif choice == '4':
            atualizar_registros(medico_controller, paciente_controller, consulta_controller)
        elif choice == '5':
            listar_registros(medico_controller, paciente_controller, consulta_controller)
        elif choice == '6':
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def gerar_relatorios(consulta_controller):
    while True:
        print("\n--- Relatórios ---")
        print("1. Consultas por médico (detalhadas)")
        print("2. Total de consultas agendadas por médico")
        print("3. Voltar ao menu principal")
        choice = input("Escolha um relatório: ")

        if choice == '1':  # Relatório detalhado por médico
            consulta_controller.consultas_por_medico_detalhadas()

        elif choice == '2':  # Total de consultas por médico
            consulta_controller.consultas_por_medico()

        elif choice == '3':  # Voltar ao menu principal
            return
        else:   
            print("Opção inválida. Por favor, tente novamente.")

def inserir_registros(medico_controller, paciente_controller, consulta_controller):
    while True:
        print("\n--- Inserir Registros ---")
        print("1. Inserir Médico")
        print("2. Inserir Paciente")
        print("3. Inserir Consulta")
        print("4. Voltar ao menu principal")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            while True:
                nome = input("Nome do Médico: ")
                especialidade = input("Especialidade: ")
                telefone = input("Telefone: ")
                medico_controller.inserir_medico(nome, especialidade, telefone)

                continuar = input("Deseja inserir outro médico? (s/n): ").strip().lower()
                if continuar != 's':
                    break

        elif choice == '2':
            while True:
                nome = input("Nome do Paciente: ")
                telefone = input("Telefone: ")
                paciente_controller.inserir_paciente(nome, telefone)

                continuar = input("Deseja inserir outro paciente? (s/n): ").strip().lower()
                if continuar != 's':
                    break

        if choice == '3':  # Inserir Consulta
            while True:
                # Selecionar Médico
                print("\n--- Selecionar Médico ---")
                medicos = medico_controller.listar_medicos(return_data=True)
                medico_opcoes = [(medico[0], f"{medico[1]} ({medico[2]})") for medico in medicos]
                medico_id = selecionar_item("Selecione o Médico", medico_opcoes)

                if not medico_id:
                    print("Nenhum médico selecionado. Tente novamente.")
                    continue

                # Selecionar Paciente
                print("\n--- Selecionar Paciente ---")
                pacientes = paciente_controller.listar_pacientes(return_data=True)
                paciente_opcoes = [(paciente[0], f"{paciente[1]}") for paciente in pacientes]
                paciente_id = selecionar_item("Selecione o Paciente", paciente_opcoes)

                if not paciente_id:
                    print("Nenhum paciente selecionado. Tente novamente.")
                    continue

                # Selecionar Status
                print("\n--- Selecionar Status da Consulta ---")
                status_opcoes = [
                    ("Em andamento", "Em andamento"),
                    ("Concluído", "Concluído"),
                    ("Cancelado", "Cancelado")
                ]
                status = selecionar_item("Selecione o Status da Consulta", status_opcoes)

                if not status:
                    print("Nenhum status selecionado. Tente novamente.")
                    continue

                # Inserir Consulta
                data_consulta = input("Data da Consulta (YYYY-MM-DD): ")
                hora_consulta = input("Hora da Consulta (HH:MM): ")
                consulta_controller.inserir_consulta(medico_id, paciente_id, data_consulta, hora_consulta, status)

                continuar = input("Deseja inserir outra consulta? (s/n): ").strip().lower()
                if continuar != 's':
                    break

        elif choice == '4':  # Voltar ao menu principal
            return
        else:
            print("Opção inválida. Por favor, tente novamente.")

def remover_registros(medico_controller, paciente_controller, consulta_controller):
    while True:
        print("\n--- Remover Registros ---")
        print("1. Remover Médico")
        print("2. Remover Paciente")
        print("3. Remover Consulta")
        print("4. Voltar ao menu principal")
        choice = input("Escolha uma opção: ")

        if choice == '1':  # Remover Médico
            while True:
                # Listar Médicos
                print("\n--- Selecionar Médico para Remoção ---")
                medicos = medico_controller.listar_medicos(return_data=True)
                medico_opcoes = [(str(medico[0]), f"{medico[1]} ({medico[2]})") for medico in medicos]
                medico_id = selecionar_item("Selecione o Médico para Remover", medico_opcoes)

                if not medico_id:
                    print("Nenhum médico selecionado. Tente novamente.")
                    continue

                # Remover Médico
                medico_controller.remover_medico(ObjectId(medico_id))  # Converter para ObjectId
                print("Médico removido com sucesso!")

                continuar = input("Deseja remover outro médico? (s/n): ").strip().lower()
                if continuar != 's':
                    break

        elif choice == '2':  # Remover Paciente
            while True:
                # Listar Pacientes
                print("\n--- Selecionar Paciente para Remoção ---")
                pacientes = paciente_controller.listar_pacientes(return_data=True)
                paciente_opcoes = [(str(paciente[0]), f"{paciente[1]}") for paciente in pacientes]
                paciente_id = selecionar_item("Selecione o Paciente para Remover", paciente_opcoes)

                if not paciente_id:
                    print("Nenhum paciente selecionado. Tente novamente.")
                    continue

                # Remover Paciente
                paciente_controller.remover_paciente(ObjectId(paciente_id))  # Converter para ObjectId
                print("Paciente removido com sucesso!")

                continuar = input("Deseja remover outro paciente? (s/n): ").strip().lower()
                if continuar != 's':
                    break

        elif choice == '3':  # Remover Consulta
            while True:
                # Listar Consultas
                print("\n--- Selecionar Consulta para Remoção ---")
                consultas = consulta_controller.listar_consultas(return_data=True)
                consulta_opcoes = [(str(consulta[0]), f"Médico: {consulta[1]}, Paciente: {consulta[2]}, Data: {consulta[3]}") for consulta in consultas]
                consulta_id = selecionar_item("Selecione a Consulta para Remover", consulta_opcoes)

                if not consulta_id:
                    print("Nenhuma consulta selecionada. Tente novamente.")
                    continue

                # Remover Consulta
                consulta_controller.remover_consulta(ObjectId(consulta_id))  # Converter para ObjectId
                print("Consulta removida com sucesso!")

                continuar = input("Deseja remover outra consulta? (s/n): ").strip().lower()
                if continuar != 's':
                    break

        elif choice == '4':  # Voltar ao menu principal
            return

        else:
            print("Opção inválida. Por favor, tente novamente.")

def atualizar_registros(medico_controller, paciente_controller, consulta_controller):
    while True:
        print("\n--- Atualizar Registros ---")
        print("1. Atualizar Médico")
        print("2. Atualizar Paciente")
        print("3. Atualizar Consulta")
        print("4. Voltar ao menu principal")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            while True:
                medico_controller.listar_medicos()
                medico_id = input("ID do Médico a ser atualizado: ")
                nome = input("Novo nome (ou pressione Enter para manter o atual): ")
                especialidade = input("Nova especialidade (ou pressione Enter para manter a atual): ")
                telefone = input("Novo telefone (ou pressione Enter para manter o atual): ")
                medico_controller.atualizar_medico(medico_id, nome=nome, especialidade=especialidade, telefone=telefone)

                continuar = input("Deseja atualizar outro médico? (s/n): ").strip().lower()
                if continuar != 's':
                    break

        elif choice == '2':
            while True:
                paciente_controller.listar_pacientes()
                paciente_id = input("ID do Paciente a ser atualizado: ")
                nome = input("Novo nome (ou pressione Enter para manter o atual): ")
                telefone = input("Novo telefone (ou Enter para manter o atual): ")
                paciente_controller.atualizar_paciente(paciente_id, nome=nome, telefone=telefone)

                continuar = input("Deseja atualizar outro paciente? (s/n): ").strip().lower()
                if continuar != 's':
                    break

        elif choice == '3':
            while True:
                consulta_controller.listar_consultas()
                consulta_id = input("ID da Consulta a ser atualizada: ")
                data_consulta = input("Nova data (YYYY-MM-DD) (ou Enter para manter a atual): ")
                hora_consulta = input("Nova hora (HH:MM) (ou Enter para manter a atual): ")
                status = input("Novo status (ou Enter para manter o atual): ")
                consulta_controller.atualizar_consulta(consulta_id, data_consulta=data_consulta, hora_consulta=hora_consulta, status=status)

                continuar = input("Deseja atualizar outra consulta? (s/n): ").strip().lower()
                if continuar != 's':
                    break

        elif choice == '4':
            # Sai do menu de atualização e retorna ao menu principal
            return

        else:
            print("Opção inválida. Por favor, tente novamente.")

def listar_registros(medico_controller, paciente_controller, consulta_controller):
    while True:
        print("\n--- Listar Registros ---")
        print("1. Listar Médicos")
        print("2. Listar Pacientes")
        print("3. Listar Consultas")
        print("4. Voltar ao menu principal")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            medico_controller.listar_medicos()  # Lista médicos formatados
        elif choice == '2':
            paciente_controller.listar_pacientes()  # Lista pacientes formatados
        elif choice == '3':
            consulta_controller.listar_consultas()  # Lista consultas formatadas
        elif choice == '4':
            return
        else:
            print("Opção inválida. Por favor, tente novamente.")
            continue

        # Perguntar se deseja listar outro tipo de dado
        continuar = input("\nDeseja listar outro tipo de dado? (s/n): ").strip().lower()
        if continuar != 's':
            break

    print("\n--- Listar Registros ---")
    print("1. Listar Médicos")
    print("2. Listar Pacientes")
    print("3. Listar Consultas")
    choice = input("Escolha uma opção: ")

    if choice == '1':
        medicos = medico_controller.listar_medicos(return_data=True)
        if medicos:
            print(tabulate(medicos, headers=["ID", "Nome", "Especialidade", "Telefone"], tablefmt="grid"))
    
    elif choice == '2':
        pacientes = paciente_controller.listar_pacientes(return_data=True)
        if pacientes:
            print(tabulate(pacientes, headers=["ID", "Nome", "Telefone"], tablefmt="grid"))
    
    elif choice == '3':
        consulta_controller.listar_consultas()
    else:
        print("Opção inválida. Por favor, tente novamente.")
        
if __name__ == '__main__':
    main()
