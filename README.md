# MUNICAOBALOTE
Projeto de TCC

#### BANCO DE DADOS ####

| roubados | CREATE TABLE `roubados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data` varchar(300) DEFAULT NULL,
  `local` varchar(100) DEFAULT NULL,
  `placa` varchar(100) DEFAULT NULL,
  `horario` varchar(200) DEFAULT NULL,
  `tudo` varchar(10000) DEFAULT NULL,
  `data_postagem` date DEFAULT NULL,
  `modelo` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=72978 DEFAULT CHARSET=utf8 |


| balote_auditoria | CREATE TABLE `balote_auditoria` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_telegram` int(11) DEFAULT NULL,
  `mensagem` varchar(10000) DEFAULT NULL,
  `resposta` varchar(10000) DEFAULT NULL,
  `data` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=14210 DEFAULT CHARSET=utf8 |


| balote_encontrados | CREATE TABLE `balote_encontrados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_telegram` int(11) DEFAULT NULL,
  `placa` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=63 DEFAULT CHARSET=utf8 |


| cadastro_balote | CREATE TABLE `cadastro_balote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_telegram` varchar(300) DEFAULT NULL,
  `nome` varchar(300) DEFAULT NULL,
  `batalhao` varchar(300) DEFAULT NULL,
  `nivel` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_telegram` (`id_telegram`)
) ENGINE=MyISAM AUTO_INCREMENT=378 DEFAULT CHARSET=utf8 |


