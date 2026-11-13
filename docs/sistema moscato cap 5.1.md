REPÚBLICA BOLIVARIANA DE VENEZUELA 

MINISTERIO DEL PODER POPULAR PARA LA EDUCACIÓN UNIVERSITARIA 

UNIVERSIDAD POLITECNICA TERRITORIAL AGROINDUSTRIAL 

DEL ESTADO TÁCHIRA 

SEDE SAN CRISTÓBAL – ESTADO TÁCHIRA 

DESARROLLO DE UN SISTEMA DE ESCRITORIO PARA LA GESTION DE PEDIDOS EN EL RESTAURANTE MOSCATO, SAN CRISTOBAL ESTADO TACHIRA. 

Trabajo Presentado como Requisito para Aprobar la Unidad Curricular Proyecto Socio tecnológico II en el Programa Nacional de Formación en Informática, para Optar al Título de Técnico Superior Universitario en Informática. 

AUTORES: 

Castro Rodríguez Manuel A. 

Castellano Anaya Johana L. 

ASESOR ACADÉMICO: 

Ing. Vicenzo Quagliano 

San Cristóbal, Julio 2026. 

Índice general 

RESUMEN iv 

INTRODUCCIÓN 1 

CAPÍTULO I 2 

CONTEXTO DEL PROYECTO 2 

1.1 Identificación De La Comunidad. 2 

1.2 Población beneficiada. 3 

1.3 Organizaciones vinculadas al proyecto. 4 

1.4 Diagnostico Participativo (IAP) 4 

1.5 Cronogramas De Actividades. 5 

1.5 Planteamiento del Problema 6 

1.6.1 Objetivo General: 9 

1.6.2 Objetivos Específicos: 9​ 

1.7 Justificación del Proyecto 9 

CAPITULO II 12 

MARCO TEORICO 12 

2.1 Antecedentes 12 

2.2 Bases teóricas 14 

2.2.1 Gestión administrativa de restaurantes 14 

2.2.2 Base de datos para gestión de pedidos y comandas 15 

2.2.3 Sistema de escritorio en Python e interfaz con tkinter 16 

2.2.4 Control de calidad de software 16 

Fuente: Castellano y Castro (2026) 19 

2.3 Bases legales 19 

2.3.1 Constitución de la República Bolivariana de Venezuela (1999) 19 

2.3.2 Ley de Infogobierno (2014) 20 

2.3.3 Ley Especial contra Delitos Informáticos (2001) 21 

2.3.4 Ley Orgánica de Ciencia, Tecnología e Innovación (LOCTI, 2022) 22 

2.3.5 Decreto Nº 3.390 (2004) 23 

2.4 Definición de Términos Básicos 23 

CAPITULO III 26 

MARCO METODOLOGICO 26 

3.3 Procedimiento Técnico 27 

3.4 Población y Muestra 29 

3.5 Técnicas e Instrumentos para la Recolección de Datos 29 

3.6 Procedimiento para el Análisis de los Datos 30 

3.7 Plan de Acción del Producto o Servicio. 31 

CAPITULO IV 34 

PRODUCTO Y/O SERVICIO. 34 

4.1 Análisis de los Resultados 34 

4.2 Propuesta del Producto o Servicio En función de la metodología técnica. 35 

4.2.1 Objetivo de la Propuesta (Producto o Servicio) 35 

4.2.2 Memoria Descriptiva 35 

CAPITULO V 47 

CONCLUSIONES Y RECOMENDACIONES 47 

5.1 Conclusiones 47 

5.2 Recomendaciones 48 

Índice de figuras. 

Ubicación Geografia de la Comunidad 3 

Árbol del Problema 7 

Diagrama en Casos de Uso 44 

Diagrama de Clases 45 

Diagrama de Estados 46 

Diagrama de Secuencias 47 

Diagrama de Actividades 49 

Índice de Cuadros 

Matriz FODA 6 Cronograma de Actividades 8 

Unidad de Análisis 20 

Plan de acción 35 Índices Financieros 40 Flujo Neto Proyectado (3 años) 40 

REPÚBLICA BOLIVARIANA DE VENEZUELA MINISTERIO DEL PODER POPULAR PARA LA EDUCACIÓN UNIVERSITARIA INSTITUTO UNIVERSITARIO DE TECNOLOGÍA AGROINDUSTRIAL PROGRAMA NACIONAL DE FORMACIÓN EN INFORMÁTICA DESARROLLO DE UN SISTEMA DE ESCRITORIO PARA LA GESTION DE PEDIDOS EN EL RESTAURANTE MOSCATO, SAN CRISTOBAL, ESTADO TACHIRA 

Autores: Castellano A. Johana L. Castro R. Manuel A. Tutor: Quagliano Vincenzo Fecha: septiembre, 2026 

RESUMEN 

El presente proyecto plante el desarrollo de un sistema de escritorio para optimizar la gestión de pedidos y comandas en el Restaurante Moscato, ubicado en San Cristóbal, estado Táchira. En la investigación se diagnosticó como problemática central lo que seria la dependencia de procesos operativos manuales basados en el uso excesivo de papel para el registro de las órdenes, lo cual generaba tiempos de demora prolongados, extravió de tickets y una falta de sincronización entre el área de atención y la cocina. Como respuesta a esta necesidad, el objetivo general consistió en desarrollar una solución tecnológica que automatice el flujo de información utilizando el lenguaje de programación Python, la librería visual CustomTkinter y el gestor de base de datos de MySQL. Para su ejecución, se adoptó un enfoque metodológico cualitativo, de campo y de acción-participación, fundamentado técnicamente en la metodología ágil de Programación Extrema (XP) y apoyado en técnicas de recolección como la observación directa y entrevistas 

semiestructuradas a los informantes clave, siendo el resultado más destacado la implementación de un sistema interactivo que opera a través de una red local, la cual cuenta con interfases adaptadas a los roles de los trabajadores para registrar órdenes digitalmente y actualizar su status de preparación en tiempo real. La conclusión más importante determina que la adopción de esta herramienta tecnológica suprime errores de transcripción manual, agiliza la comunicación bidireccional y provee reportes que son valiosos para la toma de decisiones, fortaleciendo la calidad del servicio y la eficiencia del establecimiento 

Palabras clave: gestión de pedidos, sistema de escritorio, Python, base de datos, metodología XP. 

# INTRODUCCIÓN 

En la actualidad, el sector gastronómico demanda cada vez niveles mas altos de dinamismo, precisión y calidad de atención al cliente. Dentro de este entorno competitivo, la fluidez operativa de un restaurante no solo depende de la calidad de sus platos , sino también de la efectividad con la que se gestiona la información desde el momento en el que el cliente realiza un pedido hasta que esté en su preparación, la integración de herramientas digitales adaptadas a las dinámicas propias del servicio ha demostrado ser el camino optimo para modernizar los flujos de trabajo interno, reducir tiempos de espera y optimizar del control de las operaciones. Bajo este panorama se enmarca la realidad del Restaurante Moscato que durante su trayectoria el local mantuvo un esquema de trabajo tradicional sustentado en el registro manual de comandas mediante papel y lápiz. Esta modalidad originaba diversas fallas operativas cotidianas, tales como demoras en el traslado físico de los pedidos hacia la cocina, eventuales extravíos de tickets durante las horas de mayor afluencia, errores de interpretación en la caligrafía de las órdenes y una marcada desconexión en la comunicación entre el personal de la sala y el del área de preparación. Ante estas limitaciones, el presente proyecto se orientó hacia el desarrollo e implementación de un sistema de escritorio diseñado a la medida de las necesidades del restaurante, siendo el propósito fundamental de esta herramienta reemplazar el 

flujo en papel por uno totalmente digitalizado que interconecta los puestos de trabajo mediante una red local. De esta manera, el sistema permite registrar los pedidos de una forma ágil desde el área de atención, transmitirlos instantáneamente a la cocina para su preparación y ofrecer a la gerencia un control mayor. Como resultado principal, se logró materializar una plataforma estable que redujo significativamente los tiempos de procesamiento de las comandas, elimino por completo las inconsistencias en los pedidos y proporciono un mecanismo automatizado para la generación de reportes elevando tanto la eficiencia operacional como la experiencia general del usuario. Finalmente, con la finalidad de ofrecer una estructura clara y ordenada de la 

investigación, el informe se distribuye en cinco capítulos fundamentales: Capítulo I (Contexto del Proyecto): contiene el planteamiento de la problemática, los objetivos formulados y la justificación del estudio. Capítulo II (Marco Teórico): este reúne los antecedentes, referentes teóricos y las bases legales que sustentan la propuesta. Capítulo III (Marco Metodológico): Donde se detallan el enfoque de investigación, los instrumentos de recolección de datos y el proceso del desarrollo aplicado. Capítulo IV (Diseño e Implementación): En el cual se presentan la arquitectura del sistema, el diseño de las pantallas operativas y las pruebas de usabilidad realizadas. Capitulo V (Conclusiones y Recomendaciones): donde se exponen las síntesis finales en función de los objetivos y las orientaciones para la sostenibilidad de la herramienta en el tiempo. 

CAPÍTULO I 

CONTEXTO DEL PROYECTO 

Identificación De La Comunidad. 

El Restaurante Moscato que surge en San Cristóbal en 2020, un establecimiento que se dedica al sector gastronómico con un enfoque en la elaboración de platos de comida china. Este negocio cumple un rol activo al ofrecer servicios de consumo en sitio y atención de pedidos externos, tomando así posición como una fuente de actividad económica local en cuanto al área gastronómica. 

El establecimiento se encuentra ubicado en la ciudad de San Cristóbal, capital del estado Táchira, específicamente dentro de la jurisdicción de la Parroquia la concordia en el Municipio San Cristóbal. El inmueble en la avenida 19 de abril situándose justo en frente de la universidad nacional experimental de la seguridad (UNES), Esta ubicación presenta un flujo constante de personas lo que genera una buena dinámica económica. 

Figura 1. Ubicación geográfica de la Comunidad 

1 

Fuente: Google maps (2026) 

Se describen como el restaurante que abre la oportunidad a una evolución culinaria única en la región, cuya historia es una prueba real de adaptación y resiliencia. En el pasado, el local funcionó como sede de “Metro Café”, una panadería tradicional de referencia para los habitantes de San Cristóbal; sin embargo, ante las complejidades socioeconómicas del sector comercial, el negocio cerró sus puertas para iniciar una transformación profunda. Esta reestructuración total culminó con la fundación de "Moscato", migrando del concepto convencional hacia una propuesta gastronómica internacional. 

Misión: Brindar a las personas un espacio donde vivan experiencia gastronómica internacional que pueda satisfacer sus paladares, fusionando sabores extraordinarios adaptados al paladar local. 

Visión: Esta proyectada a la modernización de sus servicios, aspirando a mediante herramientas tecnológicas puedan agilizar muchos procesos operativos y poder brindar mejor atención. 

