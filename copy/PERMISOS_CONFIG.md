# CONFIGURACIÓN DE PERMISOS EN GITHUB ACTIONS
# Para evitar errores de permisos al hacer push o modificar workflows

## IMPORTANTE: Permiso `workflows: write`

El error principal es: "refusing to allow a GitHub App to create or update workflow without `workflows` permission"

### Ejemplo de configuración completa de permisos:
```yaml
permissions:
  actions: write        # Permite gestionar actions
  id-token: write       # Permite autenticación OIDC
  contents: write       # Permite modificar código y push
  pull-requests: write  # Permite gestionar PRs
  issues: write         # Permite gestionar issues
  workflows: write      # PERMISO CRUCIAL: Permite modificar archivos .github/workflows/
```

## ESTRATEGIA DE IDENTIDAD DE GIT

Siempre configurar identidad de bot:
```yaml
- name: Configurar identidad de Git
  run: |
    git config --global user.name "github-actions[bot]"
    git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
```

## CHECKOUT CON PERSISTENCIA DE CREDENCIALES

```yaml
- name: Checkout repository
  uses: actions/checkout@v6
  with:
    persist-credentials: true  # IMPORTANTE
    fetch-depth: 0             # IMPORTANTE para push
```

## NODE VERSION
GitHub Actions usa Node 22 por defecto. Si necesitas Node 20:
```yaml
env:
  ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION: true
```

## REGISTROS IMPORTANTES EN LOS ARCHIVOS DE LA CARPETA copy/

1. opencode-corrected.yml - Con permiso workflows: write añadido
2. test-push-corrected.yml - Con permiso completos para testing