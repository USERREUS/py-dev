# Python-Project
Little factory project

UPD!!!
Работает только все, что связано с LPH (подогреватель).

Собственно по организации совместной работы:
1. В главную ветку изменения не вносить.
2. После commitа изменений не сливать с главной веткой, только после обсуждения.
3. По возможности создавать и контролировать задачи в проектах.

PS. 1. В проектах есть готовый список текущих задач. Перед внесением изменений нужно создать задачу. После внесения изменений закрыть задачу с отсылкой на нее в комментарии. Такой порядок для облегчения контроля версий и поиска ошибок.
PS. 2. Перед внесением изменений создать новую ветку, в ней внести изменения и отправить запрос на слияние. После того, как изменения приняты в основной ветке, временную ветку удалить.

SQL Scripts:
-- Table: public.lph_inp_data

-- DROP TABLE IF EXISTS public.lph_inp_data;

CREATE TABLE IF NOT EXISTS public.lph_inp_data
(
    id integer NOT NULL DEFAULT nextval('"LPH_id_seq"'::regclass),
    heating_vapor_pressure numeric(20,4),
    heating_steam_temperature numeric(20,4),
    saturation_temperature numeric(20,4),
    heated_condensate_pressure numeric(20,4),
    condensate_temperature numeric(20,4),
    condensate_flow numeric(20,4),
    efficiency_factor numeric(3,2),
    CONSTRAINT "LPH_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.lph_inp_data
    OWNER to postgres;

COMMENT ON TABLE public.lph_inp_data
    IS 'Table for LPH input data';
    
-- Table: public.lph_out_data

-- DROP TABLE IF EXISTS public.lph_out_data;

CREATE TABLE IF NOT EXISTS public.lph_out_data
(
    id integer NOT NULL DEFAULT nextval('lph_out_data_id_seq'::regclass),
    steam_consumption numeric(20,4),
    parallel_pipes integer,
    heat_transfer_coefficient numeric(20,4),
    created_date timestamp(0) without time zone NOT NULL DEFAULT now(),
    CONSTRAINT lph_out_data_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.lph_out_data
    OWNER to postgres;

COMMENT ON TABLE public.lph_out_data
    IS 'Таблица для выходных данных функции подогревателя';