Objetivo General: Pretendemos ser una organización gastronómica altamente reconocida en la ciudad por la excelencia y rapidez en el servicio al cliente, la impecable presentación de nuestros platos internacionales y la sincronización perfecta de nuestras operaciones en sala y cocina a través de herramientas de software avanzadas. 

1.2 Población beneficiada. 

La población beneficiada con la implementación del sistema de escritorio en el Restaurante Moscato se divide en dos categorías fundamentales. De manera directa, el proyecto favorece a un equipo de cinco trabajadores: un administrador responsable de la gestión contable y gerencial, dos encargados de atención al cliente en salón quienes también realizan el registro digital de pedidos, y dos operadores en el área de 

cocina dedicados a la elaboración de los platos según las comandas recibidas. Este grupo, compuesto por hombres y mujeres en edad adulta, optimizará sus labores mediante la automatización de tareas y la eliminación de métodos analógicos. Por otra parte, los beneficiarios indirectos abarcan una afluencia estimada de mil cien clientes mensuales, quienes experimentarán una mejora sustancial en la precisión y rapidez de su servicio. Asimismo, la modernización tecnológica fortalece la competitividad del restaurante, proyectando una imagen de eficiencia que beneficia al desarrollo comercial del sector. 

# 1.3 Organizaciones vinculadas al proyecto. 

El desarrollo del presente proyecto socio tecnológico se fundamenta 

en la unión entre el sector académico y el sector productivo local, estableciendo un vínculo directo con el Restaurante Moscato como la organización base que suministra la información y el escenario operativo para la implementación del sistema. De igual manera, se encuentra vinculada de manera institucional la Universidad Politécnica Territorial Agroindustrial del Estado Táchira (UPTAIET), la cual, a través del Programa Nacional de Formación en Informática, proporciona el soporte académico y metodológico necesario para la ejecución de la propuesta. 

1.4 Diagnostico Participativo (IAP) 

Con base en el diagnóstico participativo y la observación directa realizada en las instalaciones del restaurante Moscato, se logró identificar el punto crítico que afecta la operatividad diaria: la gestión ineficiente de los pedidos a través de procesos estrictamente manuales. A partir de este análisis en conjunto con el personal, se determinaron de manera estructurada las causas fundamentales que originan esta situación y los efectos negativos que repercuten directamente en la calidad del servicio, elementos que se esquematizan a continuación mediante el Árbol del Problema: 

Cuadro 1. Matriz FODA 

Análisis interno 

Análisis externo 

Fortalezas (F) 

Disposición de la gerencia y el personal para adoptar nuevas tecnologías y mejorar el servicio. 

Cuentan con un equipo de trabajo (meseros y cocineros) que conoce perfectamente el menú y la dinámica del local. 

Ubicación estratégica lo que garantizara un flujo constante de 

persona y buena dinámica económica. 

Base de clientes fidelizados que valoran la propuesta y calidad gastronómica del lugar. 

Oportunidades (O) 

Desarrollo de un sistema de escritorio a la medida mediante el proyecto socio tecnológico (PFN informática) 

Uso de herramientas de software libre (Python y MySQL) que reducen costos de licencias y se alinean a las leyes tecnológicas del país. 

Atracción de nuevos clientes al reducir los tiempos de espera y mejorar la imagen corporativa del restaurante. 

Capacitación gratuita para los empleados por parte de los desarrolladores. 

Debilidades (D) 

Toma de pedidos (comandas) manuales en papel, susceptibles a tachaduras, ilegibilidad o perdida. 

Deficiencia en la comunicación rápida entre el área de las mesas y la cocina. 

Retrasos y susceptibilidad a errores matemáticos al momento de calcular y totalizar manualmente los consumos de cada mesa. 

Inexistencia de una base de datos estructurada que permita generar reportes de auditoria o análisis de productos. 

Amenazas (A) 

Pérdida de clientes por insatisfacción debido a pedidos erróneos o tiempos de espera prolongados en horas pico. 

Competencia de otros restaurantes en San Cristóbal que ya cuentan 

con procesos de atención automatizados. 

Descontrol administrativo a largo plazo por falta de un registro histórico de ventas confiable. 

Fluctuaciones o cortes imprevistos en el servicio eléctrico de la región, lo cual representa un riesgo para la continuidad operativa y la vida útil de los equipos. 

cuadro 1 Matriz FODA 

Fuente: Castellano y Castro (2026) 

Figura 2. Árbol del problema. 

2 

2 

# 1.5 Cronogramas De Actividades. 

En este apartado se incluyen las actividades que se van a desarrollar para la ejecución del informe del Proyecto Socio Tecnológico II. Se hace el uso de diagrama de Gantt para ilustrar el cronograma. 

Cuadro 2. cronograma de actividades 

Tiempo 

Actividades 

Marzo 

Abril 

Mayo 

Junio 

Julio 

Agosto 

1 

2 

3 

4 

1 

2 

3 

4 

1 

2 

3 

4 

1 

2 

3 

4 

1 

2 

3 

4 

1 

2 

3 

4 

Elegir comunidad 

Ubicar información de la comunidad 

Elaborar Capítulos I y II 

Elaborar Capítulo III 

Elaborar Capítulos 

IV y V 

Defensa pública 

Entrega informe final 

cuadro 2 Cronograma de Actividades 

Fuente: Castellano y Castro (2026) 

# 1.5 Planteamiento del Problema 

En la actualidad a nivel mundial, la industria gastronómica enfrenta el reto de optimizar la eficiencia en la toma de pedidos, donde el uso de métodos tradicionales como el lápiz y el papel para registrar comandas representa un problema significativo que afecta la sostenibilidad de cualquier negocio. La digitalización en 

restaurantes mejora la eficiencia operativa, reduce pérdidas y proporciona datos para tomar decisiones. La implementación de tecnología en la gestión de pedidos automatiza procesos, elimina los tiempos de espera por errores en transcripciones manuales, mejora la experiencia del cliente y aumenta la satisfacción de los trabajadores. Los sistemas de información integrados disminuyen los errores humanos y facilitan la comunicación entre las distintas áreas, dejando en evidencia que las organizaciones que no se adaptan a tales tendencias tecnológicas pueden llegar a enfrentar severas 

desventajas en la calidad y rapidez de su atención. A nivel general, la gestión de pedidos representa la columna vertebral de estos procesos; si la transmisión de información en esta fase falla debido a errores en comandas escritas manualmente, se desencadena un efecto dominó que compromete toda la estructura operativa y administrativa. En contexto de Latinoamérica, las pequeñas y medianas empresas de restaurantes operan bajo entornos económicamente exigentes que demandan una estricta optimización de costos y tiempos, especialmente en la gestión de pedidos y comandas. Estas empresas suelen mantener sistemas operativos atrasados debido a la falta de adopción de tecnologías adaptadas a sus necesidades diarias. Esta ausencia de automatización genera fallas persistentes en la sincronización entre el área de pedidos y la cocina, exponiendo a los negocios locales a vulnerabilidad operativa al depender casi exclusivamente de comandas artesanales escritas en papel. En el caso específico de Venezuela, un estudio sobre tendencias de innovación digital en PYMES confirma que la mayoría de los restaurantes se encuentra en etapas iniciales de madurez digital, con oportunidades de mejora específicas en automatización de procesos internos como la gestión de pedidos y logística. Por lo que, el desarrollo de un sistema de escritorio de gestión de pedidos que digitaliza las comandas para agilizar su envío a la cocina responde directamente a esta necesidad de automatización operativa en el sector servicios. Concretamente en el estado Táchira, esta problemática es evidente de manera directa en el restaurante “Moscato”, El conflicto central en el restaurante reside en la absoluta dependencia que existe con los procesos manuales para la gestión de pedidos y comandas dentro del restaurante, bajo este modelo, el flujo de información desde que el 

cliente realiza su orden hasta que el platillo empieza su preparación depende de registros escritos a mano y desplazamientos físicos constantes del personal. De esta manera, este método artesanal presenta una vulnerabilidad en su estructura: la alta susceptibilidad al error humano; A la falta de legibilidad en las notas se le suma el hecho de que los tickets físicos son muy susceptibles a extraviarse, duplicarse en un lugar tan dinámico como lo es una cocina. Bajo esa perspectiva, la dinámica actual obliga al personal de la sala a moverse repetidamente entre las mesas y el área de producción para entregar las órdenes, lo que genera una latencia incensaría en el servicio; La ausencia de una canal de comunicación eficiente y automatizado evita que la información llegue de forma inmediata y estandarizada a la cocina; Especialmente durante las horas de mayor frecuencia de cliente o “picos de demanda. Como indica Walker y Lundberg (2021) “Los sistemas manuales de comandas incrementan los tiempos de espera en un 25-40% durante horas pico, generando cuellos de botella que reducen la satisfacción del cliente y la rotación de mesas" (p. 312). La saturación del sistema manual genera cuellos de botella que escalan con los tiempos de espera provocan confusión en la secuencia de salida de los platos a las mesas. De persistir esta situación el restaurante se enfrentaría a un escenario de colapso operativo. La saturación del sistema manual continuará provocando demoras lo que a mediano plazo comprometerá la rentabilidad, el control interno del negocio. Tomando en cuenta esta realidad resulta inevitable la necesidad de intervenir en el proceso mediante el desarrollo de un sistema de gestión de pedidos. Esta alternativa tecnológica propone digitalizar todo el flujo de trabajo ya que el mesero registrara la orden desde una laptop en la sala, eliminando así la necesidad de ir y venir constantemente físicamente hacia el área de preparación, el pedido será recibido de manera instantánea en una segunda laptop ubicada en una parte estratégica en la cocina, a través de esta interfaz, el cocinero podrá aceptar la orden y, una vez este culminada la preparación, notificar al sistema del mesero que el pedido está listo para ser llevado a los comensales, garantizando así una comunicación estandarizada, bidireccional y en tiempo real. En función de lo planteado y con el propósito de guiar el proyecto de investigación hacia el diseño de la solución tecnológica mencionada, se formulan las siguientes interrogantes: 

¿Cuál es la situación actual de los procesos de toma de pedidos y flujo de información dentro del restaurante de comida china Moscato? 

¿Cuáles son los requerimientos técnicos y funcionales necesarios para diseñar un sistema que integre la toma de órdenes en sala con la recepción y notificación de estatus mediante una segunda laptop en el área de cocina? 

¿De qué manera la automatización de las comandas mediante una interfaz digital bidireccional optimizará la coordinación del personal y mejorará el control interno del establecimiento? 

1.6 Objetivos Del Proyecto 

1.6.1 Objetivo General: 

Desarrollar un sistema de escritorio para la gestión de pedidos utilizando Python, CustomTkinter y MySQL para optimizar los procesos operativos del restaurante "Moscato" en San Cristóbal, estado Táchira. 

1.6.2 Objetivos Específicos:​ 

Identificar las necesidades actuales al momento del manejo de​ pedidos y el flujo de la información dentro del restaurante para basarse en esas necesidades. 

Diseñar una base de datos relacional en MySQL para el​ almacenamiento de productos, mesas y registros de ventas. 

