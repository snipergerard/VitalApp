#DROP DATABASE IF EXISTS vitalapp;
CREATE DATABASE vitalapp;
USE vitalapp;

-- Tabla de roles
CREATE TABLE Rol (
    idRol INT PRIMARY KEY AUTO_INCREMENT,
    Tipo_Rol VARCHAR(20) NOT NULL
);

-- Tabla de usuarios
CREATE TABLE Usuarios (
    idUsuario INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Correo VARCHAR(255) NOT NULL,
    Contraseña VARCHAR(255) NOT NULL,
    idRol INT,
    FOREIGN KEY (idRol) REFERENCES Rol(idRol)
);

-- Tabla de especialidades
CREATE TABLE Especialidad (
    idEspecialidad INT PRIMARY KEY AUTO_INCREMENT,
    Nombre_Especialidad VARCHAR(100) NOT NULL,
    Descripcion VARCHAR(255) NOT NULL
);

-- Tabla de médicos (vinculados a usuarios y especialidades)
CREATE TABLE Medicos (
    idMedico INT PRIMARY KEY AUTO_INCREMENT,
    idEspecialidad INT,
    idUsuario INT,
    Nombre_medico VARCHAR(100) NOT NULL,
    Telefono VARCHAR(15) NOT NULL,
    Correo VARCHAR(255) NOT NULL,
    FOREIGN KEY (idEspecialidad) REFERENCES Especialidad(idEspecialidad),
    FOREIGN KEY (idUsuario) REFERENCES Usuarios(idUsuario)
);

-- Tabla de pacientes (vinculados a usuarios)
CREATE TABLE Pacientes (
    idPaciente INT PRIMARY KEY AUTO_INCREMENT,
    idUsuario INT,
    Nombre_Paciente VARCHAR(100) NOT NULL,
    Fecha_nacimiento DATE NOT NULL,
    Genero VARCHAR(50) NOT NULL,
    Telefono VARCHAR(15) NOT NULL,
    Direccion VARCHAR(70) NOT NULL,
    Correo VARCHAR(255) NOT NULL,
    FOREIGN KEY (idUsuario) REFERENCES Usuarios(idUsuario)
);

-- Tabla de horarios
CREATE TABLE Horario (
    idHorario INT PRIMARY KEY AUTO_INCREMENT,
    Hora TIME NOT NULL,
    Disponible BOOLEAN DEFAULT TRUE
  
);

-- Tabla de citas
CREATE TABLE Citas (
    idCita INT PRIMARY KEY AUTO_INCREMENT,
    idPaciente INT,
    idMedico INT,
    idHorario INT,
    Fecha_cita DATETIME NOT NULL,
    Motivo_consulta VARCHAR(255),
    Estado VARCHAR(50) DEFAULT 'Pendiente',
    FOREIGN KEY (idPaciente) REFERENCES Pacientes(idPaciente),
    FOREIGN KEY (idMedico) REFERENCES Medicos(idMedico),
    FOREIGN KEY (idHorario) REFERENCES Horario(idHorario)
);

-- Tabla de tratamientos
CREATE TABLE Tratamientos (
    idTratamientos INT PRIMARY KEY AUTO_INCREMENT,
    idCita INT,
    Descripcion VARCHAR(255),
    Medicamentos VARCHAR(255),
    Dosis VARCHAR(100),
    Duracion VARCHAR(100),
    FOREIGN KEY (idCita) REFERENCES Citas(idCita)
);

CREATE TABLE HistorialMedico (
    idHistorial INT PRIMARY KEY AUTO_INCREMENT,
    idPaciente INT,
    Peso DECIMAL(5,2),
    Altura DECIMAL(5,2),
    GrupoSanguineo VARCHAR(5),
    EnfermedadesCronicas VARCHAR(255),
    Alergias VARCHAR(255),
    HistorialFamiliar VARCHAR(255),
    Habitos VARCHAR(255),
    EstadoGeneral VARCHAR(100),
    Observaciones TEXT,
    UltimaVisita DATE,
    FechaActualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (idPaciente) REFERENCES Pacientes(idPaciente)
);

