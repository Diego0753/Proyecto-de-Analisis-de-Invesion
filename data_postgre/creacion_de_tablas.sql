BEGIN;


CREATE TABLE public.historico_aba_macroactivos
(
    ingestion_year character varying(200) COLLATE pg_catalog."default",
    ingestion_month character varying(2) COLLATE pg_catalog."default",
    ingestion_day character varying(2) COLLATE pg_catalog."default",
    id_sistema_cliente text COLLATE pg_catalog."default",
    macroactivo character varying(20) COLLATE pg_catalog."default",
    cod_activo character varying(20) COLLATE pg_catalog."default" NOT NULL,
    aba character varying(100) COLLATE pg_catalog."default",
    cod_perfil_riesgo character varying(10) COLLATE pg_catalog."default" NOT NULL,
    cod_banca character varying(10) COLLATE pg_catalog."default" NOT NULL,
    year character varying(4) COLLATE pg_catalog."default",
    month character varying(2) COLLATE pg_catalog."default"
);

CREATE TABLE public.catalogo_activos
(
    activo character varying(100) COLLATE pg_catalog."default",
    cod_activo character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT catalogo_activos_pkey PRIMARY KEY (cod_activo)
);

CREATE TABLE public.catalogo_banca
(
    cod_banca character varying(10) COLLATE pg_catalog."default" NOT NULL,
    banca character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT cat_banca_pkey PRIMARY KEY (cod_banca)
);

CREATE TABLE public.cat_perfil_riesgo
(
    cod_perfil_riesgo character varying(10) COLLATE pg_catalog."default" NOT NULL,
    perfil_riesgo character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT cat_perfil_riesgo_pkey PRIMARY KEY (cod_perfil_riesgo)
);

ALTER TABLE public.historico_aba_macroactivos
    ADD CONSTRAINT cod_activo FOREIGN KEY (cod_activo)
    REFERENCES public.catalogo_activos (cod_activo) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE public.historico_aba_macroactivos
    ADD CONSTRAINT cod_banca FOREIGN KEY (cod_banca)
    REFERENCES public.catalogo_banca (cod_banca) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE public.historico_aba_macroactivos
    ADD CONSTRAINT cod_perfil_riesgo FOREIGN KEY (cod_perfil_riesgo)
    REFERENCES public.cat_perfil_riesgo (cod_perfil_riesgo) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;