Programar la interfaz gráfica de la aplicación mediante la librería​ CustomTkinter, incorporando la generación de reportes que sirvan para la toma de decisiones de la organización. 

Realizar pruebas de funcionamiento y usabilidad que garantice la​ correcta operabilidad del sistema de escritorio. 

1.7 Justificación del Proyecto 

Este estudio se justifica plenamente en la necesidad de modernizar 

y automatizar flujos operativos del restaurante Moscato, donde la evolución de métodos manuales a un entorno digitalizado no solo representa una mejoría únicamente estética, sino una solución integral a nudos críticos de gestión. Al respecto Laudon, 

K. C., y Laudon, J. P. (2022) establecen que, en la economía digital actual, las organizaciones que no implementan sistemas de información integrados enfrentan desventajas competitivas significativas, detallando además que la automatización de procesos operativos, como la gestión de pedidos, puede mejorar la eficiencia en un 30-50% y reducir costos operativos sustancialmente. Sobre esta base conceptual, la investigación favorece al fortalecimiento del conocimiento sobre la automatización de procesos internos, sirviendo como antecedente valioso para futuros estudios que busquen optimizar la gestión en el sector socio productivo gastronómico. Desde la perspectiva técnica, este proyecto permite materializar el "saber hacer" mediante el diseño y desarrollo de un sistema de escritorio que integra software y equipos de procesamiento de forma eficiente. El aporte técnico radica en la creación de un sistema de comunicación bidireccional que vincula la toma de pedidos en sala, gestionada desde una primera laptop, con su recepción inmediata y control de estatus a través de una segunda laptop ubicada en el área de cocina. Esto se traduce en un incremento directo de la eficacia operativa, eliminando la redundancia de tareas, suprimiendo por completo la dependencia del papel (frente a comandas manuales o tickets impresos) y optimizando el flujo de datos en tiempo real dentro de las instalaciones de Moscato. En cuanto al contexto estudiantecomunidad, la realización de este proyecto ha permitido una interacción directa con la realidad laboral del restaurante, agilizando la detección de anomalías que afectan el clima organizacional y la calidad del servicio. A través de la observación y vivencia en el sitio, se identificó que el estrés laboral y la desorganización en horas de alta demanda son factores que pueden mitigarse con una herramienta tecnológica adecuada. Desde el punto de vista social, el impacto se refleja en la mejora sustancial de las condiciones de trabajo para los meseros y cocineros. Al contar con una interfaz digital que organiza visualmente las órdenes y permite notificar cuando un plato está listo sin necesidad de desplazamientos físicos, el personal experimenta una reducción en 

la carga de trabajo físico y mental, promoviendo una cultura de orden y profesionalismo que beneficia tanto a los trabajadores como a la comunidad de usuarios que frecuentan el establecimiento. Finalmente, este proyecto se encuentra estrechamente vinculado con el Plan de Desarrollo Económico y Social de la Nación, enmarcado en las políticas de soberanía tecnológica. La propuesta se alinea con las directrices que buscan el desarrollo de soluciones informáticas nacionales que impulsen la eficiencia de las organizaciones, contribuyendo a la independencia técnica del sector comercial. Asimismo, se inserta en las Líneas de Investigación del PNF en Informática, específicamente en el desarrollo de software y gestión de datos, cumpliendo con la transversalidad del eje Proyecto. Esta integración multidimensional de saberes demuestra cómo la academia y la tecnología se ponen al servicio de la resolución de problemas reales en las comunidades y organizaciones, elevando la calidad de vida y fortaleciendo el tejido productivo del país a través de la innovación aplicada. 

# CAPITULO II 

MARCO TEORICO 

2.1 Antecedentes 

En el orden internacional se presenta a Byron Mauricio Ramírez Nastacuas (2023) el cual hizo un proyecto de investigación en Ecuador denominado "Sistema web y aplicación móvil para la gestión de pedidos en el restaurante “La Aduana”", presentado en la Universidad Pontificia del Ecuador Sede Ibarra. 

La presente investigación se desarrolló con el propósito de realizar una herramienta tecnológica que ayude para la toma de pedidos, y la gestión de ventas. El cual le permitirá innovar dentro del restaurante ofreciendo un servicio más rápido reduciendo el tiempo para tomar la orden a su vez evitar órdenes equivocadas a la hora de servir el plato, y mejor calidad para los clientes, el cual es una ayuda para los meseros olvidando ya la nota pagable para las 

órdenes, al mismo tiempo una ayuda para la parte de administración ofreciendo una importante asistencia para monitorear el rendimiento de las ventas dentro del establecimiento. Y para ello contara con un aplicativo móvil para la realizar las órdenes a los clientes en el cual se basará en el formato de comanda, y para la parte de la administración contara con un aplicativo web para visualizar las actividades diarias y visualizar sus ventas. (p.1) 

Tomando como base el anterior trabajo de investigación, su vinculación ayuda a comprobar lo efectivo que puede resultar la erradicación del papel mediante la comunicación digital entre áreas, también validando la separación de interfaces según su rol como usuario, lo que optimiza significativamente el control interno. 

En el punto de vista nacional se encuentra Kevin Peraza (2024) quien presentó un proyecto especial de grado en Palo Negro, estado Aragua titulado “Análisis del control de inventario y sus implicaciones en mejores prácticas de gestión de materias primas en el restaurante McDonald's del Centro Comercial Parque Los Aviadores, Palo Negro”, presentado en el Instituto Universitario de Tecnología de Administración Industrial (IUTA) Extensión Maracay. 

El presente trabajo de grado tiene como finalidad analizar el control de inventario y sus implicaciones en las mejores prácticas de gestión de materias primas en el restaurante McDonald's del Centro Comercial Parque Los Aviadores. Esta investigación de modalidad de Proyecto Factible, viable y de nivel descriptivo, apoyada en una investigación de campo y de carácter documental, utilizará técnicas e instrumentos de recolección de datos tales como la observación directa y la aplicación de entrevistas semiestructuradas dirigidas al personal administrativo y operativo de cocina. Tras analizar el diagnóstico, se determinó que la ausencia de sistemas automatizados de control inmoviliza valiosos recursos financieros e incrementa considerablemente los costos de pedidos al no contar con un seguimiento síncrono del stock. Así, se concluye que un manejo dinámico y parametrizado del inventario de insumos es crítico para evitar mermas de almacén, garantizando la operatividad del establecimiento y resguardando la rentabilidad general de la empresa. (p.11) 

El antecedente ya mencionado habla sobre la importancia de la evaluación de la gestión del stock para que el aprovisionamiento de insumos sea idóneo. Esto aporta un excelente valor a este proyecto al demostrar que el procesamiento de las comandas y los pedidos realizados en el salón no debe operar de manera aislada, sino estrechamente integrado con una base de datos relacional local que actualice e interactúe dinámicamente con las existencias de ingredientes en cocina para evitar pérdidas monetarias y quiebres de inventario. 

En el ámbito estatal están Desirre Lisbeth Suarez Segura y Yorman Josue Galindo Pastran (2024) quienes presentaron un proyecto de investigación en la comunidad de San Cristóbal, estado Táchira titulado “Plataforma web integrada para la gestión de pedidos, control de inventario, recursos humanos, compras y generación de reportes de ventas en una empresa”, presentado en la Universidad Nacional Experimental del Táchira (UNET). 

El presente proyecto tiene su campo de acción en el sector socio productivo de San Cristóbal, estado Táchira y tiene como objetivo general desarrollar una plataforma informática integrada para la automatización, control y centralización del flujo de pedidos, compras, inventarios de productos, gestión de personal y reportes estadísticos de ventas con la finalidad de elevar la productividad empresarial. Esta investigación se encuadró bajo metodologías formales de ingeniería de software para el desarrollo y 

despliegue ágil, abordando las etapas de levantamiento de requisitos de negocio, diseño de la arquitectura del backend y frontend del sistema, modelado relacional de la base de datos, codificación de los módulos y ejecución de pruebas funcionales. Al culminar el estudio, se llegó a la conclusión de que la automatización de la comanda y la gestión operativa mediante bases de datos relacionales previene la pérdida de registros físicos por transcripción incorrecta, suprime la redundancia de tareas y optimiza drásticamente la comunicación síncrona entre el área de salón y la cocina en tiempo real. 

Según el anterior trabajo de investigación, da a conocer la posibilidad de la creación de un sistema amplio que cubra las necesidades transaccionales de la empresa utilizando bases de datos 

relacionales integradas de manera interactiva. Esta información es de gran aporte para este proyecto, ya que confirma que en el contexto local andino el uso de motores relacionales de almacenamiento local (como MySQL Server) representa la estrategia de diseño óptima para interconectar con total consistencia las terminales de sala y cocina a través de la red WiFi interna del restaurante sin riesgo de caídas operativas ante la inestabilidad de la conexión a internet de la región. 

# 2.2 Bases teóricas 

Las bases teóricas proporcionan el marco conceptual necesario para sustentar el desarrollo del sistema de gestión de pedidos para un restaurante. A continuación, se presentan los conceptos clave aplicados en esta investigación. 

# 2.2.1 Gestión administrativa de restaurantes 

La gestión administrativa en los restaurantes requiere de instrumentos que permitan organizar de forma eficiente los pedidos, coordinar al personal y mejorar la calidad del servicio que se ofrece. Por lo tanto, la automatización de procesos se ha vuelto en una herramienta clave para optimizar la operatividad del negocio. Mantilla S. (2026) señalan que 

La integración de tecnología y gestión digital optimiza profundamente el sector de servicios, impulsando la evolución de los sistemas de pedidos en restaurantes; aquí herramientas como automatización 

y quioscos de autoservicio son ya indispensables, pues un estudio reciente sobre su usabilidad confirmó un diseño de interfaz óptimo mejora drásticamente, la experiencia y comprensión del usuario, minimizando errores e incrementando eficiencia y satisfacción en el 

proceso de pedido (p. 38) 

Este planteamiento valida que la implementación de soluciones tecnológicas no solo mejora la eficiencia operativa, sino que 

también fortalece la experiencia del usuario y facilita la comunicación de las distintas áreas del restaurante. De igual manera, Burgos Cando (2015) afirma en su investigación que el principal objetivo de un sistema de pedidos es “mejorar la gestión de pedidos en los restaurantes” y ofrecer un servicio más ágil, permitiendo mostrar los pedidos realizados y que su llegada a la cocina sea un poco más rápida. En función de ello, se puede afirmar que el desarrollo de un sistema de gestión de pedidos para un restaurante contribuye a reducir errores, agilizar la atención y garantizar un mejor control administrativo del establecimiento. 

2.2.2 Base de datos para gestión de pedidos y comandas 

La gestión eficiente de los procesos operativas y administrativas en un entorno gastronómico exige el uso de bases de datos capaces de registrar, organizar y conectar entidades dinámicas como mesas, pedidos, catálogo de productos y flujo de comandas. Según Coronel y Morris (2017), el diseño estructurado de una base de datos es el núcleo de cualquier sistema transaccional que busque la eficiencia y la disminución de errores. En su obra explican: 

