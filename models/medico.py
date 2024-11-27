class Medico:
    def __init__(self, nome, especialidade, telefone, _id=None):
        self._id = _id  # ID gerado pelo MongoDB
        self.nome = nome
        self.especialidade = especialidade
        self.telefone = telefone

    def to_dict(self):
        """Converte o objeto para um dicionário (para MongoDB)."""
        return {
            "_id": self._id,
            "nome": self.nome,
            "especialidade": self.especialidade,
            "telefone": self.telefone,
        }

    @staticmethod
    def from_dict(data):
        """Cria um objeto Medico a partir de um dicionário."""
        return Medico(
            _id=data.get("_id"),
            nome=data["nome"],
            especialidade=data["especialidade"],
            telefone=data["telefone"],
        )
