class Paciente:
    def __init__(self, nome, telefone, _id=None):
        self._id = _id  # ID gerado pelo MongoDB
        self.nome = nome
        self.telefone = telefone

    def to_dict(self):
        """Converte o objeto para um dicionário (para MongoDB)."""
        return {
            "_id": self._id,
            "nome": self.nome,
            "telefone": self.telefone,
        }

    @staticmethod
    def from_dict(data):
        """Cria um objeto Paciente a partir de um dicionário."""
        return Paciente(
            _id=data.get("_id"),
            nome=data["nome"],
            telefone=data["telefone"],
        )