La implementación del modelo relacional en los sistemas de información empresariales permite estructurar los datos en tablas lógicamente independientes, pero interconectadas a través de claves. Esta arquitectura elimina la redundancia y asegura la integridad referencial durante el procesamiento de transacciones, garantizando que el registro de ventas, inventarios y operaciones diarias se realice de manera consistente y con alta disponibilidad para la toma de decisiones. (p. 54) 

Este concepto es fundamental para el presente proyecto, ya que el diseño de la base de datos mediante MySQL representa la base estructural del sistema de Moscato. A través de este modelo relacional, se organizará de manera lógica la información 

correspondiente a la distribución de las mesas, el menú de productos y los pedidos detallados. Esto permitirá que la digitalización de la comanda se ejecute de forma automatizada y completa, asegurando que los pedidos fluyan sin pérdida de información y garantizando así que los datos almacenados sean lo 

más preciso para la una mejor armonía y gestión administrativa. 

2.2.3 Sistema de escritorio en Python e interfaz con Customtkinter 

En el desarrollo de software local, no es suficiente con solo estructurar una lógica interna y la base de datos, es indispensable proporcionar al usuario un entorno visual (ventanas, botones y cuadros de texto) que le permita tener interacción con el sistema sin necesidad de conocer el código de programación, Para ello, el lenguaje de python integra librerías nativas orientadas a la construcción de interfaces gráficas. Por lo que en la documentación oficial de la Python Software Foundation (2024), en su apartado sobre preguntas frecuentes sobre la interfaz gráfica de usuario, expone lo siguiente: 

Los empaquetados estándar de Python incluyen una interfaz orientada a objetos para el conjunto de widgets de Tcl/Tk, llamada tkinter. Esta es probablemente la más fácil de instalar (ya que viene incluida con la mayoría de las distribuciones binarias de Python) y usar Tcl/Tk es totalmente portable a macOS, Windows y plataformas Unix. Dependiendo de a qué plataforma o plataformas estés apuntando, hay también múltiples alternativas, pero Tkinter provee el conjunto estándar. 

Tomando como base esta arquitectura nativa para el desarrollo del sistema se seleccionó la librería CustomTkinter, la cual funciona como una extensión avanzada sobre Tkinter, esta herramienta conserva la portabilidad, ligereza y estructura orientada a objetos del estándar de Python, pero añade componentes visuales modernos, personalizables y ergonómicos (como estilos actualizados y soporte nativo para temas claros y oscuros). La integración de CustomTkinter permite programas de manera eficiente las distintas pantallas requeridas por la organización, como la recepción de pedidos y la visualización en la cocina, 

garantizando una interfaz intuitiva para el personal operativo y facilitando la incorporación de módulos para la generación de reportes. 

2.2.4 Control de calidad de software 

La fase final en la construcción de cualquier sistema no se limita únicamente a la escritura de código, sino también a la verificación exhaustiva de su correcto funcionamiento y fiabilidad, por lo tanto, para que un sistema sea considerado apto para operar en un entorno real, debe someterse a ciertos procesos de evaluación que validen cómo se comporta frente a los usuarios. Con relación a esto, López Echaverry et al. (2008) explican lo siguiente respecto a los procesos de garantía en cuanto a la calidad. 

La garantía de calidad se inicia con las acciones que se realizan durante la planificación como el conjunto de procedimientos, técnicas y herramientas durante el ciclo de vida, las actividades de auditoria tales como revisiones técnicas o inspecciones, optimizando los criterios de correctitud y completitud y las funciones de información de la gestión, más orientadas a la documentación y al desarrollo de pruebas (p. 328). 

Tomando en cuenta lo planteado por los autores, la calidad del software no es una situación aislada al finalizar el proyecto, sino la ejecución de pruebas que verifican la exactitud del programa. En el caso del sistema de escritorio Moscato, este principio es el fundamento de la fase de validación, así que, aplicar un control de calidad permitirá someter el aplicativo a pruebas de funcionamiento, garantizando que la interfaz gráfica sea altamente intuitiva para el personal del restaurante. 

Cuadro 3. Unidad de análisis 

Objetivo general: Desarrollar un sistema de escritorio para la gestión de pedidos utilizando Python, CustomTkinter y MySQL para optimizar los procesos operativos del restaurante "Moscato" en San Cristóbal, estado Táchira. 

OBJETIVOS ESPECIFICOS 

UNIDAD DE ANÁLISIS 

CATEGORÍAS 

SUBCATEGORIAS 

Identificar las necesidades actuales al momento del manejo de pedidos y el flujo de la información dentro del restaurante para basarse en esas necesidades. 

Cuál es el proceso actual de atención al cliente, toma de pedidos y comunicación interna del Restaurante Moscato. 

. Gestión de pedidos 

. Flujo de información 

Formato de registro de la orden. 

Incidencia de errores o perdidas de comandas. 

Tiempos de toma en los pedidos. 

Canal de transmisión de información sala-cocina. 

Tiempo de respuesta y atención. 

Diseñar una base de datos relacional en MySQL para el almacenamiento de productos, mesas y registros de ventas. 

El modelo de los datos y la arquitectura técnica del formato de almacenamiento de información. 

. Modelado de base de datos 

. Especificaciones de datos. 

Entidades (Tablas: Empleados, usuario, pedido, mesa, detalle del pedido, producto) 

Relaciones 

Definición de campos y tipos de datos. 

Programar la interfaz gráfica de la aplicación mediante la librería CustomTkinter, incorporando la generación de reportes que sirvan para la toma de decisiones de la organización. 

El desarrollo de la interfaz gráfica y los módulos funcionales de reportes. 

. Interfaz gráfica de usuario (GUI) 

. Sistema de reportes gerenciales 

Diseño de componentes visuales (Ventanas, botones, formularios) 

Implementación técnica con librería Customtkinter. 

Generación de informes (Productos vendidos) 

Uso de la información 

para toma de decisiones. 

Realizar pruebas de funcionamiento y usabilidad que garantice la correcta operabilidad del sistema de escritorio. 

El sistema de escritorio de Moscato durante su fase de validación. 

. Control de calidad de software 

. Pruebas de usabilidad. 

Validación de funcionamiento. 

Detección y corrección de errores. 

Rapidez y eficiencia en la interacción. 

cuadro 3 Unidad de Análisis 

Fuente: Castellano y Castro (2026) 

2.3 Bases legales 

El marco legal del desarrollo del sistema de escritorio para la gestión de pedidos del Restaurante Moscato se fundamenta en 

diversas normativas nacionales que regulan el uso de tecnologías de información, el fomento de la innovación técnica, el acceso seguro a los datos y el resguardo de la propiedad informática. A continuación, se presentan las principales leyes que respaldan este proyecto. 

2.3.1 Constitución de la República Bolivariana de Venezuela (1999) 

La Constitución de Venezuela establece principios fundamentales que garantizan el acceso a la información y promueven el uso de tecnologías de información en distintos ámbitos. El Estado debe garantizar el acceso universal a la información mediante servicios públicos de comunicación, incluyendo plataformas tecnológicas de informática. Sobre este aspecto, el texto constitucional establece: 

Artículo 108. Los medios de comunicación social, públicos y 

privados, deben contribuir a la formación ciudadana. El Estado 

garantizará servicios públicos de radio, televisión y redes de bibliotecas e informática, con el fin de permitir el acceso universal 

a la información. Los centros educativos deben incorporar el 

conocimiento y aplicación de las nuevas tecnologías, de sus 

innovaciones, según los requisitos que establezca la ley. (p.45) 

Asimismo, el Estado reconoce la importancia de la ciencia y la tecnología como instrumentos fundamentales para el desarrollo nacional. 

Artículo 110. El Estado reconocerá el interés público de la ciencia, 

tecnología, el conocimiento, la innovación y sus aplicaciones y los servicios de información necesarios por ser instrumentos fundamentales para el desarrollo económico, social y político del país, así como para la seguridad y soberanía nacional. Para el 

fomento y desarrollo de esas actividades, el Estado destinará recursos suficientes y creará el sistema nacional de ciencia y tecnología de acuerdo con la ley. (p.45) 

Estas disposiciones respaldan el desarrollo de proyectos tecnológicos en el país, asegurando que el Restaurante Moscato pueda implementar un sistema de escritorio local que optimice sus procesos de pedidos y comandas utilizando herramientas de software avanzadas y ajustadas a los marcos institucionales. 

2.3.2 Ley de Infogobierno (2014) 

La Ley de Infogobierno establece los principios, bases y lineamientos que rigen el uso de tecnologías de información para mejorar los servicios y garantizar la transparencia del sector tecnológico. Se define el propósito de la ley, indicando lo siguiente: 

Artículo 1. Esta Ley tiene por objeto establecer los principios, 

bases y lineamientos que rigen el uso de las tecnologías de información en el Poder Público y el Poder Popular, para mejorar 

la gestión pública y los servicios que se prestan a las personas; impulsando la transparencia del sector público, la participación y el ejercicio pleno del derecho de soberanía, así como promover 

el desarrollo de las tecnologías de información libres en el Estado; garantizar la independencia tecnológica; la apropiación social del conocimiento; así como la seguridad y defensa de la Nación. (p.1) 

En relación con el uso de software libre y estándares abiertos en el ecosistema nacional, el Artículo 34 establece los criterios obligatorios para el Poder Público en las actividades de desarrollo e 

implementación tecnológica. Sobre este aspecto, el artículo señala: 

Artículo 34. El desarrollo, adquisición, implementación y uso de las Tecnologías de información por el Poder Público, tiene 

como base el conocimiento libre. En las actuaciones que se 

realicen con el uso de las tecnologías de información, solo se emplearán programas informáticos en software libre y estándares abiertos para garantizar al Poder Público el control sobre las 

tecnologías de información empleadas y el acceso de las personas a los servicios prestados. (p.13) 

Debido a que el presente proyecto es concebido y desarrollado bajo el soporte de la Universidad Politécnica Territorial Agroindustrial del Estado Táchira (UPTAIET), la ley provee un marco normativo que respalda la creación de soluciones basadas en código libre. De este modo, la elección de Python, CustomTkinter y MySQL para el sistema del Restaurante Moscato cumple perfectamente con estas directrices de independencia tecnológica y apropiación social del conocimiento. 

2.3.3 Ley Especial contra Delitos Informáticos (2001) 

Esta ley establece regulaciones sobre la seguridad informática, la prevención de delitos informáticos y la protección de datos personales almacenados en sistemas digitales. En el Artículo 1, se establece el propósito de la normativa, señalando: 

Artículo 1. La presente Ley tiene por objeto la protección integral 

de los sistemas que utilicen tecnologías de información, así como la 

prevención y sanción de los delitos cometidos contra tales sistemas 

o cualquiera de sus componentes, o de los cometidos mediante el 

uso de dichas tecnologías, en los términos previstos en esta Ley. (p.1) 

