CREATE DATABASE vitalapp;
USE vitalapp;

CREATE TABLE Rol (
    idRol INT PRIMARY KEY AUTO_INCREMENT,
    Tipo_Rol VARCHAR(20) NOT NULL
);

CREATE TABLE Usuarios (
    idUsuario INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Correo VARCHAR(255) NOT NULL,
    Contraseña VARCHAR(255) NOT NULL,
    idRol INT,
    FOREIGN KEY (idRol) REFERENCES Rol(idRol)
);

CREATE TABLE Medicos (
    idMedico INT PRIMARY KEY AUTO_INCREMENT,
    Nombre_medico VARCHAR(100) NOT NULL,
    Telefono VARCHAR(15) NOT NULL,
    Correo VARCHAR(255) NOT NULL
    -- Puedes agregar idUsuario si quieres vincular con la tabla Usuarios
);

CREATE TABLE Pacientes (
    idPaciente INT PRIMARY KEY AUTO_INCREMENT,
    Nombre_Paciente VARCHAR(100) NOT NULL,
    Fecha_nacimiento DATE NOT NULL,
    Genero VARCHAR(50) NOT NULL,
    Telefono VARCHAR(15) NOT NULL,
    Direccion VARCHAR(70) NOT NULL,
    Correo VARCHAR(255) NOT NULL
    -- Puedes agregar idUsuario si quieres vincular con la tabla Usuarios
);

CREATE TABLE Citas (
    idCita INT PRIMARY KEY AUTO_INCREMENT,
    idPaciente INT,
    idMedico INT,
    Fecha_cita DATETIME NOT NULL,
    Motivo_consulta VARCHAR(255),
    Estado VARCHAR(50) DEFAULT 'Pendiente',
    FOREIGN KEY (idPaciente) REFERENCES Pacientes(idPaciente),
    FOREIGN KEY (idMedico) REFERENCES Medicos(idMedico)
);

CREATE TABLE Tratamientos (
    idTratamientos INT PRIMARY KEY AUTO_INCREMENT,
    idCita INT,
    Descripcion VARCHAR(255),
    Medicamentos VARCHAR(255),
    Dosis VARCHAR(100),
    Duracion VARCHAR(100),
    FOREIGN KEY (idCita) REFERENCES Citas(idCita)
);