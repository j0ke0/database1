PGDMP      
                |            users    16.3    16.3 �    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    24594    users    DATABASE     |   CREATE DATABASE users WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_Australia.1252';
    DROP DATABASE users;
                postgres    false            �            1259    32824    har    TABLE     -  CREATE TABLE public.har (
    pk integer NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.har;
       public         heap    postgres    false            �            1259    32823    assembling_stage_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.assembling_stage_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.assembling_stage_pk_seq;
       public          postgres    false    220            �           0    0    assembling_stage_pk_seq    SEQUENCE OWNED BY     F   ALTER SEQUENCE public.assembling_stage_pk_seq OWNED BY public.har.pk;
          public          postgres    false    219                        1259    65832    bat    TABLE     -  CREATE TABLE public.bat (
    pk integer NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.bat;
       public         heap    postgres    false            �            1259    65831 
   bat_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.bat_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 !   DROP SEQUENCE public.bat_pk_seq;
       public          postgres    false    256            �           0    0 
   bat_pk_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE public.bat_pk_seq OWNED BY public.bat.pk;
          public          postgres    false    255            �            1259    32899    borrow_goods    TABLE     @  CREATE TABLE public.borrow_goods (
    id integer NOT NULL,
    logged_in_users character varying(255) NOT NULL,
    unit character varying(50) NOT NULL,
    location_area character varying(50),
    qty integer,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    work_order character varying(60)
);
     DROP TABLE public.borrow_goods;
       public         heap    postgres    false            �            1259    32898    borrow_return_id_seq    SEQUENCE     �   CREATE SEQUENCE public.borrow_return_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.borrow_return_id_seq;
       public          postgres    false    228            �           0    0    borrow_return_id_seq    SEQUENCE OWNED BY     L   ALTER SEQUENCE public.borrow_return_id_seq OWNED BY public.borrow_goods.id;
          public          postgres    false    227            �            1259    57536    con    TABLE     -  CREATE TABLE public.con (
    pk integer NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.con;
       public         heap    postgres    false            �            1259    57535 
   con_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.con_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 !   DROP SEQUENCE public.con_pk_seq;
       public          postgres    false    239            �           0    0 
   con_pk_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE public.con_pk_seq OWNED BY public.con.pk;
          public          postgres    false    238            �            1259    32814    cover    TABLE     /  CREATE TABLE public.cover (
    pk integer NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.cover;
       public         heap    postgres    false            �            1259    57552    doc    TABLE     -  CREATE TABLE public.doc (
    pk integer NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.doc;
       public         heap    postgres    false            �            1259    57551 
   doc_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.doc_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 !   DROP SEQUENCE public.doc_pk_seq;
       public          postgres    false    241            �           0    0 
   doc_pk_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE public.doc_pk_seq OWNED BY public.doc.pk;
          public          postgres    false    240            �            1259    32875    pcb    TABLE     -  CREATE TABLE public.pcb (
    pk integer NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.pcb;
       public         heap    postgres    false            �            1259    32874    engineering_stage_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.engineering_stage_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.engineering_stage_pk_seq;
       public          postgres    false    226            �           0    0    engineering_stage_pk_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.engineering_stage_pk_seq OWNED BY public.pcb.pk;
          public          postgres    false    225            �            1259    57603    final_scrap    TABLE     ?  CREATE TABLE public.final_scrap (
    id integer NOT NULL,
    logged_in_users character varying(255) NOT NULL,
    unit character varying(50) NOT NULL,
    location_area character varying(50),
    qty integer,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    work_order character varying(60)
);
    DROP TABLE public.final_scrap;
       public         heap    postgres    false            �            1259    57602    final_scrap_id_seq    SEQUENCE     �   CREATE SEQUENCE public.final_scrap_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.final_scrap_id_seq;
       public          postgres    false    244            �           0    0    final_scrap_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.final_scrap_id_seq OWNED BY public.final_scrap.id;
          public          postgres    false    243            �            1259    32907    finish_goods    TABLE     I  CREATE TABLE public.finish_goods (
    id integer NOT NULL,
    logged_in_users character varying(255) NOT NULL,
    unit character varying(50) NOT NULL,
    location_area character varying(50) NOT NULL,
    qty integer,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    work_order character varying(60)
);
     DROP TABLE public.finish_goods;
       public         heap    postgres    false            �            1259    57511    finish_goods_dropdown    TABLE     x   CREATE TABLE public.finish_goods_dropdown (
    pk integer NOT NULL,
    finish_goods text,
    logged_in_users text
);
 )   DROP TABLE public.finish_goods_dropdown;
       public         heap    postgres    false            �            1259    57510    finish_goods_dropdown_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.finish_goods_dropdown_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.finish_goods_dropdown_pk_seq;
       public          postgres    false    235            �           0    0    finish_goods_dropdown_pk_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.finish_goods_dropdown_pk_seq OWNED BY public.finish_goods_dropdown.pk;
          public          postgres    false    234            �            1259    32906    finish_goods_id_seq    SEQUENCE     �   CREATE SEQUENCE public.finish_goods_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.finish_goods_id_seq;
       public          postgres    false    230            �           0    0    finish_goods_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.finish_goods_id_seq OWNED BY public.finish_goods.id;
          public          postgres    false    229            �            1259    41086    history_gparts    TABLE     {  CREATE TABLE public.history_gparts (
    id integer DEFAULT nextval('public.borrow_return_id_seq'::regclass) NOT NULL,
    logged_in_users character varying(255) NOT NULL,
    unit character varying(50) NOT NULL,
    location_area character varying(50),
    qty integer,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    work_order character varying(60)
);
 "   DROP TABLE public.history_gparts;
       public         heap    postgres    false    227            �            1259    65824    hsg    TABLE     -  CREATE TABLE public.hsg (
    pk integer NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.hsg;
       public         heap    postgres    false            �            1259    65823 
   hsg_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.hsg_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 !   DROP SEQUENCE public.hsg_pk_seq;
       public          postgres    false    254            �           0    0 
   hsg_pk_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE public.hsg_pk_seq OWNED BY public.hsg.pk;
          public          postgres    false    253            �            1259    32813    inspection_stage_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.inspection_stage_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.inspection_stage_pk_seq;
       public          postgres    false    218            �           0    0    inspection_stage_pk_seq    SEQUENCE OWNED BY     H   ALTER SEQUENCE public.inspection_stage_pk_seq OWNED BY public.cover.pk;
          public          postgres    false    217            �            1259    57648    lab    TABLE     -  CREATE TABLE public.lab (
    pk integer NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.lab;
       public         heap    postgres    false            �            1259    57647 
   lab_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.lab_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 !   DROP SEQUENCE public.lab_pk_seq;
       public          postgres    false    252            �           0    0 
   lab_pk_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE public.lab_pk_seq OWNED BY public.lab.pk;
          public          postgres    false    251            �            1259    57640    mfp    TABLE     -  CREATE TABLE public.mfp (
    pk integer NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.mfp;
       public         heap    postgres    false            �            1259    57639 
   mfp_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.mfp_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 !   DROP SEQUENCE public.mfp_pk_seq;
       public          postgres    false    250            �           0    0 
   mfp_pk_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE public.mfp_pk_seq OWNED BY public.mfp.pk;
          public          postgres    false    249            �            1259    32864 
   quarantine    TABLE     4  CREATE TABLE public.quarantine (
    pk integer NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.quarantine;
       public         heap    postgres    false            �            1259    49308    raw_history    TABLE     q  CREATE TABLE public.raw_history (
    pk integer DEFAULT nextval('public.assembling_stage_pk_seq'::regclass) NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.raw_history;
       public         heap    postgres    false    219            �            1259    49313    raw_iqc_storage    TABLE     �  CREATE TABLE public.raw_iqc_storage (
    pk integer DEFAULT nextval('public.assembling_stage_pk_seq'::regclass) NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    good_parts boolean,
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    type character varying(10)
);
 #   DROP TABLE public.raw_iqc_storage;
       public         heap    postgres    false    219            �            1259    57520    raw_partnumbers    TABLE     �   CREATE TABLE public.raw_partnumbers (
    pk integer NOT NULL,
    partnumber character varying,
    logged_in_users character varying
);
 #   DROP TABLE public.raw_partnumbers;
       public         heap    postgres    false            �            1259    57519    raw_partnumbers_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.raw_partnumbers_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.raw_partnumbers_pk_seq;
       public          postgres    false    237            �           0    0    raw_partnumbers_pk_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.raw_partnumbers_pk_seq OWNED BY public.raw_partnumbers.pk;
          public          postgres    false    236            �            1259    57575 	   raw_scrap    TABLE     o  CREATE TABLE public.raw_scrap (
    pk integer DEFAULT nextval('public.assembling_stage_pk_seq'::regclass) NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.raw_scrap;
       public         heap    postgres    false    219            �            1259    57621    shipped_final    TABLE     
  CREATE TABLE public.shipped_final (
    pk integer NOT NULL,
    customer_name character varying,
    shipping_number character varying,
    logged_in_users character varying,
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    serials text
);
 !   DROP TABLE public.shipped_final;
       public         heap    postgres    false            �            1259    57620    shipped_final_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.shipped_final_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.shipped_final_pk_seq;
       public          postgres    false    246            �           0    0    shipped_final_pk_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.shipped_final_pk_seq OWNED BY public.shipped_final.pk;
          public          postgres    false    245            �            1259    32863    shipping_stage_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.shipping_stage_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.shipping_stage_pk_seq;
       public          postgres    false    224            �           0    0    shipping_stage_pk_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.shipping_stage_pk_seq OWNED BY public.quarantine.pk;
          public          postgres    false    223            �            1259    32834    wires    TABLE     /  CREATE TABLE public.wires (
    pk integer NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.wires;
       public         heap    postgres    false            �            1259    32833    soldering_stage_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.soldering_stage_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.soldering_stage_pk_seq;
       public          postgres    false    222            �           0    0    soldering_stage_pk_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.soldering_stage_pk_seq OWNED BY public.wires.pk;
          public          postgres    false    221            �            1259    57632    srck    TABLE     .  CREATE TABLE public.srck (
    pk integer NOT NULL,
    part_number character varying(50),
    purchase_number character varying(50),
    qty integer,
    storage character varying(100),
    logged_in_users character varying(50),
    time_stamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.srck;
       public         heap    postgres    false            �            1259    57631    srck_pk_seq    SEQUENCE     �   CREATE SEQUENCE public.srck_pk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.srck_pk_seq;
       public          postgres    false    248            �           0    0    srck_pk_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.srck_pk_seq OWNED BY public.srck.pk;
          public          postgres    false    247            �            1259    32789    users    TABLE     /  CREATE TABLE public.users (
    user_id integer NOT NULL,
    first_name character varying(50),
    last_name character varying(50),
    username character varying(50),
    password character varying(100),
    admin boolean,
    timestamp_column timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    32788    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public          postgres    false    216            �           0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public          postgres    false    215            �           2604    65835    bat pk    DEFAULT     `   ALTER TABLE ONLY public.bat ALTER COLUMN pk SET DEFAULT nextval('public.bat_pk_seq'::regclass);
 5   ALTER TABLE public.bat ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    256    255    256            �           2604    32902    borrow_goods id    DEFAULT     s   ALTER TABLE ONLY public.borrow_goods ALTER COLUMN id SET DEFAULT nextval('public.borrow_return_id_seq'::regclass);
 >   ALTER TABLE public.borrow_goods ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    228    227    228            �           2604    57539    con pk    DEFAULT     `   ALTER TABLE ONLY public.con ALTER COLUMN pk SET DEFAULT nextval('public.con_pk_seq'::regclass);
 5   ALTER TABLE public.con ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    238    239    239            �           2604    32817    cover pk    DEFAULT     o   ALTER TABLE ONLY public.cover ALTER COLUMN pk SET DEFAULT nextval('public.inspection_stage_pk_seq'::regclass);
 7   ALTER TABLE public.cover ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    218    217    218            �           2604    57555    doc pk    DEFAULT     `   ALTER TABLE ONLY public.doc ALTER COLUMN pk SET DEFAULT nextval('public.doc_pk_seq'::regclass);
 5   ALTER TABLE public.doc ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    241    240    241            �           2604    57606    final_scrap id    DEFAULT     p   ALTER TABLE ONLY public.final_scrap ALTER COLUMN id SET DEFAULT nextval('public.final_scrap_id_seq'::regclass);
 =   ALTER TABLE public.final_scrap ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    243    244    244            �           2604    32910    finish_goods id    DEFAULT     r   ALTER TABLE ONLY public.finish_goods ALTER COLUMN id SET DEFAULT nextval('public.finish_goods_id_seq'::regclass);
 >   ALTER TABLE public.finish_goods ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    230    229    230            �           2604    57514    finish_goods_dropdown pk    DEFAULT     �   ALTER TABLE ONLY public.finish_goods_dropdown ALTER COLUMN pk SET DEFAULT nextval('public.finish_goods_dropdown_pk_seq'::regclass);
 G   ALTER TABLE public.finish_goods_dropdown ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    234    235    235            �           2604    32827    har pk    DEFAULT     m   ALTER TABLE ONLY public.har ALTER COLUMN pk SET DEFAULT nextval('public.assembling_stage_pk_seq'::regclass);
 5   ALTER TABLE public.har ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    220    219    220            �           2604    65827    hsg pk    DEFAULT     `   ALTER TABLE ONLY public.hsg ALTER COLUMN pk SET DEFAULT nextval('public.hsg_pk_seq'::regclass);
 5   ALTER TABLE public.hsg ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    254    253    254            �           2604    57651    lab pk    DEFAULT     `   ALTER TABLE ONLY public.lab ALTER COLUMN pk SET DEFAULT nextval('public.lab_pk_seq'::regclass);
 5   ALTER TABLE public.lab ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    252    251    252            �           2604    57643    mfp pk    DEFAULT     `   ALTER TABLE ONLY public.mfp ALTER COLUMN pk SET DEFAULT nextval('public.mfp_pk_seq'::regclass);
 5   ALTER TABLE public.mfp ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    250    249    250            �           2604    32878    pcb pk    DEFAULT     n   ALTER TABLE ONLY public.pcb ALTER COLUMN pk SET DEFAULT nextval('public.engineering_stage_pk_seq'::regclass);
 5   ALTER TABLE public.pcb ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    226    225    226            �           2604    32867    quarantine pk    DEFAULT     r   ALTER TABLE ONLY public.quarantine ALTER COLUMN pk SET DEFAULT nextval('public.shipping_stage_pk_seq'::regclass);
 <   ALTER TABLE public.quarantine ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    224    223    224            �           2604    57523    raw_partnumbers pk    DEFAULT     x   ALTER TABLE ONLY public.raw_partnumbers ALTER COLUMN pk SET DEFAULT nextval('public.raw_partnumbers_pk_seq'::regclass);
 A   ALTER TABLE public.raw_partnumbers ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    236    237    237            �           2604    57624    shipped_final pk    DEFAULT     t   ALTER TABLE ONLY public.shipped_final ALTER COLUMN pk SET DEFAULT nextval('public.shipped_final_pk_seq'::regclass);
 ?   ALTER TABLE public.shipped_final ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    246    245    246            �           2604    57635    srck pk    DEFAULT     b   ALTER TABLE ONLY public.srck ALTER COLUMN pk SET DEFAULT nextval('public.srck_pk_seq'::regclass);
 6   ALTER TABLE public.srck ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    248    247    248            �           2604    32792    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public          postgres    false    216    215    216            �           2604    32837    wires pk    DEFAULT     n   ALTER TABLE ONLY public.wires ALTER COLUMN pk SET DEFAULT nextval('public.soldering_stage_pk_seq'::regclass);
 7   ALTER TABLE public.wires ALTER COLUMN pk DROP DEFAULT;
       public          postgres    false    221    222    222            �          0    65832    bat 
   TABLE DATA           j   COPY public.bat (pk, part_number, purchase_number, qty, storage, logged_in_users, time_stamp) FROM stdin;
    public          postgres    false    256   ��       �          0    32899    borrow_goods 
   TABLE DATA           n   COPY public.borrow_goods (id, logged_in_users, unit, location_area, qty, "timestamp", work_order) FROM stdin;
    public          postgres    false    228   �       �          0    57536    con 
   TABLE DATA           j   COPY public.con (pk, part_number, purchase_number, qty, storage, logged_in_users, time_stamp) FROM stdin;
    public          postgres    false    239   ̯       �          0    32814    cover 
   TABLE DATA           l   COPY public.cover (pk, part_number, purchase_number, qty, storage, logged_in_users, time_stamp) FROM stdin;
    public          postgres    false    218   �       �          0    57552    doc 
   TABLE DATA           j   COPY public.doc (pk, part_number, purchase_number, qty, storage, logged_in_users, time_stamp) FROM stdin;
    public          postgres    false    241   ��       �          0    57603    final_scrap 
   TABLE DATA           m   COPY public.final_scrap (id, logged_in_users, unit, location_area, qty, "timestamp", work_order) FROM stdin;
    public          postgres    false    244   �       �          0    32907    finish_goods 
   TABLE DATA           n   COPY public.finish_goods (id, logged_in_users, unit, location_area, qty, "timestamp", work_order) FROM stdin;
    public          postgres    false    230   �       �          0    57511    finish_goods_dropdown 
   TABLE DATA           R   COPY public.finish_goods_dropdown (pk, finish_goods, logged_in_users) FROM stdin;
    public          postgres    false    235   v�       �          0    32824    har 
   TABLE DATA           j   COPY public.har (pk, part_number, purchase_number, qty, storage, logged_in_users, time_stamp) FROM stdin;
    public          postgres    false    220   ��       �          0    41086    history_gparts 
   TABLE DATA           p   COPY public.history_gparts (id, logged_in_users, unit, location_area, qty, "timestamp", work_order) FROM stdin;
    public          postgres    false    231   I�       �          0    65824    hsg 
   TABLE DATA           j   COPY public.hsg (pk, part_number, purchase_number, qty, storage, logged_in_users, time_stamp) FROM stdin;
    public          postgres    false    254   G�       �          0    57648    lab 
   TABLE DATA           j   COPY public.lab (pk, part_number, purchase_number, qty, storage, logged_in_users, time_stamp) FROM stdin;
    public          postgres    false    252   ��       �          0    57640    mfp 
   TABLE DATA           j   COPY public.mfp (pk, part_number, purchase_number, qty, storage, logged_in_users, time_stamp) FROM stdin;
    public          postgres    false    250   (�       �          0    32875    pcb 
   TABLE DATA           j   COPY public.pcb (pk, part_number, purchase_number, qty, storage, logged_in_users, time_stamp) FROM stdin;
    public          postgres    false    226   ��       �          0    32864 
   quarantine 
   TABLE DATA           q   COPY public.quarantine (pk, part_number, purchase_number, qty, storage, logged_in_users, time_stamp) FROM stdin;
    public          postgres    false    224   Y�       �          0    49308    raw_history 
   TABLE DATA           r   COPY public.raw_history (pk, part_number, purchase_number, qty, storage, logged_in_users, time_stamp) FROM stdin;
    public          postgres    false    232   ��       �          0    49313    raw_iqc_storage 
   TABLE DATA           �   COPY public.raw_iqc_storage (pk, part_number, purchase_number, qty, storage, good_parts, logged_in_users, time_stamp, type) FROM stdin;
    public          postgres    false    233   x�       �          0    57520    raw_partnumbers 
   TABLE DATA           J   COPY public.raw_partnumbers (pk, partnumber, logged_in_users) FROM stdin;
    public          postgres    false    237   ��       �          0    57575 	   raw_scrap 
   TABLE DATA           p   COPY public.raw_scrap (pk, part_number, purchase_number, qty, storage, logged_in_users, time_stamp) FROM stdin;
    public          postgres    false    242   !�       �          0    57621    shipped_final 
   TABLE DATA           q   COPY public.shipped_final (pk, customer_name, shipping_number, logged_in_users, time_stamp, serials) FROM stdin;
    public          postgres    false    246   ��       �          0    57632    srck 
   TABLE DATA           k   COPY public.srck (pk, part_number, purchase_number, qty, storage, logged_in_users, time_stamp) FROM stdin;
    public          postgres    false    248   7�       �          0    32789    users 
   TABLE DATA           l   COPY public.users (user_id, first_name, last_name, username, password, admin, timestamp_column) FROM stdin;
    public          postgres    false    216   T�       �          0    32834    wires 
   TABLE DATA           l   COPY public.wires (pk, part_number, purchase_number, qty, storage, logged_in_users, time_stamp) FROM stdin;
    public          postgres    false    222   ��       �           0    0    assembling_stage_pk_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.assembling_stage_pk_seq', 299, true);
          public          postgres    false    219            �           0    0 
   bat_pk_seq    SEQUENCE SET     8   SELECT pg_catalog.setval('public.bat_pk_seq', 1, true);
          public          postgres    false    255            �           0    0    borrow_return_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.borrow_return_id_seq', 170, true);
          public          postgres    false    227            �           0    0 
   con_pk_seq    SEQUENCE SET     8   SELECT pg_catalog.setval('public.con_pk_seq', 1, true);
          public          postgres    false    238            �           0    0 
   doc_pk_seq    SEQUENCE SET     8   SELECT pg_catalog.setval('public.doc_pk_seq', 1, true);
          public          postgres    false    240            �           0    0    engineering_stage_pk_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.engineering_stage_pk_seq', 13, true);
          public          postgres    false    225            �           0    0    final_scrap_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.final_scrap_id_seq', 8, true);
          public          postgres    false    243            �           0    0    finish_goods_dropdown_pk_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.finish_goods_dropdown_pk_seq', 10, true);
          public          postgres    false    234            �           0    0    finish_goods_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.finish_goods_id_seq', 102, true);
          public          postgres    false    229            �           0    0 
   hsg_pk_seq    SEQUENCE SET     8   SELECT pg_catalog.setval('public.hsg_pk_seq', 1, true);
          public          postgres    false    253            �           0    0    inspection_stage_pk_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.inspection_stage_pk_seq', 30, true);
          public          postgres    false    217            �           0    0 
   lab_pk_seq    SEQUENCE SET     8   SELECT pg_catalog.setval('public.lab_pk_seq', 2, true);
          public          postgres    false    251            �           0    0 
   mfp_pk_seq    SEQUENCE SET     8   SELECT pg_catalog.setval('public.mfp_pk_seq', 1, true);
          public          postgres    false    249            �           0    0    raw_partnumbers_pk_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.raw_partnumbers_pk_seq', 23, true);
          public          postgres    false    236            �           0    0    shipped_final_pk_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.shipped_final_pk_seq', 61, true);
          public          postgres    false    245            �           0    0    shipping_stage_pk_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.shipping_stage_pk_seq', 24, true);
          public          postgres    false    223            �           0    0    soldering_stage_pk_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.soldering_stage_pk_seq', 8, true);
          public          postgres    false    221            �           0    0    srck_pk_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.srck_pk_seq', 1, false);
          public          postgres    false    247            �           0    0    users_user_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.users_user_id_seq', 18, true);
          public          postgres    false    215            �           2606    32832    har assembling_stage_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.har
    ADD CONSTRAINT assembling_stage_pkey PRIMARY KEY (pk);
 C   ALTER TABLE ONLY public.har DROP CONSTRAINT assembling_stage_pkey;
       public            postgres    false    220                       2606    65838    bat bat_pkey 
   CONSTRAINT     J   ALTER TABLE ONLY public.bat
    ADD CONSTRAINT bat_pkey PRIMARY KEY (pk);
 6   ALTER TABLE ONLY public.bat DROP CONSTRAINT bat_pkey;
       public            postgres    false    256            �           2606    32905    borrow_goods borrow_return_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.borrow_goods
    ADD CONSTRAINT borrow_return_pkey PRIMARY KEY (id);
 I   ALTER TABLE ONLY public.borrow_goods DROP CONSTRAINT borrow_return_pkey;
       public            postgres    false    228                       2606    57542    con con_pkey 
   CONSTRAINT     J   ALTER TABLE ONLY public.con
    ADD CONSTRAINT con_pkey PRIMARY KEY (pk);
 6   ALTER TABLE ONLY public.con DROP CONSTRAINT con_pkey;
       public            postgres    false    239                       2606    57558    doc doc_pkey 
   CONSTRAINT     J   ALTER TABLE ONLY public.doc
    ADD CONSTRAINT doc_pkey PRIMARY KEY (pk);
 6   ALTER TABLE ONLY public.doc DROP CONSTRAINT doc_pkey;
       public            postgres    false    241            �           2606    32883    pcb engineering_stage_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.pcb
    ADD CONSTRAINT engineering_stage_pkey PRIMARY KEY (pk);
 D   ALTER TABLE ONLY public.pcb DROP CONSTRAINT engineering_stage_pkey;
       public            postgres    false    226                       2606    57609    final_scrap final_scrap_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.final_scrap
    ADD CONSTRAINT final_scrap_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.final_scrap DROP CONSTRAINT final_scrap_pkey;
       public            postgres    false    244            �           2606    57518 0   finish_goods_dropdown finish_goods_dropdown_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY public.finish_goods_dropdown
    ADD CONSTRAINT finish_goods_dropdown_pkey PRIMARY KEY (pk);
 Z   ALTER TABLE ONLY public.finish_goods_dropdown DROP CONSTRAINT finish_goods_dropdown_pkey;
       public            postgres    false    235            �           2606    32913    finish_goods finish_goods_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.finish_goods
    ADD CONSTRAINT finish_goods_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.finish_goods DROP CONSTRAINT finish_goods_pkey;
       public            postgres    false    230            �           2606    41092 %   history_gparts history_goodparts_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.history_gparts
    ADD CONSTRAINT history_goodparts_pkey PRIMARY KEY (id);
 O   ALTER TABLE ONLY public.history_gparts DROP CONSTRAINT history_goodparts_pkey;
       public            postgres    false    231                       2606    65830    hsg hsg_pkey 
   CONSTRAINT     J   ALTER TABLE ONLY public.hsg
    ADD CONSTRAINT hsg_pkey PRIMARY KEY (pk);
 6   ALTER TABLE ONLY public.hsg DROP CONSTRAINT hsg_pkey;
       public            postgres    false    254            �           2606    32822    cover inspection_stage_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.cover
    ADD CONSTRAINT inspection_stage_pkey PRIMARY KEY (pk);
 E   ALTER TABLE ONLY public.cover DROP CONSTRAINT inspection_stage_pkey;
       public            postgres    false    218                       2606    57654    lab lab_pkey 
   CONSTRAINT     J   ALTER TABLE ONLY public.lab
    ADD CONSTRAINT lab_pkey PRIMARY KEY (pk);
 6   ALTER TABLE ONLY public.lab DROP CONSTRAINT lab_pkey;
       public            postgres    false    252                       2606    57646    mfp mfp_pkey 
   CONSTRAINT     J   ALTER TABLE ONLY public.mfp
    ADD CONSTRAINT mfp_pkey PRIMARY KEY (pk);
 6   ALTER TABLE ONLY public.mfp DROP CONSTRAINT mfp_pkey;
       public            postgres    false    250            �           2606    57527 $   raw_partnumbers raw_partnumbers_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.raw_partnumbers
    ADD CONSTRAINT raw_partnumbers_pkey PRIMARY KEY (pk);
 N   ALTER TABLE ONLY public.raw_partnumbers DROP CONSTRAINT raw_partnumbers_pkey;
       public            postgres    false    237                       2606    57629     shipped_final shipped_final_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.shipped_final
    ADD CONSTRAINT shipped_final_pkey PRIMARY KEY (pk);
 J   ALTER TABLE ONLY public.shipped_final DROP CONSTRAINT shipped_final_pkey;
       public            postgres    false    246            �           2606    32872    quarantine shipping_stage_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.quarantine
    ADD CONSTRAINT shipping_stage_pkey PRIMARY KEY (pk);
 H   ALTER TABLE ONLY public.quarantine DROP CONSTRAINT shipping_stage_pkey;
       public            postgres    false    224            �           2606    32842    wires soldering_stage_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.wires
    ADD CONSTRAINT soldering_stage_pkey PRIMARY KEY (pk);
 D   ALTER TABLE ONLY public.wires DROP CONSTRAINT soldering_stage_pkey;
       public            postgres    false    222            	           2606    57638    srck srck_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.srck
    ADD CONSTRAINT srck_pkey PRIMARY KEY (pk);
 8   ALTER TABLE ONLY public.srck DROP CONSTRAINT srck_pkey;
       public            postgres    false    248            �           2606    32794    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    216            �           2606    32796    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public            postgres    false    216            �           2606    41113    finish_goods work_order_unique 
   CONSTRAINT     _   ALTER TABLE ONLY public.finish_goods
    ADD CONSTRAINT work_order_unique UNIQUE (work_order);
 H   ALTER TABLE ONLY public.finish_goods DROP CONSTRAINT work_order_unique;
       public            postgres    false    230            �   R   x�3�tr153��742�"�@g� WGCN���J��Ģ�̼�*N##]3]C3Cs+#S+#=3cSCK�=... ��k      �   �   x���=�1�:��Ő���t
��r"�Z����7{X�,L�O�������ˡ=��O�Y�:���f`�`@��8v�E�|���LB6� ��7m���0+��,��
4�")�O�q\�Y���Bd d�F�����p:��4�j���QC�Y2f�d�_��y�9[����1�I��jY>E |5UrO������[k��	u�      �      x������ � �      �   �   x�u�M
�0�ur�\�!���.�
Ek��Pp�AZ�n���K�0���Iќ�P�C�4 9�����t������6��U&L&$��x�8P�Qt���lB����0�ybu|�+B�����P�J���R�2�����3�=(�霳��)�_��39      �   N   x�3�t�w65��742��tr�44���ϩTp-.H,J��K��4202�50�54Q00�20�21�374524����� Ue�      �     x���KK1�u�+�����k�� R��͠C�-���fꈥ�B����̹As�|�p�n����?�զsd�Nؐ! �@�@vQ��f�x�����fO�n� �!�ra�t.PT|B�4�д�es�-��n�t�n���1ܧCa�I�~���]��V��cA�������,buϞM�.��;XD�.�Q"Ii�]�"6�z��[��}�
���1��ČL^�D6����s���a�$�\M�y,9�<�/�M*�t���?6xyN?(��uBl����Z���      �   H  x�m��K1���_�wi��|Nn��P�*���݃�Uj=�_�߸�e/���潇@������|}�lV���W=��q���vҢ"�� 04ೳ��8O)�$�>x^���P8#DR�8���-d�&9���9H�5�>g~}+gj4\�
���x���9�����b8�.��q�!�^��C�cu����(����(�B�3ˡP���.��6��[<y��Ֆ�E��L;c$�Dg9���y�F�*���E�@�����n��f��=5�6d��d���̻��fݭ�e�\���[�WJ��7c���7 I~���F��i³�Z��3��      �   3   x�3��5���ϩTp-.H,J��K���r��64 )������ lv�      �   �   x�=��
�0����)�s��D�S�k7��"H+�}z�9���AV�[_ :� �v��}��L�?�gG�������-�%Su��'D��ZJ�L�@�8�_~;?��ކ��G��̚ق% �]�s�5 Z      �   �  x���KkA�ϳ�b�F�t�t��&E�؉#� a-��Hf�`�_���];�N�����d����o}��y٬��u7��	Щ�x�
P�E?�<���Kف�	�6���PA_�f�������B�e��c8�����m��zH��w�:�t� ��ͺ��^����]m��u;�t�dA�vz)%=����u������1[��z����f��|�oQMcP�2�2~H��w^d�2t&s��!GDx�ѓM�l^d��ko+���[�0�&R�C�mo䵏�l�mi|�����S9#!���ph�Ƀ����0Eu&&S��&�#�2zj�����N�A23���>�[P��2���
v��� IL(�����w�򹋒�T��ݾ�"��(�~kIU���yb��I�$*1pw����A��G!��<x\�t�]��S�_o>�ɽ�k~9��h0kK�K�#�$�����TU���M|      �   L   x�3��v761��72�44�4� ~�9�
���E)�y�U�FF&�f��f
fV��V�fz�&�\1z\\\ L��      �   u   x���A
�0����@C��NR�S�)�ҍ���h�+=���=�~��h2TPԺ+I���)��2_���#��[X�>��}4��w,�[�iB�r<m��!�%��AW��s_��!f      �   N   x�3��u042��7���44�4t1���ϩTp-.H,J��K��4202�50�54U00�24�21�3�0�4������� Ny�      �   �   x�}��j�P���O��2�I���ߢ�(wn����ѧ�Ԉ]Yfw>α����(��H��cٴT�������c�读@@2�r\ e����%" :``�8tM��{���Y4U�ZkD~Uh~��:�f�*V[��x�u�=~ߊ��ԟ�_���O�5s�3W&VF�g��^�wL��V��fW�4��c���L�      �   W   x�32�tr15��726�4262��uq�Qp�0���ϩTp-.H,J��K��4202�50�54U0��22�25�357053����� �L6      �   �  x����j�@���)�$��;��ɉ�8�颛�R����Pڧ���?-ViAH��t��$�i#�H�uߵ��� ���j^I������^��l���@�:W6+�-�/
T����cQ�q�kY����	��.��J�#�0iŬZ�H8N���)��Ȥ+H)�RJ�H����%�BtL�R���f�7|�C�F>���)ݔ�:iHu��o�ѓ�MI\���h�A,���2�9�˧����k�
0s �)��K��a
����ϭ몾<=��%؂EˢO��y�/�_g"���!h�HsB�_=�hRO�F���o���?/�OC|y�qjy�%�,�N�4�����9�M�7���;9����ɱ��Bq7_W�g��������pq���k>7b��ʻ�,'q%���*d�,�~ ��      �      x������ � �      �   |   x�3��p��N�KOO,�W�M,I�2��rF5�t�s���ϩTp-.H,J��K��2������t�w�Pih���)n���)l����!ld��㈩�Ȑ�#�Sؘ��1C8F��� 6�M~      �   d  x����N�0�s�y�E�c'un�V�$ؠ-p�$N���0!4*�J��S~�&1g�9R0g��D2��ۦvd6Oo�y}�y���{7�3�3P��f /U!�)����	'$�L�%R$5�����6}}��q3	���#k�dQ�Yl/��3�@�כ���H����C�b�/��f�:?��(Y�qB��O_����QH�*�z�q0�?����E��(�6c�r&��I�L�%z�2�����6cs�L*2&/ 2$��Z�M�u��fٕo"�Ȕ5���hI�З��kE%Ѳ;�D����Үs<�n��o�n�w]�aU���(V���k0�+(��JtX����"���Z���      �   �  x���͎�0���S�y���uq��v�U@�� �	�<=c���v;q���|��2@T�*zX����~�������_�2��w�� �ָBc��QC9(�t�}<�N<o��O˙90J˝�Fߣ�V��8�!*EX�b�)w�)�bؿ����.ﻓ�x�گ!^��8�i&YGө�61�q�t�"4������q��Dv�N��EӢl@K�ؘӘ�>�cʩ��?��!RKQ��6�1]�#uj�c��b��Y�x8�| ����H�CHQ[�3;啻��m�oM�����(�Y.����*bs�`��0����:���r���DppD������t�O2��Z�.A$J�B�b����T��Y��NX�nN��DZ�V�F��`KHYqa� ^Ap�n�(���pCQ�%YϨב�Ry�$MǕW�7ԫ`�	&�,���ʏ=N��q�#��}���Gl��8%��qN�
y^A	-�F9��Q�#9�+6΍cwQQz�(��l|��]$�8���vr��8u���+�T]&�8:��*����'VS��lU}|)�����mM��Q{�Y%:ǵ��n��o���V��7PYÖ�<-{�f:MǽxLOH<*���q�As�#)���Z��j�@#��b�ǆs���0      �      x������ � �      �   C  x���?o�0����+w���S�h�Z�F$qE�*��kPZ�Ƀ�{��|g$x�����ܶ�߰����η�y��m����,��qեO�JI�R5�<A2�"N:�btn<]��އ��inH�y.�Ĝ	�;�D���^+J�W0uPف{�I*MZD2.PZ3T�dN0���&�c�
=���h�a�JI�$��v��� �������^�:X��SϠ"5Br$MA�sP@ÉE a�0Rq�I1���ws�)�i8v&���\(�d⚦G���UE�4'%
-氨||z_U�.Ԯ�<�P���
�*~�%g�� ��'      �   �   x����j�0E��W�b�!K�vjc�)i���`�1�`�]�__9��RZ��à(י��b"���3�4t]{���������� IʖJe0vfOm�G�E0�����u+���qP����nĶ���L�`T˰�[V�<�&L���\�����g��g��b��p�P���Ǿ��r�(��$�2N�+G�C��궇V���א01d$݌��!F���^�M�o��Qh'
S�0u��%�R~�2{�     