El Artículo 20 aborda el resguardo de la privacidad de la información de carácter personal, estableciendo rigurosas sanciones penales y financieras para quienes accedan, utilicen o alteren estos registros sin autorización del titular. En este artículo se menciona: 

Artículo 20. Toda persona que intencionalmente se apodere, utilice, modifique o elimine por cualquier medio, sin el 

consentimiento de su dueño, la data o información personales 

de otro o sobre las cuales tenga interés legítimo, que estén 

incorporadas en un computador o sistema que utilice tecnologías 

de información, será penada con prisión de dos a seis años y multa de doscientas a seiscientas unidades tributarias. (p.5) 

El sistema de escritorio del Restaurante Moscato debe cumplir estrictamente con esta ley para garantizar el resguardo de la información de sus clientes, las comandas diarias y el control de caja. La implementación de roles de usuario (administrador, mesero y cocina) protegidos por claves de autenticación en MySQL asegura que los datos sean manejados con total ética, integridad y apego a la ley. 

2.3.4 Ley Orgánica de Ciencia, Tecnología e Innovación (LOCTI, 2022) 

En concordancia jerárquica, esta ley orgánica promueve la innovación científico-tecnológica nacional para responder de 

manera directa a los procesos productivos de la sociedad. El Artículo 1 señala: 

Artículo 1. La presente Ley tiene por objeto dirigir la generación de una ciencia, tecnología, innovación y sus aplicaciones, con base en el ejercicio de la soberanía nacional, la democracia participativa y protagónica, la justicia de género, la territorialidad y la 

nacionalidad, de acuerdo con los principios y valores de la ética socialista, con la finalidad de contribuir a la optimización de los 

procesos productivos, la seguridad y soberanía de la Nación. (p.2) 

Esta ley rige y encauza el desarrollo de soluciones de software destinadas a optimizar la productividad de las actividades comerciales locales. Al digitalizar el flujo de comandas del Restaurante Moscato en el municipio San Cristóbal del estado Táchira, los investigadores de la UPTAIET contribuyen directamente con los fines del Estado al crear metodologías aplicadas que sustituyen importaciones y reducen costos en las PYMES del sector servicios. 

# 2.3.5 Decreto Nº 3.390 (2004) 

Dentro de los decretos del Ejecutivo Nacional, este documento insta al uso preferencial del software libre desarrollado bajo estándares abiertos dentro de los sistemas de los organismos públicos y las universidades del Estado. El Artículo 1 reza: 

Artículo 1. La Administración Pública Nacional empleará prioritariamente 

Software Libre desarrollado con Estándares Abiertos, en sus sistemas, 

proyectos y servicios informáticos. A tales efectos, las Cámaras del 

Congreso, las universidades públicas y los institutos autónomos, se guiarán por lo establecido en este Decreto. (p.1) 

Dado que este proyecto socio tecnológico es desarrollado como un requisito académico formal para el PNF en Informática de la UPTAIET, se encuadra firmemente bajo las disposiciones de este Decreto nacional. La utilización de lenguajes libres de licenciamiento comercial (como Python y MySQL Server) no solo 

garantiza la soberanía y viabilidad de la solución, sino que facilita su replicabilidad comunitaria. 

2.4 Definición de Términos Básicos 

Aplicación de Escritorio: Programa informático diseñado para ejecutarse localmente en el sistema operativo de un computador personal o estación de trabajo, interactuando de manera directa con el hardware local para ofrecer un procesamiento de alta velocidad y baja latencia, prescindiendo del uso de navegadores web externos como intérpretes de su interfaz de usuario. 

Base de Datos Relacional: Estructura de almacenamiento digital que organiza la información en tablas lógicamente independientes pero relacionadas dinámicamente mediante el uso de claves primarias y claves foráneas, garantizando la consistencia de los datos operacionales de ventas y comandas y eliminando la redundancia de información transaccional. 

Comanda: Registro lógico o físico estructurado en el ámbito gastronómico que especifica los platos y bebidas seleccionados por un cliente para una mesa determinada. En un entorno digitalizado, constituye un paquete transaccional enviado a través del sistema desde el salón para su procesamiento síncrono en la cocina. 

Comunicación Síncrona: Método de transmisión de datos en redes de computadores donde el emisor y el receptor operan bajo un marco de tiempo unificado, requiriendo que la terminal de origen 

espere la confirmación inmediata de procesamiento de la terminal de destino para actualizar el estado visual de las interfaces del sistema. 

Estándar Abierto: Especificación técnica de software desarrollada colaborativamente y disponible al público sin costo comercial, destinada a asegurar la interoperabilidad, compatibilidad y libre migración de los datos 

entre diversas plataformas tecnológicas, impidiendo el monopolio de licencias propietarias cerradas. 

Integridad Referencial: Regla lógica de validez en el diseño de bases de datos relacionales que asegura que las relaciones entre tablas permanezcan válidas y consistentes, impidiendo la creación de datos huérfanos y garantizando que cada registro de comanda se asocie inequívocamente a una mesa y a un producto existentes. 

Interfaz Gráfica de Usuario (GUI): Entorno visual interactivo compuesto por componentes lógicos (ventanas, botones, listas y cajas de texto) que traduce la lógica compleja del programa en elementos intuitivos para el operario humano, facilitando la interacción directa con el sistema sin requerir comandos de consola. 

MySQL: Motor de gestión de bases de datos relacionales multihilo y multiusuario, estructurado sobre el Lenguaje de Consulta Estructurado (SQL), ampliamente utilizado bajo licencias libres para gestionar transacciones locales con alta eficiencia de almacenamiento y bajo consumo de recursos de procesamiento. 

Python: Lenguaje de programación interpretado de alto nivel y propósito general, caracterizado por una sintaxis legible y limpia, con soporte completo para programación orientada a objetos (POO), ideal para el desarrollo de lógicas de control modular en sistemas de información locales. 

Red de Área Local (LAN): Infraestructura privada de comunicación de datos que interconecta de forma física o inalámbrica (WiFi) dispositivos informáticos dentro de un entorno físico delimitado, permitiendo la transmisión de información con alta seguridad y 

velocidad sin necesidad de conexión a Internet externa. 

Software Libre: Programas informáticos distribuidos bajo licencias éticas y legales que otorgan de forma irrestricta a los usuarios las libertades de 

ejecutar, estudiar, modificar, mejorar y redistribuir el código fuente para adaptarlo a las necesidades técnicas y productivas específicas del entorno. 

CustomTkinter: Es una extensión de código abierto para la librería nativa Tkinter de Python que moderniza la apariencia visual de las interfaces gráficas de usuario (GUI). 

# CAPITULO III 

MARCO METODOLOGICO 

3.1 Enfoque Metodológico 

El presente estudio se desarrolló bajo un enfoque cualitativo, de campo, basado en una metodología de acción – participación permitiendo una integración directa en lo que sería el entorno operativo del Restaurante Moscato. Este enfoque metodológico es el más adecuado para analizar las dinámicas internas del local y desarrollar un sistema de escritorio que responda a sus necesidades específicas. Según Hernández, Fernández y Baptista (2014), la investigación cualitativa permite comprender los fenómenos de su ambiente natural, teniendo una especial atención en las estructuras y dinámicas de los participantes en su propio contexto, sobre eso, los autores establecen: 

El enfoque cualitativo se selecciona cuando el propósito es examinar la forma en que los individuos perciben y experimentan los fenómenos que los rodean, profundizando en sus puntos de vista, interpretaciones y significados. La aplicación de este diseño en entornos organizacionales permite recolectar datos directamente de la realidad donde ocurren los hechos, facilitando la identificación de problemas prácticos y la formulación de soluciones adaptadas al contexto operativo. (p. 358) 

Este enfoque facilita la estructuración del sistema de gestión de pedidos del Restaurante Moscato, ya que permite una aproximación realista a sus procesos 

internos, asegurando así que el desarrollo no sea un hecho aislado, sino una herramienta construida a partir de la experiencia directa y la observación de las necesidades reales en las áreas de mesas y cocina. 

# 3.2 Tipo De Proyecto 

De acuerdo con las clasificaciones dadas en el instructivo oficial de proyectos de la institución (UPTAIET, 2015), la propuesta se define bajo las siguientes tipologías: 

Por su Naturaleza Social (Proyecto Público o Social): Busca alcanzar un impacto directo y no netamente financiero sobre las condiciones laborales y la calidad de vida de la población objetivo (los trabajadores del restaurante), disminuyendo el estrés y la fatiga laboral a través de la digitalización de procesos manuales redundantes. 

Por el Contenido del Proyecto (Proyecto de Informática): Se centra en el análisis de necesidades, diseño relacional de bases de datos, programación orientada a objetos (en Python y MySQL) y el despliegue local de una herramienta de software transaccional. 

Por la Organización del Estudiante (Proyecto Externo): Es ejecutado y aplicado de forma interactiva en un entorno socio-productivo real ajeno al espacio físico de la institución universitaria. 

Por su Complejidad (Proyecto Complejo): Requiere la interconexión síncrona y bidireccional de múltiples estaciones de hardware lógicas que interactúan en red inalámbrica local con un gestor de bases de datos relacional (MySQL). 

3.3 Procedimiento Técnico 

El procedimiento técnico de este proyecto establece una secuencia lógica que recorre desde un escenario natural hasta uno altamente estructurado. En una primera fase, se empleó un enfoque orgánico y de escaso control mediante el diagnostico participativo y la observación directa del flujo de información del Restaurante Moscato. Posteriormente, para dar solución a la problemática detectada, la investigación adopto una táctica estructurada y de alto control tecnológico enfocada en la ingeniería del software. Para poder dirigir esta proyección tecnológica, se seleccionó como procedimiento técnico la metodología ágil de programación extrema (XP). La elección de este modelo se justifica por su capacidad de adaptación a los requerimientos cambiantes y su enfoque en la activación inmediata, estructurando el desarrollo del sistema en las siguientes fases: 

Planificación (Diagnostico): Identificación y levantamiento de los requerimientos funcionales del sistema mediante la interacción con los meseros, cocineros y el administrador del restaurante, defendiendo las necesidades de la digitalización de las comandas 

Diseño (Arquitectura de datos): Elaboración de la estructura lógica del sistema y diseño del modelo relacional de la base de datos en MySQL para gestionar mesas, productos y pedidos junto con sus detalles. 

Codificación (Desarrollo): Programación orientada a objetos utilizando el lenguaje Python, estructurando los módulos operativos y construyendo la interfaz gráfica de usuario (GUI) a través de la librería CustomTkinter para garantizar un entorno visual intuitivo. 

Pruebas (Control de calidad): Ejecución de pruebas de funcionamiento y usabilidad en entornos controlados, validando la correcta comunicación de los pedidos entre el módulo de atención en sala y la recepción en cocina. 

Respecto al dominio de este modelo procedimental en el desarrollo de sistemas, Pressman R. (2010), en su obra fundamental sobre la ingeniería del software establece lo siguiente: 

