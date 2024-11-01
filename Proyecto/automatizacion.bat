@ echo off

 set ejecutable= "C:\Program Files\PostgreSQL\12\bin\psql.exe"
 set usuario= postgres
 set db= prueba_tecnica

 set copy1= "COPY public.catalogo_banca FROM 'C:\Program Files\PostgreSQL\Import\catalogo_banca.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');"
 set copy2= "COPY public.cat_perfil_riesgo FROM 'C:\Program Files\PostgreSQL\Import\cat_perfil_riesgo.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');"
 set copy3= "COPY public.catalogo_activos FROM 'C:\Program Files\PostgreSQL\Import\catalogo_activos.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');"
 set copy4= "COPY public.historico_aba_macroactivos FROM 'C:\Program Files\PostgreSQL\Import\historico_aba_macroactivos.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';', ENCODING 'UTF8');"

 %ejecutable% -U %usuario% -d %db% -c %copy1%
 %ejecutable% -U %usuario% -d %db% -c %copy2%
 %ejecutable% -U %usuario% -d %db% -c %copy3%
 %ejecutable% -U %usuario% -d %db% -c %copy4%

echo Importacion finalizada

move "C:\Program Files\PostgreSQL\Import\catalogo_banca.csv" "C:\Program Files\PostgreSQL\Import\Importados\catalogo_banca_%date:/=-%.csv"
move "C:\Program Files\PostgreSQL\Import\cat_perfil_riesgo.csv" "C:\Program Files\PostgreSQL\Import\Importados\cat_perfil_riesgo_%date:/=-%.csv"
move "C:\Program Files\PostgreSQL\Import\catalogo_activos.csv" "C:\Program Files\PostgreSQL\Import\Importados\catalogo_activos_%date:/=-%.csv"
move "C:\Program Files\PostgreSQL\Import\historico_aba_macroactivos.csv" "C:\Program Files\PostgreSQL\Import\Importados\historico_aba_macroactivos_%date:/=-%.csv"