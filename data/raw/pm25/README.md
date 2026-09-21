# Datos crudos de PM2.5

Fuente oficial: Repositorio de Datos SIATA, *Histórico de Material
Particulado - PM2.5*.

- DOI: `10.83041/AUWZWT`
- Página: <https://datos.siata.gov.co/dataset.xhtml?persistentId=doi:10.83041/AUWZWT>
- API de metadatos: <https://datos.siata.gov.co/api/datasets/:persistentId/?persistentId=doi:10.83041/AUWZWT>
- Versión consultada: `4.0`
- Consulta comprobada: `2026-09-14`

Los archivos `.tab` se descargan con el script incluido. Para obtener
únicamente 2013 como muestra de validación, ejecute desde la raíz:

```bash
python scripts/download_pm25_dataset.py --year 2013
```

El script consulta el catálogo oficial, descarga los archivos originales y
verifica cada MD5 publicado por Dataverse. A pesar de la extensión `.tab`, los
archivos originales usan comas como delimitador; el loader lo detecta en lugar
de asumirlo.

El conjunto completo utilizado en el notebook se obtiene con:

```bash
python scripts/download_pm25_dataset.py --all
```

Una descarga existente correcta no se repite.