La programación extrema (XP) utiliza un enfoque orientado a 

objetos como paradigma preferido de desarrollo y engloba un conjunto de reglas y prácticas que ocurren en el contexto de cuatro actividades estructurales: planeación, diseño, codificación y pruebas. (...) XP fomenta la estrecha colaboración con el cliente, la entrega iterativa de software operativo y una filosofía de diseño simple que se adapta a las necesidades del negocio. (p. 62) 

La aplicación de este procedimiento técnico es esencial para el proyecto del Restaurante Moscato, ya que garantiza que el sistema de escritorio no se programe de manera aislada, sino bajo cortos ciclos de corrección y ajuste. esto asegura que la interfaz desarrollada responda de manera exacta, rápida y libre de errores a la alta exigencia que enfrenta el personal durante las horas de mayor afluencia de clientes. 

# 3.4 Población y Muestra 

Escenario: Está constituido físicamente por las instalaciones del Restaurante Moscato, ubicado en la avenida 19 de abril de la Parroquia La Concordia, Municipio San Cristóbal, Estado Táchira. Específicamente, el sistema de información se despliega de forma local en el área de salón para los meseros y en el área de cocina para los cocineros, interconectados bajo la cobertura de la red inalámbrica LAN privada del establecimiento. 

Informantes Clave: Los participantes o informantes clave que aportan la información estratégica corresponden al equipo de cinco (5) trabajadores del restaurante: 

Un (1) Administrador general, encargado de la gestión fiscal y gerencial del negocio. 

Dos (2) Meseros en el salón, responsables de tomar los pedidos físicos de los clientes. 

Dos (2) Cocineros en el área de producción, dedicados a la elaboración de los platos chinos. 

3.5 Técnicas e Instrumentos para la Recolección de Datos 

Para asegurar la validez, confiabilidad de la información 

recolectada en cada una de las etapas de la investigación, se aplicaron las siguientes técnicas e instrumentos: 

Observación Directa: 

Técnica: Permite percibir de manera directa el flujo real de los pedidos, los traslados del personal y los cuellos de botella generados en la cocina del Restaurante Moscato durante las horas pico de demanda. 

Instrumento: Guía de Observación estructurada de campo y bitácoras diarias de tiempos de servicio. 

Entrevista Semiestructurada: 

Técnica: Aplicada a los informantes clave (meseros y cocineros) para determinar los dolores específicos del modelo artesanal en papel, así como para detallar las funcionalidades necesarias del software de pedidos. 

Instrumento: Guía de Entrevista constituida por un cuestionario de preguntas abiertas con un enfoque de requisitos de negocio. 

Lista de Verificación: 

Técnica: Utilizada durante la fase de validación y usabilidad del sistema para verificar que los botones de comandas, formularios y módulos de MySQL se comporten con correctitud técnica. 

Instrumento: Matriz de Verificación de Requisitos Técnicos y de Usabilidad del Software. 

3.6 Procedimiento para el Análisis de los Datos 

El proceso de los datos recolectados se ejecutará de forma diferenciada según las características de cada dimensión del enfoque mixto: 

Análisis Cualitativo: Los argumentos obtenidos mediante las entrevistas semiestructuradas se someterán a técnicas de Análisis de 

Contenido y Categorización. Se clasificarán las necesidades de los usuarios finales en categorías funcionales de desarrollo (control de roles, estados de comandas, exportación de reportes locales), sirviendo como la guía de especificaciones lógicas de diseño para la codificación modular del software en Python y CustomTkinter. 

Análisis Cuantitativo: Los registros temporales de servicio de comandas y las tasas de errores de transcripción recolectados a través de la guía de observación estructurada serán procesados mediante la Estadística Descriptiva. Los resultados de tiempos promedios en segundos serán tabulados y comparados gráficamente mediante diagramas de barras utilizando la suite de oficina o código analítico local. Esto permitirá contrastar cuantitativamente el incremento de la eficiencia operativa tras la implantación síncrona del sistema de escritorio. 

3.7 Plan de Acción del Producto o Servicio. 

El desarrollo para el sistema requiere una planificación estructurada que permita coordinar cada una de las fases tecnológicas y operativas del proyecto, para ello, se formula un plan de acción que establece actividades clave a ejecutar para diseñar, codificar, probar e integrar la aplicación dentro del establecimiento, asegurando así que el software responda eficazmente a las necesidades administrativas y de atención al cliente. 

Cuadro 4. Plan de acción 

Objetivo General: Desarrollar un sistema de escritorio para la gestión de pedidos utilizando Python, CustomTkinter y MySQL para optimizar los procesos operativos del restaurante "Moscato" en San Cristóbal, estado Táchira. 

Objetivos específicos 

Actividades 

Tareas 

Tiempo 

Recursos 

Responsables 

Identificar las necesidades actuales al momento del manejo de pedidos y el flujo de la información dentro del restaurante para basarse en esas necesidades. 

Levantamiento de requerimientos e información inicial. 

- Visitar las instalaciones del restaurante. 

- Observar el flujo actual de comandas en papel. 

- Entrevistar al personal de sala y cocina. 

2 semanas 

Guías de observación, libretas de notas, transporte. 

Equipo investigador 

Diseñar una base de datos relacional en MySQL para el almacenamiento de productos, mesas y registros de ventas. 

Diseño de la arquitectura de datos. 

- Definir las entidades y relaciones del sistema. 

- Estructurar las tablas (Mesas, Productos, pedidos, empleados, usuarios). 

- Escribir el script de creación en MySQL. 

3 semanas 

Computadoras, software de modelado, gestor MySQL. 

Equipo investigador (Desarrolladores) 

Programar la interfaz gráfica de la aplicación mediante la librería CustomTkinter, incorporando la generación de reportes que sirvan para la toma de decisiones de la organización. 

Codificación del software y módulos visuales. 

- Programar las ventanas de usuario en Python. 

- Integrar la interfaz visual (CustomTkinter) con la base de datos. 

- Desarrollar el módulo lógico de reportes gerenciales. 

5 semanas 

Computadoras, entorno de desarrollo Python, librería CustomTkinter 

Equipo investigador (Desarrolladores). 

Realizar pruebas de funcionamiento y usabilidad que garantice la correcta operabilidad del sistema de escritorio. 

Control de calidad e implementación técnica. 

- Ejecutar pruebas de errores (debugging). 

- Validar la usabilidad de la interfaz con los meseros. 

- Realizar correcciones finales de código. 

2 semanas 

Sistema Moscato (Beta), personal del restaurante. 

Equipo investigador y personal del restaurante. 

cuadro 4 Plan de acción 

CAPITULO IV 

PRODUCTO Y/O SERVICIO. 

4.1 Análisis de los Resultados 

A partir de las técnicas e instrumentos de recolección de datos aplicados en el Restaurante Moscato específicamente la guía de observación directa de campo, la guía de entrevista semiestructurada realizada a los cinco (5) informantes clave (administrador, dos meseros y dos cocineros) y las listas de verificación, se procedió a analizar cualitativa y cuantitativamente la situación operativa actual para fundamentar la solución tecnológica. 

Proceso actual de registro y comunicación de ordenes: Los datos cualitativos obtenidos en las entrevistas confirman que el 100% de la toma de pedidos se realiza mediante papel y lápiz, lo cual obliga a los meseros a trasladarse continuamente desde las mesas en la sala hacia el área de cocina. 

Tiempos de latencia en servicio: El análisis cuantitativo mediante bitácoras de tiempo reveló que, durante las horas pico de demanda (picos de mediodía y noche), el tiempo promedio transcurrido desde que el cliente solicita el plato de comida china hasta que la orden llega físicamente al cocinero oscila entre 3 y 5 minutos (180 a 300 segundos), acumulando cuellos de botella por desplazamientos físicos e interrupciones en la cocina. 

Incidencia de errores y pérdidas de comandas: La observación directa registró una tasa aproximada del 15% de incidencias negativas relacionadas 

con notas ilegibles, duplicación de platos, confusión en el número de mesa o extravío de tiques físicos en la barra de preparación. 

Requerimientos expresados por el personal: El administrador y el personal operativo expresaron la necesidad prioritaria de automatizar el flujo de información mediante pantallas digitales sincronizadas que eliminen la dependencia del papel, reduzcan la fatiga física y permitan generar reportes periódicos para el control de ventas. 

El razonamiento justificado de estos datos demuestra que los problemas operativos no radican en el desempeño humano del personal, sino en la ausencia de una herramienta de comunicación síncrona en tiempo real. Por consiguiente, se justifica plenamente la propuesta de desarrollo de un sistema de escritorio local en Python con interfaz en CustomTkinter y base de datos relacional en MySQL, interconectado mediante red local LAN entre dos estaciones de trabajo (laptops en sala y cocina). 

4.2 Propuesta del Producto o Servicio En función de la metodología técnica. 

4.2.1 Objetivo de la Propuesta (Producto o Servicio) 

Desarrollar e implementar un sistema de escritorio para la gestión de pedidos y comandas utilizando Python, CustomTkinter y MySQL en el Restaurante Moscato, con la finalidad de automatizar la toma de órdenes en sala, sincronizar la recepción e indicación de estatus en cocina a través de una red local, y proveer reportes gerenciales para la optimización toma de decisiones organizacionales. 

4.2.2 Memoria Descriptiva 

a) Descripción o caracterización del servicio o producto 

El producto obtenido consiste en una aplicación de escritorio multiplataforma programada en el lenguaje Python 3, configurada con una interfaz gráfica de usuario (GUI) desarrollada en la librería CustomTkinter y conectada a un motor de base de datos relacional MySQL Server. El software opera bajo una arquitectura clienteservidor en Red de Área Local (LAN / WiFi privada) sin requerir conexión a Internet. 

Fases desarrolladas (Metodología Ágil Programación Extrema - XP): 

Fase de Planificación: Se levantaron las historias de usuario y requerimientos funcionales junto con el equipo del Restaurante Moscato, definiendo los tres roles de acceso principales: Administrador, Mesero (Sala) y Cocinero (Cocina). 

Fase de Diseño: Se diseñó el esquema relacional de la base de datos MySQL (tablas de empleados, usuarios, mesas, productos, pedidos y detalles de pedido) y la prototipada visual de las ventanas en CustomTkinter. 

Fase de Codificación: Se programaron los módulos en Python aplicando el paradigma de Programación Orientada a Objetos (POO), integrando controladores de bases de datos (mysqlconnector-python) y la lógica de refresco síncrono para la actualización de comandas. 

Fase de Pruebas y Validación: Se realizaron pruebas de depuración (debugging), pruebas unitarias de almacenamiento transaccional y evaluaciones de usabilidad directamente con los trabajadores del restaurante. 

Inclusión de la comunidad y socialización del proyecto: La comunidad del Restaurante Moscato (administrador, meseros y cocineros) formó parte activa en cada etapa del desarrollo. Mediante el Diagnóstico Participativo (IAP), el personal definió la distribución visual de las mesas en pantalla y la categorización de los platos chinos del menú. 

