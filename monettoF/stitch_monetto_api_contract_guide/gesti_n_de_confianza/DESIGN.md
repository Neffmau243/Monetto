---
name: Gestión de Confianza
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#454652'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#757683'
  outline-variant: '#c5c5d4'
  surface-tint: '#4356b6'
  primary: '#10298a'
  on-primary: '#ffffff'
  primary-container: '#2e42a1'
  on-primary-container: '#abb7ff'
  inverse-primary: '#bac3ff'
  secondary: '#006c49'
  on-secondary: '#ffffff'
  secondary-container: '#6cf8bb'
  on-secondary-container: '#00714d'
  tertiary: '#6f001e'
  on-tertiary: '#ffffff'
  tertiary-container: '#9a002d'
  on-tertiary-container: '#ffa2a8'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dee1ff'
  primary-fixed-dim: '#bac3ff'
  on-primary-fixed: '#001159'
  on-primary-fixed-variant: '#293d9c'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffdadb'
  tertiary-fixed-dim: '#ffb2b7'
  on-tertiary-fixed: '#40000d'
  on-tertiary-fixed-variant: '#92002a'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-currency:
    fontFamily: Manrope
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-md:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-bold:
    fontFamily: Manrope
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
  label-sm:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max-width: 1280px
  gutter: 24px
  margin-desktop: 40px
---

## Brand & Style

Este sistema de diseño se fundamenta en los pilares de la precisión, la claridad y la seguridad financiera. El estilo visual adoptado es **Corporate / Modern**, priorizando la legibilidad de los datos numéricos y la facilidad de navegación para usuarios que gestionan su patrimonio desde entornos de escritorio. 

La estética busca proyectar estabilidad mediante el uso de una paleta sobria pero funcional, donde el espacio negativo (aire) no es solo un recurso visual, sino una herramienta para reducir la carga cognitiva. El resultado es una interfaz profesional que equilibra la frialdad de los datos con una experiencia de uso fluida y acogedora.

## Colors

La paleta se divide en roles funcionales específicos para el contexto financiero:

- **Primario (Índigo Profundo):** Utilizado para elementos de marca, acciones principales y navegación, evocando autoridad y confianza.
- **Éxito (Verde Esmeralda):** Reservado exclusivamente para flujos de ingresos, saldos positivos y confirmaciones de ahorro.
- **Peligro (Rojo Coral):** Aplicado a gastos, alertas de presupuesto excedido y estados críticos, con un tono suave para no generar estrés innecesario.
- **Fondos:** Se utiliza una combinación de blanco puro (#FFFFFF) para contenedores de contenido y grises ultra-claros (#F8FAFC) para el lienzo base, creando una jerarquía de capas clara.

## Typography

Se ha seleccionado **Manrope** como tipografía única debido a su excelente rendimiento en la visualización de números y su carácter moderno y geométrico. 

Este sistema de diseño implementa una jerarquía estricta donde el rol `display-currency` se reserva para balances principales. El peso de la fuente aumenta en títulos para anclar la vista, mientras que en el cuerpo de texto se mantiene un peso regular para facilitar la lectura de transacciones largas. Se debe prestar especial atención al espaciado entre caracteres en montos monetarios para asegurar que cada dígito sea claramente distinguible.

## Layout & Spacing

El sistema utiliza un **Fixed Grid** para escritorio, optimizado para una resolución de 1440px con un ancho máximo de contenedor de 1280px. La retícula consta de 12 columnas con canales (gutters) de 24px.

El ritmo vertical se basa en una unidad de 8px. Los componentes de datos, como las tablas de transacciones, utilizan un padding interno denso para maximizar la información visible sin sacrificar la legibilidad, mientras que las secciones de dashboard utilizan márgenes más amplios (mínimo 32px) para separar visualmente los diferentes módulos financieros.

## Elevation & Depth

La profundidad se comunica mediante **sombras ambientales** extremadamente suaves. No se utilizan sombras negras; en su lugar, se emplean tonos de índigo muy diluidos (opacidad 4-8%) para elevar las tarjetas del fondo.

Este sistema de diseño define tres niveles de elevación:
1. **Nivel 0 (Base):** Fondos de aplicación en gris claro.
2. **Nivel 1 (Superficie):** Tarjetas de contenido y tablas con fondo blanco y sombra sutil.
3. **Nivel 2 (Interacción):** Menús desplegables y modales con una sombra más definida para indicar superposición física.

## Shapes

Se adopta un lenguaje de formas **Rounded** (redondeado). El radio de 0.5rem (8px) en tarjetas y botones suaviza la estética profesional, haciéndola más accesible sin perder la formalidad. Las esquinas pronunciadamente circulares se reservan para elementos de estatus (chips) o avatares, mientras que los inputs mantienen la coherencia con el radio estándar de la interfaz.

## Components

- **Tarjetas:** Son el contenedor principal. Deben tener un borde fino de 1px en un gris muy claro (#E2E8F0) para definir límites en pantallas con mucho brillo, complementando la sombra suave.
- **Botones:** El estado *primary* es índigo sólido. El estado *hover* debe oscurecer el tono un 10%. Las acciones secundarias utilizan bordes (outlined) para evitar competir visualmente con la acción principal.
- **Tablas de Transacciones:** Sin bordes verticales. Las filas deben tener un estado *hover* con un cambio sutil de color de fondo. Las cifras negativas deben aparecer en Rojo Coral y las positivas en Verde Esmeralda.
- **Inputs:** Bordes limpios con foco en Azul Primario. Las etiquetas (labels) siempre deben ser visibles sobre el campo.
- **Gráficos Minimalistas:** Gráficos de líneas y áreas sin ejes excesivos. El uso del color en los gráficos debe ser semántico: áreas de gasto en coral, áreas de ahorro en verde.
- **Chips de Estado:** Pequeñas etiquetas redondeadas con fondo de color pastel (baja opacidad del color principal) para categorizar gastos rápidamente.