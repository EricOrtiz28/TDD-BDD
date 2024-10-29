Feature: Compilar y ejecutar código

  Scenario: Compilar y ejecutar código válido
    Given el código fuente es
      """
      print("Hello, World!")
      """
    When el compilador ejecuta el código
    Then el resultado debe ser
      """
      Hello, World!
      """

  Scenario: Código contiene un token inválido
    Given el código fuente es
      """
      prnt("Hello, World!")
      """
    When el compilador ejecuta el código
    Then el resultado debe ser
      """
      Error léxico en línea 1: token 'prnt' inválido.
      """

  Scenario: Código contiene un error sintáctico
    Given el código fuente es
      """
      print "Hello, World!"
      """
    When el compilador ejecuta el código
    Then el resultado debe ser
      """
      Error sintáctico en línea 1: paréntesis faltante.
      """
