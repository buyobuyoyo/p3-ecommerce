
from typing import Optional
from app.domain.ports import RespuestaAutomaticaPort


# Base de conocimiento — se puede mover a Supabase o a un archivo JSON
FAQ: list[dict] = [
    {
        "keywords": ["estado", "orden", "pedido", "renta"],
        "respuesta": (
            "Puedes consultar el estado de tu renta en la sección 'Mis pedidos'. "
            "Si el estado es 'activo', tu película está rentada. "
            "Si necesitas más ayuda, un asistente te atenderá pronto."
        ),
    },
    {
        "keywords": ["pago", "pagar", "método", "tarjeta", "efectivo"],
        "respuesta": (
            "Aceptamos tarjetas de crédito y débito (Visa, Mastercard). "
            "También puedes pagar en efectivo en sucursal."
        ),
    },
    {
        "keywords": ["envío", "entrega", "tiempo", "cuánto tarda", "demora"],
        "respuesta": (
            "Las películas digitales están disponibles inmediatamente tras el pago. "
            "No hay envío físico."
        ),
    },
    {
        "keywords": ["horario", "atención", "abierto", "horarios"],
        "respuesta": (
            "Nuestro soporte está disponible de lunes a viernes de 9:00 a 20:00 hrs. "
            "Fuera de ese horario, este asistente automático puede ayudarte."
        ),
    },
    {
        "keywords": ["devolucion", "devolución", "cancelar", "reembolso"],
        "respuesta": (
            "Las rentas pueden cancelarse dentro de las primeras 2 horas. "
            "Después de ese periodo no se realizan reembolsos. "
            "Contáctanos si tienes un caso especial."
        ),
    },
    {
        "keywords": ["precio", "costo", "cuánto cuesta", "cuanto"],
        "respuesta": (
            "El precio de cada película está visible en el catálogo. "
            "Todas las rentas tienen una duración de 7 días."
        ),
    },
    {
        "keywords": ["hola", "buenas", "buenos días", "buenas tardes", "buenas noches", "hey"],
        "respuesta": (
            "¡Hola! Soy el asistente automático de P3 E-commerce. "
            "Puedo ayudarte con preguntas sobre pedidos, pagos, horarios y más. "
            "¿En qué te puedo ayudar?"
        ),
    },
]


class FAQRepository(RespuestaAutomaticaPort):
    """
    Implementación del motor de respuestas mediante coincidencia de keywords.
    Desacoplado del resto del sistema a través de RespuestaAutomaticaPort.
    """

    def obtener_respuesta(self, texto: str) -> Optional[str]:
        texto_lower = texto.lower()
        for entrada in FAQ:
            for keyword in entrada["keywords"]:
                if keyword in texto_lower:
                    return entrada["respuesta"]
        
        return (
            "Lo siento, no logré entender tu consulta. "
            "¿Podrías intentar con palabras como 'precio', 'horario' o 'pedido'? "
            "De igual forma, un asistente humano revisará tu mensaje pronto."
        )