La socialización del producto se llevó a cabo mediante dos jornadas de trabajo presenciales en el establecimiento: Jornada de Capacitación Técnica: Presentación de la interfaz a los dos meseros y dos cocineros, realizando simulaciones en tiempo real de registro de orden en laptop de sala, recepción instantánea en laptop de cocina y 

cambio de estado a "Listo para entregar". Sesión de Validación y Retroalimentación: Evaluación del uso del sistema durante un servicio simulado, ajustando el tamaño de los botones, la legibilidad tipográfica y los tiempos de refresco según la experiencia del usuario. 

# b) Factibilidad 

# b.1 Factibilidad técnica 

Dominio de conocimientos: Los investigadores poseen las competencias técnicas en programación Orientada a Objetos (Python), diseño de interfaces (CustomTkinter) y modelado de bases de datos relacionales (MySQL) adquiridas durante la formación académica en el PNF en Informática de la UPTAIET. 

Infraestructura comunitaria: El Restaurante Moscato cuenta con dos (2) computadores portátiles (laptops) para las estaciones de sala y cocina, así como un enrutador (router) WiFi para configurar la Red de Área Local (LAN) privada, garantizando que el entorno físico posee los requerimientos mínimos de hardware para ejecutar la solución. 

# b.2 Factibilidad económica 

El desarrollo se fundamenta en el uso de tecnologías de Software Libre y Estándares Abiertos (Python, CustomTkinter, MySQL), lo cual reduce significativamente el costo de licencias comerciales de software. 

Cuadro 5. Índices financieros 

Concepto 

Descripción 

cantidad 

Consto unitario (USD) 

Costo total (USD) Equipos de computo Laptops existentes en el establecimiento 

2 

$0.00 

$0.00 

Infraestructura de red 

Router WIFI LAN TP-Link 

1 

$35.00 

$35.00 

Licencias de software 

Python, CustomTkinter, MySql (software libre) 

1 

$0.00 

$0.00 

Mano de obra y desarrollo 

Honorarios de investigación y programación (aporte académico). 

2 

$0.00 

$0.00 

Capacitación y despliegue 

Sesiones de formación e instalación 

1 

$20.00 

$20.00 

Total, inversión inicial 

$55.00 

cuadro 5 Índices Financieros 

Plan de Inversión y Estimación de Ingresos/Ahorros 

Ahorro operativo por papel de comandas: $15,00 USD mensuales en talonarios de papel. 

Ahorro por reducción de errores en platos extraviados/mal preparados: $35,00 USD mensuales. 

Beneficio económico mensual estimado: $50,00 USD/mes ($600,00 USD/año). 

Cuadro 6 . Flujo Neto Proyectado (3 años) 

año 

Inversión inicial 

Ingresos/ahorros generados 

Costos de mantenimiento 

Flujo neto de efectivo 

0 -$55.00 $0.00 $0.00 -$55.00 1 $0.00 $600.00 $55.00 $550.00 2 $0.00 $600.00 $55.00 $550.00 3 $0.00 $600.00 $55.00 $550.00 

cuadro 6 Flujo Neto Proyectado (3 años) 

Tras una inversión inicial de $55,00 USD en el Año 0, el sistema genera $550,00 USD limpios anuales durante los primeros 3 años gracias a la reducción de desperdicios y gastos en insumos analógicos. 

Evaluación Financiera: VAN, TIR y Relación Beneficio/Cost0 

Tomando en cuenta una tasa de descuento del 10% anual: 

Valor Actual Neto (VAN): 

"VAN"=-55+550/(1+0.10)^1 +550/(1+0.10)^2 +550/ (1+0.10)^3 =-55+500+454,55+413,22=$1.312,77" USD" 

Al ser el VAN $> 0$, la propuesta es altamente rentable y viable financieramente. 

Tasa Interna de Retorno (TIR): 

TIR>800% 

(Debido a la baja inversión inicial y el alto ahorro derivado del Software Libre). 

Relación Beneficio/Costo (B/C): 

Relación B/ 

Por cada dólar invertido, el proyecto retorna $7,65 USD en beneficios económicos y ahorros operativos. 

Mezcla de Mercado (4P) 

Producto: sistema de escritorio integra de gestión de comandas y pedidos gastronómicos con reportes MYSQL. 

Precio: $0,00 en costo de licenciamiento comercial al ser un proyecto socio-tecnológico de imparto comunitario. 

Plaza: Instalación física local en el Restaurante Moscato, Av. 19 de Abril, San Cristóbal, Estado Táchira. 

Promoción: Socialización directa con el sector socio-productivo local e instituciones académicas como caso de éxito en digitalización PYME. 

# b.3 Factibilidad Social 

Indicadores Sociales: Mejora sustancial de la calidad del entorno de trabajo y disminución del estrés laboral en los 5 trabajadores del restaurante al eliminar discusiones por notas ilegibles o demoras. 

Factores de Producción: Transición del modelo tradicional analógico a un proceso digitalizado síncrono. 

Incremento en Ingresos y Empleo: Al agilizar la atención al cliente en salón, se incrementa la rotación de mesas, favoreciendo la rentabilidad del establecimiento y la estabilidad laboral del equipo de trabajo. 

# b.4 Factibilidad ambiental 

Impacto Ambiental: Eliminación total del uso de papel para comandas físicas, reduciendo la generación de desechos sólidos. 

Riesgo Ambiental y Mitigación de Amenazas: En consideración con la inestabilidad del servicio eléctrico en la región, la factibilidad técnica prevé el uso de laptops con baterías operativas y el almacenamiento de copias de seguridad de la base de datos MySQL en disco local para evitar pérdida de información transaccional ante cortes de energía. 

# b.5 Factibilidad Cultural 

Costumbres y Tradiciones: El sistema respeta la identidad culinaria del Restaurante Moscato (gastronomía china venezolana), 

adecuando la nomenclatura de la interfaz visual a las denominaciones tradicionales de los platos del menú local sin alterar las costumbres organizacionales. 

c) Presentación del Producto o Servicio: Modelado UML del Sistema 

Para el modelado y especificación técnica del sistema de escritorio del Restaurante Moscato, se utilizó el Lenguaje Unificado de Modelado (UML), lo cual permite representar de forma estandarizada la estructura, comportamiento e interacciones de la solución informática desarrollada en Python, CustomTkinter y MySQL. 

Actores del Sistema 

Administrador: Encargado de gestionar los usuarios/empleados, las mesas y consultar el panel de control y estadísticas generales del negocio. 

Mesero: Encargado de la atención en sala; crea y edita pedidos, los envía a cocina, genera la precuenta y procesa el pago y cierre de mesa. 

Cocinero: Personal operativo de cocina que visualiza los pedidos recibidos y actualiza su estado de preparación. 

Sistema / Base de Datos: Entidad de soporte automatizado encargada de almacenar, consultar y procesar las transacciones y persistencia de datos. 

Casos de Uso Principales 

UC01: Autenticarse 

UC02: Gestionar empleados 

UC03: Gestionar mesas 

UC04: Crear pedido 

UC05: Editar pedido 

UC06: Enviar pedido a cocina 

UC07: Consultar estado de cocina 

UC08: Actualizar estado del pedido 

UC09: Generar precuenta 

UC10: Cerrar mesa y pagar 

UC11: Ver panel de control y estadísticas 

Diagrama de casos de uso: 

Objetivo: Ofrece una visión global y de alto nivel sobre las funcionalidades del sistema (casos de uso) y cómo interactúa cada actor con el software. 

Actores y Responsabilidades: 

Administrador: Gestiona las credenciales de acceso (UC01), la nómina y datos del personal (UC02), la distribución/configuración de mesas (UC03) y la toma de decisiones estratégicas mediante el panel de control y reporte de estadísticas (UC11). 

Mesero: Es el actor operativo en sala. Se encarga de la toma e ingreso de pedidos (UC04), su modificación ante cambios del cliente (UC05), el envío de la comanda a cocina (UC06), la impresión de la precuenta (UC09) y la recepción del pago junto al cierre de la mesa (UC10). 

Cocinero: Actor enfocado en la preparación de alimentos. Revisa los pedidos entrantes en tiempo real (UC07) y actualiza el avance de los platos (UC08). 

Sistema / Base de Datos: Actúa como actor de soporte automatizado que garantiza la persistencia, integridad transaccional y validación de reglas de negocio para los casos de uso UC02, UC06, UC08 y 

UC10. 

Relaciones entre Casos de Uso: 

<<include>> (Inclusión): El envío a cocina (UC06) requiere obligatoriamente la previa existencia de un pedido creado (UC04). De la misma forma, la generación de precuenta (UC09) es un paso incluido dentro del proceso global de cobro y cierre de mesa (UC10). 

<<extend>> (Extensión): La edición del pedido (UC05) es una funcionalidad opcional que extiende al caso de uso básico de creación (UC04), ejecutándose únicamente si el mesero requiere corregir o agregar ítems a la comanda. 

Figura 3. Diagrama en casos de uso 

Diagrama de Clases El siguiente diagrama define la arquitectura del dominio de datos para soportar los 11 casos de uso: 

Objetivo: Representa la estructura estática de la base de datos y la arquitectura orientada a objetos del software, definiendo los atributos, métodos y relaciones entre las entidades del dominio. 

Entidades Principales: 

Usuario y Empleado: Manejan el control de acceso y los datos filiatorios del personal del restaurante. Se vinculan mediante una relación de asociación 1:1 (cada usuario corresponde a un único empleado). 

Mesa: Almacena la disponibilidad del mobiliario (DISPONIBLE, OCUPADA, EN_CUENTA). Mantiene una relación 1:N con Pedido (una mesa puede registrar múltiples pedidos a lo largo del tiempo, pero un pedido activo pertenece a una sola mesa). 

Pedido y DetallePedido: Es la estructura central de la comanda. Existe una relación de composición fuerte (1→1..*), lo que significa 

que un pedido debe contener al menos un detalle de producto y, si el pedido se elimina, sus detalles asociados también desaparecen. 

Producto: Representa el catálogo/menú ofertado (platos de comida china, bebidas, etc.), vinculado a los detalles del pedido mediante una asociación de referencia. 

Pago: Entidad que registra la transacción monetaria al cerrar el pedido (monto, método de pago y fecha), relacionada 1:0..1 con Pedido (un pedido no genera pago hasta que el cliente decide cancelar la cuenta). 

Figura 4. Diagrama de clase. 

4 

Diagrama de Estados (Ciclo de Vida del Pedido) 

Muestra los cambios de estado del pedido desde su creación por el mesero hasta el cierre y pago: 

Objetivo: Describe las transformaciones continuas por las que pasa un pedido (Pedido) desde su apertura en sala hasta su liquidación financiera. 

Flujo de Estados: 

En Creación: Estado inicial que se activa cuando el mesero abre la comanda para una mesa (UC04). En este punto se permite agregar o eliminar productos (UC05). 

