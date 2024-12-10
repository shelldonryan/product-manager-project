--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

-- Started on 2024-12-08 19:32:05

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 841 (class 1247 OID 16410)
-- Name: usertype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.usertype AS ENUM (
    'standard',
    'admin'
);


ALTER TYPE public.usertype OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 16423)
-- Name: product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product (
    id text NOT NULL,
    name text NOT NULL,
    quantity integer DEFAULT 0 NOT NULL,
    price numeric DEFAULT 0.00 NOT NULL,
    userid text NOT NULL
);


ALTER TABLE public.product OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16415)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id text NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    type public.usertype DEFAULT 'standard'::public.usertype NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 4846 (class 0 OID 16423)
-- Dependencies: 216
-- Data for Name: product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.product (id, name, quantity, price, userid) FROM stdin;
1a976515-aba7-4882-9e79-386b77a5a679	pistola m1911 calibre .45	1	10396.84	393719d1-ea7a-47b3-9c11-c5ed8ec1c484
004c3019-da6f-416f-8f65-09a61db0edb8	Revólver RT 608 calibre .357	1	7780.41	393719d1-ea7a-47b3-9c11-c5ed8ec1c484
33998c27-1a39-454e-be42-e450282c179a	Fuzil parafal calibre 7,62mm	1	19900	393719d1-ea7a-47b3-9c11-c5ed8ec1c484
b030845d-e0c0-4ed1-bfba-542be24b3990	Banana	24	5.45	51160d33-4d87-4835-a5af-88362f4ab7a0
15a764f3-3a87-4854-97cd-2779d40b6522	Cenoura	20	3.43	51160d33-4d87-4835-a5af-88362f4ab7a0
ff9c3eed-8586-4811-ae7b-ab25714987e9	Macaxeira	42	10.33	51160d33-4d87-4835-a5af-88362f4ab7a0
b21ff282-dffd-4875-aeea-24283169ffc1	simara	1	124.34	anonymous
7524f1ce-0798-4953-a172-e27e36a066c9	xupa rola	3	40.78	53aeff92-294f-4062-8414-429531eb5f62
27421ff5-d6aa-4d4d-a74a-7d75680270ab	Carteira de motorista	10	1234.67	anonymous
66e00eaa-3811-4df2-b0f7-e3bd38479c3e	Espingarda cbc military calibre .12	1	6500	393719d1-ea7a-47b3-9c11-c5ed8ec1c484
\.


--
-- TOC entry 4845 (class 0 OID 16415)
-- Dependencies: 215
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password, type) FROM stdin;
393719d1-ea7a-47b3-9c11-c5ed8ec1c484	shelldonryan	scrypt:32768:8:1$JK5w6RqDNGoQ1ubT$c1be61fbeeaf7ad2fc5b9c3514ce2c9fbee842301a8d67126ab3e3e545ec7a089c61eaafcf2d34b093ad7a29dc73bff3f214a980382429dcb41b1aaeebdbe6b5	admin
51160d33-4d87-4835-a5af-88362f4ab7a0	tawan	scrypt:32768:8:1$cJjlvCka7pzcHzf7$b4abc1d3c233deb5f2e58e98278699bdc1f9e7076b86ec063bae09ff987aa194a8efdbbf115782bb4fcc15a15261abeb925b136970ae01b71b4bb50e3998000a	standard
anonymous	anonymous	kdajbakhfa	standard
53aeff92-294f-4062-8414-429531eb5f62	Marcela	scrypt:32768:8:1$mbQGXwfhtWtkKAY2$79b0bb89800a5cf470d599f92522cccb06c6c077bdd7cb871e9660730f319b67bd9991fbb3a34ee7ec84ba911cf1cf1678a6bdd54bf4a125ab42ad4490deca21	admin
80c7849b-dca5-4d7e-a9b4-7580cb7501c1	evertoncandido	scrypt:32768:8:1$7Q09mboVp1iporCo$c5d544e78d26bbfcdd3720198f804966b785fdf756ca4c214560e7ada06dcc1183c515a984cc67ed6bf70d89142fdb7e718a9f854918a8413ff46c760dbbef06	standard
\.


--
-- TOC entry 4700 (class 2606 OID 16431)
-- Name: product product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);


--
-- TOC entry 4698 (class 2606 OID 16422)
-- Name: users user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 4701 (class 2606 OID 16432)
-- Name: product product_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(id);


-- Completed on 2024-12-08 19:32:06

--
-- PostgreSQL database dump complete
--

