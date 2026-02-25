-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 17-02-2026 a las 20:50:02
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `varchate_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `avatars`
--

CREATE TABLE `avatars` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `avatars`
--

INSERT INTO `avatars` (`id`, `nombre`, `created_at`, `updated_at`) VALUES
(1, 'avatar_01', NULL, NULL),
(2, 'avatar_02', NULL, NULL),
(3, 'avatar_03', NULL, NULL),
(4, 'avatar_04', NULL, NULL),
(5, 'avatar_05', NULL, NULL),
(6, 'avatar_06', NULL, NULL),
(7, 'avatar_07', NULL, NULL),
(8, 'avatar_08', NULL, NULL),
(9, 'avatar_09', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `certificaciones`
--

CREATE TABLE `certificaciones` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `usuario_id` bigint(20) UNSIGNED NOT NULL,
  `modulo_id` bigint(20) UNSIGNED NOT NULL,
  `intento_evaluacion_id` bigint(20) UNSIGNED NOT NULL,
  `codigo_certificado` varchar(100) NOT NULL,
  `porcentaje_obtenido` decimal(5,2) NOT NULL,
  `fecha_emision` datetime NOT NULL,
  `fecha_descarga` datetime DEFAULT NULL,
  `descargado` tinyint(1) DEFAULT 0,
  `hash_verificacion` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `certificaciones`
--

INSERT INTO `certificaciones` (`id`, `usuario_id`, `modulo_id`, `intento_evaluacion_id`, `codigo_certificado`, `porcentaje_obtenido`, `fecha_emision`, `fecha_descarga`, `descargado`, `hash_verificacion`, `created_at`, `updated_at`) VALUES
(1, 10, 1, 2, 'CERT-HTML-0010', 92.50, '2026-02-02 17:30:00', '2026-02-07 23:45:38', 1, '1a5d2dfb443d1338fa28506ccb86c2eb916801318f155fa299aacf25c7288e7f', '2026-02-02 22:30:00', '2026-02-08 00:28:13'),
(4, 11, 2, 9, 'CERT-CSS-20260208-0011', 100.00, '2026-02-08 20:27:04', '2026-02-08 20:28:59', 1, 'c39c96f14ccd315c40dc8b5a74bab0c825babc72aebdbe8fd7a3bfaa5c43c913', '2026-02-09 01:27:04', '2026-02-09 01:28:59'),
(5, 11, 1, 10, 'CERT-HTML-20260208-0011', 88.89, '2026-02-08 20:34:03', NULL, 0, '3255431890f1df6c7619a9edde1ab63b7a94f633fd7db21793aad412769241c5', '2026-02-09 01:34:03', '2026-02-09 01:34:03');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `codigo_usuario`
--

CREATE TABLE `codigo_usuario` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `usuario_id` bigint(20) UNSIGNED NOT NULL,
  `leccion_id` bigint(20) UNSIGNED NOT NULL,
  `codigo` text NOT NULL,
  `lenguaje` varchar(50) NOT NULL,
  `ejecuciones` int(11) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `codigo_usuario`
--

INSERT INTO `codigo_usuario` (`id`, `usuario_id`, `leccion_id`, `codigo`, `lenguaje`, `ejecuciones`, `created_at`, `updated_at`) VALUES
(1, 6, 2, '<!DOCTYPE html>\n<html>\n<head>\n    <title>Mi primera página</title>\n</head>\n<body>\n    <h1>¡Hola Mundo!</h1>\n    <p>Esta es mi primera página HTML.</p>\n</body>\n</html>', 'html', 5, '2026-02-02 14:00:00', '2026-02-02 14:00:00'),
(2, 6, 3, '<!DOCTYPE html>\n<html>\n<body>\n    <h1>Mi sitio web</h1>\n    <p>Bienvenido a mi página.</p>\n    <a href=\"https://www.ejemplo.com\">Visitar ejemplo</a>\n    <img src=\"imagen.jpg\" alt=\"Descripción\">\n</body>\n</html>', 'html', 3, '2026-02-02 14:30:00', '2026-02-02 14:30:00'),
(3, 6, 5, '<form action=\"/procesar\" method=\"POST\">\n    <label for=\"nombre\">Nombre:</label>\n    <input type=\"text\" id=\"nombre\" name=\"nombre\">\n    <br>\n    <label for=\"email\">Email:</label>\n    <input type=\"email\" id=\"email\" name=\"email\">\n    <br>\n    <input type=\"submit\" value=\"Enviar\">\n</form>', 'html', 7, '2026-02-02 15:00:00', '2026-02-02 15:00:00'),
(5, 10, 3, '<!DOCTYPE html>\n<html>\n<body>\n    <h1>Proyecto Final</h1>\n    <p>Este es mi proyecto completo.</p>\n    <a href=\"contacto.html\">Contacto</a>\n    <img src=\"logo.png\" alt=\"Logo\">\n    <ul>\n        <li>Item 1</li>\n        <li>Item 2</li>\n    </ul>\n</body>\n</html>', 'html', 5, '2026-02-02 15:15:00', '2026-02-02 15:15:00'),
(6, 10, 5, '<form action=\"/contacto\" method=\"POST\">\n    <h2>Formulario de Contacto</h2>\n    <label for=\"nombre\">Nombre completo:</label>\n    <input type=\"text\" id=\"nombre\" name=\"nombre\" required>\n    <br>\n    <label for=\"mensaje\">Mensaje:</label>\n    <textarea id=\"mensaje\" name=\"mensaje\" rows=\"4\"></textarea>\n    <br>\n    <button type=\"submit\">Enviar mensaje</button>\n</form>', 'html', 3, '2026-02-02 17:10:00', '2026-02-02 17:10:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ejercicios`
--

CREATE TABLE `ejercicios` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `leccion_id` bigint(20) UNSIGNED NOT NULL,
  `pregunta` text NOT NULL,
  `tipo` enum('seleccion_multiple','verdadero_falso','arrastrar_soltar') NOT NULL,
  `orden` int(11) DEFAULT 0,
  `estado` enum('activo','inactivo') DEFAULT 'activo',
  `created_by` bigint(20) UNSIGNED NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `ejercicios`
--

INSERT INTO `ejercicios` (`id`, `leccion_id`, `pregunta`, `tipo`, `orden`, `estado`, `created_by`, `created_at`, `updated_at`) VALUES
(1, 1, '¿Qué significa HTML?', 'seleccion_multiple', 1, 'activo', 6, '2026-02-01 15:35:00', '2026-02-01 15:35:00'),
(2, 1, 'HTML es un lenguaje de programación', 'verdadero_falso', 3, 'activo', 6, '2026-02-01 15:36:00', '2026-02-14 04:22:22'),
(3, 1, 'Relaciona los términos con sus definiciones', 'arrastrar_soltar', 4, 'activo', 6, '2026-02-01 15:37:00', '2026-02-14 04:22:22'),
(4, 2, '¿Cuál es la etiqueta raíz de un documento HTML5?', 'seleccion_multiple', 1, 'activo', 6, '2026-02-01 16:05:00', '2026-02-01 16:05:00'),
(5, 2, 'La etiqueta <title> va dentro de <body>', 'verdadero_falso', 2, 'activo', 6, '2026-02-01 16:06:00', '2026-02-01 16:06:00'),
(6, 3, '¿Cuál etiqueta se usa para crear un enlace?', 'seleccion_multiple', 1, 'activo', 6, '2026-02-01 16:35:00', '2026-02-01 16:35:00'),
(7, 3, 'Para imágenes se usa la etiqueta <img>', 'verdadero_falso', 2, 'activo', 6, '2026-02-01 16:36:00', '2026-02-01 16:36:00'),
(8, 3, '¿Cuál es el encabezado de mayor importancia?', 'seleccion_multiple', 3, 'activo', 6, '2026-02-01 16:37:00', '2026-02-01 16:37:00'),
(9, 3, 'Relaciona las etiquetas con su función', 'arrastrar_soltar', 4, 'activo', 6, '2026-02-01 16:38:00', '2026-02-01 16:38:00'),
(10, 5, '¿Qué atributo define la acción del formulario?', 'seleccion_multiple', 1, 'activo', 6, '2026-02-01 17:35:00', '2026-02-01 17:35:00'),
(11, 5, 'Los formularios solo pueden usar método GET', 'verdadero_falso', 2, 'activo', 6, '2026-02-01 17:36:00', '2026-02-01 17:36:00'),
(12, 5, 'Relaciona los tipos de input con su propósito', 'arrastrar_soltar', 3, 'activo', 6, '2026-02-01 17:37:00', '2026-02-01 17:37:00'),
(13, 1, 'suma', 'arrastrar_soltar', 2, 'activo', 11, '2026-02-14 04:20:32', '2026-02-14 04:22:22');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `evaluaciones`
--

CREATE TABLE `evaluaciones` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `modulo_id` bigint(20) UNSIGNED NOT NULL,
  `titulo` varchar(255) NOT NULL DEFAULT 'Evaluación Final',
  `descripcion` text DEFAULT NULL,
  `numero_preguntas` int(11) NOT NULL DEFAULT 10,
  `tiempo_limite` int(11) NOT NULL COMMENT 'Minutos',
  `puntaje_minimo` decimal(5,2) NOT NULL DEFAULT 70.00,
  `max_intentos` int(11) DEFAULT 3,
  `estado` enum('activo','inactivo') DEFAULT 'activo',
  `created_by` bigint(20) UNSIGNED NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `evaluaciones`
--

