import google.ds_python_interpreter

md_content = """# ☕ CafeSys - Cafeteria System

## 🧾 Descripción del Proyecto

**CafeSys** es una aplicación web diseñada para la gestión integral y eficiente de una cafetería. La plataforma facilita la interacción entre el negocio y sus consumidores, optimizando los procesos internos y mejorando la experiencia del usuario final.

### Funcionalidades Principales

* **Para Clientes:** Permite visualizar el menú actualizado en tiempo real y realizar pedidos de forma rápida y sencilla desde cualquier dispositivo.
* **Para Administradores:** Ofrece herramientas robustas para la gestión de pedidos, control exhaustivo de stock de productos y administración general de los recursos del negocio.

### Objetivos del Sistema
* 🚀 **Optimizar** la atención al cliente.
* ⏳ **Reducir** los tiempos de espera.
* 📊 **Mejorar** la organización interna mediante una interfaz accesible y moderna.

---

## 👥 Roles del Equipo

| Integrante | Rol | Responsabilidades |
| :--- | :--- | :--- |
| **Fredy José Aragón Carpio** | Desarrollador Backend | Programación de lógica de servidor y APIs. |
| **Gustavo Alonso Carrillo Villalta** | Administrador de Base de Datos | Diseño, gestión y optimización de datos. |
| **Diego Marcelo Arce Coaquira** | Desarrollador Frontend | Programación de interfaz de usuario y diseño UX/UI. |
| **José Manuel Bravo Rojas** | Desarrollador Fullstack | DevOps y soporte en ambas capas del desarrollo. |

---
*Este documento fue generado para la documentación técnica de CafeSys.*
"""

with open("CafeSys_Proyecto.md", "w", encoding="utf-8") as f:
    f.write(md_content)