Enviado A Cocina: Transición provocada cuando el mesero presiona "Enviar a Cocina" (UC06). El pedido se bloquea temporalmente para edición rápida y se vuelve visible en el área de preparación. 

En Preparación: El cocinero toma el pedido en pantalla e indica que los platos están en elaboración (UC08). 

Listo: El cocinero marca los platos como terminados (UC08), notificando a sala que el pedido está listo para servirse. 

Precuenta Generada: El cliente solicita la cuenta. El mesero imprime o genera el desglose de consumos (UC09). 

Pagado Y Cerrado: Estado final. Se registra el ingreso monetario, se procesa la transacción (UC10) y la mesa cambia automáticamente su estado a DISPONIBLE. 

Figura 5. Diagrama de estados. 5 

Diagrama de Secuencia (Toma de Pedido y Envío a Cocina - UC04 y UC06) 

Objetivo: Ilustra el intercambio cronológico y ordenado de mensajes entre los componentes del sistema (Mesero, Interfaz, Controlador, Base de Datos y Cocinero) durante el proceso crítico de toma y despacho de comandas. 

Traza de Interacción: 

Pasos 1-4 (Creación del Pedido - UC04): El mesero interactúa con la vista (V), seleccionando la mesa y los ítems del menú. La vista envía los datos al controlador (C), el cual ejecuta la consulta en la base de datos (BD) para registrar el pedido con estado "En Creación" y devuelve la confirmación con el ID generado. 

Pasos 5-8 (Envío a Cocina - UC06 y UC07): El mesero confirma la comanda. El controlador envía una sentencia UPDATE a la base de datos para modificar el estado del pedido a "Enviado a Cocina". Al confirmarse la transacción en la BD, la interfaz de cocina (K) recibe una notificación/refresco automático, haciendo visible la comanda en la pantalla del área de preparación sin intervención manual adicional. 

Figura 6. Diagrama de Secuencia 

6 

6 

Diagrama de Actividades (Flujo Operativo Completo) 

Objetivo: Muestra el flujo de trabajo operacional (workflow) y las decisiones lógicas que toma el sistema dependiendo del tipo de usuario que haya iniciado sesión. 

Caminos del Flujo Lógico: 

Inicio y Autenticación (UC01): Todo usuario debe ingresar sus credenciales válidas antes de acceder a las funciones del software. 

Bifurcación por Rol: 

Si es Administrador: Redirige al panel gerencial, donde puede bifurcar hacia la gestión de empleados (UC02), administración del mapa de mesas (UC03) o revisión de métricas financieras e ingresos (UC11). 

Si es Mesero: Sigue una secuencia operativa lineal orientada al 

servicio al cliente: creación de pedidos (UC04) → edición opcional (UC05) → envío a comandera (UC06) → emisión de precuenta (UC09) → cobro final y liberación de mesa (UC10). 

Si es Cocinero: Entra en un bucle repetitivo de consulta de órdenes en pantalla (UC07) y actualización iterativa del estado de los platos (UC08) hasta que no queden órdenes pendientes en la cola de trabajo. 

7 Figura 7. Diagrama de Actividades. 

CAPITULO V 

CONCLUSIONES Y RECOMENDACIONES 

5.1 Conclusiones 

A través de lo que fue la observación directa y las entrevistas semiestructuradas, se pudo comprobar que la dependencia absoluta al papel y lápiz para registrar las comandas origina tiempos de latencia prolongados generan una tasa de error de alrededor el 15% de los pedidos, lo que demostró la urgencia de digitalizar el proceso operativo. A si mismo la estructuración del modelo en MySQL resultó ser la solución más favorable para la organización sistemática de entidades criticas como mesas, productos, pedidos y empleados, garantizando así la integridad referencial de los datos transaccionales, eliminando la redundancia y sentando una base de almacenamiento robusto. El desarrollo bajo el lenguaje Python, apoyado en la librería CustomTkinter, permitiendo materializar una interfaz gráfica moderna, intuitiva y de alta calidad visual. Esta elección tecnológica superó las limitaciones estéticas de las herramientas tradicionales, ofreciendo un entorno ergonómico y correctamente seccionado según los roles de administrador, mesonero y cocinero, De la misma forma, la integración de la lógica de programación orientada a objetos facilitó la generación de reportes gerenciales ofreciendo a la gerencia un instrumento 

tecnológico amigable. Lo anterior permitió que las jornadas de validación ejecutadas junto a los informantes clave confirmaron la estabilidad operativa del aplicativo, los ajustes aplicados en los tiempos de refresco visual y la tipografía consolidaron un canal estrecho de comunicación en tiempo real entre la sala y la cocina, entregando como 

producto final un sistema intuitivo y plenamente adaptado al alto dinamismo del restaurante. 

# 5.2 Recomendaciones 

Se sugiere programar revisiones preventivas a los equipos de computación y al enrutador (router) Wifi de las instalaciones, de esta manera asegurando que la cobertura de la Red de Área Local (LAN) no sufra latencias o alguna intermitencia que competa la comunicación de los pedidos en los horarios con la mayor cantidad de cliente. Es recomendable mantener una fase de acompañamiento activo durante los primeros meses de implantación definitiva, fomentando la retroalimentación continua con los trabajadores para afianzar el uso de los módulos y evitar que el personal incurra en prácticas antiguas. Tomando como base lo que sería la estructura relacional lograda, se propone a la organización invertir a mediano plazo en la expansión del software mediante la incorporación de un módulo de inventario, el cual, al sincronizarse con la preparación de cada comanda este descuente de forma automática la materia prima que fue utilizada, optimizando así los procesos de auditoría y reposición de almacén. 

Bibliografía 

López Echeverry, A. M., Cabrera, C., & Valencia Ayala, L. E. (2008). 

Introducción a la calidad de software. Scientia Et Technica, XIV (39), 326-331. 

Pressman, R. S. (2010). Ingeniería del software: Un enfoque práctico (7.ª ed.). 

Arias, F. (2012). El proyecto de investigación: Introducción a la metodología científica (6.ª ed.). Editorial Episteme. 

Burgos Cando, C. X. (2015). Desarrollo de un sistema web para la gestión de pedidos en un restaurante. Aplicación a un caso de estudio, Tesis de licenciatura, Escuela Politécnica Nacional. https:// bibdigital.epn.edu.ec/handle/15000/10337 

Hernández Sampieri, R., Fernández Collado, C., y Baptista Lucio, P. (2014). Metodología de la investigación (6.ª ed.). 

Instituto Universitario de Tecnología Agroindustrial. (2015). Instructivo para la presentación escrita del Proyecto de los Programas Nacionales de Formación. IUTAI, San Cristóbal, Venezuela. 

Coronel, C., y Morris, S. (2017). Bases de datos: Diseño, implementación y administración (11.ª ed.). Cengage Learning. 

Gómez, M. (2018). Innovación digital y desarrollo organizacional: Proyectos socio-tecnológicos en organizaciones socio productivas. Editorial Tecnológica Venezolana. 

Walker, J. R., & Lundberg, D. E. (2021). Introduction to hospitality (8th ed.). Pearson. 

Laudon, K. C., & Laudon, J. P. (2022). Management information systems: Managing the digital firm (17th ed.). Pearson. 

Ramírez Nastacuas, B. M. (2023). Sistema web y aplicación móvil para la gestión de pedidos en el restaurante "La Aduana" Trabajo de grado, Pontificia Universidad Católica del Ecuador Sede Ibarra. Repositorio Institucional PUCESI. https://repositorio.puce.edu.ec/ server/api/core/bitstreams/ec8919d8ba82-4b52-88ed-757877d1098b/content 

Crece con BNC. (2024). Tendencias de innovación digital en PYMES venezolanas. https://crececonbnc.com/tendencias-de-innovaciondigital-en-pymes-venezolanas/ 

Peraza, K. (2024). Análisis del control de inventario y sus implicaciones en mejores prácticas de gestión de materias primas en el restaurante McDonald's del Centro Comercial Parque Los Aviadores, Palo Negro (Trabajo especial de grado). Instituto Universitario de Tecnología de Administración Industrial (IUTA), Extensión Maracay, Venezuela. https://iutamaracay.com.ve/ iuta_webpage/archivos/M1AE7VD%20-%20TEG%20%20Kevin%20Peraza%20-%20ID27589541%20-%202024II.pdf 

Suarez Segura, D. L., y Galindo Pastran, Y. J. (2024). Plataforma web integrada para la gestión de pedidos, control de inventario, recursos humanos, compras y generación de reportes de ventas en una empresa (Trabajo de grado). Universidad Nacional Experimental del Táchira (UNET), San Cristóbal, Venezuela. Repositorio Institucional UNET. https:// repositorio.unet.edu.ve:8443/jspui/browse? type=author&value=Galindo+Pastran%2C+Yorman+Josue 

Python Software Foundation. (2024). Preguntas frecuentes sobre la Interfaz Gráfica de Usuario (GUI). Documentación de Python 3.12. https://docs.python.org/es/3/faq/gui.html 

CLAB Group. (2026, 18 enero). Digitalización en restaurantes: qué es, por qué es clave y cómo aplicar la digitalización en tu restaurante. https://clabgroup.com/es/blog/digitalizacionrestaurantes/ 

OlaClick. (2026, 6 abril). Cómo hacer una gestión de pedidos eficientes para tu restaurante. https://olaclick.com/es/sistemapara/carnes/como-hacer-una-gestion-de-pedidos-eficientes-para-turestaurante/ 

Mantilla Sánchez, E. L., Robles Loje, E. J., Alvarez Méndez, G. M., Mozo-Avalos, J. A., Acosta-Plasencia, N. A., Chuquipoma Medina, S. D., & Córdova-Otero, J. L. (2026). Sistemas de gestión de pedidos en restaurantes: Una revisión sistemática. CIENTÍFICA 

TECHNOLOGICA, 1(1). https://revistas.unitru.edu.pe/index.php/ 

ctech/article/view/7426 

Constitución de la República Bolivariana de Venezuela. (1999). Gaceta Oficial de la República Bolivariana de Venezuela, N° 36.860 (Extraordinaria), de fecha 30 de diciembre de 1999. 

Decreto N° 3.390. (2004). Decreto mediante el cual se dispone que la Administración Pública Nacional empleará prioritariamente Software Libre desarrollado con 

Estándares Abiertos en sus sistemas, proyectos y servicios. Gaceta Oficial de la República Bolivariana de Venezuela, N° 38.095, de fecha 28 de diciembre de 2004. 

Ley de Infogobierno. (2013). Gaceta Oficial de la República Bolivariana de Venezuela, N° 40.274, de fecha 17 de octubre de 2013. 

Ley Especial contra los Delitos Informáticos. (2001). Gaceta Oficial de la República Bolivariana de Venezuela, N° 37.313, de fecha 30 de octubre de 2001. 

Ley Orgánica de Ciencia, Tecnología e Innovación. (2010). Gaceta Oficial de la República Bolivariana de Venezuela, N° 39.575, de fecha 16 de diciembre de 2010. 