INSERT INTO `evaluaciones` (`id`, `modulo_id`, `titulo`, `descripcion`, `numero_preguntas`, `tiempo_limite`, `puntaje_minimo`, `max_intentos`, `estado`, `created_by`, `created_at`, `updated_at`) VALUES
(1, 1, 'Evaluación Final de HTML', 'Evalúa tus conocimientos sobre HTML5, estructura básica, etiquetas esenciales y formularios.', 10, 30, 80.00, 3, 'activo', 11, '2026-02-01 18:00:00', '2026-02-14 03:41:06'),
(2, 2, 'Evaluación Final de CSS', 'Evalúa tus conocimientos sobre selectores, propiedades y box model en CSS.', 8, 25, 75.00, 3, 'activo', 6, '2026-02-03 17:30:00', '2026-02-03 17:30:00'),
(3, 3, 'Prueba 1', 'ejercicos', 1, 30, 70.00, 3, 'activo', 11, '2026-02-14 03:29:44', '2026-02-14 03:57:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `intentos_ejercicios`
--

CREATE TABLE `intentos_ejercicios` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `usuario_id` bigint(20) UNSIGNED NOT NULL,
  `ejercicio_id` bigint(20) UNSIGNED NOT NULL,
  `opcion_seleccionada_id` bigint(20) UNSIGNED DEFAULT NULL,
  `respuesta_texto` text DEFAULT NULL,
  `es_correcta` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `intentos_ejercicios`
--

INSERT INTO `intentos_ejercicios` (`id`, `usuario_id`, `ejercicio_id`, `opcion_seleccionada_id`, `respuesta_texto`, `es_correcta`, `created_at`) VALUES
(1, 6, 1, 1, NULL, 1, '2026-02-02 13:31:00'),
(2, 6, 2, 5, NULL, 1, '2026-02-02 13:32:00'),
(3, 6, 4, 9, NULL, 1, '2026-02-02 14:01:00'),
(4, 6, 5, 13, NULL, 1, '2026-02-02 14:02:00'),
(5, 6, 6, 14, NULL, 1, '2026-02-02 14:31:00'),
(6, 6, 7, 17, NULL, 1, '2026-02-02 14:32:00'),
(7, 6, 8, 19, NULL, 1, '2026-02-02 14:33:00'),
(15, 10, 1, 1, NULL, 1, '2026-02-02 13:05:00'),
(16, 10, 2, 5, NULL, 1, '2026-02-02 13:06:00'),
(17, 10, 4, 9, NULL, 1, '2026-02-02 14:05:00'),
(18, 10, 5, 13, NULL, 1, '2026-02-02 14:06:00'),
(19, 10, 6, 14, NULL, 1, '2026-02-02 15:05:00'),
(20, 10, 7, 17, NULL, 1, '2026-02-02 15:06:00'),
(21, 10, 8, 19, NULL, 1, '2026-02-02 15:07:00'),
(22, 10, 10, 25, NULL, 1, '2026-02-02 17:05:00'),
(23, 10, 11, 29, NULL, 1, '2026-02-02 17:06:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `intentos_evaluacion`
--

CREATE TABLE `intentos_evaluacion` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `usuario_id` bigint(20) UNSIGNED NOT NULL,
  `evaluacion_id` bigint(20) UNSIGNED NOT NULL,
  `intento_numero` int(11) NOT NULL,
  `fecha_inicio` datetime NOT NULL,
  `fecha_fin` datetime DEFAULT NULL,
  `tiempo_utilizado` int(11) DEFAULT NULL COMMENT 'Segundos',
  `puntuacion_total` decimal(5,2) DEFAULT 0.00,
  `porcentaje_obtenido` decimal(5,2) DEFAULT 0.00,
  `preguntas_correctas` int(11) DEFAULT 0,
  `preguntas_incorrectas` int(11) DEFAULT 0,
  `aprobado` tinyint(1) DEFAULT 0,
  `estado` enum('en_progreso','completado','expirado') DEFAULT 'en_progreso',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `intentos_evaluacion`
--

INSERT INTO `intentos_evaluacion` (`id`, `usuario_id`, `evaluacion_id`, `intento_numero`, `fecha_inicio`, `fecha_fin`, `tiempo_utilizado`, `puntuacion_total`, `porcentaje_obtenido`, `preguntas_correctas`, `preguntas_incorrectas`, `aprobado`, `estado`, `created_at`, `updated_at`) VALUES
(1, 6, 1, 1, '2026-02-02 11:00:00', '2026-02-02 16:30:00', 1800, 85.00, 85.00, 8, 2, 1, 'completado', '2026-02-02 16:00:00', '2026-02-02 21:30:00'),
(2, 10, 1, 1, '2026-02-02 16:00:00', '2026-02-02 16:25:00', 1500, 92.50, 92.50, 9, 1, 1, 'completado', '2026-02-02 21:00:00', '2026-02-02 21:25:00'),
(9, 11, 2, 1, '2026-02-08 20:15:19', '2026-02-08 20:17:07', -108, 20.00, 100.00, 2, 0, 1, 'completado', '2026-02-09 01:15:19', '2026-02-09 01:17:07'),
(10, 11, 1, 1, '2026-02-08 20:30:03', '2026-02-08 20:31:55', -113, 80.00, 88.89, 8, 1, 1, 'completado', '2026-02-09 01:30:03', '2026-02-09 01:31:55');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lecciones`
--

CREATE TABLE `lecciones` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `modulo_id` bigint(20) UNSIGNED NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `contenido` longtext NOT NULL,
  `orden` int(11) DEFAULT 0,
  `tiene_editor_codigo` tinyint(1) DEFAULT 0,
  `tiene_ejercicios` tinyint(1) DEFAULT 0,
  `cantidad_ejercicios` int(11) DEFAULT 0,
  `estado` enum('activo','inactivo') DEFAULT 'activo',
  `created_by` bigint(20) UNSIGNED NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `lecciones`
--

INSERT INTO `lecciones` (`id`, `modulo_id`, `titulo`, `slug`, `contenido`, `orden`, `tiene_editor_codigo`, `tiene_ejercicios`, `cantidad_ejercicios`, `estado`, `created_by`, `created_at`, `updated_at`) VALUES
(1, 1, '¿Qué es HTML?', 'que-es-html', '<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14px; font-weight:400; font-style:normal;\">\n<h1 align=\"center\" style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:20pt; font-weight:600; color:#ff0004;\">Introducción a HTML</span></h1>\n<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Sans Serif\'; font-size:18pt;\">HTML (HyperText Markup Language) es el lenguaje estándar para crear páginas web. Describe la estructura de una página web mediante etiquetas (tags).</span><img src=\"placeholder.jpg\" alt=\"Imagen\" /></p>\n<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-style:italic;\">HTML no es un lenguaje de programación, sino de marcado que define la estructura del contenido.</span></p></body></html>', 1, 0, 1, 4, 'activo', 6, '2026-02-01 15:30:00', '2026-02-14 04:22:22'),
(2, 1, 'Estructura básica de un documento HTML', 'estructura-basica-html', '<h1>Estructura básica</h1><p>Todas las páginas HTML tienen una estructura básica:</p><pre>&lt;!DOCTYPE html&gt;<br>&lt;html&gt;<br>&lt;head&gt;<br>  &lt;title&gt;Título de la página&lt;/title&gt;<br>&lt;/head&gt;<br>&lt;body&gt;<br>  &lt;h1&gt;Mi primera página&lt;/h1&gt;<br>&lt;/body&gt;<br>&lt;/html&gt;</pre>', 2, 1, 1, 2, 'activo', 6, '2026-02-01 16:00:00', '2026-02-01 16:00:00'),
(3, 1, 'Etiquetas HTML esenciales', 'etiquetas-html-esenciales', '<h1>Etiquetas esenciales</h1><p>Algunas etiquetas básicas que debes conocer:</p><ul><li><strong>&lt;h1&gt; a &lt;h6&gt;</strong>: Encabezados</li><li><strong>&lt;p&gt;</strong>: Párrafos</li><li><strong>&lt;a&gt;</strong>: Enlaces</li><li><strong>&lt;img&gt;</strong>: Imágenes</li><li><strong>&lt;ul&gt;, &lt;ol&gt;, &lt;li&gt;</strong>: Listas</li></ul>', 3, 1, 1, 4, 'activo', 6, '2026-02-01 16:30:00', '2026-02-01 16:30:00'),
(4, 1, 'Atributos en HTML', 'atributos-html', '<h1>Atributos HTML</h1><p>Los atributos proporcionan información adicional sobre los elementos HTML.</p><p>Ejemplo:</p><pre>&lt;a href=\"https://www.ejemplo.com\" target=\"_blank\"&gt;Visitar sitio&lt;/a&gt;</pre><p>En este ejemplo, <code>href</code> y <code>target</code> son atributos.</p>', 4, 1, 0, 0, 'activo', 6, '2026-02-01 17:00:00', '2026-02-01 17:00:00'),
(5, 1, 'Formularios HTML', 'formularios-html', '<h1>Formularios HTML</h1><p>Los formularios permiten la interacción con el usuario:</p><pre>&lt;form action=\"/procesar\" method=\"POST\"&gt;<br>  &lt;label for=\"nombre\"&gt;Nombre:&lt;/label&gt;<br>  &lt;input type=\"text\" id=\"nombre\" name=\"nombre\"&gt;<br>  &lt;input type=\"submit\" value=\"Enviar\"&gt;<br>&lt;/form&gt;</pre>', 5, 1, 1, 3, 'activo', 6, '2026-02-01 17:30:00', '2026-02-01 17:30:00'),
(6, 2, '¿Qué es CSS?', 'que-es-css', '<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14px; font-weight:400; font-style:normal;\">\n<h1 style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:xx-large; font-weight:600;\">Introducción a CSS</span></h1>\n<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">CSS (Cascading Style Sheets) es el lenguaje utilizado para describir la presentación de documentos HTML.</p></body></html>', 1, 0, 0, 2, 'activo', 6, '2026-02-03 15:30:00', '2026-02-16 21:28:55'),
(7, 2, 'Selectores CSS', 'selectores-css', '<h1>Selectores CSS</h1><p>Los selectores permiten seleccionar elementos HTML para aplicar estilos.</p>', 2, 1, 1, 3, 'activo', 6, '2026-02-03 16:00:00', '2026-02-03 16:00:00'),
(8, 2, 'Propiedades de texto', 'propiedades-texto-css', '<h1>Propiedades de texto</h1><p>Aprende a controlar la apariencia del texto con CSS.</p>', 3, 1, 0, 0, 'activo', 6, '2026-02-03 16:30:00', '2026-02-03 16:30:00'),
(9, 2, 'Box Model', 'box-model-css', '<h1>Box Model</h1><p>El modelo de caja es fundamental para el diseño web con CSS.</p>', 4, 1, 1, 2, 'activo', 6, '2026-02-03 17:00:00', '2026-02-03 17:00:00'),
(10, 3, 'Prueba', 'prueba', '<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Hola prueba</p></body></html>', 1, 0, 0, 0, 'activo', 11, '2026-02-14 03:29:16', '2026-02-14 03:29:16');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `migrations`
--

CREATE TABLE `migrations` (
  `id` int(10) UNSIGNED NOT NULL,
  `migration` varchar(255) NOT NULL,
  `batch` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `migrations`
--

INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES
(213, '2026_01_23_215552_create_avatars_table', 1),
(214, '2026_01_24_200119_create_certificaciones_table', 1),
(215, '2026_01_24_200119_create_codigo_usuario_table', 1),
(216, '2026_01_24_200119_create_ejercicios_table', 1),
(217, '2026_01_24_200119_create_evaluaciones_table', 1),
(218, '2026_01_24_200119_create_intentos_ejercicios_table', 1),
(219, '2026_01_24_200119_create_intentos_evaluacion_table', 1),
(220, '2026_01_24_200119_create_lecciones_table', 1),
(221, '2026_01_24_200119_create_modulos_table', 1),
(222, '2026_01_24_200119_create_opciones_ejercicio_table', 1),
(223, '2026_01_24_200119_create_opciones_evaluacion_table', 1),
(224, '2026_01_24_200119_create_preguntas_evaluacion_table', 1),
(225, '2026_01_24_200119_create_progreso_lecciones_table', 1),
(226, '2026_01_24_200119_create_progreso_modulo_table', 1),
(227, '2026_01_24_200119_create_ranking_table', 1),
(228, '2026_01_24_200119_create_respuestas_evaluacion_table', 1),
(229, '2026_01_24_200119_create_usuarios_table', 1),
(230, '2026_01_24_200122_add_foreign_keys_to_certificaciones_table', 1),
(231, '2026_01_24_200122_add_foreign_keys_to_codigo_usuario_table', 1),
(232, '2026_01_24_200122_add_foreign_keys_to_ejercicios_table', 1),
(233, '2026_01_24_200122_add_foreign_keys_to_evaluaciones_table', 1),
(234, '2026_01_24_200122_add_foreign_keys_to_intentos_ejercicios_table', 1),
(235, '2026_01_24_200122_add_foreign_keys_to_intentos_evaluacion_table', 1),
(236, '2026_01_24_200122_add_foreign_keys_to_lecciones_table', 1),
(237, '2026_01_24_200122_add_foreign_keys_to_modulos_table', 1),
(238, '2026_01_24_200122_add_foreign_keys_to_opciones_ejercicio_table', 1),
(239, '2026_01_24_200122_add_foreign_keys_to_opciones_evaluacion_table', 1),
(240, '2026_01_24_200122_add_foreign_keys_to_preguntas_evaluacion_table', 1),
(241, '2026_01_24_200122_add_foreign_keys_to_progreso_lecciones_table', 1),
(242, '2026_01_24_200122_add_foreign_keys_to_progreso_modulo_table', 1),
(243, '2026_01_24_200122_add_foreign_keys_to_ranking_table', 1),
(244, '2026_01_24_200122_add_foreign_keys_to_respuestas_evaluacion_table', 1),
(245, '2026_01_24_205925_create_personal_access_tokens_table', 1),
(246, '2026_01_30_045853_create_sessions_table', 1),
(247, '2026_01_31_163541_create_password_reset_tokens_table', 1),
(248, '2026_02_01_235809_create_user_attempts_table', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modulos`
--

CREATE TABLE `modulos` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `descripcion_larga` longtext DEFAULT NULL,
  `modulo` enum('introduccion','html','css','javascript','php','sql') NOT NULL,
  `orden_global` int(11) DEFAULT 0,
  `estado` enum('activo','inactivo','borrador') DEFAULT 'borrador',
  `total_lecciones` int(11) DEFAULT 0,
  `created_by` bigint(20) UNSIGNED NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `modulos`
--

INSERT INTO `modulos` (`id`, `titulo`, `slug`, `descripcion_larga`, `modulo`, `orden_global`, `estado`, `total_lecciones`, `created_by`, `created_at`, `updated_at`) VALUES
(1, 'Introducción a HTML', 'introduccion-a-html', 'Aprende los fundamentos de HTML5, la estructura básica de una página web, etiquetas esenciales y buenas prácticas de desarrollo web. Este módulo te preparará para crear tus primeras páginas web desde cero.', 'html', 2, 'activo', 5, 6, '2026-02-01 15:00:00', '2026-02-01 15:00:00'),
(2, 'Introducción a CSS', 'introduccion-a-css', 'Aprende a dar estilo a tus páginas web con CSS3. Desde conceptos básicos hasta técnicas avanzadas de diseño responsivo y animaciones.', 'css', 3, 'activo', 4, 6, '2026-02-03 15:00:00', '2026-02-03 15:00:00'),
(3, 'prueba', 'prueba', 'prueba', 'html', 4, 'inactivo', 1, 11, '2026-02-14 03:00:08', '2026-02-16 21:31:30'),
(5, 'prueba 2', 'prueba-2', '<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14px; font-weight:400; font-style:normal;\">\n<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>', 'html', 5, 'activo', 0, 11, '2026-02-16 21:42:08', '2026-02-16 21:42:08'),
(6, 'prueba3', 'prueba3', '<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14px; font-weight:400; font-style:normal;\">\n<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>', 'html', 6, 'activo', 0, 11, '2026-02-16 21:50:26', '2026-02-16 21:50:26');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `opciones_ejercicio`
--

CREATE TABLE `opciones_ejercicio` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `ejercicio_id` bigint(20) UNSIGNED NOT NULL,
  `texto` text NOT NULL,
  `es_correcta` tinyint(1) DEFAULT 0,
  `orden` int(11) DEFAULT 0,
  `pareja_arrastre` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `opciones_ejercicio`
--

INSERT INTO `opciones_ejercicio` (`id`, `ejercicio_id`, `texto`, `es_correcta`, `orden`, `pareja_arrastre`, `created_at`) VALUES
(1, 1, 'HyperText Markup Language', 1, 1, NULL, '2026-02-01 15:35:00'),
(2, 1, 'HighTech Modern Language', 0, 2, NULL, '2026-02-01 15:35:00'),
(3, 1, 'HyperTransfer Markup Language', 0, 3, NULL, '2026-02-01 15:35:00'),
(4, 2, 'Verdadero', 0, 1, NULL, '2026-02-01 15:36:00'),
(5, 2, 'Falso', 1, 2, NULL, '2026-02-01 15:36:00'),
(6, 3, 'Etiqueta', 1, 1, 'Elemento HTML', '2026-02-01 15:37:00'),
(7, 3, 'Atributo', 1, 2, 'Información adicional', '2026-02-01 15:37:00'),
(8, 3, 'Elemento', 1, 3, 'Contenido con etiquetas', '2026-02-01 15:37:00'),
(9, 4, '<html>', 1, 1, NULL, '2026-02-01 16:05:00'),
(10, 4, '<body>', 0, 2, NULL, '2026-02-01 16:05:00'),
(11, 4, '<head>', 0, 3, NULL, '2026-02-01 16:05:00'),
(12, 5, 'Verdadero', 0, 1, NULL, '2026-02-01 16:06:00'),
(13, 5, 'Falso', 1, 2, NULL, '2026-02-01 16:06:00'),
(14, 6, '<a>', 1, 1, NULL, '2026-02-01 16:35:00'),
(15, 6, '<link>', 0, 2, NULL, '2026-02-01 16:35:00'),
(16, 6, '<href>', 0, 3, NULL, '2026-02-01 16:35:00'),
(17, 7, 'Verdadero', 1, 1, NULL, '2026-02-01 16:36:00'),
(18, 7, 'Falso', 0, 2, NULL, '2026-02-01 16:36:00'),
(19, 8, '<h1>', 1, 1, NULL, '2026-02-01 16:37:00'),
(20, 8, '<h6>', 0, 2, NULL, '2026-02-01 16:37:00'),
(21, 8, '<header>', 0, 3, NULL, '2026-02-01 16:37:00'),
(22, 9, '<p>', 1, 1, 'Párrafo', '2026-02-01 16:38:00'),
(23, 9, '<ul>', 1, 2, 'Lista no ordenada', '2026-02-01 16:38:00'),
(24, 9, '<h2>', 1, 3, 'Encabezado nivel 2', '2026-02-01 16:38:00'),
(25, 10, 'action', 1, 1, NULL, '2026-02-01 17:35:00'),
(26, 10, 'method', 0, 2, NULL, '2026-02-01 17:35:00'),
(27, 10, 'type', 0, 3, NULL, '2026-02-01 17:35:00'),
(28, 11, 'Verdadero', 0, 1, NULL, '2026-02-01 17:36:00'),
(29, 11, 'Falso', 1, 2, NULL, '2026-02-01 17:36:00'),
(30, 12, 'text', 1, 1, 'Texto simple', '2026-02-01 17:37:00'),
(31, 12, 'email', 1, 2, 'Correo electrónico', '2026-02-01 17:37:00'),
(32, 12, 'submit', 1, 3, 'Botón de envío', '2026-02-01 17:37:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `opciones_evaluacion`
--

CREATE TABLE `opciones_evaluacion` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `pregunta_evaluacion_id` bigint(20) UNSIGNED NOT NULL,
  `texto` text NOT NULL,
  `es_correcta` tinyint(1) DEFAULT 0,
  `orden` int(11) DEFAULT 0,
  `pareja_arrastre` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `opciones_evaluacion`
--

INSERT INTO `opciones_evaluacion` (`id`, `pregunta_evaluacion_id`, `texto`, `es_correcta`, `orden`, `pareja_arrastre`, `created_at`) VALUES
(1, 1, 'HyperText Markup Language', 1, 1, NULL, '2026-02-01 18:05:00'),
(2, 1, 'HighTech Modern Language', 0, 2, NULL, '2026-02-01 18:05:00'),
(3, 1, 'HyperTransfer Markup Language', 0, 3, NULL, '2026-02-01 18:05:00'),
(4, 2, 'Verdadero', 0, 1, NULL, '2026-02-01 18:06:00'),
(5, 2, 'Falso', 1, 2, NULL, '2026-02-01 18:06:00'),
(6, 3, '<html>', 1, 1, NULL, '2026-02-01 18:07:00'),
(7, 3, '<body>', 0, 2, NULL, '2026-02-01 18:07:00'),
(8, 3, '<head>', 0, 3, NULL, '2026-02-01 18:07:00'),
(9, 4, 'Verdadero', 0, 1, NULL, '2026-02-01 18:08:00'),
(10, 4, 'Falso', 1, 2, NULL, '2026-02-01 18:08:00'),
(11, 5, '<a>', 1, 1, NULL, '2026-02-01 18:09:00'),
(12, 5, '<link>', 0, 2, NULL, '2026-02-01 18:09:00'),
(13, 5, '<href>', 0, 3, NULL, '2026-02-01 18:09:00'),
(14, 6, '<p>', 1, 1, 'Párrafo', '2026-02-01 18:10:00'),
(15, 6, '<ul>', 1, 2, 'Lista no ordenada', '2026-02-01 18:10:00'),
(16, 6, '<h1>', 1, 3, 'Encabezado principal', '2026-02-01 18:10:00'),
(17, 7, 'action', 1, 1, NULL, '2026-02-01 18:11:00'),
(18, 7, 'method', 0, 2, NULL, '2026-02-01 18:11:00'),
(19, 7, 'type', 0, 3, NULL, '2026-02-01 18:11:00'),
(20, 8, 'Verdadero', 0, 1, NULL, '2026-02-01 18:12:00'),
(21, 8, 'Falso', 1, 2, NULL, '2026-02-01 18:12:00'),
(22, 9, '<h1>', 1, 1, NULL, '2026-02-01 18:13:00'),
(23, 9, '<h6>', 0, 2, NULL, '2026-02-01 18:13:00'),
(24, 9, '<header>', 0, 3, NULL, '2026-02-01 18:13:00'),
(27, 11, 'Cascading Style Sheets', 1, 1, NULL, '2026-02-08 20:15:16'),
(28, 11, 'Computer Style Sheets', 0, 2, NULL, '2026-02-08 20:15:16'),
(29, 11, 'Creative Style System', 0, 3, NULL, '2026-02-08 20:15:16'),
(30, 12, 'color', 1, 1, NULL, '2026-02-08 20:15:16'),
(31, 12, 'text-color', 0, 2, NULL, '2026-02-08 20:15:16'),
(32, 12, 'font-color', 0, 3, NULL, '2026-02-08 20:15:16'),
(33, 12, 'text-style', 0, 4, NULL, '2026-02-08 20:15:16'),
(34, 13, 'Verdadero', 0, 1, NULL, '2026-02-13 22:41:06'),
(35, 13, 'Falso', 0, 2, NULL, '2026-02-13 22:41:06'),
(36, 14, '1', 0, 1, NULL, '2026-02-13 22:57:00'),
(37, 14, '3', 0, 2, NULL, '2026-02-13 22:57:00'),
(38, 14, '2', 1, 3, NULL, '2026-02-13 22:57:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `password_reset_tokens`
--

INSERT INTO `password_reset_tokens` (`email`, `token`, `created_at`) VALUES
('varchate25@gmail.com', '$2y$12$4fjTnxl58H/ipUOKAAudou89Q.Q5Y6Y7SgBjZzhptcGppZxcGUTGK', '2026-02-02 06:23:25');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personal_access_tokens`
--

CREATE TABLE `personal_access_tokens` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `tokenable_type` varchar(255) NOT NULL,
  `tokenable_id` bigint(20) UNSIGNED NOT NULL,
  `name` text NOT NULL,
  `token` varchar(64) NOT NULL,
  `abilities` text DEFAULT NULL,
  `last_used_at` timestamp NULL DEFAULT NULL,
  `expires_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `personal_access_tokens`
--

INSERT INTO `personal_access_tokens` (`id`, `tokenable_type`, `tokenable_id`, `name`, `token`, `abilities`, `last_used_at`, `expires_at`, `created_at`, `updated_at`) VALUES
(1, 'App\\Models\\Usuario', 2, 'auth_token', '33d3b67c23e54f55fdb01cce2d561e3cee2837bc9829ba7ec97958a7a302b059', '[\"*\"]', NULL, NULL, '2026-02-02 06:40:00', '2026-02-02 06:40:00'),
(2, 'App\\Models\\Usuario', 2, 'auth_token', 'b67a67f728746e99f217a100f0237886e4f684c79c02bd2c07ac691395a6d0ea', '[\"*\"]', NULL, NULL, '2026-02-02 06:54:47', '2026-02-02 06:54:47'),
(3, 'App\\Models\\Usuario', 2, 'auth_token', 'd50dbeb262283de4bf13825fb6e8ee4fec5e7ce8ba8822e2d0fa1a862626bf36', '[\"*\"]', NULL, NULL, '2026-02-02 06:54:51', '2026-02-02 06:54:51'),
(4, 'App\\Models\\Usuario', 2, 'auth_token', '398d2214e7c0eb528a34a49901434e0d49c71bc9484833b376d14528e7f71051', '[\"*\"]', '2026-02-02 07:30:49', NULL, '2026-02-02 07:04:55', '2026-02-02 07:30:49'),
(5, 'App\\Models\\Usuario', 11, 'auth_token', '629ef7d39d36a40bb1a513abf5628fef2446d53f4320112362516b9140b72013', '[\"*\"]', '2026-02-07 01:12:04', NULL, '2026-02-07 00:55:42', '2026-02-07 01:12:04'),
(6, 'App\\Models\\Usuario', 11, 'auth_token', '35944e2a1e16ebce8cbbe809bc04cd972f10681060deeccc2e2c407b3985798e', '[\"*\"]', '2026-02-07 02:01:26', NULL, '2026-02-07 01:12:54', '2026-02-07 02:01:26'),
(7, 'App\\Models\\Usuario', 11, 'auth_token', '79c1178c9afa3d4ce77236a3cc474e04513003cff25dbdae2b3207363ef42537', '[\"*\"]', '2026-02-07 02:02:28', NULL, '2026-02-07 02:01:31', '2026-02-07 02:02:28'),
(8, 'App\\Models\\Usuario', 11, 'auth_token', '37c430a35aaa8f10ce23704150f4647957459c5e009c7e5a50e0ff146b512966', '[\"*\"]', '2026-02-07 02:35:34', NULL, '2026-02-07 02:02:34', '2026-02-07 02:35:34'),
(9, 'App\\Models\\Usuario', 11, 'auth_token', '3e19cb1b4515b534aaf0193920d6c6d43526fc0eab543d12363f40243a4174ba', '[\"*\"]', '2026-02-08 05:51:48', NULL, '2026-02-07 02:35:45', '2026-02-08 05:51:48'),
(10, 'App\\Models\\Usuario', 11, 'auth_token', 'b9c970dfccc200063d6f398e540689a6e920f2f6f02000dd9ce68d189920ba6d', '[\"*\"]', '2026-02-09 01:34:03', NULL, '2026-02-08 22:32:00', '2026-02-09 01:34:03'),
(11, 'App\\Models\\Usuario', 11, 'auth_token', '2023c47a9581bdd471c14c6e761817e658055c32b29b2ab54097e60052a7ca31', '[\"*\"]', NULL, NULL, '2026-02-14 01:18:51', '2026-02-14 01:18:51'),
(12, 'App\\Models\\Usuario', 11, 'auth_token', 'b01c3f2b54c2ba0af3421cb936decee90f4a7aff44609c5cd641ba6c5e67114b', '[\"*\"]', NULL, NULL, '2026-02-14 01:20:17', '2026-02-14 01:20:17'),
(13, 'App\\Models\\Usuario', 11, 'auth_token', 'cb77a09cda26b1cd184ca4b9e21deac9e8adba322ed164ded87d810a71b74581', '[\"*\"]', NULL, NULL, '2026-02-14 01:21:25', '2026-02-14 01:21:25'),
(14, 'App\\Models\\Usuario', 11, 'auth_token', '4983e90a7a69ba33fd9722d9dd42930b6bfbfd80eb769d5ec88c502d2fd2483f', '[\"*\"]', '2026-02-14 01:26:57', NULL, '2026-02-14 01:26:55', '2026-02-14 01:26:57'),
(15, 'App\\Models\\Usuario', 11, 'auth_token', 'b0a88be3527906b8091112b58552d269a00fc8b5dd7c07fe535094ae8a42482b', '[\"*\"]', '2026-02-14 01:28:49', NULL, '2026-02-14 01:28:44', '2026-02-14 01:28:49'),
(16, 'App\\Models\\Usuario', 11, 'auth_token', 'a29d8ffe71c3e3132c5fcea3433623876579f478501c7e900828c18d1d9edc29', '[\"*\"]', '2026-02-14 01:31:23', NULL, '2026-02-14 01:31:00', '2026-02-14 01:31:23'),
(17, 'App\\Models\\Usuario', 11, 'auth_token', '108e1c12089f6216044c39b300e831336ae273238974cc6b75c58022e2798a03', '[\"*\"]', '2026-02-14 01:32:51', NULL, '2026-02-14 01:32:34', '2026-02-14 01:32:51'),
(18, 'App\\Models\\Usuario', 11, 'auth_token', '5e36af73ddd20fec71828b4965754f9ff080e2a2fc795e8831b286335bcb8b55', '[\"*\"]', '2026-02-14 01:37:03', NULL, '2026-02-14 01:36:48', '2026-02-14 01:37:03'),
(19, 'App\\Models\\Usuario', 11, 'auth_token', '34725534afb704b5688df43036cf6d2822034dd1501ed2986e783c93d6415e07', '[\"*\"]', '2026-02-14 01:38:34', NULL, '2026-02-14 01:38:20', '2026-02-14 01:38:34'),
(20, 'App\\Models\\Usuario', 11, 'auth_token', '599ccd8e5cfb2b26ff6284e3a164e02714020d364386dfef886fcdca8df8ee5f', '[\"*\"]', '2026-02-14 01:41:01', NULL, '2026-02-14 01:40:26', '2026-02-14 01:41:01'),
(21, 'App\\Models\\Usuario', 11, 'auth_token', '33358c894a0ce8f972d40c2139715c06391b06000c29388a871429cca8426b18', '[\"*\"]', NULL, NULL, '2026-02-14 01:43:44', '2026-02-14 01:43:44'),
(22, 'App\\Models\\Usuario', 11, 'auth_token', '9b26f21cba6a55c7157812c4284d20e99b541d0b288dabef773aa479b90bbeb5', '[\"*\"]', '2026-02-14 01:45:47', NULL, '2026-02-14 01:45:06', '2026-02-14 01:45:47'),
(23, 'App\\Models\\Usuario', 11, 'auth_token', 'ddc33ab8c4318772af6b6df59b4acae5407b4866a4b38ad129a81f408e9ea0e7', '[\"*\"]', '2026-02-14 01:49:06', NULL, '2026-02-14 01:48:31', '2026-02-14 01:49:06'),
(24, 'App\\Models\\Usuario', 11, 'auth_token', '5d19fb89b7d6083bf602579199096f9b3bbbfc74d18d5e672b2bb20bc1c699a3', '[\"*\"]', '2026-02-14 01:51:18', NULL, '2026-02-14 01:50:52', '2026-02-14 01:51:18'),
(25, 'App\\Models\\Usuario', 11, 'auth_token', 'b33869989e0abfe3050b0b42ca4eb2741ef8a42f28ec8c120626eafc43b2cf6f', '[\"*\"]', '2026-02-14 01:56:02', NULL, '2026-02-14 01:53:28', '2026-02-14 01:56:02'),
(26, 'App\\Models\\Usuario', 11, 'auth_token', '882c1c93db6c2d296ef4a8897d35e9be5fb071b7d57770ce3f37fe4948a933e1', '[\"*\"]', '2026-02-14 01:56:26', NULL, '2026-02-14 01:56:17', '2026-02-14 01:56:26'),
(27, 'App\\Models\\Usuario', 11, 'auth_token', '6894bee8c59fb01485728010baf31ac87c198d1b99c6b9d3ce04a362e7ee18bf', '[\"*\"]', '2026-02-14 01:58:49', NULL, '2026-02-14 01:58:14', '2026-02-14 01:58:49'),
(28, 'App\\Models\\Usuario', 11, 'auth_token', '0a9191f8a9daaafdf5365ddd1e85c1379214ac1fdd5e8bf278bdfdaf2af68200', '[\"*\"]', '2026-02-14 02:02:51', NULL, '2026-02-14 02:02:49', '2026-02-14 02:02:51'),
(29, 'App\\Models\\Usuario', 11, 'auth_token', '6e4c13cb562cbc252c3674102b63f92c31dfc02cce1f707c6ac3461ae030ff23', '[\"*\"]', '2026-02-14 02:03:59', NULL, '2026-02-14 02:03:57', '2026-02-14 02:03:59'),
(30, 'App\\Models\\Usuario', 11, 'auth_token', 'ded7a5b788767245629f0bfbf3fd2f71276e06ddefc9dd0406bc12d3771ad950', '[\"*\"]', '2026-02-14 02:04:47', NULL, '2026-02-14 02:04:37', '2026-02-14 02:04:47'),
(31, 'App\\Models\\Usuario', 11, 'auth_token', 'bc32e2032919a0c4ec12b33d0cd0225fab70d1ffa0a6fb67f0e2936f197693a6', '[\"*\"]', '2026-02-14 02:10:36', NULL, '2026-02-14 02:10:02', '2026-02-14 02:10:36'),
(32, 'App\\Models\\Usuario', 11, 'auth_token', 'acf69666f23a9ba3be4ad8ce03a74f8dfa19bf296bd5f120391007e99c000186', '[\"*\"]', '2026-02-14 02:11:19', NULL, '2026-02-14 02:11:12', '2026-02-14 02:11:19'),
(33, 'App\\Models\\Usuario', 11, 'auth_token', 'f7c6752c84677af69886f5788b0fdd1e7033753c9a6c17be6ac23d7c05875914', '[\"*\"]', '2026-02-14 02:13:20', NULL, '2026-02-14 02:13:13', '2026-02-14 02:13:20'),
(34, 'App\\Models\\Usuario', 11, 'auth_token', '9debebe8e735408f17d5c07c5692bbfc719a5d365f14ce55a03f264f87edde53', '[\"*\"]', '2026-02-14 02:15:42', NULL, '2026-02-14 02:13:37', '2026-02-14 02:15:42'),
(35, 'App\\Models\\Usuario', 11, 'auth_token', '2a988165ed024de426c9433075cd03aab50e68750f2b3180039bf570dcef0402', '[\"*\"]', '2026-02-14 02:19:27', NULL, '2026-02-14 02:18:52', '2026-02-14 02:19:27'),
(36, 'App\\Models\\Usuario', 11, 'auth_token', '3a568c0fbc025999847069db2486e267aab98d31bf241d84225355642fd4a7ef', '[\"*\"]', '2026-02-14 02:27:07', NULL, '2026-02-14 02:22:55', '2026-02-14 02:27:07'),
(37, 'App\\Models\\Usuario', 11, 'auth_token', '6c66522b55d93e551ac9aaec0ec9474d9b5ee4331b0845db6162721eea1cd299', '[\"*\"]', '2026-02-14 02:31:10', NULL, '2026-02-14 02:30:05', '2026-02-14 02:31:10'),
(38, 'App\\Models\\Usuario', 11, 'auth_token', '98d255ab9a5041d163cf70f1d6b9b048eeeebf335da1383e3d33d3737fa82db5', '[\"*\"]', '2026-02-14 02:35:18', NULL, '2026-02-14 02:34:51', '2026-02-14 02:35:18'),
(39, 'App\\Models\\Usuario', 11, 'auth_token', '11b8b961c82730a0abb5800db9960342f87a7c4af34a7f143955bcee66df177b', '[\"*\"]', '2026-02-14 02:37:45', NULL, '2026-02-14 02:36:56', '2026-02-14 02:37:45'),
(40, 'App\\Models\\Usuario', 11, 'auth_token', 'd4b10f34f321515f1e3a93770133d7e61383b78b0114873e7a9ccd9532d999ac', '[\"*\"]', '2026-02-14 02:38:30', NULL, '2026-02-14 02:38:11', '2026-02-14 02:38:30'),
(41, 'App\\Models\\Usuario', 11, 'auth_token', '619f288d5839378504acc5f55c08820797ba319ebf94729953298aa2ab728de0', '[\"*\"]', '2026-02-14 02:51:57', NULL, '2026-02-14 02:50:52', '2026-02-14 02:51:57'),
(42, 'App\\Models\\Usuario', 11, 'auth_token', 'b103d7a77abf405c0d93b2acfe14928e8cf1b797215d58628c4ff80964ab5c02', '[\"*\"]', '2026-02-14 02:53:32', NULL, '2026-02-14 02:53:13', '2026-02-14 02:53:32'),
(43, 'App\\Models\\Usuario', 11, 'auth_token', '380adbb300cc1974cdc9a3edd46f056bfa7ffe29419f80209dfe4db914120116', '[\"*\"]', '2026-02-14 03:00:20', NULL, '2026-02-14 02:58:45', '2026-02-14 03:00:20'),
(44, 'App\\Models\\Usuario', 11, 'auth_token', 'bb46194155d287d1a6bf15c4ced2dc9c5ff531270b393655b84eef74f5a95e55', '[\"*\"]', '2026-02-14 03:12:28', NULL, '2026-02-14 03:11:49', '2026-02-14 03:12:28'),
(45, 'App\\Models\\Usuario', 11, 'auth_token', '4155992a90e4b499f5a8fb0071b795e86763987aa7bbc99ef43a5c01838554b5', '[\"*\"]', '2026-02-14 03:14:38', NULL, '2026-02-14 03:13:03', '2026-02-14 03:14:38'),
(46, 'App\\Models\\Usuario', 11, 'auth_token', '5bee49982063752b447909ed482d247a810fb553f9bb1b61e9128002881ff28d', '[\"*\"]', '2026-02-14 03:16:15', NULL, '2026-02-14 03:15:07', '2026-02-14 03:16:15'),
(47, 'App\\Models\\Usuario', 11, 'auth_token', 'fd7cd76dc184a6a22cc57edbc18931b1b95c94e42d06507a954fd2abe7f19dfc', '[\"*\"]', '2026-02-14 03:21:09', NULL, '2026-02-14 03:20:50', '2026-02-14 03:21:09'),
(48, 'App\\Models\\Usuario', 11, 'auth_token', 'e3f2f1b27931db4921f3abe2987b6bdd20a583db691ec9c82ca91102d2e27371', '[\"*\"]', '2026-02-14 03:30:06', NULL, '2026-02-14 03:28:18', '2026-02-14 03:30:06'),
(49, 'App\\Models\\Usuario', 11, 'auth_token', '06b7b6f7bde243099606bf82ad997c846443543db2dc5a80b879d363c3cf50e0', '[\"*\"]', '2026-02-14 03:35:35', NULL, '2026-02-14 03:34:49', '2026-02-14 03:35:35'),
(50, 'App\\Models\\Usuario', 11, 'auth_token', '1613da5ebce9dcf461af2647062ae337f0a05a07b6c4c34ecb17f0f2fd5aa28e', '[\"*\"]', '2026-02-14 03:41:47', NULL, '2026-02-14 03:39:24', '2026-02-14 03:41:47'),
(51, 'App\\Models\\Usuario', 11, 'auth_token', '8e876b4b84cb4608930ac7c35fabcbb45eee8ef04656102189d9bc0ae83fd978', '[\"*\"]', '2026-02-14 03:43:09', NULL, '2026-02-14 03:42:04', '2026-02-14 03:43:09'),
(52, 'App\\Models\\Usuario', 11, 'auth_token', '7bbb3de955723cac2742fe4aeea8bdd296c2ab543ff9b71c69e5bcd40fee02af', '[\"*\"]', '2026-02-14 03:59:51', NULL, '2026-02-14 03:55:38', '2026-02-14 03:59:51'),
(53, 'App\\Models\\Usuario', 11, 'auth_token', '0f287b4301ebe6fa824c09f54c4e329a3dd2b49a8fc807e1c88223d9f2c3fab4', '[\"*\"]', '2026-02-14 04:05:48', NULL, '2026-02-14 04:03:12', '2026-02-14 04:05:48'),
(54, 'App\\Models\\Usuario', 11, 'auth_token', '1e380bdd46242ebaa7ede223bb0d46b8076e779df342fe7a8e6252af6f75d261', '[\"*\"]', '2026-02-14 04:17:29', NULL, '2026-02-14 04:15:24', '2026-02-14 04:17:29'),
(55, 'App\\Models\\Usuario', 11, 'auth_token', '0459c0e37cd39e2c577cabf19d284db8043141edcf1eb58ae561f542a919c1f0', '[\"*\"]', '2026-02-14 04:23:33', NULL, '2026-02-14 04:18:59', '2026-02-14 04:23:33'),
(56, 'App\\Models\\Usuario', 11, 'auth_token', '10dcee9af9a2e3fb33b6e76ebb470019cb24073c131ff028bfd674e35b3f3e8e', '[\"*\"]', '2026-02-14 04:36:37', NULL, '2026-02-14 04:35:32', '2026-02-14 04:36:37'),
(57, 'App\\Models\\Usuario', 11, 'auth_token', 'af892215323ba2adfc3cf73e37fc248eff7ea3c1bd0ac5af7f37fda5f97d4597', '[\"*\"]', '2026-02-14 04:37:56', NULL, '2026-02-14 04:37:21', '2026-02-14 04:37:56'),
(58, 'App\\Models\\Usuario', 11, 'auth_token', 'b56c49bbe4f2593aed52dcfd613e52b2de076e545c1ddd2cc5153132bffc755c', '[\"*\"]', '2026-02-14 04:45:44', NULL, '2026-02-14 04:43:39', '2026-02-14 04:45:44'),
(59, 'App\\Models\\Usuario', 11, 'auth_token', 'd4c4e94ebffc6f90abd00d9811f0a06ad10b5dc2417167c17e3794fe3a083a27', '[\"*\"]', '2026-02-14 04:47:56', NULL, '2026-02-14 04:47:42', '2026-02-14 04:47:56'),
(60, 'App\\Models\\Usuario', 11, 'auth_token', '699f3f12e8eb7d83233060fe16bf4c0d76d59988c40e9d08a63fe65277afdd6e', '[\"*\"]', '2026-02-14 04:52:04', NULL, '2026-02-14 04:50:58', '2026-02-14 04:52:04'),
(61, 'App\\Models\\Usuario', 11, 'auth_token', '49d9ee55fbab722bfd6979ab07b34adad5d46aad27af0ff7f1896a748f0fc477', '[\"*\"]', '2026-02-14 05:02:19', NULL, '2026-02-14 05:02:04', '2026-02-14 05:02:19'),
(62, 'App\\Models\\Usuario', 11, 'auth_token', 'f9078fd2274700ac17af1f912f004c2864ebbf8a65caa63a12a666db2140063d', '[\"*\"]', '2026-02-14 05:06:21', NULL, '2026-02-14 05:06:06', '2026-02-14 05:06:21'),
(63, 'App\\Models\\Usuario', 11, 'auth_token', '2fa6ea2b78e895c0387ad66489239b839a90fdadb16f6ba15cb8502f179bcc62', '[\"*\"]', '2026-02-14 05:08:14', NULL, '2026-02-14 05:07:08', '2026-02-14 05:08:14'),
(64, 'App\\Models\\Usuario', 11, 'auth_token', '9db60f05559a171d3c6b1ecfbcd2914f1e8b0fcbb9cbe2265432408b86d41125', '[\"*\"]', '2026-02-14 05:11:03', NULL, '2026-02-14 05:10:47', '2026-02-14 05:11:03'),
(65, 'App\\Models\\Usuario', 11, 'auth_token', '78de20a59e37b605c3637405f1e5b281ef246c6e0fdfb073e370ff2d259405fd', '[\"*\"]', '2026-02-14 05:12:58', NULL, '2026-02-14 05:12:43', '2026-02-14 05:12:58'),
(66, 'App\\Models\\Usuario', 11, 'auth_token', 'a05cce15c0dc74609f1d906746b09e47f6e0b79700264b415d2554396b2289fa', '[\"*\"]', '2026-02-14 05:15:18', NULL, '2026-02-14 05:15:03', '2026-02-14 05:15:18'),
(67, 'App\\Models\\Usuario', 11, 'auth_token', '6370becda02891c7386c46efb88709cc5d98746d4c8ae918852f04251a068a61', '[\"*\"]', '2026-02-14 05:15:56', NULL, '2026-02-14 05:15:40', '2026-02-14 05:15:56'),
(68, 'App\\Models\\Usuario', 11, 'auth_token', '8d25d18b0a8a85e16512c0b1dce6372171571fd0897be249178ab8ebec91535e', '[\"*\"]', '2026-02-14 05:19:02', NULL, '2026-02-14 05:18:46', '2026-02-14 05:19:02'),
(69, 'App\\Models\\Usuario', 11, 'auth_token', '5b8589f5ab04099734ce5efb5a1713fa17a2fca0ac1cad780d464b05d3d50334', '[\"*\"]', '2026-02-14 21:30:21', NULL, '2026-02-14 21:26:38', '2026-02-14 21:30:21'),
(70, 'App\\Models\\Usuario', 11, 'auth_token', '36fab414871170a09ac77e72cd52b204411316e78539f6d19413e2907303ea88', '[\"*\"]', '2026-02-15 22:02:32', NULL, '2026-02-15 22:02:15', '2026-02-15 22:02:32'),
(71, 'App\\Models\\Usuario', 11, 'auth_token', '291a6d2e6e2db195d36d0215bab88cec7298f1f719847035b49e298a06f6b1e0', '[\"*\"]', NULL, NULL, '2026-02-15 22:05:22', '2026-02-15 22:05:22'),
(72, 'App\\Models\\Usuario', 11, 'auth_token', 'a5affa23a470586e57a8148b87cfeb6977679149a2c61c71a8792b612aa6119d', '[\"*\"]', '2026-02-15 22:14:18', NULL, '2026-02-15 22:14:04', '2026-02-15 22:14:18'),
(73, 'App\\Models\\Usuario', 11, 'auth_token', '6f141a911488f76b5a9aeda1d42af1e9bf2e442b46aba3a7be6902de4df5a2d0', '[\"*\"]', '2026-02-15 22:17:17', NULL, '2026-02-15 22:16:41', '2026-02-15 22:17:17'),
(74, 'App\\Models\\Usuario', 11, 'auth_token', '00d1dae0390f8af2ac64ceb099401ac13e173b1b4d7445a07f3a9d6b5db11424', '[\"*\"]', '2026-02-15 22:21:54', NULL, '2026-02-15 22:20:31', '2026-02-15 22:21:54'),
(75, 'App\\Models\\Usuario', 11, 'auth_token', '7372a46f8e80aff2b4a6be0e2c541bf6e43e7282f204748232135c1055fe2c6c', '[\"*\"]', '2026-02-15 22:28:52', NULL, '2026-02-15 22:28:37', '2026-02-15 22:28:52'),
(76, 'App\\Models\\Usuario', 11, 'auth_token', 'b2fd74fe61add032d8b3a2ba9e1261d71cc73ba2037689e3a830480d0b85ffb4', '[\"*\"]', NULL, NULL, '2026-02-15 22:29:10', '2026-02-15 22:29:10'),
(77, 'App\\Models\\Usuario', 11, 'auth_token', '7d6550615479a0579d2d67384b7ffe35af4461e13929919b55eadbcb694c6fb9', '[\"*\"]', NULL, NULL, '2026-02-15 22:29:39', '2026-02-15 22:29:39'),
(78, 'App\\Models\\Usuario', 11, 'auth_token', '668bd6efc1b8cf7f33e726540c99c9d05a52c42d819567cc37524c9e5dfdd0f8', '[\"*\"]', NULL, NULL, '2026-02-15 22:31:44', '2026-02-15 22:31:44'),
(79, 'App\\Models\\Usuario', 11, 'auth_token', 'b6d8a3eb9c358498c7c87ea20271c3232baf7ead12bed6bf03c12126b547614d', '[\"*\"]', NULL, NULL, '2026-02-15 22:32:51', '2026-02-15 22:32:51'),
(80, 'App\\Models\\Usuario', 11, 'auth_token', '2607f4e9cd995159e80ea1d4b711a1f7f466864f0fc24bb033bd00927535182d', '[\"*\"]', NULL, NULL, '2026-02-15 22:39:36', '2026-02-15 22:39:36'),
(81, 'App\\Models\\Usuario', 11, 'auth_token', 'e77b46bb03ffe74fc484e5b19bb144e9908a442a1430d833890bb82990d40301', '[\"*\"]', NULL, NULL, '2026-02-15 22:40:17', '2026-02-15 22:40:17'),
(82, 'App\\Models\\Usuario', 11, 'auth_token', '919cce67e44cd6a68cf9b5e1671d8ac7ac1f03de4ca64af091df50e52e1169dd', '[\"*\"]', NULL, NULL, '2026-02-15 22:46:15', '2026-02-15 22:46:15'),
(83, 'App\\Models\\Usuario', 11, 'auth_token', 'beb08891cfbd621a6b87a2806ba7c837488467af93b785004a6c4304325f0557', '[\"*\"]', NULL, NULL, '2026-02-15 22:47:04', '2026-02-15 22:47:04'),
(84, 'App\\Models\\Usuario', 11, 'auth_token', '811250585b215864c842983c03bc8bca17f5517694d211648d366c854872f07e', '[\"*\"]', NULL, NULL, '2026-02-15 22:47:16', '2026-02-15 22:47:16'),
(85, 'App\\Models\\Usuario', 11, 'auth_token', '88babb561e0f726d0ca198f503c9124896b791358f080f89d64af650c14d9395', '[\"*\"]', NULL, NULL, '2026-02-15 22:47:39', '2026-02-15 22:47:39'),
(86, 'App\\Models\\Usuario', 11, 'auth_token', 'b904b5e91080267eed2664c6c493b3c4db614d47cb32092923557d15bef5ff6f', '[\"*\"]', NULL, NULL, '2026-02-15 22:54:18', '2026-02-15 22:54:18'),
(87, 'App\\Models\\Usuario', 11, 'auth_token', 'b09ed8c5404580161f9ef37c543ece6170e782f38ef71cdc0b05b653edfa0761', '[\"*\"]', NULL, NULL, '2026-02-15 22:56:24', '2026-02-15 22:56:24'),
(88, 'App\\Models\\Usuario', 11, 'auth_token', '868ff62582495e07d5dc0aff4395d486ca34fdf5960b5abaa55e150073996f44', '[\"*\"]', NULL, NULL, '2026-02-15 22:58:28', '2026-02-15 22:58:28'),
(89, 'App\\Models\\Usuario', 11, 'auth_token', 'dfdce99dd0455208b7a5d3c79e50d09334b06ef1bbf18c1cb31490824432e0c0', '[\"*\"]', NULL, NULL, '2026-02-15 22:59:17', '2026-02-15 22:59:17'),
(90, 'App\\Models\\Usuario', 11, 'auth_token', 'bb304fea78ffafc0ba76326c8e8accfb4d7c297a8192d8743154ae07e9240074', '[\"*\"]', NULL, NULL, '2026-02-15 23:01:30', '2026-02-15 23:01:30'),
(91, 'App\\Models\\Usuario', 11, 'auth_token', 'e949f084ebe01976ad3885b6e7a87cec9d5f0575a6af40e323ee7cad5eaf029f', '[\"*\"]', '2026-02-15 23:02:00', NULL, '2026-02-15 23:01:45', '2026-02-15 23:02:00'),
(92, 'App\\Models\\Usuario', 11, 'auth_token', 'a90252377366b0d7f8741eca23f145b891d1b14d1d178c8607648877061b6c20', '[\"*\"]', '2026-02-15 23:13:44', NULL, '2026-02-15 23:13:28', '2026-02-15 23:13:44'),
(93, 'App\\Models\\Usuario', 11, 'auth_token', '09eaf13a41111725fa1d2def12f50389da89a5f026196714f6e57d22dbec7511', '[\"*\"]', '2026-02-15 23:24:53', NULL, '2026-02-15 23:24:38', '2026-02-15 23:24:53'),
(94, 'App\\Models\\Usuario', 11, 'auth_token', '0e03082d2fb7ccf4bbfcbf25c6589e4a4df51d24e9c5efd1b4f9ed1f2f9b5fcb', '[\"*\"]', '2026-02-15 23:27:13', NULL, '2026-02-15 23:26:57', '2026-02-15 23:27:13'),
(95, 'App\\Models\\Usuario', 11, 'auth_token', '44b47fdaef3a85a2387222e02c034de623fdbe950324a85fe255a7aedc50d74f', '[\"*\"]', '2026-02-15 23:27:46', NULL, '2026-02-15 23:27:31', '2026-02-15 23:27:46'),
(96, 'App\\Models\\Usuario', 11, 'auth_token', '9cf76b5272e0cf84bc6e98272dd4a0a3465e2190034f9733353ab8699e702b92', '[\"*\"]', '2026-02-15 23:30:57', NULL, '2026-02-15 23:30:42', '2026-02-15 23:30:57'),
(97, 'App\\Models\\Usuario', 11, 'auth_token', '8e5a710ece0fe14ff60076b4324a4580d18839ed961450de80abf3fcacd0d221', '[\"*\"]', '2026-02-15 23:32:24', NULL, '2026-02-15 23:31:18', '2026-02-15 23:32:24'),
(98, 'App\\Models\\Usuario', 11, 'auth_token', 'e928cbb90478190b5f6826031d03a12532b4271b81ba208d3a65ebc4864c9fa4', '[\"*\"]', '2026-02-15 23:32:57', NULL, '2026-02-15 23:32:41', '2026-02-15 23:32:57'),
(99, 'App\\Models\\Usuario', 11, 'auth_token', 'dcf893b449c934415073e664a71721bd5dc75fffe077386df5998db823c0b21d', '[\"*\"]', '2026-02-15 23:34:27', NULL, '2026-02-15 23:34:12', '2026-02-15 23:34:27'),
(100, 'App\\Models\\Usuario', 11, 'auth_token', 'b3beb329998dffec4ddae809570730b37592fc20894328655541ba711c5b19f9', '[\"*\"]', '2026-02-15 23:57:20', NULL, '2026-02-15 23:57:04', '2026-02-15 23:57:20'),
(101, 'App\\Models\\Usuario', 11, 'auth_token', 'c934058351dbd534241144ba16f3211061ac8fceccc689376f6f6b908610e19b', '[\"*\"]', '2026-02-16 00:05:34', NULL, '2026-02-16 00:05:18', '2026-02-16 00:05:34'),
(102, 'App\\Models\\Usuario', 11, 'auth_token', '50b87633dc29729682c77085e46ae60d82743a1b02251fd7c0361c9757787c9c', '[\"*\"]', '2026-02-16 00:06:09', NULL, '2026-02-16 00:05:53', '2026-02-16 00:06:09'),
(103, 'App\\Models\\Usuario', 11, 'auth_token', 'cacd223b35e3a24dee8b63ddd1a668a5404c6aeac2930effac274b451b40da49', '[\"*\"]', '2026-02-16 00:09:28', NULL, '2026-02-16 00:09:13', '2026-02-16 00:09:28'),
(104, 'App\\Models\\Usuario', 11, 'auth_token', 'af5fb0ed05fbe7997e934264522b13cbdf9e5e511b66e0561246c2e2642093e7', '[\"*\"]', '2026-02-16 00:17:12', NULL, '2026-02-16 00:16:56', '2026-02-16 00:17:12'),
(105, 'App\\Models\\Usuario', 11, 'auth_token', 'cf0b7d261fd575b3f7fae45849bcdd9ae1e271f6e99ba7847895cf3455929723', '[\"*\"]', '2026-02-16 00:22:12', NULL, '2026-02-16 00:20:36', '2026-02-16 00:22:12'),
(106, 'App\\Models\\Usuario', 11, 'auth_token', 'e2d6df07e3d1ae249d1cc41503edf92f9b42222b73cbf9ab5ec50790876dd335', '[\"*\"]', '2026-02-16 00:22:52', NULL, '2026-02-16 00:22:37', '2026-02-16 00:22:52'),
(107, 'App\\Models\\Usuario', 11, 'auth_token', '525fd8fe0279745b0bbd47a855167958effb327a627d48432d04f04a24eda16c', '[\"*\"]', '2026-02-16 00:28:27', NULL, '2026-02-16 00:23:20', '2026-02-16 00:28:27'),
(108, 'App\\Models\\Usuario', 11, 'auth_token', 'd9e08f005fbf9432b77d9acdb879b6faaee711a070122dc2822e21e5d9ff7d36', '[\"*\"]', NULL, NULL, '2026-02-16 00:28:56', '2026-02-16 00:28:56'),
(109, 'App\\Models\\Usuario', 11, 'auth_token', '1bf4ff1417b843f867130f56bc5d81ca107966fb4f0c3622e9118731f299c335', '[\"*\"]', '2026-02-16 00:29:42', NULL, '2026-02-16 00:29:13', '2026-02-16 00:29:42'),
(110, 'App\\Models\\Usuario', 11, 'auth_token', 'b709db18cd1b0532f7cf2fceeb85c8a3fbf4e82e7ef3ecf8e84d7f237952d379', '[\"*\"]', '2026-02-16 00:31:41', NULL, '2026-02-16 00:31:23', '2026-02-16 00:31:41'),
(111, 'App\\Models\\Usuario', 11, 'auth_token', '3b78f388ef7ead9146463c4674d796204b69eb0931af5424ade257357b2f7772', '[\"*\"]', '2026-02-16 00:38:09', NULL, '2026-02-16 00:34:58', '2026-02-16 00:38:09'),
(112, 'App\\Models\\Usuario', 11, 'auth_token', '5f994b52a1ac8bf58c618c475f1d993191c5beb25b958716090e1794db1cc92c', '[\"*\"]', '2026-02-16 00:41:07', NULL, '2026-02-16 00:38:26', '2026-02-16 00:41:07'),
(113, 'App\\Models\\Usuario', 11, 'auth_token', '6f40d2656d8054b9e4882c104f3a9b4a4ebff7237e3622dbb2bf8971f0580d5a', '[\"*\"]', '2026-02-16 00:41:36', NULL, '2026-02-16 00:41:18', '2026-02-16 00:41:36'),
(114, 'App\\Models\\Usuario', 11, 'auth_token', 'b7e581d60f2630a7a6efd9a11ef932d03032997e0d815a6975b97982bc3d71a4', '[\"*\"]', '2026-02-16 00:44:57', NULL, '2026-02-16 00:44:16', '2026-02-16 00:44:57'),
(115, 'App\\Models\\Usuario', 11, 'auth_token', '5f0df1a898aff5223552f70b485b775fd143a019263b9b7b8ecef035db4b37b2', '[\"*\"]', '2026-02-16 00:45:51', NULL, '2026-02-16 00:45:33', '2026-02-16 00:45:51'),
(116, 'App\\Models\\Usuario', 11, 'auth_token', 'a0605ef2176a263f2e429fddcdd38b113a1b535bbcfe7791015ab6fe800b0bf9', '[\"*\"]', '2026-02-16 00:49:17', NULL, '2026-02-16 00:47:36', '2026-02-16 00:49:17'),
(117, 'App\\Models\\Usuario', 11, 'auth_token', 'f4b9a9dc44e5cb3809c4593b5b13afb38bf8e40e06f27d7703d11690d23e796b', '[\"*\"]', '2026-02-16 00:49:53', NULL, '2026-02-16 00:49:35', '2026-02-16 00:49:53'),
(118, 'App\\Models\\Usuario', 11, 'auth_token', 'd49207d9c131ae7f15529cf078eaba93f3cf1394060e4ce5de1389050fea1112', '[\"*\"]', '2026-02-16 00:51:06', NULL, '2026-02-16 00:50:25', '2026-02-16 00:51:06'),
(119, 'App\\Models\\Usuario', 11, 'auth_token', '431d101a69b6a03c04a13674d88d541f1aeb5b52d2d3e569b353066077b0fd17', '[\"*\"]', '2026-02-16 01:01:07', NULL, '2026-02-16 01:00:49', '2026-02-16 01:01:07'),
(120, 'App\\Models\\Usuario', 11, 'auth_token', 'c77865941e31065b0dc2efa9089e6e993cf903ed961cb1ce1bc18d2fb58a960b', '[\"*\"]', '2026-02-16 01:02:48', NULL, '2026-02-16 01:01:37', '2026-02-16 01:02:48'),
(121, 'App\\Models\\Usuario', 11, 'auth_token', 'aa8770a3ccdb784ec26ed8cd6d80ed13dc29b9ea57637378991a476d8b769cba', '[\"*\"]', '2026-02-16 01:03:22', NULL, '2026-02-16 01:03:04', '2026-02-16 01:03:22'),
(122, 'App\\Models\\Usuario', 11, 'auth_token', '22fc182d38a400106232af58a3e5b54f7e5b1d5920fb1a5a99fdf62861fcbd0c', '[\"*\"]', '2026-02-16 01:04:20', NULL, '2026-02-16 01:04:02', '2026-02-16 01:04:20'),
(123, 'App\\Models\\Usuario', 11, 'auth_token', 'bc9febf998a8e349b19f6dee92e9d07129ac0fd50f7b2cb87a965f9a89df5ed1', '[\"*\"]', '2026-02-16 01:05:00', NULL, '2026-02-16 01:04:42', '2026-02-16 01:05:00'),
(124, 'App\\Models\\Usuario', 11, 'auth_token', '04ac402c981ac600f530d9e65e106f9d93ebd081bcc921478a0a8db30dc621a6', '[\"*\"]', '2026-02-16 01:05:42', NULL, '2026-02-16 01:05:24', '2026-02-16 01:05:42'),
(125, 'App\\Models\\Usuario', 11, 'auth_token', '6eae1ce2b80964f3cfbc0e4656ac3dc5401e0d8e3ec4fdf483f1267a98b52a5c', '[\"*\"]', '2026-02-16 01:07:18', NULL, '2026-02-16 01:07:00', '2026-02-16 01:07:18'),
(126, 'App\\Models\\Usuario', 11, 'auth_token', '7e7f09cd1a310d33bf0d1d6289c7f647369a693f3e3b0bee49f7f0d80cfdcf5a', '[\"*\"]', '2026-02-16 01:09:10', NULL, '2026-02-16 01:08:30', '2026-02-16 01:09:10'),
(127, 'App\\Models\\Usuario', 11, 'auth_token', 'cfd0fbe428fd26fa6f50aafbf04349067e3e61390a41ef4081983375eaad7285', '[\"*\"]', '2026-02-16 01:11:51', NULL, '2026-02-16 01:11:10', '2026-02-16 01:11:51'),
(128, 'App\\Models\\Usuario', 11, 'auth_token', '61ccbf8482b2c339bc5e5e6da0266d6556482667544bd1353e7dce70f7495b39', '[\"*\"]', '2026-02-16 01:13:31', NULL, '2026-02-16 01:12:50', '2026-02-16 01:13:31'),
(129, 'App\\Models\\Usuario', 11, 'auth_token', '6a834dfa47d15d0043b030aebd99b2aa3620a9517474d25244fc16c3ca3fd96a', '[\"*\"]', '2026-02-16 17:51:01', NULL, '2026-02-16 17:39:48', '2026-02-16 17:51:01'),
(130, 'App\\Models\\Usuario', 11, 'auth_token', '22a882c837f12ac85dd3fd52382c28354680e690313bd14150e975befdd318f6', '[\"*\"]', '2026-02-16 17:55:21', NULL, '2026-02-16 17:51:10', '2026-02-16 17:55:21'),
(131, 'App\\Models\\Usuario', 11, 'auth_token', '2e2eee632554696bb1d2f2724bf79841b7a394ff0fe2e469ed7140fdc8826e9b', '[\"*\"]', '2026-02-16 17:55:53', NULL, '2026-02-16 17:55:35', '2026-02-16 17:55:53'),
(132, 'App\\Models\\Usuario', 11, 'auth_token', '1efacd91a344f86bdabcc8c101344915cb221045b3586a413e0fe4e46915a661', '[\"*\"]', '2026-02-16 17:56:42', NULL, '2026-02-16 17:56:24', '2026-02-16 17:56:42'),
(133, 'App\\Models\\Usuario', 11, 'auth_token', '50c111f5dd87d369e224f77a19026d2840a214d1727e711cd8ef71036733888e', '[\"*\"]', '2026-02-16 17:57:14', NULL, '2026-02-16 17:56:56', '2026-02-16 17:57:14'),
(134, 'App\\Models\\Usuario', 11, 'auth_token', '4deab7b5f1e5e85aaed323998f66aca7af5f4741617853ffe6defe4d489f7267', '[\"*\"]', '2026-02-16 17:57:46', NULL, '2026-02-16 17:57:28', '2026-02-16 17:57:46'),
(135, 'App\\Models\\Usuario', 11, 'auth_token', '1ce6117c8b5011a62403b3035e90c3a84581dc0ecb24edabcd381462247c508a', '[\"*\"]', '2026-02-16 17:58:29', NULL, '2026-02-16 17:58:11', '2026-02-16 17:58:29'),
(136, 'App\\Models\\Usuario', 11, 'auth_token', 'ac0f610b2b178a9eaecb7b06fd35f566cddcaadc15d4a2c0b362985a2543f3c3', '[\"*\"]', '2026-02-16 17:59:18', NULL, '2026-02-16 17:59:00', '2026-02-16 17:59:18'),
(137, 'App\\Models\\Usuario', 11, 'auth_token', '39cff2a2d23480f3f008e11692a28ad02b2364545e51a392633012515919d889', '[\"*\"]', '2026-02-16 18:01:36', NULL, '2026-02-16 18:01:18', '2026-02-16 18:01:36'),
(138, 'App\\Models\\Usuario', 11, 'auth_token', 'dac9925bef18d86e69d4b9610725c01e567dd69fc4e70f283a2f4716851b08d9', '[\"*\"]', '2026-02-16 18:04:02', NULL, '2026-02-16 18:02:51', '2026-02-16 18:04:02'),
(139, 'App\\Models\\Usuario', 11, 'auth_token', 'c612d2ab48b43a12826c41eabfdd274b7881d69df227c32a7181578889d6fd8d', '[\"*\"]', '2026-02-16 18:05:51', NULL, '2026-02-16 18:05:33', '2026-02-16 18:05:51'),
(140, 'App\\Models\\Usuario', 11, 'auth_token', 'b300f43f008e4f6041326379ce8dd81fb4275a508d3add70c36f487dff9a8232', '[\"*\"]', '2026-02-16 18:06:27', NULL, '2026-02-16 18:06:10', '2026-02-16 18:06:27'),
(141, 'App\\Models\\Usuario', 11, 'auth_token', '51824ebfc5c00d4ece59bc8405730a05b3f3cc99ca6dc1d0d9d3114c90862c16', '[\"*\"]', '2026-02-16 19:29:22', NULL, '2026-02-16 19:25:11', '2026-02-16 19:29:22'),
(142, 'App\\Models\\Usuario', 11, 'auth_token', '9caa1e7043f2b929d7d64132c24aff9162ab804a31e3e95d005a149df75de7c6', '[\"*\"]', '2026-02-16 19:33:15', NULL, '2026-02-16 19:31:35', '2026-02-16 19:33:15'),
(143, 'App\\Models\\Usuario', 11, 'auth_token', '7e301f015c47d197f448603698cc94b5cbdfc5d9a41d5bc2a0743b80097ea17d', '[\"*\"]', '2026-02-16 20:29:42', NULL, '2026-02-16 20:29:01', '2026-02-16 20:29:42'),
(144, 'App\\Models\\Usuario', 11, 'auth_token', '84f60774b9b2559b5e4021c008ebd4de9a6718195b3f141940ff2f537fae34fd', '[\"*\"]', '2026-02-16 20:32:02', NULL, '2026-02-16 20:31:44', '2026-02-16 20:32:02'),
(145, 'App\\Models\\Usuario', 11, 'auth_token', '62060b75f6bafc1d868eb86e2579469db57b057a000a7232eeedb631f8a4bebe', '[\"*\"]', '2026-02-16 20:44:55', NULL, '2026-02-16 20:44:37', '2026-02-16 20:44:55'),
(146, 'App\\Models\\Usuario', 11, 'auth_token', 'e2ed9c04ef3d0869fc6d2baedee8aca23e5ad406228a04c1f8c6d493a0fa13a3', '[\"*\"]', '2026-02-16 20:50:57', NULL, '2026-02-16 20:50:39', '2026-02-16 20:50:57'),
(147, 'App\\Models\\Usuario', 11, 'auth_token', '02d8f10f59d87b7d6db13cc286737f99ec60bd0b74502592df8cb5fa6c368405', '[\"*\"]', '2026-02-16 20:52:41', NULL, '2026-02-16 20:52:23', '2026-02-16 20:52:41'),
(148, 'App\\Models\\Usuario', 11, 'auth_token', '49695021c77a3a7a80e77776b47c07447141ffaae4e2489dc8f8968ca489667a', '[\"*\"]', '2026-02-16 20:53:46', NULL, '2026-02-16 20:53:05', '2026-02-16 20:53:46'),
(149, 'App\\Models\\Usuario', 11, 'auth_token', '2d62cd8deae2429cce92ecca10b2e34dc8d73de1b194c3dde030b1c7981e0c25', '[\"*\"]', '2026-02-16 21:17:49', NULL, '2026-02-16 21:17:09', '2026-02-16 21:17:49'),
(150, 'App\\Models\\Usuario', 11, 'auth_token', '79a15fe5ced55cb27f0532eb5d757709ec3f443e71735f434d4c5a20da28f1ab', '[\"*\"]', '2026-02-16 21:19:11', NULL, '2026-02-16 21:18:00', '2026-02-16 21:19:11'),
(151, 'App\\Models\\Usuario', 11, 'auth_token', 'a40be1c3c829752660f2963e0f0a8586c0c02fc91af8d829c59acc1879fd5ba6', '[\"*\"]', '2026-02-16 21:21:01', NULL, '2026-02-16 21:20:45', '2026-02-16 21:21:01'),
(152, 'App\\Models\\Usuario', 11, 'auth_token', '08c246ad064b8827b73620a713d33e8f8ae5311afd6d7a4f4114c6eafd8dcadb', '[\"*\"]', '2026-02-16 21:25:20', NULL, '2026-02-16 21:25:06', '2026-02-16 21:25:20'),
(153, 'App\\Models\\Usuario', 11, 'auth_token', '21cab030bec1a7a47d3ee0263aab49d67f19dc326052308f9499d6ef579b0333', '[\"*\"]', '2026-02-16 21:29:52', NULL, '2026-02-16 21:27:44', '2026-02-16 21:29:52'),
(154, 'App\\Models\\Usuario', 11, 'auth_token', 'ff93c1af469a43f60c82cc12c9fd47b145a643708f8a638ff489332122749e08', '[\"*\"]', '2026-02-16 21:33:04', NULL, '2026-02-16 21:30:16', '2026-02-16 21:33:04'),
(155, 'App\\Models\\Usuario', 11, 'auth_token', 'a8250e4593b5879f4e0b386cb1a0583d46b43085f680ea648a33518e7b7f9709', '[\"*\"]', '2026-02-16 21:37:38', NULL, '2026-02-16 21:37:06', '2026-02-16 21:37:38'),
(156, 'App\\Models\\Usuario', 11, 'auth_token', '586e6723ce4929ef4a7179692f3eac069e0066b1db2b05aaf10e7c3a7ed50a95', '[\"*\"]', '2026-02-16 21:42:19', NULL, '2026-02-16 21:41:23', '2026-02-16 21:42:19'),
(157, 'App\\Models\\Usuario', 11, 'auth_token', 'bf626476cd4218c678c9d4e0f7bde565d4920b6605313aba2868051a51417fd1', '[\"*\"]', '2026-02-16 21:50:37', NULL, '2026-02-16 21:49:57', '2026-02-16 21:50:37'),
(158, 'App\\Models\\Usuario', 11, 'auth_token', 'aabac4ab0c39352c1fdd8931af30c7b9c786c4eb27c25056f981708ab270ff16', '[\"*\"]', '2026-02-16 21:52:15', NULL, '2026-02-16 21:51:54', '2026-02-16 21:52:15'),
(159, 'App\\Models\\Usuario', 11, 'auth_token', 'e0277694269eb5a8f9f0e60e652a1b3a2559a5091611d732dbf47255f4310c29', '[\"*\"]', '2026-02-16 21:55:36', NULL, '2026-02-16 21:54:04', '2026-02-16 21:55:36'),
(160, 'App\\Models\\Usuario', 11, 'auth_token', '0110cfc222270804c6a760ef18489500bf1685b4e1c9323ed082b6c66f5a8a95', '[\"*\"]', '2026-02-16 23:08:40', NULL, '2026-02-16 23:08:15', '2026-02-16 23:08:40'),
(161, 'App\\Models\\Usuario', 11, 'auth_token', 'd77e890ec30cbe144ee3048f9202e609c40fa92b0bdcdcbbd2db414dbd8fa026', '[\"*\"]', '2026-02-17 21:59:51', NULL, '2026-02-17 21:24:10', '2026-02-17 21:59:51'),
(162, 'App\\Models\\Usuario', 11, 'auth_token', '7c599745a1f87a2d664d407180fd900f6a4f903bbdfb47b5a0140dccdb6e24e8', '[\"*\"]', '2026-02-18 00:19:37', NULL, '2026-02-18 00:19:31', '2026-02-18 00:19:37'),
(163, 'App\\Models\\Usuario', 11, 'auth_token', 'b92ecec6d6f4c63047706f04dcd28fc2a0abaa44b859b2e9c0d73c090616db53', '[\"*\"]', '2026-02-18 00:20:26', NULL, '2026-02-18 00:20:20', '2026-02-18 00:20:26'),
(164, 'App\\Models\\Usuario', 11, 'auth_token', '99ac4260a28e45058da83cce9a87e7d5076247a244b27693d79b2cf0828867ad', '[\"*\"]', '2026-02-18 00:22:05', NULL, '2026-02-18 00:21:59', '2026-02-18 00:22:05'),
(165, 'App\\Models\\Usuario', 11, 'auth_token', 'd6f343f90113e4203cb95392aaad1c4b57f5d44b363688cc2067dacf77464302', '[\"*\"]', '2026-02-18 00:25:19', NULL, '2026-02-18 00:25:13', '2026-02-18 00:25:19'),
(166, 'App\\Models\\Usuario', 11, 'auth_token', 'f6e19a49e706d7dafe1d35d74ccd351c8d7d191e86e89c2724516a7034471ff4', '[\"*\"]', '2026-02-18 00:26:01', NULL, '2026-02-18 00:25:55', '2026-02-18 00:26:01'),
(167, 'App\\Models\\Usuario', 11, 'auth_token', '002d532dfa0a016e95a65f5c8d05a88661fd4566755e312174359fceb5a2ee47', '[\"*\"]', '2026-02-18 00:26:51', NULL, '2026-02-18 00:26:32', '2026-02-18 00:26:51'),
(168, 'App\\Models\\Usuario', 11, 'auth_token', '8c27472533c9118e2cd750c986206000cf72dc56f80bb9ea33be3ec5daef8f3c', '[\"*\"]', '2026-02-18 00:37:21', NULL, '2026-02-18 00:30:15', '2026-02-18 00:37:21'),
(169, 'App\\Models\\Usuario', 11, 'auth_token', 'a2a47417e4b540097d0c840a267fdf41aaa2f4ffd40c24e2719ee7b3cf4c98f0', '[\"*\"]', '2026-02-18 00:38:19', NULL, '2026-02-18 00:38:13', '2026-02-18 00:38:19'),
(170, 'App\\Models\\Usuario', 11, 'auth_token', 'e62ae96af29f2264dec7989242596b7eeee72751e3af1e1bde1d57c9bb49c592', '[\"*\"]', '2026-02-18 00:46:00', NULL, '2026-02-18 00:40:23', '2026-02-18 00:46:00'),
(171, 'App\\Models\\Usuario', 11, 'auth_token', 'ff8de4eccf0521c92eb9d0f1a6787dae49083018748d028008a11412faf56f32', '[\"*\"]', '2026-02-18 00:46:25', NULL, '2026-02-18 00:46:19', '2026-02-18 00:46:25'),
(172, 'App\\Models\\Usuario', 11, 'auth_token', '53358a19da6128acd197973b76aa2bd86a59a21187537bfe8b33a83ea5339df9', '[\"*\"]', '2026-02-18 00:49:18', NULL, '2026-02-18 00:49:12', '2026-02-18 00:49:18');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preguntas_evaluacion`
--

CREATE TABLE `preguntas_evaluacion` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `evaluacion_id` bigint(20) UNSIGNED NOT NULL,
  `pregunta` text NOT NULL,
  `tipo` enum('seleccion_multiple','verdadero_falso','arrastrar_soltar') NOT NULL,
  `puntos` decimal(5,2) DEFAULT 1.00,
  `orden` int(11) DEFAULT 0,
  `created_by` bigint(20) UNSIGNED NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `preguntas_evaluacion`
--

INSERT INTO `preguntas_evaluacion` (`id`, `evaluacion_id`, `pregunta`, `tipo`, `puntos`, `orden`, `created_by`, `created_at`, `updated_at`) VALUES
(1, 1, '¿Qué significa HTML?', 'seleccion_multiple', 10.00, 1, 6, '2026-02-01 18:05:00', '2026-02-01 18:05:00'),
(2, 1, 'HTML es un lenguaje de programación', 'verdadero_falso', 10.00, 2, 6, '2026-02-01 18:06:00', '2026-02-01 18:06:00'),
(3, 1, '¿Cuál es la etiqueta raíz en HTML5?', 'seleccion_multiple', 10.00, 3, 6, '2026-02-01 18:07:00', '2026-02-01 18:07:00'),
(4, 1, 'La etiqueta <title> va dentro de <body>', 'arrastrar_soltar', 10.00, 4, 6, '2026-02-01 18:08:00', '2026-02-14 04:44:24'),
(5, 1, '¿Qué etiqueta se usa para enlaces?', 'seleccion_multiple', 10.00, 5, 6, '2026-02-01 18:09:00', '2026-02-01 18:09:00'),
(6, 1, 'Relaciona las etiquetas con su función', 'arrastrar_soltar', 10.00, 6, 6, '2026-02-01 18:10:00', '2026-02-01 18:10:00'),
(7, 1, '¿Qué atributo define la acción de un formulario?', 'seleccion_multiple', 10.00, 7, 6, '2026-02-01 18:11:00', '2026-02-01 18:11:00'),
(8, 1, 'Los formularios solo pueden usar GET', 'verdadero_falso', 10.00, 8, 6, '2026-02-01 18:12:00', '2026-02-01 18:12:00'),
(9, 1, '¿Cuál es el encabezado más importante?', 'seleccion_multiple', 10.00, 9, 6, '2026-02-01 18:13:00', '2026-02-01 18:13:00'),
(11, 2, '¿Qué significa CSS?', 'seleccion_multiple', 10.00, 1, 6, '2026-02-08 20:15:16', '2026-02-08 20:15:16'),
(12, 2, '¿Qué propiedad CSS se usa para cambiar el color del texto?', 'seleccion_multiple', 10.00, 2, 6, '2026-02-08 20:15:16', '2026-02-08 20:15:16'),
(13, 1, 'PRUEBA FUNCIONAL', 'verdadero_falso', 10.00, 10, 11, '2026-02-14 03:41:06', '2026-02-14 03:41:06'),
(14, 3, 'CUANTO ES 1 +1?', 'seleccion_multiple', 10.00, 1, 11, '2026-02-14 03:57:00', '2026-02-14 03:57:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `progreso_lecciones`
--

CREATE TABLE `progreso_lecciones` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `usuario_id` bigint(20) UNSIGNED NOT NULL,
  `leccion_id` bigint(20) UNSIGNED NOT NULL,
  `vista` tinyint(1) DEFAULT 0,
  `fecha_vista` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `progreso_lecciones`
--

INSERT INTO `progreso_lecciones` (`id`, `usuario_id`, `leccion_id`, `vista`, `fecha_vista`, `created_at`, `updated_at`) VALUES
(1, 6, 1, 1, '2026-02-02 08:30:00', '2026-02-02 13:30:00', '2026-02-02 13:30:00'),
(2, 6, 2, 1, '2026-02-02 09:00:00', '2026-02-02 14:00:00', '2026-02-02 14:00:00'),
(3, 6, 3, 1, '2026-02-02 09:30:00', '2026-02-02 14:30:00', '2026-02-02 14:30:00'),
(4, 6, 4, 1, '2026-02-02 10:30:00', '2026-02-02 15:30:00', '2026-02-02 15:30:00'),
(10, 9, 1, 1, '2026-02-02 11:00:00', '2026-02-02 16:00:00', '2026-02-02 16:00:00'),
(11, 10, 1, 1, '2026-02-02 08:00:00', '2026-02-02 13:00:00', '2026-02-02 13:00:00'),
(12, 10, 2, 1, '2026-02-02 09:00:00', '2026-02-02 14:00:00', '2026-02-02 14:00:00'),
(13, 10, 3, 1, '2026-02-02 10:00:00', '2026-02-02 15:00:00', '2026-02-02 15:00:00'),
(14, 10, 4, 1, '2026-02-02 11:00:00', '2026-02-02 16:00:00', '2026-02-02 16:00:00'),
(15, 10, 5, 1, '2026-02-02 12:00:00', '2026-02-02 17:00:00', '2026-02-02 17:00:00'),
(31, 11, 6, 1, '2026-02-08 20:10:27', '2026-02-09 01:10:27', '2026-02-09 01:10:27'),
(32, 11, 7, 1, '2026-02-08 20:10:33', '2026-02-09 01:10:33', '2026-02-09 01:10:33'),
(33, 11, 8, 1, '2026-02-08 20:10:36', '2026-02-09 01:10:36', '2026-02-09 01:10:36'),
(34, 11, 9, 1, '2026-02-08 20:10:40', '2026-02-09 01:10:40', '2026-02-09 01:10:40');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `progreso_modulo`
--

CREATE TABLE `progreso_modulo` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `usuario_id` bigint(20) UNSIGNED NOT NULL,
  `modulo_id` bigint(20) UNSIGNED NOT NULL,
  `porcentaje_completado` decimal(5,2) DEFAULT 0.00,
  `lecciones_vistas` int(11) DEFAULT 0,
  `total_lecciones` int(11) DEFAULT 0,
  `ultima_leccion_vista_id` bigint(20) UNSIGNED DEFAULT NULL,
  `evaluacion_aprobada` tinyint(1) DEFAULT 0,
  `certificado_disponible` tinyint(1) DEFAULT 0,
  `fecha_ultimo_progreso` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `progreso_modulo`
--

INSERT INTO `progreso_modulo` (`id`, `usuario_id`, `modulo_id`, `porcentaje_completado`, `lecciones_vistas`, `total_lecciones`, `ultima_leccion_vista_id`, `evaluacion_aprobada`, `certificado_disponible`, `fecha_ultimo_progreso`, `created_at`, `updated_at`) VALUES
(1, 6, 1, 80.00, 4, 5, NULL, 0, 0, '2026-02-02 10:30:00', '2026-02-02 13:30:00', '2026-02-02 15:30:00'),
(4, 9, 1, 20.00, 1, 5, NULL, 0, 0, '2026-02-02 10:00:00', '2026-02-01 17:00:00', '2026-02-02 15:00:00'),
(5, 10, 1, 100.00, 5, 5, NULL, 1, 1, '2026-02-02 12:00:00', '2026-02-01 18:00:00', '2026-02-02 17:00:00'),
(6, 6, 2, 50.00, 2, 4, NULL, 0, 0, '2026-02-03 11:30:00', '2026-02-03 15:30:00', '2026-02-03 16:30:00'),
(7, 10, 2, 75.00, 3, 4, NULL, 0, 0, '2026-02-03 12:00:00', '2026-02-03 16:00:00', '2026-02-03 17:00:00'),
(14, 11, 1, 100.00, 0, 0, NULL, 1, 1, '2026-02-08 20:33:49', '2026-02-09 01:10:57', '2026-02-09 01:33:49'),
(15, 11, 2, 100.00, 4, 4, 9, 1, 1, '2026-02-08 20:28:00', '2026-02-09 01:10:57', '2026-02-09 01:28:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ranking`
--

CREATE TABLE `ranking` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `modulo_id` bigint(20) UNSIGNED NOT NULL,
  `usuario_id` bigint(20) UNSIGNED NOT NULL,
  `porcentaje_progreso` decimal(5,2) DEFAULT 0.00,
  `posicion` int(11) DEFAULT NULL,
  `fecha_ultima_actualizacion` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `ranking`
--

INSERT INTO `ranking` (`id`, `modulo_id`, `usuario_id`, `porcentaje_progreso`, `posicion`, `fecha_ultima_actualizacion`, `created_at`) VALUES
(12, 1, 10, 100.00, 1, '2026-02-02 17:00:00', '2026-02-02 22:00:00'),
(13, 1, 6, 80.00, 2, '2026-02-02 15:30:00', '2026-02-02 20:30:00'),
(16, 1, 9, 20.00, 5, '2026-02-02 15:00:00', '2026-02-02 20:00:00'),
(17, 2, 10, 75.00, 1, '2026-02-03 12:00:00', '2026-02-03 17:00:00'),
(18, 2, 6, 50.00, 2, '2026-02-03 11:30:00', '2026-02-03 16:30:00'),
(19, 2, 11, 100.00, NULL, '2026-02-08 20:28:00', '2026-02-08 20:26:47'),
(20, 1, 11, 100.00, NULL, '2026-02-08 20:33:49', '2026-02-08 20:29:41');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `respuestas_evaluacion`
--

CREATE TABLE `respuestas_evaluacion` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `intento_id` bigint(20) UNSIGNED NOT NULL,
  `pregunta_evaluacion_id` bigint(20) UNSIGNED NOT NULL,
  `opcion_seleccionada_id` bigint(20) UNSIGNED DEFAULT NULL,
  `respuesta_texto` text DEFAULT NULL,
  `es_correcta` tinyint(1) DEFAULT 0,
  `puntos_obtenidos` decimal(5,2) DEFAULT 0.00,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `respuestas_evaluacion`
--

INSERT INTO `respuestas_evaluacion` (`id`, `intento_id`, `pregunta_evaluacion_id`, `opcion_seleccionada_id`, `respuesta_texto`, `es_correcta`, `puntos_obtenidos`, `created_at`) VALUES
(4, 1, 1, 1, NULL, 1, 10.00, '2026-02-02 21:01:00'),
(5, 1, 2, 5, NULL, 1, 10.00, '2026-02-02 21:02:00'),
(6, 1, 3, 6, NULL, 1, 10.00, '2026-02-02 21:03:00'),
(7, 1, 4, 10, NULL, 1, 10.00, '2026-02-02 21:04:00'),
(8, 1, 5, 11, NULL, 1, 10.00, '2026-02-02 21:05:00'),
(9, 1, 7, 17, NULL, 1, 10.00, '2026-02-02 21:06:00'),
(10, 1, 9, 22, NULL, 1, 10.00, '2026-02-02 21:07:00'),
(12, 1, 6, NULL, '<p>-Párrafo,<ul>-Lista no ordenada,<h1>-Encabezado principal', 0, 5.00, '2026-02-02 21:09:00'),
(13, 1, 8, 20, NULL, 0, 0.00, '2026-02-02 21:10:00'),
(14, 2, 1, 1, NULL, 1, 10.00, '2026-02-02 21:15:00'),
(15, 2, 2, 5, NULL, 1, 10.00, '2026-02-02 21:16:00'),
(16, 2, 3, 6, NULL, 1, 10.00, '2026-02-02 21:17:00'),
(17, 2, 4, 10, NULL, 1, 10.00, '2026-02-02 21:18:00'),
(18, 2, 5, 11, NULL, 1, 10.00, '2026-02-02 21:19:00'),
(19, 2, 6, NULL, '<p>-Párrafo,<ul>-Lista no ordenada,<h1>-Encabezado principal', 1, 10.00, '2026-02-02 21:20:00'),
(20, 2, 7, 17, NULL, 1, 10.00, '2026-02-02 21:21:00'),
(21, 2, 8, 21, NULL, 1, 10.00, '2026-02-02 21:22:00'),
(22, 2, 9, 22, NULL, 1, 10.00, '2026-02-02 21:23:00'),
(54, 9, 11, 27, NULL, 1, 10.00, '2026-02-09 01:16:47'),
(55, 9, 12, 30, NULL, 1, 10.00, '2026-02-09 01:16:57'),
(56, 10, 1, 1, NULL, 1, 10.00, '2026-02-09 01:30:19'),
(57, 10, 2, 5, NULL, 1, 10.00, '2026-02-09 01:30:52'),
(58, 10, 3, 6, NULL, 1, 10.00, '2026-02-09 01:31:00'),
(59, 10, 4, 10, NULL, 1, 10.00, '2026-02-09 01:31:07'),
(60, 10, 5, 11, NULL, 1, 10.00, '2026-02-09 01:31:12'),
(61, 10, 7, 17, NULL, 1, 10.00, '2026-02-09 01:31:19'),
(62, 10, 9, 22, NULL, 1, 10.00, '2026-02-09 01:31:29'),
(64, 10, 8, 20, NULL, 0, 0.00, '2026-02-09 01:31:42');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sessions`
--

CREATE TABLE `sessions` (
  `id` varchar(255) NOT NULL,
  `user_id` bigint(20) UNSIGNED DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `payload` longtext NOT NULL,
  `last_activity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `sessions`
--

INSERT INTO `sessions` (`id`, `user_id`, `ip_address`, `user_agent`, `payload`, `last_activity`) VALUES
('nV6G52AVyKIDaTGiGOLWFznuqtYng0GklJjCkFZn', NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoiWEU5WjMwc1ZaaEUzUGxtaVBoY3l2d2hrdFo5dnFaMjlFMUxKMkVxciI7czo5OiJfcHJldmlvdXMiO2E6Mjp7czozOiJ1cmwiO3M6MzE6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9kYXNoYm9hcmQiO3M6NToicm91dGUiO047fXM6NjoiX2ZsYXNoIjthOjI6e3M6Mzoib2xkIjthOjA6e31zOjM6Im5ldyI7YTowOnt9fX0=', 1770585038),
('session123456', 6, '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'payload_data_here', 1770407004);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_attempts`
--

CREATE TABLE `user_attempts` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `action` varchar(255) NOT NULL,
  `success` tinyint(1) NOT NULL,
  `ip` varchar(255) DEFAULT NULL,
  `user_agent` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `user_attempts`
--

INSERT INTO `user_attempts` (`id`, `user_id`, `email`, `action`, `success`, `ip`, `user_agent`, `created_at`, `updated_at`) VALUES
(1, NULL, 'varchate25@gmail.com', 'login', 0, NULL, 'PostmanRuntime/7.51.1', '2026-02-02 06:39:42', '2026-02-02 06:39:42'),
(2, NULL, 'varchate25@gmail.com', 'login', 1, NULL, 'PostmanRuntime/7.51.1', '2026-02-02 06:40:00', '2026-02-02 06:40:00'),
(3, NULL, 'varchate25@gmail.com', 'login', 1, NULL, 'PostmanRuntime/7.51.1', '2026-02-02 06:54:47', '2026-02-02 06:54:47'),
(4, NULL, 'varchate25@gmail.com', 'login', 1, NULL, 'PostmanRuntime/7.51.1', '2026-02-02 06:54:51', '2026-02-02 06:54:51'),
(5, NULL, 'varchate25@gmail.com', 'login', 0, NULL, 'PostmanRuntime/7.51.1', '2026-02-02 07:04:33', '2026-02-02 07:04:33'),
(6, NULL, 'varchate25@gmail.com', 'login', 0, NULL, 'PostmanRuntime/7.51.1', '2026-02-02 07:04:40', '2026-02-02 07:04:40'),
(7, NULL, 'varchate25@gmail.com', 'login', 1, NULL, 'PostmanRuntime/7.51.1', '2026-02-02 07:04:55', '2026-02-02 07:04:55'),
(8, NULL, 'varchate25@gmail.com', 'login', 0, NULL, 'PostmanRuntime/7.51.1', '2026-02-02 07:25:48', '2026-02-02 07:25:48'),
(9, NULL, 'alejo29.c@gmail.com', 'login', 0, NULL, 'PostmanRuntime/7.51.1', '2026-02-07 00:54:41', '2026-02-07 00:54:41'),
(10, 11, 'alejo29.c@gmail.com', 'register', 1, '127.0.0.1', 'PostmanRuntime/7.51.1', '2026-02-07 00:55:24', '2026-02-07 00:55:24'),
(11, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'PostmanRuntime/7.51.1', '2026-02-07 00:55:42', '2026-02-07 00:55:42'),
(12, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'PostmanRuntime/7.51.1', '2026-02-07 01:12:54', '2026-02-07 01:12:54'),
(13, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'PostmanRuntime/7.51.1', '2026-02-07 02:01:31', '2026-02-07 02:01:31'),
(14, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'PostmanRuntime/7.51.1', '2026-02-07 02:02:34', '2026-02-07 02:02:34'),
(15, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'PostmanRuntime/7.51.1', '2026-02-07 02:35:45', '2026-02-07 02:35:45'),
(16, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'PostmanRuntime/7.51.1', '2026-02-08 22:32:00', '2026-02-08 22:32:00'),
(17, NULL, 'admin@email.com', 'login', 0, NULL, 'python-requests/2.31.0', '2026-02-14 01:14:40', '2026-02-14 01:14:40'),
(18, NULL, 'varchate25@gmail.com', 'login', 0, NULL, 'python-requests/2.31.0', '2026-02-14 01:16:47', '2026-02-14 01:16:47'),
(19, NULL, 'admin@email.com', 'login', 0, NULL, 'python-requests/2.31.0', '2026-02-14 01:17:31', '2026-02-14 01:17:31'),
(20, NULL, 'varchate25@gmail.com', 'login', 0, NULL, 'python-requests/2.31.0', '2026-02-14 01:17:37', '2026-02-14 01:17:37'),
(21, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:18:50', '2026-02-14 01:18:50'),
(22, NULL, 'carlos.lopez@email.com', 'login', 0, NULL, 'python-requests/2.31.0', '2026-02-14 01:19:52', '2026-02-14 01:19:52'),
(23, NULL, 'carlos.lopez@email.com', 'login', 0, NULL, 'python-requests/2.31.0', '2026-02-14 01:20:06', '2026-02-14 01:20:06'),
(24, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:20:17', '2026-02-14 01:20:17'),
(25, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:21:25', '2026-02-14 01:21:25'),
(26, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:26:55', '2026-02-14 01:26:55'),
(27, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:28:44', '2026-02-14 01:28:44'),
(28, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:31:00', '2026-02-14 01:31:00'),
(29, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:32:34', '2026-02-14 01:32:34'),
(30, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:36:47', '2026-02-14 01:36:47'),
(31, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:38:20', '2026-02-14 01:38:20'),
(32, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:40:26', '2026-02-14 01:40:26'),
(33, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:43:44', '2026-02-14 01:43:44'),
(34, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:45:06', '2026-02-14 01:45:06'),
(35, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:48:31', '2026-02-14 01:48:31'),
(36, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:50:52', '2026-02-14 01:50:52'),
(37, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:53:28', '2026-02-14 01:53:28'),
(38, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:56:17', '2026-02-14 01:56:17'),
(39, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 01:58:14', '2026-02-14 01:58:14'),
(40, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:02:49', '2026-02-14 02:02:49'),
(41, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:03:57', '2026-02-14 02:03:57'),
(42, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:04:37', '2026-02-14 02:04:37'),
(43, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:10:02', '2026-02-14 02:10:02'),
(44, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:11:12', '2026-02-14 02:11:12'),
(45, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:13:13', '2026-02-14 02:13:13'),
(46, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:13:37', '2026-02-14 02:13:37'),
(47, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:18:52', '2026-02-14 02:18:52'),
(48, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:22:55', '2026-02-14 02:22:55'),
(49, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:30:05', '2026-02-14 02:30:05'),
(50, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:34:51', '2026-02-14 02:34:51'),
(51, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:36:56', '2026-02-14 02:36:56'),
(52, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:38:11', '2026-02-14 02:38:11'),
(53, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:50:52', '2026-02-14 02:50:52'),
(54, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:53:13', '2026-02-14 02:53:13'),
(55, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 02:58:45', '2026-02-14 02:58:45'),
(56, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 03:11:49', '2026-02-14 03:11:49'),
(57, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 03:13:03', '2026-02-14 03:13:03'),
(58, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 03:15:07', '2026-02-14 03:15:07'),
(59, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 03:20:50', '2026-02-14 03:20:50'),
(60, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 03:28:18', '2026-02-14 03:28:18'),
(61, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 03:34:49', '2026-02-14 03:34:49'),
(62, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 03:39:24', '2026-02-14 03:39:24'),
(63, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 03:42:04', '2026-02-14 03:42:04'),
(64, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 03:55:38', '2026-02-14 03:55:38'),
(65, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 04:03:12', '2026-02-14 04:03:12'),
(66, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 04:15:24', '2026-02-14 04:15:24'),
(67, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 04:18:59', '2026-02-14 04:18:59'),
(68, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 04:35:32', '2026-02-14 04:35:32'),
(69, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 04:37:21', '2026-02-14 04:37:21'),
(70, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 04:43:39', '2026-02-14 04:43:39'),
(71, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 04:47:42', '2026-02-14 04:47:42'),
(72, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 04:50:58', '2026-02-14 04:50:58'),
(73, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 05:02:04', '2026-02-14 05:02:04'),
(74, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 05:06:06', '2026-02-14 05:06:06'),
(75, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 05:07:08', '2026-02-14 05:07:08'),
(76, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 05:10:47', '2026-02-14 05:10:47'),
(77, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 05:12:43', '2026-02-14 05:12:43'),
(78, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 05:15:03', '2026-02-14 05:15:03'),
(79, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 05:15:40', '2026-02-14 05:15:40'),
(80, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 05:18:46', '2026-02-14 05:18:46'),
(81, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-14 21:26:38', '2026-02-14 21:26:38'),
(82, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-15 22:02:15', '2026-02-15 22:02:15'),
(83, NULL, 'alejo29.c@gmail.co', 'login', 0, NULL, 'python-requests/2.31.0', '2026-02-15 22:03:12', '2026-02-15 22:03:12'),
(84, NULL, 'alejo29.c@gmail.co', 'login', 0, NULL, 'python-requests/2.31.0', '2026-02-15 22:03:32', '2026-02-15 22:03:32'),
(85, NULL, 'alejo29.c@gmail.com', 'login', 0, NULL, 'python-requests/2.31.0', '2026-02-15 22:03:43', '2026-02-15 22:03:43'),
(86, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-15 22:05:22', '2026-02-15 22:05:22'),
(87, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-15 22:14:04', '2026-02-15 22:14:04'),
(88, NULL, 'alejo29.c@gmail.co', 'login', 0, NULL, 'python-requests/2.31.0', '2026-02-15 22:14:58', '2026-02-15 22:14:58'),
(89, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-15 22:16:41', '2026-02-15 22:16:41'),
(90, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-15 22:20:31', '2026-02-15 22:20:31'),
(91, NULL, 'alejo29.c@gmail.co', 'login', 0, NULL, 'python-requests/2.31.0', '2026-02-15 22:22:35', '2026-02-15 22:22:35'),
(92, NULL, 'alejo29.c@gmail.co', 'login', 0, NULL, 'python-requests/2.31.0', '2026-02-15 22:28:13', '2026-02-15 22:28:13'),
(93, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-15 22:28:37', '2026-02-15 22:28:37'),
(94, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-15 22:29:10', '2026-02-15 22:29:10'),
(95, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-15 22:29:39', '2026-02-15 22:29:39'),
(96, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-15 22:31:44', '2026-02-15 22:31:44'),
(97, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-15 22:32:51', '2026-02-15 22:32:51'),
(98, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-15 22:39:35', '2026-02-15 22:39:35'),
(99, NULL, 'alejo29.c@gmail.co', 'login', 0, NULL, 'python-requests/2.31.0', '2026-02-15 22:39:47', '2026-02-15 22:39:47'),
(100, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-15 22:40:17', '2026-02-15 22:40:17'),
(101, NULL, 'alejo29.c@gmail.co', 'login', 0, NULL, 'Varchate-Admin/1.0', '2026-02-15 22:46:07', '2026-02-15 22:46:07'),
(102, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 22:46:15', '2026-02-15 22:46:15'),
(103, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 22:47:04', '2026-02-15 22:47:04'),
(104, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 22:47:16', '2026-02-15 22:47:16'),
(105, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'python-requests/2.31.0', '2026-02-15 22:47:39', '2026-02-15 22:47:39'),
(106, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 22:54:18', '2026-02-15 22:54:18'),
(107, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 22:56:24', '2026-02-15 22:56:24'),
(108, NULL, 'alejo29.c@gmail.co', 'login', 0, NULL, 'Varchate-Admin/1.0', '2026-02-15 22:56:33', '2026-02-15 22:56:33'),
(109, NULL, 'alejo29.c@gmail.co', 'login', 0, NULL, 'Varchate-Admin/1.0', '2026-02-15 22:56:39', '2026-02-15 22:56:39'),
(110, NULL, 'alejo29.c@gmail.com', 'login', 0, NULL, 'Varchate-Admin/1.0', '2026-02-15 22:56:46', '2026-02-15 22:56:46'),
(111, NULL, 'alejo29.c@gmail.com', 'login', 0, NULL, 'Varchate-Admin/1.0', '2026-02-15 22:57:03', '2026-02-15 22:57:03'),
(112, NULL, 'alejo29.c@gmail.com', 'login', 0, NULL, 'Varchate-Admin/1.0', '2026-02-15 22:57:28', '2026-02-15 22:57:28'),
(113, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 22:58:28', '2026-02-15 22:58:28'),
(114, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 22:59:17', '2026-02-15 22:59:17'),
(115, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:01:30', '2026-02-15 23:01:30'),
(116, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:01:45', '2026-02-15 23:01:45'),
(117, NULL, 'alejo29.c@gmail.co', 'login', 0, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:06:11', '2026-02-15 23:06:11'),
(118, NULL, 'linaa@gmail.com', 'login', 0, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:06:28', '2026-02-15 23:06:28'),
(119, NULL, 'linaa@gmail.com', 'login', 0, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:06:34', '2026-02-15 23:06:34'),
(120, NULL, 'linaa@gmail.com', 'login', 0, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:07:20', '2026-02-15 23:07:20'),
(121, NULL, 'lina.c@gmail.com', 'login', 0, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:07:33', '2026-02-15 23:07:33'),
(122, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:13:28', '2026-02-15 23:13:28'),
(123, NULL, 'alejo29.c@gmail.co', 'login', 0, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:16:07', '2026-02-15 23:16:07'),
(124, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:24:38', '2026-02-15 23:24:38'),
(125, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:26:57', '2026-02-15 23:26:57'),
(126, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:27:31', '2026-02-15 23:27:31'),
(127, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:30:42', '2026-02-15 23:30:42'),
(128, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:31:18', '2026-02-15 23:31:18'),
(129, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:32:41', '2026-02-15 23:32:41'),
(130, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:34:12', '2026-02-15 23:34:12'),
(131, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-15 23:57:04', '2026-02-15 23:57:04'),
(132, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:05:18', '2026-02-16 00:05:18'),
(133, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:05:53', '2026-02-16 00:05:53'),
(134, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:09:13', '2026-02-16 00:09:13'),
(135, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:16:56', '2026-02-16 00:16:56'),
(136, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:20:36', '2026-02-16 00:20:36'),
(137, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:22:37', '2026-02-16 00:22:37'),
(138, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:23:20', '2026-02-16 00:23:20'),
(139, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:28:56', '2026-02-16 00:28:56'),
(140, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:29:13', '2026-02-16 00:29:13'),
(141, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:31:23', '2026-02-16 00:31:23'),
(142, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:34:58', '2026-02-16 00:34:58'),
(143, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:38:26', '2026-02-16 00:38:26'),
(144, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:41:18', '2026-02-16 00:41:18'),
(145, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:44:16', '2026-02-16 00:44:16'),
(146, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:45:33', '2026-02-16 00:45:33'),
(147, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:47:36', '2026-02-16 00:47:36'),
(148, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:49:35', '2026-02-16 00:49:35'),
(149, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 00:50:25', '2026-02-16 00:50:25'),
(150, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 01:00:49', '2026-02-16 01:00:49'),
(151, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 01:01:37', '2026-02-16 01:01:37'),
(152, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 01:03:04', '2026-02-16 01:03:04'),
(153, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 01:04:02', '2026-02-16 01:04:02'),
(154, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 01:04:42', '2026-02-16 01:04:42'),
(155, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 01:05:24', '2026-02-16 01:05:24'),
(156, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 01:07:00', '2026-02-16 01:07:00'),
(157, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 01:08:30', '2026-02-16 01:08:30'),
(158, NULL, 'alejo29.c@gmail.co', 'login', 0, NULL, 'Varchate-Admin/1.0', '2026-02-16 01:09:13', '2026-02-16 01:09:13'),
(159, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 01:11:10', '2026-02-16 01:11:10'),
(160, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 01:12:50', '2026-02-16 01:12:50'),
(161, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 17:39:48', '2026-02-16 17:39:48'),
(162, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 17:51:10', '2026-02-16 17:51:10'),
(163, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 17:55:35', '2026-02-16 17:55:35'),
(164, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 17:56:24', '2026-02-16 17:56:24'),
(165, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 17:56:56', '2026-02-16 17:56:56'),
(166, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 17:57:28', '2026-02-16 17:57:28'),
(167, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 17:58:11', '2026-02-16 17:58:11'),
(168, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 17:59:00', '2026-02-16 17:59:00'),
(169, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 18:01:18', '2026-02-16 18:01:18'),
(170, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 18:02:51', '2026-02-16 18:02:51'),
(171, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 18:05:33', '2026-02-16 18:05:33'),
(172, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 18:06:10', '2026-02-16 18:06:10'),
(173, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 19:25:11', '2026-02-16 19:25:11'),
(174, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 19:31:34', '2026-02-16 19:31:34'),
(175, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 20:29:01', '2026-02-16 20:29:01'),
(176, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 20:31:44', '2026-02-16 20:31:44'),
(177, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 20:44:37', '2026-02-16 20:44:37'),
(178, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 20:50:39', '2026-02-16 20:50:39'),
(179, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 20:52:23', '2026-02-16 20:52:23'),
(180, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 20:53:05', '2026-02-16 20:53:05'),
(181, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 21:17:09', '2026-02-16 21:17:09'),
(182, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 21:18:00', '2026-02-16 21:18:00'),
(183, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 21:20:45', '2026-02-16 21:20:45'),
(184, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 21:25:06', '2026-02-16 21:25:06'),
(185, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 21:27:44', '2026-02-16 21:27:44'),
(186, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 21:30:16', '2026-02-16 21:30:16'),
(187, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 21:37:06', '2026-02-16 21:37:06'),
(188, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 21:41:23', '2026-02-16 21:41:23'),
(189, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 21:49:57', '2026-02-16 21:49:57'),
(190, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 21:51:54', '2026-02-16 21:51:54'),
(191, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 21:54:04', '2026-02-16 21:54:04'),
(192, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-16 23:08:15', '2026-02-16 23:08:15'),
(193, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-17 21:24:10', '2026-02-17 21:24:10'),
(194, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-18 00:19:31', '2026-02-18 00:19:31'),
(195, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-18 00:20:20', '2026-02-18 00:20:20'),
(196, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-18 00:21:59', '2026-02-18 00:21:59'),
(197, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-18 00:25:13', '2026-02-18 00:25:13'),
(198, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-18 00:25:55', '2026-02-18 00:25:55'),
(199, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-18 00:26:32', '2026-02-18 00:26:32'),
(200, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-18 00:30:15', '2026-02-18 00:30:15'),
(201, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-18 00:38:13', '2026-02-18 00:38:13'),
(202, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-18 00:40:23', '2026-02-18 00:40:23'),
(203, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-18 00:46:19', '2026-02-18 00:46:19'),
(204, NULL, 'alejo29.c@gmail.com', 'login', 1, NULL, 'Varchate-Admin/1.0', '2026-02-18 00:49:12', '2026-02-18 00:49:12');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `rol` enum('administrador','aprendiz') DEFAULT 'aprendiz',
  `estado` enum('activo','inactivo') DEFAULT 'activo',
  `tema_preferido` enum('claro','oscuro') DEFAULT 'claro',
  `proveedor_auth` enum('email','google','facebook') DEFAULT 'email',
  `auth_provider_id` varchar(255) DEFAULT NULL,
  `token_verificacion` varchar(100) DEFAULT NULL,
  `token_restablecimiento` varchar(100) DEFAULT NULL,
  `fecha_expiracion_token` datetime DEFAULT NULL,
  `intentos_fallidos` tinyint(4) DEFAULT 0,
  `bloqueado_hasta` datetime DEFAULT NULL,
  `ultimo_acceso` datetime DEFAULT NULL,
  `terms_accepted` tinyint(1) NOT NULL DEFAULT 0,
  `terms_accepted_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `avatar_id` bigint(20) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `email_verified_at`, `password`, `rol`, `estado`, `tema_preferido`, `proveedor_auth`, `auth_provider_id`, `token_verificacion`, `token_restablecimiento`, `fecha_expiracion_token`, `intentos_fallidos`, `bloqueado_hasta`, `ultimo_acceso`, `terms_accepted`, `terms_accepted_at`, `created_at`, `updated_at`, `avatar_id`) VALUES
(6, 'Varchate', 'varchate25@gmail.com', NULL, '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'administrador', 'activo', 'claro', 'email', NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2026-02-02 23:26:27', '2026-02-02 23:26:27', '2026-02-06 19:43:23', 1),
(9, 'María García', 'maria.garcia@email.com', NULL, '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'aprendiz', 'activo', 'claro', 'email', NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, NULL, '2026-02-01 15:00:00', '2026-02-01 15:00:00', 4),
(10, 'Pedro Martínez', 'pedro.martinez@email.com', NULL, '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'aprendiz', 'activo', 'oscuro', 'email', NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, NULL, '2026-02-01 16:00:00', '2026-02-01 16:00:00', 5),
(11, 'Alejo', 'alejo29.c@gmail.com', '2026-02-07 00:55:36', '$2y$12$DZ8/FvhydBbUS14vFKrm5uu4q.xqnengw1BlX.MC5snB7uAv9l6Wm', 'administrador', 'activo', 'claro', 'email', NULL, NULL, NULL, NULL, 0, NULL, NULL, 1, '2026-02-07 00:55:24', '2026-02-07 00:55:24', '2026-02-16 21:29:07', 1),
(13, 'Carlos Rodríguez', 'carlos.rodriguez@email.com', '2026-02-17 19:44:36', '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'administrador', 'activo', 'claro', 'email', NULL, NULL, NULL, NULL, 0, NULL, '2026-02-16 10:00:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 2),
(14, 'Ana López', 'ana.lopez@email.com', '2026-02-17 19:44:36', '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'administrador', 'activo', 'oscuro', 'email', NULL, NULL, NULL, NULL, 0, NULL, '2026-02-16 09:30:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 3),
(15, 'Luis Fernando Torres', 'luis.torres@email.com', '2026-02-17 19:44:36', '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'aprendiz', 'activo', 'claro', 'email', NULL, NULL, NULL, NULL, 0, NULL, '2026-02-15 18:20:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 4),
(16, 'Camila Restrepo', 'camila.restrepo@email.com', '2026-02-17 19:44:36', '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'aprendiz', 'activo', 'claro', 'email', NULL, NULL, NULL, NULL, 0, NULL, '2026-02-15 16:45:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 5),
(17, 'Andrés Felipe Gómez', 'andres.gomez@email.com', '2026-02-17 19:44:36', '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'aprendiz', 'activo', 'oscuro', 'email', NULL, NULL, NULL, NULL, 0, NULL, '2026-02-14 14:30:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 6),
(18, 'Valentina Díaz', 'valentina.diaz@email.com', '2026-02-17 19:44:36', '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'aprendiz', 'activo', 'claro', 'email', NULL, NULL, NULL, NULL, 0, NULL, '2026-02-14 11:15:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 7),
(19, 'Javier Hernández', 'javier.hernandez@email.com', '2026-02-17 19:44:36', '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'aprendiz', 'activo', 'claro', 'email', NULL, NULL, NULL, NULL, 0, NULL, '2026-02-13 20:10:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 8),
(20, 'Sofía Mejía', 'sofia.mejia@email.com', '2026-02-17 19:44:36', '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'aprendiz', 'activo', 'oscuro', 'email', NULL, NULL, NULL, NULL, 0, NULL, '2026-02-13 15:40:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 1),
(21, 'Diego Alejandro Castro', 'diego.castro@email.com', '2026-02-17 19:44:36', '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'aprendiz', 'activo', 'claro', 'email', NULL, NULL, NULL, NULL, 0, NULL, '2026-02-12 12:25:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 2),
(22, 'Laura Patricia Ríos', 'laura.rios@email.com', '2026-02-17 19:44:36', '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'aprendiz', 'activo', 'claro', 'email', NULL, NULL, NULL, NULL, 0, NULL, '2026-02-12 10:50:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 3),
(23, 'Miguel Ángel Silva', 'miguel.silva@email.com', '2026-02-17 19:44:36', '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'aprendiz', 'inactivo', 'oscuro', 'email', NULL, NULL, NULL, NULL, 3, '2026-02-17 15:44:36', '2026-02-11 22:15:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 4),
(24, 'Roberto Méndez', 'roberto.mendez@gmail.com', '2026-02-17 19:44:36', NULL, 'aprendiz', 'activo', 'claro', 'google', 'google_123456789', NULL, NULL, NULL, 0, NULL, '2026-02-16 08:20:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 5),
(25, 'Patricia Vega', 'patricia.vega@yahoo.com', '2026-02-17 19:44:36', NULL, 'aprendiz', 'activo', 'claro', 'facebook', 'fb_987654321', NULL, NULL, NULL, 0, NULL, '2026-02-15 19:35:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 6),
(26, 'Fernando Quintana', 'fernando.quintana@email.com', '2026-02-17 19:44:36', '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'aprendiz', 'activo', 'oscuro', 'email', NULL, NULL, NULL, NULL, 0, NULL, '2026-02-16 07:10:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 7),
(27, 'Gabriela Silva', 'gabriela.silva@email.com', '2026-02-17 19:44:36', '$2y$12$VKOgkBP3yqcffq6Lk.GSNeOgKQDVgkr6EIhsa2hJ6P4NkJy2Gt8ha', 'aprendiz', 'activo', 'claro', 'email', NULL, NULL, NULL, NULL, 0, NULL, '2026-02-15 23:40:00', 1, '2026-02-17 19:44:36', '2026-02-17 19:44:36', '2026-02-17 19:44:36', 8);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `avatars`
--
ALTER TABLE `avatars`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `avatars_nombre_unique` (`nombre`);

--
-- Indices de la tabla `certificaciones`
--
ALTER TABLE `certificaciones`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_usuario_modulo_cert` (`usuario_id`,`modulo_id`),
  ADD UNIQUE KEY `codigo_certificado` (`codigo_certificado`),
  ADD KEY `idx_codigo` (`codigo_certificado`),
  ADD KEY `idx_usuario` (`usuario_id`),
  ADD KEY `modulo_id` (`modulo_id`),
  ADD KEY `intento_evaluacion_id` (`intento_evaluacion_id`);

--
-- Indices de la tabla `codigo_usuario`
--
ALTER TABLE `codigo_usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_usuario_leccion` (`usuario_id`,`leccion_id`),
  ADD KEY `leccion_id` (`leccion_id`);

--
-- Indices de la tabla `ejercicios`
--
ALTER TABLE `ejercicios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_leccion_orden` (`leccion_id`,`orden`),
  ADD KEY `created_by` (`created_by`);

--
-- Indices de la tabla `evaluaciones`
--
ALTER TABLE `evaluaciones`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_modulo_evaluacion` (`modulo_id`),
  ADD KEY `idx_modulo` (`modulo_id`),
  ADD KEY `created_by` (`created_by`);

--
-- Indices de la tabla `intentos_ejercicios`
--
ALTER TABLE `intentos_ejercicios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_usuario_ejercicio` (`usuario_id`,`ejercicio_id`),
  ADD KEY `ejercicio_id` (`ejercicio_id`),
  ADD KEY `opcion_seleccionada_id` (`opcion_seleccionada_id`);

--
-- Indices de la tabla `intentos_evaluacion`
--
ALTER TABLE `intentos_evaluacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_usuario_evaluacion` (`usuario_id`,`evaluacion_id`),
  ADD KEY `evaluacion_id` (`evaluacion_id`),
  ADD KEY `idx_aprobado` (`aprobado`);

--
-- Indices de la tabla `lecciones`
--
ALTER TABLE `lecciones`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_modulo_slug` (`modulo_id`,`slug`),
  ADD KEY `idx_modulo_orden` (`modulo_id`,`orden`),
  ADD KEY `created_by` (`created_by`);

--
-- Indices de la tabla `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `modulos`
--
ALTER TABLE `modulos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `idx_modulo` (`modulo`),
  ADD KEY `idx_orden` (`orden_global`),
  ADD KEY `created_by` (`created_by`);

--
-- Indices de la tabla `opciones_ejercicio`
--
ALTER TABLE `opciones_ejercicio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_ejercicio` (`ejercicio_id`);

--
-- Indices de la tabla `opciones_evaluacion`
--
ALTER TABLE `opciones_evaluacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_pregunta` (`pregunta_evaluacion_id`);

--
-- Indices de la tabla `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`email`);

--
-- Indices de la tabla `personal_access_tokens`
--
ALTER TABLE `personal_access_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `personal_access_tokens_token_unique` (`token`),
  ADD KEY `personal_access_tokens_tokenable_type_tokenable_id_index` (`tokenable_type`,`tokenable_id`),
  ADD KEY `personal_access_tokens_expires_at_index` (`expires_at`);

--
-- Indices de la tabla `preguntas_evaluacion`
--
ALTER TABLE `preguntas_evaluacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_evaluacion_orden` (`evaluacion_id`,`orden`),
  ADD KEY `created_by` (`created_by`);

--
-- Indices de la tabla `progreso_lecciones`
--
ALTER TABLE `progreso_lecciones`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_usuario_leccion` (`usuario_id`,`leccion_id`),
  ADD KEY `idx_usuario_modulo` (`usuario_id`,`leccion_id`),
  ADD KEY `leccion_id` (`leccion_id`);

--
-- Indices de la tabla `progreso_modulo`
--
ALTER TABLE `progreso_modulo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_usuario_modulo` (`usuario_id`,`modulo_id`),
  ADD KEY `idx_progreso` (`modulo_id`,`porcentaje_completado`),
  ADD KEY `idx_usuario` (`usuario_id`),
  ADD KEY `fk_progreso_modulo_ultima_leccion` (`ultima_leccion_vista_id`);

--
-- Indices de la tabla `ranking`
--
ALTER TABLE `ranking`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_modulo_usuario` (`modulo_id`,`usuario_id`),
  ADD KEY `idx_ranking_modulo` (`modulo_id`,`porcentaje_progreso`,`fecha_ultima_actualizacion`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `respuestas_evaluacion`
--
ALTER TABLE `respuestas_evaluacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_intento` (`intento_id`),
  ADD KEY `pregunta_evaluacion_id` (`pregunta_evaluacion_id`),
  ADD KEY `opcion_seleccionada_id` (`opcion_seleccionada_id`);

--
-- Indices de la tabla `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sessions_user_id_index` (`user_id`),
  ADD KEY `sessions_last_activity_index` (`last_activity`);

--
-- Indices de la tabla `user_attempts`
--
ALTER TABLE `user_attempts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_attempts_user_id_foreign` (`user_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `usuarios_avatar_id_foreign` (`avatar_id`),
  ADD KEY `idx_email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `avatars`
--
ALTER TABLE `avatars`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `certificaciones`
--
ALTER TABLE `certificaciones`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `codigo_usuario`
--
ALTER TABLE `codigo_usuario`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `ejercicios`
--
ALTER TABLE `ejercicios`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `evaluaciones`
--
ALTER TABLE `evaluaciones`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `intentos_ejercicios`
--
ALTER TABLE `intentos_ejercicios`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT de la tabla `intentos_evaluacion`
--
ALTER TABLE `intentos_evaluacion`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `lecciones`
--
ALTER TABLE `lecciones`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=249;

--
-- AUTO_INCREMENT de la tabla `modulos`
--
ALTER TABLE `modulos`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `opciones_ejercicio`
--
ALTER TABLE `opciones_ejercicio`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de la tabla `opciones_evaluacion`
--
ALTER TABLE `opciones_evaluacion`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT de la tabla `personal_access_tokens`
--
ALTER TABLE `personal_access_tokens`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=173;

--
-- AUTO_INCREMENT de la tabla `preguntas_evaluacion`
--
ALTER TABLE `preguntas_evaluacion`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `progreso_lecciones`
--
ALTER TABLE `progreso_lecciones`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT de la tabla `progreso_modulo`
--
ALTER TABLE `progreso_modulo`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `ranking`
--
ALTER TABLE `ranking`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `respuestas_evaluacion`
--
ALTER TABLE `respuestas_evaluacion`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT de la tabla `user_attempts`
--
ALTER TABLE `user_attempts`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=205;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `certificaciones`
--
ALTER TABLE `certificaciones`
  ADD CONSTRAINT `certificaciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `certificaciones_ibfk_2` FOREIGN KEY (`modulo_id`) REFERENCES `modulos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `certificaciones_ibfk_3` FOREIGN KEY (`intento_evaluacion_id`) REFERENCES `intentos_evaluacion` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `codigo_usuario`
--
ALTER TABLE `codigo_usuario`
  ADD CONSTRAINT `codigo_usuario_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `codigo_usuario_ibfk_2` FOREIGN KEY (`leccion_id`) REFERENCES `lecciones` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `ejercicios`
--
ALTER TABLE `ejercicios`
  ADD CONSTRAINT `ejercicios_ibfk_1` FOREIGN KEY (`leccion_id`) REFERENCES `lecciones` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `ejercicios_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `evaluaciones`
--
ALTER TABLE `evaluaciones`
  ADD CONSTRAINT `evaluaciones_ibfk_1` FOREIGN KEY (`modulo_id`) REFERENCES `modulos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `evaluaciones_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `intentos_ejercicios`
--
ALTER TABLE `intentos_ejercicios`
  ADD CONSTRAINT `intentos_ejercicios_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `intentos_ejercicios_ibfk_2` FOREIGN KEY (`ejercicio_id`) REFERENCES `ejercicios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `intentos_ejercicios_ibfk_3` FOREIGN KEY (`opcion_seleccionada_id`) REFERENCES `opciones_ejercicio` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `intentos_evaluacion`
--
ALTER TABLE `intentos_evaluacion`
  ADD CONSTRAINT `intentos_evaluacion_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `intentos_evaluacion_ibfk_2` FOREIGN KEY (`evaluacion_id`) REFERENCES `evaluaciones` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `lecciones`
--
ALTER TABLE `lecciones`
  ADD CONSTRAINT `lecciones_ibfk_1` FOREIGN KEY (`modulo_id`) REFERENCES `modulos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lecciones_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `modulos`
--
ALTER TABLE `modulos`
  ADD CONSTRAINT `modulos_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `opciones_ejercicio`
--
ALTER TABLE `opciones_ejercicio`
  ADD CONSTRAINT `opciones_ejercicio_ibfk_1` FOREIGN KEY (`ejercicio_id`) REFERENCES `ejercicios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `opciones_evaluacion`
--
ALTER TABLE `opciones_evaluacion`
  ADD CONSTRAINT `opciones_evaluacion_ibfk_1` FOREIGN KEY (`pregunta_evaluacion_id`) REFERENCES `preguntas_evaluacion` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `preguntas_evaluacion`
--
ALTER TABLE `preguntas_evaluacion`
  ADD CONSTRAINT `preguntas_evaluacion_ibfk_1` FOREIGN KEY (`evaluacion_id`) REFERENCES `evaluaciones` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `preguntas_evaluacion_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `progreso_lecciones`
--
ALTER TABLE `progreso_lecciones`
  ADD CONSTRAINT `progreso_lecciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `progreso_lecciones_ibfk_2` FOREIGN KEY (`leccion_id`) REFERENCES `lecciones` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `progreso_modulo`
--
ALTER TABLE `progreso_modulo`
  ADD CONSTRAINT `fk_progreso_modulo_ultima_leccion` FOREIGN KEY (`ultima_leccion_vista_id`) REFERENCES `lecciones` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `progreso_modulo_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `progreso_modulo_ibfk_2` FOREIGN KEY (`modulo_id`) REFERENCES `modulos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `ranking`
--
ALTER TABLE `ranking`
  ADD CONSTRAINT `ranking_ibfk_1` FOREIGN KEY (`modulo_id`) REFERENCES `modulos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `ranking_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `respuestas_evaluacion`
--
ALTER TABLE `respuestas_evaluacion`
  ADD CONSTRAINT `respuestas_evaluacion_ibfk_1` FOREIGN KEY (`intento_id`) REFERENCES `intentos_evaluacion` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `respuestas_evaluacion_ibfk_2` FOREIGN KEY (`pregunta_evaluacion_id`) REFERENCES `preguntas_evaluacion` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `respuestas_evaluacion_ibfk_3` FOREIGN KEY (`opcion_seleccionada_id`) REFERENCES `opciones_evaluacion` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `user_attempts`
--
ALTER TABLE `user_attempts`
  ADD CONSTRAINT `user_attempts_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_avatar_id_foreign` FOREIGN KEY (`avatar_id`) REFERENCES `avatars` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
