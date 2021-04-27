--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

-- Started on 2021-04-27 15:00:04

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 206 (class 1259 OID 25197)
-- Name: author; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.author (
    author_id integer NOT NULL,
    author_firstname character varying NOT NULL,
    author_lastname character varying NOT NULL
);


ALTER TABLE public.author OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 25195)
-- Name: author_author_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.author_author_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.author_author_id_seq OWNER TO postgres;

--
-- TOC entry 3040 (class 0 OID 0)
-- Dependencies: 205
-- Name: author_author_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.author_author_id_seq OWNED BY public.author.author_id;


--
-- TOC entry 208 (class 1259 OID 25208)
-- Name: book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book (
    book_id integer NOT NULL,
    author_id integer NOT NULL,
    booktitle character varying NOT NULL,
    floor character varying NOT NULL,
    book_publisher character varying NOT NULL,
    stock integer NOT NULL
);


ALTER TABLE public.book OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 25206)
-- Name: book_book_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.book_book_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.book_book_id_seq OWNER TO postgres;

--
-- TOC entry 3041 (class 0 OID 0)
-- Dependencies: 207
-- Name: book_book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.book_book_id_seq OWNED BY public.book.book_id;


--
-- TOC entry 204 (class 1259 OID 25186)
-- Name: borrower; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.borrower (
    borrower_id integer NOT NULL,
    returndate character varying NOT NULL,
    borrowerdate character varying NOT NULL,
    std_id bigint NOT NULL
);


ALTER TABLE public.borrower OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 25184)
-- Name: borrower_borrower_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.borrower_borrower_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.borrower_borrower_id_seq OWNER TO postgres;

--
-- TOC entry 3042 (class 0 OID 0)
-- Dependencies: 203
-- Name: borrower_borrower_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.borrower_borrower_id_seq OWNED BY public.borrower.borrower_id;


--
-- TOC entry 210 (class 1259 OID 25220)
-- Name: borrowers_books; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.borrowers_books (
    book_id integer NOT NULL,
    borrower_id integer NOT NULL
);


ALTER TABLE public.borrowers_books OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 25217)
-- Name: category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.category (
    book_id integer NOT NULL,
    cat_id integer NOT NULL
);


ALTER TABLE public.category OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 25167)
-- Name: categorylist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categorylist (
    cat_id integer NOT NULL,
    categoryname character varying NOT NULL,
    des character varying NOT NULL
);


ALTER TABLE public.categorylist OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 25165)
-- Name: categorylist_cat_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categorylist_cat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categorylist_cat_id_seq OWNER TO postgres;

--
-- TOC entry 3043 (class 0 OID 0)
-- Dependencies: 200
-- Name: categorylist_cat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categorylist_cat_id_seq OWNED BY public.categorylist.cat_id;


--
-- TOC entry 202 (class 1259 OID 25176)
-- Name: student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student (
    std_id bigint NOT NULL,
    std_firstname character varying NOT NULL,
    std_lastname character varying NOT NULL,
    std_major character varying NOT NULL,
    std_year character varying NOT NULL
);


ALTER TABLE public.student OWNER TO postgres;

--
-- TOC entry 2887 (class 2604 OID 25200)
-- Name: author author_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.author ALTER COLUMN author_id SET DEFAULT nextval('public.author_author_id_seq'::regclass);


--
-- TOC entry 2888 (class 2604 OID 25211)
-- Name: book book_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book ALTER COLUMN book_id SET DEFAULT nextval('public.book_book_id_seq'::regclass);


--
-- TOC entry 2886 (class 2604 OID 25189)
-- Name: borrower borrower_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.borrower ALTER COLUMN borrower_id SET DEFAULT nextval('public.borrower_borrower_id_seq'::regclass);


--
-- TOC entry 2885 (class 2604 OID 25170)
-- Name: categorylist cat_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorylist ALTER COLUMN cat_id SET DEFAULT nextval('public.categorylist_cat_id_seq'::regclass);


--
-- TOC entry 2896 (class 2606 OID 25205)
-- Name: author author_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.author
    ADD CONSTRAINT author_pk PRIMARY KEY (author_id);


--
-- TOC entry 2898 (class 2606 OID 25216)
-- Name: book book_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT book_pk PRIMARY KEY (book_id);


--
-- TOC entry 2894 (class 2606 OID 25194)
-- Name: borrower borrower_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.borrower
    ADD CONSTRAINT borrower_pk PRIMARY KEY (borrower_id);


--
-- TOC entry 2890 (class 2606 OID 25175)
-- Name: categorylist categorylist_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorylist
    ADD CONSTRAINT categorylist_pk PRIMARY KEY (cat_id);


--
-- TOC entry 2892 (class 2606 OID 25183)
-- Name: student student_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pk PRIMARY KEY (std_id);


--
-- TOC entry 2900 (class 2606 OID 25238)
-- Name: book author_book_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT author_book_fk FOREIGN KEY (author_id) REFERENCES public.author(author_id);


--
-- TOC entry 2904 (class 2606 OID 25243)
-- Name: borrowers_books book_borrowers_books_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.borrowers_books
    ADD CONSTRAINT book_borrowers_books_fk FOREIGN KEY (book_id) REFERENCES public.book(book_id);


--
-- TOC entry 2902 (class 2606 OID 25248)
-- Name: category book_category_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT book_category_fk FOREIGN KEY (book_id) REFERENCES public.book(book_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2903 (class 2606 OID 25233)
-- Name: borrowers_books borrower_borrowers_books_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.borrowers_books
    ADD CONSTRAINT borrower_borrowers_books_fk FOREIGN KEY (borrower_id) REFERENCES public.borrower(borrower_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2901 (class 2606 OID 25223)
-- Name: category category_list_category_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_list_category_fk FOREIGN KEY (cat_id) REFERENCES public.categorylist(cat_id);


--
-- TOC entry 2899 (class 2606 OID 25228)
-- Name: borrower student_borrower_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.borrower
    ADD CONSTRAINT student_borrower_fk FOREIGN KEY (std_id) REFERENCES public.student(std_id);

INSERT INTO author (author_firstname,author_lastname)values
('กรรวี','บุญชัย'),('ภาศกร','พาเจริญ'),('Henry','thoryT')

INSERT INTO categorylist(categoryname, des)VALUES 
('วิทยาศาสตร์','คอมพิวเตอร์'),
('วิทยาศาสตร์','ฟิสิกส์'),
('วิทยาศาสตร์','เคมี'),
('เทคโนโลยี','คอมพิวเตอร์'),
('วิทยาศาสตร์','การแพทย์')

INSERT INTO student
(std_id, std_firstname, std_lastname, std_major, std_year) VALUES

(62102010169,'ธนพัฒน์','เอี่ยมประเสริฐ','วิทยาการคอมพิวเตอร์','2'),
(62102010030,'อุกฤษฏ์','เกิดศิริ','วิทยาการคอมพิวเตอร์','2'),
(12345,'KAE','BANK','วิทยาการคอมพิวเตอร์','3')

INSERT INTO book(
author_id, booktitle, floor, book_publisher, stock) VALUES 

(3,'เคมี01','4','เคมีCompany',1),
(2,'ฟิสิกส์ 01','1','ฟิสิกส์ Company',1),
(1,'Database','5','Computer Company',2)

INSERT INTO category(book_id, cat_id)VALUES
(1,1),(2,2),(3,2)


INSERT INTO borrowers_books(book_id, borrower_id)VALUES (1, 83);










-- Completed on 2021-04-27 15:00:05

--
-- PostgreSQL database dump complete
--

