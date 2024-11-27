class Consulta:
    def __init__(self, medico_id, paciente_id, data_consulta, hora_consulta, status, _id=None):
        self._id = _id  # ID gerado pelo MongoDB
        self.medico_id = medico_id
        self.paciente_id = paciente_id
        self.data_consulta = data_consulta
        self.hora_consulta = hora_consulta
        self.status = status

    def to_dict(self):
        """Converte o objeto para um dicionário (para MongoDB)."""
        return {
            "_id": self._id,
            "medico_id": self.medico_id,
            "paciente_id": self.paciente_id,
            "data_consulta": self.data_consulta,
            "hora_consulta": self.hora_consulta,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data):
        """Cria um objeto Consulta a partir de um dicionário."""
        return Consulta(
            _id=data.get("_id"),
            medico_id=data["medico_id"],
            paciente_id=data["paciente_id"],
            data_consulta=data["data_consulta"],
            hora_consulta=data["hora_consulta"],
            status=data["status"],
        )
