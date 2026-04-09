-- =====================================
-- CREACION DE LA BASE DE DATOS
-- =====================================
CREATE DATABASE IF NOT EXISTS sistema_tareas;
USE sistema_tareas;

-- =====================================
-- TABLA USUARIO
-- =====================================
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    tipo ENUM('estudiante', 'docente') NOT NULL
);

-- =====================================
-- TABLA CURSO
-- =====================================
CREATE TABLE IF NOT EXISTS curso (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_curso VARCHAR(100) NOT NULL,
    id_docente INT,

    FOREIGN KEY (id_docente) REFERENCES usuario(id_usuario)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- =====================================
-- TABLA TAREA
-- =====================================
CREATE TABLE IF NOT EXISTS tarea (
    id_tarea INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    fecha_limite DATE NOT NULL,
    id_curso INT NOT NULL,

    FOREIGN KEY (id_curso) REFERENCES curso(id_curso)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =====================================
-- TABLA ENTREGA
-- =====================================
CREATE TABLE IF NOT EXISTS entrega (
    id_entrega INT AUTO_INCREMENT PRIMARY KEY,
    archivo VARCHAR(255),
    fecha_entrega DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) DEFAULT 'enviado',
    nota DECIMAL(5,2),

    id_tarea INT NOT NULL,
    id_usuario INT NOT NULL,

    FOREIGN KEY (id_tarea) REFERENCES tarea(id_tarea)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);